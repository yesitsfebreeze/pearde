---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
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
