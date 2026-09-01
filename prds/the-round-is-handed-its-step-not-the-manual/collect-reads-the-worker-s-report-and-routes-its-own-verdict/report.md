# report — collect reads the worker's report and routes its own verdict

Verdict: DONE

Implementer pass over the two specs, workflow `probe-then-spec` followed. The
build's pass one (uncommitted, in tree) had already landed both halves; this
run verified them against the specs and the repo's own gate.

## Workflow probe-then-spec

| step | result |
|---|---|
| 1 read-the-contract | prd.md, spec01, spec02, probe/probe_route.py read; every `@` resolved; `git status --short` recorded before the first edit (20 M paths + 1 untracked README under `resources/board/example/memos/` — all pass-one or sibling edits, none mine) |
| 2 capture-the-harness-baseline | 14 harnesses whose inputs the footprint touches baselined into `scratch-baseline/` (counts quoted below); `index.py check` exit 0; `doctor.sh` exit 0, all rows ok |
| 3 attempt-the-build | nothing new to build — probe harness prints `14 passed, 0 failed`, prose edits stand in `workers.md`/`loop.md`/`solo.md`, tool half stands in `collect.py`; no fork hit |
| 4 re-run-the-harnesses | all 14 re-run, same order, same command line: every count equal to baseline; no new harness (`find … verify.sh` still 45) |
| 5 write-the-specs | specs already written; not this run's act. `specced --check --as engineer` over the pair: ok, complexity 30 |

No back-edge taken. No workflow file edited.

### Edits

- spec01's Verify block greps doctor with `grep -q "briefs   ok"` (three
  spaces) — the real row prints `briefs      ok      5 blocks…` (six spaces),
  so the check as spelled can never pass. Replacement:
  `bash resources/doctor.sh 2>&1 | grep -qE "briefs +ok"`. Ran the
  replacement; it passes. The acceptance box itself is honest.

## Harness counts — baseline and re-run, identical

brief-is-printed 104/104 · collect-is-a-command 133/133 ·
collect-keeps-its-word 101/101 · carried-across-layout 7/7 ·
the-loop-is-commands 58/58 · hunks-land-where-they-came-from 47/47 ·
check-crosses-member-boundaries 18/18 · window-that-ends 26/26 ·
too-big-splits-itself 60/60 · workflow-attach 47/47 ·
workflow-improve 70/71 · line-tells-the-truth 85/85 · two-questions 25/25 ·
readme-in-three-rings 71/74. Doctor rows byte-identical at end (statusline
excluded per the atomic).

## Verify output

- spec01 verify block: the `briefs   ok` needle failed as spelled (see
  Edits); the corrected chain passes — loop.md holds no
  "SPECCED → pearde specced" text (0 hits), workers.md names `--report` at
  lines 36/297/326 and keeps the judgment sentences at 305, brief-is-printed
  prints `104/104 checks pass`, doctor prints `briefs      ok`.
- spec02 verify block verbatim: `ROUTE-OK` — probe `14 passed, 0 failed`
  (exit 0), `py_compile resources/board/collect.py` clean.
- Spec boxes ticked one by one as each check ran, quoting output in the box
  line.

## Findings (outside my scope)

1. **workflow-improve harness red, pre-existing and expected**: line 332
   pins `references/parts/workers.md` containing 'any of the three, plus
   `## Workflow <slug>`' — the implementer's verdict-to-command table row
   this PRD's contract deleted (see `git diff` line
   `-| any of the three, plus …`). Per the fails-when row "a needle names a
   sentence the contract deleted", left red at 70/71. Proposed edit for the
   harness's owner: re-aim the doc row to the surviving sentence,
   '`## Workflow <slug>` present in the report' (workers.md line 137), or
   drop the row — the "five actions" row beneath it already covers the rest.
2. **readme-in-three-rings red, pre-existing, unrelated**: 71/74 — "D seven
   rows in the README — got '0' want '7'", "H quickstart.sh exits 0",
   "H …every check passed". Reads README.md and quickstart.sh, none of my
   footprint; baseline red before the first edit.
3. `route_report` refusal message names stdin, not the slug, when a
   `## Scores` slug resolves to nothing (carried over from the pass-one
   report; still open, one line in `collect.py`, not this build's path).
4. No fixture board leaked into `serve.py status` (checked at end: only the
   four real members); `git status --short` lists nothing at the repo root
   and no untracked `prds/<slug>/` except this PRD's own tree.

## What stands vs what was built where

In-place edits to existing footprint files (cannot be staged under `probe/`):
the prose in `workers.md`, `loop.md`, `solo.md` and the `--report` flag plus
verdict routing in `resources/board/collect.py` — all pass one, uncommitted.
Under the PRD's `probe/`: `probe_route.py` (spec02's harness deliverable)
and this run's `scratch-baseline/` outputs. Nothing new was needed from this
run; no repair was asked for.
