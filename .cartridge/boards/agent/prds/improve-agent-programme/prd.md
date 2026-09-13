---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: agent
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-agent-programme
needs:
- '@agent/improve-agent-task-baseline'
- '@agent/improve-agent-resume-boundaries'
- '@agent/improve-agent-decision-attribution'
---

# Agent loop improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Compare cartridge-native and Codex task outcomes reproducibly](../improve-agent-task-baseline/prd.md)
- [Resume interrupted runs without replaying uncertain mutations](../improve-agent-resume-boundaries/prd.md)
- [Trace tool dispatch to exact context and route configuration](../improve-agent-decision-attribution/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-agent-programme`; maximum five rounds.
