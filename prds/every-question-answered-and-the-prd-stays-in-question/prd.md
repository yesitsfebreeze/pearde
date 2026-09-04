---
state: done
origin: requested
priority: 78
complexity: 18
blast-radius: mid
repo: pearde
footprint:
  - resources/board/transitions.py
  - resources/questions.py
---

# every-question-answered-and-the-prd-stays-in-question — a `question` PRD whose answers were written by hand has no command that will move it

When this is done, a PRD in `question` whose `## Answers` block already
satisfies every question can be moved out of `question` by a command. Today
neither verb accepts it: `answer` refuses because nothing is owed, `release`
refuses because `question` is not one of its source states, and the only
remaining move is the hand-edited `state:` the guard exists to forbid.

## The consequence, named

On 2026-09-03, on the manola board, `address-form-ihr-euch` — priority 9, the
node every dictionary-touching PRD waited behind — sat in `state: question`
with both of its questions answered. `scan` agreed the work was unblocked and
printed `questions 0 open · 1 answered`, and still listed the PRD under
**waiting on you**. Measured, in order:

```
$ pearde answer address-form-ihr-euch Q2 "<the answer>"
pearde answer: refused — answer: Q2 is already answered

$ pearde answer address-form-ihr-euch Q1 "<the answer>"
pearde answer: refused — answer: Q1 is already answered

$ pearde release address-form-ihr-euch open --dry
pearde release: refused — release: address-form-ihr-euch is `question` —
analyzing → refine|question|open, claimed → blocked|failed
```

Three things make it the tool's defect rather than a slip:

- **`question` → `open` exists in exactly one place and it is unreachable.**
  `transitions.py:792` moves the state only on the call that answers the *last
  owed* question. A PRD that arrives at zero-owed by any other route — a worker
  writing the `## Answers` block directly, a merge, a hand-authored PRD — can
  never take that branch again, because `answer` guards on `qid not in
  questions_of(prd)` and refuses a second answer to the same id.
- **`release` is the general escape hatch and it does not list `question` as a
  source.** Its own refusal text enumerates `analyzing` and `claimed` only, so
  the state with no exit is the one state a person is most likely to be looking
  at — it is the state that means *the board is waiting for a human*.
- **The remaining move is the one the house rules forbid.** `AGENTS.md` and the
  role skill both say state is set by the transition commands and never
  hand-edited, and the guard refuses a hand-written `state:`. So a correctly
  behaved operator is stuck, and the incorrect one edits frontmatter — which is
  how a real board ends up with states nothing wrote.

The instance recovered on its own roughly forty minutes later, which is worse
rather than better as evidence: whatever moved it is not a documented verb, so
the exit is neither reachable on demand nor reproducible.

## Why the empty passes matter to the same fix

`doctor` on that board reports `questions broken · 61 passs the user cannot act
on`, every one of the form:

```
accessibility: `## Questions` with nothing under it — a heading that says a
pass exists when none does
accessibility: `## Answers` with nothing under it — unanswered reads the same
as unasked
```

Sixty-one of them, mostly on `done` PRDs. That is the same seam from the other
side: the question block's shape is not held to anything after the PRD stops
being asked about, so `questions_of()` and the `## Answers` text can disagree
and nothing notices. A fix that only adds a `release` source state leaves the
disagreement in place.

## Constraints

- **Do not make `answer` idempotent by letting it re-answer.** An answer is a
  record; overwriting one silently is worse than the stall. If re-answering is
  the chosen route it prints what it is replacing and says so in the row.
- **Whatever moves the state writes a `.transitions.jsonl` row.** The reason
  this instance is hard to describe is that its recovery wrote no legible one.
- The board's own guard against hand-written `state:` stays exactly as strict.
- Both verbs keep `--dry` real, per `an-unknown-flag-refuses`.

## Pointers

- `resources/board/transitions.py:772-800` — `cmd_answer`, the guard and the
  single `question` → `open` branch
- `resources/board/transitions.py` — `release`'s source-state table and its
  refusal text
- `resources/questions.py` — `questions_of()`, and the empty-block check
  `doctor` surfaces
- the instance: `manola` board, `pearde/prds/address-form-ihr-euch/prd.md`,
  two `## Answers` entries per question id, written by a worker rather than by
  `answer`

## Acceptance

- [x] a PRD in `question` with nothing owed can be moved to `open` by a documented command, and the command is named in `references/parts/handles.md`
- [x] the move writes a `.transitions.jsonl` row naming the from-state, the to-state and why it was allowed
- [x] `answer` still refuses to overwrite an existing answer silently
- [x] `questions_of()` and the `## Answers` block cannot disagree without `questions check` saying so
- [x] `--dry` on the new path prints the transition and writes nothing
- [x] a probe reproduces the stall from a pristine tree before the fix and fails after it

## Questions

### Q1: How a piece of work leaves the waiting-for-a-person state once nothing is left to answer

A piece of work is parked waiting on a person, they have answered everything it
asked, and it stays parked. One existing command would cover this with one more
line; a new one would name it honestly as a repair. Which should it be?

1. **Extend the letting-go command** — the one people already reach for learns this case, and nothing new has to be learned. (recommended)
2. **A repair command of its own** — a separate word, which only accepts work whose questions are all satisfied and explains itself when they are not.
3. **A re-check on the answering command** — it re-reads the answers on record and moves the work on if nothing is owed.

<!-- for the board: option 1 is one row in release's source-state table (question joins analyzing); option 2 is a new verb plus a handles.md row; option 3 keeps the move inside cmd_answer at transitions.py:792 but needs a flag that does not re-answer -->

## Answers

### Q1: How a piece of work leaves the waiting-for-a-person state once nothing is left to answer

**Extend the letting-go command** — the one people already reach for learns this case, so nothing new has to be learned. (recommended)

## Blocked

**2026-09-03 19:20 — the lane will not rebase**

`lane/every-question-answered-and-the-prd-stays-in-question` does not land on `session/s34612`; 1 file(s) disagree:

- `resources/questions.py`

Nothing is lost: the worker's commits are on `lane/every-question-answered-and-the-prd-stays-in-question` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-question-answered-and-the-prd-stays-in-question`.

**2026-09-03 21:00 — the lane will not rebase**

`lane/every-question-answered-and-the-prd-stays-in-question` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/questions.py`

Nothing is lost: the worker's commits are on `lane/every-question-answered-and-the-prd-stays-in-question` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-question-answered-and-the-prd-stays-in-question`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/every-question-answered-and-the-prd-stays-in-question` does not land on `session/s62223`; 1 file(s) disagree:

- `resources/questions.py`

Nothing is lost: the worker's commits are on `lane/every-question-answered-and-the-prd-stays-in-question` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-question-answered-and-the-prd-stays-in-question`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/every-question-answered-and-the-prd-stays-in-question` does not land on `session/s62223`; 1 file(s) disagree:

- `resources/questions.py`

Nothing is lost: the worker's commits are on `lane/every-question-answered-and-the-prd-stays-in-question` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-question-answered-and-the-prd-stays-in-question`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/every-question-answered-and-the-prd-stays-in-question` does not land on `session/s62223`; 1 file(s) disagree:

- `resources/questions.py`

Nothing is lost: the worker's commits are on `lane/every-question-answered-and-the-prd-stays-in-question` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-question-answered-and-the-prd-stays-in-question`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/every-question-answered-and-the-prd-stays-in-question` does not land on `session/s85810`; 1 file(s) disagree:

- `resources/questions.py`

Nothing is lost: the worker's commits are on `lane/every-question-answered-and-the-prd-stays-in-question` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-question-answered-and-the-prd-stays-in-question`.

**2026-09-04 02:54 — the lane will not rebase**

`lane/every-question-answered-and-the-prd-stays-in-question` does not land on `session/s85810`; 1 file(s) disagree:

- `resources/questions.py`

Nothing is lost: the worker's commits are on `lane/every-question-answered-and-the-prd-stays-in-question` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-question-answered-and-the-prd-stays-in-question`.

## Report

spec01: exit 0
  ok   — release asking open moved a hand-answered question PRD to open
  ok   — .transitions.jsonl row names why the move was allowed
  ok   — release still refuses when a question is owed — pearde release: refused — answer: unanswered — Q1
  ok   — the drill count and release agree — both call the padded-bold answer unread
  ok   — questions check names the answer shape the gate refuses
probe: PASS

spec02: exit 0
  ok   — release asking open moved a hand-answered question PRD to open
  ok   — .transitions.jsonl row names why the move was allowed
  ok   — release still refuses when a question is owed — pearde release: refused — answer: unanswered — Q1
  ok   — the drill count and release agree — both call the padded-bold answer unread
  ok   — questions check names the answer shape the gate refuses
probe: PASS
