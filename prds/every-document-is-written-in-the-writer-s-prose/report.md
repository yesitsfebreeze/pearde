Verdict: REFINE

# every document is written in the writer's prose — analyst report

## What the build did

Followed `probe-then-spec`. Read the contract, queried the knowledge base
(gap enqueued, see below), listed the board's workflows and picked
`probe-then-spec`, then measured the tree the contract targets: 117 tracked
`.md` files, 87,496 words by `wc -w`, before any edit.

Grouped every tracked `.md` file by directory and by word count
(`git ls-files '*.md'`, `wc -w` per file — see `probe/prose_probe.py`, left
uncommitted in the tree):

| group | files | words |
|---|---|---|
| `references/parts` | 28 | 34,815 |
| `references/*.md` (loose) | 17 | 19,700 |
| `resources/scout` | 4 | 9,387 |
| `references/templates` | 16 | 7,647 |
| `references/skills` | 19 | 5,259 |
| root (`index.md`, `README.md`, `SKILL.md`) | 3 | 3,541 |
| `references/personas` | 5 | 3,212 |
| `references/agents` | 3 | 1,073 |
| `resources/board/example/**`, `resources/board/knowledge/**` | 22 | ~2,470 |

Built a probe checker (`probe/prose_probe.py stat`) against the real tree:
mean sentence length is already at or under 24 words in 116 of 117 files
(only `references/skills/pearde-scout.md` runs long, at 39). The 30%+ cut
the contract asks for is a cut of words, mostly redundant ones, not a fix to
run-on sentences — `resources/prose.py`'s design needs a word-count and
waste-word gate more than a sentence-length one, and the density work itself
is the bulk of the effort, spread unevenly: `references/parts` alone is 40%
of the tree's words.

## Why REFINE

Two independent contracts hide inside one PRD: building the checker
(`resources/prose.py`, the `references/language.md` Density section) is a
code-and-rules unit; rewriting 117 files' prose under it is a content unit
with zero cross-file dependency — a rewrite of `references/parts/view.md`
never touches `references/skills/pearde-scout.md`. Spec'd as one PRD, the
rewrite alone needs well over 6 specs to stay inside any file's own
`## Verify and Proof` block, and the combined `complexity` of a checker plus
an 87k-word, fact-exact rewrite clears `split-above: 40` on the honest weight
of `references/parts` alone. Splitting by directory keeps every child's
footprint disjoint and lets every rewrite child run in parallel once the
checker exists.

## Findings

- `@references/personas/writer.md` — the density rules' named source — is
  untracked in the orchestrator's checkout (`git status` there: `??`) and
  absent from this lane's worktree, per the harnesses-copy-tracked-files-only
  finding on record. I read its content directly from the orchestrator's
  checkout to do this analysis; no child spec below can build against it
  until someone stages and commits it. Outside this PRD's footprint, not a
  fix I made.
- `python3 resources/index.py check` is red before any edit, on two lines
  outside this PRD's footprint: `references/skills/pearde-machine.md` has no
  row in `references/files.md`, and `resources/board/edit.py` references
  `@questions.py`, not on disk. Pre-existing, not this PRD's to fix.
- `bash resources/doctor.sh` in this lane reports `board broken` and most
  rows `off`, because the lane worktree carries no `.pearde/` of its own
  (it's gitignored) and `doctor.sh` does not walk up to find the shared one
  the way `knowledge.py`/`pearde.py` do. A lane-wide quirk, not this PRD's.
- `python3 resources/knowledge.py query` found nothing on record for this
  contract's question; it auto-enqueued `wiki/pending/260902-1c7c.md`.
- `resources/board/example/**` and `resources/board/knowledge/**` hold
  fixture/data `.md` — grouped as their own child so a rewrite there can be
  checked against any harness reading the example verbatim before it lands.

## Scores

Each child returns its own `complexity`/`blast-radius` when it is specced;
none is scored here since none is a spec set.

## Split

| child | contract | needs |
|---|---|---|
| a-density-checker-and-the-root-docs-are-rewritten | `resources/prose.py` checks word count, mean sentence length, unbound waste words and banned openers/closers per file; `references/language.md` carries the `## Density` section; `references/files.md`, `index.md`, `README.md` and `SKILL.md` are rewritten dense | — |
| the-parts-reference-is-rewritten-dense | every file under `references/parts/` (28 files, 34,815 words) rewritten dense, every fact intact | a-density-checker-and-the-root-docs-are-rewritten |
| the-loose-reference-files-are-rewritten-dense | every loose file under `references/` except `language.md` and `files.md` (15 files, 16,857 words) rewritten dense | a-density-checker-and-the-root-docs-are-rewritten |
| templates-personas-and-agents-are-rewritten-dense | `references/templates/`, `references/personas/` and `references/agents/` rewritten dense, prescribed shapes kept | a-density-checker-and-the-root-docs-are-rewritten |
| skills-and-scout-docs-are-rewritten-dense | `references/skills/` and `resources/scout/` docs rewritten dense (includes the one file over the sentence-length target) | a-density-checker-and-the-root-docs-are-rewritten |
| example-and-knowledge-fixtures-are-rewritten-dense | `resources/board/example/**` and `resources/board/knowledge/**` rewritten dense, checked against any harness reading them verbatim | a-density-checker-and-the-root-docs-are-rewritten |
