---
complexity: 12
footprint:
  - resources/board/init.py
---

# spec01 — `pearde vault` waits instead of refusing, one writer at a time

`cmd_vault` in `resources/board/init.py` no longer refuses when Obsidian is
running: the flagless run and `--wait` now share one path, `wait_for_quit()`
— print the quit instruction, poll `obsidian_running()` at `WAIT_TICK`
intervals up to `WAIT_TICKS`, raise `Refused` naming the process on timeout.
A file lock (`VAULT_LOCK`, `tempfile.gettempdir()/pearde-vault.lock`,
machine-wide because `obsidian.json` is one file machine-wide) is claimed
with `acquire_vault_lock()` before the wait starts and dropped with
`release_vault_lock()` after the register write; a lock held by a live pid
refuses with `the writer is already held`, a lock left by a dead one is
cleared and retried. This was built and probed in the probe pass, not just
read from the contract — `probe/probe_vault_wait.py` exercises all four
acceptance boxes below against a faked `obsidian.json` and a mocked
`obsidian_running()`, since this machine has no real Obsidian process to
quit.

**What stands.** `wait_for_quit`, `acquire_vault_lock`, `release_vault_lock`,
`_lock_holder_alive`, `VAULT_LOCK`, and `cmd_vault`'s body rewired onto them —
all in `resources/board/init.py`, already built.

**What is left.** Nothing in the footprint above. Two things noticed outside
it are in this PRD's `report.md` under `## Findings`, not fixed here:
`cmd_init` and `cmd_upgrade` still tell a person to run
`pearde vault --wait --open` after registering under a running app — still
correct, since `--wait` still works, just no longer the only way; and
`unhide_board`'s default call inside `cmd_vault` raises unconditionally on
this tree today because `BOARD_DIR` is now the dotted name, which is a
different PRD's territory (`the-board-name-is-one-dotted-constant`, claimed,
in flight) and reproduced only inside the probe's own fixture by passing
`--dir` explicitly to route around it.

## Acceptance

- [x] `pearde vault` with no flag and Obsidian "running" prints the quit
      line and completes once "running" turns false, instead of raising
      `Refused` — no flag named anywhere in that path
- [x] `pearde vault --wait` still waits, writes and returns 0 under a mocked
      run with no TTY involved
- [x] a second `cmd_vault` call made while a first is inside `wait_for_quit`
      raises `Refused` whose text contains `already held`
- [x] a wait where `obsidian_running()` never turns false raises `Refused`
      within the configured tick budget (no hang) whose text names
      `Obsidian`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde/.pearde/.lanes/pearde-vault-without-wait
python3 -m py_compile resources/board/init.py
python3 /Users/feb/dev/infra/pearde/.pearde/prds/pearde-vault-without-wait/probe/probe_vault_wait.py
```

Expected tail: `all passed`, exit 0.
