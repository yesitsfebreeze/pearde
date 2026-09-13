---
complexity: low
footprint: ["src/roster.rs","src/channels.rs","src/mailbox.rs",".cartridge/docs/README.md",".cartridge/docs/client-mapping.md",".cartridge/docs/retention.md",".cartridge/tests/integration/mapping.test.ts",".cartridge/tests/integration/retention.test.ts",".cartridge/tests/unit/main/mapping_tests.rs",".cartridge/tests/unit/main/repair_tests.rs",".cartridge/tests/unit/main/retention_tests.rs",".cartridge/tests/unit/recovery.rs","Cargo.toml","src/main.rs","src/mapping.rs","src/recovery.rs","src/retention.rs","src/observations.rs","src/lib.rs","src/change_record.rs","src/changes.rs",".cartridge/tests/unit/main/change_records_tests.rs"]
---

# spec01 — Verify integrated sessions improvements

This owner rollup has external `needs` rather than nested engine children. Run
executable verification and bind its source footprint to the union of all three
leaf contracts, so a future shared-source change invalidates this receipt too.
Require engine-verified completion of mapping, retention and recovery at collection;
a green state marker alone is insufficient. Each leaf retains its independent
review, acceptance and receipt history. No source code or durable user data changes
are part of this rollup.

Run the integrated native sessions suite and the real SDK mapping/retention/harness
fixtures. Reconnect identity comes only from host configuration; unconfigured
services remain instance scoped. Retention protects activity/pins/references,
preserves journal backups and resumes explicitly. Recovery diagnoses exact bytes
and narrowly repairs eligible legacy-empty data using exclusive backup and stale
revision protection. Tests preserve old transcripts on refusal, isolate forged
metadata and retain interrupted/replacement evidence.

Record limitations without upgrading them into stronger guarantees: the native
API remains host-trusted, external references need host registration, transcript
writers retain their existing single-writer boundary across processes, direct
filesystem races are not a distributed transaction, and no recovery path replays
model/tool work automatically. Public check/build and existing harness tests remain
recorded consumer evidence; all destructive fixtures use disposable directories.

## Acceptance

- [x] All three dependency receipts are engine-verified at the integrated source footprint, with independent review scores at least 90 within inherited rounds.
- [x] The combined native and SDK gates pass, including actual harness cleanup compatibility and guarded late activity.
- [x] Evidence names integrated revisions, tested mitigations and remaining authority/concurrency/recovery limitations.

## Verify and Proof

```sh
cd ../prd.ctg
bun -e 'for (const ref of ["@sessions/improve-sessions-client-mapping","@sessions/improve-sessions-retention","@sessions/improve-sessions-recovery"]) { const run = Bun.spawnSync(["./prd", "verified-status", ref, "--json"]); const result = JSON.parse(run.stdout.toString()); if (run.exitCode || !result.data?.verified) throw new Error(ref + ": " + (result.error || result.data?.reason)); console.log(JSON.stringify(result.data)); }'
```

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test sessions
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just build sessions
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just build harness
SESSIONS_BINARY="$PWD/target/tool-result-contract/debug/sessions" HARNESS_BINARY="$PWD/target/tool-result-contract/debug/harness" bun test ../sessions.ctg/.cartridge/tests/integration/mapping.test.ts ../sessions.ctg/.cartridge/tests/integration/retention.test.ts
```
