#!/usr/bin/env python3
"""PROBE fixture — two throwaway boards in two repos, one file, two names.

Everything the dispatcher has to get right is a race, and a race cannot be
proved against the real board: the answer would depend on what this machine
happened to be doing. So the cases run against boards built in a temp dir at
run time, with a stand-in adapter binary whose behaviour is written by the
case — sleep, die on a 402, exit instantly.

    python3 fixture.py dry        --dry names every row and writes nothing
    python3 fixture.py clash      two boards, one real file → serialised
    python3 fixture.py dead       the adapter 402s → named, retried once, dead
    python3 fixture.py instant    the adapter exits 0 in 0s → dead, not "in"
    python3 fixture.py refuse     the claim gate refuses → named and skipped
    python3 fixture.py alive      two clean rows → both run, both "in"

Each prints `PASS <case>` or `FAIL <case> — <what it saw>` and exits 0/1.
"""
import os
import shutil
import sys
import tempfile
import time

# The probe's own copy of the dispatcher is gone: it moved to
# `resources/board/dispatch.py` with spec01, and these cases must exercise the
# SHIPPED file or they prove nothing about what runs.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("PEARDE_ROOT", "/Users/feb/dev/infra/pearde")
sys.path.insert(0, os.path.join(ROOT, "resources"))
sys.path.insert(0, os.path.join(ROOT, "resources", "board"))
import dispatch as D             # noqa: E402  the shipped dispatcher
import machine as mach           # noqa: E402


PRD = """---
state: {state}
origin: requested
priority: {prio}
complexity: 10
blast-radius: low
footprint:
  - {foot}
---

# {rel} — {rel}

{rel}
"""

SETTINGS = """---
name: {name}
language: English
workers: {workers}
pipeline: 0
weight-default: 20
---

# {name}
"""


def board(root, name, prds, workers=0, files=True):
    """A repo with a board in it. `git init` because `plan.repo_root` walks
    for `.git` and a footprint that resolves nowhere reads as no footprint —
    the exact failure [[260902-b1f6]] records for a worktree board."""
    repo = os.path.join(root, name)
    os.makedirs(os.path.join(repo, ".pearde", "prds"), exist_ok=True)
    os.makedirs(os.path.join(repo, ".git"), exist_ok=True)
    with open(os.path.join(repo, ".pearde", "settings.md"), "w") as f:
        f.write(SETTINGS.format(name=name, workers=workers))
    for rel, spec in prds.items():
        d = os.path.join(repo, ".pearde", "prds", rel)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "prd.md"), "w") as f:
            f.write(PRD.format(rel=rel, state=spec.get("state", "open"),
                               prio=spec.get("prio", 50),
                               foot=spec["foot"]))
        if not files:
            continue
        target = os.path.join(repo, spec["foot"])
        os.makedirs(os.path.dirname(target) or repo, exist_ok=True)
        if not os.path.exists(target) and not os.path.islink(target):
            open(target, "a").close()
    return name, os.path.join(repo, ".pearde")


def stand_in(root, name, body):
    p = os.path.join(root, name)
    with open(p, "w") as f:
        f.write("#!/usr/bin/env bash\n" + body + "\n")
    os.chmod(p, 0o755)
    return {"id": name, "name": name, "command": [p, "{prompt}", "{rel}"],
            "prompt": "/pearde run {rel}"}


def run(entries, nslots, ad, grace=0.25, **kw):
    # the grace window is a real number of seconds on the real thing; here it
    # is shortened so a case costs a fraction of a second instead of ten
    D.GRACE = grace
    rows, notes, _ = mach.frontier(entries, nslots)
    lines = []
    done, refused, dead = D.dispatch(entries, rows, nslots, ad,
                                     log=lines.append, poll_every=0.05, **kw)
    return rows, lines, done, refused, dead


# ── the cases ────────────────────────────────────────────────────────────────

def case_clash(root):
    """alpha owns `shared/f.py`. beta's footprint is `link/f.py`, a symlink
    into alpha's checkout — two boards, two repos, two footprint STRINGS that
    resolve to one inode. This is the case the parent PRD names: the skills
    on this machine are symlinks into this tree, so a pass on another board
    edits this one."""
    a = board(root, "alpha", {"one": {"foot": "shared/f.py", "prio": 90}})
    # beta's own file is NOT materialised: `link` is the symlink itself, and
    # creating `link/f.py` first would make it a real directory and the case
    # would prove nothing.
    b = board(root, "beta", {"two": {"foot": "link/f.py", "prio": 80}},
              files=False)
    os.symlink(os.path.join(root, "alpha", "shared"),
               os.path.join(root, "beta", "link"))

    # a stand-in that records its own overlap window: it appends start and end
    # stamps to one file, so "were they ever both running" is a fact on disk
    stamp = os.path.join(root, "stamps")
    ad = stand_in(root, "slow",
                  f'echo "start $$ $(date +%s.%N)" >> {stamp}; sleep 0.6; '
                  f'echo "end   $$ $(date +%s.%N)" >> {stamp}')
    rows, lines, done, refused, dead = run([a, b], 8, ad)
    if len(done) != 2:
        return False, f"{len(done)} of 2 ran · {lines} · refused {refused}"
    ev = [l.split() for l in open(stamp)]
    starts = sorted(float(e[2]) for e in ev if e[0] == "start")
    ends = sorted(float(e[2]) for e in ev if e[0] == "end")
    if len(starts) != 2:
        return False, f"{len(starts)} launches recorded"
    if starts[1] < ends[0]:
        return False, ("the two ran together — the second started "
                       f"{ends[0] - starts[1]:.2f}s before the first ended")
    return True, f"serialised · gap {starts[1] - ends[0]:.2f}s"


def case_dead(root):
    """The gateway said 402. The process starts, the pid is real, and the
    worker never existed."""
    a = board(root, "alpha", {"one": {"foot": "a.py"}})
    ad = stand_in(root, "dying",
                  'echo "API Error: 402 {\\"error\\":\\"credit balance\\"}"; '
                  'exit 1')
    rows, lines, done, refused, dead = run([a], 4, ad)
    txt = " | ".join(lines)
    if done:
        return False, f"reported {done} as worked · {txt}"
    if len(dead) != 1:
        return False, f"dead {dead} · {txt}"
    if "402" not in dead[0][1]:
        return False, f"the reason does not name the error: {dead[0][1]}"
    if sum(1 for l in lines if l.startswith("out ")) != 2:
        return False, f"re-dispatch did not happen once: {txt}"
    return True, dead[0][1][:80]


def case_instant(root):
    """Exit 0, immediately, with an empty log — the launch "succeeded" and
    nothing was worked. Without the grace window this counts as done."""
    a = board(root, "alpha", {"one": {"foot": "a.py"}})
    ad = stand_in(root, "instant", "exit 0")
    rows, lines, done, refused, dead = run([a], 4, ad)
    if done:
        return False, f"counted an instant exit as worked: {done}"
    if len(dead) != 1 or "launch grace" not in dead[0][1]:
        return False, f"dead {dead} · {lines}"
    return True, dead[0][1][:80]


def case_refuse(root):
    """A row the claim gate refuses. `needs:` an unfinished sibling is the
    cheapest refusal to build; the point is that it is NAMED, not dropped."""
    a = board(root, "alpha", {"one": {"foot": "a.py", "state": "question"},
                              "two": {"foot": "b.py"}})
    # `two` needs `one`, and `one` is asking — the gate refuses `two`
    p = os.path.join(a[1], "prds", "two", "prd.md")
    src = open(p).read().replace("blast-radius: low",
                                 "blast-radius: low\nneeds:\n  - one")
    open(p, "w").write(src)
    ad = stand_in(root, "slow2", "sleep 0.6")
    rows, lines, done, refused, dead = run([a], 4, ad)
    named = [r for r in refused if r[1]]
    if not named and not any(r["held"] for r in rows):
        return False, f"nothing refused and nothing held · {lines}"
    if any(a_ == "@alpha/two" for a_, _ in done):
        return False, f"dispatched a row the gate refuses · {done}"
    return True, (f"refused {named}" if named
                  else "held by the frontier before dispatch")


def case_alive(root):
    """Two clean rows on two boards, no clash: both run, both come back in.
    The control — without it every case above passes on a dispatcher that
    launches nothing."""
    a = board(root, "alpha", {"one": {"foot": "a.py"}})
    b = board(root, "beta", {"two": {"foot": "b.py"}})
    ad = stand_in(root, "ok", "sleep 0.6")
    rows, lines, done, refused, dead = run([a, b], 4, ad)
    if len(done) != 2 or dead:
        return False, f"done {done} dead {dead} refused {refused} · {lines}"
    return True, f"both in · {len(lines)} lines"


def case_noclash(root):
    """The control for `clash`: the same two boards with beta's footprint a
    file of its own, no symlink. They MUST overlap — a serialiser that always
    serialises passes `clash` and is worthless."""
    a = board(root, "alpha", {"one": {"foot": "shared/f.py", "prio": 90}})
    b = board(root, "beta", {"two": {"foot": "own/f.py", "prio": 80}})
    stamp = os.path.join(root, "stamps")
    ad = stand_in(root, "slow",
                  f'echo "start $$ $(date +%s.%N)" >> {stamp}; sleep 0.6; '
                  f'echo "end   $$ $(date +%s.%N)" >> {stamp}')
    rows, lines, done, refused, dead = run([a, b], 8, ad)
    if len(done) != 2:
        return False, f"{len(done)} of 2 ran · {lines}"
    ev = [l.split() for l in open(stamp)]
    starts = sorted(float(e[2]) for e in ev if e[0] == "start")
    ends = sorted(float(e[2]) for e in ev if e[0] == "end")
    if starts[1] >= ends[0]:
        return False, ("two unrelated footprints were serialised — the "
                       "clash check is answering yes to everything")
    return True, f"overlapped by {ends[0] - starts[1]:.2f}s"


def case_adapter(root):
    """The shipped `adapters/claude.json`, its binary overridden the way the
    daemon's own `adapter_bin` allows. Proves the dispatcher launches through
    the adapter set the view already uses, not a second launcher of its own."""
    a = board(root, "alpha", {"one": {"foot": "a.py"}})
    seen = os.path.join(root, "argv")
    bin_ = os.path.join(root, "stub")
    with open(bin_, "w") as f:
        f.write(f'#!/usr/bin/env bash\nprintf "%s\\n" "$@" > {seen}\n'
                f'sleep 0.6\n')
    os.chmod(bin_, 0o755)
    old = os.environ.get("PEARDE_ADAPTER_BIN")
    os.environ["PEARDE_ADAPTER_BIN"] = bin_
    try:
        ad = D.adapter()
        rows, lines, done, refused, dead = run([a], 4, ad)
    finally:
        if old is None:
            os.environ.pop("PEARDE_ADAPTER_BIN", None)
        else:
            os.environ["PEARDE_ADAPTER_BIN"] = old
    if len(done) != 1:
        return False, f"done {done} dead {dead} · {lines}"
    argv = open(seen).read().splitlines() if os.path.exists(seen) else []
    if not any("/pearde run one" in x for x in argv):
        return False, f"the adapter's prompt did not reach the binary: {argv}"
    return True, f"{ad['id']} · argv {argv}"


def case_dry(root):
    """`--dry` names every row and moves nothing. Proved on boards this case
    built, so the answer does not depend on what other sessions are doing:
    every `prd.md` byte-identical afterwards, no `run-*.log` written, and the
    stand-in adapter's own stamp file never created — it was never run."""
    a = board(root, "alpha", {"one": {"foot": "a.py"}})
    b = board(root, "beta", {"two": {"foot": "b.py"}})
    stamp = os.path.join(root, "ran")
    ad = stand_in(root, "never", f'echo ran >> {stamp}; sleep 0.6')

    def snap():
        out = {}
        for _, path in (a, b):
            for dp, _dirs, fs in os.walk(os.path.dirname(path)):
                for f in fs:
                    # a rebuilt cache is not a board move — `plan.scan`
                    # writes it on any read, the read path included, and it
                    # is git-ignored on the board for that reason
                    if f == "parse-cache.json":
                        continue
                    fp = os.path.join(dp, f)
                    try:
                        out[fp] = open(fp, "rb").read()
                    except OSError:
                        pass
        return out

    before = snap()
    rows, lines, done, refused, dead = run([a, b], 4, ad, dry=True)
    after = snap()
    if os.path.exists(stamp):
        return False, "--dry started the adapter"
    logs = [f for _, p_ in (a, b)
            for dp, _d, fs in os.walk(p_) for f in fs
            if f.startswith("run-") and f.endswith(".log")]
    if logs:
        return False, f"--dry opened a run log: {logs}"
    moved = sorted(set(before) ^ set(after)) + sorted(
        k for k in before if k in after and before[k] != after[k])
    if moved:
        return False, f"--dry moved {len(moved)} file(s): {moved[:3]}"
    would = [l for l in lines if l.startswith("would ")]
    if len(would) != 2:
        return False, f"{len(would)} `would` lines for 2 rows · {lines}"
    if dead or refused:
        return False, f"dead {dead} refused {refused}"
    return True, f"{len(would)} would · nothing on disk moved"


def _window(stamp):
    ev = [l.split() for l in open(stamp)]
    return (sorted(float(e[2]) for e in ev if e[0] == "start"),
            sorted(float(e[2]) for e in ev if e[0] == "end"))


def case_cap(root):
    """A board's own `workers:` is READ and honoured as a per-board cap under
    the machine-wide count, and never written. alpha says `workers: 1` and has
    two unrelated rows: with four machine-wide slots they must still serialise.
    beta is the control — `workers: 0` is unlimited, and its two overlap."""
    stamp = os.path.join(root, "stamps")
    ad = stand_in(root, "slow3",
                  f'echo "start $$ $(date +%s.%N)" >> {stamp}; sleep 0.6; '
                  f'echo "end   $$ $(date +%s.%N)" >> {stamp}')
    a = board(root, "alpha", {"one": {"foot": "a.py", "prio": 90},
                              "two": {"foot": "b.py", "prio": 80}}, workers=1)
    before = open(os.path.join(a[1], "settings.md"), "rb").read()
    rows, lines, done, refused, dead = run([a], 4, ad)
    if len(done) != 2:
        return False, f"{len(done)} of 2 ran · {lines}"
    if open(os.path.join(a[1], "settings.md"), "rb").read() != before:
        return False, "the dispatcher wrote the board's settings.md"
    starts, ends = _window(stamp)
    if len(starts) != 2 or starts[1] < ends[0]:
        return False, "a `workers: 1` board ran two at once"

    os.remove(stamp)
    b = board(root, "beta", {"three": {"foot": "c.py", "prio": 90},
                             "four": {"foot": "d.py", "prio": 80}}, workers=0)
    rows, lines, done, refused, dead = run([b], 4, ad)
    starts, ends = _window(stamp)
    if len(starts) != 2 or starts[1] >= ends[0]:
        return False, "`workers: 0` imposed a cap — it means unlimited"
    return True, "workers: 1 serialised · workers: 0 overlapped"


def case_adapters(root):
    """Two adapters configured and none named: it refuses with the list rather
    than picking one. Named, it takes the one named."""
    real = D.servelib.load_adapters
    D.servelib.load_adapters = lambda: [{"id": "a"}, {"id": "b"}]
    try:
        try:
            D.adapter()
        except SystemExit as e:
            msg = str(e)
        else:
            return False, "it picked one of two adapters"
        if "a" not in msg or "b" not in msg:
            return False, f"the refusal does not list them: {msg}"
        if D.adapter("b")["id"] != "b":
            return False, "--adapter did not pick the named one"
        try:
            D.adapter("zzz")
        except SystemExit as e2:
            named = "zzz" in str(e2)
        else:
            named = False
        if not named:
            return False, "an unknown --adapter was not refused by name"
    finally:
        D.servelib.load_adapters = real
    return True, msg.split(" — ")[-1][:70]


def case_once(root):
    """`--once` fills the pool once and returns — it does not wait for the
    fill to drain. One slot, two rows: one goes out, the second is still
    queued, and the call is back before the first worker is."""
    a = board(root, "alpha", {"one": {"foot": "a.py", "prio": 90},
                              "two": {"foot": "b.py", "prio": 80}})
    ad = stand_in(root, "slow4", "sleep 3")
    t0 = time.time()
    rows, lines, done, refused, dead = run([a], 1, ad, once=True)
    dt = time.time() - t0
    out = [l for l in lines if l.startswith("out ")]
    if len(out) != 1:
        return False, f"{len(out)} launched into one slot · {lines}"
    if dt > 2.0:
        return False, f"--once waited {dt:.1f}s for the fill to drain"
    return True, f"1 out, returned in {dt:.2f}s"


def case_deadline(root):
    """`--deadline S` stops FILLING after S seconds and names what is still in
    flight. It kills nothing."""
    a = board(root, "alpha", {"one": {"foot": "a.py", "prio": 90},
                              "two": {"foot": "b.py", "prio": 80}})
    ad = stand_in(root, "slow5", "sleep 3")
    rows, lines, done, refused, dead = run([a], 1, ad,
                                           deadline=time.time() + 0.3)
    stop = [l for l in lines if l.startswith("stop ")]
    if not stop:
        return False, f"no deadline line · {lines}"
    if "in flight" not in stop[0]:
        return False, f"the deadline line names nothing in flight: {stop[0]}"
    return True, stop[0][:70]


def case_workers_flag(root):
    """`--workers N` overrides the load-derived count and SAYS SO in the
    reading — a cap nobody can see is a cap nobody can debug."""
    n, reading = mach.slots()
    over = f"{3} slots (override) · " + reading
    if "(override)" not in over:
        return False, "the override is not in the reading"
    src = open(os.path.join(D.BOARD, "dispatch.py")).read()
    if 'slots (override)' not in src:
        return False, "dispatch.py does not label the override"
    if "nslots = a.workers" not in src:
        return False, "--workers does not replace the load-derived count"
    return True, f"load-derived {n} · --workers labels its override"


CASES = {"dry": case_dry, "clash": case_clash, "noclash": case_noclash, "adapter": case_adapter, "dead": case_dead, "instant": case_instant,
         "refuse": case_refuse, "alive": case_alive,
         "cap": case_cap, "adapters": case_adapters,
         "once": case_once, "deadline": case_deadline,
         "workers": case_workers_flag}


def main(argv):
    want = argv or list(CASES)
    bad = 0
    for name in want:
        root = tempfile.mkdtemp(prefix=f"pearde-fx-{name}-")
        try:
            ok, why = CASES[name](root)
        except Exception as e:
            import traceback
            ok, why = False, traceback.format_exc().splitlines()[-3:]
        finally:
            shutil.rmtree(root, ignore_errors=True)
        print(("PASS " if ok else "FAIL ") + f"{name:8} {why}")
        bad += 0 if ok else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
