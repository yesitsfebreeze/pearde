---
complexity: medium
footprint:
  - src/mailbox.rs
  - src/main.rs
  - src/mapping.rs
  - .cartridge/tests/unit/main/mapping_tests.rs
  - .cartridge/tests/integration/mapping.test.ts
  - .cartridge/docs/client-mapping.md
---

# spec01 — Resolve client conversations using host-owned scope

Add native sessions `mapping` lookup and `connect` resolve-or-create operations.
Only immutable host `config.client_context` supplies authenticated_client,
workspace and profile. All three nonempty values plus an explicit nonempty
`external_conversation` are necessary for durable scope; missing values use a
process/connection-scoped in-memory mapping. The host must create one scoped
sessions instance for each authenticated connection and never populate identity
from clientInfo, model arguments or unverified headers. Existing shared sessions
profiles retain connection scope. This API does not authorize existing general
sessions/buffer operations or add authentication to MCP/proxy transports.

Lookup returns scope, session ID or null, and an opaque mapping-index revision.
Connect requires `expected_revision` only when creating, reuses an existing valid
mapping, and cannot accept a target ID to adopt someone else's session. Keys hash
an unambiguous tuple of host principal/workspace/profile and explicit external ID.
Connection scope ignores metadata and does not survive a new instance; stored
session files may remain, but no reconnect mapping is invented.

Store only key-to-session references in a separate bounded versioned index under
`.client-mappings/`; preserve existing snapshots/transcripts byte-for-byte on
lookup/reconnect. Use a nonblocking OS lock, fresh disk revision comparison,
exclusive temporary file, file sync, atomic rename and directory sync. Stale
revisions, lock contention, corrupt/oversized index and missing/corrupt targets
fail explicitly without automatic replay. Creating a new empty session precedes
index publication; if publication fails, report its orphan ID and preserve it.
After rename sync failure report uncertainty and require lookup. No eviction or
legacy migration silently deletes mappings. Limit each scope input to 4096 bytes,
index to 8 MiB and 10,000 entries.

## Acceptance

- [x] Real SDK process reconnect resolves the same host-authenticated scope/external ID; copied metadata and changed principal, workspace or profile cannot resolve it.
- [x] Missing identity/scope/external ID stays connection-scoped; request fields cannot override configured identity; existing sessions remain readable.
- [x] Stale revision, concurrent lock/CAS, corrupt index/target and write/sync/rename failure preserve durable data or report explicit partial publication with orphan ID.
- [x] Lookup/reconnect preserve transcript snapshot bytes; existing recovery/checkpoint gates pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just test sessions
```

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just build sessions
SESSIONS_BINARY="$PWD/target/sessions-mapping/debug/sessions" bun test ../sessions.ctg/.cartridge/tests/integration/mapping.test.ts
```

Run public `just check sessions`. All fixtures use disposable directories and
synthetic principals. Snapshot creation remains the existing owner operation;
index errors never rewrite or repair existing transcript files automatically.
