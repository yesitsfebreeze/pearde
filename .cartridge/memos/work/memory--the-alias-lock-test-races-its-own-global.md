---

kind: work
level: 10
status: done
estimate: 1h
description: "`lock_serializes_canonical_aliases_and_releases` fails about one run in five under a parallel suite — the third process-global race found in `commands` after the exit flag and the freed port, and the last one keeping `cargo test -p commands --lib` from being green five times running"
read_when: "cargo test -p commands is red on commands_compact, or finishing the exit-flag split"
---

# the alias lock test races its own global

Measured 2026-09-08 while the freed-port fix ran its Check: five consecutive `cargo test -p commands --lib` runs, and run four failed
`commands_compact::tests::lock_serializes_canonical_aliases_and_releases` with a
panic at `src/commands/src/commands_compact.rs:577`. The other four runs passed.

This is the third of the three defects [[@prd/work/memory--the-exit-flag-tests-race-each-other.md]]
turned out to be, and the same shape as the two already fixed: a test asserting
about a process-global while 127 siblings run in the same process. The exit flag
moved to its own integration binary
(`f10f4b53`); the freed port became a socket the test owns and never listens on
(`2689b579`); this one is still open, and while it is, the parent memo's Check —
`cargo test -p commands --lib` green five times running — cannot pass.

Corrected 2026-09-09 by [[@prd/work/memory--the-handover-test-cannot-retake-its-own-lock.md]]: it is
not a global. `:577` asserts that `lock_root` succeeds on a root whose lock was
just dropped, and flock lives on the open file description, so a child forked by
any sibling test inherits the released lock for the window between fork and
exec — measured at under 2 ms, 2 blocked cycles in 20,000. Moving the test to
its own binary would only hide it: the same refusal reaches a real `memory
compact` whenever the process spawning `git` is the one taking the lock.

## Do

Give `lock_root` (`src/commands/src/commands_compact.rs:94`) the patience
`store_core::lock::acquire` now has: retry `WouldBlock` every 1 ms for a bounded
100 ms before refusing. The test is not the subject and needs no edit; do not
move it to its own binary, do not serialise the crate's suite, do not
`#[ignore]` it.

## Check

`cargo test -p commands --lib` run five times in a row is green five times, and
the alias-lock test still fails when the lock's release is removed by an inverse
edit.

Done 2026-09-09 in `ff6312e4`: the bounded wait `acquire` grew in `57a25c35` is
now `store_core::lock::try_lock_patiently`, called by both it and `lock_root`.
Thirty consecutive `cargo test -p commands --lib` runs were green; with the
test's `drop(lock)` removed by inverse edit, `:575` fails as it should.
