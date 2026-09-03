#!/usr/bin/env python3
"""pearde silence — whether a held PRD is still moving.

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

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import memos as memolib  # noqa: E402 — on the path by the rule
import questions as qlib  # noqa: E402 — the drill count, one reader with list
import render as renderlib  # noqa: E402 — on the path by the rule
import workflows as wflib  # noqa: E402 — on the path by the rule
from prdfile import (bad_value, claim_of, hours, standing)  # noqa: E402,F401
from repos import (repo_root)  # noqa: E402,F401
from registry import (MEMBER_SIGIL, spec_data)  # noqa: E402,F401

# ── silence ──────────────────────────────────────────────────────────────────
# The board cannot see a worker. What it can see is files: an implementer
# writes in the repo, an analyst's probe lives in the PRD folder, and either
# moving is a live worker. A claim whose files have not moved for longer than
# `claim-ttl` is silent. `silent_of` is the one rule — the scan line, the
# page's row and `sweep` read it from here, so none of them can disagree about
# which claim has gone quiet. Read off files, never off a process.
CLAIM_TTL = "30m"
SILENT_STATES = {"claimed", "analyzing"}   # the in-flight band, and only it


def claim_ttl(settings):
    """`claim-ttl` from settings.md, in minutes. `30m`, `2h`, `1d` read as
    `hours()` reads them; a bare number is minutes. Default 30."""
    v = str(settings.get("claim-ttl", CLAIM_TTL) or CLAIM_TTL).strip()
    if v.isdigit():
        return float(v)
    h = hours(v)
    if h <= 0:
        bad_value("settings.md", "claim-ttl", v)
        return 30.0
    return h * 60


def prd_repo(prd):
    """Where the PRD's code lives — `collect`'s rule (`repo_of` there):
    `repo:` that is a directory, absolute or relative to the board's repo,
    else the board's own repo. The footprint silence is read over is the one
    collect commits.

    "The board's own repo" is the CODE repo, not the board dir. `repo_root`
    stops at any `.git`, and a board that is a git repo of its own — a nested
    `.pearde` with its own `.git`, or a linked worktree whose `.pearde/.git`
    is a gitdir file, which is what this machine runs — answers with the
    board itself; every footprint would then resolve under `.pearde/` to
    nothing and `newest_mtime` read 0.0. So when the walk stops AT the board,
    step out and walk from its parent, exactly as `repo_of` does. A board
    that is a plain subdirectory of its repo never trips this: the walk went
    past it already."""
    board = os.path.abspath(prd["board_path"])
    root = repo_root(board)
    if root == board:
        root = repo_root(os.path.dirname(board)) or root
    root = root or os.path.dirname(board)
    raw = str(prd["fm"].get("repo", "") or "").strip()
    if raw:
        for cand in (raw, os.path.join(root, raw)):
            if os.path.isdir(cand):
                r = repo_root(cand)
                if r:
                    return session_tree(board, r)
    return session_tree(board, root)


def session_tree(board, root):
    """`root`, or the worktree the running session holds of it — the same
    last step `collect.repo_of` takes, so silence is measured in the tree
    the session's own commands write. The import is here and not at the top:
    `session` imports THIS module, and a module-level import either way
    round is a cycle. It is also the reason this is a function and not one
    more line inside `prd_repo` — `session.instead_of` swallows its own
    failures, so a board with no ledger costs one dict lookup."""
    try:
        import session as sessionlib
    except ImportError:
        return root
    return sessionlib.instead_of(board, root)


def newest_mtime(paths):
    """The newest mtime under any of `paths` — a file's own, a directory's
    walked, dot-dirs and `__pycache__` skipped since nothing a worker does
    lives there. A path that is not on disk counts nothing: a footprint names
    what the work will touch, not what exists yet."""
    newest = 0.0
    for p in paths:
        if os.path.isfile(p):
            try:
                newest = max(newest, os.stat(p).st_mtime)
            except OSError:
                pass
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs
                           if not d.startswith(".") and d != "__pycache__"]
                for f in files:
                    try:
                        newest = max(newest,
                                     os.stat(os.path.join(root, f)).st_mtime)
                    except OSError:
                        pass
    return newest


def silent_of(prd, settings, collect=None, now=None):
    """Minutes since anything of this PRD's last moved, when that is longer
    than `claim-ttl`; None otherwise. THE rule for a quiet worker.

    "Anything of this PRD's" is its directory and every path of its footprint
    union — the PRD's own plus its specs', the union `collect` commits — in
    its repo. Only a held PRD in the in-flight band can be silent: a `blocked`
    one is waiting on a person, and a PRD to collect is a worker that
    finished, which is the opposite of one that went quiet. `collect` is
    `standing()`'s verdict; pass it when you already hold it."""
    if prd["state"] not in SILENT_STATES or not claim_of(prd["fm"]):
        return None
    if collect is None:
        collect = standing(prd)[3]
    if collect:
        return None
    repo = prd_repo(prd)
    _, feet = spec_data(prd)
    paths = [prd["dir"]] + [os.path.join(repo, f) for f in feet
                            if not f.startswith(MEMBER_SIGIL)]
    newest = newest_mtime(paths)
    if not newest:
        return None
    age = ((time.time() if now is None else now) - newest) / 60
    return age if age >= claim_ttl(settings) else None


def fmt_age(minutes):
    """`42m` under ninety minutes, `1.5h` past it — the page's own spelling
    for a holding time, so the scan and the row read the same word."""
    return f"{round(minutes)}m" if minutes < 90 else f"{minutes / 60:.1f}h"
