---
complexity: high
footprint:
- src/roster.rs
- src/channels.rs
- src/mailbox.rs
- src/main.rs
- src/mapping.rs
- src/retention.rs
- .cartridge/tests/unit/main/retention_tests.rs
- .cartridge/tests/integration/retention.test.ts
- .cartridge/docs/retention.md
- src/observations.rs
---

# spec01 — Preview and journal guarded session cleanup

Add native `retention_preview {older_than, limit<=100}`, `retention_apply
{older_than, candidates:[{id,revision}]}`, and explicit `retention_resume {job}`.
Preview uses fresh snapshot SHA-256 revisions and reports eligible/retained IDs,
reasons, physical snapshot bytes and nonempty transcript record counts separately.
Bound inventory to 10,000 snapshots and read at most 8 MiB per snapshot; unreadable,
invalid, oversized or unknown-phase records are retained with explicit unknown
record counts. Only empty/known terminal agent phases qualify; starting, running,
approval waiting and non-null pending state do not. Apply enforces the cutoff and
fresh revision again; callers cannot bypass eligibility with fabricated candidates.

Add read-only `retention_protection {id}` plus revision-checked
`retention_protect {id,expected_revision,pinned,references}`. Host-registered named
references and pins live in a separate bounded atomic metadata file, preserving
snapshot bytes. Existing child-parent references, durable client mappings and this
instance's connection mapping also protect targets. Unknown/corrupt reference
metadata fails closed. Hosts remain responsible for registering external references.

An owner mutation barrier and each target's existing session gate cover fresh
eligibility checks and deletion; OS metadata/index locks protect reference writes
and mapping publication. Ordinary session mutations cannot become active between
check and deletion. Generic `delete` uses the same active/pin/reference guard,
closing the harness ring's existing list/distill/delete race without changing its
successful deletion shape. Existing transcript writes retain the single active
writer requirement across processes; this does not claim distributed session locking.

Before deletion, durably journal only the explicitly submitted candidates under
`.retention/jobs/<job>/`, preserve an exclusive exact-byte backup, mark backed_up,
then unlink/sync the original and mark deleted. Resume validates that same journal
and backup, rechecks still-present targets, never expands the candidate set, never
replays model/tool work, and preserves newly protected/changed targets as refused.
A missing original with committed backup is reconciled as deleted; completed entries
never delete a later replacement. Report partial job IDs on failure. No automatic
startup cleanup, backup removal or retry; malformed evidence fails closed.

## Acceptance

- [x] Preview distinguishes byte and record counts; active, waiting, pending, pinned, child-referenced, mapped and registered-reference targets are retained.
- [x] Activity/pin/reference/revision changes after preview refuse apply and generic delete where applicable, preserving snapshot/transcript bytes.
- [x] Simulated interruption after journal, backup and unlink resumes only recorded targets, preserves exact backups and never touches retained or later replacement sessions.
- [x] Real SDK preview/protection/apply/resume and harness-compatible generic delete behavior pass alongside existing recovery/checkpoint/mapping gates.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just test sessions
```

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just build sessions
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just build harness
SESSIONS_BINARY="$PWD/target/sessions-mapping/debug/sessions" HARNESS_BINARY="$PWD/target/sessions-mapping/debug/harness" bun test ../sessions.ctg/.cartridge/tests/integration/mapping.test.ts ../sessions.ctg/.cartridge/tests/integration/retention.test.ts
```

Run public check sessions and public harness tests, preserving concurrent harness
work. Every deletion fixture uses a disposable directory. Failures retain original
files and backups or report a journal-backed partial deletion; no user data is
cleaned during development. Existing mapping and recovery receipts require refresh.
