---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: capabilities-live-with-their-owners
needs:
- '@mcp/clients-share-document-execution'
---

# A document invokes validated memo writes

Expose the existing write API through one owner-local document; keep revision and link validation in memo.

## Acceptance

- [ ] Valid create and revision-matched update read back exactly.
- [ ] Stale revisions and unresolved links leave source bytes intact.
- [ ] Reload preserves the previous usable document on invalid replacement.

## Proof and recovery

Start at [service.rs](../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `capabilities-live-with-their-owners`; maximum five rounds.
