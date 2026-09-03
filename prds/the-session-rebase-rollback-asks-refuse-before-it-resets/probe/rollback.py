#!/usr/bin/env python3
"""probe — the rollback arm of `session.land` on a conflicting rebase.

Builds a real repo with a board, takes a session worktree, makes a conflict
that `rebase` cannot resolve, and calls `land`. Three things are measured:

  mine    — this session holds the tree: the gate lets the reset through,
            the branch is back at the pre-rebase SHA and the error names the
            conflicting file (the contract's second acceptance box).
  theirs  — a LIVE PEER holds it on the ledger: the gate refuses the reset
            and the rollback is unharmed, because `rebase --abort` had
            already put the branch back. This is the whole point of the gate.
  symlink — the same fixture built under an UNRESOLVED path (macOS `/var` ->
            `/private/var`). `land` hands the gate the path `git worktree
            list` prints, which git has resolved, while the ledger holds the
            path `session take` wrote, which is not: the two strings differ
            and the owning session reads as a stranger. Fail-closed, so
            nothing is lost — but the gate is answering the wrong question.

Run:  python3 rollback.py                    # all three
      python3 rollback.py mine theirs        # pick cases

The tree under test is the lane checkout this probe sits beside; override
with PEARDE_TREE.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

TREE = os.environ.get(
    "PEARDE_TREE",
    "/Users/feb/dev/infra/pearde/.pearde/.lanes/"
    "the-session-rebase-rollback-asks-refuse-before-it-resets")
sys.path.insert(0, os.path.join(TREE, "resources", "board"))


def git(root, *args, check=True):
    r = subprocess.run(("git", "-C", root) + args,
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit("git %s in %s: %s" % (" ".join(args), root,
                                               r.stderr or r.stdout))
    return r


def build(tmp):
    """A repo with a board in it, one commit, on branch `main`."""
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "probe@example.com")
    git(repo, "config", "user.name", "probe")
    board = os.path.join(repo, ".pearde")
    os.makedirs(os.path.join(board, ".state"))
    open(os.path.join(board, "settings.md"), "w").write("# settings\n")
    open(os.path.join(repo, ".gitignore"), "w").write(".pearde/\n")
    open(os.path.join(repo, "shared.txt"), "w").write("base\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "base")
    return repo, board


def run(case):
    tmp = tempfile.mkdtemp(prefix="pearde-probe-")
    # every case but `symlink` resolves the root first: on macOS the temp dir
    # is reached through /var -> /private/var, and an unresolved root is the
    # `symlink` case's whole subject rather than a background condition.
    if case != "symlink":
        tmp = os.path.realpath(tmp)
    try:
        return _run(case, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _run(case, tmp):
    repo, board = build(tmp)
    os.environ["PEARDE_SESSION_PID"] = str(os.getpid())
    import session as s          # imported AFTER the env is set
    import lanes as laneslib

    rc = s.cmd_take(board)
    assert rc == 0, "session take failed"
    ident = s.my_id()
    wt = s.tree_of(board, ident)
    br = s.branch_of(ident)

    # the session's own commit, on the file the checkout is about to move
    open(os.path.join(wt, "shared.txt"), "w").write("session\n")
    git(wt, "add", "-A")
    git(wt, "commit", "-qm", "session edit")
    was = git(wt, "rev-parse", br).stdout.strip()

    # and a conflicting commit on the branch a person reads
    open(os.path.join(repo, "shared.txt"), "w").write("person\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "person edit")

    # dirt the rollback must not eat
    open(os.path.join(wt, "dirt.txt"), "w").write("uncommitted\n")

    if case == "theirs":
        # a live peer (this probe's parent) is written into the ledger AHEAD
        # of our own row, holding the same tree: `refuse.holder` reads the
        # first row that covers the path, so the tree stops being ours.
        rows = s.read_ledger(board)
        peer = dict(rows[0])
        peer.update({"id": "s-peer", "pid": os.getppid(),
                     "started": s.started(os.getppid()) or ""})
        s.write_ledger(board, [peer] + rows)

    # every git the rollback runs, recorded: whether the `reset --hard` RAN
    # is the only difference the two cases can show. `rebase --abort` has
    # already put the branch back by then, so the SHA is the same either way
    # and the SHA alone cannot tell a gated run from an ungated one.
    calls = []
    real = laneslib.git
    gate = {}

    def spy(root, *args, **kw):
        calls.append(list(args))
        return real(root, *args, **kw)

    real_gate = laneslib._may_discard

    def gatespy(tree):
        ans = real_gate(tree)
        gate.update({"tree": tree, "answer": ans})
        return ans

    laneslib.git = spy
    laneslib._may_discard = gatespy
    err = None
    try:
        s.land(board)
    except laneslib.LaneError as e:
        err = str(e)
    finally:
        laneslib.git = real
        laneslib._may_discard = real_gate

    after = git(wt, "rev-parse", br).stdout.strip()
    status = git(wt, "status", "--porcelain", check=False).stdout.strip()
    reset_ran = any(a[:2] == ["reset", "--hard"] for a in calls)
    return {"case": case, "error": err, "was": was, "after": after,
            "restored": was == after,
            "names_the_file": bool(err and "shared.txt" in err),
            "reset_hard_ran": reset_ran,
            "dirt_kept": "dirt.txt" in status,
            "status": status.splitlines(),
            "gate_asked": bool(gate),
            "gate_answer": gate.get("answer"),
            "gate_tree_is_the_ledger_s": gate.get("tree") == wt,
            "git": [" ".join(a[:3]) for a in calls]}


if __name__ == "__main__":
    # each case gets a process of its own: `session` caches nothing, but the
    # ledger, the env pid and the module's board are per-run state, and one
    # process per case keeps the two runs from reading each other's.
    if sys.argv[1:2] == ["--one"]:
        print(json.dumps(run(sys.argv[2]), indent=2))
        sys.exit(0)
    bad = 0
    for c in (sys.argv[1:] or ["mine", "theirs", "symlink"]):
        r = subprocess.run([sys.executable, os.path.abspath(__file__),
                            "--one", c], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        bad |= r.returncode
    sys.exit(1 if bad else 0)
