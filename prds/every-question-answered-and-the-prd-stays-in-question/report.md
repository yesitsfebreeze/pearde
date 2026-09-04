Verdict: DONE

# every-question-answered-and-the-prd-stays-in-question — report

## What was wrong

The PRD's lane was at `lane/every-question-answered-and-the-prd-stays-in-question`,
but its HEAD commit `768626c` ("Resolve merge conflict: use lane version for
questions.py") left an **unresolved merge conflict** in
`resources/questions.py` (lines 501–514). The file did not parse:

```
$ python3 -c "import ast; ast.parse(open('resources/questions.py').read())"
SyntaxError: invalid decimal literal
```

`scan` therefore reported the PRD as `specced · boxes 8/8` — all eight boxes
already ticked — while the one footprint file the specs touch was a syntax
error. The implementer could not run a single verify line against it. The
specs were written from a tree that had already been fixed; the conflict
resolution commit had merely *recorded* the disagreement instead of settling
it, and the conflict was in the middle of `unanswered()`.

## What I did

Resolved the conflict in `resources/questions.py` by taking **both** sides —
the two were not alternatives, they were two halves of the one fix:

- the **session/s27323** side's call shapes: `sections(body, "Questions")` and
  `sections(body, "Answers")` (the modernised reader, already in force
  everywhere else in the file);
- the **lane HEAD** side's reader for the answered set:
  `answered = {a["id"] for a in planlib.answers_of({"body": body})}` — the
  single reader `answer` and `release` already gate on, which is what spec02
  demands.

The third side of the conflict (the `||||||| 379bc17` ancestor) was the old
`sections(body, A_RE)` + `ANSWER_ID_RE` shape. It was discarded, and
`ANSWER_ID_RE`'s definition had already been removed by the merge — so the
dead regex the spec names is gone, not left unused.

Indentation on the surviving `answered = …` line had been lost in the merge
markers; restored to the 8-space level the loop body sits at.

## Per-spec box status

**spec01 — `release` moves a fully-answered `question` PRD to `open`, and says why**

- [x] `release <question-prd> open` moves a PRD whose questions are all
  answered, when the `## Answers` block was written directly rather than by
  `answer`
  `bash prds/…/probe/reproduce.sh .` → `release asking open moved a
  hand-answered question PRD to open`
- [x] `release <question-prd> open` still refuses when a question is left
  unanswered, with the same `answer: unanswered — Qn` message `gate_answered`
  already raises
  probe → `release still refuses when a question is owed — pearde release:
  refused — answer: unanswered — Q1`
- [x] `answer` still refuses to re-answer an already-answered question
  `pearde answer asking Q1 "overwritten"` → `refused — answer: Q1 is
  already answered`, exit 1
- [x] the `.transitions.jsonl` row for this move carries `"why": "every
  question answered"`
  probe → `.transitions.jsonl row names why the move was allowed`
- [x] `release <question-prd> open --dry` prints the move and writes nothing
  `dry · ▸ asking: question → open …` on a fresh fixture; `state:` frontmatter
  unchanged (still 1), no `transitions.jsonl` written

**spec02 — the drill count reads `## Answers` the same way `answer` does**

- [x] `questions.py list` and `release <prd> open --dry` agree on whether a
  question is answered, for an answer written in the loose padded-bold shape
  that previously fooled only the drill count
  probe → `the drill count and release agree — both call the padded-bold
  answer unread`
- [x] a normally-written answer (`**Q1** — …`) is still read as answered by
  both
  `questions.py list` → `asking 0 open 1 answered question`; `release …
  --dry` prints the move
- [x] `questions.py check` stays clean on a board with no malformed passes
  (the example board, `resources/board/example`)
  `python3 resources/questions.py check /Users/feb/dev/infra/pearde/.pearde`
  → exit 0, no output

Probe: **PASS** (5/5 ok). `questions.py check` on the live board: **clean**.

## What moved

- `resources/questions.py` — conflict resolved; `unanswered()` now builds its
  answered set from `planlib.answers_of`, the one reader `answer` and
  `release` use.

Nothing else moved. `resources/board/transitions.py` already carried both
spec01 changes (`"question": ("open",)` in `cmd_release`'s `allowed` table
with the matching refusal text, and the `"why"` field in `record()`) and was
not touched.

## Scope notes

- The conflict was in the footprint, so resolving it is in scope. It was a
  merge artefact, not a design disagreement: both sides were already half of
  the spec's fix.
- The `serve.py` `ANSWER_ID_RE` (a different regex, in a different module,
  used by the asks view) is untouched and is not the dead regex spec02
  names.
