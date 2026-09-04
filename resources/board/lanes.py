#!/usr/bin/env python3
"""Lanes — one git worktree per worker, on `lane/<slug>`.

A worker never edits the checkout the orchestrator holds. `claim` cuts a
branch `lane/<slug>` off the code repo's HEAD and checks it out into a
worktree of its own; the brief names that worktree as `<repo>`, so every
path the worker writes lands there. `collect` merges the lane back into the
branch the checkout is on, runs the verify blocks and the gate on the
MERGED tree, and commits there. `sweep` removes the worktree of a claim it
releases.

Where the worktree lives: `<board>/.lanes/<slug>`. `.lanes/` is a dotfile
directly under the board, so `collect.scratch` skips it and no lane is ever
offered to a commit. Outside the code repo would need a directory the user
never asked for; inside it, anywhere but under the board, would be dirt on
every `git status` the person runs.

**That is the commit, not the ignore, and the two are not the same guard.**
This said the board dir was machine-local scratch because `.pearde/` is
gitignored — which is false wherever the plan is tracked, and the plan is
tracked on any board whose PRDs are meant to be shared. There `git status`
sees the worktrees, and `git add -A` stages them: one board mid-pass held
seven lanes and 36 GB. `init.ignored_names` and `init.BOARD_IGNORED` carry
`.lanes/` for exactly this reason; a board initialised before they did has
to be told once.

The branch name is fixed: `plan.LANE_RE` already reads `lane/<slug>` as
work on this machine, and the lane bar is drawn off it.
"""

import os
import re
import sys

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import common  # noqa: E402

LANES_DIR = ".lanes"


class LaneError(Exception):
    """git said no. The message is what the caller prints."""


class Conflict(LaneError):
    """The lane and the branch it lands on disagree about a file, and no
    tool can pick. A subclass, so every caller that already catches
    `LaneError` keeps working; the extra attributes are for the one caller
    that reports it instead of stopping.

    `files` is what git named on the conflict, `branch` is `lane/<slug>`
    and `onto` is the branch it was landing on. They are carried as data
    and not only in the message because the caller writes them into
    `prd.md`, and re-parsing a sentence to get a file list back is how a
    reason drifts from what git actually said."""

    def __init__(self, message, branch, onto, files):
        super().__init__(message)
        self.branch, self.onto, self.files = branch, onto, list(files)


def branch_of(slug):
    """`lane/<slug>` — `plan.LANE_RE` reads it back. A nested PRD's rel
    carries `/`, which a branch name takes as a path component; the lane
    for `a/b` is `lane/a-b`, one segment under `lane/`, so the ref never
    collides with a directory ref of the same prefix."""
    return "lane/" + re.sub(r"[^A-Za-z0-9._-]+", "-", str(slug)).strip("-")


def lane_dir(board, slug):
    return os.path.join(board, LANES_DIR,
                        re.sub(r"[^A-Za-z0-9._-]+", "-", str(slug)).strip("-"))


def _may_discard(tree):
    """May this process throw `tree`'s uncommitted work away? The rule and
    the reasoning are @resources/board/refuse.py. False when the module will
    not load: a lane whose dirt is left standing is a report a person can
    read, and the alternative is the loss that memo records."""
    try:
        import refuse as refuselib
        ok, _ = refuselib.allowed(refuselib.board_above(None, tree), tree)
        return ok
    except Exception:
        return False


def git(root, *args, check=True):
    return common.run_git(root, *args, check=check, raise_as=LaneError)


def exists(board, slug):
    return os.path.isdir(lane_dir(board, slug))


def board_rel(board, repo):
    """The board's path inside the code repo, or None when the board is
    not under it. `.pearde/` gitignored by its own repo answers None as
    surely as a board kept somewhere else does — the caller only needs the
    string when the repo TRACKS the board, and an untracked path costs the
    sparse-checkout exclusion nothing."""
    rel = os.path.relpath(os.path.abspath(board), os.path.abspath(repo))
    if rel == os.curdir or rel.startswith(os.pardir) or os.path.isabs(rel):
        return None
    return rel.replace(os.sep, "/")


def create(board, repo, slug, base=None):
    """Cut `lane/<slug>` off `base` (the repo's HEAD by default) and check
    it out at `<board>/.lanes/<slug>`. Returns the worktree path.

    The lane is materialised WITHOUT the board directory. A repo that
    tracks its own `.pearde/` hands every worktree a stale copy of the
    board, and a worker running any board command from its lane resolves
    to that phantom: measured, `pearde scan` from inside a lane printed
    `0 PRDs` against a live board holding one — silently, no error. So the
    worktree is added `--no-checkout`, the board's path is excluded by a
    `--no-cone` sparse-checkout, and the checkout follows. The excluded
    path keeps its skip-worktree bit, so a later `git add -A` in the lane
    does not delete the board from the tree (measured: it did not). A
    board the repo does not track needs none of this and gets it anyway,
    where it costs one command and no behaviour.

    The lane's regenerable directories are shared, not rebuilt.
    `link_shared` points `node_modules`, the graphify cache and the
    Obsidian plugin bundles at one copy per machine under the git common
    dir. Measured on this repo: the checkout git tracks is 2.1 MB, and 27
    lanes held 143 MB — the difference is entirely what each lane
    regenerated for itself. Sharing runs after the checkout, on ignored
    paths only, and never fails a claim: a store that cannot be written is
    a lane with its own copies, which is exactly where this started.

    Idempotent on the path: a lane dir that is already a worktree of this
    repo is returned as it stands — a re-claim after a `failed` continues
    the work that is standing there, which is the whole point of leaving a
    probe uncommitted. Sharing is re-run on that path too, so a lane cut
    before the store existed picks it up on its next claim. A path that
    exists and is NOT a worktree is a refusal, never a silent reuse."""
    d = lane_dir(board, slug)
    br = branch_of(slug)
    if os.path.isdir(d):
        if os.path.exists(os.path.join(d, ".git")):
            link_shared(d)
            return d
        raise LaneError(f"lane: {d} exists and is not a worktree — "
                        "move it or remove it")
    os.makedirs(os.path.dirname(d), exist_ok=True)
    have = git(repo, "rev-parse", "--verify", "--quiet", br,
               check=False).returncode == 0
    if have:
        git(repo, "worktree", "add", "--no-checkout", d, br)
    else:
        args = ["worktree", "add", "--no-checkout", "-b", br, d]
        if base:
            args.append(base)
        git(repo, *args)
    rel = board_rel(board, repo)
    if rel and os.path.exists(os.path.join(board, ".git")):
        # Only when the board is its OWN git repo. The exclusion and the
        # symlink back are how a lane runs a board it does not hold — a
        # repo that tracks its own `.pearde/` hands every worktree a stale
        # copy otherwise. A board that is not a repo has nothing to exclude:
        # its files are not in the code repo's index at all, and symlinking
        # them in makes them paths "beyond a symbolic link" that `git
        # rebase` refuses — measured 2026-09-04 on the flat layout in
        # `a-board-s-own-file-commits-in-the-board-repo`, whose fixture cut
        # a lane at `.pearde/.lanes/p1` and died
        # `'.pearde/prds/p1/prd.md' is beyond a symbolic link` before a
        # single file was staged.
        git(d, "sparse-checkout", "set", "--no-cone", "/*",
            "!/" + rel, check=False)
        git(d, "checkout")
        link_board(board, repo, d)
    else:
        git(d, "checkout")
    link_shared(d)
    return d


def link_board(board, repo, tree):
    """Point the tree's excluded board path at the one real board.

    `create` and `session.take` both sparse-check the board OUT of their
    worktree, so a spec whose verify block runs `.pearde/prds/<prd>/probe/…`
    exits 127 there and the collect refuses on a probe that is fine. One
    symlink back is what a tree needs to run the board's own scripts.
    Advisory like `link_shared`: a tree that cannot be linked still works
    for everything that does not read the board."""
    rel = board_rel(board, repo)
    if not rel:
        return None
    dst = os.path.join(tree, rel)
    if os.path.lexists(dst):
        return dst
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        os.symlink(os.path.relpath(os.path.abspath(board),
                                   os.path.dirname(os.path.abspath(dst))), dst)
    except OSError:
        return None
    return dst


def link_shared(tree):
    """Point this tree's regenerable directories at the machine's one copy.
    Returns what changed, or [] when nothing could be done.

    Advisory by construction. A claim that dies because a cache could not
    be symlinked has traded a disk problem for a work problem, so every
    failure here — the module absent, the store unwritable, a path git
    turns out to track — leaves the lane with its own copies and says
    nothing. `pearde share` is where a person asks why."""
    try:
        import shared as sharedlib
        return [r for r in sharedlib.apply_tree(tree)
                if r["action"] not in ("linked", "skipped")]
    except Exception:
        return []


def remove(board, repo, slug, force=True):
    """Drop the worktree. The BRANCH stays — an unmerged lane is work this
    machine holds and `plan.lanes` draws it; removing the branch would
    erase a swept worker's commits. Uncommitted dirt in the lane dies with
    the worktree, which is what a sweep means."""
    d = lane_dir(board, slug)
    if not os.path.isdir(d):
        return False
    args = ["worktree", "remove"] + (["--force"] if force else []) + [d]
    git(repo, *args)
    git(repo, "worktree", "prune", check=False)
    return True


def worktree_of(repo, branch):
    """The worktree `branch` is checked out in, or None. `rebase` has to
    run where the branch lives — git refuses to move a branch another
    worktree holds — and `merge` is handed a slug, not a path."""
    out = git(repo, "worktree", "list", "--porcelain", check=False).stdout
    path = None
    for line in out.splitlines():
        if line.startswith("worktree "):
            path = line[len("worktree "):].strip()
        elif line.strip() == "branch refs/heads/" + branch:
            return path
    return None


def cut_base(repo, slug):
    """The commit `lane/<slug>` was cut off — the merge base of the branch
    the checkout is on and the lane. `None` when there is no lane branch.

    Read it BEFORE `merge` runs: the rebase there replays the lane onto the
    checkout's HEAD, and from that moment the merge base IS that HEAD. The
    answer afterwards is not wrong, it is a different question — nothing
    has moved since the lane was re-based — and it names no file."""
    br = branch_of(slug)
    if git(repo, "rev-parse", "--verify", "--quiet", br,
           check=False).returncode != 0:
        return None
    return git(repo, "merge-base", "HEAD", br,
               check=False).stdout.strip() or None


def moved_since_cut(repo, slug):
    """The files the checkout's branch changed since the lane was cut, in
    git's own spelling, relative to the repo root, sorted. `[]` when there
    is no lane and when nothing landed while the worker ran.

    This is exactly the set the rebase in `merge` is about to replay the
    worker's commits on top of — what moved under the worker's feet. The
    caller narrows it to the footprint: every other name is a file the PRD
    never claimed, and printing those would make the line unreadable on any
    repo where landing anything is normal."""
    base = cut_base(repo, slug)
    if not base:
        return []
    head = git(repo, "rev-parse", "HEAD", check=False).stdout.strip()
    if not head or base == head:
        return []
    out = git(repo, "diff", "--name-only", base + ".." + head,
              check=False).stdout
    return sorted({l.strip() for l in out.splitlines() if l.strip()})


def merge(repo, slug, out=None):
    """Land `lane/<slug>` on the branch the checkout is on as the lane's
    OWN commits, and no others. Returns how many landed.

    Rebase, then `merge --ff-only`. A plain `git merge` onto a checkout
    that moved since the lane was cut writes a merge commit on top of the
    lane's — two commits for one PRD, and
    @references/parts/commits.md says one. `merge --squash` gives one
    commit and leaves the branch reading unmerged forever, which would
    break the lane bar `plan.lanes` draws off `git branch --merged`.
    Rebasing first measured linear, one commit, and `--merged` listed the
    lane.

    A conflict — in the rebase or in the merge — raises `Conflict` with the
    files on it, the lane branch left exactly as it was, and the checkout on
    the commit it was on. The caller reports it: `collect.land_lane` turns it
    into a `blocked` PRD naming those files, so no lane sits `claimed` with a
    conflict nobody was told about. A conflict a person can fix by hand is
    worth more than a rollback that loses which file disagreed, so the files
    are read before anything is aborted.

    A rebase that never gets under way is not a conflict: `git rebase`
    refuses outright when the lane's tree is dirty (exactly what
    `land_lane` leaves standing on paths outside the footprint — see
    `resources/board/collect.py`), and starts no rebase at all. `rebase
    --abort` then fails with "no rebase in progress" — measured: exit 128,
    nothing changed — and a `reset --hard` run anyway would discard that
    dirt though nothing of the lane's history ever moved (measured: the
    worker's uncommitted change was gone after, `git status` clean, the
    branch tip unchanged throughout). So the hard reset runs only once
    `rebase --abort` itself reports a rebase it actually stopped;
    otherwise the lane is left exactly as it was handed to this
    function, dirt included, and the raise below is the only effect."""
    br = branch_of(slug)
    if git(repo, "rev-parse", "--verify", "--quiet", br,
           check=False).returncode != 0:
        return None                      # no lane: nothing to merge
    ahead = git(repo, "rev-list", "--count", "HEAD.." + br).stdout.strip()
    if ahead in ("", "0"):
        return 0                         # the lane committed nothing
    onto = git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    wt = worktree_of(repo, br)
    if wt:
        was = git(wt, "rev-parse", br).stdout.strip()
        r = git(wt, "rebase", onto, check=False)
        if r.returncode != 0:
            files = conflicts(wt)
            aborted = git(wt, "rebase", "--abort", check=False)
            if aborted.returncode == 0 and _may_discard(wt):
                # a real rebase was under way — `--abort` already put the
                # branch and its tree back at `was`; this is redundant
                # belt-and-suspenders for it, never the first thing to
                # touch the tree. `_may_discard` is the second condition
                # because `wt` is a WORKER's tree and this process is not
                # in it: the memo
                # `a-session-that-writes-a-shared-checkout-can-revert-
                # another-session-s-work` puts `reset --hard` out of bounds
                # in a tree the running session does not own, and a
                # redundant reset is the cheapest thing on this board to
                # give up.
                git(wt, "reset", "--hard", was, check=False)
            raise Conflict(
                f"merge conflict: {br} onto {onto} — "
                + (", ".join(files) if files else "see git status"),
                br, onto, files)
        ahead = git(repo, "rev-list", "--count", "HEAD.." + br).stdout.strip()
    r = git(repo, "merge", "--ff-only", "--no-edit", br, check=False)
    if r.returncode != 0:
        files = conflicts(repo)
        git(repo, "merge", "--abort", check=False)
        raise Conflict(
            f"merge conflict: {br} into {onto} — "
            + (", ".join(files) if files else "see git status"),
            br, onto, files)
    return int(ahead or 0)


def conflicts(repo):
    out = git(repo, "diff", "--name-only", "--diff-filter=U",
              check=False).stdout
    return [l for l in out.splitlines() if l.strip()]


def dirty(board, slug):
    """The lane's uncommitted paths — what a worker left standing."""
    d = lane_dir(board, slug)
    if not os.path.isdir(d):
        return []
    out = git(d, "status", "--porcelain", check=False).stdout
    return [l[3:] for l in out.splitlines() if l.strip()]


def commit_all(board, slug, message):
    """Commit everything standing in the lane, on the lane's branch. The
    worker never commits; this is the ORCHESTRATOR closing the lane before
    it merges — one commit per PRD, in the lane, and the merge carries it
    into the checkout's branch."""
    d = lane_dir(board, slug)
    if not os.path.isdir(d):
        return None
    git(d, "add", "-A")
    if not git(d, "diff", "--cached", "--quiet", check=False).returncode:
        return None                      # nothing staged
    git(d, "commit", "-m", message)
    return git(d, "rev-parse", "HEAD").stdout.strip()[:12]


def list_lanes(board):
    d = os.path.join(board, LANES_DIR)
    if not os.path.isdir(d):
        return []
    return sorted(x for x in os.listdir(d)
                  if os.path.isdir(os.path.join(d, x)))


def _finds_board(entry, board):
    """`entry` (a direct child of a lane) resolves to the live board."""
    try:
        return os.path.realpath(entry) == os.path.realpath(board)
    except OSError:
        return False


def check(board):
    """One line per lane, on this machine, that cannot reach the live
    board — `doctor`'s row. `create` sparse-checks the board's own path
    out of every lane and symlinks it back in (see `link_board`, where
    that exists); a lane cut before that symlink was added, or cut while
    the caller's own `repo` was a session worktree NESTED inside the
    board (`board_rel` answers None there — the board is the session
    tree's ancestor, not the other way round — so the link is silently
    never made), keeps the exclusion and loses the link. Either way the
    lane's own `.pearde/prds/…` (or whatever this board is called) is
    `No such file or directory`, and nothing before this said so — a
    worker finds out only when a probe it wrote exits 127 inside it.

    Scans the lane's own top level only: every board this repo has ever
    named sits directly under a repo root, and a board nested deeper is
    outside what this check can tell apart from an ordinary subdirectory.
    """
    problems = []
    for slug in list_lanes(board):
        d = lane_dir(board, slug)
        if not os.path.exists(os.path.join(d, ".git")):
            continue                                   # not a worktree
        try:
            names = os.listdir(d)
        except OSError:
            continue
        if not any(_finds_board(os.path.join(d, n), board) for n in names):
            problems.append(f"{slug}: no link to the board")
    return problems


def relink(board, slug):
    """The repair `doctor --fix` runs for one `check` line: a plain
    symlink to the board, named after it, at the lane's root — where
    `link_board` puts it for the ordinary (board sits at the repo root)
    case. Refuses rather than overwrites when something already answers
    that name and it is not this link; returns the path made, or None."""
    d = lane_dir(board, slug)
    if not os.path.exists(os.path.join(d, ".git")):
        return None
    dst = os.path.join(d, os.path.basename(os.path.abspath(board)))
    if os.path.lexists(dst):
        return dst if _finds_board(dst, board) else None
    try:
        os.symlink(os.path.relpath(os.path.abspath(board), d), dst)
    except OSError:
        return None
    return dst
