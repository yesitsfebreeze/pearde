---
state: done
origin: requested
priority: 90
complexity: 35
blast-radius: high
footprint:
  - resources/board/schedule.py
  - resources/board/plan.py
workflow: probe-then-spec
actual: 3.13h
---

# the plan is parallel and only dispatch is capped

`plan` bakes two dispatch-time restrictions into the plan itself. The result is
a plan that reads as a queue, on boards whose work is not one — and a person
reading it staffs against a wall nobody will experience.

**Measured on `/Users/feb/dev/manola/pearde`, 2026-09-03**, 16 live PRDs:

| plan built from | wall | peak |
|---|---|---|
| `needs:` + footprint clash edges — as shipped | 159.7 h | 4 |
| `needs:` alone — the real dependency graph | **85.3 h** | **10** |

The footprint edges cost **47 % of the plan and six PRDs of width**. On that
board only **two** of nine post-frontier edges were real `needs:`; every other
one printed `(footprint)`, and almost all resolved to a single 1,855-line file
that the clashing PRDs write in disjoint key ranges.

## The two restrictions, and why neither belongs in the plan

**1 — the footprint clash is an edge in `edges`.** `schedule.py:255-262` adds
`after[s].append(r)` *and* `edges[s].append(r)` for every overlapping pair, so
the clash orders the schedule, the topological depth, `unblocks`, and therefore
the frontier.

`dispatch.py` already enforces the same guarantee at runtime, and says so in its
own docstring:

> Clash-checking the in-flight set rather than a precomputed wave is the same
> guarantee — no two writers on one real path — reached without a barrier:
> wave 2's first row starts the moment wave 1's clashing row is in, instead of
> waiting for wave 1's slowest.

So the constraint is enforced twice: once statically, pessimistically, in the
plan, and once dynamically, correctly, at dispatch. The static copy is the one
that lies — it fixes an order dispatch will not follow.

**2 — `workers:` caps the plan's simulation.** `schedule.py:301`,
`nslots = workers if workers > 0 else max(len(todo), 1)`. A board's worker
budget is a statement about how many agents may run, not about how much of the
work is independent. `run.py:615` already calls `compute_plan(path, workers=0)`
for exactly this reason on the machine-wide runner; the per-board `plan` does
not.

On the board measured above the cap happened not to bind — 3, 6 and unlimited
all returned 159.7 h — which is itself the finding: **raising workers changed
nothing, so the plan was never worker-bound, and the label `wall @ 3 workers`
pointed a reader at the wrong lever.**

## What must be true when this is done

- **The plan's structure is `needs:` and nothing else.** Footprint overlap is
  reported, never scheduled.
- **A footprint clash is still visible**, because it is real and it is what
  dispatch will serialise — as a note on the row (`shares
  src/i18n/dictionaries.ts with X`), not as an `after` edge that moves it down
  the plan.
- **The wall is a band, not a number.** The dependency floor (the critical path)
  and the clash-serialised ceiling, both printed, so a reader sees what the
  shared files cost and can decide to split one.
- **`workers:` does not shape the plan.** It stays the dispatch cap —
  `board_caps` / `plan_workers` keep reading it, `dispatch` keeps honouring it —
  and `plan` may print it as context, never as a constraint on the schedule.
- The frontier widens as a consequence, which is the point: `plan_frontier`
  offers clashing rows together and `dispatch` holds the loser at launch, which
  is the arrangement the dispatcher was built for.

## Constraints

- **`after` stays computed.** `mapfile.py:174` ships it to the view — *„a
  footprint clash, serialized pairwise: this PRD starts when those end"* — and
  the Gantt draws it. What changes is that it stops feeding `edges`; the map
  keeps the pairs so the view can still draw them, and the view's own wording
  is corrected in the same pass if it now overstates.
- **Do not remove the clash guarantee anywhere.** `dispatch.py` is the enforcer
  and is not touched. A change that lets two workers write one path is the
  failure this must not cause.
- **`unblocks` changes meaning** once clash edges leave `edges` — it becomes the
  weight waiting on a real dependency rather than on a file collision. That is
  the correct meaning and it re-orders the frontier; say so in the spec.
- Boards that genuinely want the staffed simulation keep it: `compute_plan`
  takes an explicit cap, and `plan --workers N` prints that view.
- `.pearde/` here is a live board with workers in flight on `common.py`,
  `dispatch.py` and the lock. Rebase before collect.

## Pointers

- `resources/board/schedule.py:244-262` — `edges`, and where the clash is added
- `resources/board/schedule.py:301` — `nslots`
- `resources/board/schedule.py:321` — `pending`, the capped/uncapped hold split
- `resources/board/plan.py:459-464` — the two wall lines already written for
  both readings
- `resources/board/dispatch.py:231-238` — the runtime clash check, and its
  argument for not precomputing waves
- `resources/board/run.py:615` — `compute_plan(path, workers=0)`, the precedent
- `resources/board/mapfile.py:174` — `after` in the view payload

## Acceptance

- [x] the plan's schedule is built from `needs:` only, and a footprint overlap moves no PRD
- [x] a clashing PRD still shows what it shares and with which PRD, on its own row
- [x] `plan` prints both walls — the dependency floor and the clash-serialised ceiling — and neither is labelled as the other
- [x] `workers:` shapes no schedule; `dispatch` still refuses a second writer on one real path, proved by a test that tries
- [x] the manola board re-measures at the floor, not the ceiling: peak ≥ 10 where it was 4
- [x] the view still draws the pairwise clash, and its wording matches what the plan now claims

## Report

spec01: exit 0
PASS: a and b both in frontier
PASS: wall_floor == 10 (settings workers:1 ignored)
PASS: wall_ceiling == 20
PASS: peak == 2 unconstrained
PASS: explicit cap 1 -> peak 1
PASS: explicit cap 1 -> wall 20

spec02: exit 0
PASS: shares note on a's or b's row (bare)
PASS: no `then, as gates clear` section (bare, nothing else gates)
PASS: bare prints floor and ceiling, not `wall @ N workers`
PASS: capped run ALSO prints floor/ceiling
PASS: capped run additionally names the staffed simulation

spec03: exit 0
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk
references/parts/handles.md references @@purge — no such keyword
references/parts/handles.md references @resources/board/purge.py — not on disk
PASS: wording corrected, no new drift

spec04: exit 0
windows: {'a': {'start': 1788455106.33019, 'end': 1788455106.970104}, 'c': {'start': 1788455106.337097, 'end': 1788455106.985095}, 'b': {'start': 1788455107.032289, 'end': 1788455107.708321}}
done=3 refused=0 dead=0
PASS: a/b serialized on the shared path, c ran alongside
