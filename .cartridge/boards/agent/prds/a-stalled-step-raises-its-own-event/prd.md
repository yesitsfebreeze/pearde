---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: a-stalled-step-raises-its-own-event
footprint:
- /Users/feb/dev/cartridge/agent.ctg/cartridge.json
- /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
- /Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
---

# a-stalled-step-raises-its-own-event

A stuck run says so. When a model stream or tool call crosses a budget declared for its step type, the agent notifies one attributable stall event, once per escalating threshold. The event informs a watcher; it never cancels the step or changes its phase or outcome.

## Acceptance

- [ ] Under paused test time, a step held past its budget emits exactly one stall event naming run, step, tool and elapsed time; past a second threshold, exactly one more.
- [ ] A step finishing inside its budget, or a step type with no declared budget, emits none.
- [ ] A stall event alone leaves phase, step and outcome unchanged; finish, cancel or restart leaves no pending stall timer.
- [ ] A subscriber to the agent's channel receives the stall event in order with the run's other events.

## Proof and recovery

Baseline (agent `fad6d3b`): no budget setting in `agent.ctg/cartridge.json` and no stall emission in `agent.ctg/src`. Active calls are tracked in `Live.active` (`agent.ctg/src/lib.rs:125-140`); events leave through `Run::emit` (`agent.ctg/src/lib.rs:544`), which notifies listeners and publishes on the `agent` channel. The host's channel `subscribe` with `since` replay (cartridge `c9ef10b`) already delivers to subscribers, so this leaf drops its need on `@runtime/a-listener-subscribes-to-event-types`. Budgets are declared settings; an absent budget settles to null and disables stall events.

Precondition without a PRD: agent still targets the host API removed in cartridge `ee7e295` (`agent.ctg/src/main.rs:14,42`); no agent gate builds until it is ported to declared events.

First probe: a failing test in `run_state.rs` using `driver_tool(_, false)` under `tokio::time::pause`. Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run for this plan. Failure: a timer error drops that stall event and never affects the step; with no subscriber the event still reaches the channel's bounded replay buffer.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
