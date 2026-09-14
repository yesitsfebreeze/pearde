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
