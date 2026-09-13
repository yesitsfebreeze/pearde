# Verified authenticated direct mailboxes

Source: `965108d9c29bce1a41a518917d6c8892e67e42bf`. [Exact source/consumer inputs and commands](proof-inputs.json).

- **51 native sessions tests passed**, retaining all 41 earlier mapping/retention/recovery/checkpoint tests, including the unchanged original parent/mailbox test.
- Public sessions check/build and harness build passed.
- **10 actual SDK integration tests, 178 assertions passed**, including prior mapping/retention/harness coverage and new credential scope, owner-lineage forgery, concurrent duplicate-safe posts, bounded receipts and restart/ack behavior.
- Write/file-sync/rename/directory-sync failures are exercised for post, read and acknowledgement. An uncertain post reconciles by message ID without a duplicate; a failed acknowledgement can reflect only its previously delivered boundary, leaving later messages unread.
- Legacy parent or nested metadata cannot grant membership; generic create/update/save lineage writes and mailbox buffer overwrite/append/close are refused. Explicit host bindings override inherited lineage. Credentials do not appear in stored snapshots or SDK reply/event frames.

All fixtures use synthetic credentials and disposable session stores. Existing
concurrent harness source was preserved and its digest is recorded. Scope and
concurrency limits remain explicit in [mailbox documentation](../../../../../../sessions.ctg/.cartridge/docs/mailbox.md) and proof inputs.

Independent review remains round 3, **95/100**, by coordinator `/root`. No criterion
was relaxed. Named/public channel work is still separate; the untouched historical
claim and exact canonical mailbox delta are recorded in
[channel-prerequisite-analysis.md](channel-prerequisite-analysis.md).

Coordinator must collect this PRD and refresh mapping, retention, recovery and the
programme receipt because their shared main.rs contract changed.
