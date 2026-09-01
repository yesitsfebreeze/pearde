---
complexity: 18
footprint:
  - resources/board/plan.py
---

# spec01 — `pearde next` answers the step, the decision and the command

`cmd_next` in `resources/board/plan.py`, registered as `COMMANDS["next"]` and
reachable as `pearde next [board]` and `python3 resources/board/plan.py next
[board]`. It reads and never writes: no state moves, no round file written.
In one call it prints the loop step the board is on, the decision that step
asks the orchestrator to make, and the exact command to run. The step
selection reads the same bands `cmd_scan` prints — `pressure_bands` over
`compute_plan` — plus `drill_questions`, so `next` can never disagree with
`scan` about what the board is doing. A `## Owed` line in
`.pearde/.state/round.md` stands first when one is written. The first-line
gate checks — no `.pearde/settings.md`, a master with no `name:` — come out
as step 1.

The precedence order, each state printing the step the loop assigns it:
unput drill questions → step 2 (the drill-round wording when two or more
stand, the one-standing-is-not-a-gate wording over one); the collect band →
step 6; `refine` in the waiting-on-you band → step 3; `failed` → step 6 with
`pearde release <prd> failed`; the ready band → step 4 (state `open`) or
step 5 (state `specced`), with `pearde claim`/`pearde brief` naming the
actual PRD rel and the dispatch target `pearde-analyst`/`pearde-implementer`;
the gated band with its `dispatchable` reason (the `workflow:` gate naming
itself the one refusal the round clears); in-flight-only → a wait line
pointing at step 6; the board blocked on a person → step 8 with the step-7
knowledge query first; nothing at all → step 8, hand back `DRAINED`.

What already stands: the whole of this spec is implemented in the tree,
uncommitted, with `pressure_bands` extracted from `cmd_scan` by pass one of
this PRD and `cmd_next` built on it. Verified on the live board (gated leaf
case, owed line), on fixture boards for ready/collect/refine/failed/drill/
gated/flight/drained/first-run, and on a master fixture whose ready queue
spans a member (`@fix/<prd>` in the printed command). What remains is the
acceptance boxes below, ticked by a check that can fail.

## Acceptance

- [x] `python3 resources/board/plan.py next` on a fixture board with one
  `state: open` PRD prints a line starting `step 4 · spec ahead`, a
  `decision:` line, and a `pearde claim <rel> <worker>` line naming that PRD
  — fixture run: `PASS box1-step4 / box1-decision / box1-claim`
- [x] the same fixture with the PRD `state: specced` and one closed acceptance
  box prints `step 5 · implement` and `→ dispatch as pearde-implementer`
  — fixture run: `PASS box2-step5 / box2-dispatch`
- [x] a fixture with two PRDs carrying unanswered `### Qn` questions prints
  `step 2 · answer` with the drill-round wording and both question titles,
  and never a ready/claim line
  — fixture run: `PASS box3-step2 / box3-drill / box3-title1 / box3-title2 /
  box3-noclaim`
- [x] a fixture whose only live PRD is claimed with every acceptance box
  closed under `## Acceptance` prints `step 6 · collect` and
  `pearde collect <rel>` — fixture run: `PASS box4-step6 / box4-cmd`
- [x] a fixture with nothing live and nothing parked prints
  `step 8 · hand back` and `DRAINED` — fixture run: `PASS box5-step8 /
  box5-drained`
- [x] a board with no `.pearde/settings.md` prints step 1 and `pearde init`;
  a master with members and no `name:` prints the ask-the-user decision
  — fixture runs: `PASS box6a-step1 / box6a-init / box6b-master / box6b-ask`
- [x] `python3 resources/pearde.py next --help` exits 0 and prints the
  docstring's first line, and `pearde help` lists `next` — run:
  `pearde next  the loop step the round is on — its decision…`, exit 0;
  `pearde help` line 53 lists it
- [x] a round file carrying an `## Owed` line prints `owed: <first line>`
  before the step block — fixture run: `PASS box8-owed / box8-order`

## Verify and Proof

```sh
python3 resources/board/plan.py next            # live board: a step block, exit 0
python3 resources/pearde.py next --help          # docstring line, exit 0
python3 resources/index.py check                 # silent, exit 0
```

The fixtures were built at run time under `mktemp -d` (never under
`.pearde/`) and removed; re-creating them is five `printf` blocks — the
shapes are recorded in this spec's acceptance boxes.