---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: a-stalled-step-raises-its-own-event
needs:
- '@runtime/a-listener-subscribes-to-event-types'
---

# a-stalled-step-raises-its-own-event

When a step crosses a declared budget threshold, emit one attributable stall event. Emit once per escalating threshold; the event informs a watcher and does not cancel the step or change its outcome.

## Acceptance

- [ ] A step held past its budget emits exactly one stall event naming the run, the step, the tool and the elapsed time; holding it past a second threshold emits exactly one more.
- [ ] A step finishing inside its budget emits none.
- [ ] The stall event alone leaves the phase, the step and the run's outcome unchanged.
- [ ] A stall event reaches a subscribed listener and appears on the run's stream like any other event.
- [ ] A profile that declares no budget for a type emits no stall events for it.

## Proof and recovery

Start at [model_loop.rs](../../../model_loop.rs), [run_state.rs](../../../run_state.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test agent` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-stalled-step-raises-its-own-event`; maximum five rounds.
