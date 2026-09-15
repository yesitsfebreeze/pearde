---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1h"
---

# src/store/README.md describes store_core — move it to the crate it documents and give `store` a README that names the registry, or delete it and leave lib.rs the front door

## Do

`src/store/README.md` is titled "the LMDB storage primitive and its advisory
lock" and its body describes the environment, the hot/cold tiers, the embedding
index and `Lock` — all of which live in `src/store_core`, which has no README.
`src/store/src/lib.rs` says `store` is the per-process registry of open stores
and the persist-closure factory. The wrong layer line that made this visible is
already gone ([[a-readme-restated-the-layer-line-and-nine-of-fifteen-drifted]]);
the misplaced body is what is left.

Move `src/store/README.md` to `src/store_core/README.md`, and decide the second
half rather than assuming it: either `store` gets a README naming the registry,
or it gets none and `src/store/src/lib.rs` is its front door — the same choice
the eight crates that already carry no README made. Check the `## ABI` block
that travels with the file against `src/store_core/src/lib.rs` before it lands;
the one in `src/llm/README.md` typed two `u64` constants as `u32`, so these
blocks are ungated too.

**Done 2026-09-08.** The file is `src/store_core/README.md`, moved by
`git mv` so the history follows it, and `store` gets none: its `lib.rs` is
sixteen lines whose `//!` header already says the crate is the per-process
registry over `store_core`'s environment, so a README could only restate it —
the ninth crate to take that choice. The ABI block was wrong in three places
against `src/store_core/src/lib.rs`: it named a `pub mod base_store` the split
dissolved (`Store` and its `cold_*` methods sit at the crate root, `cold` is
private and re-exports only `ColdRow`), it called the lock `Lock` where the
type is `WriterLock`, and its tests line ran `cargo test -p store`. So was one
invariant: "one store per directory, enforced by `Lock`" is false —
`Store::open` takes no lock at all, `lock::acquire` is advisory and only
writers ask for it (`commands_serve`, `reembed`, `gc`, `rekey`, `consolidate`,
`migrate`), which is why a reader opens the same dir freely.

## Acceptance
`rg -l 'LMDB' src/*/README.md` names `src/store_core/README.md` and not
`src/store/README.md`, and `just check` is green.
