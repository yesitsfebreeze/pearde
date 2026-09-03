#!/usr/bin/env python3
"""pearde repos — the git tree under a board, and the lanes cut off it.

Cut out of plan.py; plan.py re-exports every name here, so every caller that
imports `plan` keeps working. Python 3 stdlib only.
"""
import collections
import datetime
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
# win: a cp1252 console cannot encode the box/greek glyphs this prints,
# and the trailing summary dies on UnicodeEncodeError. Force UTF-8 out.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memos as memolib  # noqa: E402 — the skill root, one dir up
import questions as qlib  # noqa: E402 — the drill count, one reader with list
import render as renderlib  # noqa: E402 — beside this script
import workflows as wflib  # noqa: E402 — the skill root, one dir up


# ── lanes: what main has not seen ─────────────────────────────────────────────
# Work happens on a branch per PRD — `lane/<slug>` or `lane/<n>-<slug>` — and
# it lands by merging into that repo's main.
# A lane that is still unmerged is work that exists on this machine and nowhere
# else, no matter what the board says about it.
#
# The board and git each know half of it, and neither half is enough: the board
# knows the work is finished and its acceptance boxes are closed, git knows main
# has never seen the commits. Crossing them is the whole point — a finished PRD
# whose lane is merged is history, an unmerged lane whose PRD is still open is
# in flight, and only the intersection is a queue of things to land.

LANE_RE = re.compile(r"^lane/(?:(\d+)-)?(.+?)(?:-\d+)?$")
LANE_TTL = 3.0          # git is cheap, but not once per row per render
_LANES = {}             # board path -> (expires, scan)


def repo_root(path):
    """The repo a board sits in, by walk-up. `git rev-parse --show-toplevel`
    answers the same question and costs a fork, and the watcher asks once a
    second per board — so it walks."""
    d = os.path.abspath(path)
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        nxt = os.path.dirname(d)
        if nxt == d:
            return None
        d = nxt


def ref_stamp(path):
    """The git side of a board, as (mtime, size) over the refs a merge moves.
    Pure stats: this is what the watcher polls to notice that a lane landed,
    and it must not fork anything. A `.git` file (a worktree) has no refs of
    its own here and stamps as nothing."""
    root = repo_root(path)
    g = os.path.join(root, ".git") if root else None
    if not g or not os.path.isdir(g):
        return ()
    out = []
    for rel in ("refs/heads", "packed-refs", "HEAD"):
        try:
            st = os.stat(os.path.join(g, rel))
            out.append((rel, st.st_mtime_ns, st.st_size))
        except OSError:
            out.append((rel, 0, 0))
    return (root, tuple(out))


def git(root, *args):
    """stdout, or None if git said no. Never raises: a board that is not in a
    repo is an ordinary case here, not an error."""
    try:
        r = subprocess.run(("git", "-C", root) + args,
                           capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def scan_lanes(path):
    """{"root", "ahead", "lanes": {slug: {"branch"}}} for one board.

    `ahead` is main's commits that origin has not got — None when the repo has
    no remote at all, which is a different thing from being in sync and is
    drawn as such. A board outside a repo scans to nothing and says so quietly.

    Only `lane/` branches count — the agent worktrees (`worktree-wf_*`) are
    scratch, not lanes."""
    root = repo_root(path)
    if not root:
        return {"root": None, "ahead": None, "lanes": {}}
    lanes = {}
    out = git(root, "branch", "--no-merged", "main",
              "--format=%(refname:short)") or ""
    for b in out.split("\n"):
        m = LANE_RE.match(b.strip())
        if m:
            slug = m.group(2)
            # a retry (`-2`, `-3`) is the same lane; first branch name wins
            if slug not in lanes:
                lanes[slug] = {"branch": b.strip()}
    ahead = None
    if git(root, "remote", "get-url", "origin"):
        n = git(root, "rev-list", "--count", "origin/main..main")
        ahead = int(n.strip()) if n and n.strip().isdigit() else None
    return {"root": root, "ahead": ahead, "lanes": lanes}


def lanes(path):
    now = time.time()
    hit = _LANES.get(path)
    if hit and hit[0] > now:
        return hit[1]
    got = scan_lanes(path)
    _LANES[path] = (now + LANE_TTL, got)
    return got
