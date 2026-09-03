#!/usr/bin/env python3
"""pearde schedule — what may run now, and in what order.

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
from boards import (die)  # noqa: E402,F401
from prdfile import (HOLDING_STATES, LIVE_STATES, body_has_open_box, claim_of, dur, num, standing)  # noqa: E402,F401
from registry import (board_settings, scan, spec_data)  # noqa: E402,F401
from needs import (resolve_need, resolve_needs, unscanned_need)  # noqa: E402,F401
from vision import (axis_depth)  # noqa: E402,F401



# ── plan ──────────────────────────────────────────────────────────────────────

def overlap(a, b):
    return any(x == y or x.startswith(y + "/") or y.startswith(x + "/")
               for x in a for y in b)


def dispatchable(prd, prds, board=None, holder=None):
    """None when `claim` would take this PRD now, else why not — one string,
    `<gate>: <why>`, the gate word first so `transitions.gate_claim` raises
    it as it stands and `brief` maps it to a skip word.

    The one place the gates are written. `compute_plan`'s ready band,
    `cmd_scan`'s `ready` and `gated` sections and `gate_claim` all call it,
    so the scan cannot list as ready what `claim` refuses — the memo
    `a-parked-child-holds-the-parent` is the day they disagreed. The gates:

    - unclaimed — it carries a `claim:` naming someone other than `holder`.
      `holder` is `None` for every caller but `brief` briefing a worker who
      names itself — the one case where a claim is not a refusal, because
      the worker holding it is the one asking.
    - leaf — a child is not `done`. A parked child is neither done nor
      coming, so it holds the parent for good: `held by <child> (parked)`.
    - container — children, every one `done`, and no specs or open box of
      its own. Finished work `collect` closes, never a thing to dispatch;
      `claim` on it is the trap `a-container-cannot-reach-done` records.
    - needs — a `needs:` entry naming nothing, or a PRD not `done`. The
      one exception is a cross-board need whose board is not in this
      scan: nothing here can say whether it is done, so it is ignored,
      the answer `resolve_needs` already gives the schedule.
    - workflow — `workflow:` names no workflow in any library it can see;
      `board` is the master's library when there is one.

    The state is not checked here: the callers partition by state first,
    and a `claimed` PRD is in flight, not refused."""
    rel = prd["rel"]
    held = claim_of(prd["fm"])
    if held and held["who"] != holder:
        return f"unclaimed: {rel} carries `claim: {prd['fm']['claim']}`"
    parked = [c for c in prd["children"]
              if prds[c]["state"] not in LIVE_STATES
              and prds[c]["state"] != "done"]
    if parked:
        return (f"leaf: {rel} held by "
                + ", ".join(f"{c} (parked)" for c in parked))
    live = [c for c in prd["children"] if prds[c]["state"] != "done"]
    if live:
        return (f"leaf: {rel} has children not done — "
                + ", ".join(os.path.basename(c) for c in live))
    sdir = os.path.join(prd["dir"], "specs")
    specs = (os.path.isdir(sdir)
             and any(f.endswith(".md") for f in os.listdir(sdir)))
    if prd["children"] and not specs and not body_has_open_box(prd):
        return "container: every child done — pearde collect closes it"
    deps = prd["fm"].get("needs", [])
    for d in (deps if isinstance(deps, list) else [deps]):
        t = resolve_need(prds, prd, d)
        if t is None:
            # A cross-board need whose board is not in this scan is ignored,
            # not held — the answer `resolve_needs` gives the schedule, so the
            # gate and the edges say one thing. Every other unresolvable need
            # names something this board should hold and does not: a hold.
            if unscanned_need(prds, d, board or prd.get("board_path")):
                continue
            return f"needs: `{d}` names no PRD on this board"
        if prds[t]["state"] != "done":
            return f"needs: {t} is `{prds[t]['state']}`, not done"
    # The footprint clash is no longer a gate. Every worker works in a lane
    # of its own (@resources/board/lanes.py), so two PRDs on one file are
    # two branches, not two writers in one tree: the plan's edge still
    # orders them — `footprint_clash` is what `compute_plan` reads — and
    # the collide is resolved at the merge, where a conflict is a red
    # collect naming the file. Refusing the claim here only serialized what
    # the plan already serialized, and stalled a board that had lanes.
    v = prd["fm"].get("workflow")
    if isinstance(v, list):
        return ("workflow: the key holds one slug — a list is a break, not "
                "an absence; fix the shape or remove the key")
    mark = workflow_marks(board or prd["board_path"], {rel: prd}).get(rel, "")
    if mark.endswith("?"):
        return (f"workflow: `{mark[:-1]}` names no workflow in "
                f"{prd['board_path']}/workflows — fix the slug or remove "
                "the key")
    return None

# The words that say "no cap" in settings.md or on the flag. The board
# assumes unlimited parallel agents; a number is a cap the user chose.
UNLIMITED = ("", "0", "off", "unlimited", "∞")


def parse_workers(value):
    """A `workers:` value as the cap — 0 is unlimited, and the default."""
    s = str(value if value is not None else "").strip().lower()
    if s in UNLIMITED:
        return 0
    try:
        return max(int(s), 0)
    except ValueError:
        return 0


def plan_workers(board, workers):
    if workers is not None:
        return parse_workers(workers)
    try:
        return max(int(board_settings(board).get("workers", 0)), 0)
    except (TypeError, ValueError):       # `off`, `unlimited`, `∞`
        return parse_workers(board_settings(board).get("workers"))


def workers_label(n):
    """What a cap prints as — `∞` when there is none."""
    return "∞" if not n else str(n)

def compute_plan(board, workers=None, warn=True):
    """The plan as data — None when there is nothing to schedule.

    Separate from the printing because a master board's plan is a function of
    every member's state: it has to be recomputable on a file change, not only
    when somebody remembers to run `plan`. `cmd_plan` prints what this
    returns. `reconcile` only saves it."""
    settings = board_settings(board)
    workers = plan_workers(board, workers)
    prds = scan(board)
    todo = {r: p for r, p in prds.items() if p["state"] in LIVE_STATES}
    parked = sorted(r for r, p in prds.items()
                    if p["state"] not in LIVE_STATES and p["state"] != "done")
    if not todo:
        return None
    needs = resolve_needs(prds, todo, warn, board)

    est, feet = {}, {}
    for r, p in todo.items():
        e, f = spec_data(p)
        # complexity is the weight. est is the fallback for an unscored PRD
        est[r] = (e or num(p["fm"], "complexity", r)
                  or dur(p["fm"], "est", r))
        feet[r] = f
    # A parent with live children is a container: the work is in the children,
    # and weighing it too counts the same work twice. It still waits for them.
    for r, p in todo.items():
        if any(c in todo for c in p["children"]):
            est[r] = 0.0
    known = [e for e in est.values() if e > 0]
    avg = (sum(known) / len(known) if known
           else num(settings, "weight-default", "settings.md", 50) or 50)
    for r, p in todo.items():
        if not est[r] and not any(c in todo for c in p["children"]):
            est[r] = avg

    # In flight, a PRD weighs only what is LEFT of it. An implementer closes an
    # acceptance box as it lands the check behind it, so the specs on disk say
    # how much of a held PRD is already standing — and a plan that keeps
    # weighing the whole of it stands still exactly while the board is moving
    # fastest. The floor is a twentieth: collecting the work is itself work,
    # and a bar of zero width is a PRD that vanished off the timeline.
    boxes, collect = {}, []
    for r, p in todo.items():
        frac, closed, total, ready_to_collect = standing(p)
        boxes[r] = (closed, total)
        if ready_to_collect:
            collect.append(r)
        if total and p["state"] in HOLDING_STATES:
            est[r] = max(est[r] * (1 - frac), est[r] * 0.05)
    # A container — children every one `done`, nothing of its own — is
    # finished work `collect` closes, never a thing to dispatch. It joins the
    # list here, once, so `scan`, `plan` and a bare `collect` read one list.
    for r, p in todo.items():
        if (p["state"] in ("open", "specced") and r not in collect
                and (dispatchable(p, prds, board) or "")
                .startswith("container:")):
            collect.append(r)

    def prio(r):
        return num(todo[r]["fm"], "priority", r)

    # The vision axis orders the frontier: asap lanes first, then on-axis
    # deepest-first, then the old widest-door order. A PRD off the axis (or a
    # board with no axis) keeps the old order. The axis is `prds/vision.md`,
    # read by `axis_depth`; the asap lane is a PRD declaring `axis: asap`
    # in its frontmatter — the "see it working" ask, scheduled by priority,
    # not hops.
    axis = axis_depth(board, prds)
    def asap(r):
        return str(todo[r]["fm"].get("axis", "")).strip() == "asap"
    def axis_rank(r, unblocks=None):
        u = (unblocks or {}).get(r, 0)
        if asap(r):
            return (0, 0, -u, -prio(r), r)
        d = axis.get(r)
        if d is not None:
            return (1, -d, -u, -prio(r), r)
        return (2, 0, -u, -prio(r), r)

    # A footprint clash serializes the PAIR, never a pass. An agent starts
    # the moment its own gates clear, so a barrier would hold back every PRD
    # it shares nothing with. The clash is an edge: the lower-priority PRD is
    # `after` the higher one, and only that pair is ordered. Two PRDs already
    # ordered by a dependency path need no edge — the path is the order.
    edges = {r: list(needs[r]) for r in todo}

    def path(a, b, _seen=None):
        """a reaches b along edges — a runs after b already."""
        if _seen is None:
            _seen = set()
        if a == b:
            return True
        _seen.add(a)
        return any(d not in _seen and path(d, b, _seen) for d in edges[a])

    after = {r: [] for r in todo}
    ranked = sorted(todo, key=lambda x: axis_rank(x))
    for i, r in enumerate(ranked):
        for s in ranked[i + 1:]:
            if (overlap(feet[r], feet[s])
                    and not path(s, r) and not path(r, s)):
                after[s].append(r)      # s yields: r outranks it
                edges[s].append(r)

    # topological order over needs + after; a cycle in `needs` is an error
    # (an `after` edge is only ever added between unordered PRDs, so it
    # cannot close one)
    depth, visiting = {}, set()
    def dp(r):
        if r in depth:
            return depth[r]
        if r in visiting:
            die(f"needs cycle through {r}")
        visiting.add(r)
        depth[r] = 1 + max((dp(d) for d in edges[r]), default=0)
        visiting.discard(r)
        return depth[r]
    for r in todo:
        dp(r)

    # what dispatching a PRD opens: the weight transitively waiting behind it.
    # The frontier orders by this — the door that opens widest goes first
    feeds = {r: [] for r in todo}
    for r, ds in edges.items():
        for d in ds:
            feeds[d].append(r)
    down = {}
    for r in sorted(todo, key=lambda x: -depth[x]):
        acc = set()
        for s in feeds[r]:
            acc.add(s)
            acc |= down[s]
        down[r] = acc
    unblocks = {r: sum(est[s] for s in down[r]) for r in todo}

    # The calendar is a simulation, not the plan: dispatch every PRD the
    # moment its edges are done and a worker is free, best door first. The
    # dispatch order it visits IS the plan's order. The offsets only feed the
    # Gantt dates — a staffing guess, never a fact about the plan.
    # No cap means every ready PRD starts the moment its edges clear: the
    # schedule is then the critical-path schedule itself.
    nslots = workers if workers > 0 else max(len(todo), 1)
    left = {r: len(edges[r]) for r in todo}
    ready = [r for r in todo if not left[r]]
    # The ready band is `dispatchable`, the one predicate `claim` reads. A
    # PRD with no edge left that the gate would still refuse — a parked
    # child, a stale claim, a dangling workflow — is held to the tail of the
    # schedule: visible, never offered. A container is collect's, not a
    # hold; it folds at zero like any weightless PRD.
    held = {}
    for r in list(ready):
        if todo[r]["state"] not in ("open", "specced"):
            continue
        why = dispatchable(todo[r], prds, board)
        if why and not why.startswith("container:"):
            held[r] = why
            if workers > 0:
                ready.remove(r)
    # With no cap the hold costs no slot: a held PRD keeps its place on the
    # critical path (the frontier still never offers it), so the wall is
    # the path's length. Under a cap the held go to the tail, as before.
    pending = list(held) if workers > 0 else []
    running, schedule, order, t0 = [], {}, [], 0.0
    def take(pool):
        best = min(pool, key=lambda x: axis_rank(x, unblocks))
        pool.remove(best)
        return best
    def finish(r):
        for s in feeds[r]:
            left[s] -= 1
            if not left[s]:
                ready.append(s)
    while ready or running or pending:
        # a container weighs nothing and holds no worker — it folds away the
        # moment its children are done
        while ready:
            zero = [r for r in ready if est[r] <= 0]
            if not zero:
                break
            for r in zero:
                ready.remove(r)
                schedule[r] = {"start": t0, "end": t0}
                order.append(r)
                finish(r)
        while ready and len(running) < nslots:
            r = take(ready)
            schedule[r] = {"start": t0, "end": t0 + est[r]}
            order.append(r)
            running.append((schedule[r]["end"], r))
        if not running and not ready and pending:
            # nothing left that can run: the held go at the tail, in order,
            # so what waits on them is scheduled after them, not never
            for r in pending:
                schedule[r] = {"start": t0, "end": t0 + est[r]}
                order.append(r)
                running.append((schedule[r]["end"], r))
            pending = []
        if not running:
            continue
        running.sort()
        t0, r = running.pop(0)
        finish(r)
    wall = max((s["end"] for s in schedule.values()), default=0.0)
    # the most PRDs running at once — what the schedule asks for at its widest
    marks = sorted([(s["start"], 1) for r, s in schedule.items() if est[r] > 0]
                   + [(s["end"], -1) for r, s in schedule.items() if est[r] > 0])
    peak = run = 0
    for _, d in marks:
        run += d
        peak = max(peak, run)
    return {"prds": prds, "todo": todo, "parked": parked, "settings": settings,
            "workers": workers, "needs": needs, "est": est, "feet": feet,
            "boxes": boxes, "collect": sorted(collect), "held": held,
            "after": after, "schedule": schedule, "order": order,
            "unblocks": unblocks, "wall": wall, "avg": avg, "peak": peak,
            "prio": {r: prio(r) for r in todo}}

def weight_of(prd, avg):
    """One PRD's weight, done or live — `complexity`, else the specs' sum,
    else `est`, else the board average. `compute_plan` weighs only live work;
    the progress line's percentage needs the closed PRDs too."""
    e, _ = spec_data(prd)
    return (num(prd["fm"], "complexity", prd["rel"]) or e
            or dur(prd["fm"], "est", prd["rel"]) or avg)


def progress_terms(board, prds=None, settings=None):
    """Every term of the progress line, computed once.

    @references/parts/progress.md defines them; deriving them by hand off a
    board scan is a page of arithmetic a pass pays for at every state change,
    and pays again after every compaction."""
    prds = scan(board) if prds is None else prds
    settings = board_settings(board) if settings is None else settings
    live = {r: p for r, p in prds.items() if p["state"] in LIVE_STATES}
    scored = [w for w in (num(p["fm"], "complexity", r)
                          for r, p in prds.items()) if w > 0]
    avg = (sum(scored) / len(scored) if scored
           else num(settings, "weight-default", "settings.md", 50) or 50)

    def origin(p):
        return "derived" if str(p["fm"].get("origin", "")).strip() == \
            "derived" else "requested"

    req = {r: p for r, p in prds.items()
           if origin(p) == "requested" and (p["state"] in LIVE_STATES
                                            or p["state"] == "done")}
    der = {r: p for r, p in prds.items()
           if origin(p) == "derived" and (p["state"] in LIVE_STATES
                                          or p["state"] == "done")}
    wt = {r: weight_of(p, avg) for r, p in req.items()}
    done_w = sum(w for r, w in wt.items() if req[r]["state"] == "done")
    all_w = sum(wt.values())
    counts = collections.Counter(p["state"] for p in prds.values())
    parked = [r for r, p in prds.items()
              if p["state"] not in LIVE_STATES and p["state"] != "done"]
    return {
        "prds": prds, "live": live, "avg": avg, "counts": counts,
        "parked": parked,
        "done": (sum(1 for p in req.values() if p["state"] == "done"),
                 len(req)),
        "pct": round(100 * done_w / all_w) if all_w else 0,
        "derived": (sum(1 for p in der.values() if p["state"] == "done"),
                    len(der)),
        "open": (counts.get("open", 0), len(prds)),
        "openpct": (round(100 * counts.get("open", 0) / len(prds))
                    if prds else 0),
    }


def workflow_marks(board, prds):
    """{rel: "<slug>" | "<slug>?"} for every PRD carrying a `workflow:`.

    The `?` is the break @references/workflow.md names, and it covers two
    cases that read as one on a line: the slug is in no library this PRD can
    see, or the file is there and is an **atomic** — a route was asked for and
    a single step was found. Both leave the worker without a route, so both
    mark; `workflows.py check` is where they are told apart, in words.

    A member PRD resolves against its own board's library first and the
    master's second, the order `needs:` resolves in. Each library is scanned
    once per call — this runs once per `scan`, not once per PRD.
    """
    marks, libs = {}, {}

    def lib(b):
        if b not in libs:
            libs[b] = wflib.scan(b)
        return libs[b]

    for rel, p in prds.items():
        v = p["fm"].get("workflow")
        if not v:
            continue
        if isinstance(v, list):
            # A shape error, not an absence. @references/workflow.md says the
            # key holds one slug and anything else is a break, so it marks
            # like one — the line shows it and the loop does not dispatch it.
            # `workflows.py check` is where it is named in words.
            marks[rel] = ",".join(str(x).strip() for x in v) + "?"
            continue
        slug = str(v).strip()
        if not slug:
            continue
        seen = [b for b in (p.get("board_path"), board) if b]
        ok = any(lib(b).get(slug, {}).get("kind") == "workflow" for b in seen)
        marks[rel] = slug if ok else slug + "?"
    return marks


def pressure_bands(board, prds, r):
    """(collect, yours, flight, ready, gated, why) — the pressure order's own
    bands, over the live PRDs `compute_plan` returned in `r["order"]`. One
    computation, read by `cmd_scan` for the sections it prints and by
    `cmd_next` for the one it acts on — @references/parts/order.md.

    Everything above `in flight` is something this pass can act on now;
    `in flight` is held by somebody else. A PRD in exactly one band, never
    two."""
    order = r["order"] if r else []
    collect = list(r["collect"]) if r else []
    needs = r["needs"] if r else {}
    after = r["after"] if r else {}
    rest = [x for x in order if x not in collect]
    # `blocked` is a wall a person has to take down, not a free PRD. It holds
    # its worker, so it is not in flight either — filing it under `ready` was
    # the scan calling a PRD dispatchable that nothing can dispatch.
    yours = [x for x in rest if prds[x]["state"] in ("question", "blocked",
                                                     "refine", "failed")]
    flight = [x for x in rest if prds[x]["state"] in ("analyzing", "claimed")
              and x not in yours]
    free = [x for x in rest if x not in flight and x not in yours]
    # `dispatchable` is the one predicate `claim` reads: a PRD it refuses is
    # never listed as ready. A container — children all done, nothing of its
    # own — is already in `collect`: `compute_plan` put it there, the one list
    # `scan`, `plan` and a bare `collect` read.
    why = {x: dispatchable(prds[x], prds, board) for x in free}
    for x in collect:   # a container's row says why it is here, in its own words
        w = (dispatchable(prds[x], prds, board)
             if prds[x]["state"] in ("open", "specced") else None)
        if (w or "").startswith("container:"):
            why[x] = w
    # `after` is the footprint-overlap edge and nothing else — `compute_plan`
    # builds it from `overlap(feet[r], feet[s])` alone, and `cmd_plan` labels
    # every one of them `(footprint)`. It orders the pair; it no longer holds
    # the second back. Every worker works in a git worktree of its own
    # (@resources/board/lanes.py), so two PRDs on one file are two branches
    # that the merge reconciles — and holding the second here would put back,
    # one command along, the single-tree serializer `claim`'s gate just gave
    # up. `needs` still gates: that is a real dependency and no branch fixes
    # it. The plan's own frontier keeps the edge, so `pearde plan` still says
    # which of the two goes first.
    ready = [x for x in free if not why[x] and not needs.get(x)]
    gated = [x for x in free if x not in ready]
    return collect, yours, flight, ready, gated, why

def plan_frontier(r):
    """`plan`'s ready set — every PRD nothing gates, in dispatch order. The
    same list `vision --next` prints alone."""
    return [x for x in r["order"]
            if not r["needs"][x] and not r["after"][x] and r["est"][x] > 0
            and x not in r["held"]]
