---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-memory-tool-programme
needs:
- '@memory/improve-memory-tool-get'
- '@memory/improve-memory-tool-correct'
- '@memory/improve-memory-tool-errors'
---

# tool.memory covers exact readback, correction and actionable failures

The memory-tool wrapper was dropped on 2026-09-14 (root commit `9e4cde8`), and memory.ctg now serves `tool.memory` itself from `src/cartridge.rs`. This parent tracks the three remaining improvements to that tool. To implement, claim one of the leaves; the parent carries no implementation of its own.

## Acceptance

- [ ] Each linked leaf passes its own review and acceptance at one memory.ctg revision.
- [ ] Integration gate: at that revision, `just test` passes from /Users/feb/dev/cartridge/memory.ctg, and one integration case drives `tool.memory` through query → get → correct → get → forget → get, with each failure code observed where its leaf specifies.
- [ ] Any leaf limitation, such as `tool_writes` staying off by default, is recorded here rather than closed silently.

## Work items

- [Agents read one recalled fact back by ID through tool.memory](../improve-memory-tool-get/prd.md)
- [Agents correct or forget one identified fact through tool.memory](../improve-memory-tool-correct/prd.md)
- [tool.memory failures carry a stable code the agent can act on](../improve-memory-tool-errors/prd.md)

## Review

[Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.

## From the retired work memo

Folded 2026-09-15 from `work/improve-memory-tool-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Memory tool adapter improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Memory tool adapter, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Retrieve a recalled fact by stable ID | [improve-memory-tool-get](../improve-memory-tool-get/prd.md) |
| 2. Correct or forget one identified fact through the tool boundary | [improve-memory-tool-correct](../improve-memory-tool-correct/prd.md) |
| 3. Return actionable memory failures and enforce the tool schema | [improve-memory-tool-errors](../improve-memory-tool-errors/prd.md) |

### Downside coverage

1. Engine outages propagate: normalize errors without pretending recall is empty.
2. The current surface cannot manage fact lifecycle: add narrow evidence/correction operations.
3. An adapter duplicates contracts: keep translation thin and cover schema/execution parity before any consolidation.

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
- [ ] The integrated Memory tool adapter behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test memory-tool
just check memory-tool
just test memory --test cartridge
just test policy
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
