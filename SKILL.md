---
name: pearde
description: Install this repo's skills for whichever agent is reading, then work the PRD board at .pearde/prds/. One pass: materialise a folder per file in skills/ — pearde, pearde-drill, pearde-memo, pearde-view, pearde-report, pearde-master, pearde-doctor, pearde-persona, pearde-persona-ask, pearde-persona-create, pearde-scout, pearde-workflow, pearde-grammar, pearde-health, pearde-graph, pearde-knowledge, pearde-machine — wherever this agent discovers skills, then hand off to the board and carry on with the request. Use for "/pearde", "install pearde", "set up pearde", "wire up the skills", and everything the board answers to.
---

# pearde — install, then work

The installer. This repo must be invocable before any of its skills are —
this file exists for that gap, and stops existing the moment the gap closes.

## 1. Install

Read @references/install.md and follow it. One pass, no questions unless a
step genuinely cannot be decided from what is on the machine.

```bash
bash @resources/install.sh --apply <skills-dir>
```

Working out `<skills-dir>`, step one of @references/install.md, is the only
part this repo cannot do for you. Report which of its four cases you hit and
where you installed — that sentence is the install's only record.

## 2. This file retires itself

`skills/pearde.md` is the real board skill. While this installer exists, two
files answer to `pearde`, so `--apply`'s last act replaces this one with a
link to that one — the installer gone, the skill it stood in for live.
Nothing is lost: `git checkout SKILL.md` restores it, to re-install or to
install elsewhere.

Installing by hand rather than through `@resources/install.sh` takes the same
last step by hand:

```bash
ln -sfn skills/pearde.md SKILL.md
```

Only inside the skills directory, under the name `pearde`, does the installer
shadow the skill. Cloned anywhere else, nobody discovers this file and
nothing retires.

## 3. Then work the request

Read @README.md and carry on with what was actually asked — installing came
first, and answers no question of its own.

---

- `skills/` — one file per skill. The file name is the command.
- `references/` — read. The workflow, the personas, the templates, the rules.
- `resources/` — run. The board service, scout, the status line, doctor.
- @index.md is the map: `@<path>` is one file, `@@<keyword>` is a scope.
  @references/files.md is the manifest behind it, one row per file.
