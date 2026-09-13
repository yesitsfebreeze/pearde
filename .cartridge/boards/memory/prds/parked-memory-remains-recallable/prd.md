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
canonical-scope: parked-memory-remains-recallable
needs:
- '@memory/memory-004'
---

# parked-memory-remains-recallable

Share the hot/mixed/cold fixtures and ranking question with MEMORY-004 while retaining a separate exact-readback invariant. Candidate scoring and resolution must agree before top-k; do not solve missing cold edges by silently filtering parked facts. Bound cold I/O and expose unavailable data.

## Acceptance

- [ ] The same indispensable fact remains discoverable and exact-readable in hot, half-cold and all-cold layouts.
- [ ] A unavailable cold segment yields partial status and bounded I/O without stalling available results or calling a model.
- [ ] Linked-evidence, historical and multi-evidence metrics are reported separately, and no default switch or index-membership churn is inferred from this fix.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `parked-memory-remains-recallable`; maximum five rounds.
