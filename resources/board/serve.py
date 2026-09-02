#!/usr/bin/env python3
"""pearde serve — the board's live service: one daemon per machine, watching
every registered board and serving the view that reads and writes it.

    serve.py ensure [board]   start the daemon if none runs, register a board
                              (default: walk up from the cwd); safe to run on
                              every session start
    serve.py run [board…]     the daemon, foreground — what `ensure` detaches;
                              the boards are what a hot reload hands forward
    serve.py status           the daemon and every board it watches
    serve.py wait  [board]    block until the board moves, then say what did
    serve.py forget <name>    stop watching one board
    serve.py stop             stop the daemon
    serve.py reap [--dry-run] [--pid <n>]
                              stop every daemon on this machine that watches
                              no board still on disk — the fixtures' leftovers.
                              --pid narrows it to the ones named, which is how
                              a check stops only what it started
    serve.py selfcheck        assert the search ranker's own arithmetic

Singleton by port bind: the daemon owns 127.0.0.1:8443 (PEARDE_PORT
overrides), and a second `run` refuses to start because the bind fails. That
is the whole locking story — no pidfile to go stale.

Its own lifetime is its own business. A board directory that vanishes is
forgotten on the next tick, and a daemon that has watched nothing for
IDLE_EXIT_S exits. That is what stops a harness fixture — which points a
daemon at a `mktemp -d` board and then deletes it — from leaving a process
behind: no teardown of the fixture's can be relied on, because a SIGKILL runs
no trap and `ensure` detaches the child into its own session anyway. `reap`
clears the ones from before that rule existed, and keeps every daemon younger
than PEARDE_REAP_GRACE_S — a daemon a `SessionStart` hook has just started
watches nothing until its `/register` lands, and looks exactly like a leak.

What it does, per registered board, within about a second of a file changing:

  - re-orders a master board's schedule in place, keeping the anchor day, so a
    state written in one member re-plans the whole board
  - writes the day's history row, which is the only memory the board has
  - bumps a per-board sequence number the view and any agent long-poll on

It watches its own source too: edit render.py (or any module here) and the
daemon re-execs and every open page reloads itself, within about a second. The
data swap keeps its place; a code reload keeps only what the URL holds — which
view, which filter, which PRD — because that is where the page writes it.

A board keys by repo name plus any dot-dirs on its path (`racer/.mi/prds` →
`racer-mi`), or by `name:` in its settings.md when it has one — so two boards
in one repo still get distinct watch entries and /board/ URLs.

A master board (`members:` in its settings.md) is watched over its members'
files too, and registering one registers every member as a board in its own
right: the master carries the merged plan, each member keeps its own.

`all` is the other way several boards are read at once, and the opposite kind
of thing: not a board and not a plan, but one page over every board this
daemon watches — no settings, no schedule of its own, no write back through
it. The watch set is its whole configuration. @references/parts/all.md.

Everything is local. The board is the files; this serves them, and the edits
the view makes go back into the same files through one set of writers
(edit.py). Nothing is written outside a board: there is no machine-wide
registry, because a board records its own registration in its own
`<board>/.state/serve.json` and the daemon holds the union of them in memory
only. `ensure` is safe on every session start, so a board re-announces itself
whenever someone opens a session on it — that, and not a file, is what
rebuilds the watch set after a daemon restart.

The daemon's log is `<board>/.state/serve.log` of the board whose `ensure`
started it, named to the child through PEARDE_SERVE_LOG. It is a rolling
tail, not a record — the daemon keeps the last LOG_MAX_LINES of it and drops
the 2xx request lines, so what survives is transitions, reload notices and
tracebacks. An adapter's run log is `<board>/.state/run-<prd>.log`, in the
board the run is on.

HTTP API, all JSON, all 127.0.0.1-only:

  GET  /status                     daemon + boards: seq, last pass, last error
  GET  /data?board=<name>          the view payload + seq
  GET  /wait?board=<name>&seq=<n>[&boot=<s>]
                                   long-poll: 200 {seq, boot} on change, 204
                                   quiet — and 200 at once on a stale boot,
                                   which tells the page to reload its code
  GET  /board/<name>               the view itself — `all` is every watched
                                   board on one page, read-only, held in no
                                   file (@references/parts/all.md)
  GET  /                           302 to a board — the title is the switcher,
                                   so there is no index page to keep
  GET  /prd?board=<name>&rel=<rel> one PRD in full: frontmatter, body, specs
  GET  /report?board=<name>        `prds/report.md`, the board for a person
  GET  /memos?board=<name>         the board's decision records
  GET  /answers?board=<name>       every question the board has answered,
                                   newest first
  GET  /search?board=<name>&q=<text>[&kinds=<a,b>]
                                   one search over the whole board — prds,
                                   specs, memos, wiki, workflows, the report,
                                   the settings. `re:<pat>` or `/<pat>` greps
                                   by regex; anything else is a literal
                                   substring plus a fuzzy pass over names.
                                   Ranked, best first; each hit carries the
                                   jump its kind implies. `kinds` keeps only
                                   those kinds — applied here and not in the
                                   page, so a kind the cap dropped is still
                                   reachable; `counts` always covers every
                                   kind found, filter or no filter
  GET  /adapters                   configured launch targets: [{id, name}] —
                                   resources/board/adapters/*.json, see below
  POST /register {"cwd": path}     add the board found walking up from cwd
  POST /sync     {"board": name}   force a pass now
  POST /new      {"board","title","body"?,"parent"?,"priority"?,"est"?}
                                   write a new PRD
  POST /edit     {"board","prd","title"?,"fm"?,"body"?,"append"?,"retract"?}
                                   write one PRD — what the detail pane saves
  POST /report   {"board","prd","text"}   a worker's report → `## Report`
  POST /run      {"board","prd","adapter"?}
                                   launch that PRD's pass with one configured
                                   adapter — its own command, its own prompt
                                   template (resources/board/adapters/*.json;
                                   `claude.json` ships by default). `adapter`
                                   optional only when exactly one is
                                   configured. Detached, cwd the repo root.
                                   `open` only; 409 otherwise
  POST /unregister {"board": name} stop watching it
  POST /stop                       shut the daemon down

Python 3 stdlib only.
"""
import datetime
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
# win: a cp1252 console cannot encode the box/greek glyphs this prints,
# and the trailing summary dies on UnicodeEncodeError. Force UTF-8 out.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan as planlib  # noqa: E402
import render as renderlib  # noqa: E402
import memos as memoslib  # noqa: E402
import edit as editlib  # noqa: E402
import transitions as translib  # noqa: E402 — the one writer of `state:`
import all as alllib  # noqa: E402 — the `all` page's merge

PORT = int(os.environ.get("PEARDE_PORT", "8443"))
DIR = os.path.dirname(os.path.abspath(__file__))
# The daemon's own log. `ensure` opens `<board>/.state/serve.log` of the board
# it is registering and hands the path to the child in the environment; the
# child trims that same file. Empty in a process that was not spawned that way
# — a `serve.py run` in a terminal logs to the terminal, and trims nothing.
LOG_PATH = os.environ.get("PEARDE_SERVE_LOG") or ""
LOG_MAX_LINES = 2000   # the log is a rolling tail, not a record
LOG_TRIM_S = 60.0      # how often the daemon trims its own log

# The `**Qn**` that opens one answer line — the shape @plan.ANSWER_LINE_RE
# reads back, matched here on what the page is about to write.
ANSWER_ID_RE = re.compile(r"(?m)^\s*\*\*\s*(Q?\d+[a-z]?)\s*\*\*")


def trim_log(path=None):
    """Keep the last LOG_MAX_LINES of the log, in place.

    The daemon's stdout and stderr are the log: `ensure` spawns it with the
    file opened `"a"`, so both fds carry O_APPEND and every write seeks to
    the current end. Shortening the file underneath them is safe — the next
    write lands at the new EOF, not at a stale offset — so the trim rewrites
    the same inode instead of rotating to a second file the fds would not
    follow. Lines, not bytes: a byte cap cuts a traceback mid-line, and a
    traceback is the one thing this file exists to keep.
    """
    path = path or LOG_PATH
    if not path:
        return   # not spawned with a log — stdout is a terminal or a pipe
    try:
        with open(path, "r+", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
            if len(lines) <= LOG_MAX_LINES:
                return
            fh.seek(0)
            fh.writelines(lines[-LOG_MAX_LINES:])
            fh.truncate()
    except OSError:
        pass  # no log yet, or it is not ours to trim — never fatal
POLL_S = 1.0       # how often each board is stat-swept
SETTLE_S = 0.4     # a change must hold still this long before a sync
WAIT_MAX_S = 25    # long-poll ceiling; clients just re-poll
# How long the daemon runs with nothing left to watch before it exits. A
# fixture starts a daemon, points it at a `mktemp -d` board and deletes the
# directory; the watch loop caught the OSError and kept spinning, so the
# process outlived the board by days. The lifetime is the daemon's own
# business — no fixture can be trusted to run a teardown, because a SIGKILL
# runs no trap and `ensure` puts the child in its own session anyway.
# Generous, because a cold daemon legitimately watches nothing between its
# bind and the `/register` that `ensure` sends a moment later.
IDLE_EXIT_S = float(os.environ.get("PEARDE_IDLE_EXIT_S", "180"))
# The process whose `ensure` spawned this daemon, named to the child through
# the environment the way PEARDE_SERVE_LOG is. It gates one rule and one only:
# a daemon watching nothing but EPHEMERAL boards outlives nobody. A fixture
# SIGKILLed mid-run runs no trap, so its `mktemp -d` board survives too and
# the vanished-board rule never fires — this is the leash that does. A daemon
# watching a real board is never touched by it, whoever started it.
OWNER_PID = int(os.environ.get("PEARDE_SERVE_OWNER") or 0)
# How old a daemon must be before `reap` is allowed to have an opinion about
# it. `ensure` binds the port first and POSTs `/register` a moment later, so
# for a short window a daemon somebody very much wants watches nothing at all
# — and before the bind it answers no `/status` either. The `SessionStart`
# hook `pearde guard on` writes runs exactly that on every session start, and
# `doctor.sh --harnesses` ends its sweep with `reap`, so the two meet
# routinely on this machine. Reaping inside that window kills what the session
# just brought up. Nothing is bought by being quicker: `reap` exists for the
# daemons that predate IDLE_EXIT_S, which are hours or days old, and a daemon
# that really did die on arrival is ended by IDLE_EXIT_S by itself.
REAP_GRACE_S = float(os.environ.get("PEARDE_REAP_GRACE_S", "60"))

# Two reloaders, two stamps. The board hot-reloads its data. The page
# hot-reloads its own code, and the daemon hot-reloads itself — but they move
# separately now. `PY_SOURCES` is what the daemon re-execs on: `render.py` was
# imported once, so editing it changes nothing until the process is replaced.
# `view.js` and `view.css` never need a re-exec — the page fetches them by
# stamp, and a live page re-imports a moved view without a reload.
PY_SOURCES = [os.path.join(DIR, f)
              for f in ("serve.py", "render.py", "plan.py", "edit.py",
                        "transitions.py", "all.py")]
PY_SOURCES.append(os.path.join(os.path.dirname(DIR), "memos.py"))
VIEW_SOURCES = [os.path.join(DIR, f) for f in ("view.css", "view.js")]


def source_stamp():
    """The Python code — what a re-exec gives a fresh copy of."""
    return ",".join(str(os.stat(p).st_mtime_ns)
                    for p in PY_SOURCES if os.path.exists(p))


def view_stamp():
    """The page's own code — what an open page swaps in place, no reload.

    Baked into the served page and returned on every /wait, so an open page
    that renders against a stale stamp re-imports `view.js` where it stands
    (LIVE_JS), and the ?v= on each linked asset busts the browser's cache of
    it. Not part of the re-exec: the daemon only serves these two files."""
    return ",".join(str(os.stat(p).st_mtime_ns)
                    for p in VIEW_SOURCES if os.path.exists(p))


BOOT = source_stamp()
REFUSED = None     # a stamp that would not compile; do not say so twice


# ── boards ─────────────────────────────────────────────────────────────────────

def serve_name(path):
    """The daemon's board key: the repo name, plus the dot-dirs between it and
    prds/ — `racer/.mi/prds` keys as `racer-mi`, `realm/.claude/prds` as
    `realm-claude`. Two boards may legitimately want the same name, but a
    daemon key cannot: it is the watch entry and the /board/ URL, and two
    boards must never share one.

    This is the name that must always exist and always be unique, so it stays a
    pure function of the path. A board that renamed itself is preferred over it
    by `register()`, which can see whether that name is free — see
    `declared_name()`."""
    dots, d = [], os.path.dirname(os.path.abspath(path))
    while d and d != "/":
        base = os.path.basename(d)
        if not base.startswith("."):
            break
        dots.append(re.sub(r"[^A-Za-z0-9_-]", "", base))
        d = os.path.dirname(d)
    return "-".join([planlib.project_name(path)] + list(reversed(dots)))


class Board:
    def __init__(self, path):
        self.path = path  # the prds/ directory
        self.name = serve_name(path)
        self.seq = 0
        self.refs = ()      # the repos' refs, so a merge is a change too
        self.digest = None       # of the .md files — what "changed" means
        self.plan_digest = None  # of after+planned_at — fires a mirror
                                 # when `plan` re-ordered
        self.last_sync = None
        self.last_error = None
        self.history_day = None
        self.lock = threading.Lock()      # one mirror pass at a time
        self.cond = threading.Condition()  # /wait sleepers


BOARDS = {}  # name → Board
BOARDS_LOCK = threading.Lock()


class AllBoard:
    """`all` — every watched board on one page (@references/parts/all.md).

    Not a Board: it has no path, nothing on disk, no mirror pass and no watch
    entry. What it needs from a Board is the half the page talks to — a
    sequence number and a condition to sleep on — because the `all` page
    long-polls `/wait` exactly like a board's own. Its payload is recomputed
    per request out of the boards it merges, so there is nothing here to keep
    in step."""

    def __init__(self):
        self.name = alllib.KEY
        self.path = None
        self.seq = 0
        self.last_sync = None
        self.last_error = None
        self.cond = threading.Condition()


ALL = AllBoard()


def is_all(name):
    return (name or "") == alllib.KEY


def all_entries():
    """[(key, path)] — every board the daemon watches, in the order the page
    lists them. The watch set IS the configuration: `all` has no file naming
    what it merges, and a board joins it by being registered."""
    return sorted((b.name, b.path) for b in boards())

# ── the Start button: a click launches a pass ────────────────────────────────
# The view has no way to drive a Claude Code session itself — the daemon does,
# since it already runs local Python with subprocess access. RUNNING tracks one
# in-flight launch per (board, prd) so a second click while the first pass is
# still starting up is refused rather than spawning a duplicate session; it is
# not the board's own claim tracking (`claim:` in the PRD, which the spawned
# pass writes for itself once it picks the PRD up) and is dropped the moment
# the process this daemon started exits.
RUNNING = {}  # (board name, prd rel) → Popen
RUN_LOCK = threading.Lock()

ADAPTERS_DIR = os.path.join(DIR, "adapters")


def load_adapters():
    """Every configured launch target — one JSON file per adapter in
    resources/board/adapters/. `{"name": <picker label>, "command":
    [argv...], "prompt": <template, default "/pearde run {rel}">}`.
    `{prompt}` in `command` is replaced by the rendered prompt string,
    `{rel}` in either by the PRD's relative path. Each adapter phrases its
    own prompt: a pearde-aware agent (claude.json ships one) gets the
    `/pearde run <rel>` handle; an adapter for something that has never
    heard of pearde would instead template a plain-language task
    description in its own `prompt` field — this function does not care
    which, it only fills in placeholders.

    Missing dir or no valid files: empty list — the Start button then
    simply does not render (`ADAPTERS.length > 0` in view.js), same as an
    unserved page today. A malformed file is skipped with a stderr line,
    not a crash: one bad adapter must not take the others down with it."""
    if not os.path.isdir(ADAPTERS_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(ADAPTERS_DIR)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(ADAPTERS_DIR, fn)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            command = data.get("command")
            if not isinstance(command, list) or not command or not all(
                    isinstance(p, str) for p in command):
                raise ValueError("'command' must be a non-empty list of strings")
            out.append({
                "id": fn[:-5],
                "name": data.get("name") or fn[:-5],
                "command": command,
                "prompt": data.get("prompt") or "/pearde run {rel}",
            })
        except Exception as e:
            print(f"serve: adapter {fn!r} invalid, skipped ({e})", file=sys.stderr)
    return out


def adapter_bin(argv0):
    """Resolves one adapter's command[0] to a runnable path. An adapter that
    already names an existing absolute path is trusted as-is — an install
    with two adapters under test, each its own stand-in binary, needs both
    to resolve independently. Only a bare/relative name (the common case:
    `"claude"`, found via PATH) falls through to `PEARDE_ADAPTER_BIN`,
    which overrides *that* resolution for a machine where it is not the
    PATH entry, or a build under test naming its own; replaces the old
    adapter-specific `PEARDE_CLAUDE_BIN` now that an install can configure
    more than one adapter."""
    if os.path.isabs(argv0) and os.path.exists(argv0):
        return argv0
    override = os.environ.get("PEARDE_ADAPTER_BIN")
    if override:
        return override
    return shutil.which(argv0)


def plan_digest(path):
    """Of the plan alone — its edges and the day it was made. Hashing the
    content rather than stat-ing the file means a write that changed no order
    is not a change: the watcher fires when `plan` actually re-ordered."""
    mp, _ = planlib.load_map(path)
    return hash(json.dumps([mp.get("after"), mp.get("planned_at")],
                           sort_keys=True))


def member_paths(path):
    """The member boards of a master, the live ones only. Read fresh on every
    pass: `members:` is a setting, and a board joins or leaves a master by one
    line in settings.md — the daemon must not need a restart for that."""
    try:
        return [p for _, p in planlib.members(path) if os.path.isdir(p)]
    except Exception:
        return []


def lane_digest(path):
    """The board's git side: the refs of every repo it draws lanes from. A
    lane merging into main moves these and nothing else — the landing queue
    shrinks, the plan does not change — so this is watched apart from the
    board's own files and answered with a bump rather than a whole sync."""
    return tuple(planlib.ref_stamp(p)
                 for _, p in (planlib.members(path) or [(None, path)]))


def digest(path):
    """(rel, mtime, size) over every .md under the board — prd.md, specs,
    memos, settings — plus the board's own `view.user.css` and `view.user.js`,
    and the same under every member board when this is a master: the master's
    plan is a function of their states, so a change there is a change here.
    The map file and the rendered gantt are ours and excluded, or every sync
    would trigger the next.

    A user asset is board content, not skill source — it belongs here rather
    than in SOURCES, so editing one reloads the page without re-execing the
    daemon."""
    rows = []
    roots = [path] + member_paths(path)
    mdir, external = memoslib.memos_dir(path)
    if external and os.path.isdir(mdir):
        roots.append(mdir)  # decisions living outside the board still mirror live
    for base in roots:
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.endswith(".md") or (root == base and f in (
                        renderlib.USER_CSS, renderlib.USER_JS)):
                    fp = os.path.join(root, f)
                    try:
                        st = os.stat(fp)
                    except OSError:
                        continue
                    # keyed by root too: two boards under one master both
                    # have a settings.md, and one rel must not shadow the other
                    rows.append((base + "::" + os.path.relpath(fp, base),
                                 st.st_mtime_ns, st.st_size))
    return hash(tuple(sorted(rows)))


EPHEMERAL = ("/tmp/", "/private/tmp/", "/var/folders/", "/private/var/folders/")


def entry_path(board):
    """`<board>/.state/serve.json` — one board's own registration, and the
    only file this daemon writes about the watch set."""
    return os.path.join(planlib.state_dir(board), "serve.json")


def save_entry(b):
    """Record that this board is watched, in the board. No machine-wide list
    exists to fall out of date: the file says one thing about one board, and
    the daemon holds the union of them in memory.

    A board on an ephemeral filesystem is watched but never recorded — the
    file would go with the directory, and a marker that outlives nothing is
    not worth the write."""
    if b.path.startswith(EPHEMERAL):
        return
    try:
        with open(entry_path(b.path), "w", encoding="utf-8") as fh:
            json.dump({"path": b.path, "name": b.name, "port": PORT,
                       "at": datetime.datetime.now().isoformat(
                           timespec="seconds")}, fh, indent=1)
    except OSError:
        pass   # a read-only board is still watchable; the marker is a note


def drop_entry(b):
    """`forget` — the board stops saying it is watched."""
    try:
        os.remove(entry_path(b.path))
    except OSError:
        pass


def declared_name(path):
    """`name:` from the board's settings.md, or "" — one name across the
    project, the watch entry and the `/board/<name>` URL. A master board needs
    it: it is named for what it owns, not for the directory it sits in.

    A preference, not a key. Two projects may share a name on purpose —
    `realm/.mi/prds` and `realm/.claude/prds` both declare `realm` to mirror
    into one project. Two boards must never share a watch key, so `register()`
    takes this name only when it is free and falls back to the path
    derivation, which is unique by construction — the loser keeps its
    meaningful `realm-claude` instead of an order-dependent `realm-2`."""
    declared = str(planlib.board_settings(path).get("name", "")).strip()
    return re.sub(r"[^A-Za-z0-9_.-]", "-", declared) if declared else ""


def register(path):
    """Add one prds/ dir. The board's declared name keys it when that name is
    free, else the project-dir name — two boards sharing a name is already the
    collision `register()` breaks by suffixing."""
    path = os.path.abspath(path)
    b = Board(path)
    with BOARDS_LOCK:
        for name, cur in BOARDS.items():
            if cur.path == path:
                return cur, False
        want = declared_name(path)
        if want and want not in BOARDS and not is_all(want):
            b.name = want
        if is_all(b.name):
            # `all` is the merged page's URL. A board that would key that way
            # is suffixed instead — the page is not a board's to take.
            b.name = f"{b.name}-board"
        n = 2
        while b.name in BOARDS:  # same key, different path: suffix, never replace
            b.name = f"{serve_name(path)}-{n}"
            n += 1
        BOARDS[b.name] = b
    save_entry(b)
    bump(ALL)     # one more board is a change to the merged page
    return b, True


def boards():
    with BOARDS_LOCK:
        return list(BOARDS.values())


def by_name(name):
    with BOARDS_LOCK:
        return BOARDS.get(name or "")


# ── the mirror pass ────────────────────────────────────────────────────────────

def bump(b):
    with b.cond:
        b.seq += 1
        b.cond.notify_all()
    # `all` is a render over the others: whatever moved on one of them moved
    # on it, and a page open on `all` has to be told by the same tick.
    if b is not ALL:
        bump(ALL)


def history(b):
    """One row a day per board, written by whoever is watching. It is the only
    memory the board has — without it the burn-down has nothing to draw."""
    try:
        row = planlib.write_history(b.path)
        b.history_day = row["d"]
    except Exception:
        pass


def mirror(b, force=False):
    """One pass over a board that changed: re-order its schedule, write the
    day's history row, bump the sequence every reader is parked on. It writes
    nothing but the board's own files."""
    with b.lock:
        # Every board re-orders before it mirrors, master or not. A master's
        # plan spans repos nobody re-plans by hand. A plain board's goes stale
        # for a nearer reason — a held PRD weighs what is LEFT of it, so
        # closing one acceptance box re-sizes its bar and moves everything
        # downstream. The anchor day is kept: `plan` re-anchors, this only
        # re-orders, and reconcile returns early when nothing moved.
        try:
            planlib.reconcile(b.path)
        except SystemExit:
            b.last_error = "plan: needs cycle — reconcile skipped"
        except Exception as e:
            b.last_error = f"reconcile: {type(e).__name__}: {e}"
        bump(b)
        try:
            if b.history_day != datetime.date.today().isoformat():
                history(b)
            b.plan_digest = plan_digest(b.path)
            b.last_sync = time.time()
            b.last_error = None
        except Exception as e:  # a pass must never kill the watcher
            b.last_error = f"{type(e).__name__}: {e}"


def restart(stamp):
    """This view's own code moved — replace the process with itself.

    Safe because nothing that matters is lost across the exec. The watch set
    is the one thing that lives only in memory — there is no machine-wide
    registry to reload — so the daemon hands it to its successor on the
    command line: `run <board>…`. A process passing its own state to itself
    needs no file outside a board, and the set survives every hot reload. The
    listening socket is not inherited across exec so the port frees itself,
    and every client parked on /wait reconnects on its own and finds the new
    BOOT. A file caught half-written does not compile — say so once and keep
    serving the old code rather than exec'ing into a daemon that cannot
    start."""
    global REFUSED
    time.sleep(SETTLE_S)              # an editor mid-save settles first
    if source_stamp() != stamp:
        return                        # still moving; the next tick finds it
    for p in PY_SOURCES:
        # every source here is Python — a page's .css and .js are not reloaded
        # by re-exec any more: they are served by stamp, read fresh on each
        # request, and a live page re-imports a moved view without a reload.
        if not p.endswith(".py"):
            continue
        try:
            with open(p, "rb") as fh:
                compile(fh.read(), p, "exec")
        except SyntaxError as e:
            REFUSED = stamp
            print(f"serve: {os.path.basename(p)}:{e.lineno}: {e.msg} "
                  f"— not reloading", flush=True)
            return
        except OSError:
            return
    print("serve: source changed — reloading", flush=True)
    sys.stdout.flush()
    os.execv(sys.executable,
             [sys.executable, os.path.abspath(__file__), "run"]
             + sorted(b.path for b in boards()))


def vanished():
    """Drop every board whose directory is gone, and say how many are left.

    A board directory that no longer exists is not a board with an error — it
    is not a board. `digest()` raised OSError on it and the loop simply moved
    on, so a fixture's `mktemp -d` board stayed in the watch set, in `status`,
    and in the process table, for as long as the machine stayed up. Forgetting
    it here is what makes `IDLE_EXIT_S` reachable."""
    gone = [b for b in boards() if not os.path.isdir(b.path)]
    if gone:
        with BOARDS_LOCK:
            for b in gone:
                if BOARDS.get(b.name) is b:
                    del BOARDS[b.name]
        for b in gone:
            print(f"serve: {b.name} is gone from disk — no longer watching "
                  f"{b.path}", flush=True)
        bump(ALL)     # one board fewer is a change to the merged page
    return len(boards())


def orphaned():
    """True when this daemon watches only throwaway boards and the process
    that started it is gone.

    `save_entry` already refuses to record an EPHEMERAL board, on the grounds
    that a marker outliving nothing is not worth the write — the same reading
    applies to the process. A daemon holding nothing but `mktemp -d` boards is
    a fixture's, and once the fixture is gone nobody can ever ask it for
    anything again: its port is one nothing remembers and its boards are
    directories only that run knew about."""
    if not OWNER_PID:
        return False
    bs = boards()
    if any(not b.path.startswith(EPHEMERAL) for b in bs):
        return False
    try:
        os.kill(OWNER_PID, 0)
    except ProcessLookupError:
        return True
    except OSError:
        return False   # alive but not ours to signal
    return False


def watch():
    last_view = None
    last_trim = time.monotonic()
    last_live = time.monotonic()
    orphan_since = None
    while True:
        # The owner leash is a grace period, not a trigger. A session start on
        # a throwaway board legitimately outlives the shell that ran `ensure`
        # — a harness asserts exactly that, one poll later — and the leak this
        # closes was measured in days, so nothing is bought by exiting in the
        # same second. IDLE_EXIT_S bounds both rules.
        if orphaned():
            if orphan_since is None:
                orphan_since = time.monotonic()
            elif time.monotonic() - orphan_since >= IDLE_EXIT_S:
                print(f"serve: the run that started this daemon "
                      f"(pid {OWNER_PID}) has been gone {IDLE_EXIT_S:.0f}s and "
                      f"no board it watches outlives it — exiting", flush=True)
                os._exit(0)
        else:
            orphan_since = None
        if vanished():
            last_live = time.monotonic()
        elif time.monotonic() - last_live >= IDLE_EXIT_S:
            # Nothing to watch and nothing arriving. `ensure` starts a daemon
            # for a board and a session start re-announces every board it
            # cares about, so a daemon that has been handed none for this long
            # is one no board asked for any more.
            print(f"serve: nothing watched for {IDLE_EXIT_S:.0f}s — exiting",
                  flush=True)
            os._exit(0)
        if time.monotonic() - last_trim >= LOG_TRIM_S:
            last_trim = time.monotonic()
            trim_log()   # the daemon keeps its own log bounded while it runs
        stamp = source_stamp()
        if stamp != BOOT and stamp != REFUSED:
            restart(stamp)
        # the page's own code moved — wake every parked /wait so the pages
        # learn the new view stamp now, not after their 25s timeout
        vs = view_stamp()
        if vs != last_view:
            last_view = vs
            for b in boards():
                with b.cond:
                    b.cond.notify_all()
        for b in boards():
            try:
                d = digest(b.path)
            except OSError:
                d = None
            if d is not None and d != b.digest:
                time.sleep(SETTLE_S)  # a worker mid-write settles first
                d2 = digest(b.path)
                if d2 == d:           # still moving? next tick finds it at rest
                    b.digest = d2
                    mirror(b)
            elif d is not None and plan_digest(b.path) != b.plan_digest:
                mirror(b)             # `plan` moved, and it writes only the map
            else:
                try:
                    refs = lane_digest(b.path)
                except OSError:
                    refs = b.refs
                if refs != b.refs:    # a lane landed: redraw, do not re-plan
                    b.refs = refs
                    bump(b)
        time.sleep(POLL_S)


# ── http ───────────────────────────────────────────────────────────────────────

LIVE_JS = """<script>
/* The board moved. Fetch the payload and hand it to the page, which swaps it
   in where it stands — scroll, zoom, selection and the open inspector all
   survive. A page that cannot swap, or a payload that will not parse, reloads.

   The view's own code moving is the other case, and a swap cannot help there:
   the page was rendered against a stamp a newer view.js no longer is, so it
   re-imports the module where it stands. The new module disposes the
   listeners the old copy left behind and mounts itself — from a payload made
   fresh just before, and with the dirty inspector and the scroll handed over
   in __pearde_restore. No reload: the daemon's JSON contract never changed,
   so only the page itself has to come across. */
(async () => {
  let seq = __SEQ__;
  let view = "__VIEW__";   // the page's own code this page was rendered from
  for (;;) {
    try {
      const base = window.__BASE || "";
      // the page's own view stamp travels with the poll — the daemon answers
      // at once when the view's code moved, so a page does not wait out a
      // board's silence to hear that its own file changed
      const r = await fetch(base + "/wait?board=__NAME__&seq=" + seq +
                            "&view=" + encodeURIComponent(view));
      if (r.status === 200) {
        const out = await r.json();
        if (out.view && out.view !== view) {
          view = out.view;
          // hand the half-typed inspector and the scroll to the next copy
          if (typeof window.__pearde_save === "function") window.__pearde_save();
          try {
            const d = await (await fetch(base + "/data?board=__NAME__")).json();
            if (d.payload) window.__PAYLOAD__ = d.payload;
            await import(base + "/view.js?v=" + encodeURIComponent(view));
          } catch (e) { location.reload(); return; }
          seq = out.seq;
          continue;
        }
        seq = out.seq;
        // never write over someone typing in the inspector — the page is
        // live, but a half-written body is not the board's to throw away.
        // Hold, and pick the change up when the field is clean.
        while (window.__pearde_hold && window.__pearde_hold())
          await new Promise(s => setTimeout(s, 2000));
        if (window.__pearde_refresh) await window.__pearde_refresh();
        else { location.reload(); return; }
      }
    } catch (e) { await new Promise(s => setTimeout(s, 3000)); }
  }
})();
</script>"""


# ── search: what a hit is worth ───────────────────────────────────────────
# ⌘K lists every match in one column, so the ordering IS the feature: a
# hundred true hits with the wanted one at rank 60 is a failed search. Three
# things decide a score, in this order of weight: WHERE the match is (a
# title beats a body line), WHAT it matched (a whole word beats a fragment
# inside another word), and WHAT KIND of file holds it (a PRD someone wrote
# beats a note graphify generated). Everything is one integer so the sort is
# one key and the page never re-ranks.

# what a file is worth before anything matched — hand-written work first,
# generated notes last. A `board` hit is settings, the vision, graph output:
# real, but not what anyone means by "search the board".
KIND_RANK = {"prd": 60, "spec": 50, "memo": 55, "report": 40,
             "workflow": 35, "wiki": 30, "board": 10}

# Two tiers, and nothing crosses between them. A literal or regex match is a
# fact about the file; a fuzzy match is a guess about what the reader meant.
# So every literal hit — even one in a generated note — sorts above every
# fuzzy one, and kind rank only ever orders within a tier.
LITERAL = 1000


def score_line(kind, low, at, needle, in_name, rx):
    """One line's score. `low` is the line lowercased, `at` where the match
    starts, `in_name` whether the file's own title or path also carries the
    needle — a body hit in a file that is itself about the word outranks the
    same body hit anywhere else."""
    s = LITERAL + KIND_RANK.get(kind, 0)
    if rx is not None:               # a regex says nothing about word shape
        return s + 20
    n = len(needle)
    before = low[at - 1] if at else " "
    after = low[at + n] if at + n < len(low) else " "
    word = not before.isalnum() and not after.isalnum()
    s += 40 if word else 10
    if at == 0:
        s += 10                      # the line opens with it
    if in_name:
        s += 45                      # the file is about this word
    # a heading is the line a reader wants over the paragraph under it
    if low.lstrip().startswith("#"):
        s += 25
    return s


# A fuzzy hit is a guess about what someone meant; a literal one is a fact.
# So every fuzzy score is squeezed into this band and every literal hit
# starts above it — the fuzzy pass can reorder itself all it likes and can
# never push a real match down the list.
FUZZY_MAX = 99


def fuzzy(needle, hay):
    """Subsequence match, scored 0..FUZZY_MAX. Used only on a file's title and
    path, never on its body: fuzzy over every line of a board is noise, fuzzy
    over its names is how `bwiki` finds `board/wiki`.

    Two things separate an abbreviation from a coincidence, and both are
    required. TIGHTNESS: the matched letters must sit close together — `dspch`
    inside `dispatch` is a word someone shortened, the same letters scattered
    across a sentence are an accident, so a match spread wider than a few
    times the needle is refused outright. WORD STARTS: initials of the words
    score, letters buried mid-word barely do, which is what makes `bwiki`
    prefer `board/wiki` over a name that merely contains those letters."""
    if len(needle) < 3:
        return 0                     # two letters match nearly anything
    i, run, raw, first, last, starts = 0, 0, 0, None, 0, 0
    for j, ch in enumerate(hay):
        if i < len(needle) and ch == needle[i]:
            if first is None:
                first = j
            last = j
            at_word = j == 0 or not hay[j - 1].isalnum()
            starts += at_word
            raw += 1 + run + (3 if at_word else 0)
            run += 1
            i += 1
        else:
            run = 0
    if i < len(needle):
        return 0
    # The letters have to be a compression of something, not a scatter across
    # a paragraph-length name. Two shapes qualify and the span rule only
    # applies to the first: letters packed close together (`dspch` inside
    # `dispatch`), or letters that are the WORDS' OWN INITIALS, which by
    # definition sit as far apart as the words do — refusing those on span
    # would throw away the initialism, the one abbreviation everybody types.
    span = last - first + 1
    if (starts * 2 < len(needle)
            and span > max(len(needle) * 4, len(needle) + 12)):
        return 0
    # perfect: every letter a word start and adjacent — 4 per letter
    best = len(needle) * 4
    q = min(1.0, raw / best)
    # Two names that match equally well: the shorter one is the better guess,
    # because more of it is the thing the reader typed. Worth a fifth of the
    # band — enough to break a tie, never enough to beat a real quality gap.
    brevity = 1.0 / (1.0 + len(hay) / 40.0)
    return max(1, round(FUZZY_MAX * (q * 0.8 + brevity * 0.2)))


def board_json(b):
    return {"name": b.name, "path": b.path, "seq": b.seq,
            "last_sync": b.last_sync, "last_error": b.last_error,
            "members": [n for n, _ in planlib.members(b.path)]}


class Handler(BaseHTTPRequestHandler):
    server_version = "pearde-serve"

    def log_message(self, fmt, *args):  # requests go to serve.log, quietly
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

    def log_request(self, code="-", size="-"):
        """Only the requests that went wrong.

        The view long-polls /wait for as long as a page is open, so a line
        per request is a line per second per page — which is how this log
        reached hundreds of megabytes. A 2xx tells us nothing the board does
        not already say; a 4xx or 5xx is the reason someone opens this file.
        """
        n = getattr(code, "value", code)
        try:
            n = int(n)
        except (TypeError, ValueError):
            n = 0
        if not (200 <= n < 300):
            super().log_request(code, size)

    def reply(self, code, body, ctype="application/json"):
        raw = body if isinstance(body, bytes) else (
            body.encode() if isinstance(body, str)
            else json.dumps(body).encode())
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    # A prefix a reverse proxy may mount this under. Stripped here and
    # remembered, so every route below is written once and the page it renders
    # knows which base its own fetches have to use.
    PREFIX = "/timeline"

    def q(self):
        from urllib.parse import urlparse, parse_qs
        u = urlparse(self.path)
        path = u.path
        self.base = ""
        if path == self.PREFIX or path.startswith(self.PREFIX + "/"):
            self.base = self.PREFIX
            path = path[len(self.PREFIX):] or "/"
        return path, {k: v[0] for k, v in parse_qs(u.query).items()}

    def vault_root(self, board_path):
        """The vault this board belongs to, as `(root, id, prefix)` — the
        directory Obsidian opens, the id it is registered under (`None` when it
        is not) and what a board-relative path carries in front of it inside
        that vault. The vault is the PROJECT (the board's parent) since
        2026-09-02, so the prefix is the board's own folder; a board that never
        migrated is still found under its own path, where its vault used to
        root, and its prefix is empty. The id is looked up in Obsidian's own
        register by exact path, the same lookup the status line does."""
        cfg = os.path.expanduser("~/Library/Application Support/obsidian/"
                                 "obsidian.json")
        if not os.path.exists(cfg):
            cfg = os.path.join(os.environ.get("XDG_CONFIG_HOME",
                                              os.path.expanduser("~/.config")),
                               "obsidian", "obsidian.json")
        board_path = board_path.rstrip("/")
        project = os.path.dirname(board_path)
        wants = [(project, os.path.basename(board_path) + "/"),
                 (board_path, "")]
        try:
            with open(cfg, encoding="utf-8") as fh:
                vaults = (json.load(fh).get("vaults") or {})
        except (OSError, ValueError):
            vaults = {}
        for root, prefix in wants:
            for k, v in vaults.items():
                if os.path.realpath(str(v.get("path", ""))) \
                        == os.path.realpath(root):
                    return root, k, prefix
        # never registered: the folder holding `.obsidian/` is still the vault,
        # and `obsidian://open?path=` opens it — the status line's own fallback
        for root, prefix in wants:
            if os.path.isdir(os.path.join(root, ".obsidian")):
                return root, None, prefix
        return None, None, ""

    def vault_uri(self, board_path, rel):
        """obsidian://open for one note of the board's vault. A project never
        registered has no id to name, and `None` sends the hit nowhere the page
        can go — `path=` opens a vault, not a file inside one."""
        root, vid, prefix = self.vault_root(board_path)
        if not vid:
            return None
        path = prefix + rel
        stem = path[:-3] if path.endswith(".md") else path
        from urllib.parse import quote
        return f"obsidian://open?vault={vid}&file={quote(stem)}"

    def search_board(self, bpath, mode, rx, needle, key=None):
        """Every hit in one board. `key` is that board's /board/<key> name on
        the `all` page and None on the board's own: it prefixes what a hit
        jumps to, so a row found here opens the PRD it belongs to whichever
        page asked."""
        pre = f"{planlib.MEMBER_SIGIL}{key}/" if key else ""
        prds = planlib.scan(bpath)
        memos = {os.path.relpath(m["path"], bpath): m
                 for m in memoslib.scan(bpath).values()
                 if os.path.isabs(m.get("path") or "")
                 and (m["path"] + os.sep).startswith(bpath + os.sep)}
        SKIP = {"__pycache__", "graphs", "state"}
        MAX_PER_FILE = 12
        hits = []
        for root, dirs, files in os.walk(bpath):
            dirs[:] = sorted(d for d in dirs
                             if not d.startswith(".") and d not in SKIP)
            for f in sorted(files):
                if not f.endswith(".md") or f == "README.md":
                    continue
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, bpath)
                parts = rel.split(os.sep)
                kind, title, jump = "board", f, None
                # anything the vault holds that has no view of its own —
                # settings, the vision, graphify's notes — opens in
                # Obsidian, the one place the file is readable whole
                uri = self.vault_uri(bpath, rel)
                if parts[0] == "prds":
                    p = next((p for p in prds.values()
                              if fp.startswith(p["dir"] + os.sep)
                              or fp == os.path.join(p["dir"], "prd.md")),
                             None)
                    if p:
                        kind = ("spec" if "specs" in parts else "prd")
                        title = p["title"]
                        jump = (pre + p["rel"]) if p.get("rel") else None
                elif parts[0] == "memos":
                    m = memos.get(rel)
                    kind = "memo"
                    title = (m.get("subject") or m.get("slug") or f) if m else f
                elif parts[0] in ("wiki", "workflows"):
                    kind = "wiki" if parts[0] == "wiki" else "workflow"
                elif rel == "report.md":
                    kind = "report"
                # the path a person reads carries the board on `all`: two
                # boards both have a `settings.md`, and a bare rel would say
                # nothing about which one this is
                shown = (key + "/" + rel) if key else rel
                where = (title + " " + shown).lower()
                in_name = mode == "text" and needle in where
                n_file, first = 0, None
                try:
                    with open(fp, encoding="utf-8", errors="replace") as fh:
                        for ln, line in enumerate(fh, 1):
                            # what a fuzzy hit shows as context: the first
                            # line a person wrote. `---`, a frontmatter
                            # key and a heading's own `#` are not it —
                            # the title already says that much.
                            t = line.strip()
                            if (first is None and t and t != "---"
                                    and not t.startswith("#")
                                    and not re.match(r"^[\w-]+:", t)
                                    and not t.startswith("`state:")):
                                first = t[:200]
                            low = line.lower()
                            at = (rx.search(line).start()
                                  if rx and rx.search(line)
                                  else (low.find(needle) if rx is None
                                        else -1))
                            if at < 0:
                                continue
                            hits.append({
                                "kind": kind, "rel": jump, "title": title,
                                "path": shown, "line": ln, "board": key,
                                "text": line.strip()[:200], "uri": uri,
                                "score": score_line(kind, low, at, needle,
                                                    in_name, rx)})
                            n_file += 1
                            if n_file >= MAX_PER_FILE:
                                break
                except OSError:
                    continue
                # nothing in the body, but the name is a fuzzy match: the
                # file itself is the hit, opened at its first line. This is
                # the half of ⌘K that finds a note by an abbreviation.
                if mode == "text" and not n_file:
                    fz = fuzzy(needle, where)
                    if fz > 0:
                        hits.append({
                            "kind": kind, "rel": jump, "title": title,
                            "path": shown, "line": 1, "board": key,
                            "text": first or "", "uri": uri,
                            "fuzzy": True,
                            "score": fz + KIND_RANK.get(kind, 0)})
        return hits

    def do_GET(self):
        path, q = self.q()
        if path == "/status":
            bs = [board_json(b) for b in boards()]
            if bs:
                # `all` is a page, not a watch entry — it is in this list
                # because the switcher reads this list, and a page nobody can
                # find is a page nobody opens. `virtual` is how the switcher
                # tells it from a board it could open a file in.
                bs.append({"name": alllib.KEY, "path": None, "seq": ALL.seq,
                           "last_sync": None, "last_error": None,
                           "virtual": True,
                           "members": [b["name"] for b in bs]})
            return self.reply(200, {"pid": os.getpid(), "port": PORT,
                                    "boot": BOOT, "boards": bs})
        if path == "/data":
            if is_all(q.get("board")):
                # recomputed per request, never mirrored: `all` has no state
                # of its own to go stale, and the boards it merges each keep
                # their own plan on disk
                return self.reply(200, {"seq": ALL.seq, "payload":
                    renderlib.enrich(alllib.payload(all_entries()))})
            b = by_name(q.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            # enriched, not raw: the critical-path arithmetic is Python's, and
            # the page swaps this payload in without a reload — so what it gets
            # here has to be exactly what the initial render embedded.
            payload = renderlib.enrich(planlib.gantt_payload(
                b.path, planlib.scan(b.path), planlib.load_map(b.path)[0],
                planlib.board_settings(b.path)))
            return self.reply(200, {"seq": b.seq, "payload": payload})
        if path in ("/view.js", "/view.css"):
            # the page's own code, served as files so a live page can re-import
            # a moved view where it stands. Every request reads the file fresh;
            # the `?v=` stamp on the page's links is the cache-buster, so these
            # are served uncached — what the browser already has is never stale
            # for long enough to matter. Python never re-execs for these: an
            # open page swaps the new module in on its own.
            name = path[1:]
            try:
                body = open(os.path.join(DIR, name), encoding="utf-8").read()
            except OSError:
                return self.reply(404, {"error": "no such asset"})
            ctype = ("text/javascript; charset=utf-8" if name == "view.js"
                     else "text/css; charset=utf-8")
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body.encode())))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(body.encode())
            return
        if path == "/prd":
            # everything the timeline cannot fit on a bar: the PRD itself, its
            # specs and its file. The chart asks for this when a row is
            # clicked, so the view is a place to read the work and not only to
            # look at its shape.
            rel = q.get("rel") or ""
            if is_all(q.get("board")):
                # every row on the merged page is addressed `@<board>/<rel>`,
                # so the file it stands for is one lookup away — the page
                # reads a PRD where it lives and writes none
                key, rel = alllib.unqualify(rel)
                b = by_name(key)
            else:
                b = by_name(q.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            prd = planlib.scan(b.path).get(rel)
            if not prd:
                return self.reply(404, {"error": f"no PRD at {rel}"})
            specs = []
            sdir = os.path.join(prd["dir"], "specs")
            for f in sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []:
                if not f.endswith(".md"):
                    continue
                fm, title, body = planlib.parse_prd(os.path.join(sdir, f))
                closed, total = planlib.acceptance_of(body)
                specs.append({"file": f, "title": title or f,
                              "est": fm.get("est", ""),
                              "complexity": fm.get("complexity", ""),
                              "state": fm.get("state", ""),
                              "footprint": fm.get("footprint", []),
                              "boxes": [closed, total],
                              "body": body})
            return self.reply(200, {
                "rel": rel, "title": prd["title"], "state": prd["state"],
                "fm": {k: v for k, v in prd["fm"].items()},
                "body": prd["body"], "specs": specs,
                "path": prd.get("footer") or f"prds/{rel}/prd.md",
                "file": os.path.join(prd["dir"], "prd.md"),
                "board": prd.get("board"),
            })
        if path == "/answers":
            # what the board has already settled. The asks view takes an
            # answered question out of the inbox and shows it here instead,
            # newest first — so going through a pass is a list that empties,
            # and a decision made a week ago is still readable next to it.
            if is_all(q.get("board")):
                targets = all_entries()
            else:
                b = by_name(q.get("board"))
                if not b:
                    return self.reply(404, {"error": "unknown board"})
                targets = [(None, b.path)]
            out = []
            for key, bpath in targets:
                pre = f"{planlib.MEMBER_SIGIL}{key}/" if key else ""
                for rel, prd in planlib.scan(bpath).items():
                    for a in planlib.answers_of(prd):
                        out.append(dict(a, rel=pre + rel, prd=prd["title"],
                                        state=prd["state"],
                                        board=key or prd.get("board")))
            # by date, and a stamped answer sorts above an unstamped one:
            # undated is older than anything the view has written
            out.sort(key=lambda a: (a["date"] or "", a["rel"], a["id"]),
                     reverse=True)
            return self.reply(200, {"answers": out})
        if path == "/memos":
            if is_all(q.get("board")):
                return self.reply(200, {"memos": alllib.memos(all_entries())})
            b = by_name(q.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            ms = memoslib.scan(b.path)
            out = [{"slug": m["slug"], "subject": m.get("subject"),
                    "kind": m.get("kind"), "status": m.get("status"),
                    "date": str(m.get("date") or ""), "path": m.get("path"),
                    "prds": (m["fm"].get("prds") if isinstance(
                        m["fm"].get("prds"), list) else
                        [m["fm"]["prds"]] if m["fm"].get("prds") else []),
                    "body": m.get("body", "")}
                   for m in ms.values()]
            out.sort(key=lambda m: (str(m["status"]), str(m["date"])),
                     reverse=True)
            return self.reply(200, {"memos": out})
        if path == "/search":
            # one search over everything the board is — prds and their specs,
            # memos, wiki, workflows, the report and the settings — so ⌘K in
            # the view can list where a word lives and jump to it. The jump is
            # decided by the hit's kind: a prd or spec opens the inspector, a
            # memo opens the memos view, anything else the vault also holds
            # opens in Obsidian.
            #
            # Three ways to match, one box:
            #   `re:<pat>` or `/<pat>`   a regular expression, case-insensitive
            #                            — grep, for when the shape is known
            #   anything else            literal substring per line, plus a
            #                            fuzzy pass over titles and paths, so
            #                            `bwiki` finds `board/wiki`
            # Every hit carries a score and the list comes back sorted by it:
            # a title match beats a body match, a whole word beats a fragment,
            # a PRD beats a generated graph note, and a fuzzy name match sits
            # below every literal one.
            #
            # On `all` the same walk runs over every watched board and the
            # scores compete in one list — one box for the whole machine.
            name = q.get("board")
            if is_all(name):
                targets = all_entries()
            else:
                b = by_name(name)
                if not b:
                    return self.reply(404, {"error": "unknown board"})
                targets = [(None, b.path)]
            raw = (q.get("q") or "").strip()
            if len(raw) < 2:
                return self.reply(200, {"hits": [], "mode": "none"})
            mode, rx = "text", None
            if raw.startswith("re:") or raw.startswith("/"):
                pat = raw[3:] if raw.startswith("re:") else raw[1:].rstrip("/")
                try:
                    rx = re.compile(pat, re.I)
                    mode = "regex"
                except re.error as e:
                    return self.reply(200, {"hits": [], "mode": "regex",
                                            "error": f"bad pattern: {e}"})
                if not pat:
                    return self.reply(200, {"hits": [], "mode": "regex"})
            needle = raw.lower()
            MAX_HITS = 300
            hits = []
            for key, bpath in targets:
                hits += self.search_board(bpath, mode, rx, needle, key)
            # The counts are taken over EVERY hit, before any kind filter and
            # before the cap — they are what the filter chips offer, so they
            # have to say what is findable, not what survived. Filtering here
            # rather than in the page is the whole reason this is a parameter:
            # `workflow` hits that the cap dropped behind 300 PRD hits would
            # be unreachable if the page filtered a truncated list.
            counts = {}
            for h in hits:
                counts[h["kind"]] = counts.get(h["kind"], 0) + 1
            want = {k for k in (q.get("kinds") or "").split(",") if k}
            if want:
                hits = [h for h in hits if h["kind"] in want]
            hits.sort(key=lambda h: (-h["score"], h["path"], h["line"]))
            return self.reply(200, {"hits": hits[:MAX_HITS], "mode": mode,
                                    "total": len(hits), "counts": counts,
                                    "capped": len(hits) > MAX_HITS})
        if path == "/vault":
            # ctrl+O in the page — the project in Obsidian, opened at the vault
            # root rather than at a note, because the shortcut is "show me the
            # vault" and picking a landing note would be a guess. Same lookup
            # and same fallback as the status line's `▸vault`: the id when the
            # project is registered, `path=` when it holds a `.obsidian/` but
            # was never opened, and `null` — which the page says out loud —
            # when there is no vault to open at all. `all` merges boards that
            # have their own vaults each, so it names none.
            if is_all(q.get("board")):
                return self.reply(200, {"uri": None, "root": None,
                                        "why": "merged"})
            b = by_name(q.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            root, vid, _ = self.vault_root(b.path)
            if not root:
                return self.reply(200, {"uri": None, "root": None,
                                        "why": "none"})
            from urllib.parse import quote
            uri = (f"obsidian://open?vault={vid}" if vid
                   else "obsidian://open?path=" + quote(root))
            return self.reply(200, {"uri": uri, "root": root})
        if path == "/adapters":
            return self.reply(200, [{"id": a["id"], "name": a["name"]}
                                    for a in load_adapters()])
        if path == "/report":
            # the board's state for a person — `prds/report.md`, read from
            # disk on each call like `/prd`. Not parsed here: the page renders
            # the text, and an absent file is `null`, which draws nothing.
            if is_all(q.get("board")):
                # a report is one board's state written for a person. Several
                # boards have several of them, and picking one would be a lie
                # about the rest — the merged page draws its dashboard instead
                return self.reply(200, {"text": None, "path": None})
            b = by_name(q.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            fp = os.path.join(b.path, "report.md")
            try:
                text = open(fp, encoding="utf-8").read()
            except OSError:
                text = None
            return self.reply(200, {"text": text, "path": fp})
        if path == "/wait":
            b = ALL if is_all(q.get("board")) else by_name(q.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            try:
                since = int(q.get("seq", "-1"))
            except ValueError:
                since = -1
            # the page tells us which view it was rendered against. If the
            # files it needs moved since then it answers now, not in 25s —
            # there is no board change to wait for, the page has to re-import.
            cur_view = view_stamp()
            if q.get("view") is not None and q.get("view") != cur_view:
                return self.reply(200, {"seq": b.seq, "view": cur_view,
                                        "last_error": b.last_error})
            with b.cond:
                if b.seq == since:
                    b.cond.wait(WAIT_MAX_S)
                if b.seq == since:
                    return self.reply(204, b"")
                return self.reply(200, {"seq": b.seq, "view": view_stamp(),
                                        "last_error": b.last_error})
        ROUTES = ("/", "/status", "/data", "/wait", "/prd", "/memos",
                  "/search",
                  "/answers", "/view.js", "/view.css")
        want = None
        if path.startswith("/board/") or path.startswith("/timeline/"):
            want = path.split("/", 2)[2].strip("/")
        elif self.base and path not in ROUTES and path.count("/") == 1:
            # behind the proxy the friendly form is /timeline/<board>, so a
            # single unrecognised segment under the prefix is a board name
            want = path[1:]
        if want is not None:
            virtual = is_all(want)
            b = ALL if virtual else by_name(want)
            if not b or (virtual and not boards()):
                return self.reply(404, "unknown board", "text/plain")
            # `all` renders from the merge and from no board directory, so
            # nothing board-local reaches it: no report.md, no view.user.css,
            # no view.user.js. Those belong to a board, and this page is over
            # all of them.
            payload = (alllib.payload(all_entries()) if virtual
                       else planlib.gantt_payload(
                           b.path, planlib.scan(b.path),
                           planlib.load_map(b.path)[0],
                           planlib.board_settings(b.path)))
            head = (f'<script>window.__BASE={json.dumps(self.base)};'
                    f'window.__BOARD={json.dumps(b.name)};</script>')
            live = "" if q.get("nolive") else (
                LIVE_JS.replace("__NAME__", b.name)
                       .replace("__SEQ__", str(b.seq))
                       .replace("__VIEW__", view_stamp()))
            # the shell links the view as files, so an open page can re-import
            # a moved `view.js` where it stands; the payload and the report's
            # mtime are baked as globals ahead of the module. The head's own
            # __BASE/__BOARD go in first — the module reads all four off window.
            html = (renderlib.render_shell(payload, b.path, self.base,
                                           view_stamp())
                    .replace("</head>", head + "</head>")
                    .replace("</body>", live + "</body>"))
            return self.reply(200, html, "text/html; charset=utf-8")
        if path == "/":
            # The board title is the switcher, so there is no index page.
            # Land on a board — the master if one is registered, since it is
            # the merged view, else the first by name. The bare list covers
            # the one case the switcher cannot: no board registered at all.
            bs = sorted(boards(), key=lambda x: x.name)
            if bs:
                # one board is its own answer. More than one and the honest
                # landing is the page that holds them all — a master, which
                # carries a merged plan, else `all`, which carries the lot.
                first = next((b.name for b in bs if planlib.is_master(b.path)),
                             alllib.KEY if len(bs) > 1 else bs[0].name)
                self.send_response(302)
                self.send_header("Location", f"{self.base}/board/{first}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            return self.reply(200,
                "<!doctype html><meta charset=utf-8>"
                "<title>pearde</title>"
                "<body style='font:14px system-ui;padding:2em'>"
                "<h1>no board registered</h1>"
                "<p><code>resources/board/serve.py ensure &lt;path&gt;</code> "
                "registers one.</p>",
                "text/html; charset=utf-8")
        self.reply(404, {"error": "no such route"})

    def do_POST(self):
        path, _ = self.q()
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self.reply(400, {"error": "bad json"})
        # `all` is a display (@references/parts/all.md). Every write names a
        # board and lands in that board's files; the merged page holds none of
        # them, so it is refused here rather than guessed at. The page's rows
        # carry the board they came from — the door is one click away.
        if is_all(body.get("board")) and path in (
                "/new", "/edit", "/report", "/run", "/unregister"):
            return self.reply(409, {"error": "all is a display, not a board — "
                                    "open the PRD's own board to write it"})
        if path == "/register":
            try:
                board = planlib.find_board(body.get("cwd") or None)
            except SystemExit:
                return self.reply(404, {"error": "no prds/ found from cwd"})
            b, new = register(board)
            if new:
                threading.Thread(target=mirror, args=(b, True),
                                 daemon=True).start()
            # Registering a master registers its members too: each member keeps
            # its own project, and a member nobody watches would mirror only
            # when its own session happens to be open.
            brought = []
            for path in member_paths(board):
                mb, mnew = register(path)
                if mnew:
                    brought.append(mb.name)
                    threading.Thread(target=mirror, args=(mb, True),
                                     daemon=True).start()
            return self.reply(200, {"board": board_json(b), "new": new,
                                    "members": brought})
        if path == "/sync":
            if is_all(body.get("board")):
                # the merged page has no pass of its own: syncing it is
                # syncing every board it draws
                for b in boards():
                    mirror(b, force=True)
                return self.reply(200, {"name": alllib.KEY, "seq": ALL.seq,
                                        "boards": [b.name for b in boards()]})
            b = by_name(body.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            mirror(b, force=True)
            return self.reply(200, board_json(b))
        if path == "/new":
            # Filing work from the view. The template is the board's own, so a
            # PRD written here is the same shape as one written by hand — and
            # `origin: requested` because a person asked for it.
            b = by_name(body.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            # `transitions.add` is the one way a PRD is filed: the slug is
            # its gate, and the line it prints lands in serve.log.
            try:
                rel = translib.add(
                    b.path, body.get("title") or "", "view",
                    priority=int(body.get("priority") or 0),
                    body=body.get("body") or "",
                    parent=(body.get("parent") or "").strip("/") or None,
                    out=lambda line: print(line, flush=True))
            except translib.Refused as e:
                return self.reply(409, {"error": str(e)})
            except ValueError:
                return self.reply(400, {"error": "priority is an integer"})
            threading.Thread(target=mirror, args=(b,), daemon=True).start()
            return self.reply(200, {"prd": rel})
        if path == "/edit":
            # The view writes the board one structured line at a time,
            # atomically, frontmatter and body never in the same write.
            # A claim is reported, not enforced — whoever is looking at this
            # page is the authority.
            b = by_name(body.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            rel = body.get("prd") or ""
            prd = planlib.scan(b.path).get(rel)
            if not prd:
                return self.reply(404, {"error": f"no PRD at {rel}"})
            path_md = os.path.join(prd["dir"], "prd.md")
            # An answer this PRD already carries is refused before anything
            # is written — the same rule `answer` enforces on the command
            # line, on the other door into `## Answers`. Without it a page
            # showing a stale pass writes a second answer to a settled
            # question, and the newer line contradicts the recorded one with
            # nothing to say which is the decision. Checked first, so a
            # refusal leaves the file exactly as it was.
            if body.get("append") and body.get("heading") == "Answers":
                held = translib.answered_of(prd)
                dup = [q for q in ANSWER_ID_RE.findall(str(body["append"]))
                       if planlib._qid(q) in held]
                if dup:
                    return self.reply(409, {"prd": rel, "wrote": [], "error":
                        "answer: " + ", ".join(planlib._qid(q) for q in dup)
                        + (" is" if len(dup) == 1 else " are")
                        + " already answered — retract before answering again"})
            # body first: it replaces everything under the frontmatter, so a
            # title written before it would be the first thing overwritten
            wrote = []
            if body.get("body") is not None:
                editlib.set_body(path_md, str(body["body"]))
                wrote.append("body")
            if body.get("append"):
                editlib.append_section(path_md, body.get("heading", "Notes"),
                                       str(body["append"]))
                wrote.append("append")
            if body.get("retract"):
                # reopening one question: its `**Qn**` line leaves
                # `## Answers`, so every counter sees it back on the frontier
                if editlib.retract_answer(path_md, str(body["retract"])):
                    wrote.append("retract")
            if body.get("title"):
                editlib.set_title(path_md, str(body["title"])[:250])
                wrote.append("title")
            fm = dict(body.get("fm") or {})
            # `state:` has one writer — the transition. A person at the page
            # is the user talking to the board and is not gated, so the call
            # is forced, and the line in serve.log says `forced · view`.
            # It goes last: the answer flow appends the answer and sets
            # `open` in one call, and the gate reads the file as appended.
            state = fm.pop("state", None)
            for k, v in fm.items():
                if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", str(k)):
                    continue
                if v in (None, ""):
                    editlib.del_key(path_md, k)
                else:
                    editlib.set_key(path_md, k, str(v).replace("\n", " "))
                wrote.append(k)
            if state not in (None, ""):
                try:
                    translib.transition(
                        b.path, rel, str(state).strip(), "view", force=True,
                        source="view",
                        out=lambda line: print(line, flush=True))
                    wrote.append("state")
                except translib.Refused as e:
                    if wrote:
                        threading.Thread(target=mirror, args=(b,),
                                         daemon=True).start()
                    return self.reply(409, {"error": str(e), "wrote": wrote,
                                            "prd": rel})
            if wrote:
                threading.Thread(target=mirror, args=(b,), daemon=True).start()
            return self.reply(200, {"wrote": wrote, "prd": rel,
                                    "claim": prd["fm"].get("claim")})
        if path == "/report":
            # A worker's report is evidence — it belongs with the PRD it is
            # evidence about. Appended to `## Report`, nothing else.
            b = by_name(body.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            rel, text = body.get("prd", ""), body.get("text", "")
            if not rel or not text:
                return self.reply(400, {"error": "prd and text required"})
            prd = planlib.scan(b.path).get(rel)
            if not prd:
                return self.reply(404, {"error": f"no PRD at {rel}"})
            editlib.append_section(os.path.join(prd["dir"], "prd.md"),
                                   "Report", text)
            threading.Thread(target=mirror, args=(b,), daemon=True).start()
            return self.reply(200, {"wrote": f"{rel}/prd.md"})
        if path == "/run":
            # The Start button. Only `open` is offered one in the view, and
            # this is the server-side half of that same rule — a stale page,
            # or a second tab, must not launch a pass on a PRD that already
            # moved on.
            b = by_name(body.get("board"))
            if not b:
                return self.reply(404, {"error": "unknown board"})
            rel = body.get("prd") or ""
            prd = planlib.scan(b.path).get(rel)
            if not prd:
                return self.reply(404, {"error": f"no PRD at {rel}"})
            if prd["state"] != "open":
                return self.reply(409, {"error":
                    f"{rel} is {prd['state']}, not open"})

            adapters = load_adapters()
            if not adapters:
                return self.reply(500, {"error":
                    "no adapter configured — add one under resources/board/adapters/"})
            adapter_id = body.get("adapter")
            if adapter_id:
                adapter = next((a for a in adapters if a["id"] == adapter_id), None)
                if not adapter:
                    return self.reply(404, {"error": f"no adapter {adapter_id!r}"})
            elif len(adapters) == 1:
                adapter = adapters[0]
            else:
                # The view only shows a picker at 2+ adapters and always
                # sends one; a caller that skips the picker (a script, an
                # older cached page) is the only way to land here.
                return self.reply(400, {"error":
                    "multiple adapters configured, specify one",
                    "adapters": [a["id"] for a in adapters]})

            key = (b.name, rel)
            with RUN_LOCK:
                cur = RUNNING.get(key)
                if cur and cur.poll() is None:
                    return self.reply(409, {"error": "already starting"})

            # Each adapter renders its own prompt template (a pearde-aware
            # agent gets "/pearde run <rel>"; one that has never heard of
            # pearde gets whatever plain-language task text its own
            # adapters/*.json spells out) and its own command argv — this
            # daemon does not assume either.
            prompt = adapter["prompt"].format(rel=rel)
            argv = [part.format(prompt=prompt, rel=rel) for part in adapter["command"]]
            resolved = adapter_bin(argv[0])
            if not resolved:
                return self.reply(500, {"error":
                    f"{argv[0]!r} not found on PATH — set PEARDE_ADAPTER_BIN "
                    f"or fix the {adapter['id']} adapter's command"})
            argv[0] = resolved

            # the run happens on this board, so its log lands in this board
            safe = re.sub(r"[^A-Za-z0-9_-]", "_", rel)
            log = open(os.path.join(planlib.state_dir(b.path),
                                    f"run-{safe}.log"), "a")
            try:
                # Windows resolves many CLI launchers (via shutil.which) to a
                # .CMD shim — CreateProcess cannot launch that directly, only
                # cmd.exe can, so this one call needs shell=True there. POSIX
                # never does: shell=True with a list there hands the extra
                # args to the shell itself as $0/$1, not to the command, so
                # the CLI would run with none of its arguments. Not
                # adapter-specific — any adapter's Windows binary can be a
                # shim, so this stays unconditional on `os.name`.
                proc = subprocess.Popen(
                    argv, cwd=os.path.dirname(b.path), stdout=log, stderr=log,
                    start_new_session=True, shell=(os.name == "nt"))
            except OSError as e:
                return self.reply(500, {"error": f"could not start: {e}"})
            with RUN_LOCK:
                RUNNING[key] = proc
            return self.reply(200, {"started": True, "board": b.name,
                                    "prd": rel, "adapter": adapter["id"],
                                    "pid": proc.pid})
        if path == "/unregister":
            name = body.get("board")
            with BOARDS_LOCK:
                b = BOARDS.pop(name or "", None)
            if not b:
                return self.reply(404, {"error": "unknown board"})
            drop_entry(b)
            return self.reply(200, {"forgot": name})
        if path == "/stop":
            self.reply(200, {"stopping": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        self.reply(404, {"error": "no such route"})


# ── daemon lifecycle ───────────────────────────────────────────────────────────

def call(path, payload=None, timeout=3):
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"},
        method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        return json.loads(raw) if raw else {}


def running():
    try:
        return call("/status")
    except (urllib.error.URLError, OSError):
        return None


def cmd_run(paths=()):
    """`run [<board>…]` — the daemon. The paths are what a previous instance
    of this process handed forward across a hot-reload exec, never a file: a
    cold daemon starts watching nothing and boards arrive by `ensure`."""
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print(f"serve: port {PORT} is taken — a daemon already runs "
              f"(or set PEARDE_PORT)", file=sys.stderr)
        return 1
    # No boards at boot but the ones this process was handed: there is no
    # machine-wide list to read, and a daemon that invented one would be
    # writing outside every board. Boards arrive by `ensure`, which every
    # session start runs — see the module docstring for the cost of that.
    for p in paths:
        if os.path.isdir(p):
            register(p)
    threading.Thread(target=watch, daemon=True).start()
    print(f"serve: watching on http://127.0.0.1:{PORT} — "
          f"{len(boards())} board(s)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


def cmd_ensure(arg):
    board = planlib.find_board(arg)  # dies with the usual message if none
    if not running():
        # The daemon logs into the board that started it — one root, and the
        # child is told which through the environment. It watches many boards
        # and its log lives in one of them; nothing outside a `.pearde/`.
        log_path = os.path.join(planlib.state_dir(board), "serve.log")
        trim_log(log_path)   # a log left long by an older build starts bounded
        log = open(log_path, "a")
        subprocess.Popen([sys.executable, os.path.abspath(__file__), "run"],
                         stdout=log, stderr=log, start_new_session=True,
                         env={**os.environ, "PEARDE_SERVE_LOG": log_path,
                              # who to outlive, and who not to. `ensure` is
                              # short-lived; its parent is the session or the
                              # harness that wanted the daemon.
                              "PEARDE_SERVE_OWNER": str(os.getppid())})
        for _ in range(50):
            if running():
                break
            time.sleep(0.1)
        else:
            print(f"serve: daemon did not come up — see {log_path}",
                  file=sys.stderr)
            return 1
        print(f"serve: started on http://127.0.0.1:{PORT}")
    out = call("/register", {"cwd": board})
    b = out["board"]
    print(f"serve: {'registered' if out['new'] else 'watching'} {b['name']} "
          f"· {b['path']} · live view http://127.0.0.1:{PORT}/board/{b['name']}")
    if b.get("members"):
        print(f"serve: master of {len(b['members'])} board(s) — "
              + ", ".join(b["members"])
              + (f" · also registered: {', '.join(out['members'])}"
                 if out.get("members") else ""))
    return 0


def cmd_status():
    st = running()
    if not st:
        print("serve: not running")
        return 1
    print(f"serve: up on http://127.0.0.1:{st['port']} · pid {st['pid']}")
    for b in st["boards"]:
        age = (f"{int(time.time() - b['last_sync'])}s ago"
               if b["last_sync"] else "never")
        note = f" · {b['last_error']}" if b["last_error"] else ""
        mem = (f" · master of {len(b['members'])}: "
               + ", ".join(b["members"])) if b.get("members") else ""
        print(f"  {b['name']:16} synced {age}{note} · {b['path']}{mem}")
    return 0


def cmd_wait(arg, timeout):
    """Block until the board moves, then say what moved. An orchestrator with
    nothing left to dispatch parks here instead of ending the pass — see
    @references/parts/loop.md.

    Exit 0 = something happened (the inbox, or any board change), 1 = the
    timeout ran out quietly, 2 = no daemon."""
    board = planlib.find_board(arg)
    st = running()
    if not st:
        print("serve: not running — nothing to wait on", file=sys.stderr)
        return 2
    name = next((b["name"] for b in st["boards"]
                 if os.path.abspath(b["path"]) == os.path.abspath(board)), None)
    if not name:
        print(f"serve: {board} is not registered — run `ensure` first",
              file=sys.stderr)
        return 2
    seq = next(b["seq"] for b in st["boards"] if b["name"] == name)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            out = call(f"/wait?board={name}&seq={seq}",
                       timeout=WAIT_MAX_S + 10)
        except (urllib.error.URLError, OSError):
            print("serve: daemon went away while waiting", file=sys.stderr)
            return 2
        if not out:
            continue                      # 25 quiet seconds; park again
        print(f"serve: {name} moved · seq {out.get('seq')}")
        return 0
    print(f"serve: {name} quiet for {timeout}s")
    return 1


def cmd_stop():
    if not running():
        print("serve: not running")
        return 0
    try:
        call("/stop", {})
    except (urllib.error.URLError, OSError):
        pass  # it died mid-reply, which is the goal
    print("serve: stopped")
    return 0


def daemon_pids():
    """Every `serve.py run` on this machine but our own, newest last.

    The process table is the only place a stranded daemon exists. There is no
    machine-wide registry to consult — that is settled and gone — and a daemon
    on a spare `PEARDE_PORT` is reachable by no port anyone remembers. So the
    scan starts from `ps`, and every judgement about a pid is made by asking
    the daemon itself."""
    me = os.getpid()
    try:
        out = subprocess.run(["ps", "-eo", "pid=,command="],
                             capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    found = []
    for line in out.splitlines():
        line = line.strip()
        pid, _, cmd = line.partition(" ")
        if not pid.isdigit() or int(pid) == me:
            continue
        # the daemon's own argv: `<python> …/serve.py run [board…]`. A shell
        # or an editor whose command line merely quotes the phrase is not one.
        parts = cmd.split()
        if len(parts) >= 3 and os.path.basename(parts[1]) == "serve.py" \
                and parts[2] == "run":
            found.append(int(pid))
    return found


def listen_port(pid):
    """The TCP port `pid` listens on, or None. `lsof` is the only portable
    reader of that on both macOS and Linux; without it, nothing here can name
    a daemon's port and `reap` says so rather than guessing."""
    try:
        out = subprocess.run(
            ["lsof", "-nP", "-a", "-p", str(pid), "-iTCP", "-sTCP:LISTEN"],
            capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    for line in out.splitlines()[1:]:
        m = re.search(r":(\d+)\s*\(LISTEN\)", line)
        if m:
            return int(m.group(1))
    return None


def age_s(pid):
    """Seconds since `pid` started, or None when `ps` will not say.

    `ps -o etimes=` is procps-only and darwin's ps rejects the keyword;
    `etime=` is on both, printing `[[dd-]hh:]mm:ss`. A pid whose age cannot be
    read is reported as None and treated by the caller as young, which is the
    safe direction: keeping a stranded daemon one more sweep costs a process,
    stopping a live one costs somebody's session."""
    try:
        out = subprocess.run(["ps", "-o", "etime=", "-p", str(pid)],
                             capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    t = out.strip()
    if not t:
        return None
    days, _, rest = t.partition("-")
    if not rest:
        days, rest = "0", days
    try:
        secs = 0.0
        for part in rest.split(":"):
            secs = secs * 60 + float(part)
        return secs + float(days) * 86400
    except ValueError:
        return None


def stranded(pid):
    """(verdict, port, detail) for one daemon pid.

    Stranded means: it watches nothing that still exists. A daemon watching
    one live board is a daemon someone is using, whatever port it is on — the
    board's own directory is the whole test, and it is a test no neighbouring
    session can move under us.

    A daemon younger than REAP_GRACE_S is kept before any of that is asked.
    Between `ensure`'s bind and the `/register` that follows it, a wanted
    daemon is indistinguishable from a stranded one — it watches nothing, and
    a moment earlier it answered nothing — and a `SessionStart` hook puts a
    daemon in that window on every session start."""
    age = age_s(pid)
    if age is not None and age < REAP_GRACE_S:
        port = listen_port(pid)
        return False, port, (f"started {age:.0f}s ago — inside the "
                             f"{REAP_GRACE_S:.0f}s grace a session start needs "
                             f"to register its board")
    port = listen_port(pid)
    if port is None:
        return True, None, "listening on no port"
    try:
        with urllib.request.urlopen(
                f"http://127.0.0.1:{port}/status", timeout=3) as r:
            st = json.loads(r.read() or b"{}")
    except (urllib.error.URLError, OSError, ValueError):
        return True, port, f"port {port} answers no /status"
    if st.get("pid") != pid:
        return False, port, f"port {port} is answered by pid {st.get('pid')}"
    # A `/status` payload is another process's JSON, and a board entry mid-
    # register carries a null `path`. `b.get("path", "")` returns that None —
    # the default is only for a MISSING key — and `os.path.isdir(None)` raises
    # TypeError, which took the whole reap down with a traceback. A reaper
    # that crashes on one malformed neighbour reaps nothing at all, which is
    # worse than the leak it exists to clear.
    bs = [b for b in st.get("boards") or [] if isinstance(b, dict)]
    live = [b for b in bs if os.path.isdir(b.get("path") or "")]
    if live:
        return False, port, (f"watching {len(live)} live board(s): "
                             + ", ".join(str(b.get("name") or "?")
                                         for b in live))
    n = len(bs)
    return True, port, (f"watching {n} board(s), none on disk" if n
                        else "watching no board")


def cmd_reap(dry=False, only=None):
    """`reap` — stop every daemon nothing needs any more.

    The fix for the leak is `IDLE_EXIT_S`, which makes a daemon end its own
    life; this is for the ones already running when that landed, and for a
    machine where a fixture died between `run` and its first `/register`.

    `--pid <n>` narrows the sweep to pids the caller names. That is for a
    check, not for a person: a harness proving the stop path has to stand
    REAP_GRACE_S down to reach it, and a grace-less sweep over the whole
    process table would stop a neighbouring session's daemon in the very
    window the grace exists to protect. A check that reaps only the pids it
    started cannot do that. The sweep `doctor.sh` runs names no pid and keeps
    the shipped grace, which is what makes it safe beside another session."""
    pids = daemon_pids()
    if only:
        pids = [p for p in pids if p in only]
    if not pids:
        print("serve: no other serve.py daemon is running")
        return 0
    killed = 0
    for pid in pids:
        bad, port, why = stranded(pid)
        where = f"pid {pid}" + (f" · port {port}" if port else "")
        if not bad:
            print(f"serve: keeping {where} — {why}")
            continue
        if dry:
            print(f"serve: would stop {where} — {why}")
            killed += 1
            continue
        if port is not None:
            try:
                urllib.request.urlopen(urllib.request.Request(
                    f"http://127.0.0.1:{port}/stop", data=b"{}",
                    headers={"Content-Type": "application/json"},
                    method="POST"), timeout=3).read()
            except (urllib.error.URLError, OSError):
                pass   # it died mid-reply, which is the goal
        for _ in range(20):
            try:
                os.kill(pid, 0)
            except OSError:
                break
            time.sleep(0.1)
        else:
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass
        print(f"serve: stopped {where} — {why}")
        killed += 1
    print(f"serve: {killed} of {len(pids)} stranded")
    return 0


def cmd_selfcheck():
    """`serve.py selfcheck` — the search ranker's own arithmetic, asserted.

    Ordering IS the feature of ⌘K: a hundred true hits with the wanted one at
    rank 60 is a failed search. Two properties hold it up and neither is
    visible by reading a score — that every literal match outranks every
    fuzzy one whatever kinds they are, and that fuzzy refuses a scatter while
    still taking an initialism. Both are one arithmetic slip away from
    silently inverting, and nothing else in the tree would notice.
    """
    bad = []

    def check(name, cond):
        print(("  ok   " if cond else "  FAIL ") + name)
        if not cond:
            bad.append(name)

    # the tiers cannot meet: the worst literal hit beats the best fuzzy one
    worst_lit = LITERAL + min(KIND_RANK.values())
    best_fz = FUZZY_MAX + max(KIND_RANK.values())
    check(f"every literal hit outranks every fuzzy one "
          f"({worst_lit} > {best_fz})", worst_lit > best_fz)

    # a whole word beats a fragment of one, same file, same kind
    word = score_line("prd", "the window closed", 4, "window", False, None)
    frag = score_line("prd", "a windowless room", 2, "window", False, None)
    check(f"a whole word beats a fragment ({word} > {frag})", word > frag)

    # the fuzzy pass: what it must take, and what it must refuse
    for needle, hay, want in (
            ("bwiki", "board/wiki", True),                # a compression
            ("abcdef", "alpha bravo charlie delta echo foxtrot", True),
            ("wndw", "the pass runs in a window that ends", True),
            ("xyzq", "board/wiki", False),                # letters absent
            ("ab", "a b", False),                         # too short to mean
            ("abcdef", "xxaxx xxbxx xxcxx xxdxx xxexx xxfxx zzz", False)):
        got = fuzzy(needle, hay) > 0
        check(f"{needle!r} {'matches' if want else 'does not match'} "
              f"{hay[:34]!r}", got == want)

    # word starts beat buried letters; a shorter name breaks a tie
    check("word-start letters beat buried ones",
          fuzzy("bwiki", "board/wiki") > fuzzy("bwiki", "xbxwxixkxix"))
    check("the shorter of two equal names wins",
          fuzzy("abc", "alpha bravo charlie")
          > fuzzy("abc", "alpha bravo charlie delta echo foxtrot golf"))
    # and no fuzzy score can escape its band
    check("no fuzzy score leaves the band",
          all(0 <= fuzzy(n, h) <= FUZZY_MAX
              for n, h in (("bwiki", "board/wiki"), ("a", "a"),
                           ("abc", "abc"), ("zz", "zzzzzzzz"))))

    print(f"selfcheck: {len(bad)} failed" if bad else "selfcheck: all passed")
    return 1 if bad else 0


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "status"
    if cmd == "run":
        return cmd_run([a for a in args[1:] if not a.startswith("-")])
    if cmd == "ensure":
        return cmd_ensure(args[1] if len(args) > 1 else None)
    if cmd == "status":
        return cmd_status()
    if cmd == "stop":
        return cmd_stop()
    if cmd == "reap":
        rest = args[1:]
        # `--pid` narrows a machine-wide action, so a pid it cannot read must
        # REFUSE. Dropping the bad value and carrying on would leave `only`
        # empty, and an empty filter means "every daemon on this machine" —
        # so `--pid "$PIDVAR"` with PIDVAR unset would silently become the
        # grace-less machine-wide sweep the flag exists to prevent.
        only = []
        i = 0
        while i < len(rest):
            if rest[i] == "--pid":
                val = rest[i + 1] if i + 1 < len(rest) else ""
                if not val.isdigit() or int(val) <= 0:
                    print(f"serve: reap --pid wants a process id, got "
                          f"{val!r} — refusing rather than widening to every "
                          f"daemon on this machine", file=sys.stderr)
                    return 2
                only.append(int(val))
                i += 2
                continue
            i += 1
        return cmd_reap(dry="--dry-run" in rest, only=only)
    if cmd == "selfcheck":
        return cmd_selfcheck()
    if cmd == "wait":
        rest = [a for a in args[1:] if not a.startswith("--")]
        return cmd_wait(rest[0] if rest else None,
                        next((int(a[len("--timeout="):]) for a in args
                              if a.startswith("--timeout=")), 900))
    if cmd == "forget":
        if len(args) < 2:
            print("serve: forget <board-name>", file=sys.stderr)
            return 2
        if not running():
            print("serve: not running")
            return 1
        try:
            call("/unregister", {"board": args[1]})
            print(f"serve: forgot {args[1]}")
            return 0
        except urllib.error.HTTPError:
            print(f"serve: no board named {args[1]}", file=sys.stderr)
            return 1
    print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
