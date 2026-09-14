---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: the-swarm-talks-on-a-board
needs:
- '@sessions/an-agent-is-one-lookup-from-the-roster'
- '@sessions/the-agents-chat-through-one-tool'
- '@sessions/a-board-message-is-a-reference-not-a-payload'
- '@sessions/the-board-log-replays-who-did-what'
---

# the-swarm-talks-on-a-board

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation. Channels, cursors and the roster already exist in `sessions.ctg/src`; the open leaves add the agent tool and post event, typed references, and the ordered replay.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] At one pinned sessions revision, a two-actor fixture posts with references, restarts the sessions node mid-exchange, and replays the exchange from `follow` with no lost or duplicated line.
- [ ] An actor presenting another actor's `from`, or a reference outside its scope, is refused during that run, and the refusal appears in neither actor's unread lines.
- [ ] Remaining limitations are recorded at that revision, including that coalescing wake bursts into one run is a harness listener's outcome, not this parent's.

## Work items

- [an-agent-is-one-lookup-from-the-roster](../an-agent-is-one-lookup-from-the-roster/prd.md)
- [the-agents-chat-through-one-tool](../the-agents-chat-through-one-tool/prd.md)
- [a-board-message-is-a-reference-not-a-payload](../a-board-message-is-a-reference-not-a-payload/prd.md)
- [the-board-log-replays-who-did-what](../the-board-log-replays-who-did-what/prd.md)

## Integration gate

From /Users/feb/dev/cartridge: `just test sessions` against the baseline recorded by the first leaf (release-status lists 8 failing sessions tests), plus the two-actor fixture added to `sessions.ctg/.cartridge/tests/integration/`; neither has run for this plan.

## Review

[Review history](review.md); rounds inherited, maximum five.
