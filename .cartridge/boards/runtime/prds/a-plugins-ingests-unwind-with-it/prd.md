---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: a-plugins-ingests-unwind-with-it
needs:
- '@runtime/disk-adapters-detach-without-forgetting-memory'
---

# a-plugins-ingests-unwind-with-it

Runtime owns disposal of transient adapters; memory owns an explicit source-retraction operation with durable provenance. A transient projection is identified by owner generation and effect ID, while ordinary ingest remains durable. Rehome only lifecycle orchestration and retain the engine integrity requirement as a referenced contract.

## Acceptance

- [ ] Disposing an old effect retracts only its own transient projection and cannot retract a successor generation.
- [ ] A durable fact ingested through the same adapter stays recallable after disposal/reload.
- [ ] Reattachment uses documented source/content identity and records retraction reasons; no plugin runtime is reintroduced inside memory.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-plugins-ingests-unwind-with-it`; maximum five rounds.
