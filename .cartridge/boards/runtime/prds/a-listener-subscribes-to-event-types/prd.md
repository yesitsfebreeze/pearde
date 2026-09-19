---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 100
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: a-listener-subscribes-to-event-types
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/transport/cartridge.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs
---

# a-listener-subscribes-to-event-types

A stream subscriber is told when replay cannot cover the gap since its last envelope. Listening by event type is already delivered: `listen` declarations, schema checks, per-edge tokens, timeouts and bounded queues ([transport.txt](../../../../../../cartridge.ctg/docs/transport.txt)). What remains is in the channel code in [transport/cartridge.rs](../../../../../../cartridge.ctg/src/transport/cartridge.rs). `publish_kind` keeps a bounded `history` and an in-memory `seq`. `join` replays envelopes newer than `since` without saying when the oldest retained one is already past it. The count also starts again at 1 when a publisher restarts, so a resubscribe from an old `last` can drop new envelopes. Both come from reading the source and are not reproduced yet.

## Acceptance

- [ ] A subscriber resubscribing from a `since` older than the retained history receives one `gap` envelope naming the first and last missing sequence numbers, followed by the retained replay in order.
- [ ] After the publisher restarts, a resubscribe from the old cursor still receives every new envelope (for example, a per-generation epoch goes into the envelope and `since`).
- [ ] A slow subscriber is still disconnected at a full queue and the publisher never blocks. Existing `streams_replay_and_then_deliver_live` keeps passing.

## Proof and recovery

First add failing reproductions for both cases next to `streams_replay_and_then_deliver_live` in [host.rs tests](../../../../../../cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs). Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`. Not run. Compatibility: subscribers that ignore `kind: gap` keep working. There is no durable journal: retained history stays bounded in memory.

## Decision (2026-09-19, ASP coordinator cartridge-1f)

The `needs` entry on `@agent/an-event-declares-its-type` is removed. This
PRD's own text says "No hard prerequisites", and the evidence agrees: the gap
envelope and the epoch live in `publish_kind` and `join` in
`src/transport/cartridge.rs`, which carry any channel's envelopes and never
read an event's declared type. The entry held the whole ring chain
(`@root/the-event-ring-...`, the ASP event child and the JEV rollup) behind a
question about the agent's projection frame that this change does not touch.

## Dependencies and review

No hard prerequisites. The acceptance overlaps `documents-own-live-processes/document-event-activation` ("overflow reports a gap"); this leaf is the canonical owner of the channel gap. [Review](review.md): inherits 2 rounds.

## From the retired work memo

Folded 2026-09-15 from `work/a-listener-subscribes-to-event-types.md` (status open, estimate 1d). The PRD state above is authoritative.

> A cartridge subscribes to the run stream by event type and answers by posting, never by acting on the run directly

### Outcome

A cartridge can listen to what agents are doing without reading a transcript. Each
event a run writes is published with its type, session and run, and a cartridge
registers the types it wants and receives them in order as they are written. That
is how tools connect to each other: a memory, a board bridge, a supervisor or a
metric sees the stream it cares about and nothing else.

A listener's only way back in is a post. It cannot cut a step, answer an approval
or change a phase, because the run task is the one thing deciding what the run
does; a listener that wants the run to change course posts an event and lets
[a-priority-event-unblocks-the-step](../../../agent/prds/a-priority-event-unblocks-the-step/prd.md) decide.

A listener never holds a run up. It is dispatched without the run waiting on it,
bounded, and a listener that errors or hangs is dropped and recorded rather than
stalling the agent.

### Check

- [ ] With a listening cartridge in the profile, every event of a run reaches it
      once, in stream order, carrying its type, session and run.
- [ ] A listener registered for one type receives only that type.
- [ ] A listener that errors, and a listener that never returns, leave the run's
      timing and journal unchanged; both are recorded as failed delivery.
- [ ] A listener that posts back produces exactly one event on the stream,
      attributed to that listener and not to the agent.
- [ ] With the listening cartridge removed from the profile, the run's journal,
      projections and telemetry are unchanged, and no subscription remains.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. The host already carries listeners: a cartridge registers one
over the wire and the host dispatches to it (`core/cartridge.rs:407`,
`core/sdk.rs:137,279`, `core/lua.rs:195`). The run already publishes every stage
through `emit`, which stamps `session`, `run`, `seq`, `revision` and the kind
(`builtin/agent/lib.rs:561`). What is missing is that these are two unconnected
facts: `emit` notifies, nobody subscribes by type, and the events a listener would
want are the ones `emit` currently uses for the UI's own liveness.

The delivery guarantee to aim for is the honest one, not the expensive one: this
is a notification channel over a journal that is already durable, so a listener
that missed an event reads the stream, and the subscription does not become a
second source of truth.
