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
canonical-scope: a-live-run-accepts-events-from-outside
needs:
- '@agent/an-event-declares-its-type'
- '@sessions/sub-agent-sessions-record-parent-and-mailbox'
footprint:
- /Users/feb/dev/cartridge/agent.ctg/cartridge.json
- /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
- /Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
---

# a-live-run-accepts-events-from-outside

A working run can be told something. The agent declares and listens to a post event (recommended `agent.post`). Its outcome is `answered` only after the post is durable in the existing sessions mailbox, with message ID and sequence. The run stays the sole writer of its journal and drains posts only at whole boundaries: after a reply or a complete tool group. A post to a session with no live run stays durable and opens its next run.

## Acceptance

- [ ] A post during a tool loop lands exactly once in the journal with sender and arrival, never between an assistant tool-call message and its results, and the next assembled request carries it.
- [ ] A crash after `answered` but before drain replays the post exactly once, keyed by its mailbox message ID.
- [ ] Posting while the run turns idle neither loses an answered post nor starts two consumers; a full drain queue yields `declined` and writes nothing.
- [ ] A sender without the post edge is refused by the host; an unknown session or out-of-scope actor writes nothing.

## Proof and recovery

Baseline (agent `fad6d3b`, cartridge `c9ef10b`): the agent serves only start/status/context/cancel/answer/tools (`agent.ctg/src/lib.rs:235`). The host already authenticates senders per edge and schema-checks payloads; sessions already authenticates mailbox actors and dedupes message IDs (`sessions.ctg/src/mailbox.rs:132`). Reuse both. Drain where `pending_calls` is empty in `agent.ctg/src/model_loop.rs`; writes go through `Run::save` with `expected_revision` (`agent.ctg/src/lib.rs:521`).

Precondition without a PRD: agent still calls the removed `transport::cartridge::run`/`ctx.provide`/`ctx.call` (`agent.ctg/src/main.rs:14,33,42`). Until it is ported to declared events, no agent gate builds.

First probe: a failing post test in `run_state.rs`. Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run for this plan. Failure: a checkpoint conflict retries the drain from the mailbox cursor; `v:1` transcripts stay readable.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
