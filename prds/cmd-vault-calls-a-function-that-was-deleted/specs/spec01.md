---
complexity: 5
footprint:
  - resources/board/init.py
---

# spec01 — `pearde vault` calls `obsreg.running()`/`obsreg.write()`, not the deleted names

`da1aa69` (one-register-writer) moved `obsidian_running()` and
`register_vault()` out of `resources/board/init.py` into
`resources/board/obsidian_register.py` as `running()`/`write()`, and updated
`cmd_init`/`cmd_upgrade` to call `obsreg.running()`/`obsreg.write()`. It left
`cmd_vault` and the `wait_for_quit()` helper it calls still naming the old,
now-undefined functions, so `pearde vault` raises `NameError` before it
writes anything.

**Already done, in this lane's `resources/board/init.py` (uncommitted):**
`wait_for_quit()` and `cmd_vault()`'s two register calls now go through
`obsreg.running()` / `obsreg.write(d, retire=board)`. A probe at
`prds/cmd-vault-calls-a-function-that-was-deleted/probe/reproduce_and_verify.py`
reproduces the original crash pattern and asserts both that no call to the
deleted names remains and that `cmd_vault` completes end to end against a
stubbed `obsreg`.

**Left to finish:** none — this closes the PRD. The spec exists to carry the
acceptance boxes and land the diff that is already sitting in this lane's
working tree.

## Acceptance

- [x] `resources/board/init.py` contains no call to `obsidian_running(` or `register_vault(`
- [x] `wait_for_quit()` calls `obsreg.running()`
- [x] `cmd_vault()`'s two register-writing branches call `obsreg.write(d, retire=board)`
- [x] `python3 resources/pearde.py vault <dir> --dir pearde` against a real board no longer raises `NameError` (may still legitimately refuse or wait on Obsidian's own state)

## Verify and Proof

```sh
! grep -n "obsidian_running(\|register_vault(" resources/board/init.py   # expect no output
python3 .pearde/prds/cmd-vault-calls-a-function-that-was-deleted/probe/reproduce_and_verify.py
```
