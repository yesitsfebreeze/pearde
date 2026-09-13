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
canonical-scope: improve-gitfs-snapshot-selection
footprint:
- /Users/feb/dev/cartridge/gitfs.ctg/service.rs
- /Users/feb/dev/cartridge/gitfs.ctg/store.rs
- /Users/feb/dev/cartridge/gitfs.ctg/ship.rs
- /Users/feb/dev/cartridge/gitfs.ctg/secrets.rs
- /Users/feb/dev/cartridge/gitfs.ctg/cartridge.json
---

# Snapshot exactly the selected owned paths

snapshot.paths captures only the caller-selected owned files and reports inaccessible files instead of silently claiming success.

## Acceptance

- [ ] Own A and B, edit both on disk, snapshot only A: overlay B remains unchanged; an empty selection snapshots nothing.
- [ ] Unowned/invalid paths are rejected, read failures are reported, and guarded edits and materialization conflict tests still pass.

- [ ] Use temporary Git repos/remotes for checks. Preserve unrelated index/worktree/ref changes. Roll back API additions before applying migrations; committed/pushed mutations require a recorded reconciliation/revert, not an assertion that cancellation undid them.

## Proof and recovery

Start at [service.rs](../../../service.rs), [store.rs](../../../store.rs), [ship.rs](../../../ship.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-gitfs-snapshot-selection`; maximum five rounds.
