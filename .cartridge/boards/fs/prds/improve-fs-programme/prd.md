---
repo: /Users/feb/dev/cartridge/fs.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: fs
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-fs-programme
needs:
- '@fs/improve-fs-change-provenance'
- '@fs/improve-fs-revision-guards'
- '@fs/improve-fs-search-pages'
---

# Filesystem tools improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Share change attribution between direct files and overlays](../improve-fs-change-provenance/prd.md)
- [Use consistent stale-write checks for filesystem mutations](../improve-fs-revision-guards/prd.md)
- [Bound and continue file search without losing result identity](../improve-fs-search-pages/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-fs-programme`; maximum five rounds.
