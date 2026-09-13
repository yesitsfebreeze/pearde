---
kind: work
description: "Deliver the three Memory improvements with explicit risk coverage"
status: open
subwork:
  - "[[@prd/work/root--improve-memory-owner-access.md]]"
  - "[[@prd/work/root--improve-memory-readiness.md]]"
  - "[[@prd/work/root--improve-memory-provenance.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["planning memory improvements", "reviewing memory cartridge readiness"]
---

# Memory improvement plan

## Outcome

Deliver the three improvements requested for Memory, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Query a memory store through its existing owner | [[@prd/work/root--improve-memory-owner-access.md]] |
| 2. Report memory readiness separately from registration | [[@prd/work/root--improve-memory-readiness.md]] |
| 3. Expose fact provenance freshness and conflicts consistently | [[@prd/work/root--improve-memory-provenance.md]] |

## Downside coverage

1. Writer ownership can block recall: attach to the legitimate owner, preserving single-writer integrity.
2. Model endpoints can fail: return bounded, attributable failures and test with local fixtures.
3. Facts can age or conflict: expose provenance and freshness without inventing truth.

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
- [ ] The integrated Memory behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test memory --test cartridge
just check memory
just test memory
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
