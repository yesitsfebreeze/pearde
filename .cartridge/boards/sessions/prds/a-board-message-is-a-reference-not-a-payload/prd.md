---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: a-board-message-is-a-reference-not-a-payload
needs:
- '@sessions/the-agents-chat-through-one-tool'
---

# A channel post carries typed references beside bounded text

Channel lines today accept only `channel`, `from`, `ts`, `seq`, `message_id`, `run` and `text` ≤512 bytes (`records` in `sessions.ctg/src/channels.rs`). Add an optional bounded `references` array whose entries name an owner-qualified target: `memo` path@revision, `session` id, `channel` name#seq, or `file` owner/path#range. Sessions validates shape and size and dereferences only its own session/channel forms; other owners' targets are resolved by the reader through its own declared needs, so sessions carries no sibling protocol (root decision `a-cartridge-brings-its-own-surface.md`).

## Acceptance

- [ ] A second authorized actor reading a post gets every reference back verbatim; its `session`/`channel` references resolve through sessions to the exact line or a named `missing`/`out_of_scope` result.
- [ ] Malformed forms, over-count or over-byte reference lists, and an unknown kind are refused before append, leaving the snapshot bytes unchanged; the same `message_id` with changed references conflicts.
- [ ] A reference into another scope discloses nothing beyond `out_of_scope`; legacy lines without references still read and replay unchanged.

## Proof and recovery

Start: `sessions.ctg/src/channels.rs`, `sessions.ctg/src/mailbox.rs` (`normalize`), `sessions.ctg/.cartridge/docs/channels.md`, tests `sessions.ctg/.cartridge/tests/unit/main/channel_tests.rs` and `sessions.ctg/.cartridge/tests/integration/channels.test.ts`. First record the current `just test sessions` baseline: release-status notes 8 failing sessions tests, which must be named before new failures are judged. Gates from /Users/feb/dev/cartridge: `just test sessions`, `just check sessions` (not run). Caps are settings in `sessions.ctg/cartridge.json`, not constants. Rollback: the field is optional; reverting leaves existing snapshots readable.

## Dependencies and review

Needs the agent-facing channel surface. [Review history](review.md); rounds inherited, maximum five.

## From the retired work memo

Folded 2026-09-15 from `work/a-board-message-is-a-reference-not-a-payload.md` (status open, estimate 1d). The PRD state above is authoritative.

> Agents exchange pointers into the shared record, so a swarm's messages stay small while its context stays complete

### Outcome

A message names where something is, not what it says. A board line carries
references — a memo path, a session id, a channel and sequence, a file path and
line, a run id — and the receiver resolves what it needs through the tools it
already has. Pasted file content, restated plans and quoted transcripts are
refused by the line cap rather than tolerated, so the swarm's token cost grows
with the number of things said and not with the size of what they are about.

The shared context is the record and the store, both already readable by every
agent. The board carries the pointers into them.

### Check

- [ ] A reference in a line resolves for another session: given a posted memo
      path and a channel sequence, a second agent reads both through existing
      tools without further messages.
- [ ] A line that inlines a file body exceeds the cap and is refused; the same
      information posted as a path and a line range is accepted.
- [ ] The protocol memo states the reference forms, and a probe shows an agent
      following one to the thing it names.
- [ ] Measured on one recorded multi-agent task, the board's total posted bytes
      are a small fraction of the bytes the referenced material would have cost;
      the result records both numbers.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. Everything a message would want to quote is already
addressable: memos are `<kind>/<name>.md` in a record every enabled cartridge
shares, `tool.memo` resolves and reads them, sessions and runs have ids, and
channel lines will have sequence numbers from
[the-board-is-channels-of-lines](../the-board-is-channels-of-lines/prd.md). What is missing is the discipline and its
enforcement point — without a cap, a model will paste, and a swarm's cost becomes
quadratic in what it has read.

### Spec

Define the reference forms once, in the protocol memo, and keep them the ones the
system already uses: `[[memo-name]]` for the record, `session:<id>`,
`run:<id>`, `<channel>#<seq>`, `path:line`. No new resolver: each form is
already resolvable by a tool the agent has.

The cap is the enforcement. A line that does not fit is refused with the cap in
the message, which teaches by failing at the moment of the mistake rather than by
a prompt instruction the model may skip. Where a long payload is genuinely
needed, the answer is to write it as a memo and post its name — which also makes
it durable and reviewable instead of stranded in a channel.

This is the same economy the harness already applies to context: bounded rendered
blocks plus retrievable detail. The board inherits it rather than inventing a
second policy.
