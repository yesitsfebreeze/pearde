#!/usr/bin/env python3
"""pearde needs — what a PRD waits on before it may run.

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
from registry import (MEMBER_SIGIL, board_name)  # noqa: E402,F401


def needs_index(prds):
    """(by dir name, by (board, name-or-rel)) — what a `needs:` entry is
    looked up in."""
    by_name, local = {}, {}
    for r in sorted(prds):
        by_name.setdefault(os.path.basename(r), []).append(r)
        local.setdefault((prds[r]["board"], os.path.basename(r)), r)
        local.setdefault((prds[r]["board"], prds[r]["local"]), r)
    return by_name, local


def resolve_need(prds, prd, d, idx=None):
    """The rel one `needs:` entry names, or None.

    Own board first, so a member's `needs: sibling` keeps meaning its own
    sibling and joining a master rewrites no member PRD. Across boards the
    form is qualified — `@<member>/<prd>`. A bare name matching PRDs on two
    boards resolves to nothing on purpose: guessing which was meant is how a
    worker gets sent at code another repo has not written."""
    by_name, local = idx or needs_index(prds)
    d = str(d).strip().rstrip("/")
    if d in prds:
        return d
    if (prd.get("board"), d) in local:
        return local[(prd.get("board"), d)]
    if d.startswith("@"):
        # `@<board>/<prd>` names another board on purpose. Scanned without
        # that board — a member on its own — the honest answer is "not here",
        # never the basename. A cross-tree node writes the same child name on
        # every member, so the fallback would resolve a qualified need to the
        # very PRD doing the needing, and the cycle check would kill the scan.
        return None
    same = by_name.get(os.path.basename(d), [])
    return same[0] if len(same) == 1 else None


def need_board(d):
    """The board a qualified `needs:` entry names — `@<board>/<prd>` → `<board>`
    — or None when the entry names no board at all."""
    d = str(d).strip().rstrip("/")
    if not d.startswith(MEMBER_SIGIL) or "/" not in d:
        return None
    return d[len(MEMBER_SIGIL):].split("/", 1)[0] or None


def scanned_boards(prds, board=None):
    """Every board name this scan can answer for: the members it merged, plus
    the board's own `name:` when the caller knows the path — a master's own
    PRDs carry `board: None`, so without it a need under the master's own name
    would read as a board that is not here."""
    names = {p.get("board") for p in prds.values() if p.get("board")}
    if board:
        names.add(board_name(board))
    return names


def unscanned_need(prds, d, board=None):
    """True when `d` is a cross-board need whose board is not in this scan.

    A member worked on its own board carries `needs: @<other>/<prd>` for a
    board this session never read. Nothing here can say whether it is done, and
    a gate that holds on what it cannot see holds for good — so it is ignored
    and reported, the answer `resolve_needs` already gave the schedule. A
    qualified need naming a board that IS in the scan is a different thing: the
    board is here and the PRD is not, which is a typo, and a typo still holds."""
    b = need_board(d)
    return bool(b) and b not in scanned_boards(prds, board)


def resolve_needs(prds, todo, warn=True, board=None):
    """rel → the rels it waits on. A parent implicitly needs its undone
    children — work flows to the leaves — and a need on a `done` PRD is
    satisfied."""
    idx = needs_index(prds)
    needs = {}
    for r, p in todo.items():
        deps = p["fm"].get("needs", [])
        deps = deps if isinstance(deps, list) else [deps]
        needs[r] = [c for c in p["children"] if c in todo]
        for d in deps:
            t = resolve_need(prds, p, d, idx)
            if t is None:
                ds = str(d).strip()
                if warn and unscanned_need(prds, ds, board):
                    print(f"plan: {r} needs '{d}' — that board is not in this "
                          f"scan, ignored", file=sys.stderr)
                    continue
                if ds.startswith(MEMBER_SIGIL):
                    if warn:
                        print(f"plan: {r} needs '{d}' — that board is in this "
                              f"scan and holds no such PRD", file=sys.stderr)
                    continue
                same = idx[0].get(os.path.basename(ds), [])
                if warn and len(same) > 1:
                    print(f"plan: {r} needs '{d}' — {len(same)} PRDs of that "
                          f"name ({', '.join(same)}); qualify it as "
                          f"@<board>/<prd>", file=sys.stderr)
                elif warn:
                    print(f"plan: {r} needs '{d}' — no such PRD, ignored",
                          file=sys.stderr)
            elif t in todo and t not in needs[r]:
                needs[r].append(t)
    return needs
