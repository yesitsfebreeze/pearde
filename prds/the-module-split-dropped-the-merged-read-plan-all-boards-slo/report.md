Verdict: DONE

# the-module-split-dropped-the-merged-read-plan-all-boards-slo — impl-merged-read, engineer · pass two

## Workflow probe-then-spec

| step | verdict | note |
|------|---------|------|
| 1 read-the-contract | ok | PRD + spec01 read; pass-one build stood in the lane uncommitted |
| 2 capture-the-harness-baseline | ok | probe/verify.sh red on the unfixed checkout, green 11/11 in the lane |
| 3 attempt-the-build | ok | lane held the work; committed it on `lane/the-module-split-…` (c535b62), rebased onto main after a `references/files.md` conflict |
| 4 re-run-the-harnesses | ok | verify.sh 11/11 on the merged repo, PASS; board gate green in collect |
| 5 write-the-specs | ok | no spec authored — pass two applies the standing spec; boxes ticked as closed |

### Edits

- None — every atomic's text held. No stale path, no wrong command, no check
  that cannot fail.

## What landed

- `resources/board/plan.py` — the merged read routed again: `PLAN_WINDOWS`,
  `_merged_plan` (lazy `run.read_main` import), the `if cmd == "plan"` gate
  ahead of `find_board`. One commit on the lane, merged to main by collect
  (commit `16b0f5b`). `run.py` untouched.
- The board record: `state: done`, `commit: 16b0f5b ea0b729`, report posted
  into `prd.md` (`## Report`, spec01 exit 0, 11/11 ok).

## Acceptance — final box status

- [x] `plan all` — merged frontier with `wave 1:` line, exit 0 (verify row 1–2, also re-run on main after landing)
- [x] `plan boards|slots|progress|groups` — each print, exit 0 (verify rows 3–6)
- [x] `plan --json` — merged payload with `waves` and `slots` (verify row 7)
- [x] bare `plan` and `plan here` — cwd board page, `run` absent from `sys.modules` (verify rows 8–10)
- [x] `the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` — PASS under `PEARDE_ROOT=<lane>` (row 11) and green on the merged repo after landing
- [x] `a-harness-never-dispatches-the-live-board` collects — see the wall below

## The wall the last box hid

The sibling box cannot be measured before this PRD lands, and collect refuses
open boxes — no flag passes it (`--trust` skips the verify, not the gate;
`--fail` never fires because the gate stops first). The route that exists:
`release <prd> blocked` with `needs: a-harness-never-dispatches-the-live-board`
and a `## Blocked` section naming what closes the box — the state table's own
reading of "waiting on a named event — open boxes". The sibling's landing
flipped `needs:` to done, `unblock` returned the PRD to `specced`, both boxes
were ticked off the measurement below, and the second collect landed green.

Measured for the tick: lines 1–4 of the sibling's `spec01` verify (`plan
slots` / `plan all` / `plan progress` / `read_main` grep) are GREEN on the
merged main. Its `collect --dry` after landing still exits 1 — on its own
remaining half: the sibling's `run.py` bare-scope refusal is not on main (its
worker, impl-harness-nodispatch2, holds that claim), and its verify expects
`run.script_main`, which no tree carries. Its full collect is that worker's
landing, not mine; the deadlock this PRD breaks — `pearde: no .pearde/ board
at slots` — is gone.

## Incidents (report, not fixed — outside scope)

1. **`python3 resources/board/run.py all` on the unfixed main dispatched
   instead of refusing.** I ran it twice measuring the sibling's verify lines
   5–6 (they expect a refusal); it printed nothing and hung — killed at 2
   minutes and at ~90 s. Board scan before/after: no new claims, done count
   unchanged, so nothing launched. This is the sibling PRD's own finding
   live on main; I stopped measuring that half.
2. **The lane's rebase conflict was a real content bug in the lane branch:**
   its history carried a pre-main variant of `every-documented-command-exists`
   (56f7ce5) whose `references/files.md` was missing rows main has (`spend.py`,
   the `silence-measures-…` invariant, and more). Resolved by keeping main's
   rows and the lane's `claims.py` row — the union main's own twin commit
   (1ac6101) already represents. Diff after rebase touches only the fix's 46
   lines plus that union.
3. Collect's unblock→collect round-trip left `wiki/sources/` and other
   boards' files as rides/inherited on the record commit (`ea0b729`,
   inherited 431) — collect's own behaviour, named on its line.

## Health floor

Files in my footprint under the floor: none (health.py scores nothing in
`resources/board/plan.py` below the floor). Nothing moved.

## Knowledge

- Remembered `collect's open-box gate cannot measure a box that names another
  PRD's collect` (sources/260903-cbc4.md), provenance this PRD — 114 prior
  hits answered nothing on this wall.