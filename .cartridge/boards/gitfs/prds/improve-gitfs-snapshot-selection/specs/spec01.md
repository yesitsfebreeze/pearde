---
complexity: small
footprint: ["src/service.rs",".cartridge/tests/unit/snapshot.rs","Cargo.toml","src/provenance.rs",".cartridge/tests/unit/provenance.rs",".cartridge/tests/integration/change-provenance.test.ts",".cartridge/docs/change-provenance.md"]
---

# spec01 — Snapshot selected owned paths with explicit partial failures

Resolve the optional paths selection against the current owned set before any
write. Omission selects all owned paths; an empty list selects none; duplicates
are visited once. Reject an unowned selection as a whole. Keep existing path
validation and overlay modes. Read/store failures carry the path in errors and
set the existing error flag, retaining the list of completed snapshots.

## Acceptance

- [x] Selected A changes; owned B remains untouched; empty selection and duplicate selections behave exactly as described.
- [x] Invalid/unowned selections mutate nothing; missing/unreadable paths report errors and preserve previous overlay bytes; partial success names saved paths.
- [x] Executable overlay mode, edit guards, materialization conflicts and unrelated Git index/worktree/ref state remain intact.

## Verify and Proof

```sh
cargo test --manifest-path Cargo.toml -p gitfs
```

Temporary repositories only. The existing real-consumer integration gate also
runs; no external remote, push or persistent user data is touched.
