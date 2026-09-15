---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
superseded-by: "@root/run-board-dispatches-through-the-orchestrator"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: the-board-log-replays-who-did-what
needs:
- "@sessions/the-board-is-channels-of-lines"
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

## From the retired work memo

Folded 2026-09-15 from `work/the-board-log-replays-who-did-what.md` (status open, estimate 2d). The PRD state above is authoritative.

> One ordered log carries every post, run, tool call and spawn with its ids, and replays a swarm's work as a followable story

### Outcome

A swarm's work is followable after the fact. Every event that matters — a post, a
run started and finished, a tool called and its outcome, a session spawned, a
wake — lands on one ordered log carrying the session, the parent, the run and the
call it belongs to. `follow` renders that log as a readable sequence: who did
what, in which channel, in what order, and what it cost. Filtering by session,
by channel or by run answers "what was this agent doing" without reading a
transcript.

The log is telemetry, not a second record: it says what happened, while the memo
record says what is true.

### Check

- [ ] A recorded two-agent task replays through `follow` as an ordered sequence
      naming each actor, its parent, its run and its channel, with no event
      unattributed.
- [ ] `follow{session}` and `follow{channel}` return subsets of the same ordering,
      and a `run` filter returns exactly that run's events.
- [ ] A tool call appears with its outcome and duration, and a failed call is
      distinguishable from a cancelled one.
- [ ] Events survive restart and keep their order across it.
- [ ] A wake caused by a post names the post that caused it, so a reader can
      follow cause to effect across two sessions.
- [ ] The log is bounded: past its configured size it rotates without losing the
      ordering of what remains, and `follow` says what was dropped.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. The pieces exist separately: sessions already records
lifecycle events and takes `message`, `run_started`, `tool_started` and
`tool_finished` records (`builtin/sessions/main.rs:171`), the harness appends a
run's telemetry block to the prompt, and `zirkle debug` mirrors every host socket
message to `.zirkle/logs/debug.log` as JSON lines. What is missing is one
ordering across sessions and a projection over it. The identity to thread is
already decided by [a-turn-carries-one-id-through-host-lua-and-bun](../../../root/prds/a-turn-carries-one-id-through-host-lua-and-bun/prd.md); this is
that id used as the join key rather than a new one.

### Spec

One append-only event file beside the channels, in the same store, with the same
per-append sequence discipline as a channel line — so a post and the run it woke
are orderable against each other without clock comparison. An event is
`{seq, ts, session, parent?, run?, call?, channel?, kind, name?, outcome?, ms?}`
and nothing more: no payloads, no arguments, no output. The story is who and
what, and references point at the rest, exactly as
[a-board-message-is-a-reference-not-a-payload](../a-board-message-is-a-reference-not-a-payload/prd.md) requires for messages.

`follow` is a read projection with filters and a limit, and its default output is
one line per event, indented by parent, so a swarm's shape shows in the log's
left edge. It is the thing a person reads when the swarm went wrong, so it is
plain text by default and structured on request.

Rotation is by size with the sequence preserved: the log is for following recent
work, not for auditing forever, and an unbounded log in a store that loads into
memory is a slow leak.
