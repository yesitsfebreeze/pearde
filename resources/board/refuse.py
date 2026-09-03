#!/usr/bin/env python3
"""refuse — a git command that discards uncommitted work is refused in a tree
the running session does not own.

    refuse.py tree [<path>] [--board <p>] [--json]   who owns this tree
    refuse.py cmd  '<shell line>' [--cwd <p>] [--board <p>] [--json]

`@resources/board/session.py` says WHO holds which tree. This module is the
other half of the same decision: what may be RUN in one. The memo is
`pearde/memos/a-session-that-writes-a-shared-checkout-can-revert-another-
session-s-work.md` — on 2026-09-02 three orchestrator sessions shared one
checkout, `collect`'s `unland` ran `git reset --hard` in it, and the entire
uncommitted implementation of another session's PRD was destroyed with no
object in the store to recover it from. Fixing that one call site left every
call site that was not found, which is why this is a mechanism and not a
patch: **`reset --hard`, `checkout --`, `clean` and a real `stash` are refused
in any tree the running session does not own** — in the board's own code and
in a session's own shell.

**What counts as destructive.** Only a command that can leave uncommitted
bytes nowhere git can reach. `git stash create` is not one: it writes a commit
object and leaves the worktree alone — it is what the reaper uses precisely
because it is safe. `git clean -n` is not one. `git restore --staged` alone
moves the index, not the worktree. The table is `SPELLINGS`, and every row
names the discard it can do.

**What counts as owning.** Two answers, and the second is why this is not
just `session owns`:

  1. The ledger holds a session tree and this session's pid is on that row.
  2. The command targets the very worktree the running process is working
     inside, and no OTHER live session on the ledger holds it.

Rule 2 is what keeps the mechanism usable. A worker runs in a lane
(`@resources/board/lanes.py`), a lane is on no session ledger, and a rule that
read the ledger alone would refuse a worker every legitimate `git clean` in
its own lane. It is also what keeps a person's own shell in the main checkout
working. The harm the memo records is not a process cleaning up after itself;
it is a session reaching OUT of its own tree into a tree another session is
writing, and that is exactly what rule 2 refuses.

A tree with no board above it is nobody's business here — there is no ledger,
so there is no ownership to be had, and `allowed()` says yes.

Python 3 stdlib only, and it imports nothing from the board's other modules:
`@resources/guard.py` calls this on every Bash tool call and keeps the rule
that a broken planner never blocks one, so `board` is always passed in and
never found here.
"""
import json
import os
import re
import shlex
import subprocess
import sys

SESSIONS_DIR = ".sessions"
LEDGER = os.path.join(".state", "sessions.json")
LANES_DIR = ".lanes"

# ── what discards ────────────────────────────────────────────────────────────
# One row per git verb that can leave uncommitted bytes unreachable. The
# predicate reads the verb's own arguments; a verb whose predicate says no is
# the same verb in a spelling that cannot discard, and it passes through.


def _has(args, *flags):
    return any(a in flags for a in args)


def _reset(args):
    # --hard throws the worktree away. --keep and --merge refuse rather than
    # discard, and `e5abc5b` replaced the unland call with --keep for exactly
    # that reason; --soft and --mixed never touch the worktree.
    return "--hard" in args


def _checkout(args):
    # `checkout -- <path>` overwrites the path from the index; `-f` overwrites
    # the whole tree. A plain `checkout <branch>` refuses when it would lose
    # work, so it is not one of these.
    return "--" in args or _has(args, "-f", "--force")


def _restore(args):
    # The modern spelling of `checkout --`, and the default target is the
    # worktree. `--staged` on its own moves only the index.
    return not (_has(args, "--staged", "-S") and
                not _has(args, "--worktree", "-W"))


def _clean(args):
    # Deletes untracked files outright — the one command in this table whose
    # damage no index and no stash can undo. `-n`/`--dry-run` prints instead.
    return not _has(args, "-n", "--dry-run")


STASH_SAFE = ("create", "store", "list", "show", "branch", "drop", "clear")


def _stash(args):
    # "A real stash", the memo's words. `push`/`save` revert the worktree to
    # HEAD; `pop`/`apply` write over it. `create` builds a commit object and
    # touches nothing — it is what @resources/board/session.py's reaper uses.
    # A bare `git stash` is `push`.
    sub = next((a for a in args if not a.startswith("-")), "push")
    return sub not in STASH_SAFE


def _switch(args):
    return _has(args, "-f", "--force", "--discard-changes")


SPELLINGS = {
    "reset": (_reset, "reset --hard throws the working tree away"),
    "checkout": (_checkout, "checkout -- overwrites the working tree"),
    "restore": (_restore, "restore overwrites the working tree"),
    "clean": (_clean, "clean deletes untracked files outright"),
    "stash": (_stash, "a real stash reverts the working tree"),
    "switch": (_switch, "switch --discard-changes throws the tree away"),
}

# git's own global options, the ones that take a value. Needed to find the
# verb: in `git -C /x -c a=b reset --hard`, the verb is the 5th token.
GLOBAL_WITH_VALUE = ("-C", "-c", "--git-dir", "--work-tree", "--namespace",
                     "--exec-path", "--config-env")
SHELL_BREAK = (";", "&&", "||", "|", "&", "\n")


def invocations(line):
    """Every `git …` invocation in one shell line, as (argv, cd) pairs, where
    `cd` is the directory a `cd` earlier in the same line moved to, or None.

    A `cd` holds for the REST of the line, not for the segment before the next
    `&&`. `cd /x && git clean -fdx` is how an agent writes this by hand more
    often than any other spelling, and reading the `cd` as scoped made the
    reader answer "no destructive git" for the exact case the module exists
    for — measured, before this line was written.

    Not a shell parser and not trying to be — a line this cannot read yields
    nothing, and the caller treats that as "no destructive git found", the
    same answer it gives for a line that holds none. The guard is a second
    line of defence over the board's own call sites, never the only one."""
    try:
        toks = shlex.split(line, comments=True)
    except ValueError:
        return []
    out, cd, i = [], None, 0
    while i < len(toks):
        t = toks[i]
        if t in SHELL_BREAK:
            i += 1
            continue
        if t == "cd" and i + 1 < len(toks):
            cd = toks[i + 1]
            i += 2
            continue
        if os.path.basename(t) == "git":
            j = i + 1
            argv = []
            while j < len(toks) and toks[j] not in SHELL_BREAK:
                argv.append(toks[j])
                j += 1
            out.append((argv, cd))
            i = j
            continue
        i += 1
    return out


def verb_of(argv):
    """The git verb and the arguments after it, skipping git's own global
    options, plus the `-C` directory when one is given."""
    i, at = 0, None
    while i < len(argv):
        a = argv[i]
        if a == "-C" and i + 1 < len(argv):
            at = argv[i + 1]
            i += 2
            continue
        if a in GLOBAL_WITH_VALUE and i + 1 < len(argv):
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        return a, argv[i + 1:], at
    return None, [], at


def destructive(line):
    """Every destructive git in one shell line: (verb, target dir or None,
    why). Empty when the line holds none this reader can see."""
    found = []
    for argv, cd in invocations(line):
        verb, args, at = verb_of(argv)
        if verb not in SPELLINGS:
            continue
        pred, why = SPELLINGS[verb]
        if not pred(args):
            continue
        found.append((verb, at or cd, why))
    return found


# ── who owns a tree ──────────────────────────────────────────────────────────

def _run(*args, cwd=None):
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                           timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def toplevel(path):
    """The root of the worktree `path` sits in, or None."""
    d = path if os.path.isdir(path) else os.path.dirname(path) or "."
    if not os.path.isdir(d):
        return None
    return _run("git", "-C", d, "rev-parse", "--show-toplevel")


def read_ledger(board):
    """The session ledger, read by hand. A ledger that will not parse is an
    EMPTY ledger and never an error: this runs inside a PreToolUse hook, and a
    hook that raises is a session that cannot use a tool."""
    try:
        with open(os.path.join(board, LEDGER), encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError):
        return []
    rows = d.get("sessions") if isinstance(d, dict) else d
    return rows if isinstance(rows, list) else []


def _ps_started(pid):
    out = _run("ps", "-o", "lstart=", "-p", str(pid))
    return out if out is None else out.strip()


def alive(row):
    """`alive` | `dead` | `unknown`, the same three-valued test
    @resources/board/session.py `liveness` makes, by hand and for the same
    reason the ledger is read by hand here. Only `dead` frees a tree, and
    `unknown` never does."""
    pid = row.get("pid")
    if not isinstance(pid, int):
        return "unknown"
    got = _ps_started(pid)
    if got is None:
        return "unknown"                    # ps would not answer
    if got == "":
        return "dead"                       # ps answered: the pid is gone
    want = (row.get("started") or "").strip()
    if want and " ".join(got.split()) != " ".join(want.split()):
        return "dead"                       # a reused pid is not that session
    return "alive"


def session_pid(env=None):
    """This session's pid: the first `claude` walking up the process tree, or
    `PEARDE_SESSION_PID`. Duplicated from @resources/board/session.py rather
    than imported — see the module docstring."""
    env = os.environ if env is None else env
    forced = env.get("PEARDE_SESSION_PID")
    if forced:
        try:
            return int(forced)
        except ValueError:
            return None
    pid = os.getpid()
    for _ in range(64):
        cmd = _run("ps", "-o", "comm=", "-p", str(pid))
        if cmd and os.path.basename(cmd.strip()) == "claude":
            return pid
        up = _run("ps", "-o", "ppid=", "-p", str(pid))
        if not up:
            return None
        try:
            nxt = int(up.strip())
        except ValueError:
            return None
        if nxt <= 1 or nxt == pid:
            return None
        pid = nxt
    return None


def holder(board, tree, mine=None):
    """The ledger row holding `tree`, and whether it is this session's.
    Returns (row or None, "mine" | "theirs" | "dead" | None)."""
    if mine is None:
        mine = session_pid()
    t = os.path.abspath(tree)
    for r in read_ledger(board):
        wt = os.path.abspath(r.get("worktree") or "")
        if not wt or not (t == wt or t.startswith(wt + os.sep)):
            continue
        if r.get("pid") == mine and mine is not None:
            return r, "mine"
        return r, ("dead" if alive(r) == "dead" else "theirs")
    return None, None


def allowed(board, tree, cwd=None, mine=None):
    """May a destructive git run in `tree`? Returns (bool, reason).

    The two ways to own it are the module docstring's, in that order. A tree
    with no board above it has no ledger and so no ownership: allowed."""
    if not board:
        return True, "no board above this tree — no ledger, no ownership"
    tree = os.path.abspath(tree)
    row, how = holder(board, tree, mine)
    if how == "mine":
        return True, f"this session holds it ({row.get('id')})"
    if how == "theirs":
        return False, (f"{row.get('id')} holds this tree and is alive — "
                       "its uncommitted work is not yours to discard")
    if how == "dead":
        return False, (f"{row.get('id')} holds this tree and is gone — "
                       "`pearde session reap --apply` snapshots it first")
    # Rule 2: the tree the running process is itself working inside.
    here = toplevel(cwd or os.getcwd())
    if here and os.path.abspath(here) == tree:
        return True, "this process is working inside it, and no session holds it"
    return False, ("this session does not own it — it is neither the tree on "
                   "this session's ledger row nor the tree this process is "
                   "working in")


def refuse_line(verb, tree, reason, why):
    return (f"git {verb} refused in {tree}: {reason}.\n"
            f"{why}, and the memo is "
            "pearde/memos/a-session-that-writes-a-shared-checkout-can-revert-"
            "another-session-s-work.md — three sessions shared one checkout "
            "and a reset --hard destroyed a whole uncommitted PRD.\n"
            "Run it in the tree `pearde session take` gave this session, or "
            "snapshot first: git -C <tree> stash create, then stash store.")


class Refused(Exception):
    """Raised by `guard` — the board's own call sites catch it and report."""


def guard(board, tree, verb, why="", cwd=None):
    """The board's own code calls this before it runs one of these. Raises
    `Refused` when the tree is not this session's to discard."""
    ok, reason = allowed(board, tree, cwd)
    if not ok:
        raise Refused(refuse_line(verb, tree, reason, why or
                                  SPELLINGS.get(verb, (None, "it discards "
                                                       "uncommitted work"))[1]))
    return True


def check_line(board, line, cwd=None):
    """Every refusal a shell line earns: [(verb, tree, reason, why)].

    The board that decides is the one above the TREE BEING DISCARDED, not the
    one above the cwd. Measured: `git -C <a peer's session tree> reset --hard`
    typed from a directory with no board above it went through unchecked when
    the cwd's board was the only one consulted — and the ledger that would
    have refused it was sitting one directory above the target the whole
    time. The passed-in board is the fallback, for the ordinary case where
    the target IS the cwd."""
    out = []
    for verb, at, why in destructive(line):
        base = cwd or os.getcwd()
        target = os.path.abspath(os.path.join(base, at)) if at else \
            os.path.abspath(base)
        tree = toplevel(target) or target
        b = board_above(None, tree) or board
        ok, reason = allowed(b, tree, cwd)
        if not ok:
            out.append((verb, tree, reason, why))
    return out


# ── the command ──────────────────────────────────────────────────────────────

def board_above(arg, start=None):
    """The nearest board at or above `start`, or the one named. Walked here
    with os.path alone so this module keeps importing nothing."""
    if arg:
        return os.path.abspath(arg)
    d = os.path.abspath(start or os.getcwd())
    while True:
        for name in ("pearde", ".pearde"):
            b = os.path.join(d, name)
            if os.path.isfile(os.path.join(b, "settings.md")):
                return b
        up = os.path.dirname(d)
        if up == d:
            return None
        d = up


def cmd_refuse(argv):
    """what a destructive git may do in this tree, and why"""
    verb = argv[0] if argv and argv[0] in ("tree", "cmd") else "tree"
    rest = list(argv[1:] if argv and argv[0] in ("tree", "cmd") else argv)
    opts, pos = {}, []
    i = 0
    while i < len(rest):
        a = rest[i]
        if a in ("--board", "--cwd") and i + 1 < len(rest):
            opts[a[2:]] = rest[i + 1]
            i += 2
            continue
        if a == "--json":
            opts["json"] = True
            i += 1
            continue
        pos.append(a)
        i += 1
    cwd = opts.get("cwd") or os.getcwd()
    board = board_above(opts.get("board"), cwd)
    if verb == "cmd":
        line = pos[0] if pos else ""
        bad = check_line(board, line, cwd)
        if opts.get("json"):
            print(json.dumps([{"verb": v, "tree": t, "reason": r}
                              for v, t, r, _ in bad], indent=2))
        elif not bad:
            print(f"allowed — nothing in this line discards work in a tree "
                  f"{'this session does not own' if board else 'under a board'}")
        else:
            for v, t, r, w in bad:
                print(refuse_line(v, t, r, w), file=sys.stderr)
        return 3 if bad else 0
    tree = toplevel(pos[0] if pos else cwd) or os.path.abspath(
        pos[0] if pos else cwd)
    ok, reason = allowed(board, tree, cwd)
    if opts.get("json"):
        print(json.dumps({"tree": tree, "board": board, "allowed": ok,
                          "reason": reason}, indent=2))
    else:
        print(f"{tree} — {'allowed' if ok else 'refused'}: {reason}")
    return 0 if ok else 3


cmd_refuse.flags = "--board <path> --cwd <path> --json"
COMMANDS = {"refuse": cmd_refuse}


if __name__ == "__main__":
    sys.exit(cmd_refuse(sys.argv[1:]))
