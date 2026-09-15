---
kind: work
description: "Deliver the three Filesystem tools improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-fs-change-provenance](../../../fs/prds/improve-fs-change-provenance/prd.md)"
  - "[improve-fs-revision-guards](../../../fs/prds/improve-fs-revision-guards/prd.md)"
  - "[improve-fs-search-pages](../../../fs/prds/improve-fs-search-pages/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning fs improvements", "reviewing fs cartridge readiness"]
---

# Filesystem tools improvement plan

## Outcome

Deliver the three improvements requested for Filesystem tools, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Share change attribution between direct files and overlays | [improve-fs-change-provenance](../../../fs/prds/improve-fs-change-provenance/prd.md) |
| 2. Use consistent stale-write checks for filesystem mutations | [improve-fs-revision-guards](../../../fs/prds/improve-fs-revision-guards/prd.md) |
| 3. Bound and continue file search without losing result identity | [improve-fs-search-pages](../../../fs/prds/improve-fs-search-pages/prd.md) |

## Downside coverage

1. FS duplicates existing tools: keep profiles opt-in and justify use through outcomes.
2. Direct and overlay tools overlap: make storage semantics explicit per operation.
3. Disk edits diverge from overlays: journal source/revision and reconcile deliberately.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Review current source and active ownership before implementation; the assessment does not reserve files.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Filesystem tools behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test fs
just check fs
just test gitfs
just test sessions
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
