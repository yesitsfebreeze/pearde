---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
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

## Dependencies and review

No hard prerequisites. The acceptance overlaps `documents-own-live-processes/document-event-activation` ("overflow reports a gap"); this leaf is the canonical owner of the channel gap. [Review](review.md): inherits 2 rounds.
