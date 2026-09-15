---
kind: work
description: "Deliver the three Agent loop improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-agent-task-baseline](../../../agent/prds/improve-agent-task-baseline/prd.md)"
  - "[improve-agent-resume-boundaries](../../../agent/prds/improve-agent-resume-boundaries/prd.md)"
  - "[improve-agent-decision-attribution](../../../agent/prds/improve-agent-decision-attribution/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning agent improvements", "reviewing agent cartridge readiness"]
---

# Agent loop improvement plan

## Outcome

Deliver the three improvements requested for Agent loop, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Compare cartridge-native and Codex task outcomes reproducibly | [improve-agent-task-baseline](../../../agent/prds/improve-agent-task-baseline/prd.md) |
| 2. Resume interrupted runs without replaying uncertain mutations | [improve-agent-resume-boundaries](../../../agent/prds/improve-agent-resume-boundaries/prd.md) |
| 3. Trace tool dispatch to exact context and route configuration | [improve-agent-decision-attribution](../../../agent/prds/improve-agent-decision-attribution/prd.md) |

## Downside coverage

1. The loop duplicates Codex capabilities: measure incremental task value before expansion.
2. Context/cancellation semantics require maintenance: test recovery at side-effect boundaries.
3. Nested loops blur ownership: attribute policy, retries and completion to the actual executor.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [agents-query-the-tool-graph](../../prds/agents-query-the-tool-graph/prd.md), [the-agent-spawns-wakes-and-owns-sub-agents](../../../agent/prds/the-agent-spawns-wakes-and-owns-sub-agents/prd.md). Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Agent loop behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test agent
just check agent
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
