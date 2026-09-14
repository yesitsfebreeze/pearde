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
canonical-scope: documents-own-live-processes
needs:
- '@runtime/a-listener-subscribes-to-event-types'
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/src/node.rs
- /Users/feb/dev/cartridge/cartridge.ctg/src/transport/cartridge.rs
- /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs
---

# A replaced subscriber resumes from its cursor without duplicates

A node watches another cartridge's channel with `cartridge.subscribe` (`src/node.rs` into `Ctx::subscribe`, `src/transport/cartridge.rs`), on ws/cartridge.ctg branch `transport-design` (`ba198f4`). Delivery is at least once; no external effect is promised exactly once. From source: the publisher replaces a repeated subscribe on one connection and drops a disconnected peer's entries, but neither is tested. Lua always passes `since: nil`, so a replaced subscriber cannot resume and silently misses envelopes published while it restarted.

## Acceptance

- [ ] Regression proof: subscribing twice to one cartridge and channel from a node delivers each later envelope once, to the newest handler.
- [ ] Regression proof: stopping or replacing the subscriber node emits `unsubscribe` at the publisher, and no envelope reaches the old generation.
- [ ] New: `cartridge.subscribe` accepts an optional `since`. A new generation resubscribing from its last `seq` receives every retained envelope after it, in order and once. Beyond retention it receives the needed leaf's `gap` envelope.

## Proof and recovery

First add tests next to `streams_replay_and_then_deliver_live` in `.cartridge/tests/unit/src/tests/host.rs`. The regression tests may pass immediately; the `since` test must fail first. Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`. They have not run, and they need the transport branch on main. Omitting `since` keeps today's behavior. The base keeps no durable journal; persisting the cursor is the subscriber's own job. Rollback: drop the optional argument.

## Dependencies and review

The need owns the gap envelope and the restart cursor shape (`seq`/epoch), so `since` follows its wire format. Shared footprint: `src/transport/cartridge.rs`. [Review](review.md): rounds 1–2 inherited; round 3 rebased.
