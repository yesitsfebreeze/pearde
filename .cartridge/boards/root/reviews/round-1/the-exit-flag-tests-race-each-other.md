---

kind: work
level: 10
status: open
estimate: 1h
subwork: [[the-handover-test-cannot-retake-its-own-lock]]
description: "`commands_exit`'s tests assert a process-global failure flag is clean at entry, so any test running beside them that calls `fail()` turns them red — three identical runs of `cargo test -p commands --lib` failed 1, 2 and 1 tests on unchanged code"
read_when: "cargo test -p commands is red on a test that passes when run alone"
---

# the-exit-flag-tests-race-each-other

`a_reported_failure_is_what_the_exit_status_reads`
(`src/commands/tests/exit_status.rs:7`) opens with
`assert!(!failed(), "a run that reported nothing has not failed")` and then
calls `fail(...)`. The flag it reads is process-global and the harness runs the
crate's 127 tests in parallel in one process, so the assertion is a claim about
every other test's timing, not about this one's subject. Run alone the test
passes; run with its siblings it fails, and the count is not even stable —
three identical `cargo test -p commands --lib` runs on the same unchanged
worktree failed **1, 2 and 1** tests. `rpc --lib` fails the same way under the same load, so it is the flag and not the
crate. Any lane touching either crate therefore reads a red suite it did not cause, and a real regression hides in the
noise ([[gates-are-tests]]).

The exit flag is fixed and landed: the test moved to `src/commands/tests/exit_status.rs`,
its own binary and so its own process, and `fail` is `pub` for it to reach.
Red-proofed — with the `FAILED.store` removed the test fails.

The Check is still red, and not on this flag. Five fresh runs after the move
failed on two other tests, each racing a different process-global: a test
reusing a freed port (two of five runs; fixed in `2689b579` by a socket the
test owns and never listens on) and
[[the-handover-test-cannot-retake-its-own-lock]] (one in roughly ten). The
memo's "failed 1, 2 and 1 tests" was three defects, not one. This memo is done
when the remaining child is.

## Do

Make the exit-status tests independent of what else is running: give the flag a
test-only reset the test takes under a mutex it shares with every sibling that
calls `fail()`, or move these tests into their own integration binary so the
process is theirs alone. Do not fix it by marking the test `#[ignore]` or by
serialising the whole crate's suite — the first hides the claim, the second pays
for one test with every test's runtime.

## Check

`cargo test -p commands --lib` run five times in a row is green five times, and
the exit-status test still fails when `fail()` is genuinely not reported.

