---
complexity: medium
footprint:
- Cargo.toml
- Cargo.lock
- cartridge.json
- init.lua
- src/lib.rs
- src/service.rs
- src/files.rs
- src/search.rs
- src/worker.rs
- src/store.rs
- src/overlay.rs
- src/ship.rs
- src/push.rs
- src/secrets.rs
- src/inspection.rs
- src/limits.rs
- src/provenance.rs
- src/tool_result.rs
- src/hook.rs
- src/bin/gitfs-hook.rs
- .cartridge/help.md
- .cartridge/docs/inspection.md
- .cartridge/docs/overlay-provenance.md
- .cartridge/docs/push.md
- .cartridge/docs/ship.md
- .cartridge/tests/unit/git_mode.rs
- .cartridge/tests/unit/store/
- .cartridge/tests/unit/ship/
- .cartridge/tests/unit/push/
- .cartridge/tests/unit/secrets/
- .cartridge/tests/unit/provenance.rs
- .cartridge/tests/unit/snapshot.rs
- .cartridge/tests/unit/tool_result.rs
---

# Absorb the gitfs store, tools and hook into the fs crate with no behavior change

The fs crate at 03f360e owns direct file access; gitfs owns the Git-backed
session overlay, shipping and the hook binary in a separate cartridge. This
spec moves gitfs's source, tests and docs into fs unchanged in behavior and
takes gitfs out of the composition.

## What moves

gitfs's modules — store, overlay tool, ship, push, secrets, inspection,
limits, provenance, tool_result and the hook — land in fs's src/ unchanged,
together with their unit suites under `.cartridge/tests/unit/` and their doc
pages under `.cartridge/docs/`. The `gitfs-hook` binary builds from
`src/bin/gitfs-hook.rs` declared in Cargo.toml alongside the `libfs` cdylib.
gitfs's deps (`libc`, `reqwest` with rustls) join fs's Cargo.toml.

## The fs surface grows two tools

`cartridge.json` declares `tool.gitfs` (ls, diff, rollback, materialize,
snapshot over the session branch `refs/gitfs/<session>`) and `tool.ship`
(preview/commit ship of the session branch, push, scan, undo). The manifest
test compares every tool schema, both tools included. The `mode` setting picks
where writes land: `git` (the default; every `tool.write`/`tool.edit` is one
commit on the session branch, worktree untouched until `materialize`) or
`local` (direct worktree writes). A workspace outside a Git repository always
behaves as `local`. Reads, globs and greps see the session's changes before
the worktree; digest and draft read through the same branch-first path.

## Composition

`init.lua` listens `tool.gitfs` and `tool.ship`; `config.lua` names fs's
`store_dir` instead of a gitfs block; the composed justfile and development
routine name no gitfs. gitfs board records point `repo:` at fs.ctg.
gitfs.ctg stays untouched on disk as the recovery path: re-adding its
composition line and removing the two events from fs restores the split.

## Acceptance

- [x] `fs.ctg` builds `libfs` and the `gitfs-hook` binary, and the manifest test
  compares every tool schema, `tool.gitfs` and `tool.ship` included.
- [x] Every gitfs unit suite (store, ship, push, secrets, provenance, snapshot,
  tool results) runs and passes inside `just test fs`.
- [x] `.cartridge/init.lua`, `config.lua`, the composed justfile and the
  development routine no longer name gitfs; gitfs board PRDs point `repo:`
  at fs.ctg.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/fs.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0
cargo fmt -p fs -- --check
cargo clippy -p fs --all-targets -- -D warnings
cargo test -p fs --all-targets
```

The test run shows the absorbed suites (`store::tests::`, `ship::tests::`,
`push::tests::`, `secrets::tests::`, `provenance::tests::`,
`tool_result::tests::`, snapshot) and builds the `gitfs-hook` binary. These
are the exact commands the composed `just check fs` and `just test fs` gates
run for the fs owner. Composition is checked by inspection of
`.cartridge/config.lua`, `.cartridge/init.lua` and the composed justfile, and
by `grep -ri gitfs` over the gitfs board's prd.md files pointing at fs.ctg.