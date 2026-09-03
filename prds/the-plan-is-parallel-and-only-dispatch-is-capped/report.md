Verdict: DONE

# the plan is parallel and only dispatch is capped — report

Second pass on `probe-then-spec` (`.pearde/workflows/probe-then-spec.md`, 60
runs): the specs already existed and the analyst's build already stood,
uncommitted, in the lane. This pass verified each spec's block against the
tree, ran every spec's own `## Verify and Proof`, ran the repo's gate, and
ticked boxes.

## Workflow probe-then-spec

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | read-the-contract | passed | read `prd.md` and all four specs |
| 2 | capture-the-harness-baseline | passed | per step 3's `Fails when` row for a second pass: compared `resources/index.py check`, `resources/memos.py check` and `doctor.sh` output between the checkout (`/Users/feb/dev/infra/pearde`) and the lane — identical, so any red in the lane is pre-existing, not this pass's |
| 3 | attempt-the-build | passed | entered for **no spec** — `git diff` on the lane against each spec's own footprint (`schedule.py`, `plan.py`, `mapfile.py`+`view.md`) shows the build already matches every "what stands" paragraph; spec04's `probe/verify.sh` and `probe_dispatch_clash.py` already exist in `.pearde/prds/…/probe/` and match spec04's text exactly |
| 4 | re-run-the-harnesses | passed | each spec's `## Verify and Proof` block run fresh (all PASS, exit 0) plus the repo gate: `index.py check` (3 pre-existing lines, identical in checkout and lane), `memos.py check` (rc=1, identical 43-line output in checkout and lane — missing `tags:` on pre-existing memos, none in this PRD's footprint), `doctor.sh` (same `index`/`claims`/`memos`/`knowledge`/`questions` rows red in the plain checkout too — none name a footprint file of this PRD) |
| 5 | write-the-specs | passed | no spec authored (specs already exist); acceptance boxes checked against the standing blocks and ticked where the verify output backs them |

### Edits

none — every atomic's `Fails when`/`Done when` matched what this pass found; no wrong command, stale path, unfailable check or undocumented shape surfaced.

## Per-spec verify output

**spec01** (`resources/board/schedule.py`) — all 4 boxes ticked:
```
PASS: a and b both in frontier
PASS: wall_floor == 10 (settings workers:1 ignored)
PASS: wall_ceiling == 20
PASS: peak == 2 unconstrained
PASS: explicit cap 1 -> peak 1
PASS: explicit cap 1 -> wall 20
```

**spec02** (`resources/board/plan.py`) — 5 boxes ticked (verify block's 5 checks, plus the "gated PRD that also clashes shows both" box hand-verified with a 3-PRD fixture: `c [open] p30 10.0w  (needs b; shares shared/file.md with a)`):
```
PASS: shares note on a's or b's row (bare)
PASS: no `then, as gates clear` section (bare, nothing else gates)
PASS: bare prints floor and ceiling, not `wall @ N workers`
PASS: capped run ALSO prints floor/ceiling
PASS: capped run additionally names the staffed simulation
```

**spec03** (`resources/board/mapfile.py`, `references/parts/view.md`) — 4 boxes ticked:
```
PASS: wording corrected, no new drift
```
(`index.py check` still names the 3 pre-existing lines — `resources/common.py`,
two `hotreload-test.js` dangles — none of them `mapfile.py` or `view.md`.)

**spec04** (`prds/…/probe/verify.sh`) — 3 boxes ticked, run with
`PROBE_LANE` set to this lane, launching through the real
`dispatch.dispatch`:
```
windows: {'a': {...}, 'c': {...overlaps a...}, 'b': {...starts after a ends...}}
done=3 refused=0 dead=0
PASS: a/b serialized on the shared path, c ran alongside
```

## PRD acceptance — all 6 boxes ticked

The manola-board box was measured directly (the board exists on this
machine): `compute_plan("/Users/feb/dev/manola/pearde", None)` →
`wall_floor 85.29`, `wall_ceiling 159.71`, `peak 10` — the exact floor/ceiling
the PRD's own table names, and peak 10 where it was 4.

## Findings (not specced, not fixed — outside this PRD's footprint)

- `resources/board/transitions.py`'s `sections()` still excludes a PRD from
  its own "ready" count on `r["after"].get(x)` — the identical predicate this
  PRD removed from `plan_frontier`, missed by an earlier PRD.
- `resources/board/view.js`'s peak-agents tile still reads `"at " +
  DATA.workers + " workers: " + fmtW(cal)` — `cal` is now unconditionally the
  floor; the tile's wording still implies `workers:` shapes it.
- The repo gate (`memos.py check`, `doctor.sh`'s `index`/`claims`/`questions`/
  `knowledge` rows) is red board-wide, identically in the plain checkout —
  pre-existing, unrelated to this PRD's footprint.

## Scores

complexity: 35
blast-radius: high
workflow: probe-then-spec
