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
canonical-scope: recursive-development-graph
needs:
- '@landscape/recursive-development-graph/recursive-source-census'
---

# Root search reads every permitted descendant record

Join the bounded census into root search and exact readback, preserving source-only versus callable availability.

## Acceptance

- [ ] Root search finds distinct facts from all three fixture levels.
- [ ] Inactive documentation never becomes a callable service.
- [ ] Exact reads resolve the selected owner rather than another matching basename.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `recursive-development-graph`; maximum five rounds.
