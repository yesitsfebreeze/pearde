#!/usr/bin/env python3
"""The machine frontier: every board this daemon watches merged into one
ordered list, and the concurrency a dispatch across it would use.

Discovered by `resources/pearde.py` through its `COMMANDS` dict, so it runs
from any directory — there need be no board above the cwd. The default mode is
read-only: it prints and moves nothing. `dispatch` is the one verb that moves,
and it lives in @resources/board/dispatch.py, imported only when asked for.

    pearde machine              the merged order, printed
    pearde machine boards       what the daemon watches
    pearde machine slots        the concurrency and its reading
    pearde machine progress     one progress line over the set
    pearde machine groups       the labels the watched boards declare
    pearde machine --json       the same as data
    pearde machine dispatch     the frontier run down to nothing

A group is a label a board writes on itself (`groups:` in its own
settings.md), and any of the above takes one as a bare word: `pearde machine
work`, `pearde machine work slots`, `pearde machine work dispatch`. Same read,
fewer boards. Nothing here keeps the list.
"""
import json
import os
import time
import re
import subprocess
import sys

# this file's own directory IS the board/ dir — the shipped code is imported
# from beside it, never from a path written down
BOARD = HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(BOARD))
sys.path.insert(0, BOARD)
import plan as planlib  # noqa: E402
import serve as servelib  # noqa: E402

# ── 0. the slot meter ────────────────────────────────────────────────────────
# "Dynamically by load, so we use 80% power of the machine" — the answer to Q1.
#
# Measured on this machine 2026-09-02 before any of this was written, because
# the instrument was the whole question (scratchpad meter/RESULTS.md):
#
#   local CPU     5 concurrent workers peaked at 160% of 1000% available
#                 → 0.32 core each. 80% of a 10-core machine is 800%, so a
#                   CPU-derived cap alone permits ~25, and at mean cost ~270.
#   memory        session RSS 2.28 → 2.80 GiB over the same burst
#                 → ~104 MiB each. 80% of 32 GiB permits ~180.
#   processes     top-level `claude` count did not move, 6 → 7. A subagent is
#                 a request stream inside a session, not an OS process.
#   latency       identical trivial prompt: 1 concurrent 1579 ms, 12 concurrent
#                 mean 1646 ms (stdev 104). +4% for 12x the work, no knee.
#
# So NO local meter binds at a number a person would choose: 80% of this
# machine is 25-270 workers, which is the fifty-at-once the user declined,
# reached silently. The machine is not what a worker consumes — the model
# service is, and this process cannot read that.
#
# Hence a composite, which is what the load answer honestly supports:
#   floor    1     always make progress
#   ceiling  12    the highest concurrency measured to cost nothing (+4%), and
#                  the board's own escalation continued — 3 plain, 6 master
#                  (@references/settings.md), 12 for the whole machine
#   between  the load-derived value, so a machine already busy with somebody
#            else's build drops the count instead of fighting it
#
# The ceiling is what protects the user; load only ever lowers it.
#
# `machine-ceiling: 0` lifts it, and reads as unlimited the way `workers: 0`
# and `pipeline: 0` already do on this board — the load-derived number with
# SLOT_FLOOR under it and nothing above it. The DEFAULT does not move: an
# untouched board still gets the measured 12. Only an explicit 0 lifts it,
# because unlimited is a thing a person chooses, never a thing they inherit.
#
# Under an unlimited ceiling `SLOT_CEILING` is 0, so every clamp goes through
# `_clamp` and every reading through `_ceiling_label`. A bare
# `min(SLOT_CEILING, n)` would pin the count to zero and dispatch nothing —
# the exact inversion of what the setting asks for.
TARGET = 0.80          # "80% power of the machine"
CORE_PER_WORKER = 0.32   # measured, peak
MIB_PER_WORKER = 104.0   # measured
SLOT_FLOOR = 1
CEILING_DEFAULT = 12
UNCAPPED = 0           # what `machine-ceiling: 0` resolves to — no ceiling


def board_at(start=None):
    """The board at or above `start`, or None. The same walk `pearde` does,
    written here because this command must also run where there is none."""
    d = os.path.abspath(start or os.getcwd())
    while True:
        cand = os.path.join(d, planlib.BOARD_DIR)
        if os.path.isdir(cand):
            return cand
        nxt = os.path.dirname(d)
        if nxt == d:
            return None
        d = nxt


def ceiling(board=None):
    """`machine-ceiling` — the highest concurrency this command will name.

    12 is not a limit that was found, it is the highest concurrency that was
    MEASURED to cost nothing (12 at once, +4% mean latency, no knee). A number
    like that buried in the source is a number nobody can move, so it is a
    settings key: `machine-ceiling` in the board at the cwd, read here and by
    nothing else. There is no machine-wide settings file — the board a person
    is standing in is the only one they addressed — so away from any board the
    measured default stands.

    `0` is unlimited, the same word `workers: 0` and `pipeline: 0` already
    say here. `1`-`64` is that number. Absent, unparseable or out of that
    band: 12 stands — the default is what an untouched board gets, and only
    an explicit 0 lifts the cap."""
    b = board if board is not None else board_at()
    if not b:
        return CEILING_DEFAULT
    try:
        v = planlib.board_settings(b).get("machine-ceiling")
        n = int(str(v).strip())
    except (TypeError, ValueError, OSError):
        return CEILING_DEFAULT
    if n == 0:
        return UNCAPPED
    return n if 1 <= n <= 64 else CEILING_DEFAULT


def _clamp(n):
    """A load-derived count brought inside the band. The floor always
    applies; the ceiling only where there is one."""
    n = int(n)
    if SLOT_CEILING == UNCAPPED:
        return max(SLOT_FLOOR, n)
    return max(SLOT_FLOOR, min(SLOT_CEILING, n))


def _ceiling_label():
    """What the ceiling prints as. `plan.workers_label` is the board's own
    answer — `∞`, never a bare `0`, which reads as "no slots" and means the
    opposite."""
    return planlib.workers_label(SLOT_CEILING)


# Resolved once, at import, off the cwd this process was started in — the cwd
# does not move inside one run, and every reading printed below names it.
SLOT_CEILING = ceiling()


def _busy_now(seconds=1):
    """(busy fraction of all cores, cost in seconds) — an INSTANTANEOUS
    reading, or (None, cost) where there is none.

    `load1` is a one-minute average and it lags in both directions: measured
    2026-09-02, six busy cores moved it 2.14 → 3.31 in 20 s, and after a
    12-core burn ended it read 20.58 and stayed high for minutes. A meter on
    load1 alone therefore stays throttled long after the machine is free.
    This is the second opinion, and it costs a second of wall clock, so it is
    only ever asked when load1 is about to drive the count to the floor.

    The residual weakness, stated rather than hidden: this is a ONE-SECOND
    window, so a machine that is bursty rather than busy can be read either
    way — the same machine sampled twice a second apart can answer 5% and
    95%. `SLOT_FLOOR = 1` is what makes that safe: the worst reading this
    can produce still dispatches one job, so a misread costs throughput for
    one run and never progress."""
    t0 = time.time()
    try:
        if sys.platform == "darwin":
            out = subprocess.run(["top", "-l", "2", "-n", "0",
                                  "-s", str(seconds)],
                                 check=True, capture_output=True,
                                 text=True).stdout
            ms = re.findall(r"CPU usage:\s*([\d.]+)% user,\s*"
                            r"([\d.]+)% sys,\s*([\d.]+)% idle", out)
            if ms:
                return 1.0 - float(ms[-1][2]) / 100.0, time.time() - t0
        else:
            def ticks():
                with open("/proc/stat", encoding="utf-8") as fh:
                    f = [int(x) for x in fh.readline().split()[1:]]
                return sum(f), f[3] + (f[4] if len(f) > 4 else 0)
            a = ticks()
            time.sleep(seconds)
            b = ticks()
            dt, di = b[0] - a[0], b[1] - a[1]
            if dt > 0:
                return 1.0 - di / dt, time.time() - t0
    except Exception:
        pass
    return None, time.time() - t0


def _machine():
    """(cores, total MiB, load1, used MiB) — None for what it cannot read, and
    the caller falls back to the ceiling rather than guessing. darwin reads
    sysctl and vm_stat; every other posix reads /proc."""
    def sysctl(name, cast=int):
        try:
            return cast(subprocess.run(["sysctl", "-n", name], check=True,
                        capture_output=True, text=True).stdout.strip())
        except Exception:
            return None
    if sys.platform != "darwin":
        return _machine_proc()
    cores = sysctl("hw.ncpu")
    total = sysctl("hw.memsize")
    total = total / 1048576.0 if total else None
    load1 = None
    try:
        load1 = os.getloadavg()[0]
    except (OSError, AttributeError):
        pass
    used = None
    if total:
        try:
            out = subprocess.run(["vm_stat"], check=True, capture_output=True,
                                 text=True).stdout
            page = int(re.search(r"page size of (\d+)", out).group(1))
            # macOS "free" is not "available": inactive and purgeable pages
            # are reclaimable on demand, and counting only `free` reported
            # 31.2 of 32 GiB used on an idle machine, which drove the meter
            # to its floor. free + inactive + speculative + purgeable.
            free = sum(int(m) for m in re.findall(
                r"Pages (?:free|inactive|speculative|purgeable):\s+(\d+)",
                out))
            used = total - (free * page / 1048576.0)
        except Exception:
            used = None
    return cores, total, load1, used


def _machine_proc(root="/"):
    """The same four numbers off /proc, for a board on linux. `MemAvailable`
    is the kernel's own answer to the question `vm_stat` needs four counters
    to approximate — free plus what is reclaimable without swapping.

    `root` is for the test that proves this branch parses without a linux to
    run it on: point it at a directory holding `proc/loadavg` and
    `proc/meminfo` and the same code reads them."""
    cores = total = load1 = used = None
    try:
        cores = os.cpu_count()
    except Exception:
        pass
    try:
        if root == "/":
            load1 = os.getloadavg()[0]
        else:
            with open(os.path.join(root, "proc/loadavg"),
                      encoding="utf-8") as fh:
                load1 = float(fh.read().split()[0])
    except (OSError, AttributeError, ValueError, IndexError):
        pass
    try:
        mem = {}
        with open(os.path.join(root, "proc/meminfo"), encoding="utf-8") as fh:
            for line in fh:
                k, _, v = line.partition(":")
                mem[k] = float(v.split()[0]) / 1024.0     # kB → MiB
        total = mem.get("MemTotal")
        avail = mem.get("MemAvailable")
        if total is not None and avail is not None:
            used = total - avail
    except Exception:
        pass
    return cores, total, load1, used


def slots():
    """(n, reading) — how many run at once, and the sentence that says why.

    A cap nobody can see is a cap nobody can debug, so the reading is printed
    beside the order every time (contract step 4)."""
    cores, total, load1, used = _machine()
    bits, cands = [], []
    if cores and load1 is not None:
        free_cores = TARGET * cores - load1
        n = free_cores / CORE_PER_WORKER
        cands.append((n, f"cpu {load1:.2f} of {cores} loaded, "
                         f"{free_cores:.1f} cores under {int(TARGET*100)}% "
                         f"→ {int(max(n,0))}"))
    if total and used is not None:
        free_mib = TARGET * total - used
        n = free_mib / MIB_PER_WORKER
        cands.append((n, f"mem {used/1024:.1f} of {total/1024:.0f} GiB used, "
                         f"{free_mib/1024:.1f} GiB under "
                         f"{int(TARGET*100)}% → {int(max(n,0))}"))
    if not cands:
        # Nothing was read, so there is no load term to hold. With a ceiling
        # set, that ceiling IS the user's answer and it stands. With none
        # set, there is no number a person gave and inventing an unbounded
        # one off an unreadable machine would be the worst of both — the
        # measured default is what is left to hold at, and it says so.
        if SLOT_CEILING == UNCAPPED:
            return CEILING_DEFAULT, (
                f"{CEILING_DEFAULT} slots · machine unreadable, holding at "
                f"the ceiling — none is set, so the measured "
                f"{CEILING_DEFAULT} stands")
        return SLOT_CEILING, (f"{SLOT_CEILING} slots · machine unreadable, "
                              f"holding at the ceiling")
    n = min(c[0] for c in cands)
    bound = min(cands, key=lambda c: c[0])[1].split()[0]
    n = _clamp(n)

    # `load1` lags: it stays high for minutes after a burn ends, so a count
    # driven to the floor by load1 alone may be throttling a machine that is
    # already free. Ask the instantaneous meter for a second opinion — but
    # ONLY here, because it costs a second of wall clock and the common
    # answer (a quiet machine, count at the ceiling) needs no confirming.
    if n == SLOT_FLOOR and bound == "cpu" and cores:
        busy, cost = _busy_now()
        if busy is not None:
            cands.append((None, f"busy {busy*100:.0f}% now ({cost:.1f}s "
                                f"sample)"))
            free_cores = (TARGET - busy) * cores
            m = int(max(0.0, free_cores) / CORE_PER_WORKER)
            m = _clamp(m)
            if m > n:
                # load1 was stale — the machine is free now
                return m, (f"{m} slots (load1 stale, ceiling "
                           f"{_ceiling_label()}) · "
                           + " · ".join(c[1] for c in cands))
    # with no ceiling there is nothing to be "at": SLOT_CEILING is 0 and the
    # count never is, so this reads `<bound>-bound` or `at the floor`
    why = ("at the ceiling" if n == SLOT_CEILING else
           "at the floor" if n == SLOT_FLOOR else f"{bound}-bound")
    return n, (f"{n} slots ({why}, ceiling {_ceiling_label()}) · "
               + " · ".join(c[1] for c in cands))




# ── 1. discovery ─────────────────────────────────────────────────────────────

def boards():
    """[(key, path)] — every board the daemon watches, from any directory.

    `ensure` when nothing answers, but only when there is a board at the cwd
    to ensure WITH: a cold daemon starts watching nothing (`cmd_run`: "there
    is no machine-wide list to read"), so starting one from a directory with
    no board buys an empty watch set and a stray process."""
    st = servelib.running()
    if st is None:
        board = board_at()
        if board is None:
            return [], ("no daemon is up and no board at the cwd — a cold "
                        "daemon watches nothing, so there is nothing to work")
        subprocess.run([sys.executable, os.path.join(BOARD, "serve.py"),
                        "ensure", board], check=False,
                       stdout=subprocess.DEVNULL)
        st = servelib.running()
        if st is None:
            return [], "daemon did not come up"
    out, skipped = [], []
    for b in st["boards"]:
        # `all` is in the watch set as a row with no path — it is the render
        # over the others, not one of them
        if not b.get("path"):
            skipped.append((b["name"], "no path — the merged page, not a board"))
            continue
        if not os.path.isdir(b["path"]):
            skipped.append((b["name"], f"gone from disk — {b['path']}"))
            continue
        out.append((b["name"], os.path.abspath(b["path"])))
    return out, skipped


# ── 1b. groups ───────────────────────────────────────────────────────────────
# A group is a label a board writes on ITSELF — `groups: work infra` in its
# own `.pearde/settings.md` — and `pearde machine work` is this same read over
# the boards carrying it. Nothing here keeps a list of which board is in which
# group, on the same rule the watch set already follows: the configuration is
# distributed to the boards, and a board nobody watches is in no group because
# it is in nothing. `## What it does not do` stands untouched — no registry is
# written, and no board's settings.md is written either; `groups:` is read.
#
# Labels, not a partition: a board may carry several, and a group is a filter
# over the set rather than a slice of a tree. `work` and `private` are two
# labels among any others, and no board is required to declare one.

VERBS = ("boards", "slots", "progress", "groups", "dispatch")

# flags whose VALUE is a bare word — `--workers 4` must not read as the group
VALUE_FLAGS = ("--workers", "--adapter", "--deadline")


def declared(path):
    """(labels, refused) — the groups a board writes on itself, and the ones
    dropped with why.

    `groups: work infra`, or the list form under `groups:`. Lowercased, so a
    board writing `Work` and one writing `work` are one group. Two labels can
    never be declared: a verb, because `pearde machine slots` has to keep
    meaning the slot reading, and `all`, which is the whole set by definition
    and so is never a subset of it. Both are refused where they are declared
    — printed by `machine groups` — rather than silently at the point of use,
    where the person cannot see what went wrong."""
    v = planlib.board_settings(path).get("groups", "")
    raw = v if isinstance(v, list) else re.split(r"[,\s]+", str(v or ""))
    out, bad = [], []
    for g in raw:
        g = str(g).strip().lower().lstrip("@")
        if not g or g in out:
            continue
        if g in VERBS:
            bad.append((g, "collides with the verb of the same name"))
        elif g == "all":
            bad.append((g, "`all` is every board — never a group of them"))
        else:
            out.append(g)
    return out, bad


def all_groups(entries):
    """{group: [board key…]} over the watch set, read off each board."""
    out = {}
    for k, p in entries:
        for g in declared(p)[0]:
            out.setdefault(g, []).append(k)
    return out


def in_group(entries, group):
    """(kept, note) — the watched boards declaring `group`, and the line that
    says what the filter left out. The note is printed with the frontier, so
    a short list is never mistaken for a quiet machine."""
    kept = [(k, p) for k, p in entries if group in declared(p)[0]]
    note = (f"group `{group}`: {len(kept)} of {len(entries)} watched board(s) "
            f"— {', '.join(k for k, _ in kept) if kept else 'none'}")
    return kept, note


def split_group(argv):
    """(group, rest) — the first bare word that is not a verb is the group.

    The verb set is closed and a label colliding with it is refused where it
    is declared, so the two never compete: `machine work slots` and `machine
    slots` both read unambiguously, in either order. A flag's value is
    skipped — `--workers 4` is a count, not a group."""
    skip = False
    for i, a in enumerate(argv):
        if skip:
            skip = False
            continue
        if a.startswith("-"):
            skip = a in VALUE_FLAGS
            continue
        if a in VERBS:
            continue
        return a.lstrip("@").lower(), list(argv[:i]) + list(argv[i + 1:])
    return None, list(argv)


def unknown_group(group, known):
    """The refusal, naming what a person can do about it."""
    have = (", ".join(sorted(known)) if known else
            "no watched board declares one")
    return (f"pearde machine: no watched board declares group `{group}` — "
            f"known: {have}. A board joins by writing `groups: {group}` in "
            f"its own .pearde/settings.md; nothing here keeps that list")


# ── 2. footprints, resolved ──────────────────────────────────────────────────

def real_feet(board_path, prd):
    """A PRD's footprint as real paths on this machine.

    `plan.qualify_paths` qualifies a MEMBER's relative footprint with its
    board name so two repos' `src/lib.ts` do not collide. That is right
    inside one board and wrong across the watch set: a plain board's own
    PRDs carry no `board`, so their paths come back bare and two boards'
    `resources/x.py` would compare EQUAL. And a path qualified `@dotfiles/…`
    is a string, so a footprint that reaches this repo through a symlink —
    the skills installed on this machine are symlinks into this tree — reads
    as a different file from the one it is.

    So: resolve against the PRD's own repo root and `realpath` it.

    Not `plan.prd_repo` — it walks up from the BOARD dir, and a board that is
    a git worktree of its own code repo (this one is: `.pearde/.git` holds
    `gitdir: …/.git/worktrees/-pearde`) stops at the board, so every
    footprint resolves under `.pearde/` where no such file exists. Walk from
    the board's PARENT, which is the code checkout on every layout."""
    _, feet = planlib.spec_data(prd)
    outer = os.path.dirname(os.path.abspath(board_path))
    root = planlib.repo_root(outer) or outer
    raw_repo = str(prd["fm"].get("repo", "") or "").strip()
    if raw_repo:
        for cand in (raw_repo, os.path.join(root, raw_repo)):
            if os.path.isdir(cand):
                root = planlib.repo_root(cand) or cand
                break
    out = []
    for f in feet:
        # undo the member qualification `spec_data` may have applied
        if f.startswith(planlib.MEMBER_SIGIL) and "/" in f:
            f = f[1:].partition("/")[2]
        p = f if os.path.isabs(f) else os.path.join(root, f)
        out.append(os.path.realpath(p))
    return out


def clash(a, b):
    """True when two footprints name one file on this machine."""
    return any(x == y or x.startswith(y + os.sep) or y.startswith(x + os.sep)
               for x in a for y in b)


# ── 3. the merged frontier ───────────────────────────────────────────────────

def frontier(entries, nslots):
    """(rows, notes, demand) — one list, not one per board. Each board's own
    plan is computed by the code that already computes it
    (`plan.compute_plan`) and the results are interleaved by that plan's own
    position — a second arithmetic here is the drift
    @references/parts/all.md warns against.

    `workers=0`: each board's schedule is drawn UNCONSTRAINED, so `start` is
    the dependency structure and nothing else, and `peak` is the board's own
    honest demand. The slot count is applied once, here, when the merged list
    is cut into waves — cutting it twice would hide work behind a cap the
    board never had (`.pearde/memos/the-board-assumes-unlimited-agents.md`).

    `demand` is the sum of every board's `peak`: how many agents the machine
    would run at its widest if nothing capped it. No second scheduler
    computes it — it is `plan.py`'s own number, added up."""
    rows, notes, demand = [], [], 0
    for key, path in entries:
        try:
            pl = planlib.compute_plan(path, workers=0, warn=False)
        except Exception as e:
            notes.append(f"{key}: unreadable — {type(e).__name__}: {e}")
            continue
        if not pl:
            # `compute_plan` answers None for two different things: a board
            # with nothing live, and a board it could not read at all. Only
            # the second is a note — a board silently contributing nothing
            # because its `prds/` is gone is a bug hidden from the whole
            # machine, and the first is just a finished board.
            if not os.path.isdir(os.path.join(path, "prds")):
                notes.append(f"{key}: unreadable — no `prds/` directory "
                             f"at {path}")
            continue
        # A master's `peak` is its MEMBERS' work at its widest, and each of
        # those members is watched in its own right and counted below — the
        # same double-count the `board` filter drops row by row. Skip it, on
        # the same rule @references/parts/all.md states: a member nobody
        # watches is not one of them.
        if not pl.get("settings", {}).get("members"):
            demand += pl.get("peak", 0)
        for rung, rel in enumerate(pl["order"]):
            prd = pl["prds"][rel]
            # a master carries its members' PRDs too, and those members are
            # registered boards in their own right — take each from its own
            if prd.get("board"):
                continue
            rows.append({
                "board": key, "path": path, "rel": rel,
                "addr": f"{planlib.MEMBER_SIGIL}{key}/{rel}",
                "rung": rung,
                "start": pl["schedule"][rel]["start"],
                "state": prd["state"],
                "prio": pl["prio"].get(rel, 0),
                "est": round(pl["est"].get(rel, 0.0), 1),
                "held": pl["held"].get(rel),
                "collect": rel in pl["collect"],
                "feet": real_feet(path, prd),
            })
    rows.sort(key=lambda r: (r["start"], -r["prio"], r["board"], r["rel"]))
    return rows, notes, demand


# ── 4. parallel legality ─────────────────────────────────────────────────────

def waves(rows, nslots):
    """The frontier cut into waves of what may run at once.

    Three gates, in order: the PRD's own `dispatchable` verdict (already in
    `held`), the slot count, and a real-path footprint clash with anything
    already in this wave. A clash serialises the PAIR — the later row falls
    to the next wave, nothing else is held back.

    A question standing on one PRD does not empty its board. `dispatchable`
    gates the asker, and this cut passes everything else through — a board
    with `asking 2` still contributes every ungated row it has."""
    # `compute_plan` only runs `dispatchable` over `open`/`specced`, because
    # for ONE board a `claimed` PRD is in flight rather than refused. Across
    # the machine that is a double-book waiting to happen: the row is in
    # somebody's window right now. Only the two dispatchable states go in.
    pool = [r for r in rows
            if not r["held"] and not r["collect"]
            and r["state"] in ("open", "specced")]
    out, why = [], {}
    while pool:
        wave, rest = [], []
        for r in pool:
            # the clash is asked for first, so a row that is BOTH out of
            # slots and clashing is told the thing it cannot fix by waiting
            blocker = next((w["addr"] for w in wave
                            if clash(r["feet"], w["feet"])), None)
            if blocker is None and len(wave) < nslots:
                wave.append(r)
            else:
                # the FIRST reason it fell — a row pushed down three waves
                # was pushed by wave 1, and that is the one worth printing
                why.setdefault(r["addr"],
                               f"footprint clash with {blocker}"
                               if blocker else "no slot free")
                rest.append(r)
        out.append(wave)
        pool = rest
    return out, why


def text(rows, waves_, skipped, notes, reading, watched, demand=0, defer=None):
    defer = defer or {}
    o = []
    for name, why in skipped:
        o.append(f"skipped {name} — {why}")
    o += notes
    boards_ = sorted({r["board"] for r in rows})
    silent = sorted(set(watched) - set(boards_))
    o.append(f"{len(boards_)} of {len(watched)} board(s) · {len(rows)} PRDs "
             f"on the frontier · {len(waves_)} wave(s)")
    if silent:
        o.append("silent: " + ", ".join(silent) + " — nothing on the frontier")
    # demand is what the boards ask for, the reading is what the machine will
    # give. The two are printed together on purpose: the gap is the whole
    # reason this command exists.
    o.append(f"demand {demand} at once, unconstrained")
    o.append(reading)
    o.append("")
    w = max((len(r["addr"]) for r in rows), default=10)
    inwave = {r["addr"] for wv in waves_ for r in wv}
    for i, r in enumerate(rows):
        # the mark says what will happen to the row, so it must agree with
        # the waves below it. Before this, a `question` or `claimed` row read
        # `ready` and then appeared in no wave — a column that cannot be wrong.
        mark = ("collect" if r["collect"] else
                "held" if r["held"] else
                "ready" if r["addr"] in inwave else
                "waits")
        # a `ready` row that is not in wave 1 was pushed by something, and
        # the reason is the only part of this page a person can act on
        note = r["held"] or defer.get(r["addr"]) or (
            f"state `{r['state']}` is not dispatchable"
            if mark == "waits" else "")
        o.append(f"{i:>3}. {r['addr']:<{w}}  {r['state']:<9} {mark:<7} "
                 f"p{r['prio']:<3} w{r['est']:<6}"
                 + (f"  {note}" if note else ""))
    o.append("")
    for n, wv in enumerate(waves_, 1):
        o.append(f"wave {n}: " + ", ".join(r["addr"] for r in wv))
    return "\n".join(o)


def progress(entries, rows, waves_, nslots):
    """One line over the merged set, in @references/parts/progress.md's
    register. The counts sum. `pct` does NOT: it is a weight fraction whose
    denominator uses each board's own `avg` for its unscored PRDs, so the two
    sums are carried and divided once at the end."""
    rd = rn = dd = dn = o = n = 0
    dw = aw = 0.0
    for _, path in entries:
        prds = planlib.scan(path)
        t = planlib.progress_terms(path, prds)
        rd += t["done"][0]; rn += t["done"][1]
        dd += t["derived"][0]; dn += t["derived"][1]
        o += t["open"][0]; n += t["open"][1]
        for r, p in prds.items():
            if str(p["fm"].get("origin", "")).strip() == "derived":
                continue
            if p["state"] not in planlib.LIVE_STATES and p["state"] != "done":
                continue
            w = planlib.weight_of(p, t["avg"])
            aw += w
            if p["state"] == "done":
                dw += w
    ready = sum(len(w) for w in waves_)
    blocked = sum(1 for r in rows if r["held"])
    coll = sum(1 for r in rows if r["collect"])
    return (f"▸ machine: {len(entries)} boards · done {rd}/{rn} · "
            f"{round(100 * dw / aw) if aw else 0}% · derived {dd}/{dn} · "
            f"open {o}/{n} · {round(100 * o / n) if n else 0}% · "
            f"ready {ready} · blocked {blocked} · collect {coll} "
            f"@{nslots} workers · as engineer")


def cmd_machine(argv):
    """every watched board as one ordered frontier — `boards`, `slots`,
    `progress`, `groups`, `--json`; prints, and moves nothing

    The one command. `pearde machine` prints the frontier; the verbs are
    windows onto the same read, and a bare word before or after one is a
    group — the same read over the boards declaring that label."""
    return main(argv)


COMMANDS = {"machine": cmd_machine}


def main(argv):
    if argv and argv[0] == "machine":
        argv = argv[1:]
    group, argv = split_group(argv)
    if argv and argv[0] == "dispatch":
        import dispatch as dispatchlib   # lazy: the read path never loads it
        pre = ["--group", group] if group else []
        return dispatchlib.main(pre + list(argv[1:]))
    entries, skipped = boards()
    if isinstance(skipped, str):
        print(f"pearde machine: {skipped}", file=sys.stderr)
        return 1
    known = all_groups(entries)
    if argv and argv[0] == "groups":
        for g in sorted(known):
            print(f"{g:16} {', '.join(known[g])}")
        loose = [k for k, p in entries if not declared(p)[0]]
        if loose:
            print(f"{'—':16} {', '.join(loose)}  (no group declared)")
        for k, p in entries:
            for bad, why in declared(p)[1]:
                print(f"{k:16} refused `{bad}` — {why}")
        if not known:
            print("no watched board declares a group — a board joins one by "
                  "writing `groups: <name>` in its own .pearde/settings.md")
        return 0
    gnote = []
    if group is not None:
        if group not in known:
            print(unknown_group(group, known), file=sys.stderr)
            return 1
        entries, note = in_group(entries, group)
        gnote = [note]
    if argv and argv[0] == "boards":
        for k, p in entries:
            # a board's own `workers:` is its cap, and `0` there means
            # unlimited — printing the bare number would read as "no
            # workers", the opposite. `workers_label` is plan.py's answer.
            cap = planlib.workers_label(planlib.plan_workers(p, None))
            gs = ", ".join(declared(p)[0]) or "—"
            print(f"{k:16} {p}  cap {cap}  groups {gs}")
        for name, why in skipped:
            print(f"{name:16} skipped — {why}")
        return 0
    nslots, reading = slots()
    if argv and argv[0] == "slots":
        print(reading)
        return 0
    rows, notes, demand = frontier(entries, nslots)
    wv, defer = waves(rows, nslots)
    if argv and argv[0] == "progress":
        print(progress(entries, rows, wv, nslots))
        return 0
    if "--json" in argv:
        print(json.dumps({"boards": [k for k, _ in entries], "rows": rows,
                          "slots": nslots, "reading": reading,
                          "demand": demand, "group": group, "groups": known,
                          "waves": [[r["addr"] for r in w] for w in wv],
                          "skipped": skipped,
                          "notes": gnote + notes}, indent=1))
    else:
        print(text(rows, wv, skipped, gnote + notes, reading,
                   [k for k, _ in entries], demand, defer))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
