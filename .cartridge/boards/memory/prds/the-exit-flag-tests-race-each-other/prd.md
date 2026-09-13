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
