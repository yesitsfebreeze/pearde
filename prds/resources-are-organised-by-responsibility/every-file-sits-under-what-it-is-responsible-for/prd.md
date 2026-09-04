---
state: failed
origin: requested
priority: 0
complexity: 18
blast-radius:
needs:
  - every-module-finds-its-siblings-by-one-rule
  - the-largest-module-is-cut-by-responsibility
---

# every-file-sits-under-what-it-is-responsible-for — Every file under `resources/` sits in a directory named for what the files in it are responsible for, the manifest and the map and the prose and the board's 51 harnesses all name the new paths, nothing is downloaded to run or draw the board, and `index.py check` and `doctor.sh` are green

Every file under `resources/` sits in a directory named for what the files in it are responsible for, the manifest and the map and the prose and the board's 51 harnesses all name the new paths, nothing is downloaded to run or draw the board, and `index.py check` and `doctor.sh` are green

## Failure

swept 2026-09-04 02:41 — claim impl-every-file-r2 2026-09-03 21:01, silent 5.7h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/resources-are-organised-by-responsibility-every-file-sits-under-what-it-is-responsible-for`, whose worktree this sweep removed — the branch is kept.
