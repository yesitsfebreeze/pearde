---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: the-board-log-replays-who-did-what
---

# Sessions replays a scope's board activity in one durable order

Channel lines carry only a per-channel `seq` (`sessions.ctg/src/channels.rs`), so a scope's activity has no single order. The host transport now provides publisher-owned channels with a bounded, non-durable replay buffer (`cartridge follow <cartridge>.<channel>`, `cartridge.ctg/docs/transport.txt`) and a `trace` id on every frame (`cartridge.ctg/src/trace.rs`). Sessions stamps a scope-wide sequence and the caller's trace on each accepted post, watch and ack in its own snapshot, and publishes them on a sessions channel. Run, tool-call and spawn records stay with their owners; the trace joins them.

## Acceptance

- [ ] Two actors' interleaved posts and acks replay from `follow` in scope-sequence order, each with actor, channel, `seq` and trace, and no message text beyond the configured cap or credentials.
- [ ] After a crash between snapshot publication and channel publish, a resubscribe with `since` rebuilds from the snapshot, and a range lost to retention is named rather than skipped.
- [ ] A subscriber sees only its own scope; the scope sequence stays monotonic across restart and legacy lines without it read as `unsequenced`.

## Proof and recovery

Start: `sessions.ctg/src/channels.rs`, `sessions.ctg/src/retention.rs`, `cartridge.ctg/docs/transport.txt` (channels, `subscribe since`), tests `sessions.ctg/.cartridge/tests/integration/channel-cursors.test.ts`. First probe whether a node reads the inbound trace. Record the `just test sessions` baseline (8 failing per release-status). Gates from /Users/feb/dev/cartridge: `just test sessions`, `just check sessions` (not run). Excluded: a cross-owner total order. Rollback: the channel is derived; the snapshot stays authoritative.

## Dependencies and review

No hard prerequisites; it shares `sessions.ctg/src/channels.rs` with the chat and reference leaves, so land them in sequence. [Review history](review.md); rounds inherited, maximum five.
