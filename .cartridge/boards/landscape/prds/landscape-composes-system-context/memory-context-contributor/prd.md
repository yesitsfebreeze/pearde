---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: landscape-composes-system-context
needs:
- '@landscape/landscape-composes-system-context/context-contributor-contract'
---

# Memory hits resolve to exact source evidence

Add memory query/readback as a contributor to the shared contract, retaining engine ownership.

## Acceptance

- [ ] A memory-only fact is found and its exact ID resolves.
- [ ] Unavailable memory respects the total deadline and reports partial status.
- [ ] Selected hydration obeys the configured count and byte limits.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `landscape-composes-system-context`; maximum five rounds.
