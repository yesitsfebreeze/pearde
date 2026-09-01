# report — two-questions-start-a-drill (implementer)

Verdict: **DONE**. Three specs, 13 acceptance boxes, all ticked against output
run here. Repo gate green (`doctor` closes `every part this repo owns checks
out`). One neighbour harness is red on the contract this PRD landed, named
below under `## Outside the footprint` — it is another PRD's file and was not
touched.

## What pass one already had, and what I changed

Pass one's code in `resources/questions.py`, `resources/board/plan.py`,
`resources/board/transitions.py` and the four manual files was correct as it
stood: the count, the section, the gate and the prose all held on first run.
Two things were not done, and both were mine:

1. **The fixture did not prove the boxes it claimed.** `probe/spec-fixture.sh`
   existed but had three holes — rebuilt, below.
2. **`references/parts/loop.md` broke two pins another PRD holds on it** —
   the only defect this run found in my own footprint. Fixed, below.

## The fixture, rebuilt — `probe/spec-fixture.sh`

Three holes, each of which let a box read green without being tested:

- **spec02 box 3 was never run.** Leg 4's own heading said "claim goes" and no
  claim was made in it — the only claim target, `other`, had been consumed by
  leg 3. The board now carries `other2`, leg 4 removes the round file first so
  the one question left is genuinely *unput* (the case the gate must still let
  through), and the claim is made and checked.
- **spec02 box 2 checked only the exit code.** It now checks the state moved
  `open → analyzing` and that `claim: w ` was written.
- **`set -e` swallowed every FAIL line.** The spec blocks invoke the script as
  `bash -e -o pipefail …`, and the legs were written `grep -q …; rc=$?` — a
  failing grep exited the script before its own `FAIL:` line printed, so a red
  box was indistinguishable from the box after it. The script now takes `-e`
  back on its first line (`set +e`) and exits on its own failure count.

Also strengthened: leg 1 checks the drill heading is the first of the six
sections the scan prints (was: the first of `drill|collect`), and both question
lines are printed by PRD, id and title; leg 6 no longer re-asserts leg 5's
empty board — it flips `sup` and `old` to `open` one at a time and watches the
count go to 1, so the `CLOSED` exclusion is proved by the count *moving*, not
by an absence.

30 checks, 0 failures.

### The boxes are falsifiable

Each was mutation-tested against a copy of `resources/` under a scratch dir,
never this tree:

| mutation | fixture |
|---|---|
| `len(pending) >= 2` → `>= 99` (the gate) | 5 fail, first `FAIL: claim exits 1 (got 0)` |
| `len(drill) >= 2` → `>= 999` (the section) | 6 fail, `FAIL: drill not first — first section is: waiting on you — 2` |
| `superseded` out of `CLOSED` | 12 fail, `FAIL: header says asking 2 over 2 PRDs` |
| the round file ignored (no `out` mark) | 5 fail, `FAIL: one's question marked · out` |

## The defect in my footprint — `references/parts/loop.md`

`the-board-runs-itself/the-loop-is-commands` pins two properties of this file,
and pass one broke both:

- **the step table gained a ninth row.** That harness counts `^| [1-8] ` to
  assert the loop still has eight steps. The step-2 trigger table's row
  `| 1 | that question, put as today |` matched it — got 9, want 8. The three
  rows are now spelled `none` / `one` / `two or more`, which is the same table
  ("verbatim in meaning", spec03 box 1) and cannot collide with a step number.
- **the file went to 173 lines against a cap of 170.** Reflowed the three
  paragraphs pass one had added to (steps 1, 2 and 8) back to 170 with no
  sentence dropped.

That harness after the fix: 60 checks, 60 pass, 0 fail.

## New — `probe/verify.sh`

This PRD had no harness, and the board's gate (`doctor.sh --harnesses`) runs
`probe/verify.sh` per PRD. Written: `## Done when` as a harness — the fixture's
legs, the four manual files' claims (including the three trigger-table rows and
the `asking N — drill first` refusal in `drill.md` and `guard.md`), the three
modules compiling, and `questions.py check` silent on the real board. Pinned at
25 checks and ending on `[ "$FAIL" -eq 0 ]`, as the census in
`the-gate-runs-the-harnesses` requires. 25 checks, 25 pass. Doctor now counts
43 harnesses.

## Verify output

| spec | boxes | block |
|---|---|---|
| spec01 — the count and the section | 5/5 | `real board: rounds clean` · `probe done · failures: 0` · `spec01 verify done`, exit 0 |
| spec02 — the claim gate | 3/3 | `probe done · failures: 0` · `spec02 verify done`, exit 0 |
| spec03 — the manual | 5/5 | `loop.md says the count` · `drill.md: two entry points` · `round.md: Asked is what the gate reads` · `guard.md names the refusal` · `questions check silent` · `spec03 verify done`, exit 0 |

Repo gate, `bash resources/doctor.sh`: `pearde: every part this repo owns
checks out.` (the `index` and `origin` rows were red when this run started —
another implementer's `orphans.py` row and the derived/requested split — and
both went green under me without my touching either).

Neighbour harnesses: every `verify.sh` on this board that names
`questions.py`, `plan.py` or `transitions.py` and does not start the view
service was run — 19 of them, all green but the one below.

## Outside the footprint — for the orchestrator, not fixed here

- **`the-board-runs-itself/transitions-are-commands/probe/verify.sh` is red on
  this PRD's own contract: 74 checks, 66 pass, 8 fail.** Its `fixture.py`
  builds a board carrying four unanswered questions (`asking` Q1–Q3,
  `badround` Q1) and no round file, then asserts `claim next impl-1` succeeds
  once its `needs:` clears. Under the drill gate that claim is now refused —
  correctly: an unput frontier of four dispatches nothing. The eight reds are
  that claim and the seven assertions downstream of it (the progress line, the
  numstat, the `.transitions.jsonl` row count). The fix is one line in that
  PRD's fixture — write `.pearde/.state/round.md` with the four titles under
  `## Asked`, or claim with `--force` — and it is that PRD's file, so it stays
  as it is here. Anyone running `doctor --harnesses` before it lands sees this
  one red.
- **`references/parts/order.md` does not know about the drill band.** Its
  pressure-order table runs 0–6 with `to collect` at the head, and its prose
  says "`plan.py scan` prints its five sections in this order" — the scan now
  prints six, drill first, and `loop.md` (in this footprint) names drill at the
  head of the order while `order.md` (not in it) does not. One band row and one
  numeral. The PRD's where-it-lands table did not name the file, so it is
  reported rather than edited.
- **`probe/drill-fixture.sh`** is pass one's probe, still green, but it writes
  to a hard-coded `/tmp/drill-fg` rather than a path it is handed.
  `spec-fixture.sh` supersedes it; kept as the record of pass one.
- **`questions.py list`'s `answered` column still counts `## Answers`
  sections, not answers** — pre-existing, unchanged, and named in the analyst's
  report before mine.

## Knowledge

Nothing was learned outside this repo — no web source, no library this tree
does not hold — so there is nothing to `remember` or `conclude`.

## Scores

complexity: 23
blast-radius: mid
workflow: probe-then-spec
