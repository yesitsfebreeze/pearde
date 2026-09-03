#!/usr/bin/env python3
"""pearde mapfile — the plan on disk, the journals, and the payload the view reads.

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
import health as healthlib  # noqa: E402 — the ranking, read fresh per payload
import memos as memolib  # noqa: E402 — on the path by the rule
import questions as qlib  # noqa: E402 — the drill count, one reader with list
import render as renderlib  # noqa: E402 — on the path by the rule
import workflows as wflib  # noqa: E402 — on the path by the rule
from boards import (STATE_DIR, guard_dir, state_dir)  # noqa: E402,F401
from prdfile import (HOLDING_STATES, LIVE_STATES, claim_of, dur, num, standing)  # noqa: E402,F401
from repos import (lanes)  # noqa: E402,F401
from registry import (_scan_one, board_name, members, scan)  # noqa: E402,F401
from silence import (silent_of)  # noqa: E402,F401
from needs import (resolve_need)  # noqa: E402,F401
from vision import (read_vision)  # noqa: E402,F401
from schedule import (compute_plan, parse_workers, workers_label)  # noqa: E402,F401


def landing(board, everything):
    """(rows, repos) — the lanes this machine is holding, in the order they
    should land.

    A row is one unmerged lane matched to the PRD it was cut for, by the slug
    both share. `ready` marks the ones the board says are finished — state
    `done`, or `collect` — and those are the ones to merge. It reads
    `collect` rather than the boxes so that "merge this" and "collect this"
    are one rule: a lane marked ready on a PRD whose `prd.md` still carries an
    open box is a merge into a gate that would refuse it. The rest are in
    flight and drawn as such: a lane at 50/54 boxes is worth seeing next to
    the queue it is about to join.

    Ready first, then by priority, then by name for stability — merging is
    collect's work, and collect goes best door first, not oldest first."""
    roots = members(board) or [(None, board)]
    rows, repos = [], []
    for name, path in roots:
        got = lanes(path)
        if got["root"] is None:
            continue
        repos.append({"board": name or board_name(board),
                      "ahead": got["ahead"], "lanes": len(got["lanes"])})
        if not got["lanes"]:
            continue
        by_slug = {}
        for t in everything:
            if (t.get("board") or None) == name:
                by_slug.setdefault(os.path.basename(t["rel"]), t)
        for slug, ln in sorted(got["lanes"].items()):
            t = by_slug.get(slug)
            boxes = (t or {}).get("boxes") or [0, 0]
            state = (t or {}).get("state") or "?"
            rows.append({
                "slug": slug, "branch": ln["branch"],
                "board": name, "rel": (t or {}).get("rel") or slug,
                "name": (t or {}).get("name") or slug,
                "title": (t or {}).get("title") or "",
                "state": state, "boxes": boxes,
                "prio": (t or {}).get("prio") or 0,
                "est": (t or {}).get("est") or 0,
                # the board's own claim that the work is finished and
                # tested: `done`, or `collect` — every acceptance box closed
                # on a held PRD AND no open box left in its own `prd.md`
                "ready": state == "done" or bool((t or {}).get("collect")),
                # a lane whose slug matches no PRD at all — the PRD was renamed
                # or never existed. Shown, because an unmerged branch nobody
                # can name is exactly the thing that gets lost
                "orphan": t is None,
            })
    rows.sort(key=lambda r: (not r["ready"], -r["prio"], r["slug"]))
    repos.sort(key=lambda r: str(r["board"]))
    return rows, repos


# ── map file ──────────────────────────────────────────────────────────────────

def load_map(board):
    path = os.path.join(state_dir(board), "plan.json")
    if os.path.isfile(path):
        return json.load(open(path, encoding="utf-8")), path
    return {"after": {}, "schedule": {}}, path


def save_map(mp, path):
    json.dump(mp, open(path, "w", encoding="utf-8"), indent=1, sort_keys=True)


def gantt_payload(board, prds, mp, settings):
    """What the local timeline renders: one bar per scheduled leaf, day offsets
    from the plan's hour offsets at `gantt-day` hours per day. Parents weigh
    nothing in the plan, so a zero-length schedule entry is a container and
    folds away.

    Done and parked PRDs carry a bar too — `past: true` and `parked: true`.
    The plan is only the half in front of us. The track runs from the first
    thing that landed to the vision — a timeline that starts at now shows a
    board that looks perpetually at its own beginning. The renderer lays
    the past out to the LEFT of now and pins the parked at now, so where we
    are is a place on the whole track, not kilometre zero of a shrinking
    one."""
    day_h = dur(settings, "gantt-day", "settings.md", "8h") or 8.0
    sched = mp.get("schedule", {})
    tasks, unplanned = [], []
    done = parked = containers = 0
    for rel in sorted(prds):
        p = prds[rel]
        st = p["state"]
        weight = round(num(p["fm"], "complexity", rel)
                       or dur(p["fm"], "est", rel), 2)
        pr = num(p["fm"], "priority", rel)
        nd = p["fm"].get("needs", [])
        nd = nd if isinstance(nd, list) else [nd]
        base = {
            "rel": rel, "name": p["name"], "title": p["title"],
            "board": p.get("board"), "state": st,
            "prio": int(pr) if pr == int(pr) else pr,
            "est": weight, "boxes": [0, 0], "part": 0,
            "held": False, "collect": False, "claim": None,
            "needs": [resolve_need(prds, p, str(n)) or str(n) for n in nd],
        }
        if st == "done":
            done += 1
            if weight > 0:
                tasks.append(dict(base, past=True))
            continue
        if st not in LIVE_STATES:
            parked += 1
            if weight > 0:
                tasks.append(dict(base, parked=True))
            continue
        s = sched.get(rel)
        if not s:
            unplanned.append(rel)
            continue
        if s["end"] <= s["start"]:
            containers += 1
            continue
        # what the run itself has closed so far, and who is holding it. Read
        # per PRD rather than once at plan time: this is the half of the
        # payload that moves between two transitions, and a view that only
        # learns it when `plan` runs is not live.
        frac, closed, total, ready_to_collect = standing(p)
        tasks.append(dict(base,
            est=round(s["end"] - s["start"], 2),
            startDay=round(s["start"] / day_h, 4),
            endDay=round(s["end"] / day_h, 4),
            # a footprint clash, named pairwise — real, and what `dispatch`
            # will serialise on the in-flight set, but it moves no bar here:
            # `startDay`/`endDay` above come from the `needs:`-only schedule,
            # so a clashing pair may draw side by side. An edge that reports,
            # never one that orders.
            after=mp.get("after", {}).get(rel, []),
            boxes=[closed, total],
            part=round(frac, 4),
            held=st in HOLDING_STATES or st == "analyzing",
            collect=ready_to_collect,
            claim=claim_of(p["fm"]),
            # the quiet worker, off the files — @references/parts/view.md.
            # None below `claim-ttl`; minutes of silence past it
            silent=silent_of(p, settings, collect=ready_to_collect),
        ))
    # Every PRD, not only the scheduled ones: the timeline draws what is left,
    # the analytics have to see what is done, parked and estimated too, and a
    # second scan of the same tree to get them would be the more expensive way
    # to say the same thing. `est` here is the PRD's own — spec_data reads every
    # spec file on the board, which is a plan-time cost, not a render one.
    everything = []
    for rel in sorted(prds):
        p = prds[rel]
        prio = num(p["fm"], "priority", rel)
        # boxes for live PRDs only: a `done` PRD's specs are history, and
        # reading every one of them is the plan-time cost this loop avoids.
        # `collect` comes from `standing`, the same reader `tasks[]` above
        # uses — this row and that one describe the same PRD in the same
        # payload, and a second spelling of the rule here is how they came to
        # disagree about a PRD whose specs are closed and whose `prd.md` is
        # not (`prds/memos/done-counts-which-boxes.md`).
        closed, total, collect = 0, 0, False
        if p["state"] in LIVE_STATES:
            _, closed, total, collect = standing(p)
        everything.append({
            "rel": rel, "name": p["name"], "title": p["title"],
            "state": p["state"], "board": p.get("board"),
            "parent": p.get("parent"),
            "prio": int(prio) if prio == int(prio) else prio,
            "est": round(dur(p["fm"], "est", rel), 2),
            "actual": round(dur(p["fm"], "actual", rel), 2),
            # the weight the board schedules by — complexity, falling back
            # to est. est and actual are records the plan never schedules
            # by; `calibrate` fits real hours from them
            "weight": round(num(p["fm"], "complexity", rel)
                            or dur(p["fm"], "est", rel), 2),
            "boxes": [closed, total],
            "collect": collect,
            "kids": len(p.get("children") or []),
            # prd.md's own mtime — cheap (one stat, no git call), unlike the
            # archive's done_at which needs `git log --follow` per PRD and is
            # deliberately kept out of this per-second-rebuilt payload. Used
            # by the board view to sort the done column by how recently each
            # PRD last changed.
            "mtime": os.path.getmtime(os.path.join(p["dir"], "prd.md")),
        })
    land, repos = landing(board, everything)
    return {
        "board": board_name(board),
        # a master's members, in plan order — the renderer groups by them
        "boards": [n for n, _ in members(board)],
        "all": everything,
        "history": read_history(board),
        # the cost series — @references/parts/guard.md. `guard` is None when
        # no session file exists, and the page says `no guard`
        "transitions": read_transitions(board),
        "guard": guard_view(board),
        # the states the loop works, then any the user parked work in
        "states": sorted(LIVE_STATES | {"done"}) + sorted(
            {p["state"] for p in prds.values()} - LIVE_STATES - {"done"}),
        "anchor": mp.get("planned_at") or datetime.date.today().isoformat(),
        "dayHours": day_h,
        # this board's fit from `calibrate` — weight to real hours at the
        # display edge only; the schedule above never read it. `tune` is the
        # hand-set margin the view multiplies on top of the fit
        "calib": read_calibration(board),
        "tune": TUNE,
        "workers": workers_label(parse_workers(settings.get("workers", "0"))),
        # the one sentence `prds/vision.md` says the board is for — the page
        # prints it under the numbers. Empty when the board declares none
        "vision": {"purpose": (read_vision(board) or {}).get("vision", "")},
        "counts": {"done": done, "parked": parked, "containers": containers,
                   "collect": sum(1 for t in tasks if t["collect"]),
                   "held": sum(1 for t in tasks if t["held"])},
        "unplanned": unplanned,
        "tasks": tasks,
        # what this machine is holding that main has never seen
        "landing": land, "repos": repos,
        # the ranking, worst first — read fresh off `health/ranking.md` on
        # every payload, the same file `pearde health list` reads. None on a
        # board with no health record; the section says `not scored`
        "health": healthlib.view_payload(board),
    }


HISTORY_FILE = os.path.join(STATE_DIR, "history.jsonl")


def read_history(board):
    """One line per day, appended by the live service: what the board looked
    like that day. It is the only thing here with a memory — every other number
    is what is true now — so the burn-down is the one chart that cannot be
    derived from a scan."""
    rows = []
    try:
        for line in open(os.path.join(board, HISTORY_FILE), encoding="utf-8"):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        return []
    return rows[-400:]


TRANSITIONS_FILE = os.path.join(STATE_DIR, "transitions.jsonl")


def read_transitions(board, last=30):
    """The last `last` rows transitions.py `record` appended — one per state
    move, carrying the guard's count for the window before it (`calls`,
    `reads`, `refused`, `tokens`, each `null` when no guard was counting).
    The analytics draw calls per transition off these; `.history.jsonl`
    stays the burn-down's."""
    rows = []
    try:
        for line in open(os.path.join(board, TRANSITIONS_FILE),
                         encoding="utf-8"):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        return []
    return rows[-last:]


# The guard's session files — resources/guard.py writes them, one per session
# under `<board>/.state/guard`, and `PEARDE_GUARD_STATE` moves the directory
# for both. `guard_dir(board)` is defined beside `state_dir()` above. plan.py
# only reads: the newest file is the live session, because the guard touches
# its file on every tool call, and the call that runs `pearde status` is
# the last one it saw. Per board, so the newest file is the newest session
# *on this board* — a session working another board is not this one.


def guard_sessions(board):
    """[(session, mtime, data)] oldest first, or [] with no state dir or no
    file in it — `no guard`, never zero."""
    out = []
    gd = guard_dir(board)
    try:
        names = [n for n in os.listdir(gd) if n.endswith(".json")]
    except OSError:
        return out
    for n in names:
        path = os.path.join(gd, n)
        try:
            out.append((n[:-5], os.stat(path).st_mtime,
                        json.load(open(path, encoding="utf-8"))))
        except (OSError, ValueError):
            continue
    out.sort(key=lambda x: x[1])
    return out


def guard_block(board, data):
    """The per-board counter block a session file holds for `board`, or
    None."""
    return (data.get("boards") or {}).get(os.path.realpath(board))


def guard_view(board):
    """What the analytics draw: every session that counted on this board,
    oldest first, or None when the guard has left no file at all."""
    sessions = guard_sessions(board)
    if not sessions:
        return None
    rows = []
    for sid, mtime, data in sessions:
        b = guard_block(board, data)
        if b is None:
            continue
        rows.append({"session": sid, "at": round(mtime, 3),
                     "refused": int(b.get("refused", 0)),
                     "calls": int(b.get("calls", 0)),
                     "transitions": int(b.get("transitions", 0))})
    return {"sessions": rows[-30:]}


def session_line(board):
    """`pearde status`'s one line on the cost of this session — the newest
    guard file's block for this board. `no guard` when there is no file;
    a session that has not counted here yet says so."""
    sessions = guard_sessions(board)
    if not sessions:
        return "this session: no guard"
    b = guard_block(board, sessions[-1][2])
    if b is None:
        return "this session: no calls counted on this board"
    calls = int(b.get("calls", 0))
    n = int(b.get("transitions", 0))
    per = f"{calls / n:.1f}" if n else "—"
    return (f"this session: {calls} calls · {int(b.get('refused', 0))} refused"
            f" · {n} transitions · {per} per transition")


def write_history(board, prds=None):
    """Today's row, once. Rewrites today's line rather than appending a second,
    so a daemon restarted six times in a day still leaves one point."""
    prds = scan(board) if prds is None else prds
    today = datetime.date.today().isoformat()
    row = {"d": today, "states": {}, "hleft": 0.0, "hdone": 0.0,
           "done": 0, "left": 0}
    for rel, p in prds.items():
        st = p["state"]
        row["states"][st] = row["states"].get(st, 0) + 1
        h = (num(p["fm"], "complexity", rel)
             or dur(p["fm"], "est", rel))
        if st == "done":
            row["done"] += 1
            row["hdone"] += h
        elif st in LIVE_STATES:
            row["left"] += 1
            row["hleft"] += h
    row["hleft"], row["hdone"] = round(row["hleft"], 2), round(row["hdone"], 2)
    state_dir(board)   # the burn-down is the first thing a fresh board writes
    path = os.path.join(board, HISTORY_FILE)
    rows = [r for r in read_history(board) if r.get("d") != today] + [row]
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    os.replace(tmp, path)
    return row

# ── calibration ───────────────────────────────────────────────────────────────
# How many real hours a unit of weight costs THIS agent on THIS board, fitted
# from every done PRD of the board that recorded an `actual:`. The plan still
# schedules in weight — the constant only translates at the display edge, so
# a bad fit can mislabel an axis but never re-order the work.
#
# Per board, not per machine: the fit used to pool every board the daemon had
# ever registered, which needed a machine-wide list of boards to read. There
# is no such list any more — one root, the board's `.pearde/` — and a board's
# own done PRDs are the more honest sample anyway. A board with no `actual:`
# on record shows raw weight, which is what it did before any board was
# calibrated.


def calib_path(board):
    return os.path.join(state_dir(board), "calibration.json")

# The one hand-tunable knob. Hours shown = weight × fitted kw × TUNE.
# The fit says how fast this machine has been; TUNE is the margin on top —
# raise it when the board keeps finishing later than it promised, lower it
# when it keeps beating the number.
TUNE = 1.618


def fmt_w(w, calib):
    """Weight, printed as tuned real hours when a fit exists, else as raw
    weight. Display only — nothing schedules by this."""
    if calib and calib.get("kw"):
        return f"{w * calib['kw'] * TUNE:.1f}h"
    return f"{w:.1f}w"


def read_calibration(board):
    """The fitted constants, or None before `calibrate` has run here."""
    try:
        c = json.load(open(calib_path(board), encoding="utf-8"))
        return c if c.get("n") else None
    except (OSError, ValueError):
        return None


def calib_rows(board):
    """(board, rel, est_h, actual_h, weight) for every done PRD of `board`
    carrying an `actual:`, its members included. est and actual are records
    the plan never schedules by — which is exactly what makes them honest
    calibration data: nobody gamed a number nothing was reading."""
    rows = []
    seen = set()
    for b in [board] + [p for _, p in members(board)]:
        b = os.path.abspath(b)
        if b in seen or not os.path.isdir(b):
            continue
        seen.add(b)
        name = os.path.basename(os.path.dirname(b)) or b
        for rel, p in sorted(_scan_one(b).items()):
            if p["state"] != "done":
                continue
            act = dur(p["fm"], "actual", rel)
            if act <= 0:
                continue
            w = num(p["fm"], "complexity", rel)
            rows.append((name, rel, dur(p["fm"], "est", rel), act, w))
    return rows

def reconcile(board):
    """Recompute the schedule in place, keeping the anchor day. True when it
    moved.

    A master board's plan spans repos nobody re-plans by hand — a state
    written in one member re-orders the whole board. Re-anchoring is `plan`'s
    work. This only re-orders, so the bars keep the day the plan was made."""
    r = compute_plan(board, None, warn=False)
    if not r:
        return False
    mp, mp_path = load_map(board)
    if (mp.get("after") == r["after"] and mp.get("schedule") == r["schedule"]
            and mp.get("planned_at")):
        return False
    mp["after"], mp["schedule"] = r["after"], r["schedule"]
    mp.setdefault("planned_at", datetime.date.today().isoformat())
    save_map(mp, mp_path)
    if os.path.isfile(os.path.join(board, renderlib.VIEW_FILE)):
        renderlib.write(board, gantt_payload(board, r["prds"], mp, r["settings"]))
    return True
