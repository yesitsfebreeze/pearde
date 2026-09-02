#!/usr/bin/env python3
"""Lanes — one git worktree per worker, on `lane/<slug>`.

A worker never edits the checkout the orchestrator holds. `claim` cuts a
branch `lane/<slug>` off the code repo's HEAD and checks it out into a
worktree of its own; the brief names that worktree as `<repo>`, so every
path the worker writes lands there. `collect` merges the lane back into the
branch the checkout is on, runs the verify blocks and the gate on the
MERGED tree, and commits there. `sweep` removes the worktree of a claim it
releases.

Where the worktree lives: `<board>/.lanes/<slug>`. The board dir is already
machine-local scratch on the code repo (`.pearde/` is gitignored) and
`.lanes/` is a dotfile directly under the board, which `collect.scratch`
skips and the board's own `.gitignore` drops — so a lane costs no row in
either repo. Outside the code repo would need a directory the user never
asked for; inside it, anywhere but under the board, would be dirt on every
`git status` the person runs.

The branch name is fixed: `plan.LANE_RE` already reads `lane/<slug>` as
work on this machine, and the lane bar is drawn off it.
"""

import os
import re
import subprocess

LANES_DIR = ".lanes"


class LaneError(Exception):
    """git said no. The message is what the caller prints."""


def branch_of(slug):
    """`lane/<slug>` — `plan.LANE_RE` reads it back. A nested PRD's rel
    carries `/`, which a branch name takes as a path component; the lane
    for `a/b` is `lane/a-b`, one segment under `lane/`, so the ref never
    collides with a directory ref of the same prefix."""
    return "lane/" + re.sub(r"[^A-Za-z0-9._-]+", "-", str(slug)).strip("-")


def lane_dir(board, slug):
    return os.path.join(board, LANES_DIR,
                        re.sub(r"[^A-Za-z0-9._-]+", "-", str(slug)).strip("-"))


def git(root, *args, check=True):
    r = subprocess.run(("git", "-C", root) + args,
                       capture_output=True, text=True, timeout=60)
    if check and r.returncode != 0:
        raise LaneError((r.stderr or r.stdout).strip()
                        or f"git {' '.join(args)} exit {r.returncode}")
    return r


def exists(board, slug):
    return os.path.isdir(lane_dir(board, slug))


def create(board, repo, slug, base=None):
    """Cut `lane/<slug>` off `base` (the repo's HEAD by default) and check
    it out at `<board>/.lanes/<slug>`. Returns the worktree path.

    Idempotent on the path: a lane dir that is already a worktree of this
    repo is returned as it stands — a re-claim after a `failed` continues
    the work that is standing there, which is the whole point of leaving a
    probe uncommitted. A path that exists and is NOT a worktree is a
    refusal, never a silent reuse."""
    d = lane_dir(board, slug)
    br = branch_of(slug)
    if os.path.isdir(d):
        if os.path.exists(os.path.join(d, ".git")):
            return d
        raise LaneError(f"lane: {d} exists and is not a worktree — "
                        "move it or remove it")
    os.makedirs(os.path.dirname(d), exist_ok=True)
    have = git(repo, "rev-parse", "--verify", "--quiet", br,
               check=False).returncode == 0
    if have:
        git(repo, "worktree", "add", d, br)
    else:
        args = ["worktree", "add", "-b", br, d]
        if base:
            args.append(base)
        git(repo, *args)
    return d


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


def merge(repo, slug, out=None):
    """Merge `lane/<slug>` into the branch the checkout is on, no fast
    forward off, `--no-commit` never: the lane's own commits land, and
    `collect`'s commit rides on top of the merged tree.

    A conflict is left in the tree and raised — the caller reports it red
    and names the files. `--abort` is the caller's call, not this one's: a
    conflict the person can fix by hand is worth more than a clean rollback
    that loses which file disagreed."""
    br = branch_of(slug)
    if git(repo, "rev-parse", "--verify", "--quiet", br,
           check=False).returncode != 0:
        return None                      # no lane: nothing to merge
    ahead = git(repo, "rev-list", "--count", "HEAD.." + br).stdout.strip()
    if ahead in ("", "0"):
        return 0                         # the lane committed nothing
    r = git(repo, "merge", "--no-edit", br, check=False)
    if r.returncode != 0:
        files = conflicts(repo)
        git(repo, "merge", "--abort", check=False)
        raise LaneError(
            f"merge conflict: {br} into "
            f"{git(repo, 'rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()}"
            f" — {', '.join(files) if files else 'see git status'}")
    return int(ahead)


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
