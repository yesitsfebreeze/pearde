---

kind: work
level: 10
status: done
estimate: 1h
description: "`a_handover_with_no_listener_frees_the_store_and_returns` failed 6 runs in 60 re-acquiring its own writer lock — flock lives on the open file description, so a child forked by any sibling test inherits the lock for the ~1 ms between fork and exec; `acquire` now waits a bounded 100 ms for it and no longer calls a non-WouldBlock error a holder"
read_when: "a writer reports a holder that does not exist, or a flock is refused right after it was released"
---

# the-handover-test-cannot-retake-its-own-lock

`a_handover_with_no_listener_frees_the_store_and_returns`
(`src/commands/src/commands_serve.rs:1239`) takes the writer lock on a fresh
tempdir, hands the store over with no successor fd, and re-acquires. It failed
about once in ten full `cargo test -p commands --lib` runs, and the cause is not
the one this memo suspected: reproduced 2026-09-09, 6 failures in 60 runs of the
`commands` lib binary, the error printed rather than swallowed by `is_ok()`,
every one of them `Held { holder: Some("daemon pid <the test's own pid>") }` —
`WouldBlock`, not an errno. A transient `flock` error folded into `Held` is
ruled out.

flock lives on the **open file description**, not on the process or the fd. A
child forked anywhere in the process inherits the lock, and `O_CLOEXEC` closes
the fd at `exec`, not before, so for the window between the two a lock this
process released is still held by its own half-born child; the `commands` suite
spawns `git` and daemon processes from sibling tests all through the run.
Isolated with std alone — `File::try_lock`, no memory code, acquire-drop-reacquire
on a private tempdir — eight threads spawning `/usr/bin/true` blocked 2 of
20,000 cycles and zero threads blocked 0 of 20,000, worst window 1.6 ms, nothing
ever failing to free. `rekey_refuses_while_the_writer_lock_is_held` was the same
red (6 in 60) and cleared with the same fix;
`commands_compact::tests::lock_serializes_canonical_aliases_and_releases` is the
same defect in a second `try_lock` of its own and is corrected in
[[@prd/work/memory--the-alias-lock-test-races-its-own-global.md]].

## Do

Done, three commits on `src/store_core/src/lock.rs` plus the test's message.
`WouldBlock` is `LockError::Held` and any other `io::Error` is `LockError::Io` —
a production defect on its own, since `memory gc` or `memory reembed` read the stale
name out of the lock file and announced a holder that does not exist. The
handover test panics with the `LockError` it got instead of asserting `is_ok()`.
`acquire` retries `WouldBlock` every 1 ms for a bounded 100 ms before reporting
`Held`: a real holder holds for a process lifetime, so the wait separates a fork
window from a live writer and still never blocks on a daemon that never exits.
`holder()` is left un-patient on purpose — it is a status query on ten display
paths, and 100 ms of waiting to print a name is worse than a 1 ms phantom.

## Check

Met. `cargo test -p commands --lib` run twenty times in a row: this test green
twenty times, against 6 failures in 60 runs before the fix.
