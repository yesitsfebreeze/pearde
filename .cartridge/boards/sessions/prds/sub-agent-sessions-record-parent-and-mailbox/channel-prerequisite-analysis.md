# Canonical mailbox and historical channels boundary

The root work-map maps source `sub-agent-sessions-record-parent-and-mailbox`
(source entry near line 1454, canonical entry near line 4335) to
`@sessions/sub-agent-sessions-record-parent-and-mailbox`. Its preserved source alias
is `.cartridge/memos/work/root--sub-agent-sessions-record-parent-and-mailbox.md`.

There is no source/canonical work-map entry for `the-board-is-channels-of-lines`.
The separate memo `.cartridge/memos/work/root--the-board-is-channels-of-lines.md`
still records historical active owner `sys-38/implementer-the-board-is-channels-of-lines`
and unchecked checks. It is preserved unchanged. Current sessions source at b772c6e
has per-session mailbox buffers but no named channel store, catalogue or cursor API.
Roster, agents-chat and board-log PRDs reference that memo only in prose; roster
has no executable needs edge to a channel implementation.

Canonical mailbox scope covers direct recipient snapshots, authorized sender and
recipient membership, durable monotonic message identities, bounded read receipts
and restart-safe cursor acknowledgement. It must reuse the existing mailbox buffer.
This provides a direct-message primitive for future channels but does not implement
arbitrary named/public channels, channel catalogue/activity, channel membership,
watch subscriptions, idle wake delivery or global channel journal ordering. Those
requirements remain explicit delta for coordinator normalization before roster work.
No claim or completion is inferred from the old historical marker, and no new
identity is invented to reset review history.
