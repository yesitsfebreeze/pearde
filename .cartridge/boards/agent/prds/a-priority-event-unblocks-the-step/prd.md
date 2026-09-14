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
canonical-scope: a-priority-event-unblocks-the-step
needs:
- '@agent/a-live-run-accepts-events-from-outside'
footprint:
- /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
- /Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/src/stream.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
---

# a-priority-event-unblocks-the-step

A post marked priority interrupts the current step and the same run continues. Cancellation and preemption stay distinct signals: `cancel` still ends the run; priority requests coalesce by accepted post ID. Every projected tool group is closed with explicit interrupted/unknown outcomes before the event is inserted; late effects stay available for reconciliation although late responses are not appended.

## Acceptance

- [ ] Priority during a model stream keeps the partial reply as an interruption record, carries partial and event into the next request, and the run reaches `completed` without a second run.
- [ ] Priority during a cancellable tool sends one cancel for that call identity; a committed late effect is recorded known or unknown and never replayed.
- [ ] Uncancellable work finishes before insertion and the journal records the wait; a pending approval stays unanswered and bound to its original call and arguments.
- [ ] Cancel and priority released at the same boundary end `cancelled`; no priority path can produce `cancelled`.

## Proof and recovery

Baseline (agent `fad6d3b`): one `watch<bool>` cancel channel (`agent.ctg/src/lib.rs:127`) makes every cut terminal. The stream already returns `StreamOutcome::Cancelled` with the visible partial (`agent.ctg/src/stream.rs:120,144`); exact-call cancel is sent once (`agent.ctg/src/lib.rs:149,428`); `close_pending` writes `interrupted-outcome-unknown` (`agent.ctg/src/model_loop.rs:60`). Split that signal; add no second cancellation path.

Precondition without a PRD: agent still targets the host API removed in cartridge `ee7e295` (`agent.ctg/src/main.rs:14,42`); no agent gate builds until it is ported to declared events.

First probe: turn `cancel_during_cancellable_tool_invokes_exact_call_cancel_and_no_late_append` (`.cartridge/tests/unit/run_state.rs:419`) into a failing priority variant. Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run for this plan. Failure: if continuing after the cut errors, the run ends `failed` with outcomes preserved, never replayed; existing transcripts are unchanged.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
