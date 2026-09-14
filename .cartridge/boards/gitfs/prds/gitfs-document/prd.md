---
repo: /Users/feb/dev/cartridge/gitfs.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: gitfs
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: capabilities-live-with-their-owners
needs:
- '@mcp/clients-share-document-execution'
---

# A document preserves session overlay semantics

Expose overlay read/edit/materialize through the existing GitFS service; shipping remains a separate reviewed operation.

## Acceptance

- [ ] Overlay edits leave disk unchanged until explicit materialization.
- [ ] A different session cannot materialize the caller's paths.
- [ ] Failure reports partial effects and never retries an uncertain mutation.

## Proof and recovery

Start at [service.rs](../../../service.rs), [store.rs](../../../store.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `capabilities-live-with-their-owners`; maximum five rounds.
