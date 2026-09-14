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
canonical-scope: one-search-covers-the-record-and-memory
---

# one-search-covers-the-record-and-memory

Use landscape-composes-system-context as the canonical implementation and retain this record as memory-contributor acceptance. Memory stays optional and owns exact fact retrieval; metadata-only candidates are query-bounded before body hydration.

## Acceptance

- [ ] A memory-only phrase and a memo/tool phrase produce correctly attributed hits from one query.
- [ ] Returned memory IDs read back exactly through the surviving memory adapter; missing/deleted facts are explicit, not replaced by a semantic requery.
- [ ] Disabled memory yields useful remaining results; configured unavailable memory yields named partial status within the deadline and no second writer.

## Proof and recovery

Start at [lib.rs](../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-search-covers-the-record-and-memory`; maximum five rounds.
