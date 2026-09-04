---
complexity: 8
footprint:
  - references/parts/board.md
  - resources/board/transitions.py
  - resources/board/registry.py
  - resources/board/mapfile.py
  - resources/board/plan.py
  - resources/board/vision.py
  - resources/board/schedule.py
  - resources/board/collect.py
  - resources/board/prdfile.py
---

# spec01 — the board layout is drawn where it lives, and no docstring names a moved path

`references/parts/board.md` drew `settings.md`, `vision.md`, `memos/` and
`workflows/` as children of `prds/`. They are siblings of it, and so are
`grammar.md`, `report.md`, `health/` and `wiki/`. The scan root is
`<board>/prds/` and nothing outside it is a candidate PRD, so the old tree
told a reader the walk covers files it never sees.

Nine modules carried the same drift in docstrings and comments: `prds/.plan.json`,
`prds/.claims/`, `prds/.pass.md`, `prds/.transitions.jsonl`, `prds/settings.md`
and `prds/vision.md`. The state files moved to `<board>/.state/`, `.claims/`
sits directly under the board, and `settings.md` and `vision.md` sit beside
`prds/`. `collect.scratch`'s docstring listed `.pass.md`, `.history.jsonl` and
`.plan.json` as dotfiles directly under the board; all three are inside
`.state/` now. `prdfile.standing` and `mapfile` both cited a memo,
`done-counts-which-boxes.md`, that is on no board — the rule it was supposed to
hold is written out in `standing`'s own docstring, so the citation points there
instead of at a file nobody can open.

**What already stands** (built in the analysis pass, uncommitted in the lane):
all of it. `board.md` draws the board root with `prds/` as one child, names the
eight siblings in a sentence under the tree, and its `specs/` bullet now says
that `specs` is the one name `registry._scan_one` prunes — `memos/` and
`workflows/` need no pruning, being outside the scan root. The nine modules are
swept.

**What is left to finish**: review and commit. Do not rewrite `init.py`'s
`repair_graph_view` docstring: its `prds/knowledge/board` and `prds/memos` name
an *older vault layout on purpose*, as the shape a stale `graph.json` still
carries, and correcting it would delete the reason the function exists.

## Acceptance

- [ ] `grep -rn 'prds/settings\|prds/vision\|prds/\.plan\|prds/\.claims\|prds/\.pass\|prds/\.transitions' resources references` (excluding `__pycache__` and `node_modules`) returns nothing.
- [ ] `references/parts/board.md`'s tree block is rooted at the board directory, shows `prds/` as one child, and shows `settings.md`, `vision.md`, `grammar.md`, `report.md`, `memos/`, `workflows/`, `health/` and `wiki/` at the same level as `prds/`.
- [ ] `board.md` states in prose that those eight are siblings of `prds/` and that the scan root is `<board>/prds/`, and its bullet names `specs` as the only directory `registry._scan_one` prunes.
- [ ] No file under `resources/` names `done-counts-which-boxes.md`, and every `memos/<slug>.md` a module still cites is a file on the board.
- [ ] `resources/board/init.py`'s `repair_graph_view` docstring still names `prds/knowledge/board` and `prds/memos` as the stale layout.
- [ ] Every module in the footprint byte-compiles, and `python3 resources/index.py check` names no file in this footprint. (Four problems on the tree predate this PRD — `resources/common.py`'s missing row, `hotreload-test.js` in two places, and `commits.md`'s `@pearde/memos/` citation — and none is this PRD's to fix.)

## Verify and Proof

```sh
sh .pearde/prds/the-tree-holds-only-what-a-board-uses/the-documented-board-matches-the-code/probe/verify.sh "$PWD" "$PWD/.pearde"
python3 -m py_compile resources/board/transitions.py resources/board/registry.py resources/board/mapfile.py resources/board/plan.py resources/board/vision.py resources/board/schedule.py resources/board/collect.py resources/board/prdfile.py
test -z "$(grep -rn 'prds/settings\|prds/vision\|prds/\.plan\|prds/\.claims\|prds/\.pass\|prds/\.transitions' resources references --exclude-dir=__pycache__ --exclude-dir=node_modules)"
grep -q 'siblings of `prds/`' references/parts/board.md
grep -q 'prds/knowledge/board' resources/board/init.py
test -z "$(python3 resources/index.py check 2>&1 | grep -E 'board\.md|transitions\.py|registry\.py|mapfile\.py|plan\.py|vision\.py|schedule\.py|collect\.py|prdfile\.py')"
```
