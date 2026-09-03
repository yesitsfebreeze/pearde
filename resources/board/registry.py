#!/usr/bin/env python3
"""pearde registry — the PRDs a board holds and the boards a master merges.

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
from boards import (BOARD_DIR, BOARD_DIRS, PRDS_DIR, prds_dir)  # noqa: E402,F401
import prdfile  # noqa: E402 — a rebound global, read live
from prdfile import (dur, num, parse_cache_load, parse_cache_save, parse_prd)  # noqa: E402,F401



# ── master boards ─────────────────────────────────────────────────────────────
# A master board merges other boards into one plan. The PRDs never move: each
# member keeps its own prds/, its own settings, its own view, and the
# orchestrator writes state into the member's own prd.md. Only the plan — the
# edges, the schedule, the merged mirror — lives at the master.
#
# A member PRD is addressed `@<member>/<rel>` board-wide. The sigil is what
# makes one flat namespace safe: a PRD directory is never named `@…`, so a
# qualified rel can never collide with a master's own PRD.
MEMBER_SIGIL = "@"

MEMBER_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def members(board):
    """[(name, path)] — the member boards a master board merges.

    `members:` in prds/settings.md, one `- <path>` or `- <name>: <path>` per
    line. A relative path resolves against the board dir, so a master beside
    its members reads `- ../model/prds`; a path at a repo root gains `/prds`
    when that exists. The name is the address, so it defaults to the same
    walk-up that names the board and is suffixed rather than replaced
    on a collision — two members must never share a key."""
    raw = board_settings(board).get("members", [])
    if isinstance(raw, str):
        raw = [raw]
    out, seen = [], set()
    for item in raw:
        head, sep, tail = str(item).partition(":")
        if sep and MEMBER_NAME_RE.match(head.strip()):
            name, path = head.strip(), tail
        else:
            name, path = "", str(item)
        path = os.path.expanduser(path.strip())
        # absolute always: this path is handed to the daemon, which walks it
        # from a working directory that has nothing to do with the board's
        path = os.path.abspath(os.path.join(board, path))
        # A member names a BOARD, not a prds dir: the old layout had the two
        # coincide (`<root>/prds`), so appending `/prds` when it exists was
        # right. Since the board moved to `<repo>/.pearde`, that test also
        # fires on a nested board — `.pearde` holding `prds/` — and the
        # double board then double-joins in _scan_one (`.pearde/prds/prds`),
        # which walks nothing and silently drops every member PRD. Distinguish:
        # the board dir IS its `.git`-holding `.pearde` (its own git repo) or
        # holds the board's settings.md — then it is the board, and _scan_one
        # wants just it.
        # A member path is a board when it IS a `.pearde` — its own git
        # repo, or it holds the board's settings.md, or its basename says so.
        # Passing such a path through the `/prds` append below would make
        # `_scan_one` walk `.pearde/prds/prds` and scan nothing: a nested
        # board member read as empty. Any other path with a `prds/` inside
        # is the old repo-root member, and `/prds` is appended as before.
        is_nested_board = (os.path.basename(path) in BOARD_DIRS
                           or os.path.isfile(os.path.join(path, "settings.md"))
                           or os.path.isdir(os.path.join(path, ".git")))
        if not is_nested_board and os.path.isdir(
                os.path.join(path, "prds")):
            path = os.path.join(path, "prds")
        name = name or re.sub(r"[^A-Za-z0-9_.-]", "-", project_name(path))
        base, n = name, 2
        while name in seen:
            name, n = f"{base}-{n}", n + 1
        seen.add(name)
        out.append((name, path))
    return out


def is_master(board):
    return bool(members(board))


def qualify_paths(prd, paths):
    """A member's footprint is written relative to its own repo, so two
    projects both touching `src/lib.ts` are not touching the same file:
    qualify it with the member name before anything compares two of them. An
    absolute path is left as written — that is how a deliberate cross-repo
    overlap still clashes."""
    b = prd.get("board")
    if not b:
        return paths
    return [p if p.startswith("/") else f"{MEMBER_SIGIL}{b}/{p}" for p in paths]


def _scan_one(board, prefix="", bname=None):
    prds = {}
    scan_root = prds_dir(board)
    for root, dirs, files in os.walk(scan_root):
        dirs[:] = [d for d in dirs if d not in ("specs",)]
        if "prd.md" in files and root != scan_root:
            local = os.path.relpath(root, scan_root)
            rel = prefix + local
            fm, title, body = parse_prd(os.path.join(root, "prd.md"))
            prds[rel] = {
                "rel": rel,
                "local": local,
                "name": os.path.basename(local),
                "fm": fm,
                "title": title or os.path.basename(local),
                "body": body,
                "state": fm.get("state", "open"),
                "dir": root,
                "board": bname,            # None on the board's own PRDs
                "board_path": board,
                # where a reader finds the file: the real path for a member,
                # the contract path for the board's own
                "footer": (os.path.join(root, "prd.md") if bname
                           else f"{BOARD_DIR}/{PRDS_DIR}/{local}/prd.md"),
            }
    return prds


def scan(board):
    """{rel: prd} for every dir holding prd.md — the board's own, and every
    member board's when this is a master, addressed `@<member>/<rel>`.

    Loads the parse cache from this board's `.state/` first (every prd.md and
    spec on the board and its members is keyed by abspath, and every call
    stats the file, so a member's edit is a miss whatever board holds the
    cache) and saves the merged entries back after."""
    parse_cache_load(board)
    prds = _scan_one(board)
    for name, path in members(board):
        if os.path.isdir(path):
            prds.update(_scan_one(path, f"{MEMBER_SIGIL}{name}/", name))
    for rel, p in prds.items():
        p["children"] = [r for r in prds if os.path.dirname(r) == rel]
        parent = os.path.dirname(rel)
        p["parent"] = parent if parent in prds else None
    if prdfile._PCACHE_DIRTY:
        parse_cache_save(board)
    return prds


def spec_data(prd):
    """(weight, footprints) unioned over specs/*.md, plus the PRD's own
    `footprint:`. The weight is each spec's `complexity`, falling back to its
    `est`. A PRD declares its footprint before it is specced and while an
    implementer holds its spec files — the planner needs the paths either way,
    and frontmatter on prd.md is the one place no worker writes."""
    sdir = os.path.join(prd["dir"], "specs")
    own = prd["fm"].get("footprint", [])
    feet = list(own) if isinstance(own, list) else [own]
    est = 0.0
    if os.path.isdir(sdir):
        for f in sorted(os.listdir(sdir)):
            if f.endswith(".md"):
                fm, _, _ = parse_prd(os.path.join(sdir, f))
                fp = fm.get("footprint", [])
                feet += fp if isinstance(fp, list) else [fp]
                where = f"{prd['rel']}/specs/{f}"
                est += (num(fm, "complexity", where)
                        or dur(fm, "est", where))
    return est, qualify_paths(prd, [f.rstrip("/") for f in feet if f])

def project_name(board):
    """The board's containing dir names the project — except a dot-dir
    (`.mi/prds`), which is not a name anyone means: walk up until an ancestor
    can carry it. `board` as the last resort, never empty."""
    d = os.path.dirname(os.path.abspath(board))
    while d and d != "/":
        base = os.path.basename(d)
        if base and not base.startswith("."):
            return base
        # dirname's fixpoint is not always "/" — a Windows drive root ("C:/")
        # maps to itself, and without this guard the walk never exits
        nxt = os.path.dirname(d)
        if nxt == d:
            break
        d = nxt
    return "board"


def infer_name(board):
    """A master board's name from its members — `mitosys+model+realm+shared`.

    A master board is named for what it owns, and until somebody names it the
    members are the only honest description of that. Long lists fold: past
    four names the join is a wall of text nobody reads, and the count carries
    the same information."""
    names = [n for n, _ in members(board)]
    if not names:
        return project_name(board)
    joined = "+".join(names)
    if len(joined) <= 40 and len(names) <= 4:
        return joined
    return f"{names[0]}+{len(names) - 1} more"


def board_name(board):
    """What the board calls itself: `name:` in prds/settings.md, else inferred
    — from the members on a master board, from the directory walk-up on a
    plain one. Inference is a placeholder: the first pass that meets an
    unnamed master board asks the user and writes `name:`."""
    raw = str(board_settings(board).get("name", "")).strip()
    return re.sub(r"[^A-Za-z0-9_. -]", "-", raw) or infer_name(board)

def scan_memos(board):
    """{slug: memo} — the board's own memos, plus every member board's when
    this is a master, slugged `@<member>/<slug>`. The file never moves: a
    decision belongs to the repo it governs, and the master only folds them
    into one index the way it folds the plan into one timeline."""
    ms = dict(memolib.scan(board))
    for name, path in members(board):
        for slug, m in memolib.scan(path).items():
            q = f"{MEMBER_SIGIL}{name}/{slug}"
            ms[q] = dict(m, slug=q)
    return ms

def board_settings(board):
    path = os.path.join(board, "settings.md")
    if os.path.isfile(path):
        fm, _, _ = parse_prd(path)
        return fm
    return {}

def serve_url(board):
    """Where the live view is, if the service is up. The file above always
    works; this one is the same render with the detail pane and the edits."""
    port = os.environ.get("PEARDE_PORT", "8443")
    return f"http://127.0.0.1:{port}/board/{board_name(board)}"
