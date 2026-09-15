---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 1
review-status: passed
canonical-scope: the-board-is-channels-of-lines
needs: ["@sessions/sub-agent-sessions-record-parent-and-mailbox"]
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
---

# Durable scoped channels over the mailbox line primitive

Provide named append-only channels with ordered bounded reads and a catalogue in sessions. Reuse the authenticated mailbox authority and line codec/append rules; `session:<id>` addresses the existing recipient mailbox without migration or duplicate storage. Other channel names are shared only inside the host-provisioned actor scope. This canonical delta preserves the [historical active source and claim](../../../../memos/work/root--the-board-is-channels-of-lines.md) verbatim; it does not reclaim or certify that historical worker's work.

## Acceptance

- [x] Actual SDK concurrent posts assign distinct per-channel sequences, retry by message ID is idempotent, and channel lines/catalogue survive restart.
- [x] Forged senders/scopes, unauthorized direct reads, unsafe names/paths, oversized text and full/corrupt stores are refused without changing accepted data.
- [x] Ordered reads and catalogue obey row/byte limits with explicit remaining counts; cursors beyond the end return empty, and legacy send/mailbox lines are visible through the direct-channel alias without rewriting snapshots.
- [x] Pre-publication failures preserve earlier bytes; uncertain post-publication failures expose uncertainty and retries reconcile by ID. Notifications follow accepted publication only.

[Measured baseline](baseline.json): the current real SDK rejects post/read/channels, while direct authenticated mailboxes already persist ordered lines. Existing native and SDK mailbox tests remain compatibility gates. Single active writer is the existing snapshot contract. Durable read acknowledgements, watcher/wake routing, roster prompts and a global cross-channel causal journal remain their separate existing PRDs; this leaf exposes no execution or approval authority.

## Review

No scored review for the historical active memo was found in the round-1 inventory; it was explicitly excluded as active. First concrete delta review is pending, with any discovered prior rounds to be inherited before proceeding.

## From the retired work memo

Folded 2026-09-15 from `work/the-board-is-channels-of-lines.md` (status active, owner sys-38/implementer-the-board-is-channels-of-lines, estimate 1d). The PRD state above is authoritative.

> The sessions store serves named channels of append-only message lines, and the per-session mailbox becomes one of them

### Outcome

A message board lives in the sessions cartridge: named channels, each an ordered
append-only sequence of short message lines that survives restart. `post` appends
one line to a channel and returns its sequence number; `read` returns a channel's
lines from a sequence onward, newest-bounded by a limit; `channels` lists every
channel with its last sequence and last activity. Every line carries `from`, `ts`,
`seq` and the run it came from, so a reader can always ask who said it and when.

The existing per-session mailbox is the direct-message case of this store, not a
second implementation: a session's mailbox is the channel addressed to that
session, and `send`/`mailbox` keep their current shape over it.

### Check

- [ ] `post{channel,from,text}` returns an increasing `seq` per channel, and two
      concurrent posts to one channel get distinct sequence numbers with no lost
      line.
- [ ] `read{channel,since,limit}` returns lines in order from `since`, and a
      `since` beyond the end returns empty rather than an error.
- [ ] Restarting the cartridge returns the same channels, lines and sequence
      numbers from disk.
- [ ] `sessions send{id,from,text}` and `sessions mailbox{id}` keep their current
      behaviour, proven by the existing mailbox test passing unchanged while the
      line is also readable through `read` on that session's channel.
- [ ] A line over the configured length cap is refused with a message naming the
      cap, and the channel is unchanged.
- [ ] A post to an unknown channel creates it; `channels` then lists it with its
      last sequence and activity time.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. The mailbox already exists and is close: `sessions
send{id,from,text}` appends `{"from","to","text","ts"}` as one JSON line to a
lazily created buffer named `mailbox` on the target session and notifies with
that session as the event target; `mailbox{id}` parses the lines back
(`builtin/sessions/main.rs:666`, `:682`). Sessions already persist per session
under `sessions.dir`, so durability is the store's existing property. What is
missing is a name other than a session id, a sequence number, and a read cursor:
`mailbox` returns the whole buffer, which is exactly what a swarm must not do
every turn.

### Spec

Channels are keyed by name. A session-addressed channel keeps the session's
snapshot as its home so a child's messages travel and expire with it; a named
public channel is stored beside the sessions in `sessions.dir` under its own
file. One append path, one parse path, both reached by the mailbox ops and the
channel ops.

A line is `{seq, channel, from, to?, ts, run?, text}`. `seq` is per channel and
monotonic; the store assigns it under the same lock that appends, so it is the
ordering every reader and the log agree on. `text` is capped (default 512 bytes,
configured, refused above it) — the cap is what keeps a channel readable and the
token cost of catching up bounded.

`read` takes `since` and `limit` and is the only way to catch up, so an agent
pays for what it has not seen rather than for the channel's history. Events keep
their current shape: a post notifies with the channel as the target, which is
what lets [the-agents-chat-through-one-tool](../the-agents-chat-through-one-tool/prd.md) wake a watcher.
