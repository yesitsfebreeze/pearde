---
complexity: 6
footprint:
  - index.md
  - references/files.md
  - references/knowledge.md
  - references/obsidian.md
  - references/parts/all.md
  - references/templates/grammar.md
  - resources/knowledge.py
---

# spec04 — the map names the tasks, and nothing names the skills

Every `@references/skills/...` anchor in `index.md` and `references/files.md`
becomes its `references/tasks/` path or `@SKILL.md`, the `@@skills`, `@@install`
and `@@update` scopes are rewritten around the one skill, and the manifest grows
a row per moved file and loses the one for `install.sh`. `resources/knowledge.py`'s
folder-to-kind map calls `references/tasks` a `task`. `pearde index check` is the
gate and it is the whole proof.

**This stands in the lane already** — every path is rewritten, the three scopes
are correct, and `python3 resources/index.py check` reports one problem, which is
a pre-existing defect outside this footprint (`references/parts/commits.md`
naming `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`, not on
disk). What is left to finish is the *wording* of the rewritten rows: several
still read as if a folder of skills existed, and `references/files.md`'s second
column should say what each task file is rather than repeat the verb.

## Acceptance

- [x] `python3 resources/index.py check` reports nothing inside this footprint
- [x] `references/files.md` holds one row per `references/tasks/*.md` and a row for `@SKILL.md`, and no row for `@resources/install.sh`
- [x] `@@skills` resolves to `@SKILL.md`, `references/tasks/`'s files and `@references/install.md`, and to nothing else
- [x] `@@install` and `@@update` name no installer script
- [x] `resources/knowledge.py` maps `references/tasks` to `task`, and `references/skills` appears nowhere in it
- [x] `references/templates/grammar.md`'s **skill** row describes one skill whose body is an index, not one file per skill
- [x] `python3 resources/index.py scope skills` prints 20 anchors, every one on disk

## Verify and Proof

```sh
python3 resources/index.py check | grep -v 'references/parts/commits.md' | tee /dev/stderr | test "$(wc -l)" -eq 0
python3 resources/index.py scope skills
grep -c '@references/tasks/' references/files.md    # 18
grep -c 'install\.sh' references/files.md index.md  # 0
grep -c 'references/skills' resources/knowledge.py  # 0
```
