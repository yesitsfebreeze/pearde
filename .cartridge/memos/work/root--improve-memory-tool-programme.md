---
kind: work
description: "Deliver the three Memory tool adapter improvements with explicit risk coverage"
status: open
subwork:
  - "[[@prd/work/root--improve-memory-tool-get.md]]"
  - "[[@prd/work/root--improve-memory-tool-correct.md]]"
  - "[[@prd/work/root--improve-memory-tool-errors.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["planning memory-tool improvements", "reviewing memory-tool cartridge readiness"]
---

# Memory tool adapter improvement plan

## Outcome

Deliver the three improvements requested for Memory tool adapter, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Retrieve a recalled fact by stable ID | [[@prd/work/root--improve-memory-tool-get.md]] |
| 2. Correct or forget one identified fact through the tool boundary | [[@prd/work/root--improve-memory-tool-correct.md]] |
| 3. Return actionable memory failures and enforce the tool schema | [[@prd/work/root--improve-memory-tool-errors.md]] |

## Downside coverage

1. Engine outages propagate: normalize errors without pretending recall is empty.
2. The current surface cannot manage fact lifecycle: add narrow evidence/correction operations.
3. An adapter duplicates contracts: keep translation thin and cover schema/execution parity before any consolidation.

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
- [ ] The integrated Memory tool adapter behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test memory-tool
just check memory-tool
just test memory --test cartridge
just test policy
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
