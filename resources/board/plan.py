#!/usr/bin/env python3
"""pearde plan — the board, read and ordered.

    plan.py plan  [board] [--workers N]   the frontier and the dispatch order
    plan.py reconcile [board]             re-order the schedule, keep the anchor
    plan.py gantt [board] [--open]        render the view to prds/.view.html
    plan.py calibrate [board]             fit hours-per-weight from every done
                                          PRD with an `actual:` on every
                                          registered board; the view prints
                                          real hours beside weight from it
    plan.py members [board]               what a master board merges
    plan.py status [board]                the board, its members, its memos
    plan.py example <dir>                 copy the example board to <dir> —
                                          an empty or new directory; never
                                          run in place
    plan.py vision [board] [--json|--next|--check]
                                          the axis prds/vision.md declares:
                                          depth per PRD, the critical chain,
                                          the off-axis set

board = the prds/ directory, a directory holding one, or omitted to walk up
from the cwd. The plan persists in prds/.plan.json. The view reads it.

Python 3 stdlib only.
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
from boards import (EXAMPLE_FLAGS, Flags, NotABoard, PASS_FILE, cmd_example, die, find_board)  # noqa: E402,F401
from prdfile import (LIVE_STATES, _h2_sections, claim_of, drill_questions, question_counts)  # noqa: E402,F401
from registry import (_scan_one, board_settings, is_master, members, scan, scan_memos, serve_url)  # noqa: E402,F401
from silence import (fmt_age, silent_of)  # noqa: E402,F401
from vision import (VISION_FILE, critical_chain, read_vision, vision_axis, vision_json)  # noqa: E402,F401
from schedule import (compute_plan, plan_frontier, pressure_bands, progress_terms, workers_label, workflow_marks)  # noqa: E402,F401
from mapfile import (TUNE, calib_path, calib_rows, fmt_w, gantt_payload, load_map, read_calibration, reconcile, save_map, session_line)  # noqa: E402,F401
import prdfile  # noqa: E402,F401 — _PCACHE and friends are rebound at run

# The module every caller imports. Each name below stands where it
# always stood; only the file holding it changed.
from boards import (BOARD_DIR, BOARD_DIRS, EXAMPLE, LEGACY_BOARD_DIR, LEGACY_MACHINE_DIR, PRDS_DIR, SCAN_SKIP, SETTINGS, STATE_DIR, board_above, board_at, board_in, board_link, board_named, board_scanned, guard_dir, is_board_dir, migrate_legacy_state, named_boards, prds_dir, state_dir, two_boards, walk_up)  # noqa: E402,F401
from prdfile import (ANSWER_LINE_RE, BOX_RE, CACHE_VERSION, CLAIM_TS_RE, HOLDING_STATES, ITEM_RE, KEY_RE, QUESTION_HEAD_RE, ZERO_RE, _BAD_SEEN, _parse_prd_uncached, _qid, acceptance, acceptance_of, answers_of, bad_value, body_has_open_box, dur, hours, num, opens_an_unticked_box, parse_cache_load, parse_cache_path, parse_cache_save, parse_prd, standing, strip_comment, strip_list_marker)  # noqa: E402,F401
from repos import (LANE_RE, LANE_TTL, _LANES, git, lanes, ref_stamp, repo_root, scan_lanes)  # noqa: E402,F401
from registry import (MEMBER_NAME_RE, MEMBER_SIGIL, board_name, infer_name, project_name, qualify_paths, spec_data)  # noqa: E402,F401
from silence import (CLAIM_TTL, SILENT_STATES, claim_ttl, newest_mtime, prd_repo, session_tree)  # noqa: E402,F401
from needs import (need_board, needs_index, resolve_need, resolve_needs, scanned_boards, unscanned_need)  # noqa: E402,F401
from vision import (axis_depth, resolve_addr)  # noqa: E402,F401
from schedule import (UNLIMITED, dispatchable, overlap, parse_workers, plan_workers, weight_of)  # noqa: E402,F401
from mapfile import (HISTORY_FILE, TRANSITIONS_FILE, guard_block, guard_sessions, guard_view, landing, read_history, read_transitions, write_history)  # noqa: E402,F401


def cmd_calibrate(board):
    rows = calib_rows(board)
    if not rows:
        print("calibrate: no done PRD on this board carries an `actual:`"
              " — nothing to fit.\n"
              "Record `actual:` on the DONE transition and run this again.")
        return
    for name, rel, e, a, w in rows:
        print(f"  {name:12} {rel:32} "
              + (f"est {e:6.2f}h" if e else "est      —")
              + f" · actual {a:6.2f}h"
              + (f" · w {w:.0f}" if w else ""))
    ew = [(e, a) for _, _, e, a, _ in rows if e > 0]
    ww = [(w, a) for _, _, _, a, w in rows if w > 0]
    # ratio of sums, not mean of ratios: a five-minute PRD must not outvote
    # a three-day one. The quantiles of the per-PRD ratio are the band.
    ke = round(sum(a for _, a in ew) / sum(e for e, _ in ew), 4) if ew else 0
    kw = round(sum(a for w, a in ww) / sum(w for w, _ in ww), 4) if ww else 0
    q = sorted(a / w for w, a in ww)
    pick = lambda p: round(q[min(len(q) - 1, int(p * len(q)))], 4) if q else 0
    calib = {"kw": kw, "ke": ke, "n": len(rows), "nw": len(ww),
             "p20": pick(.2), "p80": pick(.8),
             "boards": sorted({r[0] for r in rows}),
             "fitted": datetime.date.today().isoformat()}
    path = calib_path(board)
    json.dump(calib, open(path, "w", encoding="utf-8"), indent=1)
    print(f"\nn={len(rows)} done PRDs across {len(calib['boards'])} board(s)")
    if ke:
        print(f"k est→actual    = {ke}  (agent is {round(1 / ke, 1)}× faster"
              " than its estimates)")
    if kw:
        print(f"k weight→hours  = {kw} h/w · band P20 {calib['p20']}"
              f" – P80 {calib['p80']}")
        print(f"hours shown     = weight × {kw} × {TUNE}"
              " (TUNE — the hand-set margin, hard-coded in mapfile.py)")
    print(f"saved: {path}")
    # re-render so the open page shows the new constant without waiting for
    # the next board edit
    cmd_gantt(board)


def cmd_gantt(board, open_after=False):
    mp, _ = load_map(board)
    if not mp.get("schedule") or not mp.get("planned_at"):
        print("gantt: no plan on record — planning first\n")
        cmd_plan(board, None)
        mp, _ = load_map(board)
    path = renderlib.write(
        board, gantt_payload(board, scan(board), mp, board_settings(board)))
    print(f"gantt: {path}")
    if open_after:
        import webbrowser
        webbrowser.open("file://" + os.path.abspath(path))

def cmd_scan(board):
    """The whole board as one page a pass can hold — step 1, in one call.

    Everything the loop reads at the top of a pass: the counts, the progress
    terms, what is finished and waiting to be closed, what is dispatchable
    now, what gates the rest, who holds what, and how many questions are
    standing. It replaces a tree walk plus a `prd.md` read per PRD plus a spec
    read per box count, which is the same information at a hundred times the
    tokens — and re-derives none of it after a compaction."""
    t = progress_terms(board)
    prds, avg = t["prds"], t["avg"]
    r = compute_plan(board, None, warn=False)
    order = r["order"] if r else []
    boxes = r["boxes"] if r else {}
    needs = r["needs"] if r else {}
    after = r["after"] if r else {}
    est = r["est"] if r else {}
    bands = pressure_bands(board, prds, r)
    wf = workflow_marks(board, prds)
    settings = board_settings(board)     # `claim-ttl`, for the silent word
    mem = [n for n, _ in members(board)]
    # The axis, when the board declares one: how much live work is on the way
    # to the vision and how much is not. A board with no terminals prints
    # neither this nor the marks below — its scan reads as it always has.
    vis = read_vision(board)
    ax = vision_axis(board, prds, vis) if vis else None
    axis_note = ""
    if ax:
        on = sum(1 for x in t["live"] if ax["depth"].get(x) is not None)
        axis_note = f" · axis: {on} on · {len(t['live']) - on} off"
    # the drill count — the second entry point of @references/drill.md § The
    # board's own frontier: over one unanswered question, the drill section
    # below stands first and nothing is dispatched until the pass is out.
    drill = drill_questions(board)
    asking = ""
    if drill:
        askers = len({rel for rel, _q, _t, _o in drill})
        asking = (f" · asking {len(drill)} over {askers} PRD"
                  + ("s" if askers != 1 else ""))
    print(f"board: {board} · {len(prds)} PRDs"
          + (f" · master of {len(mem)}: " + ", ".join(mem) if mem else "")
          + (f" · workers={workers_label(r['workers'])}" if r else "")
          + asking
          + axis_note)
    if vis and vis["vision"]:
        print(f"vision: {vis['vision']}")
    if t["counts"]:
        print("counts: " + " · ".join(f"{s} {n}" for s, n in sorted(
            t["counts"].items(), key=lambda kv: -kv[1])))
    rd, rn = t["done"]
    dd, dn = t["derived"]
    o, n = t["open"]
    print(f"progress: done {rd}/{rn} · {t['pct']}%"
          + (f" · derived {dd}/{dn}" if dn else "")
          + f" · open {o}/{n} · {t['openpct']}%")
    if t["parked"]:
        print("parked: " + ", ".join(sorted(t["parked"])))

    why = {}                              # rel → `dispatchable` reason, below

    def line(x):
        p = prds[x]
        c, tt = boxes.get(x, (0, 0))
        cl = claim_of(p["fm"])
        q, a = question_counts(p)
        bits = [f"{p['state']:9}", x, f"p{p['fm'].get('priority', 0)}",
                f"w{est.get(x, 0):.0f}"]
        if wf.get(x):
            bits.append("wf " + wf[x])
        if ax and ax["depth"].get(x) is None:
            bits.append("off-axis")
        if tt:
            bits.append(f"boxes {c}/{tt}")
        if needs.get(x):
            bits.append("needs " + ",".join(os.path.basename(d)
                                            for d in needs[x]))
        if after.get(x):
            bits.append("after " + ",".join(os.path.basename(d)
                                            for d in after[x]))
        if why.get(x) and not needs.get(x) and not after.get(x):
            # the gate's own words, when no `needs`/`after` bit already
            # says it — `held by <child> (parked)`, a container, a clash
            bits.append(why[x])
        if cl:
            bits.append(f"claim {cl['who']}"
                        + (f" since {cl['since']}" if cl["since"] else ""))
        if q:
            bits.append(f"questions {q}/{a} answered")
        # the same word the page prints on the row — one rule, `silent_of`
        sil = silent_of(p, settings, collect=x in collect)
        if sil is not None:
            bits.append(f"silent {fmt_age(sil)}")
        return "  " + " · ".join(bits)

    # One PRD, one section, in THE PRESSURE ORDER — the single ranking this
    # board is worked in, and the same one the timeline stacks its rows by.
    # See @references/parts/order.md. Everything above `in flight` is something
    # this pass can act on now; `in flight` is held by somebody else. A PRD
    # listed twice is a pass that has to work out which line meant it.
    # `bands` is the one computation of it — `cmd_next` reads the same call.
    collect, yours, flight, ready, gated, why = bands
    # The drill section, FIRST — above collect, the pressure order's own head:
    # the scan opens on the questions waiting on the user. A question already
    # out — the pass file's `## Asked` carries it — is marked `out`, carried
    # and never re-put; `claim` counts the unput ones and refuses.
    if len(drill) >= 2:
        askers = len({rel for rel, _q, _t, _o in drill})
        print(f"\ndrill — asking {len(drill)} over {askers} PRD"
              + ("s" if askers != 1 else "")
              + " · one pass to the user before any claim")
        for rel, qid, title, is_out in drill:
            print(f"  {rel} · {qid} {title}" + (" · out" if is_out else ""))
    for title, group in (
            (f"collect — {len(collect)} finished, waiting to be closed",
             collect),
            (f"waiting on you — {len(yours)}", yours),
            (f"in flight — {len(flight)} held by a worker", flight),
            (f"ready — {len(ready)} dispatchable now, in order", ready),
            (f"gated — {len(gated)}, as their gates clear", gated)):
        if not group:
            continue
        print("\n" + title)
        for x in group:
            print(line(x))
    rf = os.path.join(board, PASS_FILE)
    print(f"\nround: {rf}" + ("" if os.path.isfile(rf) else "  (not written)"))


def knowledge_step(board):
    """Print step 7 — what the knowledge layer owes this round, if anything.

    Reads @resources/knowledge.py `stale_rows`: three mtimes, no note parsed,
    so this is affordable on every `next`. The tools are advisory to the
    loop, never a gate — an unimportable knowledge.py, a board with no wiki
    and a machine with no `gh` all print nothing and change nothing about
    which step the pass is on.
    """
    try:
        import knowledge as kb  # noqa: E402 — beside this file, per pearde_path
        store = kb.Store(os.path.join(board, "wiki"))
        rows = [r for r in kb.stale_rows(store) if r[0] >= 0]
    except Exception:
        return
    if not rows:
        return
    print(f"step 7 · knowledge — {len(rows)} tool(s) behind the board")
    print("  decision: none — each is one command, and the record is what"
          " step 2 answers a fork from")
    for _over, name, state, command in sorted(rows, key=lambda r: -r[0]):
        print(f"  {name}: {state}")
        print(f"  {command}")


def cmd_next(argv):
    """the loop step the pass is on — its decision and the exact command

    One call after `scan`: which of the eight steps the board is on, the
    decision that step asks the orchestrator to make, and the command to run
    — @references/parts/loop.md, with the step selection read off the same
    bands `cmd_scan` prints. Reads and never writes: no state moves, no pass
    file written, safe at any point. The pass file's `## Owed` line, when
    one is written, stands first — it is the pass's own memory of what is
    next, and it outranks nothing: the bands below it are the board's answer.
    """
    board = find_board(argv[0] if argv else None)
    rf = os.path.join(board, PASS_FILE)
    if os.path.isfile(rf):
        try:
            lines = [l for l in "\n".join(_h2_sections(
                open(rf, encoding="utf-8").read(), "Owed")).splitlines()
                if l.strip()]
        except OSError:
            lines = []
        if lines:
            print("owed: " + lines[0].lstrip("- ").strip())
    if not os.path.isfile(os.path.join(board, "settings.md")):
        print("step 1 · scan — no .pearde/settings.md here: first run")
        print("  decision: nothing — read; init says English on its first line")
        print("  pearde init")
        return
    if is_master(board) and not str(board_settings(board).get("name", "")).strip():
        print(f"step 1 · scan — master of {len(members(board))} with no name:")
        print("  decision: ask the user and write it into settings.md")
        return
    prds = scan(board)
    r = compute_plan(board, None, warn=False)
    collect, yours, flight, ready, gated, why = \
        pressure_bands(board, prds, r)
    # Every actionable section prints, in step order — the whole set this
    # turn acts on, with the board assuming unlimited parallel agents. Each
    # section only when non-empty; the first line keeps its shape.
    unput = [(rel, qid, title) for rel, qid, title, out
             in drill_questions(board) if not out]
    # Step 7 · knowledge, on EVERY pass. It used to print only at step 8,
    # under `nothing left to dispatch` — so on a board that never drained it
    # never printed, and the sweep, the corpus map and the board notes went
    # weeks between runs while the loop ran hourly. Three `stat` calls, and
    # only the stale tools take a line: a current board pays one line saying
    # so, or nothing when knowledge.py is not importable at all.
    knowledge_step(board)
    acted = False
    if unput:
        gate = (" — one drill pass to the user before any claim"
                if len(unput) > 1 else
                " — one standing is not a gate; put it and keep working")
        print(f"step 2 · answer — asking {len(unput)}{gate}")
        print("  decision: what to put to the user, and what they said")
        for rel, qid, title in unput:
            print(f"  {rel} · {qid} {title}")
        print('  pearde answer <prd> Q<n> "<text>" per answer')
        print("  claims on PRDs these questions do not touch go ahead; the"
              " rest wait — pearde claim says which")
        acted = True
    if collect:
        print(f"step 6 · collect — {len(collect)} finished, waiting to be"
              " closed")
        print("  decision: whether to believe the report; whether an edit"
              " was the atomic's")
        for x in collect:
            print(f"  pearde collect {x}")
        acted = True
    refine = [x for x in yours if prds[x]["state"] == "refine"]
    if refine:
        print(f"step 3 · refine — {len(refine)} came back REFINE")
        print("  decision: whether the analyst's `## Split` table is usable;"
              " a drill when it is not")
        for x in refine:
            print(f"  pearde refine {x} < report")
        acted = True
    failed = [x for x in yours if prds[x]["state"] == "failed"]
    if failed:
        print(f"step 6 · collect — {len(failed)} failed")
        print("  decision: what a failed attempt needs — `## Failure` first")
        for x in failed:
            print(f"  pearde release {x} failed")
        acted = True
    if ready:
        x = ready[0]
        impl = prds[x]["state"] == "specced"
        more = f" · {len(ready) - 1} more in order" if len(ready) > 1 else ""
        print(f"step {5 if impl else 4} · "
              f"{'implement' if impl else 'spec ahead'} — ready: {x}" + more)
        print("  decision: which persona the job wears")
        print("  dispatch every one of these in this turn, each as its own"
              " background worker — a worker's prompt is the brief command,"
              " not its output")
        for x in ready:
            impl = prds[x]["state"] == "specced"
            print(f"  pearde claim {x} <worker>")
            print(f"  pearde brief {x} --worker <worker>"
                  f" → dispatch as pearde-{'implementer' if impl else 'analyst'}")
        acted = True
    if acted:
        return
    if gated:
        x = gated[0]
        w = why.get(x) or ""
        print(f"gated — {x}: {w}")
        if w.startswith("workflow:"):
            print("  decision: the one refusal you clear yourself — fix the"
                  " slug or remove the key, then claim in the same pass")
        else:
            print("  decision: none — the gate clears as its own work lands")
        return
    if flight:
        print(f"in flight — {len(flight)} held by workers · nothing to act on")
        print("  next: a worker's line is step 6 — `pearde collect <prd>`")
        return
    if yours:
        print("step 8 · drill, then hand back — everything left is blocked"
              " on a person")
        for x in yours:
            print(f"  {x} · {prds[x]['state']}")
        print('  step 7 first: pearde knowledge query'
              ' "<the frontier\'s question>"')
        print("  drill pass → .pearde/.state/ask.md; rewrite"
              " .pearde/report.md and the pass file; hand back ASK / BLOCKED")
        return
    print("step 8 · hand back — nothing left to dispatch or ask")
    print("  rewrite .pearde/report.md and the pass file; hand back DRAINED")

def cmd_plan(board, workers):
    r = compute_plan(board, workers)
    if not r:
        print("plan: nothing to do — no undone PRDs")
        return
    prds, todo, parked = r["prds"], r["todo"], r["parked"]
    est, feet, needs, after = r["est"], r["feet"], r["needs"], r["after"]
    sched, unblocks = r["schedule"], r["unblocks"]
    cal = read_calibration(board)
    fw = lambda w: fmt_w(w, cal)
    mem = [n for n, _ in members(board)]
    print(f"plan: {len(todo)} PRDs"
          f" · workers={workers_label(r['workers'])}"
          f" · unspecced est'd at {fw(r['avg'])}"
          + (f" · master of {len(mem) + 1} boards: "
             + ", ".join([os.path.basename(os.path.dirname(board))] + mem)
             if mem else "")
          + (f" · {len(parked)} parked: " + ", ".join(
              f"{os.path.basename(r_)} [{prds[r_]['state']}]" for r_ in parked)
             if parked else ""))
    # Before everything else, because it comes before everything else: every
    # PRD here is finished work, and every PRD waiting on one of them waits
    # until it is committed and set `done`.
    if r["collect"]:
        print(f"\ncollect: {len(r['collect'])} finished, waiting to be closed")
        for x in r["collect"]:
            c, t = r["boxes"][x]
            print(f"  ✓ {x} [{todo[x]['state']}] {c}/{t} boxes closed")
    # The frontier, then the queue. There are no passes: a PRD starts the
    # moment its own gates clear, so the plan is the dispatch order and what
    # gates each entry — not waves that would hold unrelated work hostage to
    # the slowest member of a pass.
    frontier = plan_frontier(r)
    wf = workflow_marks(board, prds)
    if frontier:
        # `ready now` is the dispatch list, and step 5 of @references/parts/
        # loop.md skips a PRD whose `workflow:` names no workflow. The other
        # two skips already show here — an unmet `needs:` drops a PRD out of
        # this list, a footprint clash prints `after … (footprint)` — so
        # without this the one skip the ordering does NOT model is the one
        # the list silently contradicts. Display only: the mark is printed,
        # the order is untouched. Only the `?` form prints, because this
        # parenthetical is the register of what holds a PRD back and a slug
        # that resolves holds back nothing.
        print(f"\nready now — {len(frontier)} in parallel, widest door first")
        for x in frontier:
            p = todo[x]
            hot = p["state"] in ("question", "blocked", "refine", "failed")
            tags = ["waiting on you"] if hot else [] if feet[x] \
                else ["unspecced"]
            if wf.get(x, "").endswith("?"):
                tags.append("wf " + wf[x])
            print(f"  · {x} [{p['state']}] p{p['fm'].get('priority', 0)}"
                  f" {fw(est[x])} · unblocks {fw(unblocks[x])}"
                  + (f"  ({'; '.join(tags)})" if tags else ""))
    held = r["held"]
    gated = [x for x in r["order"]
             if (needs[x] or after[x] or x in held) and est[x] > 0]
    if gated:
        print("\nthen, as gates clear — dispatch order")
        for x in gated:
            p = todo[x]
            why = []
            if x in held:
                why.append(held[x])
            if needs[x]:
                why.append("needs " + ", ".join(os.path.basename(d)
                                                for d in needs[x]))
            if after[x]:
                why.append("after " + ", ".join(os.path.basename(d)
                                                for d in after[x])
                           + " (footprint)")
            if not feet[x]:
                why.append("unspecced")
            if wf.get(x, "").endswith("?"):
                # the mark the ready line carries, on the line the hold
                # moved it to — a dangling slug is visible in both lists
                why.append("wf " + wf[x])
            print(f"  · {x} [{p['state']}] p{p['fm'].get('priority', 0)}"
                  f" {fw(est[x])}" + (f"  ({'; '.join(why)})" if why else ""))
    if r["workers"]:
        print(f"\n≈ {fw(r['wall'])} wall @ {r['workers']} workers — a staffing"
              f" guess, not a promise. The dependency structure above is the"
              f" plan · peak {r['peak']} at once")
    else:
        print(f"\n≈ {fw(r['wall'])} on the critical path with unlimited agents"
              f" · peak {r['peak']} at once — the dependency structure above"
              " is the plan")

    mp, mp_path = load_map(board)
    mp["after"] = r["after"]
    mp["schedule"] = r["schedule"]
    mp["planned_at"] = datetime.date.today().isoformat()
    save_map(mp, mp_path)
    lpath = renderlib.write(board, gantt_payload(board, prds, mp, r["settings"]))
    print(f"\nview: {lpath}")
    print(f"      {serve_url(board)}   (live, with the board's other views)")

def cmd_status(board):
    prds = scan(board)
    ms = scan_memos(board)
    bad = memolib.check(board) if memolib.scan(board) else []
    memo_note = ""
    if ms:
        memo_note = (f" · {len(ms)} memos"
                     + (f" ({len(bad)} failing the check)" if bad else ""))
    mem = members(board)
    print(f"board: {board} · {len(prds)} PRDs{memo_note}"
          + (f" · master of {len(mem)} member board(s)" if mem else ""))
    for name, path in mem:
        if not os.path.isdir(path):
            print(f"  @{name:14} MISSING — {path}")
            continue
        n = len(_scan_one(path))
        own = "" if os.path.isfile(os.path.join(path, "settings.md")) else \
            " · no settings.md"
        print(f"  @{name:14} {n:4} PRDs · {path}{own}")
    print(f"view: {serve_url(board)}")
    print(session_line(board))

def cmd_vision(board, flags):
    """`pearde vision` — the axis for a person: depth per PRD, the critical
    chain, the off-axis set. `--json` prints what `.vision.json` held.
    `--next` prints `plan`'s ready set alone, in axis order. `--check` is the
    `doctor` row: one line, exit 0, or the dangling names, exit 1."""
    prds = scan(board)
    vis = read_vision(board)
    ax = vision_axis(board, prds, vis) if vis else None
    live = [r for r, p in prds.items() if p["state"] in LIVE_STATES]
    on = sorted((r for r in live if ax and ax["depth"].get(r) is not None),
                key=lambda r: (-ax["depth"][r], -ax["reach"][r], r))
    off = sorted(r for r in live if not ax or ax["depth"].get(r) is None)
    chain = max((ax["depth"][r] for r in on), default=0) if ax else 0
    if "--check" in flags:
        if not vis:
            print("no vision.md")
        elif ax and ax["dangling"]:
            for line in ax["dangling"]:
                print(line)
            return 1
        elif not ax:
            print("vision declared · no terminals — no axis")
        else:
            print(f"{len(ax['terminals'])} terminal"
                  f"{'' if len(ax['terminals']) == 1 else 's'}"
                  f" · {len(on)} on · {len(off)} off · longest chain {chain}")
        return 0
    if not ax:
        if vis and vis["vision"]:
            print(f"vision: {vis['vision']}")
        print("no terminals declared — " + (
            f"write prds/{VISION_FILE} first: the destination in one sentence,"
            " and terminals: naming the PRDs whose completion is it"
            if not vis else
            "the board orders by dependency, weight and priority alone"))
        return 1
    if "--json" in flags:
        json.dump(vision_json(board, prds, ax), sys.stdout, indent=1)
        print()
        return 0
    if "--next" in flags:
        r = compute_plan(board, None, warn=False)
        nxt = plan_frontier(r) if r else []
        print(f"next — {len(nxt)} dispatchable now, in axis order")
        for x in nxt:
            d = ax["depth"].get(x)
            print(f"  · {x} [{prds[x]['state']}] "
                  + (f"depth {d}" if d is not None else "off-axis")
                  + f" · unblocks {ax['reach'].get(x, 0)}")
        return 0
    print(f"vision: {ax['vision']}")
    print(f"axis: {len(on)} on · {len(off)} off · longest chain {chain}")
    for line in ax["dangling"]:
        print(f"dangling: {line}")
    if on:
        print("chain: " + " → ".join(critical_chain(ax, prds, on[0])))
    for d in sorted({ax["depth"][r] for r in on}, reverse=True):
        here = [r for r in on if ax["depth"][r] == d]
        print(f"\ndepth {d} — {len(here)} PRD{'' if len(here) == 1 else 's'}"
              + ("  ← the vision" if d == 0 else ""))
        for r in here:
            print(f"  {r} [{prds[r]['state']}]"
                  f" p{prds[r]['fm'].get('priority', 0)}"
                  f" · unblocks {ax['reach'][r]}")
    if off:
        print(f"\noff-axis — {len(off)} with no path to a terminal")
        for r in off:
            print(f"  {r} [{prds[r]['state']}]")
    return 0
VISION_FLAGS = Flags(("board",), ("json", "next", "check"))

def _vision_cli(argv):
    """`pearde vision [board] [--board <path>] [--json|--next|--check]` —
    argv is everything after the command name, the return is the exit code.
    A flag outside the declaration is refused before the board is read,
    exit 2, naming the flag and the list."""
    import transitions as translib       # the parser; it imports this module
    try:
        args = translib.Args(argv, VISION_FLAGS, "vision")
    except translib.FlagRefused as e:
        print(f"pearde vision: {e}", file=sys.stderr)
        return 2
    board = find_board(args.opt.get("board")
                       or (args.pos[0] if args.pos else None))
    return cmd_vision(board, ["--" + f for f in args.flags])

# What the `pearde` dispatcher discovers: {name: callable(argv) -> exit code}.
_vision_cli.flags = VISION_FLAGS      # what `pearde vision --help` prints
cmd_example.flags = EXAMPLE_FLAGS
COMMANDS = {"vision": _vision_cli}
COMMANDS["example"] = cmd_example
COMMANDS["next"] = cmd_next


def main():
    raw = sys.argv[1:]
    for i in range(len(raw) - 1):           # `--workers N` is `--workers=N`
        if raw[i] == "--workers":
            raw[i:i + 2] = [f"--workers={raw[i + 1]}"]
            break
    args = [a for a in raw if not a.startswith("--")]
    flags = [a for a in raw if a.startswith("--")]
    cmd = args[0] if args else "status"
    if cmd == "example":          # its argument is not a board yet
        sys.exit(cmd_example(sys.argv[2:]))
    board = find_board(args[1] if len(args) > 1 else None)
    if cmd == "plan":
        workers = next((f.split("=", 1)[1] for f in flags
                        if f.startswith("--workers=")), None)
        cmd_plan(board, workers)
    elif cmd == "reconcile":
        moved = reconcile(board)
        print(f"reconcile: {'schedule re-ordered' if moved else 'no change'}")
    elif cmd == "members":
        mem = members(board)
        if not mem:
            print(f"{board} is not a master board — no members: in settings.md")
        for name, path in mem:
            mark = "" if os.path.isdir(path) else "  MISSING"
            print(f"@{name}\t{path}{mark}")
    elif cmd == "gantt":
        cmd_gantt(board, open_after="--open" in flags)
    elif cmd == "calibrate":
        cmd_calibrate(board)
    elif cmd == "status":
        cmd_status(board)
    elif cmd == "next":
        cmd_next(sys.argv[2:])
    elif cmd == "scan":
        cmd_scan(board)
    elif cmd == "vision":
        sys.exit(cmd_vision(board, flags))
    else:
        die(f"unknown command '{cmd}' — scan | next | plan | reconcile | gantt"
            " | calibrate | members | status | vision | example")


if __name__ == "__main__":
    # `state_dir` refuses with an exception rather than `die()` so the daemon's
    # writers skip one board instead of dying. A person at the CLI wants the
    # one-line refusal, not the traceback: it is turned back here, at the
    # boundary where the process IS the caller.
    try:
        main()
    except NotABoard as e:
        die(str(e))
