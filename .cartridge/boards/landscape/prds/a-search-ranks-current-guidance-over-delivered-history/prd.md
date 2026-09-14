---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: a-search-ranks-current-guidance-over-delivered-history
---

# a-search-ranks-current-guidance-over-delivered-history

Add explicit current-guidance versus historical-evidence query intent to the existing ranker rather than universally demoting completed records. Retain measured paraphrase fixtures, source labels and usage evidence with bounded influence.

## Acceptance

- [ ] Both existing repository-gate questions find the applicable current routine in the required top positions.
- [ ] A query asking what shipped or why an old decision changed can return done/superseded evidence with its status intact.
- [ ] Equivalent snapshots sort deterministically; repeated observation counts cannot override scope, invalid-source or current-intent constraints.

## Proof and recovery

Start at [lib.rs](../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-search-ranks-current-guidance-over-delivered-history`; maximum five rounds.
