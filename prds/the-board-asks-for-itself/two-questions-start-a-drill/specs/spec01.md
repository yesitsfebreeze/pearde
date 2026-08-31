---
complexity: 10
footprint:
  - resources/questions.py
  - resources/board/plan.py
---

# spec01 — the count: `unanswered` and the scan's drill section

Already stands: `questions.unanswered(board)` in `resources/questions.py` —
one reader for the frontier, returning `[(rel, qid, title)]`: a `### Qn:` head
under `## Questions` with no matching `**Qn**` under `## Answers`, on any PRD
whose state is not `CLOSED` (`superseded` joined the terminal set for the same
reason `done` is there). `rows()` yields that count as the `open` column of
`questions.py list`. In `resources/board/plan.py`, `drill_questions(board)`
wraps it with the round file — `.pearde/.state/round.md` `## Asked`, matched by
normalized title, lenient toward `out` — and `cmd_scan` prints the count in the
header line (`asking N over M PRDs`) and, when the count is over one, a
**drill** section standing first, above *collect*, one line per question by PRD,
id and title, `· out` beside the ones the round file already lists. Zero prints
nothing; one question prints the count and no section.

## Acceptance

- [x] on a fixture board with two `question` PRDs holding one drill-format
      question each, `plan.py scan` prints `asking 2 over 2 PRDs` in the
      header and a `drill — asking 2 over 2 PRDs` section above every other
      section
- [x] with the question title written into the fixture round file's
      `## Asked`, the same scan marks the question lines `· out`
- [x] one question standing: the header count prints, no `drill` line does
- [x] zero questions: neither the header count nor the section prints
- [x] a `superseded` PRD with an unanswered round counts zero (it is in
      `CLOSED`, same as `done`)

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 -m py_compile resources/questions.py
python3 resources/questions.py check "$(pwd)/.pearde" && echo "real board: rounds clean"
CODE="$PWD" bash -e -o pipefail "$PWD/.pearde/prds/the-board-asks-for-itself/two-questions-start-a-drill/probe/spec-fixture.sh" /tmp/spec01-fixture
echo "spec01 verify done"
```

The probe script the last line runs is `spec-fixture.sh` beside this spec's
PRD: it rebuilds the fixture board under `/tmp/spec01-fixture` (`one` + `two`
question PRDs, `other` open, `old` done, `sup` superseded), runs the legs
above against this repo's `plan.py` and `questions.py`, prints one `OK` per
box, and exits nonzero with `FAIL: …` on the first box that did not hold. The
implementer runs it with its own temp path in place of `/tmp/spec01-fixture`.
`probe done · failures: 0` is the passing line.