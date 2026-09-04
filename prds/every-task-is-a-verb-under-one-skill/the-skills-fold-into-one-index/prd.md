---
state: specced
origin: requested
priority: 80
complexity: 36
blast-radius: high
needs:
  - the-machine-is-the-run-verb
---

# the skills fold into one index

`skills/` holds one file. `pearde` is the only skill this repo installs, and
its body is an index of the tasks — one row each, naming the reference to read
and the command to run. `/pearde doctor`, `/pearde drill`, `/pearde memo`,
`/pearde scout` and the rest are that index's rows, not seventeen skills.

Waits on `the-machine-is-the-run-verb`: the index names `run`, and writing it
twice is writing it wrong.

## What exists when this is done

| | now | then |
|---|---|---|
| `skills/` | 18 files | `skills/pearde.md`, alone |
| a task's body | `references/skills/pearde-<verb>.md` | `references/tasks/<verb>.md` |
| an install | 18 folders of 5 links — 85 on this machine | one symlink: `<skills-dir>/pearde` → the repo |
| `@@skills` in @index.md | 19 anchors | `@SKILL.md`, `references/tasks/`, @references/install.md |
| @references/parts/handles.md's *"Several of these are also skills of their own"* | true | gone — every handle is a verb under one skill, and the paragraph goes with it |

The verbs are the names the seventeen files already carry, minus the `pearde-`
prefix: `run`, `drill`, `memo`, `view`, `report`, `master`, `doctor`,
`update`, `persona`, `persona-ask`, `persona-create`, `scout`, `workflow`,
`grammar`, `health`, `graph`, `knowledge`.

## The one description carries every trigger

**This is the cost of the fold and the one thing that can silently break it.**
A skill fires on its `description`, so seventeen descriptions become one, and
a phrase dropped from it is a task that never fires — `"what gained stars this
week"` reaching nothing is not an error anyone sees.

So: the union of the seventeen `description:` trigger phrases is carried into
`skills/pearde.md`'s own, and a `doctor` row asserts it. That row reads every
`references/tasks/*.md`'s `## Fires on` list and fails when a phrase in one is
absent from the skill description — the check is mechanical, so the drift is
caught at the next `doctor` rather than at the next miss.

Each task file therefore opens with `## Fires on` — the phrases that used to
live in its frontmatter — and keeps its body as it is.

## The index

`skills/pearde.md`'s body is a table: verb · what it is · what to read · the
command. One row per task, one line each, and no task's knowledge in it —
@references/install.md's rule that a skill is a door and not the room holds
for the index too. The reading rule from @index.md holds harder here: a
session opens the one row it is on, never the table's worth of files.

## Installing stops building anything

**The user's words, 2026-09-02: *"when we only use ONE skill we dont need to
copy anything anymore."*** The five links per folder exist to give each of
eighteen skills a `SKILL.md`, a `README.md`, an `index.md`, a `references/`
and a `resources/` beside it. The repo root already has that shape. Eighteen
folders needed them fabricated; one skill can simply *be* the repo.

```sh
ln -s <repo> <skills-dir>/pearde     # the whole install
```

One wrinkle, and it is the only cost: `<skills-dir>/pearde/SKILL.md` has to
be the **skill**, and today the repo root's @SKILL.md is the **installer**.
With nothing left to install the installer has no job, so the root file
becomes the skill outright — the retire-itself step of @SKILL.md, done once
in the tree instead of once per install.

| now | then |
|---|---|
| `@resources/install.sh` builds 18 folders of 5 links | gone. `ln -s` is the install, and @references/install.md is one line plus how to find `<skills-dir>` |
| `@resources/update.sh` re-links the set | it removes the folders an earlier install left, and stops. A link to the repo is never stale — an edit here is live there, both ways |
| `@resources/doctor.sh`'s install rows | one row: the link exists and resolves to this repo |
| @SKILL.md retires itself at `--apply` | it *is* the skill. Nothing retires |

`update.sh` keeping the removal is the one thing that must survive: two
`pearde-doctor`s — a stale folder and an index row — is the agent seeing a
task twice, and the stale folder wins on a name match.

## What must not change

- **`pearde <cmd>` is untouched.** The shell alias, @resources/pearde.py's
  `FORWARD` table and every command under it are a separate surface from the
  skills, and this contract does not fold them.
- **A task's body keeps its own file.** The fold is of the entry points, not
  of the knowledge — one file per task under `references/tasks/`, read on
  demand.
- **@references/files.md gets a row per moved file**, and every
  [Keywords](#keywords) row in @index.md naming a `references/skills/` path is
  rewritten. `pearde index check` is the gate.

## Verify

`ls skills/` is one line. `python3 resources/pearde.py index check` is clean,
`python3 resources/pearde.py doctor` reports `skills ok`, and no
`references/skills/` path survives anywhere in the tree.

`<skills-dir>` holds one entry named `pearde`, it is a symlink, and
`readlink -f` on it is this repo. `resources/install.sh` is not in the tree.
`git grep -c 'five links'` is 0.

## Blocked

**2026-09-03 21:54 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `session/s27323`; 6 file(s) disagree:

- `index.md`
- `references/files.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-03 21:55 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `session/s27323`; 6 file(s) disagree:

- `index.md`
- `references/files.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-03 21:56 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `main`; 6 file(s) disagree:

- `index.md`
- `references/files.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `session/s62223`; 6 file(s) disagree:

- `index.md`
- `references/files.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `main`; 6 file(s) disagree:

- `index.md`
- `references/files.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `session/s62223`; 6 file(s) disagree:

- `index.md`
- `references/files.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `session/s62223`; 6 file(s) disagree:

- `index.md`
- `references/files.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `session/s62223`; 6 file(s) disagree:

- `index.md`
- `references/files.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `session/s85810`; 5 file(s) disagree:

- `index.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 04:02 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `main`; 5 file(s) disagree:

- `index.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 04:05 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `main`; 5 file(s) disagree:

- `index.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.

**2026-09-04 04:18 — the lane will not rebase**

`lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` does not land on `main`; 5 file(s) disagree:

- `index.md`
- `references/obsidian.md`
- `references/skills/pearde.md`
- `resources/install.sh`
- `resources/update.sh`

Nothing is lost: the worker's commits are on `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`.
