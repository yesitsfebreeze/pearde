---
complexity: medium
footprint:
  - Cargo.toml
  - src/main.rs
  - src/recovery.rs
  - .cartridge/tests/unit/main/repair_tests.rs
  - .cartridge/tests/unit/recovery.rs
  - .cartridge/docs/README.md
---

# spec01 — Inspect recovery state and guard the narrow legacy repair

Add sessions recovery{id} as a read-only fresh on-disk report: missing,
legacy-empty eligible, legacy nonempty, corrupt/unavailable, valid, incomplete
run. Name safe next actions and the SHA-256 of the exact inspected bytes.
Never infer that a live/incomplete run's external effects were rolled back.

repair{id,expected_revision} requires that digest, a regular file, and the
existing strictly empty legacy shape. Create the existing exclusive backup,
fsync it, and recheck the original bytes at the existing temp-file rename
boundary. Preserve the backup on a conflict or failure; do not overwrite a newer
snapshot, auto-retry a repair, or repair during loading. Keep existing atomic
persistence and uncertain-directory-sync behavior.

## Acceptance

- [x] Missing, legacy-empty, corrupt and incomplete-run reports are distinct, identify exact revisions when available, and modify no files.
- [x] Only eligible legacy-empty snapshots repair; old bytes are backed up exclusively; stale digests and repeated repairs preserve existing data and backups.
- [x] A deterministic pre-commit hook changes the source after backup; the commit guard refuses and preserves newer bytes. Existing legacy loading and atomic persistence gates pass.

## Verify and Proof

```sh
cargo test --manifest-path Cargo.toml -p sessions
```

Add the already-used sha2 crate and update the composition's existing shared
Cargo lock entry separately. No additional remote dependency version is needed.
The existing single-process session gate serializes API writers. The final
revision check detects observed external edits; it is not an OS compare-and-swap
against arbitrary uncooperative writes after that check.
