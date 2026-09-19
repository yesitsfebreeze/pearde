---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 100
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
needs:
  - "@runtime/a-listener-subscribes-to-event-types"
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

## From the retired work memo

Folded 2026-09-15 from `work/a-stalled-step-raises-its-own-event.md` (status open, estimate 1d). The PRD state above is authoritative.

> A step that runs longer than what it is for emits one stall event naming the run, the step and the elapsed time, and cancels nothing itself

### Outcome

A run that is stuck says so. A step measured against the budget declared for its
type emits, on crossing it, one event naming the run, the step, the tool it is in
and how long it has been there. That is the signal the unblock is acted on: a
watching agent or the user sees a run spending far more than the work is worth and
posts the event that redirects it.

The stall event decides nothing. It does not cut the step, change the phase or end
the run — an automatic cut would be a timeout, and a timeout guesses. Judging
whether twenty minutes is too long for *this* work is the watcher's, and the
signal exists so the watcher has something to judge.

Crossing is reported once per threshold, escalating, not repeated: a long step
produces a few events as it gets worse, never one per tick.

### Check

- [ ] A step held past its budget emits exactly one stall event naming the run,
      the step, the tool and the elapsed time; holding it past a second threshold
      emits exactly one more.
- [ ] A step finishing inside its budget emits none.
- [ ] The stall event alone leaves the phase, the step and the run's outcome
      unchanged.
- [ ] A stall event reaches a subscribed listener and appears on the run's stream
      like any other event.
- [ ] A profile that declares no budget for a type emits no stall events for it.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. The run already measures itself: `elapsed_ms`, `model_turns`,
`reasoning_bytes` and per-tool counts are accumulated and reported as telemetry on
`run_finished` (`builtin/agent/lib.rs`), and the harness already renders a live
telemetry block for the current run below the prompt frame
(`builtin/harness/README.md`). The numbers exist; they are summarised after the
fact and at the end, which is the one moment a stall no longer matters.

The active call is already tracked with its identity and cancellability while it
runs (`lib.rs:113,142`), so the step being timed is already named. What is added is
a deadline per type, an escalating threshold, and one event.
