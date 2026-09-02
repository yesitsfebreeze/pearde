# the-worker-parts-are-rewritten-dense — implementer report

Verdict: DONE

Pass two. The rewrite was already in the lane, uncommitted, as pass one left it.
Nothing was rewritten this pass: every box was re-run against that tree and
ticked as it closed. 15 of 15 across three specs. `prose.py check` exits 0 on
all seven parts; the three committed harnesses hold their `HEAD` baselines; no
backticked token, no `@` link, no table row and no heading present at `HEAD`
went missing.

Diff: `7 files changed, 189 insertions(+), 197 deletions(-)`, no file renamed
or deleted.

## Boxes

| spec | boxes | files |
|---|---|---|
| spec01 | 6/6 | `references/parts/workers.md` |
| spec02 | 5/5 | `workflows.md`, `personas.md` |
| spec03 | 4/4 | `consult.md`, `health.md`, `grammar.md`, `memos.md` |

## Verify output

`spec01`:

```
python3 resources/prose.py check references/parts/workers.md   -> exit 0
brief.check()                                                  -> briefs problems: 0
grep -qF '> fits the build ahead, ...  Then read'              -> ok
grep -qF 'is the belief and the `## Workflow` rows, as above.' -> ok
the-brief-names-the-verdict-line-collect-requires   13 ok · 2 FAIL   (HEAD baseline)
workflows-on-the-board/workflow-improve             70/71 checks pass (HEAD baseline)
```

`spec02`:

```
python3 resources/prose.py check workflows.md personas.md      -> exit 0
`--as <id>` on the line          -> present
`export PEARDE_AS=<id>`          -> present, unbroken
`· as <id>`                      -> present, unbroken
`▸ … · as <id>`                  -> present, unbroken
the-board-runs-itself/the-next-line-runs   96 checks · 94 pass · 2 fail (HEAD baseline)
```

`spec03`:

```
python3 resources/prose.py check consult health grammar memos  -> exit 0
python3 resources/index.py check | grep -c ''                  -> 3
  references/skills/pearde-machine.md is on disk with no row in references/files.md
  references/language.md references @references/personas/writer.md — not on disk
  resources/board/edit.py references @questions.py — not on disk
  (none names references/parts/ — every @ link in the four resolves)
git diff --diff-filter=RD -- references/parts/                 -> empty
 consult.md 27 +-- | grammar.md 14 +-- | health.md 40 +-- | memos.md 27 +--
```

## The fact audit

`probe/audit.sh`, the committed pass-one probe, run over all seven:

```
workers    words 3939->3918  rows 20->20  heads 1->1
workflows  words 1366->1360  rows 22->22  heads 5->5
personas   words 1303->1275  rows 19->19  heads 7->7
consult    words  629->616   rows  7->7   heads 5->5
health     words  747->736   rows  5->5   heads 5->5
grammar    words  472->466   rows  6->6   heads 4->4
memos      words  250->243   rows  0->0   heads 1->1
```

Every row count and heading count named in the specs matches. The probe reports
three near-misses, naive by design; all three were looked at and all three are
the same text still on the page:

- `workers.md` token `` ` reports it and ` `` — at `HEAD` the span
  `` `python3 @resources/workflows.py check` `` was split across lines 148-149,
  so the line-bounded regex saw a different fragment. It is now whole on one
  line (`references/parts/workers.md:145`), which is the density rule working.
- `health.md` link `@resources/board/init.py` — present, now ending a sentence,
  so the regex captured the trailing period with it.
- `grammar.md` link `@references/language.md.` — present as
  `@references/language.md;`, the sentence joined to the next.

Two rewrap-tolerant re-runs settle it. Comparing whitespace-normalised text,
**not one of the seven files loses a backticked token and not one loses a
link**:

```
workers    line-bounded spans 167->170; unresolved after rewrap-tolerant search: none
workflows   59->59  none      personas  42->43  none
consult     13->13  none      health    24->24  none
grammar     15->15  none      memos      9->9   none
TOTAL unresolved: 0    links_missing: [] on all seven
```

The counts that rise are spans that were broken across a line at `HEAD` and are
now unbroken — spec02's fourth box asks for exactly that.

## The rendered briefs

Rendering all five `brief:` blocks from the current `workers.md` and from
`git show HEAD:references/parts/workers.md`, then comparing on normalised
whitespace:

```
analyst      identical-after-rewrap = True
consultant   identical-after-rewrap = True
implementer  identical-after-rewrap = True
workflow     identical-after-rewrap = True
every        identical-after-rewrap = False
```

Four of five render identically once rewrapped. All of the change is inside
`brief:every`, the block both the analyst and the implementer brief carry:

```diff
-Look a word in your contract you do not know up with `python3 resources/grammar.py show`, and put a word you needed and it does not define in your report rather than inventing one.
+Look up a word in your contract you do not know with `python3 resources/grammar.py show`; a word you needed and it does not define goes in your report rather than being invented.

-… both of which are read as no verdict at all.
+… both read as no verdict at all.

-That line is the only thing `pearde collect` reads to pick the transition, and a report whose first 40 lines carry none is refused with nothing written.
+`pearde collect` reads that line and nothing else to pick the transition, and a report whose first 40 lines carry none is refused with nothing written.

-Then return one line — … Under fifteen lines back, whatever the report holds.
+Then return one line — … — under fifteen lines back, whatever the report holds.
```

Two are the reworded sentences the spec names: the `grammar.py show` sentence
and the `pearde collect` sentence. The other two are the density rule itself —
four waste words dropped (`of which are`), and two sentences joined on an
em-dash — the same class of change as the rewrapping the box already allows.

Read against the ten operative instructions the block carries — language,
frontmatter, other PRDs, writing outside the folder, the out-of-scope defect,
the grammar lookup, `knowledge.py remember`/`conclude`, the report path, the
`Verdict:` line with all four of its constraints, and the one-line return under
fifteen — **none is dropped, weakened or reordered.** This report was written
from the rewritten block; every rule in it was followable.

## The repo's own gate

`bash resources/doctor.sh`, run twice: once on the lane as it stands, once with
the seven files checked out to `HEAD` and then restored. The rows were diffed.

**No row moved.** Two lines differ and both are `ok` on both sides:

- `statusline` gains `*7` — the seven dirty files, which is the work itself.
- `vision` reads `25 off` then `26 off` — a board count that changed between the
  two runs. It is read off `pearde/prds`, not off `references/parts/`, so it is
  another session's board write, not this footprint.

The gate is red on rows that were red before this PRD and that this footprint
does not name: `index` (3, the same three spec03 pins), `origin` (1 derived PRD
with no `from:`), `memos` (39), `workflows` (25 `tags:` keys), `health` (2 files
no longer tracked, plus a stale ranking) and `knowledge` (6 notes ahead of
`graph.json`). `briefs` and `grammar` are `ok`. Grepping the whole gate output
for the seven filenames returns one line, and it is the `briefs ok` row.

## Health floor

The brief listed nothing under the floor, and nothing in the footprint is under
it. No file was moved, split or refactored — the specs are the scope and this
pass was a re-run, not a rewrite.

## Defects outside scope, reported not fixed

1. **`probe/audit.sh` cannot tell a rewrap from a loss.** Its `` `[^`\n]+` ``
   and `@[\w./-]+` regexes are line-bounded and swallow trailing punctuation, so
   a span that moves across a line break or a link that gains a `.` reads as
   missing. It reported three such here and all three were false. The script
   says so in its own header — naive by design, so a person looks — so this is
   a note on its cost, not a bug: it needs a human pass every run. A
   whitespace-normalised comparison (spans re-extracted after `\s+` to a single
   space, links compared with trailing punctuation stripped) is decidable and
   returned `TOTAL unresolved: 0` here. Not filed, not fixed.
2. **Six doctor rows are red on this checkout**, listed above, none in this
   footprint. `workflows`' 25 problems are one misspelling repeated across every
   atomic (`tags:` for a key that is not in the closed set), which reads as a
   single mechanical fix.

## Words

No word in the contract was missing from `grammar.py show`; nothing to add.
No fact was learned outside this repo, so nothing was written to `knowledge.py`.
