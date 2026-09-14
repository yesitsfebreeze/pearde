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
canonical-scope: the-run-is-a-stream-of-typed-events
needs:
- '@agent/an-event-declares-its-type'
- '@agent/a-live-run-accepts-events-from-outside'
- '@agent/a-priority-event-unblocks-the-step'
- '@runtime/a-listener-subscribes-to-event-types'
- '@agent/a-stalled-step-raises-its-own-event'
---

# the-run-is-a-stream-of-typed-events

A run is an ordered stream of declared event types: an authorised sender can post into a working run, a priority post preempts the step while the run continues, cartridges follow the run by subscribing to the agent's channel, and a stalled step reports itself. The host's declared events, per-edge tokens, outcomes and replayable channels (cartridge `ee7e295`, `c9ef10b`) are the substrate; this parent coordinates the children and is not implementation work.

## Acceptance

- [ ] Each linked child passes its own review and acceptance.
- [ ] Integration: in one disposable profile a subscriber to the agent's channel sees a stalled tool step, posts a priority event, and the run ends `completed` as one replayable run whose every journal record has a declared type; `cancel` still ends `cancelled`.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

Land in order: declared types; then live posts; then priority and stall.

- [an-event-declares-its-type](../an-event-declares-its-type/prd.md)
- [a-live-run-accepts-events-from-outside](../a-live-run-accepts-events-from-outside/prd.md)
- [a-priority-event-unblocks-the-step](../a-priority-event-unblocks-the-step/prd.md)
- [a-listener-subscribes-to-event-types](../../../runtime/prds/a-listener-subscribes-to-event-types/prd.md) — `runtime` board; the host's `subscribe` with `since` may already deliver it
- [a-stalled-step-raises-its-own-event](../a-stalled-step-raises-its-own-event/prd.md)

## Integration gate

After the children pass and the agent is ported to declared events (no PRD yet), from `/Users/feb/dev/cartridge`: `just test agent`, `just test harness`, `just test runtime`. Not run for this plan.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
