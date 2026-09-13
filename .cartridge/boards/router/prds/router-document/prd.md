---
repo: /Users/feb/dev/cartridge/router.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: router
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: capabilities-live-with-their-owners
needs:
- '@mcp/clients-share-document-execution'
---

# A document explains routing without exposing secrets

Expose status, model selection and route explanation through existing router boundaries; provider launch remains host-mediated.

## Acceptance

- [ ] Offline protocol fixtures show the selected route and its source revision.
- [ ] Unknown capability or missing credentials is explicit.
- [ ] Reads leak no credential and cannot grant a launch or retry a mutation.

## Proof and recovery

Start at [lib.rs](../../../lib.rs), [catalog.rs](../../../catalog.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test router` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `capabilities-live-with-their-owners`; maximum five rounds.
