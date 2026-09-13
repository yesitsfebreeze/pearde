---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: the-exit-flag-tests-race-each-other
---

# the-exit-flag-tests-race-each-other

Treat the exit-status integration-binary move as delivered history until a current probe disproves it. Identify the remaining handover/global-state test by its present source path, then fix that race under its own bounded outcome; do not reset a shared flag merely to make reruns green.

## Acceptance

- [ ] The exit-status test fails when the reported-failure behavior is deliberately removed, independently of sibling timing.
- [ ] A controlled handover/global-state interleaving reproduces the remaining race and verifies the proposed synchronization.
- [ ] Five unchanged isolated runs supplement causal proof, and the report names which historical fixes were reused rather than reimplemented.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-exit-flag-tests-race-each-other`; maximum five rounds.
