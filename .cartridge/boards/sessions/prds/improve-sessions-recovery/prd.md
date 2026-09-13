---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: improve-sessions-recovery
footprint: ["src/roster.rs","src/channels.rs","src/mailbox.rs","Cargo.toml","src/main.rs","src/recovery.rs",".cartridge/tests/unit/main/repair_tests.rs",".cartridge/tests/unit/recovery.rs",".cartridge/docs/README.md","src/observations.rs","src/lib.rs","src/change_record.rs","src/changes.rs",".cartridge/tests/unit/main/change_records_tests.rs","src/context.rs",".cartridge/tests/unit/main/context_tests.rs",".cartridge/tests/integration/context.test.ts"]
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
---

# Explain session damage and narrowly repair eligible snapshots

A read-only recovery report distinguishes missing, legacy, corrupt and incomplete-run records with safe next steps.

## Acceptance

- [x] Fixtures for missing, legacy-empty, corrupt and uncertain-run states produce distinct diagnoses; inspection changes no files.
- [x] Only eligible legacy-empty snapshots can be repaired, backups are preserved, and a repeated repair cannot overwrite an existing backup or transcript.

- [x] Keep old snapshots readable; any migration preserves original bytes and uses atomic revision-checked writes. Retention requires an explicit reviewed candidate set. Reverting code must not delete or reinterpret an uncertain external effect.

## Proof and recovery

Start at [main.rs](../../../main.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-sessions-recovery`; maximum five rounds.

## Verified implementation — 2026-09-13

The sessions gate passes all 25 tests. Fresh recovery reports distinguish missing,
legacy-empty, corrupt and incomplete-run fixtures without changing files. SHA-256
revisions reject stale repair requests. An injected change after backup creation
is caught at the temporary-file commit boundary, preserving newer transcript
bytes, the original backup and an unchanged in-memory store. Existing backup,
repeated-repair, canonical-transcript, atomic-write and uncertainty tests pass.
The shared Cargo lock adds only the existing sha2 dependency to sessions.

Reverify unchanged recovery acceptance after181adb2 client mapping shares src/main.rs;
prior4dd8518e receipt retained. No semantic acceptance change.

Reverify unchanged acceptance after the next integrated owner feature; earlier
181adb20 receipt retained. No contract relaxation.

Reverification at965108d9 after mailbox integration. Add the new transitive source module to verification coverage; behavioral acceptance is unchanged.

Reverification: attributed report at2a6a863 adds native main dispatch; bind src/observations.rs as transitive source, retaining previous acceptance and executable gates.

Named channel registration revalidation at 423ecd32: source footprint includes registered channels and its shared mailbox codec; acceptance and behavior gates remain unchanged.
