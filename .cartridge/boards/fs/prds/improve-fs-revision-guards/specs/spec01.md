---
complexity: medium
footprint: ["cartridge.json","src/main.rs","src/context.rs","src/files.rs","src/service.rs",".cartridge/tests/unit/service/tests.rs",".cartridge/docs/revision-guards.md","Cargo.toml"]
---

# spec01 — Recheck the observed version at filesystem publication

Reuse content observations and per-target serialization. One helper prepares a
create-new sibling, syncs its bytes and preserves existing permissions. After
preparation and immediately before publication, check cancellation, canonical
workspace confinement and the expected content (including absence). Replace
existing files by rename; publish absent targets via an exclusive hard link so
creation is complete and cannot replace another creator. Clean temporary files
on failure. Report any failure after publication as partial_success with the
changed path and no automatic retry. Retain the existing session touch boundary.

Scope the two-writer guarantee to the shared fs service. Uncooperative processes
can still write after the final check; do not advertise OS-level atomic CAS or
cross-cartridge locking. Preserve the independent gitfs overlay behavior through
its current executable-mode, guard, selection and partial-error tests.

## Acceptance

- [x] Deterministic post-preparation hooks change, delete or create a target; write and edit refuse stale publication and preserve external bytes without session touch or abandoned temps.
- [x] Two concurrent sessions observing the same content have exactly one successful differing write; the loser reports stale content. Same-size content changes are detected.
- [x] Cancellation at publication preserves the old file; symlink escape is rejected; successful write/edit preserve executable modes; creation publishes complete bytes; post-write observation/touch failures report partial_success.
- [x] Public fs tests/check and the independent gitfs compatibility tests pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test fs
```

Run the owner's public check gate and `just test gitfs` from the runtime as well.
The deterministic hook is per-service and test-only; it runs after prepared
bytes are synced, before cancellation/revision checks and publication.

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just check fs
just test gitfs
```
