---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
actual: "1h"
---

# every lane shares the trunk's CARGO_TARGET_DIR, and kache keys a test binary on source bytes alone, so `just memos-check` and `just test` in a fresh lane run a binary compiled in a deleted worktree and report violations from a tree that is gone

Three lanes on 2026-09-08 (`the-store-readme-describes-store-core`,
`claude-md-links-resolve-nowhere`, `compose-context-and-fiber`) each opened
red on a gate that had nothing to do with their change: `just memos-check`
and `cargo test --test layer_headers` failed naming
`.../<some-other-lane>/memos/SYSTEM.md is missing`. The gates read their tree
through `env!("CARGO_MANIFEST_DIR")`, which cargo tracks as an `env-dep` and
kache does not — kache keys on source bytes — so a lane is handed the binary
the previous lane compiled, with that lane's now-deleted path baked in.
`kache purge --crate-name <target>` plus a `touch` clears it.

The danger is not the false red. A gate whose tree pointer is stale can also
pass: the same binary run from a lane whose sources it never saw reports green
over the wrong directory. That overturns the condition
[[lanes-not-a-shared-tree]] set when it rejected a shared target dir.

Measured 2026-09-08: the shared `target/` carries this, and kache is second.
A machine-local `.cargo/config.toml` at the trunk sets
`[build] target-dir = "target"`, and every worktree under the trunk walks up
to it — `cargo metadata` in a lane printed `/Users/feb/dev/memory/target`.
Cargo's artifact name for an integration test does not vary with the worktree
path: two lanes both built `layer_headers-c4f7c987e8ed3a74`, one file, each
overwriting the other's `env!("CARGO_MANIFEST_DIR")`. Cargo's build lock
serialises the two builds and nothing serialises the gap between a lane's
build and its run, which is why three concurrent lanes went red and a
sequential A-then-B reproduction did not: run alone, cargo sees the
`# env-dep:CARGO_MANIFEST_DIR=` line of the dep-info change and recompiles,
and kache probes for dep-info before it answers. The false green needs no
miscache — one sibling's `cargo test` landing between this lane's build and
its run is enough.

## Do

Make a lane's gate read the lane it runs in. Either give each worktree its own
`CARGO_TARGET_DIR` in `just lane`, or add `CARGO_MANIFEST_DIR` to the cache
key kache computes for a test target — whichever the measurement in
[the-build-cache-is-off-while-its-store-sits-over-limit](../the-build-cache-is-off-while-its-store-sits-over-limit/prd.md) leaves affordable.
Do not fix it by having the gates locate the tree at runtime instead of
through `env!`: that hides the miscache from every other test that uses the
macro.

## Acceptance
From a fresh `just lane <name>` opened straight after another lane was
removed, `just memos-check` and `cargo test --test layer_headers` are green
with no `touch` and no `kache purge`, and a deliberate record violation
introduced in that lane turns the gate red naming the lane's own path.

Ran 2026-09-08 and green. `just lane` now writes the new worktree its own
`.cargo/config.toml` (`[build] target-dir = "target"`, resolved against the
lane's own root); a nearer config wins over the trunk's, so the lane compiles
and runs its own binary. Probe lane B removed, probe lane C opened:
`just memos-check` green in 46 s cold and `cargo test --test layer_headers`
green, no `touch` and no `kache purge`; a record violation planted in that
lane alone turned the gate red on
`.../stale-probe-c/memos/SYSTEM.md is missing` and on a `link to nothing:`
for a planted wikilink — the lane's own path both times. The trunk's
`.cargo/config.toml` is machine-local and stays: worktrees that already share
the trunk's `target/` keep it, and only new lanes are isolated.

**A third symptom, measured 2026-09-08.** The shared `target/` does not only
hand a lane the wrong test binary. `tests/e2e` starts a daemon from
`target/debug/memory`; a sibling lane rebuilding that path while the test runs
makes the live daemon hand over mid-assertion — `handing over to new binary` in
its log — and the test fails on a machine where nothing is wrong. Seen on
`gnn_recall::recall_over_a_graph_the_gnn_has_propagated`, green on re-run
alone, alongside three `hub::vanished_root_reaper_*` and one `rpc` health test
that behave the same way. The per-worktree target dir this memo lands closes
all of it; until it lands, a red from a full-suite run while other lanes build
proves nothing.
