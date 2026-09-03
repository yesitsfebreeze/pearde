#!/usr/bin/env python3
"""pearde vision — the axis prds/vision.md declares, and the depth along it.

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
from prdfile import (LIVE_STATES, dur, num, parse_prd)  # noqa: E402,F401
from registry import (MEMBER_SIGIL, board_name, scan)  # noqa: E402,F401
from needs import (needs_index, resolve_need)  # noqa: E402,F401


# ── the vision axis ───────────────────────────────────────────────────────────
# `prds/vision.md` says where the board is going: `vision:` in one sentence,
# `terminals:` naming the PRDs whose completion is that destination, `edges:`
# for a dependency nobody wrote as `needs:`. @references/parts/order.md.
VISION_FILE = "vision.md"


def read_vision(board):
    """`prds/vision.md` as data — {vision, terminals, edges, title, body} —
    or None when the board has none. The one reader of the file."""
    path = os.path.join(board, VISION_FILE)
    if not os.path.isfile(path):
        return None
    fm, title, body = parse_prd(path)

    def items(key):
        v = fm.get(key, [])
        v = v if isinstance(v, list) else [v]
        return [str(x).strip() for x in v if str(x).strip()]

    edges = []
    for e in items("edges"):
        a, sep, b = e.partition("->")
        edges.append((a.strip(), b.strip()) if sep else (e, ""))
    return {"vision": str(fm.get("vision", "")).strip(),
            "terminals": items("terminals"), "edges": edges,
            "title": title, "body": body}


def resolve_addr(prds, tok, board, idx=None):
    """The rel a vision address names, or None. `needs:` resolution — own
    board first, `@<member>/<rel>` across boards — plus `@<this board's
    name>/<rel>` for the board's own PRD, which a master's file writes so its
    terminals read as one list."""
    t = str(tok).strip().rstrip("/")
    own = f"{MEMBER_SIGIL}{board_name(board)}/"
    if t.startswith(own) and t[len(own):] in prds:
        return t[len(own):]
    return resolve_need(prds, {"board": None}, t, idx)


def vision_axis(board, prds=None, vis=None):
    """The axis as data, or None when the board declares no terminals.

    `depth[rel]` is the longest serial chain from that PRD to a terminal over
    `needs:` plus `edges:` — a parent is a terminal for its subtree, a done
    PRD on the chain costs no hop — or None when no terminal is reachable:
    off the axis, neither near the vision nor far from it. `reach[rel]` is
    the undone work the PRD stands in front of. `dangling` lists every
    terminal or edge end that names no PRD — what `doctor`'s `vision` row
    reports."""
    v = read_vision(board) if vis is None else vis
    if not v or not v["terminals"]:
        return None
    prds = scan(board) if prds is None else prds
    idx = needs_index(prds)
    term, dangling = set(), []
    for t in v["terminals"]:
        r = resolve_addr(prds, t, board, idx)
        if r:
            term.add(r)
        else:
            dangling.append(f"terminal {t} names no PRD")
    after = {r: set() for r in prds}       # after[x]: the rels that wait on x
    for r, p in prds.items():
        deps = p["fm"].get("needs", [])
        for d in (deps if isinstance(deps, list) else [deps]):
            t = resolve_need(prds, p, d, idx)
            if t and t != r:
                after[t].add(r)
        for c in p["children"]:            # a parent lands after its children
            after[c].add(r)
    for a, b in v["edges"]:
        ra, rb = (resolve_addr(prds, x, board, idx) for x in (a, b))
        bad = [x for x, rx in ((a, ra), (b, rb)) if not rx]
        if bad:
            dangling.append(f"edge {a} -> {b}: {', '.join(bad)} names no PRD")
        elif ra != rb:
            after[ra].add(rb)
    depth, reach = {}, {}

    def walk(r):
        if r in depth:
            return depth[r]
        depth[r] = 0 if r in term else None   # a cycle reads this partial value
        best = depth[r]
        for nxt in after[r]:
            d = walk(nxt)
            if d is None:
                continue
            step = d if prds[nxt]["state"] == "done" else d + 1
            best = step if best is None else max(best, step)
        depth[r] = 0 if r in term else best
        return depth[r]

    def down(r):
        if r in reach:
            return reach[r]
        reach[r] = set()
        acc = set()
        for nxt in after[r]:
            if prds[nxt]["state"] != "done":
                acc.add(nxt)
            acc |= down(nxt)
        reach[r] = acc
        return acc

    for r in prds:
        walk(r)
        down(r)
    return {"vision": v["vision"], "body": v["body"],
            "terminals": v["terminals"], "term": term, "after": after,
            "depth": depth, "reach": {r: len(s) for r, s in reach.items()},
            "dangling": dangling}


def axis_depth(board, prds=None):
    """{rel: depth} from the vision axis — None for a PRD off it, {} on a
    board that declares no terminals, which orders as it always has."""
    ax = vision_axis(board, prds)
    return ax["depth"] if ax else {}

def vision_json(board, prds, ax):
    """What `.vision.json` held, as data: every live PRD with its depth and
    reach, deepest first, and the off-axis set by address."""
    name = board_name(board)
    idx = needs_index(prds)
    rows = []
    for r, p in prds.items():
        if p["state"] not in LIVE_STATES:
            continue
        deps = p["fm"].get("needs", [])
        unmet = []
        for d in (deps if isinstance(deps, list) else [deps]):
            t = resolve_need(prds, p, d, idx)
            if t is None or prds[t]["state"] != "done":
                unmet.append(str(d).strip())
        specs = os.path.join(p["dir"], "specs")
        prio = num(p["fm"], "priority", r)
        d = ax["depth"].get(r)
        rows.append({
            "addr": (r if r.startswith(MEMBER_SIGIL)
                     else f"{MEMBER_SIGIL}{name}/{r}"),
            "board": p["board"] or name, "rel": p["local"],
            "state": p["state"], "depth": d, "reach": ax["reach"].get(r, 0),
            "est": dur(p["fm"], "est", r) or None, "prio": prio,
            "ready": (not p["children"] and not unmet
                      and p["state"] in ("open", "specced", "failed")),
            "on_axis": d is not None, "blocked_by": unmet,
            "nspecs": len(os.listdir(specs)) if os.path.isdir(specs) else 0,
        })
    on = sorted((x for x in rows if x["on_axis"]),
                key=lambda x: (-x["depth"], -x["reach"], -x["prio"], x["addr"]))
    return {"vision": ax["vision"], "terminals": ax["terminals"],
            "longest_chain": max((x["depth"] for x in on), default=0),
            "prds": on,
            "off_axis": [x["addr"] for x in rows if not x["on_axis"]]}


def critical_chain(ax, prds, start):
    """The serial chain from `start` to a terminal: at each hop, the
    dependent that carries the depth — a done one costs no hop."""
    chain, cur = [start], start
    while cur not in ax["term"]:
        nxt = None
        for cand in sorted(ax["after"][cur]):
            d = ax["depth"].get(cand)
            hop = 0 if prds[cand]["state"] == "done" else 1
            if d is not None and d + hop == ax["depth"][cur]:
                nxt = cand
                break
        if nxt is None or nxt in chain:
            break
        chain.append(nxt)
        cur = nxt
    return chain
