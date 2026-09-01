---
complexity: 14
footprint:
  - references/parts/loop.md
  - references/parts/handles.md
---

# spec02 — loop.md keeps the judgment, next holds the step selection

The deliverable rule this PRD carries: `references/parts/loop.md` keeps only
the right-hand column — the judgment a command cannot make. What already
stands, uncommitted in the tree:

- The step table drops the command column: `step | the orchestrator decides`.
  The exact command is `pearde next`'s to print.
- The header says which step the round is on is `pearde next`'s answer, not
  this file's, and that a round running `scan` then `next` needs no more of
  the file for the routine case.
- Step 4·5 loses the `claim`/`brief` gate mechanics (they are brief.py's
  docstring and `next`'s gated line now); it keeps the `wf <slug>?`
  self-clear rule, the check-on-the-board-the-PRD-lives-on rule, `--force`
  as escape hatch, and the whole `specced --route` mechanic.
- Step 3 is rewritten as the decision alone. Step 6 keeps the verdict→command
  mapping (a judgment on the returned line `next` cannot make) and the whole
  workflow-edit discipline; it loses nothing else. Steps 1, 2, 7, 8 keep
  their judgment untouched.
- `references/parts/handles.md` gains a `next` row — `which step the round is
  on` — beside `scan`.

What remains: the acceptance boxes below ticked from a fresh run, plus one
pass over the two cross-references that describe the file's shape
(`@references/parts/round.md`'s "re-read loop.md after a compaction" line and
`@references/parts/solo.md`'s "the table" line) to confirm each still names
something the file holds — round.md's line is true as written (the file still
holds the steps' judgment; a compacted round reads `next` first, the file for
the judgment), solo.md's needs the word checked.

Both cross-references confirmed on the fresh read: round.md's "If the steps
themselves are gone, re-read @references/parts/loop.md — that one file" is
true as written (the file still holds the steps' judgment; `next` holds the
step selection). solo.md's "@references/parts/loop.md is the table" still
names something the file holds — the two-column table stands; a solo round
reading it gets the judgment and `next` gets the step, which is the shape the
PRD's deliverable rule drew.

Run note (this implementer pass): the probe's rewrite had deleted more than
the boxes above pin — step 1's drill-count sentence, step 4·5's "and names
the gate" and check-on-the-board lines, and the swept-worker `## Workflow`
sentence — and six harnesses of DONE PRDs pin those lines
(`two-questions-start-a-drill`, `workflow-attach`, `workflow-improve`,
`the-loop-is-commands` ≤170 lines, `the-round-runs-in-a-window-that-ends`
one-page). Restored as judgment, folded back under the one-page pin
(loop.md now 168 lines), all of them green again. Consequence outside this
spec's footprint: `README.md`'s round table mirrored loop.md's rows, so it
was rewritten to the same two-column shape. `readme-in-three-rings`'s
byte-for-byte row diff stays red — its awk starts at the old
`| step | command` header, which box 1 above forbids; that pin is stale
against this spec and is named in the report, not redefined here.

## Acceptance

- [x] `references/parts/loop.md` step table has two columns (`step`,
  `the orchestrator decides`) and no command column — read: the table is
  `| step | the orchestrator decides |`, eight rows, no command column
- [x] the file's opening block names `pearde next` as the answer to which
  step the round is on — read: "Which step the round is on is `pearde
  next`'s answer, not this file's … a round that runs `scan` then `next`
  needs no more of it for the routine case"
- [x] no step paragraph restates a command invocation that `pearde next`
  prints for that step's situation (claim/brief gate mechanics gone from
  step 4·5) — read: step 4·5 says "the commands are `next`'s to print" and
  keeps only the `wf <slug>?` rule, the board rule, `--force` and
  `specced --route`
- [x] the judgment lines are intact: the step-2 unanswered table, the ASK
  protocol, the step-6 verdict mapping and workflow-edit rules, step 8's
  stop rules — read: the `| unanswered | step 2 is |` table, the
  `ask.md` + hand back `ASK` protocol, `pearde collect <prd> --report …`
  mapping and the `runs` +1 / one-writer / check-before-commit discipline,
  and step 8's "never one per PRD, never a question `## Asked` already
  lists" + DRAINED/BLOCKED handback
- [x] `references/parts/handles.md` carries a `pearde next` row — read:
  "| which step the round is on | `next` — … | `pearde next` |" beside
  `scan`
- [x] `python3 resources/index.py check` exits 0 — every `@`-anchor to
  loop.md from the other parts still resolves — run: silent, exit 0

## Verify and Proof

```sh
python3 resources/index.py check
python3 resources/index.py scope loop | grep -c "parts/loop.md"   # the scope still lists it
```