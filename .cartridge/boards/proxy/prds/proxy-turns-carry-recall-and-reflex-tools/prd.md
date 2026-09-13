---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: proxy
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: proxy-turns-carry-recall-and-reflex-tools
---

# proxy-turns-carry-recall-and-reflex-tools

Move bounded context preparation into proxy/harness consuming Landscape; memory supplies source-labelled query/readback only. Keep client-owned history/tools and native wire framing. Optional context failure yields an explicit degraded observation while forwarding the original valid request.

## Acceptance

- [ ] A fixture request receives relevant bounded memory context once with provenance and no elevation to system authority.
- [ ] Missing memory/selection failure preserves client streaming, cancellation and provider error semantics without a nested agent loop.
- [ ] Tool preparation cannot expand profile grants or hide required client tools; the same selected snapshot is inspectable without an inference call.

## Proof and recovery

Start at [service.rs](../../../service.rs), [streaming.rs](../../../streaming.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `proxy-turns-carry-recall-and-reflex-tools`; maximum five rounds.
