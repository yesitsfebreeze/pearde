#!/usr/bin/env python3
"""pearde boards — where a board is on disk, and how a new one is made.

Cut out of plan.py; plan.py re-exports every name here, so every caller that
imports `plan` keeps working. Python 3 stdlib only.
"""
import collections
import datetime
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
# win: a cp1252 console cannot encode the box/greek glyphs this prints,
# and the trailing summary dies on UnicodeEncodeError. Force UTF-8 out.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memos as memolib  # noqa: E402 — the skill root, one dir up
import questions as qlib  # noqa: E402 — the drill count, one reader with list
import render as renderlib  # noqa: E402 — beside this script
import workflows as wflib  # noqa: E402 — the skill root, one dir up
HERE = os.path.dirname(os.path.abspath(__file__))

# ── board ─────────────────────────────────────────────────────────────────────

# The board is one directory at a project root, under `.obsidian/`'s vault —
# it holds `prds/`, `memos/`, `wiki/` and `workflows/`, so a reader can see
# what the tool keeps without being told. `.state/` inside it is the
# machine-local corner: the plan, the two journals, the pass file and the
# rendered view, none of them committed, all of them regenerable.
#
# The name carries a dot. It lost one for a day — 2026-09-02 to 2026-09-03 —
# on the reading that Obsidian skips every path holding a dot-segment, so a
# vault at the project root could not see the board. That reading was right
# about Obsidian and wrong about which root the vault takes: the fix is the
# vault at `<board>/.obsidian`, which @references/obsidian.md already says, not
# a board renamed out of hiding. The undotted name cost more than it bought.
# `pearde/` is an ordinary word, so a checkout that already uses it — this
# repo sits at `infra/pearde` — answers to two names at once, and one board
# resolving twice fans every dispatch out twice and refuses every collect.
# The nine other boards on this machine never moved off `.pearde`.
#
# So the board is `.pearde/`, a real directory holding every file it owns, and
# no board file is reachable only through a symlink. `pearde` survives as the
# legacy name: `board_at` still finds a board that never migrated, and
# `pearde upgrade` moves one.
#
# The name is not fixed, either. The board's directory name is CONFIGURABLE,
# and the way it is configured is that the board says so itself: see
# `named_boards`.
BOARD_DIR = ".pearde"
LEGACY_BOARD_DIR = "pearde"
BOARD_DIRS = (BOARD_DIR, LEGACY_BOARD_DIR)
STATE_DIR = ".state"
PRDS_DIR = "prds"
SETTINGS = "settings.md"
# Never a board, and named so the scan below does not have to ask: a
# dependency tree, a build output, a vendored copy. Everything hidden is
# already skipped — the scan takes no dot-directory at all.
SCAN_SKIP = frozenset(("node_modules", "target", "vendor", "__pycache__",
                       "build", "dist"))


class NotABoard(NotADirectoryError):
    """A path that was handed to a writer and is not a board.

    An `OSError`, deliberately: every writer on this board already guards its
    open() with `except OSError`, so the daemon's `save_entry`, `drop_entry`
    and `migrate_legacy_state` skip one board instead of dying. `die()` would
    raise `SystemExit`, which is not an `Exception` and so walks straight
    through the daemon's `except Exception` watch-thread guard — one stale
    watch entry would stop every board the daemon holds. The CLI turns it back
    into a one-line refusal at its own boundary."""


def is_board_dir(p):
    """A directory is a board when it CARRIES one: `settings.md`, or a
    `prds/` directory. The name alone stopped being proof the day the dot
    came off it — `.pearde` was a name nothing else on a disk would take,
    `pearde` is an ordinary word, and a project holding a folder called that
    (a checkout of this repo beside its siblings, say) would otherwise be
    read as the board and shadow the real one next to it. Either marker is
    enough: a board mid-creation has `settings.md` before it has PRDs, and a
    board a person made by hand may have PRDs before it has settings."""
    return os.path.isdir(p) and (
        os.path.isfile(os.path.join(p, "settings.md"))
        or os.path.isdir(os.path.join(p, PRDS_DIR)))


def board_link(p):
    """What a board reached through a compatibility symlink is really called.

    `upgrade` leaves `.pearde` pointing at the directory it moved the board
    to, so every path spelled the old way keeps resolving — but the name a
    caller is handed has to be the board's own. That name is written into
    vault-relative wikilinks, and Obsidian shows no path holding a
    dot-segment, so handing back the link would put the board's own notes
    where the vault cannot see them: the exact defect the plain name exists
    to fix.

    One level, resolved beside the link, never `realpath`: a symlinked
    ANCESTOR (`/tmp` on macOS is `/private/tmp`) must stay spelled the way
    the caller spelled it, or `os.path.dirname(board)` stops matching the cwd
    every other check compares it against."""
    if not os.path.islink(p):
        return p
    return os.path.normpath(os.path.join(os.path.dirname(p), os.readlink(p)))


def named_boards(d):
    """The boards inside project dir `d` that are called neither `pearde` nor
    `.pearde` — immediate children holding `settings.md`. At most two are
    returned: one is the answer and two is a refusal, so nothing past the
    second changes either.

    This scan IS the board-directory configuration, and there is no setting
    for it anywhere. A setting would have to live in `settings.md`, inside
    the board a resolver has not found yet; a marker file at the project root
    would be a second name for one directory and a second thing to keep true;
    an environment variable is one value for a machine that watches nine
    boards; and a key in the project's `.claude/settings.json` binds this
    layout to another tool's file and makes seven resolvers — one of them a
    shell script — parse JSON on every command. The board already declares
    itself, since ab1c762: it CARRIES the file. Renaming the directory is the
    whole act of configuring it, and nothing can go stale because there is
    only ever one place the name is written.

    `settings.md` alone here, not the `prds/` half of `is_board_dir`: for the
    two known names the name is corroboration and either marker is enough,
    but a directory nothing named must carry the file only a board carries.
    A repo with `docs/prds/` in it is not a repo with two boards.

    Immediate children, one stat each, no dot-directory — `.pearde` is tried
    above by name, and a hidden board is the thing the plain name exists to
    stop being."""
    hits, seen = [], set()
    try:
        names = sorted(os.listdir(d))
    except OSError:                        # unreadable, or not a directory
        return hits
    for name in names:
        if name.startswith(".") or name in SCAN_SKIP:
            continue
        p = os.path.join(d, name)
        if not os.path.isfile(os.path.join(p, SETTINGS)):
            continue
        real = os.path.realpath(p)         # a link beside its target is one board
        if real in seen:
            continue
        seen.add(real)
        hits.append(p)
        if len(hits) == 2:
            break
    return hits


def two_boards(d, found):
    """The refusal for a project holding two boards — one sentence naming
    both. Duplicated in every resolver with that resolver's own prefix,
    the way the walk itself is."""
    return (f"two directories under {d} carry a board — "
            f"{os.path.basename(found[0])}/ and {os.path.basename(found[1])}/"
            "; a project has one board, so rename or remove one of them")


def board_named(d):
    """`<d>/pearde`, or `<d>/.pearde` when only that carries a board — the two
    names the tool knows, the second read through its compat symlink."""
    for name in BOARD_DIRS:
        p = os.path.join(d, name)
        if is_board_dir(p):
            return board_link(p)
    return None


def board_scanned(d):
    """The board of `d` that is called something else — one immediate child
    holding `settings.md`. Two of them is not a board to choose between; it
    is refused, by name."""
    found = named_boards(d)
    if len(found) > 1:
        die(two_boards(d, found))
    return found[0] if found else None


def board_in(d):
    """The board inside project dir `d`, or None — the named one, then the
    scanned one. Cheapest first, and the answer for a directory a caller
    pointed at deliberately."""
    return board_named(d) or board_scanned(d)


def walk_up(d, find):
    """`find` applied to `d` and every ancestor, first answer wins."""
    while True:
        b = find(d)
        if b:
            return b
        nxt = os.path.dirname(d)
        if nxt == d:
            return None
        d = nxt


def board_above(d):
    """The board `d` belongs to, walking up — TWO passes, and a board under a
    known name wins at any depth over a discovered one nearer the cwd.

    Discovery is the fallback, so it cannot be part of the climb. This repo
    ships `resources/board/example/`, which is a board and is meant to be —
    `pearde example <dir>` copies it — so one pass that scanned as it went
    would resolve a command run from `resources/board/` to the example
    instead of to the repo's own board one level up, and the guard would
    start counting a session's blocks against a fixture. The same is true of
    any tree that keeps a board-shaped folder as data. So: climb for `pearde/`
    and `.pearde/` first, all the way to the root, and only then climb again
    asking which directory carries `settings.md`."""
    return walk_up(d, board_named) or walk_up(d, board_scanned)


def board_at(d):
    """The board directory of project dir `d` — whatever it is called, and
    the plain name when there is none, which is what a board made here will
    be called."""
    return board_in(d) or os.path.join(d, BOARD_DIR)


def state_dir(board):
    """`<board>/.state`, made if it is not there — but only INSIDE a board
    that is already there. Every writer goes through this, so the corner the
    tool writes into cannot be assumed to exist; the board holding it can.

    `makedirs` used to make both, and that turned every reader into a writer:
    `scan` — and so `plan`, `status` and the daemon's poll — loads the parse
    cache through here, so any caller handed a stale board path (`<project>/
    .pearde` after that board moved to `<project>/pearde` without leaving the
    compat symlink: the daemon's watch set and a master's `members:` are both
    full of absolute paths spelled the old way) quietly conjured a second,
    hollow board directory holding one file. That is how a repo ends up with
    two board directories and a session writing into the wrong one. A read
    must never create a board: the path is refused instead, loudly, and the
    caller is told to point at a board that exists.

    `is_board_dir`, not `os.path.isdir`: a path this defect has already run
    on holds a HUSK — a directory at the board's old name carrying nothing
    but the `.state/` the defect made. `isdir` is true of a husk for ever, so
    a guard written on it keeps writing into the very thing it was added to
    stop, and `serve.vanished()` — which drops on the same test — never drops
    it. Carrying a board is the only property that heals a machine the defect
    has already touched."""
    if not is_board_dir(board):
        raise NotABoard(
            f"no board at {board} — a read never creates one; point at the "
            f"board that is there, or `pearde init` beside it")
    d = os.path.join(board, STATE_DIR)
    os.makedirs(d, exist_ok=True)
    return d


def guard_dir(board):
    """`<board>/.state/guard` — the guard's session files for THIS board, one
    per session. `PEARDE_GUARD_STATE` moves it for both writer and reader, so
    a harness feeding hook JSON to a throwaway project writes nowhere real."""
    return os.environ.get("PEARDE_GUARD_STATE") or os.path.join(
        state_dir(board), "guard")


# ── the install used to be a writable place; it is not any more ──────────────
# `resources/board/state/` held the daemon's registry, its log, the
# calibration fit and the guard's session cache — pearde-created, outside
# every `.pearde/`. The invariant `every-artifact-lands-inside-the-board` now
# covers it: there is one root, the board's `.pearde/`, and every path pearde
# writes is relative to it. This name survives for one job — moving what an
# older install left behind into the boards it belongs to, once.
LEGACY_MACHINE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "state")


def migrate_legacy_state():
    """Move `resources/board/state/` into the boards it was holding state
    for, then delete it. Runs on import, costs one `isdir` after the first
    time, and never raises — a command must not fail because an old install
    left a file behind.

    Destinations are read before they are written: `<board>/.state/` holds
    live pass files and the history and transitions journals, and anything
    already there outranks anything the install kept. The daemon's own
    `serve.log` and the adapters' `run-*.log` are rolling tails belonging to
    no board and are dropped, not moved."""
    d = LEGACY_MACHINE_DIR
    if not os.path.isdir(d):
        return []
    moved = []
    try:
        with open(os.path.join(d, "serve.json"), encoding="utf-8") as fh:
            boards = [b for b in json.load(fh) if os.path.isdir(b)]
    except (OSError, ValueError, TypeError):
        boards = []
    calib = os.path.join(d, "calibration.json")
    for b in boards:
        try:
            sd = state_dir(b)
        except (OSError, SystemExit):   # `state_dir` refuses a board that went
            continue
        # the registry entry: one board's own row, in its own corner
        entry = os.path.join(sd, "serve.json")
        if not os.path.exists(entry):
            try:
                with open(entry, "w", encoding="utf-8") as fh:
                    json.dump({"path": os.path.abspath(b)}, fh, indent=1)
                moved.append(entry)
            except OSError:
                pass
        # the fit was machine-wide and is now per board — copied, not moved,
        # because every board that was in it has an equal claim on it, and
        # `pearde calibrate` refits from that board's own record anyway
        dst = os.path.join(sd, "calibration.json")
        if os.path.isfile(calib) and not os.path.exists(dst):
            try:
                shutil.copy2(calib, dst)
                moved.append(dst)
            except OSError:
                pass
    # the guard's session files, split by the board each block counted on: a
    # session that worked two boards becomes one file in each. Only the boards
    # the registry named — a session file keeps a block under whatever path it
    # was told, including spellings a board has since moved off, and a stale
    # one that still resolves to a directory would seed a `.state/` corner
    # nothing owns.
    known = {os.path.abspath(b) for b in boards}
    gd = os.path.join(d, "guard")
    for n in sorted(os.listdir(gd)) if os.path.isdir(gd) else []:
        if not n.endswith(".json"):
            continue
        try:
            with open(os.path.join(gd, n), encoding="utf-8") as fh:
                data = json.load(fh)
            blocks = data.get("boards") or {}
        except (OSError, ValueError, AttributeError):
            continue
        for bpath, block in blocks.items():
            if os.path.abspath(bpath) not in known:
                continue
            dst = os.path.join(bpath, STATE_DIR, "guard", n)
            if os.path.exists(dst):
                continue
            one = {k: v for k, v in data.items() if k != "boards"}
            one["boards"] = {bpath: block}
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, "w", encoding="utf-8") as fh:
                    json.dump(one, fh)
                moved.append(dst)
            except OSError:
                pass
    shutil.rmtree(d, ignore_errors=True)
    return moved


# On import, so every entry point carries it and none has to remember:
# one `isdir` after the first run, and a failure is never fatal.
try:
    migrate_legacy_state()
except Exception:  # noqa: BLE001 — a stale install must not break a command
    pass


def prds_dir(board):
    return os.path.join(board, PRDS_DIR)


def find_board(arg):
    if arg:
        p = os.path.abspath(arg)
        if os.path.basename(p) in BOARD_DIRS and is_board_dir(p):
            return board_link(p)
        b = board_in(p)
        if b:
            return b
        # the board named directly, under whatever it is called: the file only
        # a board carries, and asked for last so a project holding one still
        # resolves to the board inside it rather than to itself
        if os.path.isfile(os.path.join(p, SETTINGS)):
            return p
        die(f"no {BOARD_DIR}/ board at {arg}")
    b = board_above(os.getcwd())
    if b:
        return b
    die(f"no {BOARD_DIR}/ board found walking up from the cwd")


def die(msg, code=2):
    print(f"pearde: {msg}", file=sys.stderr)
    sys.exit(code)

# The pass's own memory — @references/parts/pass.md. Fifteen lines the
# orchestrator rewrites at every transition, so a compacted session recovers
# by reading one file instead of re-deriving the pass from the tree.
PASS_FILE = os.path.join(STATE_DIR, "pass.md")

class Flags:
    """What one command takes: `valued` are `--name <v>` (or `--name=<v>`),
    `switches` are bare, `multi` are the valued ones that repeat. `str()` is
    the list the refusal and `--help` print — one list, so they cannot
    drift. transitions.py `Args` is the one parser of it; the class is here
    because that module imports this one, and the two commands below declare
    at import time."""

    def __init__(self, valued=(), switches=(), multi=()):
        self.valued, self.switches = tuple(valued), tuple(switches)
        self.multi = tuple(multi)

    def __str__(self):
        return (", ".join("--" + k for k in self.valued + self.switches)
                or "no flags")
EXAMPLE_FLAGS = Flags()

# ── the example board ─────────────────────────────────────────────────────────
# resources/board/example/ — one small board with a row in every band. Every
# check in this repo runs against a COPY of it: a check that ticks a box in
# the example changes what every other check sees.
EXAMPLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "example")


def cmd_example(argv):
    """`pearde example <dir>` — copy the example board to <dir>. Refuses an
    existing non-empty directory; an empty or missing one is filled. Prints
    the board path and the scan to run next. argv is everything after the
    command name, the return is the exit code. It declares no flag, and
    refuses one before anything is copied, exit 2."""
    import transitions as translib       # the parser; it imports this module
    try:
        args = translib.Args(argv, EXAMPLE_FLAGS, "example")
    except translib.FlagRefused as e:
        print(f"pearde example: {e}", file=sys.stderr)
        return 2
    if len(args.pos) != 1:
        print("usage: plan.py example <dir>", file=sys.stderr)
        return 2
    dest = os.path.abspath(args.pos[0])
    if os.path.isdir(dest) and os.listdir(dest):
        print(f"pearde: {dest} exists and is not empty — pick an empty or "
              "new directory", file=sys.stderr)
        return 2
    if os.path.exists(dest) and not os.path.isdir(dest):
        print(f"pearde: {dest} is a file, not a directory", file=sys.stderr)
        return 2
    board = os.path.join(dest, BOARD_DIR)
    try:
        import shutil
        shutil.copytree(EXAMPLE, board, dirs_exist_ok=True)
    except OSError as e:
        print(f"pearde: could not copy the example to {board} — {e}",
              file=sys.stderr)
        return 2
    print(f"example: {os.path.join(board, PRDS_DIR)}")
    print(f"      python3 {os.path.join(HERE, 'plan.py')} scan {dest}")
    return 0
