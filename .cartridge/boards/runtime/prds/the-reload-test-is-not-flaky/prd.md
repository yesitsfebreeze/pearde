---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 4
review-status: accepted
canonical-scope: the-reload-test-is-not-flaky
commit: "bd3b5e78d6e3ddd7dc7567b0c357d6fe60bd02df"
footprint: [".cartridge/tests/unit/src/tests/reload.rs","src/loader.rs",".cartridge/tests/unit/src/tests/mod.rs",".cartridge/tests/unit/src/tests/composition.rs"]
---

# the-reload-test-is-not-flaky

Reproduce the old failure with controlled barriers around build completion, reload readiness and the assertion. Replace timing guesses with an observable generation/ready boundary. Repeated runs supplement that causal proof; they do not replace it.

## Acceptance

- [x] The deliberately forced old ordering fails before the fix and passes after synchronization on the same fixture.
- [x] A bad rebuild still preserves the prior usable surface and cannot satisfy readiness for the wrong generation.
- [x] Twenty repeated runs pass on an unchanged isolated binary and the required current development test entry point includes the regression.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Revision-bound agent review](review.md). Inherits round 1 from `the-reload-test-is-not-flaky`; maximum five rounds.
