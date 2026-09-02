#!/usr/bin/env python3
"""Unit probe, pass two: `collect.owned_by` and `collect.guarded_run` where
the board is its OWN git repo, so `repo` and `board_root` are two different
roots — the shape this repo itself is in since the board moved to `pearde/`.

Pass one rebased the footprint against `board_root`. A footprint path is
spelled relative to `repo` (`sort_paths` resolves every one as
`os.path.join(repo, p)`), so that rebase named a path in neither root: the
file under test read as foreign, was parked, and the verify block measured
a clean HEAD. This probe holds the corrected grouping to `sort_paths`'s.

Run from anywhere:
    python3 .pearde/prds/a-verify-block-.../probe/probe_roots.py
"""
import os
import subprocess
import sys
import tempfile
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LANE = os.path.join(REPO, ".pearde", ".lanes",
                    "the-verify-guard-parses-git-s-own-output-before-it-trusts-it")
SRC = os.environ.get("PEARDE_ROOT") or (LANE if os.path.isdir(LANE) else REPO)
sys.path.insert(0, os.path.join(SRC, "resources"))
sys.path.insert(0, os.path.join(SRC, "resources", "board"))
import collect  # noqa: E402
assert hasattr(collect, "owned_by"), (
    f"collect.py at {SRC} has no owned_by — probing the wrong tree")

QUIET = (lambda s: None)
# `rm -rf .` is a no-op on darwin: `rm` refuses "." and exits 1 having
# deleted nothing. This empties the working tree for real, and leaves
# `.git` — a block that deletes that is past anything git can put back.
DESTROY = "find . -mindepth 1 -not -path './.git*' -delete"


def git(repo, *args):
    r = subprocess.run(("git", "-C", repo) + args, capture_output=True,
                       text=True)
    assert r.returncode == 0, f"{args}: {r.stderr}"
    return r.stdout


def init(d):
    git(d, "init", "-q")
    git(d, "config", "user.email", "t@t")
    git(d, "config", "user.name", "t")


def build(d):
    """A code repo with a board that is its own repo inside it — `repo_of`'s
    `board_root == board` branch, the layout this repo is in."""
    for p in ("resources/board/collect.py", "resources/board/other.py",
              "other/neighbour.txt"):
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(f"# {p} v1\n")
    init(d)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "code base")

    board = os.path.join(d, ".pearde")
    for p in ("prds/mine/prd.md", "prds/mine/specs/spec01.md",
              "prds/theirs/prd.md"):
        full = os.path.join(board, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(f"# {p}\n")
    init(board)
    git(board, "add", "-A")
    git(board, "commit", "-q", "-m", "board base")
    return board


def prd_at(board, name="mine", member=None):
    p = {"dir": os.path.join(board, "prds", name), "rel": name}
    if member:
        p["board"] = member
    return p


def case(name, fn):
    d = tempfile.mkdtemp()
    try:
        board = build(d)
        fn(d, board)
        print(f"PASS: {name}")
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ── R1 the grouping itself ───────────────────────────────────────────────────
def grouping_matches_sort_paths(d, board):
    owned = collect.owned_by(prd_at(board), board, d,
                             ["resources/board/collect.py"])
    assert owned[os.path.abspath(d)] == ["resources/board/collect.py"], owned
    assert owned[os.path.abspath(board)] == ["prds/mine"], owned
    # and where the two roots ARE one, the row holds both
    one = collect.owned_by(prd_at(board), board, board,
                           ["resources/board/collect.py"])
    assert one[os.path.abspath(board)] == \
        ["prds/mine", "resources/board/collect.py"], one


def member_sigil_comes_off_its_own_board(d, board):
    feet = ["@mine/src/lib.rs", "@other/src/lib.rs"]
    owned = collect.owned_by(prd_at(board, member="mine"), board, d, feet)
    assert owned[os.path.abspath(d)] == ["src/lib.rs"], owned


# ── R2 a spec's block, cwd = repo ────────────────────────────────────────────
def footprint_is_visible_to_the_block_it_is_under_test_for(d, board):
    """The pass-one bug, held down: the footprint file is dirty and the block
    must SEE the dirty text, not a parked clean HEAD."""
    foot = os.path.join(d, "resources/board/collect.py")
    open(foot, "w").write("# the change under test\n")
    open(os.path.join(d, "other/neighbour.txt"), "w").write("# foreign WIP\n")
    owned = collect.owned_by(prd_at(board), board, d,
                             ["resources/board/collect.py"])
    seen = {}

    def script(cmd, cwd, s=None):
        seen["text"] = open(os.path.join(cwd,
                            "resources/board/collect.py")).read()
        subprocess.run(["bash", "-c", DESTROY], cwd=cwd,
                       capture_output=True)
        return 0, ""
    real, collect.run = collect.run, script
    try:
        collect.guarded_run(["noop"], d, owned, out=QUIET)
    finally:
        collect.run = real
    assert seen["text"] == "# the change under test\n", seen
    assert open(os.path.join(d, "other/neighbour.txt")).read() == \
        "# foreign WIP\n"
    # the footprint IS reachable — it is what the block is measuring — so
    # the block emptying the tree takes it, and spec02's snapshot puts it
    # back with the dirty text it had, not with HEAD's
    assert open(foot).read() == "# the change under test\n", open(foot).read()


# ── R3 the gate, cwd = board_root ────────────────────────────────────────────
def the_gate_keeps_its_own_prd_and_parks_the_neighbour(d, board):
    open(os.path.join(board, "prds/mine/prd.md"), "w").write("# mine, edited\n")
    open(os.path.join(board, "prds/theirs/prd.md"), "w").write("# theirs WIP\n")
    owned = collect.owned_by(prd_at(board), board, d,
                             ["resources/board/collect.py"])
    seen = {}

    def script(cmd, cwd, s=None):
        seen["mine"] = open(os.path.join(cwd, "prds/mine/prd.md")).read()
        seen["theirs"] = open(os.path.join(cwd, "prds/theirs/prd.md")).read()
        subprocess.run(["bash", "-c", DESTROY], cwd=cwd,
                       capture_output=True)
        return 0, ""
    real, collect.run = collect.run, script
    try:
        collect.guarded_run(["noop"], board, owned, out=QUIET)
    finally:
        collect.run = real
    assert seen["mine"] == "# mine, edited\n", seen
    # the neighbour's edit is not in the tree for the run — parked, so the
    # block reads HEAD's text and the edit is not there to be destroyed
    assert seen["theirs"] == "# prds/theirs/prd.md\n", seen
    assert open(os.path.join(board, "prds/theirs/prd.md")).read() == \
        "# theirs WIP\n"
    # this PRD's own directory is owned, so the block could reach it — and
    # spec02's snapshot puts back what it deleted, with the edited text
    assert open(os.path.join(board, "prds/mine/prd.md")).read() == \
        "# mine, edited\n"
    assert git(board, "stash", "list").strip() == ""


def a_cwd_that_is_neither_root_owns_nothing(d, board):
    open(os.path.join(d, "other/neighbour.txt"), "w").write("# foreign WIP\n")
    owned = collect.owned_by(prd_at(board), board, "/nowhere",
                             ["resources/board/collect.py"])
    collect.guarded_run(["bash", "-e", "-c", DESTROY], d, owned, out=QUIET)
    assert open(os.path.join(d, "other/neighbour.txt")).read() == \
        "# foreign WIP\n"


def pass_ones_grouping_parked_the_file_under_test(d, board):
    """The defect this pass closed, as a check that fails if it comes back:
    pass one rebased the footprint against `board_root`, so with the board
    its own repo the spec's block saw `.pearde/resources/board/collect.py`
    — a path in neither root — and the file under test was parked."""
    foot = os.path.join(d, "resources/board/collect.py")
    open(foot, "w").write("# the change under test\n")
    pass_one = {os.path.abspath(d): [os.path.relpath(
        os.path.join(board, "resources/board/collect.py"), d)]}
    seen = {}

    def script(cmd, cwd, s=None):
        seen["text"] = open(os.path.join(cwd,
                            "resources/board/collect.py")).read()
        return 0, ""
    real, collect.run = collect.run, script
    try:
        collect.guarded_run(["noop"], d, pass_one, out=QUIET)
    finally:
        collect.run = real
    assert seen["text"] == "# resources/board/collect.py v1\n", (
        "pass one's grouping no longer parks the file under test — this "
        "witness has stopped witnessing anything")


if __name__ == "__main__":
    case("the grouping is `sort_paths`'s: footprint under repo, PRD dir "
         "under the board", grouping_matches_sort_paths)
    case("a member PRD's own sigil comes off, another member's stays out",
         member_sigil_comes_off_its_own_board)
    case("repo != board_root: the footprint is visible to the block, the "
         "neighbour is parked", footprint_is_visible_to_the_block_it_is_under_test_for)
    case("the gate in the board's own repo keeps this PRD's dir and parks "
         "the next PRD's", the_gate_keeps_its_own_prd_and_parks_the_neighbour)
    case("a cwd that is neither root owns nothing there",
         a_cwd_that_is_neither_root_owns_nothing)
    case("witness: pass one's grouping parked the file under test",
         pass_ones_grouping_parked_the_file_under_test)
    print("ALL PASS")
