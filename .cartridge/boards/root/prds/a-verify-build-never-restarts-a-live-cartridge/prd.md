---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
footprint:
  - cartridge.ctg
  - .cartridge/memos/routine/cartridge-proxy.md
  - .cartridge/memos/routine/cartridge-runtime.md
commit: "da31a34874f298256c04026a2896ad6598bccc0b"
---

# a verify build never restarts a live cartridge

## Outcome

Since cartridge.ctg 771e046 the host hot-restarts a cartridge whenever the
target/debug dylib it loaded changes. A `cargo test` or `cargo clippy` run in a
submodule, such as collect's second Verify pass or a worker's gate, rewrites
that dylib and restarts live cartridges, which drops other sessions' in-flight
calls. Specs work around this today with an isolated `CARGO_TARGET_DIR`. The
host should restart only on a deliberate rebuild: for example, it loads a copy
of the dylib, or it reloads only on `cartridge reload` / `just proxy`, or on a
build marker that `cargo test` never writes. The analyst picks one and records
why.

Plain `cargo test`, `cargo clippy` and `cargo check` never rewrite
`target/debug/lib<name>.dylib` themselves (analyst probe, cargo 1.94). The risky
case is a test that nests `cargo build --lib` — harness, agent, memory and memo
all do — which swaps in a new dylib inode and trips the watcher. So the check is
whether a rewritten dylib restarts a loaded node, not whether `cargo test` alone
does.

## Acceptance

- [x] In an isolated host, rewriting a loaded cartridge's `target/debug/lib<name>.dylib` the way a test's `cargo build --lib` does leaves its node running (call counter continues).
- [x] A deliberate reload picks up a new build: `Host::replace` — what `cartridge reload <id>` dispatches to (`src/cli/mod.rs:131` → `src/host/socket.rs:451-453`) and what `just proxy` runs (`cartridge-proxy.md:37`, `exec cartridge reload proxy`) — starts a node that answers out of the rebuilt module (3, which neither the node that was running (8) nor a fresh node on the old build (2) can give).
- [x] `just test lifecycle` passes.
