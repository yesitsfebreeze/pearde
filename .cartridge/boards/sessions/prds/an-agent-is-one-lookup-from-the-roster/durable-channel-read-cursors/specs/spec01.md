---
complexity: medium
footprint:
- src/main.rs
- src/mailbox.rs
- src/channels.rs
- .cartridge/tests/unit/main/channel_cursor_tests.rs
- .cartridge/tests/integration/channel-cursors.test.ts
- .cartridge/docs/channel-cursors.md
---

# Acknowledge only the named-channel batch delivered to this actor

Add native `channel_watch{channel}`, `channel_unwatch{channel}`, `channel_read{channel,limit?,max_bytes?}` and `channel_ack{channel,receipt,expected_cursor}` using existing host mailbox credentials. Only named channels are accepted; direct inbox delivery remains existing mailbox_read/ack. The authenticated actor owns the watch and cursor; caller-supplied actor/from/scope/parent metadata cannot select another actor's progress. A supplied from must match. Generic session create/update/save cannot mutate this separate owner scope registry. A watch may precede the first post, so a missing channel initially has last_sequence0.

Extend the existing version1 named scope snapshot with an optional owner-managed readers list, default empty and omitted when empty. Each authenticated actor has at most16 watched names; at most256 actor entries per scope, still inside the existing8MiB file cap. Reject duplicate actors/channels, malformed receipts, cursor beyond last sequence or mismatched scope. Only credential-authenticated operations mutate these entries. Unwatch explicitly removes its cursor/receipt; rewatch starts from0 and may redeliver. Empty actor entries are removed. No accepted channel line is deleted, repaired or rewritten as a migration. Older snapshots remain readable; older binaries may refuse newer optional owner data rather than silently discard it.

Reuse mailbox's bounded delivery and compare/ack receipt logic by extracting the existing cursor validation, batch selection and acknowledgement into helpers. Existing direct read/ack operations use the same helpers and keep response/notification behavior. Named channel_read requires an active watch and takes contiguous records after acknowledged cursor, default20/max100 rows and default8192 bytes, permitted1024..32768. It persists one pending receipt but does not acknowledge. A new read supersedes the older receipt; acknowledgement needs that exact receipt and expected base, and advances only through its delivered boundary. Concurrent later posts remain unread. Empty reads return no receipt, never skip data. An unfit next record fails without cursor changes. Names and text remain ordinary data, never execution authority.

Use the same scope gate and atomic snapshot publication as posts, retaining revision checks, pre-publication preservation and explicit directory-sync uncertainty. After uncertain ack, another read exposes the visible acknowledged cursor; retrying the old receipt may explicitly conflict and must not advance further. After uncertain read, no acknowledgement is presumed and a fresh read can redeliver. No cross-process writer safety claim is added. Roster later reads this registry; watch here records subscription intent only, without attaching runtime event handlers or starting/waking a model run.

## Acceptance

- [x] Actual SDK restart preserves watches, pending receipts and acknowledged progress; actorB cannot acknowledge actorA's receipt, and a new read rejects an older receipt.
- [x] Concurrent post after a read remains unread after ack; repeated same-time readers cannot skip a line, unwatch/rewatch explicitly redelivers, and row/byte caps refuse an unfit next record without progress.
- [x] All write/file-sync/rename/directory-sync faults leave lines intact, with exact visible-state reconciliation; legacy channel snapshots, prior mailbox tests and generic-field forgery protections pass unchanged.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just test sessions
```

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just build sessions
SESSIONS_BINARY="$PWD/target/sessions-mapping/debug/sessions" bun test ../sessions.ctg/.cartridge/tests/integration/channel-cursors.test.ts ../sessions.ctg/.cartridge/tests/integration/channels.test.ts ../sessions.ctg/.cartridge/tests/integration/mailbox.test.ts
```

Also public just check sessions; coordinator refreshes shared channel/mailbox receipts before collection. All failure fixtures use disposable stores; no live cursor advancement occurs during development.
