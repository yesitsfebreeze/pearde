#!/usr/bin/env python3
"""probe — what `pearde share` does and does not reach.

Run:  python3 probe_share.py
Makes its fixture worktree at run time under $TMPDIR, removes it after.
"""
import os, subprocess, sys, tempfile, shutil

REPO = "/Users/feb/dev/infra/pearde"
LANE = os.path.join(REPO, "pearde/.lanes/one-copy-per-machine-of-what-every-lane-regenerates")
sys.path.insert(0, os.path.join(LANE, "resources/board"))
import shared as sh  # noqa: E402


def q(*a, cwd=REPO):
    return subprocess.run(["git", "-C", cwd, *a], capture_output=True, text=True)


def probe_1_which_tree_is_checkout():
    """`share` run from a lane: what does it call `checkout`?

    `find_repo` answers the worktree the path is IN, and the board is a linked
    worktree of this same repo on its own branch — so it answers the board,
    and the board holds no `resources/board/` at all. That call is kept here
    because it is the defect: the two resolutions are printed side by side."""
    os.chdir(LANE)                      # what a worker's own call looks like
    board = sh.find_board_soft(None)
    repo = sh.find_repo(board)
    checkout = sh.find_checkout(board)
    ts = sh.trees(board, checkout)
    print(f"1  board                {board}")
    print(f"1  find_repo(board)     {repo}")
    print(f"1  find_checkout(board) {checkout}")
    print(f"1  trees()[0]           {ts[0]}")
    print(f"1  code checkout        {REPO}")
    print(f"1  VERDICT              "
          f"{'MISSES the checkout' if ts[0] != REPO else 'ok'}")
    print(f"1  checkout in trees(): {REPO in ts}")
    print(f"1  board in trees():    {board in ts}  (it offers nothing)")


def probe_2_status_hides_refusal(old_commit):
    """A tree whose .gitignore still has the trailing slash: apply refuses,
    status says nothing."""
    tmp = tempfile.mkdtemp(prefix="share-probe-")
    wt = os.path.join(tmp, "old")
    r = q("worktree", "add", "--detach", wt, old_commit)
    if r.returncode:
        print("2  SKIP", r.stderr.strip()); shutil.rmtree(tmp, True); return
    try:
        pat = [l for l in open(os.path.join(wt, ".gitignore"))
               if "node_modules" in l]
        print(f"2  fixture ignore  {[p.strip() for p in pat]}")
        rel = "resources/board/node_modules"
        print(f"2  state before    {sh.state(wt, rel)}")
        rows = sh.apply_tree(wt, name="fixture")
        for row in rows:
            if row["rel"] == rel:
                print(f"2  apply           {row['action']} — {row['note']}")
        print(f"2  state after     {sh.state(wt, rel)}")
        st = sh.state(wt, rel)
        print(f"2  status prints   {st!r}; summary buckets it under: "
              f"{'none — invisible' if st in ('store-only','absent') else st}")
    finally:
        q("worktree", "remove", "--force", wt)
        shutil.rmtree(tmp, ignore_errors=True)


def probe_3_unshared_bytes():
    """What is still duplicated per lane after share."""
    lanes = os.path.join(REPO, "pearde/.lanes")
    tot = {}
    for slug in sorted(os.listdir(lanes)):
        t = os.path.join(lanes, slug)
        if not os.path.isdir(t):
            continue
        for rel in ("pearde/graphify", "pearde/health", "pearde/wiki"):
            p = os.path.join(t, rel)
            if os.path.exists(p) and not os.path.islink(p):
                tot[rel] = tot.get(rel, 0) + sh.bytes_of(p)
    for rel, n in tot.items():
        print(f"3  {rel:<18} {sh.human(n)} across lanes, unshared")


if __name__ == "__main__":
    probe_1_which_tree_is_checkout()
    print()
    probe_2_status_hides_refusal(sys.argv[1] if len(sys.argv) > 1 else "8bbb4c1")
    print()
    probe_3_unshared_bytes()
