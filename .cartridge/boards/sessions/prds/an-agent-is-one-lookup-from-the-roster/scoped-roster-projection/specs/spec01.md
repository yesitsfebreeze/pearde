---
complexity: medium
footprint: ["src/main.rs","src/mailbox.rs","src/channels.rs","src/roster.rs",".cartridge/tests/unit/main/roster_tests.rs",".cartridge/tests/integration/roster.test.ts",".cartridge/docs/roster.md","Cargo.toml","src/lib.rs","src/change_record.rs","src/changes.rs",".cartridge/tests/unit/main/change_records_tests.rs"]
---

# One bounded read of authorized session and channel metadata

Native `roster{access_token,limit?,max_bytes?}` authenticates through existing host credentials. Scope membership is only the host actor table or private owner lineage; general parent/agent/client metadata cannot grant it. Live means a currently loaded, undeleted session record, not an attestation of an OS process or active model. Terminal and never-run records retain explicit phases. Use the existing session index, never a parallel durable roster. Read only named scope metadata and the caller's own mailbox counts; never another actor's transcript or direct inbox. Native list/get remain their documented host-trusted APIs.

Project allowlisted fields: id, bounded name, visible parent, phase, current step/run reference, created/updated timestamps, session age, per-session revision, named watches/unread and last observed named post metadata. Phase is not_started only for an empty agent state; missing/malformed evidence otherwise yields unknown. Activity duration stays null: existing checkpoints have no phase-start timestamp. Session updated time must not become a fabricated activity-start time. Raw errors, pending tool payloads, transcript content and arbitrary agent fields are excluded. Outside-scope parent IDs are null; parent cycles are labeled and ordered deterministically. Last named post uses timestamp evidence and flags ties across channels instead of fabricating a global channel order. Message text is bounded512-byte untrusted data, with explicit source/channel/seq references.

Copy bounded session metadata under the existing index read lock, releasing it before disk I/O. Scan at most4096 index entries plus the authenticated actor; if exhausted, mark scope_scan_limited with unknown total rather than reporting a complete roster or the global number of other-scope sessions. Filter membership before output. Sort visible acyclic parent trees parent-first and then creation/id, breaking cycles with a flag. Default20/max100 output rows, default8192 bytes, permitted1024..32768 for the entire response. Omitted counts describe authorized matches in the scanned window. Drop whole rows to fit; never expose a partial private field.

Read the existing named scope snapshot once under its gate, then project each visible actor's named watches and acknowledged cursor counts. Cursor source and channel source share that snapshot revision. The caller's direct inbox unread is separate, using existing mailbox cursor metadata; other actors' direct unread remains unknown. Report named source revision, each row's session revision and one observation time plus a digest of the returned projection. These are separate observations, not an atomic cross-file/global snapshot. Unavailable or corrupt named evidence yields partial roster rows with unknown channel fields; it cannot erase available session phases. Roster never writes files, acknowledges receipts or emits mutation events. A subsequent query reads fresh in-memory phase state even without a post.

## Acceptance

- [x] Actual SDK20-visible-session fixture plus outsiders proves row/byte caps, omission counts, scoped membership, private-parent suppression, no transcript/inbox reads and unchanged source bytes.
- [x] Child phase/step changes without posts become visible on next query; malformed old activity fields remain unknown and no phase duration is invented.
- [x] Watch/read/ack integration changes only the authenticated actor's unread count; read-only roster leaves cursors and events untouched, and corrupt channel state is explicitly partial.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test sessions
```

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just build sessions
SESSIONS_BINARY="$PWD/target/tool-result-contract/debug/sessions" bun test ../sessions.ctg/.cartridge/tests/integration/roster.test.ts ../sessions.ctg/.cartridge/tests/integration/channel-cursors.test.ts ../sessions.ctg/.cartridge/tests/integration/channels.test.ts ../sessions.ctg/.cartridge/tests/integration/mailbox.test.ts
```

Also public just check sessions and valid cursor/channel prerequisite receipts. Source failure never requests a repair or model/tool replay. Prompt integration is a separate harness child and remains required by the original parent.
