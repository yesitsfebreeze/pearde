---
complexity: 8
footprint:
  - resources/questions.py
---

# spec02 — the drill count reads `## Answers` the same way `answer` does

`questions.py`'s `unanswered()` — the drill count `scan`, `list` and
`gate_claim` all read — matched an answered `**Qn**` line with its own
regex, looser than `resources/board/prdfile.py`'s `answers_of` (the reader
`transitions.py`'s `answered_of` gates `answer` and `release` on). A padded
line like `** Q1 **` matched the loose reader and not the strict one, so
`scan` printed `questions 0 open` while `answer`/`release` still refused the
same PRD — the exact shape of the incident the PRD names (`address-form-
ihr-euch`, `questions 0 open · 1 answered` and still listed under waiting on
you). `unanswered()` now builds its answered set from `planlib.answers_of`
— the one reader `answer` and `release` already use — so the drill count and
the gate cannot disagree on what counts as answered: there is one reader,
not two.

The dead `ANSWER_ID_RE` this replaced is removed rather than left unused.

## Acceptance

- [x] `questions.py list` and `release <prd> open --dry` agree on whether a
  question is answered, for an answer written in the loose padded-bold shape
  that previously fooled only the drill count
- [x] a normally-written answer (`**Q1** — …`) is still read as answered by
  both
- [x] `questions.py check` stays clean on a board with no malformed passes
  (the example board, `resources/board/example`)

## Verify and Proof

```sh
bash .pearde/prds/every-question-answered-and-the-prd-stays-in-question/probe/reproduce.sh .
python3 resources/questions.py check /Users/feb/dev/infra/pearde/.pearde
```
