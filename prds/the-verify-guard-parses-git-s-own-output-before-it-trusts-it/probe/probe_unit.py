#!/usr/bin/env python3
"""Unit probe, pass one: `collect.guarded_run` (added to
`resources/board/collect.py`) against the exact incident shape —
destructive shell run where the verify/gate blocks already run, in a
checkout other work is sitting dirty in.

Run from the repo root:
    python3 .pearde/prds/the-verify-guard-parses-git-s-own-output-before-it-trusts-it/probe/probe_unit.py
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
                    "the-verify-guard-parses-git-s-own-output-before-it-trusts-it")
# PEARDE_ROOT wins: the run that counts is against the MERGED tree, and the
# lane is only the fallback for a probe run by hand mid-build.
_ROOT = os.environ.get("PEARDE_ROOT") or (LANE if os.path.isdir(LANE) else REPO)
BOARD_SRC = os.path.join(_ROOT, "resources", "board")
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


# ── pass two: the parsing, and what the healing must not destroy ────────────


def a_spaced_path_is_classified_parked_healed_and_unerased(d):
    """The blocking defect pass one landed. `git status --porcelain` quotes
    `src/a b.py`, and `line[3:]` handed every consumer `"src/a b.py"` — quotes
    and all. Owned, the file read as foreign and the block measured a clean
    HEAD; foreign, `_park`'s pathspec was refused and the WHOLE block ran
    unguarded; and `_snapshot` called it clean, so `_unerase` wrote HEAD's
    bytes over the uncommitted work while printing `put back:`.

    Two spaced paths here — one owned, one foreign — and both must come
    through exactly as their unspaced twins do."""
    own, foreign = "src/a b.py", "other/a peer file.py"
    for rel in (own, foreign, "src/plain.py", "other/plain.py"):
        full = os.path.join(d, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(f"# {rel} v1\n")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "spaced")

    rows = dict((p, c) for c, p in collect._dirty(d))
    assert rows == {}, f"a clean tree read dirty: {rows}"
    for rel in (own, foreign, "src/plain.py", "other/plain.py"):
        open(os.path.join(d, rel), "w").write(f"# {rel} UNCOMMITTED\n")
    rows = dict((p, c) for c, p in collect._dirty(d))
    assert own in rows and foreign in rows, (
        f"a path with a space never reached _dirty unquoted: {sorted(rows)}")
    assert not any(p.startswith('"') for p in rows), rows

    feet = [own, "src/plain.py"]
    assert collect.inside(own, feet), "the owned spaced path read as foreign"
    said = []
    collect.guarded_run(["bash", "-e", "-c", DESTROY], d, owned(d, feet),
                        out=said.append)
    # owned, spaced: still there, still the worker's uncommitted bytes
    for rel in feet:
        full = os.path.join(d, rel)
        assert os.path.exists(full), f"{rel} was not put back\n" + "\n".join(said)
        assert open(full).read() == f"# {rel} UNCOMMITTED\n", (
            f"{rel} was overwritten with HEAD's bytes\n" + "\n".join(said))
    # foreign, spaced: parked, so the block never reached it, and back after
    for rel in (foreign, "other/plain.py"):
        full = os.path.join(d, rel)
        assert os.path.exists(full), f"{rel} was destroyed\n" + "\n".join(said)
        assert open(full).read() == f"# {rel} UNCOMMITTED\n", rel


def a_rename_is_one_row_naming_its_destination(d):
    """`-z` spends a second record on a rename's source, and the ` -> ` the
    human form uses is not in it. A parser that misses that reads the source
    path as a status code and shifts every row after it."""
    git(d, "mv", "README.md", "READ ME.md")
    rows = collect._dirty(d)
    assert rows == [("R ", "READ ME.md")], rows


def a_peers_new_file_is_not_destroyed(d):
    """The live defect: `_heal`'s `git clean -f -d` deleted a foreign
    UNTRACKED file created inside the verify window, the stash pop never held
    it, and the output line said `put back` anyway. Nothing is deleted now —
    the bytes leave the checkout for a named place inside the git dir, and
    `collect` prints where."""
    block = ("printf 'PEER WROTE THIS\\n' > other/peer-new.txt; "
             "printf 'peer edit\\n' > README.md")
    os.makedirs(os.path.join(d, "other"), exist_ok=True)
    said = []
    collect.guarded_run(["bash", "-e", "-c", block], d,
                        owned(d, ["resources/board/plan.py"]),
                        out=said.append)
    line = [s for s in said if "moved aside" in s]
    assert len(line) == 1, said
    assert "other/peer-new.txt" in line[0], line
    aside = line[0].split("moved aside to ", 1)[1].split(":", 1)[0].strip()
    kept = os.path.join(aside, "other/peer-new.txt")
    assert os.path.exists(kept), f"the peer's file is gone: {aside}\n{said}"
    assert open(kept).read() == "PEER WROTE THIS\n", open(kept).read()
    # and a tracked foreign path IS put back to HEAD, its bytes kept too
    assert open(os.path.join(d, "README.md")).read() == "# README.md v1\n"
    assert open(os.path.join(aside, "README.md")).read() == "peer edit\n"


def heal_names_only_what_it_put_back(d):
    """Pass one printed `put back:` over every foreign row whatever the git
    calls returned, and checked none of their returncodes. The line now names
    the paths actually restored, and an untracked path — which HEAD cannot put
    back — is on the moved-aside line instead."""
    block = "printf 'litter\\n' > other/litter.txt; printf 'x\\n' > README.md"
    os.makedirs(os.path.join(d, "other"), exist_ok=True)
    said = []
    collect.guarded_run(["bash", "-e", "-c", block], d,
                        owned(d, ["resources/board/plan.py"]), out=said.append)
    back = [s for s in said if "put back:" in s and "outside its footprint" in s]
    assert len(back) == 1, said
    assert "README.md" in back[0], back
    assert "other/litter.txt" not in back[0], (
        "a path HEAD never held was named as put back: " + back[0])


def a_failed_restore_says_so(d):
    """A restore that cannot happen is reported, not silently counted."""
    said = []
    real = collect._head_blob
    collect._head_blob = lambda cwd, rel: (b"x", 0o644)
    real_open = collect.open if hasattr(collect, "open") else open

    def boom(path, *a, **k):
        if path.endswith("README.md") and "b" in (a[0] if a else k.get("mode", "")):
            raise OSError("no")
        return real_open(path, *a, **k)
    collect.open = boom
    try:
        open(os.path.join(d, "README.md"), "w").write("peer edit\n")
        collect._heal(d, ["resources/board/plan.py"], out=said.append)
    finally:
        collect._head_blob = real
        del collect.open
    assert any("NOT put back" in s and "README.md" in s for s in said), said


def a_peers_staged_entry_is_not_wiped(d):
    """`git reset -q HEAD -- <paths>` unstaged everything foreign, so a peer
    who ran `git add` inside the verify window lost their staging. A staged
    foreign path is left exactly as it is now, worktree and index, and named
    — `collect` commits through a private index, so nothing of it leaks into
    the landing."""
    def stage_as_a_peer(cmd, cwd, s=None):
        open(os.path.join(cwd, "README.md"), "w").write("peer staged\n")
        git(cwd, "add", "README.md")
        return 0, ""
    said = []
    real_run = collect.run
    collect.run = stage_as_a_peer
    try:
        collect.guarded_run(["noop"], d, owned(d, ["resources/board/plan.py"]),
                            out=said.append)
    finally:
        collect.run = real_run
    staged = git(d, "show", ":README.md")
    assert staged == "peer staged\n", f"the peer's staging was wiped: {staged!r}"
    assert open(os.path.join(d, "README.md")).read() == "peer staged\n"
    assert any("left staged" in s and "README.md" in s for s in said), said


def a_revert_to_head_is_undone(d):
    """The incident in the title, and the shape `spec02`'s box overclaimed
    against: `git reset --hard HEAD` leaves the owned file PRESENT, so
    `_unerase` saw nothing missing, `collect` committed the revert and wrote
    `done` printing nothing. HEAD's own bytes back over a snapshot that says
    otherwise is the one modification that is distinguishable, and it is
    undone."""
    rel = "resources/board/plan.py"
    open(os.path.join(d, rel), "w").write("def helper():\n    return 1\n")
    said = []
    collect.guarded_run(["bash", "-e", "-c", "git reset --hard HEAD >/dev/null"],
                        d, owned(d, [rel]), out=said.append)
    got = open(os.path.join(d, rel)).read()
    assert got == "def helper():\n    return 1\n", (got, said)
    assert any("put back" in s and rel in s for s in said), said


def an_ordinary_modification_still_stays(d):
    """The witness that keeps the case above from being "restore everything":
    a block that edits an owned file to something that is NOT HEAD is left
    alone, exactly as `spec02` decided."""
    rel = "resources/board/plan.py"
    open(os.path.join(d, rel), "w").write("# WIP\n")
    collect.guarded_run(["bash", "-e", "-c", f"printf 'formatted\\n' > {rel}"],
                        d, owned(d, [rel]), out=QUIET)
    assert open(os.path.join(d, rel)).read() == "formatted\n"


def a_footprint_symlink_comes_back(d):
    """Pass one's `_owned_files` skipped every symlink, so a footprint link a
    block deleted was never put back — and this repo's own `.pearde` is one.
    The link is snapshotted by its target string and re-made."""
    os.symlink("resources/board", os.path.join(d, "board-link"))
    os.makedirs(os.path.join(d, "sub"), exist_ok=True)
    os.symlink("../README.md", os.path.join(d, "sub/readme-link"))
    feet = ["board-link", "sub"]
    snap = collect._snapshot(d, feet)
    assert snap.get("board-link", (None,))[0] == "link", snap.get("board-link")
    assert snap["board-link"][1] == "resources/board", snap["board-link"]
    said = []
    collect.guarded_run(["bash", "-e", "-c", "rm -f board-link sub/readme-link"],
                        d, owned(d, feet), out=said.append)
    assert os.path.islink(os.path.join(d, "board-link")), said
    assert os.readlink(os.path.join(d, "board-link")) == "resources/board"
    assert os.path.islink(os.path.join(d, "sub/readme-link")), said
    assert os.readlink(os.path.join(d, "sub/readme-link")) == "../README.md"


def a_dangling_footprint_symlink_survives(d):
    """`os.stat` follows a link, so a dangling one dropped out of the snapshot
    entirely. It is read with `readlink`, which does not."""
    os.symlink("nowhere-at-all", os.path.join(d, "dangling"))
    snap = collect._snapshot(d, ["dangling"])
    assert snap == {"dangling": ("link", "nowhere-at-all", 0)}, snap
    collect.guarded_run(["bash", "-e", "-c", "rm -f dangling"], d,
                        owned(d, ["dangling"]), out=QUIET)
    assert os.path.islink(os.path.join(d, "dangling"))


def the_callers_cwd_survives_the_park(d):
    """`_park` stashes the foreign dirt with `git stash push -u`, and git
    REMOVES a directory whose last untracked file it took. When `collect` was
    called from inside the checkout that directory can be the process's own
    cwd — `collect --also <relative path>` resolves against the caller's cwd,
    so it regularly is — and the pop makes the path again as a NEW inode. The
    process still holds the deleted one, so `os.getcwd()`, `os.path.abspath`
    and every relative open raise `FileNotFoundError` for the rest of the run.
    Found by `filing-refuses-a-file-it-does-not-hold`'s harness going 52/52 ->
    45/52 on the guard; `_reattach` stands the process back up."""
    away = os.path.join(d, "away")
    os.makedirs(away)
    open(os.path.join(away, "rider.md"), "w").write("a peer's note\n")
    real, back = os.path.realpath(away), os.getcwd()
    os.chdir(away)
    try:
        collect.guarded_run(["bash", "-e", "-c", "true"], d,
                            owned(d, ["resources/board/plan.py"]), out=QUIET)
        assert os.getcwd() == real, os.getcwd()
        assert os.path.abspath("rider.md") == os.path.join(real, "rider.md")
    finally:
        os.chdir(back)
    assert open(os.path.join(away, "rider.md")).read() == "a peer's note\n"


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
    case("a path with a space is classified, parked, healed and unerased",
         a_spaced_path_is_classified_parked_healed_and_unerased)
    case("a rename is one row naming its destination, not two shifted ones",
         a_rename_is_one_row_naming_its_destination)
    case("a peer's new file is moved aside, not deleted",
         a_peers_new_file_is_not_destroyed)
    case("`put back:` names only what was actually put back",
         heal_names_only_what_it_put_back)
    case("a restore that fails says so", a_failed_restore_says_so)
    case("a peer's staged entry is not wiped", a_peers_staged_entry_is_not_wiped)
    case("a block that reverts owned work to HEAD is undone",
         a_revert_to_head_is_undone)
    case("an ordinary modification by the block still stays",
         an_ordinary_modification_still_stays)
    case("a footprint symlink comes back, target and all",
         a_footprint_symlink_comes_back)
    case("a dangling footprint symlink is snapshotted and restored",
         a_dangling_footprint_symlink_survives)
    case("the caller's cwd survives the park that emptied it",
         the_callers_cwd_survives_the_park)
    print("ALL PASS")
