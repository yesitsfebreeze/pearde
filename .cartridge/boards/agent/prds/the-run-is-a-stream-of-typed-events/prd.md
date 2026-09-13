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
canonical-scope: the-run-is-a-stream-of-typed-events
needs:
- '@agent/an-event-declares-its-type'
- '@agent/a-live-run-accepts-events-from-outside'
- '@agent/a-priority-event-unblocks-the-step'
- '@runtime/a-listener-subscribes-to-event-types'
- '@agent/a-stalled-step-raises-its-own-event'
---

# the-run-is-a-stream-of-typed-events

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [an-event-declares-its-type](../an-event-declares-its-type/prd.md)
- [a-live-run-accepts-events-from-outside](../a-live-run-accepts-events-from-outside/prd.md)
- [a-priority-event-unblocks-the-step](../a-priority-event-unblocks-the-step/prd.md)
- [a-listener-subscribes-to-event-types](../../../runtime/prds/a-listener-subscribes-to-event-types/prd.md)
- [a-stalled-step-raises-its-own-event](../a-stalled-step-raises-its-own-event/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-run-is-a-stream-of-typed-events`; maximum five rounds.
