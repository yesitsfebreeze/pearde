---
complexity: small
footprint:
  - cartridge.ctg
  - cartridge.ctg/src/loader/document.rs
  - cartridge.ctg/src/loader/mod.rs
  - cartridge.ctg/.cartridge/tests/unit/src/trust/tests.rs
  - cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs
  - .cartridge/memos/routine/cartridge-proxy.md
---

# spec01 — A rebuilt native module restarts its cartridge only on reload

Base: cartridge.ctg a965d6e (gitlink at root ab2bdca). No `needs`.

## Option chosen: reload only on a deliberate `cartridge reload <id>` (option 2)

- 771e046 added `native_candidates(root, manifest.name)` that exist to `Declared.sources`
  (`src/loader/document.rs:305-312`). The watch task restarts a slot when any source's
  (len, mtime) changes (`src/host/watch.rs`, `src/host/mod.rs:565-584`, `src/loader/mod.rs:60`).
  It was added to close an audit gap in @root/one-daemon-… ("a rebuilt native module does
  not reload nodes"), so that `just build proxy` restarts the proxy (`.cartridge/memos/routine/cartridge-proxy.md`).
- Probed (cargo 1.94): plain `cargo test`, `cargo test --all-targets`, `cargo clippy --all-targets`
  and `cargo check` leave `target/debug/lib<name>.dylib` alone, for both `cdylib` and `cdylib`+`rlib`.
  But `cargo test` rewrites it (new inode, new mtime) when a test runs `cargo build --lib`. The
  integration tests of harness, agent and memory do that (`support.rs:39`, `loop.rs:73`,
  `cartridge.rs:35`), and memo does it through bun. So a gate restarts the live cartridge.
- Option 1 (load a copy) is not needed. Cargo swaps in a new inode on every build (links=1), so it
  never overwrites a mapped image in place, and a copy alone does not stop the watcher from firing.
- Option 3 (build marker) would need a new host convention plus a write in `just build`
  (a superproject memo, outside this footprint). It would restart all the same cartridges as option 2.
- `cartridge reload <id>` (`src/host/socket.rs:451` → `replace`) stops the node process and spawns
  a new `cartridge node` (`src/host/process.rs:106-110`), which dlopens the file present now. `just proxy`
  calls `reload proxy`. The deliberate path needs no new code.

## Steps

1. `src/loader/document.rs` `resolve`: set `sources = vec![path.clone(), entry.clone()]`, with no native candidates.
   `native_candidates` stays as `load_native`'s search list. Drop the "host watches the same list"
   sentence from its doc comment in `src/loader/mod.rs`.
2. `.cartridge/tests/unit/src/trust/tests.rs`: replace
   `a_built_native_module_is_a_source_so_its_rebuild_restarts_the_cartridge` with
   `a_built_native_module_is_not_a_source_so_a_test_build_keeps_the_cartridge`, which asserts `sources.len() == 2`.
3. `.cartridge/tests/unit/src/tests/host.rs`: add `a_rewritten_native_module_restarts_only_on_reload`.
   Manifest `name: "native_fixture"`, id `native`. Copy the fixture dylib to `native/target/debug/`,
   boot the host and start `host.watch()`. A Lua call counter returns `twice(calls)`. Rewrite the dylib
   (remove, copy, `set_modified(now)`) and sleep 4× the debounce: the count continues (4). Then
   `host.replace("native")`: the count restarts (2). This is the reusable attempt in `attempt.patch`.
   It FAILS at a965d6e ("a test build restarted the node") and passes with steps 1-2.
4. Commit in cartridge.ctg, then advance the root gitlink.

Out of footprint (the coordinator decides): `.cartridge/memos/routine/cartridge-proxy.md` says
"Rebuilding the proxy (`just build proxy`) does the same on its own". That becomes false and needs
a one-line fix to "run `just proxy` or `cartridge reload <id>` after a build".

## Acceptance

- [ ] `resolve` no longer lists a built native module as a source (the trust unit test).
- [ ] In an isolated host, rewriting a loaded cartridge's `target/debug` dylib (as `cargo test` does) leaves its node running, and `reload` starts a new node on the rebuilt file (the host unit test).
- [ ] `just test lifecycle` passes against the built host.
- [ ] `cargo fmt --check` and `clippy -D warnings` are clean for cartridge.ctg.

## Verify and Proof

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-verify-build-never-restarts-a-live-cartridge-verify}"
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0
if grep -n native_candidates cartridge.ctg/src/loader/document.rs; then echo "native module still a source" >&2; exit 1; fi
cargo nextest run --manifest-path cartridge.ctg/Cargo.toml --workspace \
  -E 'test(=tests::host::a_rewritten_native_module_restarts_only_on_reload) | test(=trust::tests::a_built_native_module_is_not_a_source_so_a_test_build_keeps_the_cartridge) | test(=tests::host::a_native_module_reaches_the_base_through_the_global)'
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-verify-build-never-restarts-a-live-cartridge-verify}"
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0
cargo build --manifest-path cartridge.ctg/Cargo.toml --bin cartridge
CARTRIDGE_HOME="$(mktemp -d)"; export CARTRIDGE_HOME
just test lifecycle
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-verify-build-never-restarts-a-live-cartridge-verify}"
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER=
cargo fmt --manifest-path cartridge.ctg/Cargo.toml --all --check
cargo clippy --manifest-path cartridge.ctg/Cargo.toml --workspace --all-targets -- -D warnings
```

## Coordinator note

Added `.cartridge/memos/routine/cartridge-proxy.md` to the footprint. It currently says `just build proxy` restarts the proxy by itself, which stops being true after this change. The implementer corrects that line to name `just proxy` / `cartridge reload <id>`.
