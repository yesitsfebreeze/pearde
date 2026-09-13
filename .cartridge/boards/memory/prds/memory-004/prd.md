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
canonical-scope: MEMORY-004
---

# Mixed and cold recall preserve per-ability ranking

Decide whether mixed/cold ranking needs expansion credit, residency-aware fusion weighting, or neither. Reuse the mature fixture and authored replay corpus; preserve current/historical recall while improving linked-evidence ranking. Record the decision without switching the default.

## Acceptance

- [ ] Pinned hot, mixed and cold fixtures report linked-evidence, historical and multi-evidence metrics separately.
- [ ] Declare regression thresholds before candidate results and retain the current retrieval default.
- [ ] Unavailable cold data reports partial results within a bounded I/O budget; indispensable facts remain exact-readable.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `MEMORY-004`; maximum five rounds.
