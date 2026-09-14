---
repo: /Users/feb/dev/cartridge/tools.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-tools-bundle-provenance
footprint:
- /Users/feb/dev/cartridge/tools.ctg/src/service.rs
- /Users/feb/dev/cartridge/tools.ctg/.cartridge/tests/unit/service/tests.rs
---

# Ship bundles with source and dependency provenance

`bundle` writes a provenance record into `dist/cartridge`. `bundle` and `package` in [service.rs](../../../../../../tools.ctg/src/service.rs) already stage into a temporary folder, refuse a missing Rust binary before publishing (`packaging_refuses_missing_rust_binaries_but_accepts_lua_only`) and rename into place. They record nothing about what was built. The old `scripts/workspace.py` and `repositories.json` inputs no longer exist.

Record `PROVENANCE.json` inside the staged bundle before the rename. It holds, per repository under the composition root (submodules included), the commit and a SHA-256 of `git diff HEAD` when dirty; the SHA-256 of every copied executable; digests of each `Cargo.lock`/`bun.lock` used; the build profile; and the `rustc`, `cargo` and `bun` versions. This is metadata only and does not claim reproducible binary bytes.

## Acceptance

- [ ] Two bundles of an unchanged fixture produce byte-identical `PROVENANCE.json` (the record has no timestamp).
- [ ] Changing a copied executable, a lockfile or a tracked source file (dirty) changes exactly the corresponding digest.
- [ ] The record contains no environment values, `config.lua` contents, credentials or `.cartridge` store paths. A failing version probe fails the bundle before the rename and keeps the previous `dist/cartridge`.

## Proof and recovery

First extend `package_preserves_entries_binaries_and_notices` in [tests.rs](../../../../../../tools.ctg/.cartridge/tests/unit/service/tests.rs) with a git fixture. Gates, cwd `/Users/feb/dev/cartridge`: `just test tools`, `just check tools`. Not run. Rollback: stop writing the file. Bundles stay loadable without it.

## Dependencies and review

No hard prerequisites. Same file as `improve-tools-preflight`, so coordinate landing. Board placement under @runtime is historical. [Review](review.md): inherits 2 rounds.
