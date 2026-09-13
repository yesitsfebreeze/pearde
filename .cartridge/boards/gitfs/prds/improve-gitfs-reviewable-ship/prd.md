---
repo: /Users/feb/dev/cartridge/gitfs.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: gitfs
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-gitfs-reviewable-ship
needs:
- '@gitfs/improve-gitfs-readable-diff'
- '@gitfs/improve-gitfs-snapshot-selection'
- '@policy/improve-policy-operation-rules'
footprint:
- /Users/feb/dev/cartridge/gitfs.ctg/service.rs
- /Users/feb/dev/cartridge/gitfs.ctg/store.rs
- /Users/feb/dev/cartridge/gitfs.ctg/ship.rs
- /Users/feb/dev/cartridge/gitfs.ctg/secrets.rs
- /Users/feb/dev/cartridge/gitfs.ctg/cartridge.json
---

# Preview and control shipping with accurate attribution

Split into reviewed-tree commit and remote push/reconciliation specs under one parent. Preview binds exact owned tree, index/base revision, required gates and author attribution. Commit revalidates that snapshot; push is a separate authorized action with expected remote head and an explicit completed/refused/unknown outcome.

## Acceptance

- [ ] Unrelated staged edits and unowned paths never enter the commit.
- [ ] Changed tree, failed/timeout required gate and cancellation before commit produce no commit; an explicit message cannot bypass a required gate.
- [ ] A remote advance refuses push without force; disconnect after a possibly accepted push reconciles the recorded commit/ref rather than replaying or claiming rollback.

## Proof and recovery

Start at [service.rs](../../../service.rs), [store.rs](../../../store.rs), [ship.rs](../../../ship.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-gitfs-reviewable-ship`; maximum five rounds.
