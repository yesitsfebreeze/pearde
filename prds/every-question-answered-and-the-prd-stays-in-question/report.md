Verdict: DONE

# every-question-answered-and-the-prd-stays-in-question — implementer report

Lane `.pearde/.lanes/every-question-answered-and-the-prd-stays-in-question`,
branch `lane/every-question-answered-and-the-prd-stays-in-question`,
2 files changed, 48 insertions, 31 deletions, uncommitted.

Pass one (the probe's code, already in the tree when this run started)
carried spec01 whole and spec02's `unanswered()` rewrite. Pass two ran every
verify block against it, reproduced the stall from a pristine copy of the
tree, closed the one PRD acceptance box neither spec covered (`questions
check` was silent on the shape the gate refuses), and rewrapped one
docstring line pass one left at 98 columns.

## Spec boxes

### spec01 — `release` moves a fully-answered `question` PRD to `open`

All five boxes stand, all five re-run this pass. Verify block:
`bash .../probe/reproduce.sh <lane>` ->

```
  ok   — release asking open moved a hand-answered question PRD to open
  ok   — .transitions.jsonl row names why the move was allowed
  ok   — release still refuses when a question is owed — pearde release: refused — answer: unanswered — Q1
  ok   — the drill count and release agree — both call the padded-bold answer unread
  ok   — questions check names the answer shape the gate refuses
probe: PASS
```

The real move, on a fresh example board:

```
$ pearde release asking open --board <ex>/.pearde
▸ asking: question → open · done 2/8 · 15% · open 4/8 · 50% · ready 2 · blocked 4 · collect 1 @1 workers · pass file owed · as engineer
$ cat <ex>/.pearde/.state/transitions.jsonl
{"calls": null, "from": "question", "prd": "asking", "reads": null, "refused": null,
 "t": "2026-09-03T19:02:54", "to": "open", "tokens": null, "why": "every question answered"}
```

`--dry` on the same edge, and the directory after it:

```
$ pearde release asking open --board <ex>/.pearde --dry
dry · ▸ asking: question → open · done 2/8 · 15% · … · as engineer
  would write: .pearde/prds/asking/prd.md · .pearde/.state/transitions.jsonl
$ ls <ex>/.pearde/.state/
parse-cache.json          # no transitions.jsonl — nothing was written
```

`answer` unchanged and still refusing:

```
$ pearde answer asking Q1 "second answer" --board <ex>/.pearde
pearde answer: refused — answer: Q1 is already answered
```

### spec02 — the drill count reads `## Answers` the same way `answer` does

All three boxes stand. The same probe covers boxes 1 and 2; box 3:

```
$ python3 resources/questions.py check <fresh example board>/.pearde
$ echo $?
0
```

## What pass two added

PRD acceptance box 4 — "`questions_of()` and the `## Answers` block cannot
disagree without `questions check` saying so" — did not hold after pass one.
`unanswered()` had been pointed at `planlib.answers_of`, so the drill count
and the gate agreed; but `check`'s own accepted-shape pattern in
`resources/questions.py` was a *third* reader, looser than both:

```python
ANSWER_OK_RE = re.compile(r"^\s*\*\*\s*(Q?\d+[a-z]?)\s*\*\*", re.M)
```

The `\s*` inside the bold accepts `** Q1 **`, which `plan.py`'s
`ANSWER_LINE_RE` (`^\s*\*\*(Q?\d+[a-z]?)\*\*`) refuses. So a padded answer
was called fine by `check`, read as unanswered by `unanswered()` and refused
by `release` — a disagreement that said nothing, which is what the box
forbids. `ANSWER_OK_RE` is deleted; `unread_answers()` now builds its
accepted set by matching `planlib.ANSWER_LINE_RE` line by line — the reader
`answer` and `release` already gate on — so there is one accepted shape on
the board, not three. `ANSWER_NEARMISS_RE` gained one alternative (`|\*\*`)
so the padded shape is reported rather than merely uncounted; a well-formed
line is filtered out by the `q not in ok` test that was already there.
Measured:

```
$ python3 resources/questions.py check <board holding `** Q1 **`>
asking: Q1 is answered in a shape no reader counts — the id closes its own
bold, `**Q1** — the decision`, and the title comes after it
$ echo $?
1
$ python3 resources/questions.py check <board holding `**Q1** — …`>
$ echo $?
0
```

One assertion was added to the probe for it — the fifth `ok` line above — so
the new branch has a runnable check and the probe still goes red on the
pristine tree.

## The pristine-tree run (PRD box 6)

`git stash` is refused in a lane this session does not own, so the baseline
is an rsync copy of the lane with both footprint files replaced by their
`HEAD` blobs. Same probe, same command:

```
  FAIL — release asking open refused a fully-answered question PRD — pearde release: refused — release: asking is `question` — analyzing → refine|question|open, claimed → blocked|failed
  ok   — release still refuses when a question is owed — …
  FAIL — the drill count and release still disagree on the padded-bold answer shape
  FAIL — questions check stayed silent on an answer shape release refuses
probe: FAIL
```

Red before, green after, three of the four cases discriminating.

## The gate

`bash resources/doctor.sh` in the lane is row-for-row identical to the run
before this pass's edits: `index broken (5)`, `vault broken`, `origin broken
(40 derived · 8 with no from:)`, `memos broken (43)`, `questions broken (3)`
— all five pre-existing, all outside the footprint. The `questions` three
are `## Answers` with no `## Questions` above it on three board PRDs: that
is `check` working, not this change, and the count did not move (3 before,
3 after).

`--harnesses`: 100 harnesses, 4 green, 62 failed, 541s — a pre-existing
board condition, not this change. The whole suite cannot be re-run against
the baseline copy (harnesses rsync from `git ls-files` and the copy has no
`.git`), so the harnesses that exercise `release`, `answer` or
`questions.py` were run both ways instead:

```
transitions-are-commands       lane 66 pass · 8 fail   baseline 66 pass · 8 fail
two-questions-start-a-drill    lane 23 pass · 2 fail   baseline 23 pass · 2 fail
a-question-in-plain-words      identical output on both trees
a-parked-prd-comes-back        lane 44 pass · 0 fail   baseline 44 pass · 0 fail
the-documented-board-matches   identical failure on both trees
an-unknown-flag-refuses        lane 183/196            baseline 183/196
```

No harness moved. `jstests ok · 49/49`.

`references/parts/states.md` already reads correctly for the new edge — the
`open` row lists `release <prd> open` among the ways it is reached, and the
`question` row already says `answers written → open` — and
`references/parts/handles.md:66` already names `release`, so no doc edit was
owed (spec01 said as much).

## Notes for the board, not fixed here

- **The `answered` column of `questions.py list` is a section count, not an
  answer count.** `rows()` computes `na = sum(1 for _h, t in sections(body,
  A_RE) if t.strip())` — the number of non-empty `## Answers` *blocks* — so a
  PRD with one open question and one malformed answer prints `1 open
  1 answered`, which reads as a contradiction. It is the display shape the
  PRD quotes from the manola incident (`questions 0 open · 1 answered`).
  Pre-existing, outside both specs' boxes, and cosmetic now that the two
  counts which gate anything agree. Reported, not fixed.
- **The PRD's frontmatter `footprint` names `resources/board/questions.py`;
  the file is `resources/questions.py`.** The brief, both specs and the PRD's
  own pointers all say `resources/questions.py`, and that is the file edited.
  Frontmatter is not mine to touch.
- `knowledge.py query "two readers of the same markdown block disagree"` —
  108 hits, none on point (top hit scored 12, on `set -e` in verify blocks).
  Nothing was researched outside the repo, so nothing was written back; the
  finding above is repo-internal and belongs in a memo, not the wiki.

## Health floor

The brief listed no footprint file under the floor. `resources/questions.py`
lost a dead regex and gained a three-line helper (`qid_of`, the id
normalization that had been written inline twice); `transitions.py` gained a
two-line `why` and one rewrapped docstring line. Neither file grew a
responsibility and nothing was split.
