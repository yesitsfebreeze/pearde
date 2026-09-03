---
state: done
origin: requested
priority: 80
complexity: 38
blast-radius:
needs: every-module-finds-its-siblings-by-one-rule
actual: 5.3h
---

# every documented command exists

A doctor row `claims` that checks every `pearde <verb>` mentioned in `references/**/*.md` against `pearde help`, every settings key named in `references/settings.md` and `contract.md` against `init.py` DEFAULTS, and every memo slug cited in `resources/**/*.py` against the board's memos. Each miss is one line naming `file:line`.

## Done means

Plant `pearde frobnicate` in a reference → broken. Today's known misses are reported until fixed: `commits.md` (`commits: off`), `plan.py` citing `done-counts-which-boxes.md`, `handles.md` (`master <path>`).

## Needs

`every-module-finds-its-siblings-by-one-rule` — the same gate as the container `the-doctor-refuses-drift`.

## Report

spec01: exit 0
      48
      45
exit=1
FAIL plant

spec02: exit 0
23 settings 22 frontmatter
references/parts/handles.md:73: `pearde purge` — no such command
references/parts/view.md:51: `pearde report` — no such command
references/skills/pearde.md:3: `pearde once` — no such command
references/skills/pearde.md:3: `pearde master` — no such command
references/parts/commits.md:229: `commits:` — no settings key of that name
resources/board/mapfile.py:205: memo `done-counts-which-boxes` — no such memo on this board
resources/board/prdfile.py:347: memo `done-counts-which-boxes` — no such memo on this board
references/archive.md:1
references/settings.md:1
references/parts/contract.md:1

spec03: exit 0
  index       broken  5 problems
  claims      broken  7 drifted names
  statusline  ok      . session/s34612 no-upstream
