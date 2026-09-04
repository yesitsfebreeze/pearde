---
complexity: 7
footprint:
  - resources/index.py
  - resources/doctor.sh
---

# spec02 — a doctor row that fails when a trigger phrase falls out

One skill fires on one `description:`, so eighteen descriptions become one and a
phrase dropped from it is a task that never fires with nothing to see. This
makes the drift loud: `python3 resources/index.py skills` reads every
`references/tasks/*.md`'s `## Fires on` list and fails on any phrase absent from
`SKILL.md`'s description, and `doctor`'s `skills` row is that check.

**This stands in the lane already** — `skills()`, `skill_description()`,
`task_phrases()` and the `skills` command are in `resources/index.py`, the
`skills` row in `resources/doctor.sh` is rewritten around them, and both were
made to fail on an injected drop and on an emptied `## Fires on` before being
believed. What is left to finish is the docstring line in `index.py`'s usage
block and a row for the check in `references/parts/doctor.md`.

## Acceptance

- [x] `python3 resources/index.py skills` exits 0 and prints nothing on a clean tree
- [x] Deleting one phrase from `SKILL.md`'s description makes it exit 1 and name the task file and the phrase
- [x] Emptying one task's `## Fires on` list makes it exit 1 and name that task
- [x] A `SKILL.md` with no `description:` makes it exit 1 and say so, rather than traceback
- [x] `index.py`'s module docstring lists the `skills` command beside `check`
- [x] `bash resources/doctor.sh` reports `skills ok` with one skill, the task count and the verb names, and its `fix:` line is the `index.py skills` command
- [x] The `skills` row goes `broken` when `SKILL.md` says a `name:` other than `pearde`

## Verify and Proof

```sh
python3 resources/index.py skills && echo clean
cp SKILL.md /tmp/s.bak
python3 - <<'PY'
t=open('SKILL.md').read(); open('SKILL.md','w').write(t.replace(', "what gained stars this week"','',1))
PY
python3 resources/index.py skills; test $? -eq 1 && echo "fails on a dropped phrase"
cp /tmp/s.bak SKILL.md
bash resources/doctor.sh 2>&1 | grep -E '^  skills'
```
