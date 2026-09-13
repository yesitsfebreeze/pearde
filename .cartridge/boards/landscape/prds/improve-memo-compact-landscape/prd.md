---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: landscape
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-memo-compact-landscape
needs:
- "@landscape/improve-memo-compact-landscape/bounded-inventory-snapshot"
- "@memo/landscape-inventory-facade"
commit: "422c521aed170a4d098505c73469a1a59dccf49d"
---

# Bound landscape discovery and offer inventory drilldown

Attach this bounded projection contract to Landscape composition, retaining the existing memo facade and this work ID as coverage. Use additive request versioning before changing default output. Inventory paging and summary use the same source snapshot and canonical owner IDs.

## Acceptance

- [x] A 10,000-path fixture yields a default summary of at most 16 KiB with omitted counts; explicit pages reconstruct every permitted path exactly once.
- [x] Snapshot replacement invalidates a cursor explicitly and cannot silently mix generations.
- [x] Contributor failure produces partial status; changing presentation never rewrites source memos or observation history.

## Proof and recovery

Start at [lib.rs](../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memo-compact-landscape`; maximum five rounds.

## Owner split

The [Landscape snapshot library](bounded-inventory-snapshot/prd.md) owns collection, bounds and paging. The [memo native adapter](../../../memo/prds/landscape-inventory-facade/prd.md) owns the additive deployed request version and cache lifecycle. The original acceptance above and inherited two review rounds remain unchanged; [original leaf](original-leaf-prd.md) preserves the pre-split contract. This rollup collects only after both children and their combined native proof pass.
