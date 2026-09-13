---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: sub-agent-sessions-record-parent-and-mailbox
---

# sub-agent-sessions-record-parent-and-mailbox

First verify the already-described parent/mailbox implementation. The remaining contract is authenticated sender/recipient scope, durable message identity, bounded ordered reads and restart-safe cursor handling; reuse current snapshots rather than introducing a second inbox.

## Acceptance

- [ ] Creating a child records its parent and survives restart; forged parent or out-of-scope recipient is refused before writing.
- [ ] A retry with the same message ID cannot append a second logical message, and concurrent messages retain distinct monotonic sequence positions.
- [ ] Missing-session writes change nothing; current and legacy snapshots read correctly and unread cursors never acknowledge undelivered messages.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `sub-agent-sessions-record-parent-and-mailbox`; maximum five rounds.
