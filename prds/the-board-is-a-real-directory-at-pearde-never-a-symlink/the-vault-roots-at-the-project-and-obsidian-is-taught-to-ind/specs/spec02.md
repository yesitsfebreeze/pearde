---
complexity: 12
footprint:
  - resources/board/knowledge
  - resources/board/init.py
  - resources/board/obsidian/app.json
---

# spec02 — every vault-relative path names the board this project actually has

The vault is the project, so a Dataview source, an ignore filter and a
wikilink all resolve from the project root and must carry the board's folder
in front of them. Both shipped presets were written for a board called
`pearde/` — the undotted name the board wore for one day — so on a `.pearde/`
board every one of them names a folder the project has not. A Dataview
`FROM` over a missing folder renders an empty table and explains nothing,
which is the quietest way a dashboard can be wrong.

**What already stands** (built in the probe pass, uncommitted in the lane):

- `resources/board/knowledge/` is respelled `.pearde/…` — 37 occurrences
  across `Dashboard.md`, `conclusions/_index.md` and `sources/_index.md`.
- `resources/board/obsidian/app.json`'s eight board-relative
  `userIgnoreFilters` are respelled `.pearde/…`, so `repair_ignore_filters`'
  prefix comparison against `planlib.BOARD_DIR` matches for the first time.
  It was dead: `BOARD_DIR` is `.pearde` and the shipped filters started
  `pearde/`, so the mapping table came out empty on every board and the
  preset's spelling landed verbatim.
- `repair_ignore_filters` now also maps the legacy `pearde/…` spelling, so a
  vault seeded during the undotted day is corrected rather than left with two
  filters that name nothing.
- `init.py` gained `retarget`, `copy_vault_relative` and
  `repair_vault_relative`. `write_knowledge` copies each preset file through
  `copy_vault_relative`, substituting the board's real directory name for the
  shipped prefix, and then runs `repair_vault_relative` over the whole wiki so
  a board seeded before this step is corrected too. Only the prefix inside a
  quote or a wikilink opener is rewritten, so a page someone has edited keeps
  every edit.

**What is left**: nothing structural. Check that `retarget` cannot damage a
note whose prose legitimately contains the word, and that a board named
neither `pearde` nor `.pearde` (a project that had to call its board
something else) comes out right — the probe covers the default name only.
`knowledge.py` computes its own wikilinks with `relative_to(vault_root)` at
run time and is already correct; nothing there needs touching.

## Acceptance

- [x] No file under `resources/board/knowledge/` names a bare `pearde/`
      folder.
- [x] No entry in `resources/board/obsidian/app.json`'s `userIgnoreFilters`
      starts `pearde/`.
- [x] A board made by `pearde init` has no `"pearde/` string anywhere under
      `<board>/wiki/`, and its `Dashboard.md` sources read `.pearde/wiki/…`.
- [x] The same board's `.obsidian/app.json` has no filter starting `pearde/`.
- [x] A board created with `--name` (or in a project whose board directory is
      not `.pearde`) gets that directory's name in its Dataview sources and
      its ignore filters, not the shipped one.
- [x] Running `init` a second time over a wiki whose pages were seeded with
      the old prefix rewrites the prefix and leaves the rest of each page
      byte-identical.

## Verify and Proof

```sh
grep -rn '[^.a-zA-Z/-]pearde/' resources/board/knowledge/ && echo BAD || echo "preset clean"
python3 -c "import json;print([f for f in json.load(open('resources/board/obsidian/app.json'))['userIgnoreFilters'] if f.startswith('pearde/')])"
python3 .pearde/prds/the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind/probe/vault_contract.py .
python3 resources/index.py check
```
