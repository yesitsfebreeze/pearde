---
repo: /Users/feb/dev/cartridge/agent.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-agent-programme
needs:
- '@agent/improve-agent-task-baseline'
- '@agent/improve-agent-resume-boundaries'
- '@agent/improve-agent-decision-attribution'
---

# Agent loop improvement plan

Deliver the three assessed agent-loop improvements — measured task value, safe resume and dispatch attribution — with their downsides covered. This parent coordinates the children; it is not a fourth implementation task.

## Acceptance

- [ ] Each linked leaf passes its own review and acceptance.
- [ ] Integration: at one agent revision, `just test agent` and `just check agent` pass with all three leaves' fixtures, and the offline task corpus still rejects its wrong-patch fixture.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Compare cartridge-native and Codex task outcomes reproducibly](../improve-agent-task-baseline/prd.md)
- [Resume interrupted runs without replaying uncertain mutations](../improve-agent-resume-boundaries/prd.md)
- [Trace tool dispatch to exact context and route configuration](../improve-agent-decision-attribution/prd.md)

Shared footprint: resume and attribution both change `agent.ctg/src/lib.rs` and `run_state.rs`; land them in sequence. Reconcile before claiming with the active root memo `agents-query-the-tool-graph` (dispatch observations) and [the-agent-spawns-wakes-and-owns-sub-agents](../the-agent-spawns-wakes-and-owns-sub-agents/prd.md) (same `lib.rs`).

## Integration gate

Precondition without a PRD: agent still targets the host API removed in cartridge `ee7e295`, so no agent gate builds until it is ported to declared events. Then, from `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run for this plan.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).

## From the retired work memo

Folded 2026-09-15 from `work/improve-agent-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Agent loop improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Agent loop, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Compare cartridge-native and Codex task outcomes reproducibly | [improve-agent-task-baseline](../improve-agent-task-baseline/prd.md) |
| 2. Resume interrupted runs without replaying uncertain mutations | [improve-agent-resume-boundaries](../improve-agent-resume-boundaries/prd.md) |
| 3. Trace tool dispatch to exact context and route configuration | [improve-agent-decision-attribution](../improve-agent-decision-attribution/prd.md) |

### Downside coverage

1. The loop duplicates Codex capabilities: measure incremental task value before expansion.
2. Context/cancellation semantics require maintenance: test recovery at side-effect boundaries.
3. Nested loops blur ownership: attribute policy, retries and completion to the actual executor.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [agents-query-the-tool-graph](../../../root/prds/agents-query-the-tool-graph/prd.md), [the-agent-spawns-wakes-and-owns-sub-agents](../the-agent-spawns-wakes-and-owns-sub-agents/prd.md). Their current source, status and owner take precedence over a stale assessment.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Agent loop behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test agent
just check agent
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
