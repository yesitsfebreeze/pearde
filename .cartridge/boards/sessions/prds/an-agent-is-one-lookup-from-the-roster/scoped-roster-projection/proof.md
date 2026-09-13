# Scoped roster implementation proof

Source commit `a306370f10b78d94365b7832ce22ce8d10c09487` in Sessions. The source tree is clean; shared PRD collection remains coordinator-owned.

The existing immutable mailbox membership check is reused by a new read-only roster operation. Only bounded allowlisted checkpoint metadata is copied from the session index. Named channel lines and reader registry share one validated source snapshot; other actors' inboxes and transcripts are excluded. The caller's direct unread count is separate. Response digest, source revisions, scan/row/byte omissions, unknown phase duration and partial evidence are explicit.

- Public `just test sessions`: **82 passed**, including four new roster unit cases for legacy phase evidence, private/cyclic parents, the 4096-entry scan limit and complete JSON byte/digest bounds.
- Public `just check sessions` and `just build sessions`: passed.
- Reviewed actual SDK subset: **12 tests / 473 assertions** across roster, cursors, channels and mailbox.
- Full compatibility: **22 tests / 611 assertions**, also exercising retention with real harness, client mapping and actual runtime observations.

The 20-visible-session SDK fixture includes an out-of-scope actor and a legacy forged parent. It checks exact authorized IDs, private-parent suppression, whole-row byte omissions, hidden transcript/pending/error/inbox markers and every JSON snapshot unchanged. Copied identity/scope metadata cannot override host credentials, and generic APIs cannot rewrite private lineage. Another fixture changes child phase/step without any post, acknowledges one actor's delivery while later posts and the other actor's unread counts remain, restarts the native process, then corrupts only the disposable channel snapshot and verifies partial metadata without loss of phase evidence. A malformed other-actor inbox does not affect the caller's roster; the actual inbox owner receives explicit partial status. Equal timestamps in distinct named channels are marked ambiguous.

`src/roster.rs` is the only new transitive module needed in older receipts whose footprint includes `src/main.rs`. The scoped child already binds main/mailbox/channels/roster and its tests/docs. Coordinator must refresh dependency receipts at this commit before collection. No old receipt or shared map was edited by this worker.

Limitations remain as reviewed: host-provisioned bearer actor credentials, native legacy APIs host-trusted, loaded records do not attest a running process, no phase-start clock, separate in-memory/named observations under the existing one-writer contract, and no hostile-filesystem atomicity claim. Prompt inclusion and original roster parent completion still require the separately reviewed Harness adapter.
