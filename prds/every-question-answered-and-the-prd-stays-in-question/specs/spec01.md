---
complexity: 10
footprint:
  - resources/board/transitions.py
---

# spec01 — `release` moves a fully-answered `question` PRD to `open`, and says why

`question` joins `analyzing` and `claimed` as a `release` source state, so a
PRD whose `## Answers` block was written by hand — a worker, a merge, a
hand-authored PRD — has a documented way out once nothing is left owed. The
move routes through the same gate `answer` already runs on its own
last-question branch (`gate_answered`, via `edge_of`'s existing
`frm.lower() in qlib.WAITING` case), so a question still open still refuses
the release — the fix widens who can reach the gate, not what the gate lets
through. `answer`'s own refusal to overwrite an existing answer is untouched.
The `.transitions.jsonl` row this edge writes now carries a `why` — the same
row `record()` already appends for every move, `"why": "every question
answered"` added only when the edge is this one, since the `(from, to)` pair
alone (`question → open`) does not say why it was let through.

Already stands: `cmd_answer`'s own `question → open` branch, `edge_of`'s
routing of any `WAITING`-state source through the `answer` edge, and
`gate_answered`'s owed-check — none of it moved. This spec only widens
`cmd_release`'s own `allowed` table and adds the `why` field to `record()`.

`release` is already named in `references/parts/handles.md` — no new row.

## Acceptance

- [x] `release <question-prd> open` moves a PRD whose questions are all
  answered, when the `## Answers` block was written directly rather than by
  `answer`
- [x] `release <question-prd> open` still refuses when a question is left
  unanswered, with the same `answer: unanswered — Qn` message `gate_answered`
  already raises
- [x] `answer` still refuses to re-answer an already-answered question
- [x] the `.transitions.jsonl` row for this move carries `"why": "every
  question answered"`
- [x] `release <question-prd> open --dry` prints the move and writes nothing

## Verify and Proof

```sh
bash .pearde/prds/every-question-answered-and-the-prd-stays-in-question/probe/reproduce.sh .
```
