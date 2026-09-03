---
state: open
origin: requested
priority: 80
complexity: 20
blast-radius:
needs: every-module-finds-its-siblings-by-one-rule
---

# every documented command exists

A doctor row `claims` that checks every `pearde <verb>` mentioned in `references/**/*.md` against `pearde help`, every settings key named in `references/settings.md` and `contract.md` against `init.py` DEFAULTS, and every memo slug cited in `resources/**/*.py` against the board's memos. Each miss is one line naming `file:line`.

## Done means

Plant `pearde frobnicate` in a reference → broken. Today's known misses are reported until fixed: `commits.md` (`commits: off`), `plan.py` citing `done-counts-which-boxes.md`, `handles.md` (`master <path>`).

## Needs

`every-module-finds-its-siblings-by-one-rule` — the same gate as the container `the-doctor-refuses-drift`.
