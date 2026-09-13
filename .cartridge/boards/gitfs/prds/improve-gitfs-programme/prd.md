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
canonical-scope: improve-gitfs-programme
needs:
- '@gitfs/improve-gitfs-readable-diff'
- '@gitfs/improve-gitfs-snapshot-selection'
- '@gitfs/improve-gitfs-reviewable-ship'
commit: "b4b95bb648ea1e99b6ffc9ba3cbd562f255ca9d5"
---

# GitFS and ship improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [x] Each linked leaf passes its own review and observable acceptance.
- [x] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Inspect session changes without a mutation grant](../improve-gitfs-readable-diff/prd.md)
- [Snapshot exactly the selected owned paths](../improve-gitfs-snapshot-selection/prd.md)
- [Preview and control shipping with accurate attribution](../improve-gitfs-reviewable-ship/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-gitfs-programme`; maximum five rounds.
