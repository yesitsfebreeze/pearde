---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: the-swarm-talks-on-a-board
needs:
- '@sessions/an-agent-is-one-lookup-from-the-roster'
- '@sessions/the-agents-chat-through-one-tool'
- '@sessions/a-board-message-is-a-reference-not-a-payload'
- '@sessions/the-board-log-replays-who-did-what'
---

# the-swarm-talks-on-a-board

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [an-agent-is-one-lookup-from-the-roster](../an-agent-is-one-lookup-from-the-roster/prd.md)
- [the-agents-chat-through-one-tool](../the-agents-chat-through-one-tool/prd.md)
- [a-board-message-is-a-reference-not-a-payload](../a-board-message-is-a-reference-not-a-payload/prd.md)
- [the-board-log-replays-who-did-what](../the-board-log-replays-who-did-what/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-swarm-talks-on-a-board`; maximum five rounds.
