---
complexity: 6
footprint:
  - references/parts/statusline.md
  - references/obsidian.md
  - references/files.md
  - references/graph.md
---

# spec04 — the Obsidian vault roots at the project, in the docs as in the code

Four reference pages said the board is the vault and Obsidian roots at
`.pearde/`. The code roots it at the **project**: `knowledge.py` sets
`vault_root = board_root.parent` and writes wikilinks carrying the board's own
directory name (`[[pearde/prds/…]]`); the seed's Dataview queries read
`FROM "pearde/wiki/board"`; `init.py`'s step 4b seeds `<dir>/.obsidian/` and
its comment says the vault roots at the PROJECT; `statusline.sh` tries
`${BOARD%/*}/.obsidian` first and the board only as the pre-2026-09-02
fallback; and `doctor.sh`'s `vault` row checks `$PROJ/.obsidian` and calls a
real dot-named board **broken** for exactly this reason.

The consequence of believing the docs is concrete: a reader who roots a vault
at the board gets every Dataview query in `Dashboard.md` resolving one level
off and no code in the index at all.

**What already stands** (built in the analysis pass, uncommitted in the lane):
`statusline.md`'s heading and its `▸vault` table row; `obsidian.md`'s opening
paragraph, its root section, its register paragraph and its plugin-seed path;
`files.md`'s `init.py` row, its `obsidian/` preset row and its vault-relative
paragraph; and `graph.md`'s separate-vault sentence.

**What is left to finish**: review and commit. Both pages keep the *reason*
the old text gave — Obsidian skips any path holding a dot-segment — because
that reason is why the board's directory name is `pearde/` without the dot in
the first place, and deleting it would leave the layout looking arbitrary.

## Acceptance

- [ ] `references/parts/statusline.md`'s vault heading says the vault roots at the project, and the `▸vault` table row calls it the project, board and all.
- [ ] `references/obsidian.md` opens with the project as the vault, and its root section says the root is the project rather than `.pearde/`.
- [ ] `references/obsidian.md` says `pearde vault --wait --open` seeds `<project>/.obsidian/`, and that the plugins are seeded into the project's `.obsidian/`.
- [ ] `references/files.md`'s vault-relative paragraph says a query reads a project-relative path carrying the board's directory name, matching `resources/board/knowledge/Dashboard.md`'s own `FROM "pearde/wiki/board"`.
- [ ] `references/files.md`'s `@resources/board/init.py` and `@resources/board/obsidian/` rows name the project, not the board, as where the vault is seeded.
- [ ] No file under `references/` says the vault roots at the board or that the board is the vault; each page still explains that Obsidian skips a dot-segment.
- [ ] `python3 resources/index.py check` names no file in this footprint.

## Verify and Proof

```sh
sh .pearde/prds/the-tree-holds-only-what-a-board-uses/the-documented-board-matches-the-code/probe/verify.sh "$PWD" "$PWD/.pearde"
test -z "$(grep -rn 'roots at the board\|board is the vault' references)"
grep -q 'roots at the project' references/parts/statusline.md
grep -q 'The project is the vault' references/obsidian.md
grep -q 'the vault is the \*\*project\*\*' references/files.md
grep -q 'FROM "pearde/wiki/board"' resources/board/knowledge/Dashboard.md
grep -q 'roots at the PROJECT' resources/statusline.sh
test -z "$(python3 resources/index.py check 2>&1 | grep -E 'statusline\.md|obsidian\.md|files\.md|graph\.md')"
```
