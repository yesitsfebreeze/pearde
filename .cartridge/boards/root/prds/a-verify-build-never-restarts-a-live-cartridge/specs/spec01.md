---
complexity: small
footprint:
  - cartridge.ctg
  - cartridge.ctg/src/loader/document.rs
  - cartridge.ctg/src/loader/mod.rs
  - cartridge.ctg/.cartridge/tests/unit/src/trust/tests.rs
  - cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs
  - cartridge.ctg/.cartridge/tests/unit/src/tests/fixtures/native/Cargo.toml
  - cartridge.ctg/.cartridge/tests/unit/src/tests/fixtures/native/src/lib.rs
  - .cartridge/memos/routine/cartridge-proxy.md
  - .cartridge/memos/routine/cartridge-runtime.md
---

# spec01 — A rebuilt native module restarts its cartridge only on reload

Base: cartridge.ctg 4b13113, the head of the live submodule's `main` (the `cartridge.ctg` gitlink
at root b3a1660 is still a965d6e, two commits behind). The work was written on a965d6e and rebased
onto 4b13113; the two touch disjoint files. No `needs`.

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

### Why `just build` must not call `cartridge reload` (deliberate loss of 771e046's convenience)

Losing "`just build proxy` restarts the proxy by itself" is the point of this change, not a gap to
paper over. Wiring `just build <owner>` to end in `cartridge status && cartridge reload <owner>`
would reintroduce exactly the bug: Verify blocks already run `just build <owner>` in the live
checkout on the default target — see `boards/gitfs/overlay-mutations-report-revisions` spec01:106-108
and `boards/runtime/shipped-gitfs-profiles-grant-change-recording` spec01:53-55 — so every such gate
would restart other sessions' cartridges again. `just build runtime` also needs `daemon --replace`,
not `reload`. The @root/one-daemon audit item "a rebuilt native module does not reload nodes" is
therefore closed as **reload is explicit**: the rebuild path is `just proxy` / `cartridge reload <id>`,
and the two routine memos say so after step 4. If an explicit shortcut is ever wanted, the shape is
an opt-in `just reload <owner>`, not a reload inside `build`; it is not needed now, `cartridge reload`
already exists.

## Steps

1. `src/loader/document.rs` `resolve`: set `sources = vec![path.clone(), entry.clone()]`, with no native candidates.
   `native_candidates` stays as `load_native`'s search list. Drop the "host watches the same list"
   sentence from its doc comment in `src/loader/mod.rs`.
2. `.cartridge/tests/unit/src/trust/tests.rs`: replace
   `a_built_native_module_is_a_source_so_its_rebuild_restarts_the_cartridge` with
   `a_built_native_module_is_not_a_source_so_a_test_build_keeps_the_cartridge`, which asserts `sources.len() == 2`.
3. `.cartridge/tests/unit/src/tests/host.rs`: add `a_rewritten_native_module_restarts_only_on_reload`,
   and give the fixture (`.cartridge/tests/unit/src/tests/fixtures/native/`) a `rebuilt` feature whose
   only effect is that `twice` multiplies by 3 instead of 2 — one module, two builds that answer
   differently. Manifest `name: "native_fixture"`, id `native`. Build the fixture twice: the default
   build, and `--features rebuilt --target-dir <a second tempdir>` so the default artifact survives
   (a shared target dir would overwrite it and race
   `tests::host::a_native_module_reaches_the_base_through_the_global`, which asserts `twice(21) == 42`).
   Copy the default build to `native/target/debug/`, boot the host and start `host.watch()`. A Lua
   call counter returns `twice(calls)`. Then three legs:
   (a) rewrite the dylib with the same bytes (remove, copy, `set_modified(now)`) and sleep 4× the
   debounce — the count continues (4): a test build does not restart the node;
   (b) rewrite it with the `rebuilt` build and sleep again — the count continues *and* the answer is
   still the loaded build's (6): not even a real new build restarts the node on its own;
   (c) `host.replace("native")` — the count restarts *and* the answer is the new build's (3).
   3 is unreachable any other way: the old node would answer 8, and a fresh node on the old build 2.
   So leg (c) proves new content took effect, not merely a new process — this closes round-1 F4,
   which rounds 1 and 2 only disclosed. Leg (a) is the reusable attempt in `attempt.patch`; it FAILS
   at the base ("a test build restarted the node") and passes with steps 1-2.
4. Correct the two routine memos that promise the removed auto-restart, both composed into agent
   prompts: `.cartridge/memos/routine/cartridge-proxy.md:13-15` ("Rebuilding the proxy
   (`just build proxy`) does the same on its own: the host watches each cartridge's built module…")
   and `.cartridge/memos/routine/cartridge-runtime.md:20` ("`cartridge reload <id>`, or on its own
   when its module is rebuilt"). Both become: a rebuilt module is picked up by `just proxy` /
   `cartridge reload <id>`. Keep the surrounding sentences; runtime.md's point that `--replace` is
   for a new host build only still stands.
5. Commit in cartridge.ctg, then advance the root gitlink (the memo edits live in the superproject).

## Acceptance

- [x] `resolve` no longer lists a built native module as a source (the trust unit test).
- [x] In an isolated host, rewriting a loaded cartridge's `target/debug` dylib (as a test's nested `cargo build --lib` does) leaves its node running, even when the file it is rewritten with is a behaviourally different build (the host unit test, legs a and b).
- [x] `cartridge reload <id>` (`Host::replace`) starts a node that answers out of the file on disk now: the host unit test observes the second build's answer (3), which neither the node that was running (8) nor a fresh node on the old build (2) can give (leg c).
- [x] Neither `cartridge-proxy.md` nor `cartridge-runtime.md` still promises a rebuild restarts a cartridge on its own (Verify block 1's grep).
- [x] `just test lifecycle` passes against the built host.
- [x] `cargo fmt --check` and `clippy -D warnings` are clean for cartridge.ctg.

## Verify and Proof

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-verify-build-never-restarts-a-live-cartridge-verify}"
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0
for memo in .cartridge/memos/routine/cartridge-runtime.md .cartridge/memos/routine/cartridge-proxy.md; do test -f "$memo" || { echo "missing routine memo: $memo" >&2; exit 1; }; done
if grep -nE 'on its own when its module is rebuilt|does the same on its own' .cartridge/memos/routine/cartridge-runtime.md .cartridge/memos/routine/cartridge-proxy.md; then echo "routine memo still promises an automatic restart" >&2; exit 1; fi
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

The round-1 `grep -n native_candidates cartridge.ctg/src/loader/document.rs` guard is dropped: it
pinned the implementation's shape, and the host unit test already proves the behaviour.

Block 1's nextest filter names `tests::host::a_rewritten_native_module_restarts_only_on_reload`, so
legs (a), (b) and (c) of step 3 — including the `Some(json!(3))` assertion that closes F4 — all run
inside it; no separate block is needed.

## Coordinator note

Footprint carries both stale routine memos, `.cartridge/memos/routine/cartridge-proxy.md` and
`.cartridge/memos/routine/cartridge-runtime.md`; step 4 is the implementer's edit and Verify block 1
fails if either is left as-is. `prd.ctg/.cartridge/templates/spec.md:25` explains the isolated
`CARGO_TARGET_DIR` by this hot-restart; isolating the target stays harmless, so that wording is an
optional follow-up outside this footprint.
