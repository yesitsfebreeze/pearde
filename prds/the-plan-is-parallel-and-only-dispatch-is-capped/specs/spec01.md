---
complexity: 15
footprint:
  - resources/board/schedule.py
---

# spec01 — `compute_plan`'s schedule is `needs:` alone

The plan's structure stops being `needs:` plus a footprint clash baked in as
an `after` edge that also fed `edges`. `edges` is now the dependency graph
only; the footprint pairing is still found (same ranked, cycle-safe walk)
but landed on a second, parallel graph (`combined`, seeded from `edges`) that
never feeds back into `edges`. `workers:` stops auto-capping the discrete
event simulation that produces `wall`/`peak`/`order`/`schedule` — only an
explicit cap handed to `compute_plan` (`plan --workers N`) does; the board's
own `settings.md` value now resolves into `workers` for display and for
every other reader of it (`board_caps`, `dispatch`) alone.

**What stands** — `edges = {r: list(needs[r]) for r in todo}` never gains a
footprint entry. A new `combined` graph starts as a copy of `edges` and grows
exactly the way the old `edges` did (the same `path()`/cycle-avoidance walk,
now over `combined`), so `after[s]` is still found with the same rule
(overlap, no existing path either way) — it is simply never appended to
`edges` any more. `plan_frontier` no longer excludes on `r["after"][x]`: a
footprint clash offers both PRDs of a pair together. `compute_plan` gained
`explicit`/`cap`: `cap` is 0 unless THIS call was handed a real `workers`
argument, and every place that used to branch on `workers > 0` for the
simulation (`nslots`, the held-PRD tail-pending logic) now branches on `cap
> 0`. Two new return fields: `wall_floor` (`needs:` alone, unlimited agents
— a critical-path recursion over `edges`, not a second discrete-event
simulation) and `wall_ceiling` (the same recursion over `combined` — every
footprint clash serialised, worst case). `wall`/`peak`/`order`/`schedule`
are unchanged in shape and are now what an UNcapped run produces by default
— identical to `wall_floor`/`peak` when `cap` is 0, and the STAFFED
simulation's own numbers when a caller passes an explicit cap (`spec02`
prints that distinction; this spec only produces the numbers). A new
`overlap_paths(a, b)` helper names the actual clashing path(s) between two
footprints, for the row that reports a clash instead of scheduling around
it.

**What is left** — nothing under this footprint; verified against a
synthetic fixture (two PRDs sharing a footprint, no `needs:` between them,
plus one genuinely gated by `needs:`) and against the live board (196 PRDs,
no crash, floor 18.8h vs ceiling 27.6h vs the old single number). One
related defect this spec does NOT touch: `resources/board/transitions.py`'s
`sections()` still excludes a PRD from its own "ready" count when
`r["after"].get(x)` is truthy — a third copy of the exact predicate this
spec removes from `plan_frontier`, missed by an earlier PRD that only fixed
the CLAIM gate. Reported in the PRD's report, not fixed here — a different
file than either named in this PRD's own footprint.

## Acceptance

- [x] `edges[s]` after the ranked overlap loop contains no entry that is not
      in `needs[s]` — a footprint pairing never lands there
- [x] `plan_frontier` returns both halves of a clashing pair when neither has
      an unmet `needs:` — proved on a fixture where `a` and `b` share a
      footprint and carry no `needs:`
- [x] `compute_plan(board, None)` on a board whose `settings.md` sets
      `workers: 1` returns the SAME `wall_floor`/`peak` as `workers: 0` would
      — the setting alone does not narrow the simulation
- [x] `compute_plan(board, 1)` (an explicit cap) still narrows `wall`/`peak`
      to the one-slot simulation — the staffed view a caller may still ask
      for is not removed, only no longer the default
- [x] `wall_ceiling` on the two-PRD clash fixture equals the sum of both
      PRDs' weight; `wall_floor` on the same fixture equals the larger of
      the two alone

## Verify and Proof

```sh
cd resources/board
python3 - <<'PY'
import sys, os, tempfile
sys.path.insert(0, ".")
sys.path.insert(0, "..")
import plan as planlib

def board(td, workers_setting=None):
    b = os.path.join(td, "board")
    for n in ("a", "b"):
        os.makedirs(os.path.join(b, "prds", n))
    if workers_setting is not None:
        open(os.path.join(b, "settings.md"), "w").write(
            f"---\nworkers: {workers_setting}\n---\n")
    for n, p in (("a", 50), ("b", 40)):
        open(os.path.join(b, "prds", n, "prd.md"), "w").write(f"""---
state: open
origin: requested
priority: {p}
complexity: 10
blast-radius: low
footprint:
  - shared/file.md
---

# {n}
""")
    return b

ok = True
with tempfile.TemporaryDirectory() as td:
    b = board(td, workers_setting=1)
    r = planlib.compute_plan(b, None, warn=False)
    fr = planlib.plan_frontier(r)
    checks = [
        ("a and b both in frontier", "a" in fr and "b" in fr),
        ("wall_floor == 10 (settings workers:1 ignored)", r["wall_floor"] == 10.0),
        ("wall_ceiling == 20", r["wall_ceiling"] == 20.0),
        ("peak == 2 unconstrained", r["peak"] == 2),
    ]
    rc = planlib.compute_plan(b, 1, warn=False)
    checks.append(("explicit cap 1 -> peak 1", rc["peak"] == 1))
    checks.append(("explicit cap 1 -> wall 20", rc["wall"] == 20.0))
    for name, cond in checks:
        print(("PASS" if cond else "FAIL") + f": {name}")
        ok = ok and cond
sys.exit(0 if ok else 1)
PY
```
