---
complexity: 4
footprint:
  - resources/board/boards.py
  - resources/board/plan.py
  - resources/invariants/every-artifact-lands-inside-the-board.sh
---

# spec01 — no module runs a migration when it is imported

`resources/board/boards.py` calls `migrate_legacy_state()` at import time, so
every entry point pays an `isdir` and carries a 2026-09-01 one-shot that moved
`resources/board/state/` into the boards it held state for. That directory is
gone from this machine and the install is a symlink tree, so the function has
no work left. It goes, with the constant it rooted at the install and the
invariant exception written for it.

**Already standing** (pass one, in `probe/pass-one.diff`): the removal is
built and the invariant is green. **Left to finish**: land the diff and keep
the two gates green.

## Acceptance

- [x] `LEGACY_MACHINE_DIR` and `migrate_legacy_state` appear nowhere under `resources/`. — `grep -rn 'LEGACY_MACHINE_DIR\|migrate_legacy_state' resources/` → no match, `every-artifact-lands-inside-the-board.sh` 7 PASS 0 FAIL, `plan` imports.
- [x] `resources/board/boards.py` has no module-level call other than constant assignment — nothing runs on import. — top-level statements are imports and assignments only; `python3 -m py_compile` ok.
- [x] `resources/board/plan.py`'s re-export list names neither of the two removed names and still imports without error. — `import plan` with `resources` + `resources/board` on the path: no error.
- [x] `resources/board/boards.py` imports no module it no longer uses (`json` went with the migration). — `grep 'import json' resources/board/boards.py` → no match.
- [x] `every-artifact-lands-inside-the-board.sh` greps `MACHINE_DIR` with no `LEGACY_MACHINE_DIR` exemption, and passes. — rc=0, `PASS no MACHINE_DIR in the sources`, 7 PASS / 0 FAIL overall.

## Verify and Proof

```sh
cd "$REPO"
if grep -rn --exclude-dir=__pycache__ 'LEGACY_MACHINE_DIR\|migrate_legacy_state' --include='*.py' --include='*.sh' resources/; then exit 1; fi
python3 -c "import sys;sys.path[:0]=['resources','resources/board'];import plan"
python3 -m pyflakes resources/board/boards.py resources/board/plan.py 2>/dev/null || true
bash resources/invariants/every-artifact-lands-inside-the-board.sh
```
