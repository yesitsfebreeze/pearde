---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: the-exit-flag-tests-race-each-other
footprint: ["src/commands/Cargo.toml","src/store/core/src/lock.rs",".cartridge/tests/unit/src/store/core/src/tests/lock_test.rs","src/store/core/Cargo.toml","Cargo.lock"]
commit: "a124fd30d59bcd06062b5464810188a0288e461e"
needs:
- "@memory/the-handover-test-cannot-retake-its-own-lock"
---

# the-exit-flag-tests-race-each-other

Treat the exit-status integration-binary move as delivered history until a current probe disproves it. Identify the remaining handover/global-state test by its present source path, then fix that race under its own bounded outcome; do not reset a shared flag merely to make reruns green.

## Acceptance

- [x] The exit-status test fails when the reported-failure behavior is deliberately removed, independently of sibling timing.
- [x] A controlled handover/global-state interleaving reproduces the remaining race and verifies the proposed synchronization.
- [x] Five unchanged isolated runs supplement causal proof, and the report names which historical fixes were reused rather than reimplemented.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-exit-flag-tests-race-each-other`; maximum five rounds.

## Verified implementation — 2026-09-13

Full `just check` passed formatting and workspace/all-target clippy. Full
`just test` passed 1,339 nextest tests (17 configured skips) and documentation
tests. Five unchanged isolated runs passed all 15 exit, controlled-lock and
no-listener-handover checks. Removing FAILED.store made the exit target fail
at its reported-failure assertion; removing retry made the controlled-lock
fixture fail at its observed-WouldBlock assertion. Both mutations were restored.

The historical isolated test file and 100ms inherited-descriptor patience are
reused. The current gap was missing Cargo registration plus missing causal
coverage, not a reason to reset the global failure flag. The completed historical
work record is memory--the-handover-test-cannot-retake-its-own-lock.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--the-exit-flag-tests-race-each-other.md` (status open, estimate 1h). The PRD state above is authoritative.

> `commands_exit`'s tests assert a process-global failure flag is clean at entry, so any test running beside them that calls `fail()` turns them red — three identical runs of `cargo test -p commands --lib` failed 1, 2 and 1 tests on unchanged code

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
[the-handover-test-cannot-retake-its-own-lock](../the-handover-test-cannot-retake-its-own-lock/prd.md) (one in roughly ten). The
memo's "failed 1, 2 and 1 tests" was three defects, not one. This memo is done
when the remaining child is.

### Do

Make the exit-status tests independent of what else is running: give the flag a
test-only reset the test takes under a mutex it shares with every sibling that
calls `fail()`, or move these tests into their own integration binary so the
process is theirs alone. Do not fix it by marking the test `#[ignore]` or by
serialising the whole crate's suite — the first hides the claim, the second pays
for one test with every test's runtime.

### Check

`cargo test -p commands --lib` run five times in a row is green five times, and
the exit-status test still fails when `fail()` is genuinely not reported.
