---
repo: /Users/feb/dev/cartridge/gitfs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: gitfs
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-gitfs-reviewable-ship
needs:
- '@policy/ship-push-is-an-explicit-policy-operation'
- '@gitfs/improve-gitfs-readable-diff'
- '@gitfs/improve-gitfs-snapshot-selection'
- '@policy/improve-policy-operation-rules'
- '@gitfs/improve-gitfs-reviewable-ship/reviewed-owned-tree-commits-locally'
- '@gitfs/improve-gitfs-reviewable-ship/recorded-push-reconciles-the-exact-remote-head'
commit: "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36"
---

# Preview and control shipping with accurate attribution

Split into reviewed-tree commit and remote push/reconciliation specs under one parent. Preview binds exact owned tree, index/base revision, required gates and author attribution. Commit revalidates that snapshot; push is a separate authorized action with expected remote head and an explicit completed/refused/unknown outcome.

## Acceptance

- [x] Unrelated staged edits and unowned paths never enter the commit.
- [x] Changed tree, failed/timeout required gate and cancellation before commit produce no commit; an explicit message cannot bypass a required gate.
- [x] A remote advance refuses push without force; disconnect after a possibly accepted push reconciles the recorded commit/ref rather than replaying or claiming rollback.

## Proof and recovery

Start at [service.rs](../../../service.rs), [store.rs](../../../store.rs), [ship.rs](../../../ship.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-gitfs-reviewable-ship`; maximum five rounds.

## Owned outcomes

- [reviewed-owned-tree-commits-locally](reviewed-owned-tree-commits-locally/prd.md)
- [recorded-push-reconciles-the-exact-remote-head](recorded-push-reconciles-the-exact-remote-head/prd.md)
