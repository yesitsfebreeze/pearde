---
complexity: medium
footprint:
- Cargo.toml
- src/lib.rs
- src/change_record.rs
- src/changes.rs
- src/main.rs
- .cartridge/tests/unit/main/change_records_tests.rs
- .cartridge/tests/integration/change-records.test.ts
- .cartridge/docs/change-records.md
---

# Sessions owns change evidence, never file ownership

Expose pure shared serde DTOs in `sessions::change_record` through a small library.
The existing Sessions binary reuses them. All objects deny unknown fields.
`Evidence` contains `v:1`, `publication_id` (64 lowercase hex from 32 OS-random bytes),
`provider:fs|gitfs`, `operation:write|edit|snapshot|materialize`,
`actor:{session,run:null|string,call:null|string}`, `target:{workspace,path,storage,
overlay_ref:null|string}`, `before`, `after`, and `overlay_commit:{before,after}`
(nullable Git object IDs). `storage` is `direct` or `gitfs_overlay`; FS only reports
direct write/edit, GitFS materialize reports direct, and its other mutations report
overlay. Overlay records require the actual `refs/gitfs/...` reference. These are
reported coordinates, not a grant or proof of current ownership.

Each version is tagged `absent`, `sha256 {value}`, or `git_object {value}`. SHA256
is exactly 64 lowercase hex; Git object IDs are exactly 40 or 64 lowercase hex.
Kinds prevent comparing a Git object ID as a raw content hash. FS uses the checked
preimage and prepared bytes. GitFS uses pinned blob/commit receipts, and uses
content hashes for known materialized bytes. No file contents or free-form actor
metadata enter the log. Strings are bounded: session/run/call 256 bytes; canonical
workspace and absolute worktree path 4096 bytes; overlay ref 1024 bytes. Actor.session
must equal request id. Lexically normalized absolute path must remain inside
workspace; Sessions does not resolve files or certify current physical identity.
Historic workspace is retained even if Session.cwd later changes. Aliases are not
silently merged. Missing legacy GitFS run/call remain null, never invented.

Add `record_changes {id,records:[Evidence]}` and read-only `changes {id,offset?,limit?,
expected_revision?}` to the native owner API. Append accepts 1..64 records and
at most 256 KiB serialized request evidence. Each evidence record is at most 16 KiB.
Persist an optional schema-v1 log inside the existing Session snapshot: at most 512
records and 1 MiB serialized log, no eviction or rotation. A record has owner-assigned
sequence, publication_id, SHA256 digest of canonical serialized Evidence, and owner
observed_at. The producer generates a fresh publication_id under its mutation
guard before each possible publication, using the already-resolved getrandom0.4
crate through the shared helper; entropy failure refuses before mutation. It
retains the same ID only when recording that same known publication again.
Repeated A→B→A→B writes therefore remain distinct even with missing or reused
run/call metadata. Publication IDs are not authority credentials. Same provider/ID
with exact same evidence returns the existing sequence without another append;
same provider/ID with different evidence refuses as a conflict. Payload hash alone
is not publication identity.
Capacity and validation are checked against the full candidate batch before
publication. Reuse the current per-session gate, candidate copy and atomic file
publication, including existing uncertainty diagnostics. No new global journal or
cross-process writer protocol. Existing single-active-writer limitation remains.

Legacy `touch` and `files` stay unchanged. The new append adds each reported path
to the same display-only set, while detailed records preserve storage identity.
The detailed log stays out of existing list/get/update public metadata projections;
only the new changes API pages it. Stored snapshots retain it. This avoids
expanding every existing response by the retained log capacity.
It does not change the transcript or agent state revision. Older snapshots default
to no log; arbitrary legacy paths remain readable and gain no fabricated actor or
revision. Old binaries need not understand newly written schemas; do not promise
backward writer compatibility: mixed older writers can reject or drop new fields
and must not be used to mutate an upgraded snapshot. On every decode/read/append,
validate schema, every nested DTO, same-session actors, hashes, unique publication
IDs, contiguous monotonic sequences and all count/byte caps. Corrupt new logs fail
diagnosis without migration, eviction or repair. Caps bound retained new evidence;
this leaf does not retrofit the entire legacy snapshot/transport allocation path.

Read defaults to32 records, at most 64 and 64 KiB total response; return next_offset,
total, complete, log revision, and `trust:provider_reported_not_authorization`.
The revision hashes the complete retained log; offset>0 requires matching revision.
Reject a changed revision rather than mixing pages. Reads perform no FS inspection,
session touch, timestamp update or ownership mutation. Individual record caps
guarantee at least one record fits. Existing `get.files` exposes legacy path records.

## Acceptance

- [x] Strict shared DTO and stored-log validation reject malformed nested fields, actor/session mismatch, invalid IDs/hashes/sequences and cap overflow without eviction or repair.
- [x] Distinct publications of repeated transitions remain distinct; same-publication evidence is idempotent and ID collisions with changed evidence refuse.
- [x] Native append/read/restart and revision-bound pages preserve records, legacy files, transcript and agent revision; failure injection preserves old state or reports publication uncertainty.
- [x] Public Sessions test/check and maintained native fixtures pass at a recorded source and binary revision.

## Verify and Proof

Use actual SDK Sessions append/read/restart with fixed direct/overlay evidence,
same-publication dedupe, repeated equal-content transitions with distinct IDs,
same-ID/different-evidence refusal, actor/session mismatch, malformed/unknown nested fields,
caps without eviction, corrupt nested stored records/ID/digest/sequence rejection,
stale page refusal, and old snapshots containing only files.
Inject existing write/file-sync/rename/directory-sync failures and verify old state
or explicit uncertainty with no silent replay. Compare transcript/agent revision,
legacy file bytes on read, and raw snapshot before/after. Public commands from
runtime: `just test sessions`, `just check sessions`, `just build sessions`; then
`SESSIONS_BINARY=$CARGO_TARGET_DIR/debug/sessions bun test
../sessions.ctg/.cartridge/tests/integration/change-records.test.ts`.
Wrappers are disabled; use the coordinator-assigned shared target. Source lease
begins only after roster collection and independent review.

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test sessions
just check sessions
just build sessions
SESSIONS_BINARY="$CARGO_TARGET_DIR/debug/sessions" bun test ../sessions.ctg/.cartridge/tests/integration/change-records.test.ts
```
