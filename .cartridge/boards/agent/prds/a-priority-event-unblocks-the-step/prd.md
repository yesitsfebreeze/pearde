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
canonical-scope: a-priority-event-unblocks-the-step
needs:
- '@agent/a-live-run-accepts-events-from-outside'
---

# a-priority-event-unblocks-the-step

Keep cancellation and preemption as distinct control signals. Terminal cancel takes precedence; priority requests coalesce by accepted event ID and preserve the same run. Complete every projected tool group with explicit interrupted/unknown outcome records before inserting the priority event; retain late-effect reconciliation separately from late-response display.

## Acceptance

- [ ] Cancel and priority released at the same barrier end in cancelled, never a resumed terminal run.
- [ ] Priority during a cancellable call sends one cancel for that identity; a committed late effect remains known/unknown for reconciliation and is not replayed.
- [ ] Uncancellable work completes before event insertion and records wait duration; pending approval remains unanswered and still bound to the original revision/arguments.

## Proof and recovery

Start at [model_loop.rs](../../../model_loop.rs), [run_state.rs](../../../run_state.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test agent` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-priority-event-unblocks-the-step`; maximum five rounds.
