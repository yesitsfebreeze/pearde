#!/usr/bin/env python3
"""Unit probe, pass one: `collect.guarded_run` (added to
`resources/board/collect.py`) against the exact incident shape —
destructive shell run where the verify/gate blocks already run, in a
checkout other work is sitting dirty in.

Run from the repo root:
    python3 .pearde/prds/a-verify-block-must-not-destroy-the-checkout-it-runs-in/probe/probe_unit.py
"""
import os
import subprocess
import sys
import tempfile
import shutil

QUIET = (lambda s: None)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
# pass one's build lives in this PRD's own lane, not the shared checkout —
# `pearde brief`'s worktree, per @references/parts/board.md's lanes.
LANE = os.path.join(REPO, ".pearde", ".lanes",
                    "a-verify-block-must-not-destroy-the-checkout-it-runs-in")
BOARD_SRC = os.path.join(LANE, "resources", "board") \
    if os.path.isdir(LANE) else os.path.join(REPO, "resources", "board")
sys.path.insert(0, BOARD_SRC)
import collect  # noqa: E402
assert hasattr(collect, "guarded_run"), (
    f"collect.py at {BOARD_SRC} has no guarded_run — probing the wrong tree")
assert hasattr(collect, "owned_by"), (
    f"collect.py at {BOARD_SRC} has no owned_by — probing the wrong tree")


# `rm -rf .` is a NO-OP on darwin — `rm` refuses "." and ".." and exits 1
# without deleting anything, so a case built on it exercises no guard at all
# and cannot fail on this platform. This is the destructive block: it empties
# the working tree for real and leaves `.git` alone, because a block that
# deletes `.git` is past anything git can put back.
DESTROY = "find . -mindepth 1 -not -path './.git*' -delete"


def owned(root, feet):
    """`owned_by`'s dict for a fixture whose repo and board root are one."""
    return {os.path.abspath(root): sorted(feet)}


def git(repo, *args):
    r = subprocess.run(("git", "-C", repo) + args, capture_output=True, text=True)
    assert r.returncode == 0, f"{args}: {r.stderr}"
    return r.stdout


def build_repo(d):
    os.makedirs(d, exist_ok=True)
    git(d, "init", "-q")
    git(d, "config", "user.email", "t@t")
    git(d, "config", "user.name", "t")
    for p in ("resources/board/plan.py", "resources/board/other.py", "README.md"):
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(f"# {p} v1\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "base")


def case(name, fn):
    d = tempfile.mkdtemp()
    try:
        build_repo(d)
        fn(d)
        print(f"PASS: {name}")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _dirty_up(d):
    open(os.path.join(d, "resources/board/other.py"), "w").write("# WIP rewrite\n")
    open(os.path.join(d, "resources/board/new_untracked.py"), "w").write("# new\n")


def foreign_dirt_survives_a_wipe(d):
    _dirty_up(d)
    feet = ["resources/board/plan.py"]
    collect.guarded_run(["bash", "-e", "-c", DESTROY], d,
                        owned(d, feet), out=lambda s: None)
    assert open(os.path.join(d, "resources/board/other.py")).read() == "# WIP rewrite\n"
    assert os.path.exists(os.path.join(d, "resources/board/new_untracked.py"))
    assert os.path.exists(os.path.join(d, "README.md"))
    # and the footprint is still NOT fenced — it stayed in the tree for the
    # block to reach, which is the whole point of leaving it outside the
    # park. What spec02 adds is that a block cannot leave it DELETED: the
    # block emptied the tree, and the snapshot put this PRD's own work back.
    assert os.path.exists(os.path.join(d, "resources/board/plan.py"))


def the_wipe_really_wipes_when_it_is_not_guarded(d):
    """The witness that makes the case above able to fail: the same block,
    through the `run` the call site used before the guard."""
    _dirty_up(d)
    collect.run(["bash", "-e", "-c", DESTROY], d)
    assert not os.path.exists(os.path.join(d, "resources/board/other.py"))
    assert not os.path.exists(os.path.join(d, "README.md"))


def own_footprint_left_alone(d):
    open(os.path.join(d, "resources/board/plan.py"), "w").write("# WIP by this PRD\n")
    feet = ["resources/board/plan.py"]

    def script_appends(cmd, cwd, s=None):
        with open(os.path.join(cwd, "resources/board/plan.py"), "a") as f:
            f.write("# verify touched it\n")
        return 0, ""
    real_run = collect.run
    collect.run = script_appends
    try:
        collect.guarded_run(["noop"], d, owned(d, feet), out=lambda s: None)
    finally:
        collect.run = real_run
    content = open(os.path.join(d, "resources/board/plan.py")).read()
    assert "WIP by this PRD" in content and "verify touched it" in content, content


def reset_hard_and_clean_undone(d):
    old = git(d, "rev-parse", "HEAD").strip()
    open(os.path.join(d, "resources/board/plan.py"), "w").write("# v2\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "v2")
    open(os.path.join(d, "resources/board/other.py"), "w").write("# foreign WIP\n")
    open(os.path.join(d, "junk.txt"), "w").write("scratch\n")
    feet = ["resources/board/plan.py"]
    script = f"git reset --hard {old}; git clean -fdx"
    collect.guarded_run(["bash", "-c", script], d, owned(d, feet),
                        out=lambda s: None)
    assert open(os.path.join(d, "resources/board/other.py")).read() == "# foreign WIP\n"
    now = git(d, "rev-parse", "HEAD").strip()
    assert now != old, "HEAD was not restored to the post-verify commit"


def nothing_dirty_no_stash_left(d):
    feet = ["resources/board/plan.py"]
    collect.guarded_run(["bash", "-c", "rm README.md"], d, owned(d, feet),
                        out=lambda s: None)
    assert os.path.exists(os.path.join(d, "README.md"))
    assert git(d, "stash", "list").strip() == ""


def git_reads_see_a_correct_tree(d):
    open(os.path.join(d, "resources/board/other.py"), "w").write("# foreign WIP\n")
    feet = ["resources/board/plan.py"]

    def script(cmd, cwd, s=None):
        r = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=cwd,
                           capture_output=True, text=True)
        return (0 if r.stdout.strip() == "base" else 1), r.stdout
    real_run = collect.run
    collect.run = script
    try:
        code, output = collect.guarded_run(["noop"], d, owned(d, feet),
                                           out=lambda s: None)
    finally:
        collect.run = real_run
    assert code == 0, output
    assert open(os.path.join(d, "resources/board/other.py")).read() == "# foreign WIP\n"


# ── spec02: a block cannot delete the work it was written to measure ────────


def spec01_guard(d, scoped):
    """spec01's `guarded_run` exactly — park, run, restore head, heal, pop —
    with no snapshot. The witness the snapshot cases are measured against;
    if it ever stops losing the file, they have stopped witnessing."""
    parked = collect._park(d, scoped, QUIET)
    ref, sha = collect._head_of(d)
    try:
        collect.run(["bash", "-e", "-c", DESTROY], d)
    finally:
        collect._restore_head(d, ref, sha, QUIET)
        collect._heal(d, scoped, QUIET)
        if parked:
            subprocess.run(["git", "-C", d, "stash", "pop"],
                           capture_output=True)


def a_deleted_owned_file_comes_back(d):
    """Both snapshot branches at once: a tracked, clean path, whose bytes
    git already holds, and an untracked one, whose bytes nothing else does.
    Mode as well as content — the pre-block mode, not git's exec bit."""
    tracked = os.path.join(d, "resources/board/plan.py")
    os.chmod(tracked, 0o755)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "exec bit")
    fresh = os.path.join(d, "resources/board/fresh.py")
    open(fresh, "w").write("# untracked, and this PRD's own\n")
    os.chmod(fresh, 0o600)
    before = {p: (open(p).read(), os.stat(p).st_mode & 0o7777)
              for p in (tracked, fresh)}
    feet = ["resources/board/plan.py", "resources/board/fresh.py"]
    collect.guarded_run(["bash", "-e", "-c", DESTROY], d, owned(d, feet),
                        out=QUIET)
    for p, (text, mode) in before.items():
        assert os.path.exists(p), f"{p} was not put back"
        assert open(p).read() == text, p
        got = os.stat(p).st_mode & 0o7777
        assert got == mode, f"{p}: mode {oct(got)}, want {oct(mode)}"


def without_the_snapshot_the_same_block_loses_it(d):
    """The witness that makes the case above able to fail."""
    spec01_guard(d, ["resources/board/plan.py"])
    assert not os.path.exists(os.path.join(d, "resources/board/plan.py"))


def a_modified_owned_file_stays_modified(d):
    """A formatter or a build step editing the file under test is legitimate
    and indistinguishable from the change itself — left byte for byte."""
    p = os.path.join(d, "resources/board/plan.py")
    after = "# the formatter rewrote it\n"

    def script(cmd, cwd, s=None):
        open(p, "w").write(after)
        return 0, ""
    real, collect.run = collect.run, script
    try:
        collect.guarded_run(["noop"], d, owned(d, ["resources/board/plan.py"]),
                            out=QUIET)
    finally:
        collect.run = real
    assert open(p).read() == after, open(p).read()


def a_created_owned_file_stays_created(d):
    p = os.path.join(d, "resources/board/built.py")

    def script(cmd, cwd, s=None):
        open(p, "w").write("# the build step made it\n")
        return 0, ""
    real, collect.run = collect.run, script
    try:
        collect.guarded_run(["noop"], d, owned(d, ["resources/board/plan.py",
                                                   "resources/board/built.py"]),
                            out=QUIET)
    finally:
        collect.run = real
    assert os.path.exists(p) and "build step" in open(p).read()


def a_deletion_the_worker_made_is_not_resurrected(d):
    """A spec whose finish IS a deletion — `sort_paths` supports it. The path
    was not on disk before the block, so it was never snapshotted."""
    p = os.path.join(d, "resources/board/plan.py")
    os.remove(p)
    collect.guarded_run(["bash", "-e", "-c", "true"], d,
                        owned(d, ["resources/board/plan.py"]), out=QUIET)
    assert not os.path.exists(p), "the guard resurrected the spec's own finish"


def a_directory_footprint_is_snapshotted_by_its_files(d):
    """A footprint entry may name a directory. Both branches again: two
    tracked, clean files inside it and one untracked."""
    scratch = os.path.join(d, "resources/board/scratch.py")
    open(scratch, "w").write("# untracked, inside the owned directory\n")
    block = ("rm -f resources/board/other.py resources/board/scratch.py "
             "resources/board/plan.py")
    collect.guarded_run(["bash", "-e", "-c", block], d,
                        owned(d, ["resources/board"]), out=QUIET)
    for rel, want in (("resources/board/other.py",
                       "# resources/board/other.py v1\n"),
                      ("resources/board/plan.py",
                       "# resources/board/plan.py v1\n"),
                      ("resources/board/scratch.py",
                       "# untracked, inside the owned directory\n")):
        full = os.path.join(d, rel)
        assert os.path.exists(full), f"{rel} was not put back"
        assert open(full).read() == want, rel


def every_restored_path_is_named_on_its_own_line(d):
    said = []
    open(os.path.join(d, "resources/board/fresh.py"), "w").write("# own\n")
    feet = ["resources/board/plan.py", "resources/board/fresh.py"]
    collect.guarded_run(["bash", "-e", "-c", DESTROY], d, owned(d, feet),
                        out=said.append)
    lines = [s for s in said if "put back" in s and "own work" in s]
    assert len(lines) == 1, said
    for rel in feet:
        assert rel in lines[0], (rel, lines[0])


if __name__ == "__main__":
    case("unguarded, the block really does empty the checkout",
         the_wipe_really_wipes_when_it_is_not_guarded)
    case("foreign dirt survives a block that empties the checkout",
         foreign_dirt_survives_a_wipe)
    case("own footprint left exactly as the block leaves it", own_footprint_left_alone)
    case("`git reset --hard` + `git clean -fdx` undone, foreign dirt intact",
        reset_hard_and_clean_undone)
    case("nothing foreign — no stash left behind", nothing_dirty_no_stash_left)
    case("git reads inside the block see the real tree", git_reads_see_a_correct_tree)
    case("without the snapshot the block loses the work under test",
         without_the_snapshot_the_same_block_loses_it)
    case("a deleted owned file comes back, bytes and mode, both branches",
         a_deleted_owned_file_comes_back)
    case("an owned file the block MODIFIES stays modified",
         a_modified_owned_file_stays_modified)
    case("an owned file the block CREATES stays created",
         a_created_owned_file_stays_created)
    case("a deletion the worker made before the block stays deleted",
         a_deletion_the_worker_made_is_not_resurrected)
    case("a directory footprint: a file deleted from inside comes back",
         a_directory_footprint_is_snapshotted_by_its_files)
    case("every restored path is named on collect's own output line",
         every_restored_path_is_named_on_its_own_line)
    print("ALL PASS")
