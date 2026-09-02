#!/usr/bin/env python3
"""Ask the three readers of `needs:` what each does with each shape.

`plan.resolve_needs`  — the edges the schedule is built from
`plan.dispatchable`   — the gate `scan`, `plan`'s ready band and `claim` share
`transitions.gate_unblock` — the edge back out of `blocked`

The contract holds when the qualified need `@other/thing`, whose board is not
in the scan, is ignored by all three, and the two unresolvable-local shapes
still hold.
"""
import io, os, shutil, subprocess, sys, tempfile, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
VS_HEAD = "--vs-head" in sys.argv
if VS_HEAD:
    sys.argv = [a for a in sys.argv if a != "--vs-head"]
# The tree under test — the lane while the build is uncommitted, the repo root
# once it lands. `PEARDE_TREE=<repo>` or argv[1] re-aims it; nothing else moves.
REPO = os.path.abspath(
    (sys.argv[1] if len(sys.argv) > 1 else None)
    or os.environ.get("PEARDE_TREE")
    or os.path.join(HERE, "..", "..", "..", ".."))


def head_tree():
    """A throwaway `resources/board/` holding the two readers as HEAD has them.

    A box that passes against the build proves nothing on its own; a box that
    fails against HEAD is a box that can fail. `--vs-head` runs the same table
    there and prints how many rows go red."""
    d = tempfile.mkdtemp(prefix="xboard-head-")
    # every top-level entry symlinked, `resources/` and `resources/board/`
    # rebuilt as real dirs so the two readers can be replaced without copying
    # the tree — the rest of the imports resolve as they do in the real repo
    for name in os.listdir(REPO):
        if name != "resources":
            os.symlink(os.path.join(REPO, name), os.path.join(d, name))
    os.makedirs(os.path.join(d, "resources", "board"))
    for name in os.listdir(os.path.join(REPO, "resources")):
        if name != "board":
            os.symlink(os.path.join(REPO, "resources", name),
                       os.path.join(d, "resources", name))
    src = os.path.join(REPO, "resources", "board")
    out = os.path.join(d, "resources", "board")
    for name in os.listdir(src):
        if name not in ("plan.py", "transitions.py", "__pycache__"):
            os.symlink(os.path.join(src, name), os.path.join(out, name))
    for f in ("plan.py", "transitions.py"):
        blob = subprocess.run(
            ["git", "-C", REPO, "show", f"HEAD:resources/board/{f}"],
            capture_output=True, text=True, check=True).stdout
        with open(os.path.join(out, f), "w") as fh:
            fh.write(blob)
    return d


if VS_HEAD:
    REPO = head_tree()
sys.path.insert(0, os.path.join(REPO, "resources", "board"))
sys.path.insert(0, HERE)

import plan as planlib          # noqa: E402
import transitions              # noqa: E402
from fixture import build, build_master   # noqa: E402


def gate_unblock_reason(board, prds, prd):
    try:
        transitions.gate_unblock(board, prds, prd)
    except transitions.Refused as e:
        return str(e)
    return None


def run(make=None):
    board = (make or build)()
    try:
        prds = planlib.scan(board)
        todo = {r: p for r, p in prds.items() if p["state"] == "open"}
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            try:
                edges = planlib.resolve_needs(prds, todo, True, board)
            except TypeError:
                # HEAD's signature — the board argument is part of the build
                edges = planlib.resolve_needs(prds, todo, True)
        rows = []
        for rel in sorted(todo):
            prd = prds[rel]
            rows.append((
                rel,
                "edge" if edges.get(rel) else "no edge",
                planlib.dispatchable(prd, prds, board) or "dispatchable",
                gate_unblock_reason(board, prds, prd) or "unblocks",
            ))
        return rows, err.getvalue(), prds
    finally:
        shutil.rmtree(os.path.dirname(board), ignore_errors=True)


MASTER_EXPECT = {
    # rel:            (resolve_needs,  dispatchable,   gate_unblock)
    "resolves":       ("edge", "needs:", "unblock: needs"),
    "membertypo":     ("no edge", "needs:", "unblock: needs"),
    "absent":         ("no edge", "dispatchable", "unblocks"),
    "ownname":        ("no edge", "needs:", "unblock: needs"),
    "@member/real":   ("no edge", "dispatchable", "unblocks"),
}

EXPECT = {
    # rel:        (resolve_needs,  dispatchable,       gate_unblock)
    "plain":      ("no edge", "dispatchable", "unblocks"),
    "crossboard": ("no edge", "dispatchable", "unblocks"),
    "typo":       ("no edge", "needs:", "unblock: needs"),
    "local":      ("edge", "needs:", "unblock: needs"),
}


def report(title, make, expect):
    rows, warnings, _ = run(make)
    print(f"── {title} " + "─" * (66 - len(title)))
    for line in warnings.strip().splitlines():
        print("  plan: " + line.split("plan: ", 1)[-1])
    print()
    print(f"{'prd':<16} {'resolve_needs':<14} {'dispatchable':<48} unblock")
    bad = []
    for rel, edge, disp, unb in rows:
        print(f"{rel:<16} {edge:<14} {disp[:46]:<48} {unb[:40]}")
        want = expect[rel]
        if edge != want[0] or not disp.startswith(want[1]) \
                or not unb.startswith(want[2]):
            bad.append(rel)
    print()
    return bad


def main():
    where = "HEAD" if VS_HEAD else REPO
    print(f"tree under test: {where}\n")
    bad = report("plain board", build, EXPECT)
    bad += report("master board, one member", build_master, MASTER_EXPECT)
    n = len(EXPECT) + len(MASTER_EXPECT)
    if VS_HEAD:
        print(f"verify --vs-head: {len(bad)} of {n} rows FAIL against HEAD "
              f"— {', '.join(bad) if bad else 'none, the boxes cannot fail'}")
        return 0 if bad else 1
    if bad:
        print(f"verify: {n - len(bad)}/{n} — off contract: {', '.join(bad)}")
        return 1
    print(f"verify: {n}/{n} — every needs shape lands where the contract says")
    return 0


if __name__ == "__main__":
    sys.exit(main())
