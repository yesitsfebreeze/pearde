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
- '@landscape/recursive-development-graph/recursive-root-search'
---

# A descendant edit refreshes only its derived rows

Invalidate derived records on edit/move/reload while preserving authoritative local PRDs.

## Acceptance

- [ ] Edited child facts appear on the next fresh query.
- [ ] A moved or removed source invalidates its stale reference explicitly.
- [ ] Unrelated providers are not restarted and child records are never copied or deleted.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `recursive-development-graph`; maximum five rounds.
