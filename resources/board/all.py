#!/usr/bin/env python3
"""pearde all — every board this machine watches, on one page.

`all` is not a board. Nothing of it is on disk: no `.pearde/`, no
`settings.md`, no PRD of its own, and no edit goes back through it. It is one
render over every board the live service is watching, built fresh on each
request out of those boards' own payloads, and thrown away again.

It is not a master board (@references/parts/master.md) and replaces none. A
master is a **plan**: members named in `settings.md`, one merged schedule, one
critical path across them, one orchestrator dispatching over the group. `all`
is a **display**: no configuration, no arithmetic across a board boundary, no
dispatch. Every board keeps its own plan, and every board's rows are laid out
on their own chain — side by side on one axis whose zero is the same now.

What it merges, per board:

  - that board's **own** PRDs. A master's payload also carries its members',
    and registering a master registers every member as a board in its own
    right, so counting both would print every member PRD twice. A row
    carrying a `board` is dropped here and picked up from the member itself.
    The rule and the promise are the same sentence: `all` shows the boards
    the daemon watches, and a member nobody watches is not one of them.
  - rels are qualified `@<board key>/<rel>` — the master board's own address
    form, which the view already groups, colours and folds by. The key is the
    `/board/<name>` key, so every row on this page can name the page it came
    from.
  - a `needs` inside the board is qualified with it. One pointing across a
    board boundary is dropped: `all` draws no edge it did not compute, and
    the one place such an edge is real is the master that declared it.

`dash` is the other half — one row per board, the counts a person opens this
page for, each a door into that board's own page.

    python3 all.py <board>…      the dashboard, as text
    python3 all.py --json <board>…   the merged payload
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan as planlib  # noqa: E402
import memos as memoslib  # noqa: E402

# The one key `all` answers to. A real board keying the same way would take
# the URL from under it, which is why `serve.register()` refuses the name.
KEY = "all"

# What a person came for, in the order they came for it. `asks` is the only
# one that is a person's own queue rather than the board's.
ASK_STATES = ("question", "blocked")


def board_payload(path):
    """One board's payload, exactly as `/data` would build it for that board.
    No cheaper reader exists and none should: the numbers on this page have to
    be the numbers on that board's own page, and a second arithmetic here is
    how the two would come to disagree."""
    return planlib.gantt_payload(path, planlib.scan(path),
                                 planlib.load_map(path)[0],
                                 planlib.board_settings(path))


def qualify(rows, key):
    """That board's own rows, addressed `@<key>/<rel>`.

    A row carrying a `board` came to that payload from a member board and is
    dropped — see the module docstring. Everything a row points at is
    qualified with it, so the merged graph has exactly the edges each board
    already had and not one more."""
    out = []
    for row in rows:
        if row.get("board"):
            continue
        r = dict(row)
        r["rel"] = f"{planlib.MEMBER_SIGIL}{key}/{row['rel']}"
        r["board"] = key
        if r.get("parent"):
            r["parent"] = f"{planlib.MEMBER_SIGIL}{key}/{r['parent']}"
        for field in ("needs", "after"):
            if r.get(field):
                r[field] = [f"{planlib.MEMBER_SIGIL}{key}/{n}"
                            for n in r[field]
                            if not str(n).startswith(planlib.MEMBER_SIGIL)]
        out.append(r)
    return out


def unqualify(rel):
    """(board key, that board's own rel) — the inverse, for a route that has
    to go back to the file. `None` for anything not addressed this way."""
    if not rel.startswith(planlib.MEMBER_SIGIL) or "/" not in rel:
        return None, rel
    key, _, rest = rel[1:].partition("/")
    return key, rest


def _merge_history(into, rows):
    """One row a day per board becomes one row a day. Summed, because the
    burn-down over several boards is the work left over several boards — a
    day where two boards each shed weight shed both."""
    for r in rows:
        d = r.get("d")
        if not d:
            continue
        cur = into.setdefault(d, {"d": d, "states": {}, "hleft": 0.0,
                                  "hdone": 0.0, "done": 0, "left": 0})
        for k in ("hleft", "hdone", "done", "left"):
            cur[k] = round(cur[k] + (r.get(k) or 0), 2)
        for st, n in (r.get("states") or {}).items():
            cur["states"][st] = cur["states"].get(st, 0) + n


def dash_row(key, path, p):
    """One board, as the dashboard reads it: what is waiting on a person, what
    is in flight, what is left. Every number here is that board's own — this
    row is a link with counts on it, never a second opinion about the board."""
    live = [t for t in p.get("tasks", [])
            if not t.get("past") and not t.get("parked")]
    states = {}
    for t in p.get("all", []):
        if t.get("board"):
            continue
        states[t["state"]] = states.get(t["state"], 0) + 1
    return {
        "board": key,
        "path": path,
        "name": p.get("board") or key,
        "prds": sum(1 for t in p.get("all", []) if not t.get("board")),
        "done": p.get("counts", {}).get("done", 0),
        "collect": p.get("counts", {}).get("collect", 0),
        "held": p.get("counts", {}).get("held", 0),
        "asks": sum(states.get(s, 0) for s in ASK_STATES),
        "silent": sum(1 for t in live if t.get("silent")),
        "left": round(sum(float(t.get("est") or 0) for t in live), 2),
        "states": states,
        "purpose": (p.get("vision") or {}).get("purpose", ""),
        # a master shows here as one board like any other — its own PRDs, the
        # ones spanning members. Said so the reader knows why it is small
        "master": bool(p.get("boards")),
        "error": None,
    }


def payload(entries):
    """The merged payload — the same shape `gantt_payload` returns for one
    board, so the view draws it with the code it already has.

    `entries` is [(key, path)]: every board the daemon watches, keyed the way
    its own `/board/<key>` URL is."""
    boards, tasks, everything, unplanned = [], [], [], []
    land, repos, trans, dash = [], [], [], []
    hist, states, calibs = {}, set(), []
    counts = {"done": 0, "parked": 0, "containers": 0, "collect": 0, "held": 0}
    day_h, anchor, workers = 0.0, None, 0
    for key, path in entries:
        try:
            p = board_payload(path)
        except Exception as e:  # one unreadable board must not blank the page
            dash.append({"board": key, "path": path, "name": key, "prds": 0,
                         "done": 0, "collect": 0, "held": 0, "asks": 0,
                         "silent": 0, "left": 0, "states": {}, "purpose": "",
                         "master": False, "error": f"{type(e).__name__}: {e}"})
            continue
        boards.append(key)
        tasks += qualify(p.get("tasks") or [], key)
        everything += qualify(p.get("all") or [], key)
        unplanned += [f"{planlib.MEMBER_SIGIL}{key}/{r}"
                      for r in (p.get("unplanned") or [])]
        for row in (p.get("landing") or []):
            r = dict(row, board=key)
            if row.get("rel"):
                r["rel"] = f"{planlib.MEMBER_SIGIL}{key}/{row['rel']}"
            land.append(r)
        repos += [dict(r, board=key) for r in (p.get("repos") or [])]
        trans += [dict(r, board=key) for r in (p.get("transitions") or [])]
        _merge_history(hist, p.get("history") or [])
        states |= set(p.get("states") or [])
        for k in counts:
            counts[k] += p.get("counts", {}).get(k, 0)
        day_h = max(day_h, float(p.get("dayHours") or 0))
        a = p.get("anchor")
        anchor = a if anchor is None else min(anchor, a)
        try:
            workers += int(str(p.get("workers") or 0))
        except ValueError:
            pass
        calibs.append(json.dumps(p.get("calib"), sort_keys=True))
        dash.append(dash_row(key, path, p))
    dash.sort(key=lambda r: (-(r["asks"] + r["collect"]), -r["left"],
                             r["board"]))
    # Real hours are a fit per board (@references/parts/order.md), and two
    # fits cannot both be the axis. Agreeing boards keep theirs; disagreeing
    # ones print raw weight, which is the one number that means the same
    # thing on every board here.
    calib = (json.loads(calibs[0]) if calibs and len(set(calibs)) == 1
             else None)
    live = sorted(planlib.LIVE_STATES | {"done"})
    return {
        "board": KEY,
        # the view groups, colours and folds by these — the master board's
        # own mechanism, pointed at the watch set instead of at `members:`
        "boards": boards,
        # what this page is, said in the payload: no plan of its own, and
        # nothing here writes back
        "virtual": True,
        "readonly": True,
        "dash": dash,
        "all": everything,
        "tasks": tasks,
        "unplanned": unplanned,
        "history": [hist[d] for d in sorted(hist)],
        "transitions": sorted(trans, key=lambda r: str(r.get("at") or ""))[-60:],
        # the guard counts one session, and this page is over none of them
        "guard": None,
        "states": live + sorted(states - set(live)),
        "anchor": anchor or datetime.date.today().isoformat(),
        "dayHours": day_h or 8.0,
        "calib": calib,
        "tune": planlib.TUNE,
        "workers": str(workers or ""),
        "vision": {"purpose": ""},
        "counts": counts,
        "landing": land,
        "repos": repos,
    }


def memos(entries):
    """Every board's decisions, slugged `@<key>/<slug>` the way a master
    slugs a member's. The file never moves; this is the one page that reads
    them all at once."""
    out = []
    for key, path in entries:
        try:
            ms = memoslib.scan(path)
        except Exception:
            continue
        for m in ms.values():
            prds = m["fm"].get("prds")
            prds = prds if isinstance(prds, list) else [prds] if prds else []
            out.append({"slug": f"{planlib.MEMBER_SIGIL}{key}/{m['slug']}",
                        "subject": m.get("subject"), "kind": m.get("kind"),
                        "status": m.get("status"),
                        "date": str(m.get("date") or ""),
                        "path": m.get("path"), "board": key,
                        "prds": prds, "body": m.get("body", "")})
    out.sort(key=lambda m: (str(m["status"]), str(m["date"])), reverse=True)
    return out


def text(pl):
    """The dashboard as a person reads it in a terminal — the same rows the
    page draws, for a check that has no browser."""
    rows = pl.get("dash") or []
    if not rows:
        return "no board registered"
    w = max(len(r["board"]) for r in rows)
    out = [f"{len(rows)} board(s) · {len(pl['all'])} PRDs · "
           f"{pl['counts']['collect']} to collect · "
           f"{pl['counts']['held']} in flight"]
    for r in rows:
        if r.get("error"):
            out.append(f"{r['board']:<{w}}  unreadable — {r['error']}")
            continue
        bits = [f"{r['prds']:>4} PRDs", f"{r['left']:>7.1f}w left",
                f"{r['done']:>4} done"]
        if r["collect"]:
            bits.append(f"{r['collect']} to collect")
        if r["asks"]:
            bits.append(f"{r['asks']} waiting on you")
        if r["held"]:
            bits.append(f"{r['held']} in flight"
                        + (f" ({r['silent']} silent)" if r["silent"] else ""))
        out.append(f"{r['board']:<{w}}  " + " · ".join(bits))
    return "\n".join(out)


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("-")]
    if not paths:
        paths = [planlib.find_board(None)]
    entries = []
    for p in paths:
        p = os.path.abspath(p)
        entries.append((planlib.project_name(p), p))
    pl = payload(entries)
    print(json.dumps(pl, indent=1, sort_keys=True) if as_json else text(pl))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
