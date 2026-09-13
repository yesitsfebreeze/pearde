---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: the-track-record-is-reachable-across-stores
---

# the-track-record-is-reachable-across-stores

Use the existing hub/federation boundary for explicitly requested cross-store recall. Scope is opt-in per query with caller-authorized stores, bounded contributors and store-qualified IDs. Default cwd isolation remains unchanged; no replication or new ledger is introduced.

## Acceptance

- [ ] Two stores with the same leaf/entity name return distinct source-store/origin identities and exact readback.
- [ ] An unauthorized store is not queried or exposed, while an unavailable authorized store yields partial status within the query budget.
- [ ] Existing single-store query behavior and durable history remain compatible; federation performs no hidden writes or model calls beyond configured retrieval semantics.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-track-record-is-reachable-across-stores`; maximum five rounds.
