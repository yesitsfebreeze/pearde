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
- '@memo/one-document-serves-every-reader/executable-document-validation'
- '@runtime/launch-authority'
---

# Only an approved frozen invocation reaches spawn

Bind owner, source digest, recipe, argv, cwd and policy using host-resolved launch authority.

## Acceptance

- [ ] Changing source after approval either executes the frozen bytes or refuses.
- [ ] Forged identity, stale revision, invalid cwd and denial spawn zero processes.
- [ ] Real launch-path fixtures establish the supported platform's containment.

## Proof and recovery

Start at [runtime.rs](../../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-runner-executes-documents`; maximum five rounds.
