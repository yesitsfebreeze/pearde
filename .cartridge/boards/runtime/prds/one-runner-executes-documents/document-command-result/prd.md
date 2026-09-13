---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: one-runner-executes-documents
needs:
- '@runtime/one-runner-executes-documents/approved-document-launch'
- '@gitfs/tool-results-interoperate'
---

# A document command reports its real completion

Run one approved recipe through the existing host runner; distinguish tool failure, cancellation and uncertain effects.

## Acceptance

- [ ] A disposable command returns stdout/stderr and exit outcome.
- [ ] Cancellation stops only owned work and retains invocation identity.
- [ ] A committed mutation followed by malformed output reports uncertainty and is not retried.

## Proof and recovery

Start at [runtime.rs](../../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-runner-executes-documents`; maximum five rounds.
