---
complexity: 12
footprint:
  - resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
---

# spec02 — the invariant covers the two layouts that broke it

The invariant that claims to hold "a footprint is filed under the repo that
holds it" builds two layouts: nested (a board with a `.git` of its own) and
flat (a plain `.pearde/`). Neither of the two defects this PRD found turns it
red — the nested section only ever names a footprint the code repo's way, and
no section ever puts a code checkout under the board. A guard that stays green
through the regression it exists to catch is not a guard, and both defects
regress silently: one refuses a DONE PRD for a reason that names the wrong
function, the other writes an empty commit and reports success.

**What already stands.** Nothing in this file. The PRD's own probe covers both
layouts at the `foot_root` and `sort_paths` level and runs green
(`probe/verify.sh`, 7 checks); this unit takes the same two cases end to end
through `collect`, which is what the invariant measures and the probe does not.

**What is left.** Two sections, built on the fixtures the file already has.

## Acceptance

- [x] a nested-layout section names a footprint spelled the BOARD's own way — a file under `prds/<prd>/`, where every probe on this board is told to live — and it lands in the board repo's commit
- [x] that section is red against a `collect.py` without `foot_places`, so it can fail
- [x] an "under" section builds the code repo as a checkout INSIDE the board directory and asserts the footprint lands in the CODE repo's commit, not the board's
- [x] that section asserts the board repo's commit does not carry the code path under any spelling — the old behaviour was silent, so an exit code and a `fatal:` grep cannot catch it
- [x] every fixture is under the one `mktemp -d` the file already removes on exit, and the live tree is untouched
- [x] the file still prints one line per assertion and a count, and exits non-zero when any line is `FAIL`
- [x] the count is at least 16, up from 12

## Verify and Proof

```sh
PEARDE_ROOT="$PWD" bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
PEARDE_ROOT="$PWD" bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh | grep -c '^PASS'
PEARDE_ROOT="$PWD" bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh | grep -c 'under:'
PEARDE_ROOT="$PWD" bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh | grep -c 'board-spelled'
PEARDE_ROOT="$PWD" bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh | grep -c 'every fixture is under one mktemp -d, removed on exit'
```
