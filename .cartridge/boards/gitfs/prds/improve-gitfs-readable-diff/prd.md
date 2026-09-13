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
canonical-scope: improve-gitfs-readable-diff
needs:
- '@policy/improve-policy-operation-rules'
- '@gitfs/tool-results-interoperate'
footprint:
- /Users/feb/dev/cartridge/gitfs.ctg/service.rs
- /Users/feb/dev/cartridge/gitfs.ctg/store.rs
- /Users/feb/dev/cartridge/gitfs.ctg/ship.rs
- /Users/feb/dev/cartridge/gitfs.ctg/secrets.rs
- /Users/feb/dev/cartridge/gitfs.ctg/cartridge.json
---

# Inspect session changes without a mutation grant

A read-only caller can list/read session files and compare overlay, disk and base revisions before materialization.

## Acceptance

- [ ] With writes denied, real MCP list/read/diff succeed and leave Git refs, index and worktree unchanged.
- [ ] An external disk edit is visible as a conflict with both revisions; oversized diffs are bounded with drilldown.

- [ ] Use temporary Git repos/remotes for checks. Preserve unrelated index/worktree/ref changes. Roll back API additions before applying migrations; committed/pushed mutations require a recorded reconciliation/revert, not an assertion that cancellation undid them.

## Proof and recovery

Start at [service.rs](../../../service.rs), [store.rs](../../../store.rs), [ship.rs](../../../ship.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-gitfs-readable-diff`; maximum five rounds.
