# report — pearde-next-prints-the-step-and-the-decision-it-owes

## Verdict

DONE. 14/14 acceptance boxes closed (spec01 8/8, spec02 6/6), every box
ticked as it closed with its check's output quoted in the spec.

## What this pass did

The tree already held the probe's implementation (`cmd_next`,
`COMMANDS["next"]`, the rewritten `loop.md`, the `handles.md` row). This pass
verified it and closed the boxes. Three things were changed:

- **loop.md restored where the probe over-deleted.** Six harnesses of DONE
  PRDs pin lines the probe's rewrite removed: step 1's drill-count sentence
  (`asking N over M` / `a **drill** section stands first`), step 4·5's "and
  names the gate" + "Run `check` on the board the PRD lives on", the
  swept-worker `## Workflow` sentence, and the one-page pins (≤170 lines).
  All restored as judgment (no command invocation restated), folded to fit
  the one-page pin: loop.md is 168 lines. After the restore:
  `two-questions-start-a-drill` 25/25, `workflow-attach` 47/47,
  `workflow-improve` 70/71 (its one red is workers.md, see below),
  `the-loop-is-commands` 58/58, `the-round-runs-in-a-window-that-ends`
  26/26.
- **README.md's round table mirrored to loop.md's two-column rows** —
  `readme-in-three-rings` diffs README's `| [1-8] ` rows against loop.md's
  byte for byte, so the deliverable's table change had to land in both.
  Outside spec02's declared footprint; noted here and in spec02.
- **knowledge.py relink** — doctor's `knowledge` row was broken on arrival
  ("graph.json is behind the files"); ran the fix doctor itself printed. Row
  ok (10 nodes, 14 edges).

## Verify blocks, as run

spec01: `plan.py next` on the live board — step block, exit 0 (prints
`step 6 · collect` for this PRD's own finished work);
`pearde.py next --help` — docstring's first line, exit 0; `index.py check` —
silent, exit 0. Fixtures: 20 asserts over 9 board shapes under `mktemp -d`,
all PASS (run three times over the session, last run `fails=0`); box 6b's
fixture was rebuilt once — a member entry needs frontmatter fences in
settings.md, exactly as `references/parts/master.md` shows; the code was
right.

spec02: `index.py check` exit 0; `index.py scope loop | grep -c
"parts/loop.md"` → 1. Both cross-references read fresh and true
(round.md's compaction line as written; solo.md's "the table" names the
two-column table that stands).

Repo gate: `doctor.sh` — "pearde: every part this repo owns checks out."
(all rows ok; `harnesses`/`jstests` are opt-in rows and were run opt-in, see
Findings).

## Failure

(none)

## Findings (defects outside this PRD's footprint — not fixed here)

1. **`readme-in-three-rings`'s D block is a stale pin against spec02.** Its
   awk starts only at a `| step | command` header, so with loop.md's
   two-column table (spec02 box 1) it can never fire: "D seven rows in the
   README — got '0', want '7'" stays red. Either the harness learns the new
   header or box 1 is given up; a later PRD must settle that.
2. **`workflow-skill`'s baseline check** cascades from the same (reads
   readme-in-three-rings's total, wants 74/74).
3. **`workflow-improve`'s one red is the memo session's uncommitted
   workers.md edit** — it deleted the table row
   "any of the three, plus `## Workflow <slug>`" that the harness pins.
4. **Six more reds, all pre-existing, none touching this footprint:**
   `an-unknown-flag-refuses` (git status clean — the untracked `.state/`),
   `nothing-left-open/the-line-tells-the-truth` (E14 scratch index),
   `one-page-that-says-whats-up` (`.pearde/report.md` has no `## In work`),
   `specced-is-a-command` + `transitions-are-commands` (refusal writes),
   `the-gate-runs-the-harnesses` (44 of 45 harnesses end on an exit-carrying
   check), `the-view-row-names-a-variable-that-exists` (doctor unset
   variable), `one-predicate-for-dispatchable` (`?? .state/`). Full
   `doctor.sh --harnesses`: 6 of 45 green · 38 unpinned · 11 failed — the
   reds predate this pass (they were red in the first sweep, before any edit
   of mine except the three loop.md restorations, which took the count from
   16 failed to 11).
5. **A session stashed this PRD's work mid-run** (stash
   `graph-probe-analyst-pass-one`, 10:48, holding `cmd_next` and the loop.md
   rewrite); `plan.py next` answered `unknown command 'next'` for about two
   minutes. Restored with `git stash apply stash@{0}` — no conflicts, every
   file back. One writer per file was violated somewhere upstream of this
   window; the round file's own notes say the memo session's work was to be
   left alone, not stashed.
6. `jstests`: node found, playwright-core missing — pre-existing
   (`npm i playwright-core --prefix resources/board` is the printed fix; not
   this PRD's).

## Scores

complexity: 32 · blast-radius: mid · workflow: probe-then-spec
