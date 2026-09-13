---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: fs
work-kind: rollup
review-round: 3
review-status: "passed"
canonical-scope: improve-fs-programme
needs:
- '@fs/improve-fs-change-provenance'
- '@fs/improve-fs-revision-guards'
- '@fs/improve-fs-search-pages'
footprint: [".cartridge/docs/change-provenance.md",".cartridge/docs/revision-guards.md",".cartridge/docs/search-pages.md",".cartridge/tests/integration/change-provenance.test.ts",".cartridge/tests/unit/search/tests.rs",".cartridge/tests/unit/service/tests.rs","Cargo.toml","cartridge.json","src/context.rs","src/files.rs","src/main.rs","src/search.rs","src/service.rs"]
commit: "3a79023311b1a9b30c383ec8c71cf31c20a69ee7"
---

# Filesystem tools improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [x] Each linked leaf passes its own review and observable acceptance.
- [x] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Share change attribution between direct files and overlays](../improve-fs-change-provenance/prd.md)
- [Use consistent stale-write checks for filesystem mutations](../improve-fs-revision-guards/prd.md)
- [Bound and continue file search without losing result identity](../improve-fs-search-pages/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-fs-programme`; maximum five rounds.
