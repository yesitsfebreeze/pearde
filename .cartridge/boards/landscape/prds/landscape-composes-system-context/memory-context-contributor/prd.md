---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: landscape-composes-system-context
footprint:
- src/lib.rs
- src/memory.rs
- .cartridge/tests/unit/src/memory/tests.rs
- .cartridge/docs/memory-context.md
needs:
- '@landscape/landscape-composes-system-context/context-contributor-contract'
commit: "3b9f72854c39ddd90128a48bfce2667e387c3fba"
---

# Memory hits resolve to exact source evidence

Add memory query/readback as a contributor to the shared contract, retaining engine ownership.

## Acceptance

- [x] A memory-only fact is found and its exact ID resolves.
- [x] Unavailable memory respects the total deadline and reports partial status.
- [x] Selected hydration obeys the configured count and byte limits.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 3 independent agent review](review.md). Inherits round 1 from `landscape-composes-system-context`; maximum five rounds.

Inventory registration revalidation: unchanged acceptance and verification at Landscape 3b9f728; source footprint additionally binds the registered inventory module.
