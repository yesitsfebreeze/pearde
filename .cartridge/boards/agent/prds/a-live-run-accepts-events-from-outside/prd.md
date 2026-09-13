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
canonical-scope: a-live-run-accepts-events-from-outside
needs:
- '@agent/an-event-declares-its-type'
---

# a-live-run-accepts-events-from-outside

Authenticate sender and target scope at the host. A successful post acknowledgement means the event has reached the sessions-owned durable inbox, with an idempotency key and monotonic sequence. The run remains its own sole journal writer and drains accepted posts only at complete reply/tool-group boundaries.

## Acceptance

- [ ] Crash after acceptance but before drain replays the event exactly once in the projected journal using the same inbox ID.
- [ ] Posting while the run transitions to idle cannot lose an acknowledged event or start two consumers; bounded full queues refuse before acceptance.
- [ ] Forged sender, nonexistent session and cross-scope target write nothing; non-projecting types remain visible in inspection without entering model context.

## Proof and recovery

Start at [model_loop.rs](../../../model_loop.rs), [run_state.rs](../../../run_state.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test agent` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-live-run-accepts-events-from-outside`; maximum five rounds.
