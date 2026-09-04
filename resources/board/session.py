#!/usr/bin/env python3
"""pearde session — one worktree per run session, a ledger of who holds
which, and a reaper that snapshots before it deletes.

    session.py take  [<board>] [--board <path>] [--json]
    session.py list  [<board>] [--board <path>] [--json]
    session.py reap  [<board>] [--board <path>] [--apply] [--json]
    session.py land  [<board>] [--board <path>] [--dry] [--json]
    session.py owns  [<path>] [--board <path>] [--json]

`@resources/board/lanes.py` gives every WORKER a worktree. It gives the
session that dispatches them nothing, and on 2026-09-02 three orchestrator
sessions shared one checkout and two of them lost work — the whole of it in
`.pearde/memos/a-session-that-writes-a-shared-checkout-can-revert-another-
session-s-work.md`. This module is the layer above lanes: the session takes a
checkout of its own before it dispatches anything, the ledger records who
holds what, and a new session reaps what is gone.

**Who a session is.** The process tree, walked up from this process to the
first `claude` process — `take` from a session's own shell finds that
session's pid and nothing else, because every command a session runs is a
descendant of it. `PEARDE_SESSION_PID` overrides it, which is how the probe
drives this without a session. The id is `s<pid>`; the ledger also stores the
process's start time, because a pid is reused and a start time is not.

**Liveness is three-valued, and only `dead` reaps.** Alive when the pid is
running and its start time matches the ledger's. Dead when the pid is gone,
or running under a start time that is not the recorded one — a reused pid.
**Unknown** when `ps` will not answer at all, and unknown never reaps: the
false positive here destroys exactly the work this module exists to protect,
so the test is conservative by construction. `/tmp/cc-socks/<pid>.sock` is
corroboration when it is there and never a verdict on its own — a session
whose socket a cleanup removed is still a session.

**The reaper snapshots first, and never touches the tree it snapshots.**
`git stash push -u` would do it, but stash is one of the four commands the
memo puts out of bounds in a tree the running session does not own, and it
reverts the worktree before the removal that may then fail. So the snapshot
is built in a COPY of the dead worktree's own index — `add -A` into it, then
`write-tree` and `commit-tree` — and stored as `refs/pearde/reaped/<id>`.
Measured: tracked edits, staged renames, untracked files and untracked nested
directories all land in that commit, the worktree is byte-identical
afterwards, and the ref outlives `worktree remove`. The index is COPIED
rather than read fresh from HEAD so the lane's sparse-checkout exclusions keep
their skip-worktree bit; a fresh `read-tree HEAD` reads every excluded path as
deleted and writes a snapshot that drops it.

Gitignored paths are not in the snapshot — `add -A` does not see them, and the
board itself is one, so a reap that captured them would write the whole
machine-local corner into the object store on every sweep.

The BRANCH stays, the way `lanes.remove` keeps a swept lane's branch: an
unmerged session branch is work this machine holds.

Ledger: `<board>/.state/sessions.json`, beside `serve.json`. Machine-local,
regenerable from `git worktree list` and gitignored — the same kind of thing
as the daemon's own registration, and no more a registry of configuration
than that one is.

Python 3 stdlib only.
"""
import json
import os
import re
import subprocess
import sys
import time

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import plan as planlib    # noqa: E402
import lanes as laneslib  # noqa: E402

SESSIONS_DIR = ".sessions"
LEDGER = "sessions.json"
SNAP_REF = "refs/pearde/reaped/"
SOCKS = "/tmp/cc-socks"

FLAGS = planlib.Flags(("board",), ("json", "apply", "dry"))


# ── who this session is ──────────────────────────────────────────────────────

def _ps(pid, fmt):
    try:
        r = subprocess.run(["ps", "-o", fmt, "-p", str(pid)],
                           capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None                      # unknown, never "gone"
    if r.returncode != 0:
        return ""                        # ps ran and the pid is not there
    return r.stdout.strip()


def parent(pid):
    out = _ps(pid, "ppid=")
    return int(out) if out and out.strip().isdigit() else None


def command(pid):
    out = _ps(pid, "command=")
    return out.strip() if out else out


def started(pid):
    """The pid's start time as `ps` prints it — the pid-reuse guard. `lstart`
    is second-resolution and stable for the life of the process on both
    macOS and Linux; `etime` is not, it counts up."""
    out = _ps(pid, "lstart=")
    return out.strip() if out else out


SESSION_CMD = re.compile(r"(^|/)claude(\s|$)")


def session_pid():
    """The pid of the session this call is running inside — the nearest
    ancestor whose command is `claude`. None when the walk reaches init
    without finding one, which is a call from outside a session."""
    env = os.environ.get("PEARDE_SESSION_PID")
    if env and env.strip().isdigit():
        return int(env.strip())
    pid, seen = os.getpid(), 0
    while pid and pid > 1 and seen < 40:
        cmd = command(pid)
        if cmd and SESSION_CMD.search(cmd.split(" --")[0]):
            return pid
        pid, seen = parent(pid), seen + 1
    return None


def sid(pid):
    return "s%d" % pid


_MINE = {}


def my_id():
    """`s<pid>` for the session this process runs inside, cached for the life
    of the process. `session_pid` costs one `ps` fork per step of the walk up
    the process tree, and `held` below is asked once per PRD by every scan —
    the daemon's included, once a second per board. A process cannot change
    which session it is inside, so the answer is computed once."""
    if "id" not in _MINE:
        pid = session_pid()
        _MINE["id"] = sid(pid) if pid else None
    return _MINE["id"]


# ── the ledger ───────────────────────────────────────────────────────────────

def ledger_path(board):
    return os.path.join(planlib.state_dir(board), LEDGER)


def read_ledger(board):
    try:
        with open(ledger_path(board), encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return []
    rows = data.get("sessions") if isinstance(data, dict) else data
    return [r for r in (rows or []) if isinstance(r, dict) and r.get("id")]


def write_ledger(board, rows):
    path = ledger_path(board)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"version": 1, "sessions": rows}, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def row_of(rows, ident):
    for r in rows:
        if r.get("id") == ident:
            return r
    return None


_LEDGER_CACHE = {}


def cached_ledger(board):
    """`read_ledger` behind an mtime check. Same reason as `my_id`: the
    resolver below is on the scan's per-PRD path, and re-parsing the ledger
    for every PRD on a 140-PRD board is a file read a hundred and forty
    times for an answer that changed on none of them."""
    path = ledger_path(board)
    try:
        st = os.stat(path)
        stamp = (st.st_mtime_ns, st.st_size)
    except OSError:
        stamp = None
    hit = _LEDGER_CACHE.get(board)
    if hit and hit[0] == stamp:
        return hit[1]
    rows = read_ledger(board) if stamp else []
    _LEDGER_CACHE[board] = (stamp, rows)
    return rows


def held(board, repo=None):
    """The worktree THIS session holds on `board`, or None.

    The one question every board command asks before it names a code repo.
    None is the ordinary answer, not a failure: a command run outside a
    session, a session that has not `take`n, a worker inside its own lane,
    and a board whose ledger names a tree that is no longer on disk all
    resolve to the checkout exactly as they did before this existed.

    `repo`, when given, is the checkout the caller resolved by walk-up; a
    ledger row for a DIFFERENT repo is not this board's answer. That is what
    keeps a master board — whose members are other repos — from handing one
    member's PRD the session tree of another.

    The tree must still be a worktree: a session whose directory was removed
    under it (a reap that raced, a person with `rm -rf`) falls back to the
    checkout rather than handing every command a path that is not there."""
    ident = my_id()
    if not ident:
        return None
    row = row_of(cached_ledger(board), ident)
    if not row:
        return None
    tree = row.get("worktree") or ""
    if not tree or not os.path.exists(os.path.join(tree, ".git")):
        return None
    if repo and os.path.realpath(row.get("repo") or "") != os.path.realpath(repo):
        return None
    return os.path.abspath(tree)


def instead_of(board, repo):
    """`repo`, or the session's own worktree of it. The call every resolver
    makes: it never returns None and never raises, so a resolver that was
    correct before stays correct when the ledger is empty or unreadable."""
    if not repo:
        return repo
    try:
        return held(board, repo) or repo
    except Exception:
        return repo


# ── liveness ─────────────────────────────────────────────────────────────────

ALIVE, DEAD, UNKNOWN = "alive", "dead", "unknown"


def liveness(row):
    """(verdict, why). Only DEAD is reapable."""
    pid = row.get("pid")
    if not isinstance(pid, int) or pid <= 1:
        return UNKNOWN, "no pid on the row"
    now = started(pid)
    if now is None:
        return UNKNOWN, "ps would not answer"
    if now == "":
        return DEAD, f"pid {pid} is gone"
    was = (row.get("started") or "").strip()
    if not was:
        return UNKNOWN, f"pid {pid} runs, and the row records no start time"
    if now != was:
        return DEAD, f"pid {pid} was reused — started {now}, not {was}"
    return ALIVE, f"pid {pid} running since {now}"


def has_sock(row):
    pid = row.get("pid")
    return bool(pid) and os.path.exists(os.path.join(SOCKS, f"{pid}.sock"))


# ── the worktree ─────────────────────────────────────────────────────────────

def branch_of(ident):
    return "session/" + re.sub(r"[^A-Za-z0-9._-]+", "-", str(ident)).strip("-")


def tree_of(board, ident):
    return os.path.join(board, SESSIONS_DIR,
                        re.sub(r"[^A-Za-z0-9._-]+", "-", str(ident)).strip("-"))


def repo_of(board):
    """The code repo the board sits in — `collect.repo_of` without a PRD to
    ask. A board that is its own worktree resolves to the repo enclosing it."""
    root = planlib.repo_root(board)
    if root and os.path.abspath(root) == os.path.abspath(board):
        enclosing = planlib.repo_root(os.path.dirname(root))
        if enclosing:
            return enclosing
    return root


def create(board, repo, ident):
    """Cut `session/<id>` and check it out at `<board>/.sessions/<id>`,
    with the board excluded exactly the way a lane excludes it. Idempotent
    on the path."""
    d = tree_of(board, ident)
    br = branch_of(ident)
    if os.path.isdir(d):
        if os.path.exists(os.path.join(d, ".git")):
            return d
        raise laneslib.LaneError(
            f"session: {d} exists and is not a worktree — move it or remove it")
    os.makedirs(os.path.dirname(d), exist_ok=True)
    have = laneslib.git(repo, "rev-parse", "--verify", "--quiet", br,
                        check=False).returncode == 0
    if have:
        laneslib.git(repo, "worktree", "add", "--no-checkout", d, br)
    else:
        laneslib.git(repo, "worktree", "add", "--no-checkout", "-b", br, d)
    rel = laneslib.board_rel(board, repo)
    if rel:
        laneslib.git(d, "sparse-checkout", "set", "--no-cone",
                     "/*", "!/" + rel, check=False)
    laneslib.git(d, "checkout")
    laneslib.link_board(board, repo, d)
    return d


def git_dir(tree):
    out = laneslib.git(tree, "rev-parse", "--absolute-git-dir",
                       check=False).stdout.strip()
    return out or None


def snapshot(repo, tree, ident):
    """Commit everything standing in `tree` — tracked edits, staged state and
    untracked files — under `refs/pearde/reaped/<id>`, without touching the
    tree. Returns (sha, files) or (None, []) when the tree is clean.

    The index is a copy of the worktree's own, so skip-worktree bits survive
    and a sparse exclusion is not snapshotted as a deletion."""
    gd = git_dir(tree)
    if not gd:
        return None, []
    idx = os.path.join(gd, "pearde-reap-index")
    src = os.path.join(gd, "index")
    try:
        if os.path.exists(src):
            with open(src, "rb") as a, open(idx, "wb") as b:
                b.write(a.read())
        elif os.path.exists(idx):
            os.remove(idx)
    except OSError as e:
        raise laneslib.LaneError(f"session: cannot copy the index of {tree}: {e}")
    env = dict(os.environ, GIT_INDEX_FILE=idx)

    def g(*args, check=True):
        r = subprocess.run(("git", "-C", tree) + args, env=env,
                           capture_output=True, text=True, timeout=120)
        if check and r.returncode != 0:
            raise laneslib.LaneError((r.stderr or r.stdout).strip())
        return r

    try:
        if not os.path.exists(src):
            g("read-tree", "HEAD", check=False)
        g("add", "-A")
        head = laneslib.git(tree, "rev-parse", "HEAD", check=False).stdout.strip()
        tree_sha = g("write-tree").stdout.strip()
        if head:
            head_tree = laneslib.git(
                tree, "rev-parse", "HEAD^{tree}", check=False).stdout.strip()
            if tree_sha == head_tree:
                return None, []          # nothing standing: no snapshot
        files = [l for l in g("diff", "--name-only", "--cached", head or
                              "4b825dc642cb6eb9a060e54bf8d69288fbee4904",
                              check=False).stdout.splitlines() if l.strip()]
        msg = f"pearde reap snapshot of {ident} — {time.strftime('%Y-%m-%d %H:%M:%S')}"
        args = ["commit-tree", tree_sha, "-m", msg]
        if head:
            args += ["-p", head]
        sha = g(*args).stdout.strip()
    finally:
        try:
            os.remove(idx)
        except OSError:
            pass
    laneslib.git(repo, "update-ref", SNAP_REF + str(ident), sha)
    return sha, files


# ── the commands ─────────────────────────────────────────────────────────────

def cmd_take(board, as_json=False):
    pid = session_pid()
    if pid is None:
        print("session take: no session process above this one — "
              "run it from a session, or set PEARDE_SESSION_PID",
              file=sys.stderr)
        return 2
    repo = repo_of(board)
    if not repo:
        print(f"session take: no git repo above {board}", file=sys.stderr)
        return 2
    ident = sid(pid)
    rows = read_ledger(board)
    row = row_of(rows, ident)
    try:
        tree = create(board, repo, ident)
    except laneslib.LaneError as e:
        print(f"session take: {e}", file=sys.stderr)
        return 1
    fresh = row is None
    if fresh:
        row = {"id": ident}
        rows.append(row)
    row.update({"pid": pid, "started": started(pid) or "",
                "cmd": (command(pid) or "")[:200],
                "worktree": os.path.abspath(tree), "branch": branch_of(ident),
                "repo": os.path.abspath(repo),
                "taken": row.get("taken") or time.strftime("%Y-%m-%d %H:%M:%S"),
                "host": os.uname().nodename})
    write_ledger(board, rows)
    if as_json:
        print(json.dumps(row, indent=2))
    else:
        print(f"session {ident} · {'took' if fresh else 'holds'} "
              f"{row['worktree']} · {row['branch']}")
    return 0


def cmd_list(board, as_json=False):
    rows = read_ledger(board)
    out = []
    mine = session_pid()
    for r in rows:
        v, why = liveness(r)
        out.append(dict(r, alive=v, why=why, sock=has_sock(r),
                        mine=(r.get("pid") == mine),
                        exists=os.path.isdir(r.get("worktree") or "")))
    if as_json:
        print(json.dumps({"sessions": out}, indent=2))
        return 0
    if not out:
        print("no sessions on the ledger")
        return 0
    for r in out:
        mark = "*" if r["mine"] else " "
        gone = "" if r["exists"] else " · tree gone"
        sock = " · sock" if r["sock"] else ""
        print(f"{mark} {r['id']:<10} {r['alive']:<8} {r['why']}{sock}{gone}")
        print(f"    {r.get('worktree','')}")
    return 0


def cmd_reap(board, apply=False, as_json=False):
    """Snapshot and remove the worktree of every session on the ledger that
    is provably gone. A live session, and a session whose liveness cannot be
    decided, is never touched — and neither is this one."""
    repo = repo_of(board)
    rows = read_ledger(board)
    mine = session_pid()
    acts, keep = [], []
    for r in rows:
        v, why = liveness(r)
        if r.get("pid") == mine and mine is not None:
            keep.append(r)
            acts.append({"id": r["id"], "do": "keep", "why": "this session"})
            continue
        if v != DEAD:
            keep.append(r)
            acts.append({"id": r["id"], "do": "keep", "why": f"{v}: {why}"})
            continue
        tree = r.get("worktree") or ""
        act = {"id": r["id"], "do": "reap", "why": why, "worktree": tree}
        if not os.path.isdir(tree):
            act["do"] = "forget"
            act["why"] = why + " · worktree already gone"
            acts.append(act)
            if apply:
                continue
            keep.append(r)
            continue
        if apply:
            try:
                sha, files = snapshot(repo, tree, r["id"])
                act["snapshot"] = sha
                act["files"] = files
                laneslib.git(repo, "worktree", "remove", "--force", tree)
                laneslib.git(repo, "worktree", "prune", check=False)
                act["removed"] = True
            except laneslib.LaneError as e:
                act["do"] = "failed"
                act["why"] = str(e)
                keep.append(r)
                acts.append(act)
                continue
        else:
            keep.append(r)
        acts.append(act)
    if apply:
        write_ledger(board, keep)
    if as_json:
        print(json.dumps({"applied": bool(apply), "actions": acts}, indent=2))
        return 0
    todo = [a for a in acts if a["do"] in ("reap", "forget")]
    for a in acts:
        if a["do"] == "keep":
            print(f"  keep   {a['id']:<10} {a['why']}")
    for a in todo:
        snap = a.get("snapshot")
        tail = (f" · snapshot {snap[:12]} ({len(a.get('files') or [])} files) "
                f"at {SNAP_REF}{a['id']}" if snap else "")
        print(f"  {a['do']:<6} {a['id']:<10} {a['why']}{tail}")
    for a in acts:
        if a["do"] == "failed":
            print(f"  failed {a['id']:<10} {a['why']}", file=sys.stderr)
    if not apply and todo:
        print(f"{len(todo)} to reap — `pearde session reap --apply` does it")
    if apply:
        print(f"reaped {len([a for a in todo if a.get('removed')])}, "
              f"{len(keep)} left on the ledger")
    return 1 if any(a["do"] == "failed" for a in acts) else 0


def branch_read_by_a_person(repo):
    """The branch the checkout is on — what a person sees when they open the
    repo. Not `main` by name: a board on a repo whose trunk is `master`, or a
    person parked on a release branch, reads that one."""
    out = laneslib.git(repo, "rev-parse", "--abbrev-ref", "HEAD",
                       check=False).stdout.strip()
    return out if out and out != "HEAD" else None


def land(board, ident=None, dry=False):
    """Put this session's commits on the branch the person reads.

    `lanes.merge` one level up, and for the same reason. The session's tree
    is where every board command now commits, so its branch is where a PRD
    lands — and a branch nobody checks out is not a place work has arrived.
    Rebase `session/<id>` onto the checkout's branch and `merge --ff-only`
    there: a plain merge writes a second commit for the PRD and
    @references/parts/commits.md allows one, and `--squash` leaves the
    branch reading unmerged forever.

    Two things it will not do. It never rebases a branch another worktree
    holds — git refuses, and so does this, by name. And it never forces the
    checkout: `merge --ff-only` is what runs there, so a checkout with
    uncommitted work of its own fails the merge and keeps that work. That
    failure is the answer, not an error to route around — the four
    destructive commands stay out of a tree this session does not own.

    Returns (branch, target, landed) or (branch, target, 0)."""
    repo = repo_of(board)
    if not repo:
        raise laneslib.LaneError(f"no git repo above {board}")
    ident = ident or my_id()
    if not ident:
        raise laneslib.LaneError(
            "no session process above this one — run it from a session, "
            "or set PEARDE_SESSION_PID")
    row = row_of(read_ledger(board), ident)
    if not row:
        raise laneslib.LaneError(f"{ident} holds no worktree on this board — "
                                 "`pearde session take` first")
    br = row.get("branch") or branch_of(ident)
    target = branch_read_by_a_person(repo)
    if not target:
        raise laneslib.LaneError(f"{repo} is on no branch — nothing to land on")
    if target == br:
        raise laneslib.LaneError(
            f"the checkout is on {br} itself — it is already the branch a "
            "person reads")
    if laneslib.git(repo, "rev-parse", "--verify", "--quiet", br,
                    check=False).returncode != 0:
        return br, target, 0
    ahead = laneslib.git(repo, "rev-list", "--count", f"{target}..{br}",
                         check=False).stdout.strip()
    if ahead in ("", "0"):
        return br, target, 0
    if dry:
        return br, target, int(ahead)
    wt = laneslib.worktree_of(repo, br)
    if wt:
        was = laneslib.git(wt, "rev-parse", br).stdout.strip()
        r = laneslib.git(wt, "rebase", target, check=False)
        if r.returncode != 0:
            files = laneslib.conflicts(wt)
            if laneslib.git(wt, "rebase", "--abort",
                            check=False).returncode == 0:
                # `--abort` has already put the branch and its tree back at
                # `was`; this is the belt over those braces. `--keep`, not
                # `--hard`: `wt` can be a tree this process is not in, and
                # `--keep` refuses where `--hard` discards — the spelling
                # `collect.unland` uses, and one @resources/board/refuse.py
                # reads as discarding nothing.
                laneslib.git(wt, "reset", "--keep", was, check=False)
            raise laneslib.LaneError(
                f"conflict: {br} onto {target} — "
                + (", ".join(files) if files else "see git status"))
        ahead = laneslib.git(repo, "rev-list", "--count", f"{target}..{br}",
                             check=False).stdout.strip()
    r = laneslib.git(repo, "merge", "--ff-only", "--no-edit", br, check=False)
    if r.returncode != 0:
        raise laneslib.LaneError(
            f"{target} would not fast-forward to {br} in {repo} — "
            + ((r.stderr or r.stdout).strip().splitlines() or [""])[0])
    return br, target, int(ahead or 0)


def cmd_land(board, dry=False, as_json=False):
    try:
        br, target, n = land(board, dry=dry)
    except laneslib.LaneError as e:
        print(f"session land: {e}", file=sys.stderr)
        return 1
    ans = {"branch": br, "target": target, "commits": n, "dry": bool(dry)}
    if as_json:
        print(json.dumps(ans, indent=2))
    elif not n:
        print(f"{br} has nothing {target} has not got")
    elif dry:
        print(f"{n} commit(s) would land {br} on {target}")
    else:
        print(f"landed {n} commit(s) — {target} is {br}")
    return 0


def cmd_owns(board, path=None, as_json=False):
    """Does the running session own `path`? Exit 0 when it does, 1 when
    another session does or nobody does. The answer for a person or a
    script; @resources/board/refuse.py asks the same question of the ledger
    by hand and never calls this."""
    p = os.path.abspath(path or os.getcwd())
    rows = read_ledger(board)
    mine = session_pid()
    owner = None
    for r in rows:
        tree = os.path.abspath(r.get("worktree") or "")
        if tree and (p == tree or p.startswith(tree + os.sep)):
            owner = r
            break
    ans = {"path": p, "owner": owner.get("id") if owner else None,
           "session": sid(mine) if mine else None,
           "mine": bool(owner and owner.get("pid") == mine and mine is not None)}
    if as_json:
        print(json.dumps(ans, indent=2))
    elif ans["mine"]:
        print(f"{p} — held by this session ({ans['session']})")
    elif owner:
        print(f"{p} — held by {owner['id']}, not this session")
    else:
        print(f"{p} — no session on the ledger holds it")
    return 0 if ans["mine"] else 1


VERBS = ("take", "list", "reap", "land", "owns")


def cmd_session(argv):
    """take/list/reap/land/owns — one tree per session"""
    import transitions as translib
    verb = argv[0] if argv and argv[0] in VERBS else None
    rest = argv[1:] if verb else argv
    if verb is None:
        print("pearde session: takes " + ", ".join(VERBS), file=sys.stderr)
        return 2
    try:
        args = translib.Args(rest, FLAGS, "session " + verb)
    except translib.FlagRefused as e:
        print(f"pearde session {verb}: {e}", file=sys.stderr)
        return 2
    pos = list(args.pos)
    board_arg = args.opt.get("board")
    path = None
    if verb == "owns" and pos and not planlib.is_board_dir(os.path.abspath(pos[0])):
        path = pos.pop(0)
    board = planlib.find_board(board_arg or (pos[0] if pos else None))
    j = "json" in args.flags
    if verb == "take":
        return cmd_take(board, j)
    if verb == "list":
        return cmd_list(board, j)
    if verb == "reap":
        return cmd_reap(board, "apply" in args.flags, j)
    if verb == "land":
        return cmd_land(board, "dry" in args.flags, j)
    return cmd_owns(board, path, j)


cmd_session.flags = str(FLAGS)
COMMANDS = {"session": cmd_session}


if __name__ == "__main__":
    sys.exit(cmd_session(sys.argv[1:]))
