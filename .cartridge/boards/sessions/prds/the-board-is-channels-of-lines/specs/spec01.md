---
complexity: medium
footprint: ["src/roster.rs","src/main.rs","src/mailbox.rs","src/channels.rs",".cartridge/tests/unit/main/channel_tests.rs",".cartridge/tests/integration/channels.test.ts",".cartridge/docs/channels.md","Cargo.toml","src/lib.rs","src/change_record.rs","src/changes.rs",".cartridge/tests/unit/main/change_records_tests.rs"]
---

# Scoped named channels and direct mailbox aliases

Native sessions operations `post{channel,text,message_id?,run?}`, `read{channel,since?,limit?,max_bytes?}` and `channels{limit?,max_bytes?,after?}` require existing host mailbox credentials. Reuse its authenticated actor/scope and immutable owner lineage; never accept copied from/scope/parent metadata as authority. A supplied from must match authenticated actor. No credential configuration means these new operations are unavailable; old send/mailbox retain their current native compatibility. Named channels share within one credential scope. Direct aliases `session:<id>` permit same-scope post and only recipient read, exactly as mailboxes; catalogue exposes only the caller's direct alias plus its scope's named channels. All new read/catalogue operations are observational and cannot acknowledge mailbox delivery.

Names are 1..128 UTF-8 bytes restricted to ASCII letters/digits/dot/underscore/hyphen, excluding leading dot; session: is the reserved direct form with existing safe session IDs. Optional run is a bounded 128-byte caller reference, explicitly not authenticated execution provenance or authority. New named rows carry channel/from/ts/seq/message_id/run?/text, with host-derived from and owner timestamp. Direct alias projection adds channel and nullable run to the existing mailbox row without rewriting it. Default text cap512 UTF-8 bytes; immutable channel_text_bytes permits1..512 for new channel posts (ordinary legacy send retains its existing512 cap). Replies name the configured cap on refusal.

Extract the existing mailbox record validation, monotonic allocation, text/message-ID validation and idempotent append logic into reusable mailbox helpers, preserving legacy normalization and all send/mailbox/read/ack behavior. Named scope storage uses those same helpers; it does not create another direct inbox. One versioned scope snapshot under sessions.dir/.channels/<SHA256(scope)>.json holds <=128 named channels, <=10000 total lines and <=8MiB serialized bytes. Scope and channel names are stored and checked inside the snapshot. No process-global journal sequence is claimed: channel seq is monotonic only inside that channel. Existing session snapshots remain their mailbox home and retention semantics. Named channels have no deletion/eviction API in this leaf; full capacity fails unchanged.

Resolve safe owned directory components, refuse symlink/nonregular or mismatched/corrupt scope files, and bound reads before parsing. Serialize each named scope's read/modify/publish under a scope gate. Use existing temporary-file + write + file-sync + rename + directory-sync publication pattern, factoring a shared helper only where it preserves session fault behavior. Compare the observed regular-file revision (or expected absence) again before rename; a changed target is a conflict, not permission to overwrite. This optimistic check does not defeat hostile filesystem races or provide cross-process locking. Reload visible state after uncertain publication; do not invent rollback. Message ID+authenticated sender deduplicates exact payload (including run), with conflict on mismatch. One active writer per store remains explicit; no cross-process serialization claim. No catalogue sidecar: metadata derives from the same committed snapshot, avoiding a split update. Local post notifications retain channel target and are emitted only for newly accepted commits; failed, uncertain or duplicate operations never assert a fresh accepted post. Durable wake recovery remains a later consumer responsibility.

Read returns earliest seq strictly greater than since(default0), ordered, default20/max100 rows and default8192/max32768/min1024 full JSON bytes; include last_sequence, through, remaining and omitted, never silently skip an unread prefix. A request since beyond last returns empty. An oversized next line that cannot fit output returns an explicit cap error rather than an advancing cursor. The historical phrase newest-bounded is refined to contiguous catch-up, preventing message loss; no durable cursor is advanced here. Catalogue sorted by channel name has default20/max100 rows, the same byte limits, an exclusive after name, per-channel last_sequence/last_activity plus total/omitted/next. A catalogue is one bounded scope snapshot plus caller mailbox snapshot, with separate revisions/observed_at and explicit partial state when the mailbox source is unavailable; no atomic cross-file claim.

## Acceptance

- [x] Unit faults cover write/file-sync/rename/directory-sync for named publication and unchanged direct mailbox paths, plus malformed/truncated/symlink/replaced files, unsafe channel names and full-store caps. Accepted bytes survive refused posts, and uncertain retries reconcile by message ID.
- [x] Actual SDK fixture uses two actors in one scope and one in another; concurrent posts, duplicate retry, forged sender/scope and unauthorized inbox reads are tested, with secrets absent from storage/replies. Restart retains exact sequence/catalogue and direct aliases show legacy and newly posted lines through the same mailbox buffer.
- [x] Exact row/byte bounds, inclusive delivery continuity after exclusive since, beyond-end empty, catalogue pagination and source revision/partial reporting are verified. Original mailbox and retention tests remain unchanged and pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test sessions
```

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just build sessions
SESSIONS_BINARY="$PWD/target/tool-result-contract/debug/sessions" HARNESS_BINARY="$PWD/target/tool-result-contract/debug/harness" bun test ../sessions.ctg/.cartridge/tests/integration/channels.test.ts ../sessions.ctg/.cartridge/tests/integration/mailbox.test.ts ../sessions.ctg/.cartridge/tests/integration/retention.test.ts
```

Also run just check sessions and verify the mailbox prerequisite receipt at the final shared source footprint. Tests use disposable stores only. Preserve historical memo claim and source; coordinator owns canonical map and receipt refreshes.
