#!/usr/bin/env python3
"""What `foot_root` must answer for each layout, and what `collect` must do
with the answer.

Run: `python3 cases.py [<path to resources/board>]` — defaults to the lane's
board modules.  Prints one line per case, then `N pass / M fail`.
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixture  # noqa: E402


def default_board():
    """`<tree>/resources/board` for the tree under test — `PEARDE_ROOT` when
    the runner named one, else the repo above the board this probe sits in."""
    root = os.environ.get("PEARDE_ROOT")
    if not root:
        b = HERE
        while b != "/" and os.path.basename(b) not in (".pearde", "pearde"):
            b = os.path.dirname(b)
        root = os.path.dirname(b)
    return os.path.join(root, "resources", "board")


rows = []


def case(name, got, want):
    ok = got == want
    rows.append(ok)
    print(f"  {'pass' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"        want {want!r}")
        print(f"        got  {got!r}")
    return ok


def load(boarddir):
    sys.path.insert(0, boarddir)
    import plan as planlib
    import collect as collectlib
    return planlib, collectlib


def foot(collectlib, planlib, board, repo, p):
    """`foot_root` as `sort_paths` calls it, with the roots collect derives."""
    prd_dir = os.path.join(board, "prds", "finished")
    board_root = planlib.repo_root(prd_dir)
    try:
        return collectlib.foot_root(p, board, board_root, repo)
    except Exception as e:                              # noqa: BLE001
        return ("raised", f"{type(e).__name__}: {e}")


def run_sort(collectlib, planlib, board, rel="finished"):
    """`sort_paths` end to end — the call that refuses a footprint it cannot
    place.  Returns `("ok", {root: union})` or `("stop", message)`."""
    prds = planlib.scan(board)
    prd = prds.get(rel)
    if prd is None:
        return ("stop", f"no PRD at {rel} — scan saw {sorted(prds)}")
    board_root = planlib.repo_root(prd["dir"])
    repo = collectlib.repo_of(prd, board, board_root)
    _, feet = planlib.spec_data(prd)
    opts = {"also": [], "widen": [], "trust": True, "dry": True,
            "also_note": None}
    try:
        plan, _ = collectlib.sort_paths(board, rel, prd, prds, board_root,
                                        repo, feet, opts, None, landed=False)
    except Exception as e:                              # noqa: BLE001
        return ("stop", f"{type(e).__name__}: {e}")
    return ("ok", {r: sorted(v["union"]) for r, v in plan.items()})


def main(boarddir):
    planlib, collectlib = load(boarddir)
    print(f"board modules: {boarddir}\n")
    tmp = tempfile.mkdtemp(prefix="probe-collect-paths-")

    # ── L1 · plain board, nothing to reroute ─────────────────────────────
    f = fixture.l1_plain(os.path.join(tmp, "l1"))
    print("L1 plain board")
    case("footprint stays in the code repo",
         foot(collectlib, planlib, f["board"], f["repo"], "src/util.py"),
         (f["repo"], "src/util.py"))

    # ── L2 · board is its own repo ───────────────────────────────────────
    f = fixture.l2_own_repo(os.path.join(tmp, "l2"))
    b, r = f["board"], f["repo"]
    print("L2 board is its own git repo")
    case("a code path stays in the code repo",
         foot(collectlib, planlib, b, r, "src/util.py"), (r, "src/util.py"))
    case("a board path spelled from the CODE repo reroutes",
         foot(collectlib, planlib, b, r, "pearde/.gitignore"),
         (b, ".gitignore"))
    case("a board path spelled the BOARD's own way resolves",
         foot(collectlib, planlib, b, r, "prds/finished/probe/verify.sh"),
         (b, "prds/finished/probe/verify.sh"))
    case("sort_paths places every footprint",
         run_sort(collectlib, planlib, b),
         ("ok", {r: ["src/util.py"],
                 b: ["prds/finished", "prds/finished/probe/verify.sh"]}))

    # ── L3 · the code repo lives under the board ─────────────────────────
    f = fixture.l3_code_under_board(os.path.join(tmp, "l3"))
    b, r = f["board"], f["repo"]
    print("L3 the code repo is checked out under the board")
    case("a code path under the board stays in the CODE repo",
         foot(collectlib, planlib, b, r, "src/util.py"), (r, "src/util.py"))
    case("sort_paths groups it under the code repo",
         run_sort(collectlib, planlib, b),
         ("ok", {r: ["src/util.py"], b: ["prds/finished"]}))

    shutil.rmtree(tmp, ignore_errors=True)
    ok, n = sum(rows), len(rows)
    print(f"\nevery fixture was under {tmp}, removed on exit")
    print(f"{ok} pass / {n - ok} fail")
    return 0 if ok == n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default_board()))
