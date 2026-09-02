# report — the standard is held to its own standard

Verdict: DONE

spec01: 6/6 boxes closed. `references/language.md` passes the checker it
defines. Change stands uncommitted in
`/Users/feb/dev/infra/pearde/pearde/.lanes/every-document-is-written-in-the-writer-s-prose-the-standard-is-held-to-its-own-standard`,
one file, `17 insertions(+), 18 deletions(-)`.

## Boxes

| box | check | proof |
|---|---|---|
| 1 | `prose.py check references/language.md` | no output, `EXIT=0` |
| 2 | `## Density` row for the convention, nine prior rules intact | `ROWS=11` (header + 10 rules), `A quoted example of banned prose is backticked` present, all nine lead phrases grep-hit |
| 3 | eleven `## Rules` bullets survive | all eleven lead phrases grep-hit; `awk` bullet count `11` |
| 4 | `## Where prose stays` + seven-row shape table + README exemption | `SHAPE=8` (header + 7), `\| README        \| a person, first time \| quickstart, then rings \|` and `a sentence there may` both present |
| 5 | `prose.py stat` at `611` words or fewer | `WORDS=587` |
| 6 | `index.py check` adds no line about `references/language.md` | `IDX=1`, the one line is the pre-existing `@references/personas/writer.md` |

## Verify and Proof

`spec01`'s block ran whole under `bash -e`:

```
spec01: 6 boxes, 11 density rows, 587 words
BLOCK_EXIT=0
```

## What the pass changed

The bare `"This is important for correctness"` in the `Rationale only where it
changes a decision` bullet was read by `@resources/prose.py` as the file's own
vague-subject prose — the rule's own counter-example failed the rule. Every
quoted example of banned prose is now backticked: the `Imperative`, `Name the
thing`, `Address, do not describe a path` and `No meta` bullets alongside it.
The convention is a `## Density` row so the next writer keeps it. Three bullets
were compressed — `Structure over prose`, `Address, do not describe a path`,
`Reach for @@` — and `## Where prose stays` lost a sentence break. No rule was
dropped, none added beyond the convention row.

## The gate

`resources/index.py check`, `resources/memos.py check`, `resources/doctor.sh`
all run. Their failures are identical before and after the change — stashing
the diff and re-running `index.py check` returns the same three lines:

```
references/skills/pearde-machine.md is on disk with no row in references/files.md
references/language.md references @references/personas/writer.md — not on disk
resources/board/edit.py references @questions.py — not on disk
```

None is in this PRD's footprint, and the `language.md` one is the writer
persona the sibling PRD `templates-personas-and-agents-are-rewritten-dense`
writes — it closes on the merge, as spec01 box 6 states.

## The sibling's block

`a-density-checker-and-the-root-docs-are-rewritten`'s spec01 asserts
`RULE_ROWS -ge 10` over the same `## Density` table. It reads `11` — the row
added here raises the count, never lowers it. Still green.

## Health

No footprint file under the floor — the brief names none, and
`references/language.md` is prose, unscored.

## Defects outside scope

Three, all pre-existing, all reported not fixed:

1. `references/skills/pearde-machine.md` has no row in `references/files.md`.
2. `resources/board/edit.py` addresses `@questions.py`, which is
   `resources/questions.py` — the address wants a repo-root path.
3. `resources/doctor.sh` reports `health broken`: two ranking rows name files
   no longer tracked (`references/parts/run.md`, `resources/board/run.py`), and
   the graph is newer than the ranking. `python3 resources/health.py score`
   regenerates it.

## Grammar

No word was needed that `python3 resources/grammar.py show` does not define.
