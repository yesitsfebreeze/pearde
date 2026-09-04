---
complexity: 12
footprint:
  - references/tasks/
  - SKILL.md
  - references/parts/handles.md
---

# spec01 — the seventeen skills become eighteen tasks, and one skill indexes them

Every `references/skills/pearde-<verb>.md` becomes `references/tasks/<verb>.md`,
opening with a `## Fires on` list holding the trigger phrases that used to sit
in its frontmatter, its body otherwise untouched. `references/skills/pearde.md`
folds into the repo root's `SKILL.md`, whose `description:` carries the union of
those lists and whose body is the index table. `references/skills/` stops
existing.

**This stands in the lane already** — the moves, the `## Fires on` lists, the
composed `SKILL.md` and the deleted directory are all in the working tree.
What is left to finish is a read of each task body for a sentence that only
made sense while it was a skill of its own.

The eighteenth verb is `plan`. `references/skills/pearde-all.md` is not in the
PRD's list of seventeen, and dropping it silently loses eighteen trigger
phrases — the exact failure the contract names. It becomes
`references/tasks/plan.md`, which is what the parent's settled table already
says the read verb is called.

## Acceptance

- [x] `references/skills/` does not exist, and `git grep -c 'references/skills'` over the tree is 0
- [x] `references/tasks/` holds exactly 18 files: `run`, `plan`, `drill`, `memo`, `view`, `report`, `master`, `doctor`, `update`, `persona`, `persona-ask`, `persona-create`, `scout`, `workflow`, `grammar`, `health`, `graph`, `knowledge`
- [x] Each of the 18 opens with a `# <verb>` heading and a `## Fires on` list of at least one backtick-quoted phrase, and no task file carries YAML frontmatter
- [x] `SKILL.md`'s frontmatter is `name: pearde` and one `description:` on a single line — a plain YAML scalar, never a block scalar and never quoted
- [x] `SKILL.md`'s body holds one table row per task, each naming the verb, what it is, `@references/tasks/<verb>.md`, and the command, and holds no task's knowledge of its own
- [x] The paragraph in `references/parts/handles.md` beginning *"Several of these are also skills of their own"* is gone, and no `pearde-<verb>` name survives in that file
- [x] `python3 resources/index.py check` reports no problem naming a task file

## Verify and Proof

```sh
test ! -e references/skills
test "$(ls references/tasks/*.md | wc -l)" -eq 18
for f in references/tasks/*.md; do head -1 "$f" | grep -q '^# ' || { echo "$f: no heading"; exit 1; }; grep -q '^## Fires on' "$f" || { echo "$f: no Fires on"; exit 1; }; done
head -3 SKILL.md | grep -q '^description: [^|>"]'
grep -c '@references/tasks/' SKILL.md          # 18
grep -c 'Several of these are also skills' references/parts/handles.md   # 0
python3 resources/index.py check
```
