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

## From the retired work memo

Folded 2026-09-15 from `work/improve-fs-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Filesystem tools improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Filesystem tools, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Share change attribution between direct files and overlays | [improve-fs-change-provenance](../improve-fs-change-provenance/prd.md) |
| 2. Use consistent stale-write checks for filesystem mutations | [improve-fs-revision-guards](../improve-fs-revision-guards/prd.md) |
| 3. Bound and continue file search without losing result identity | [improve-fs-search-pages](../improve-fs-search-pages/prd.md) |

### Downside coverage

1. FS duplicates existing tools: keep profiles opt-in and justify use through outcomes.
2. Direct and overlay tools overlap: make storage semantics explicit per operation.
3. Disk edits diverge from overlays: journal source/revision and reconcile deliberately.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Review current source and active ownership before implementation; the assessment does not reserve files.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Filesystem tools behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test fs
just check fs
just test gitfs
just test sessions
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
