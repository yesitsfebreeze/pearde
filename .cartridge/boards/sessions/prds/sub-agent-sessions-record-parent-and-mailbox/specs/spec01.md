---
complexity: high
footprint:
- src/main.rs
- src/mailbox.rs
- .cartridge/tests/unit/main/mailbox_tests.rs
- .cartridge/tests/integration/mailbox.test.ts
- .cartridge/docs/mailbox.md
- src/observations.rs
---

# spec01 — Authenticate direct mailboxes and acknowledge delivered batches

Reuse each recipient's existing mailbox buffer and atomic session snapshot. Add
optional host `mailbox_access` bindings from environment-backed opaque credentials
to immutable actor/scope membership; never log or return credentials. One owner
writer can serve several authenticated actors. Configured mailbox/child operations
require a valid credential; request `from`, `parent`, clientInfo and claimed scope
cannot grant authority. Legacy unconfigured native calls remain explicitly host
trusted, with existing parent/send/mailbox shapes; this is not transport auth or
access control for unrelated raw session/buffer APIs.

Authenticate `send` as its bound actor, validate recipients against immutable host
membership or a private owner-assigned lineage field set only by authenticated
child creation, and reject mismatched from/parent before persistence. Legacy parent
metadata never grants membership. A scoped child must name its authenticated actor
as parent; its authoritative lineage is committed with the child snapshot. Host
provisioning supplies that child's own credential separately.

Append monotonic per-mailbox `seq` and caller `message_id`; identical sender/ID/
payload retries return the original entry without append, conflicting reuse fails.
Old lines derive stable sequence from their persisted position and remain readable;
new writes do not rewrite them. Legacy sends without IDs generate one explicitly.
Protect managed mailbox buffers from generic overwrite/append/close. Cap new text
at 512 UTF-8 bytes, IDs at 128 bytes, and inbox storage at 10,000 records/8 MiB;
full inboxes fail without silent eviction.

`mailbox_read` serves only the authenticated actor's own inbox, ordered after its
durable cursor, at most 100 rows/32 KiB including response metadata. Persist a
fresh receipt for the exact delivered upper sequence without advancing the cursor.
`mailbox_ack` requires that receipt and expected cursor, and advances only through
its stored delivered boundary. A newer read invalidates an old receipt; posts
after a read remain unread. Crash/restart before response or acknowledgement never
skips messages. Empty reads need no acknowledgement. No read/post executes a tool,
wakes an agent or grants approval; named/group channels remain separate work.

## Acceptance

- [x] Existing parent/mailbox tests pass unchanged; real scoped SDK calls reject forged sender, parent and legacy-parent-derived membership before writing, while authenticated child lineage survives restart.
- [x] Same-ID retries append once; conflicts/oversize/missing recipients change nothing, and concurrent accepted messages receive distinct monotonic sequences across restart.
- [x] Bounded read receipts and explicit acknowledgements alter only the actor cursor; restart-before-ack, a superseding read, concurrent posts and failed persistence cannot acknowledge undelivered records.
- [x] Legacy lines remain readable without eager migration; generic mailbox corruption paths are refused and public native/SDK gates pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just test sessions
```

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just build sessions
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just build harness
SESSIONS_BINARY="$PWD/target/sessions-mapping/debug/sessions" HARNESS_BINARY="$PWD/target/sessions-mapping/debug/harness" bun test ../sessions.ctg/.cartridge/tests/integration/mapping.test.ts ../sessions.ctg/.cartridge/tests/integration/retention.test.ts ../sessions.ctg/.cartridge/tests/integration/mailbox.test.ts
```

Run public check sessions. Use only synthetic environment credentials and disposable
snapshot directories. Per-session mutation gates serialize the single active owner
writer; the existing cross-process transcript writer limitation remains explicit.
Failures preserve prior snapshots or retain the existing post-rename uncertainty
signal; no automatic message retry, delivery acknowledgement or legacy repair.
