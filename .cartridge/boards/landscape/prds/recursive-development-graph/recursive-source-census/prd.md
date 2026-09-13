---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: recursive-development-graph
needs:
- '@memo/memo-board-template/initialize-board'
- '@memo/one-document-serves-every-reader/document-identity'
---

# Declared descendants have distinct source identities

Traverse declared board/cartridge roots without launching providers; identify each canonical hierarchical owner.

## Acceptance

- [ ] A three-level fixture preserves same-named records under different owners.
- [ ] Backlinks, repeated mounts and symlinks terminate within depth/count/byte bounds.
- [ ] Unreadable or deleted descendants have explicit status.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `recursive-development-graph`; maximum five rounds.
