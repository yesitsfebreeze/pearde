---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: sub-agents-share-the-terminal
needs:
- '@sessions/sub-agent-sessions-record-parent-and-mailbox'
- '@agent/the-agent-spawns-wakes-and-owns-sub-agents'
- '@ui/the-panel-switches-to-a-sub-agent'
- '@sessions/the-swarm-talks-on-a-board'
- '@agent/the-run-is-a-stream-of-typed-events'
---

# sub-agents-share-the-terminal

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [sub-agent-sessions-record-parent-and-mailbox](../../../sessions/prds/sub-agent-sessions-record-parent-and-mailbox/prd.md)
- [the-agent-spawns-wakes-and-owns-sub-agents](../the-agent-spawns-wakes-and-owns-sub-agents/prd.md)
- [the-panel-switches-to-a-sub-agent](../../../ui/prds/the-panel-switches-to-a-sub-agent/prd.md)
- [the-swarm-talks-on-a-board](../../../sessions/prds/the-swarm-talks-on-a-board/prd.md)
- [the-run-is-a-stream-of-typed-events](../the-run-is-a-stream-of-typed-events/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `sub-agents-share-the-terminal`; maximum five rounds.
