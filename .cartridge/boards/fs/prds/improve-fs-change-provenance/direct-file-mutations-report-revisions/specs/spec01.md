---
complexity: medium
footprint:
- Cargo.toml
- src/main.rs
- src/service.rs
- src/files.rs
- .cartridge/tests/unit/service/tests.rs
- .cartridge/tests/integration/change-provenance.test.ts
- .cartridge/docs/change-provenance.md
---

# Report known direct publication through the Sessions schema

Depend on the Sessions library solely for the strict `Evidence` DTO. FS already
injects Sessions. Keep `fs.context`, ordinary reads and all search behavior unchanged.
Add structured mutation evidence to the files worker outcome, captured inside
the existing per-target lock: canonical invocation workspace, resolved absolute
target, provider fs, operation write/edit, context session/run/call, checked old
SHA256 or absence, prepared new SHA256, and a fresh shared-helper publication_id
created under the target guard before publication. Entropy failure refuses before
writing; an evidence retry retains the original ID and never reruns file work.
These are the bytes known published at
that point; no reread or claim that arbitrary later disk writers are excluded.
Identical-byte writes retain existing publication/touch semantics and report the
equal versions honestly. No GitFS reference or commit is synthesized.

Distinguish prepublication error from known publication followed by temp-cleanup
or observation failure. Return evidence with a partial outcome in the latter case
so service dispatch still attempts recording once; do not infer publication by
matching error prose. Existing guards, confinement, permission preservation and
postpublication error wording remain. Cancellation before publication records
nothing. Cancellation/drop after publication cannot promise rollback or durable
recording; report known partial outcome when a response is available.

The async service calls `record_changes {id:context.session,records:[evidence]}`
through the existing host callback, with a 2-second recording deadline. After successful
recording preserve ordinary success content and existing tool-result envelope.
After a known file change, a callback refusal/invalid receipt/deadline returns
`partial_success`, changed path, and explicit attribution failure or unknown;
never retry the file mutation or recorder automatically. A timeout can still be
followed by a late Sessions publication, so it is unknown rather than definitely
absent. Existing Sessions `files` remains populated by the append owner.

Validate recording receipts against returned evidence IDs/batch count; do not
treat arbitrary successful JSON as persistence proof. The transport supplies no
new principal authority. Input tool schemas continue rejecting actor/session/
backend/revision fields in model arguments. Native invocation context remains
the existing host boundary; arbitrary context is not newly authenticated.

## Acceptance

- [ ] Each known direct publication captures actual before/after SHA256, canonical target and a fresh publication_id under the existing guard; equal-content repeated publications are distinct.
- [ ] Refused/stale/cancelled writes and every read/search/fs.context operation record nothing; no external or unrelated path gains ownership.
- [ ] Known publication followed by cleanup/observation/recording failure retains evidence and reports partial or uncertain attribution without replay.
- [ ] Native real-Sessions recording/restart, existing guarded-write tests and read-only context compatibility pass through public gates.

## Verify and Proof

Unit fixtures assert exact absent/present/equal-content before/after bytes and
target, once-only callback, deterministic stale/concurrent/cancelled refusal,
postpublication observation failure with evidence, and bounded failed/hung recorder.
Native FS→real Sessions fixtures prove legacy files plus detailed record survive
restart, and a direct edit does not create a GitFS branch/owned path. Existing
`fs.context` full-byte snapshot and zero-touch tests are mandatory.
From runtime with disabled wrappers: `just test fs`, `just check fs`, `just build fs`;
then `bun test ../fs.ctg/.cartridge/tests/integration/context.test.ts
../fs.ctg/.cartridge/tests/integration/change-provenance.test.ts` using current
FS/Sessions binaries. Coordinator owns shared workspace Cargo.lock resolution.

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test fs
just check fs
just build fs
just build sessions
FS_BINARY="$CARGO_TARGET_DIR/debug/fs" SESSIONS_BINARY="$CARGO_TARGET_DIR/debug/sessions" bun test ../fs.ctg/.cartridge/tests/integration/context.test.ts ../fs.ctg/.cartridge/tests/integration/change-provenance.test.ts
```
