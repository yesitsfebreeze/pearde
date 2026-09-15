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

# the vector decoder uses fixed-size byte arrays so the installed compiler's Clippy gate passes

## Do

In `src/store_core/src/lib.rs` and `src/graph/src/diskann.rs`, decode each
complete four-byte chunk with
`as_chunks::<4>()` and pass its array directly to `f32::from_le_bytes` or `u32::from_le_bytes`.
The trailing incomplete bytes retain the existing behavior. Rust 1.98's
Clippy rejects the current `chunks_exact(4)` loop under `-D warnings`.

## Acceptance
`just check` passes and `cargo test -p store_core -p graph` passes.

**Done 2026-09-08.** Already true in the tree: every four-byte decode site
uses `as_chunks::<4>()` and hands the array straight to `f32::from_le_bytes`
or `u32::from_le_bytes` — `decode_vec_into` in `src/store_core/src/cold.rs`
(the decoder moved out of `lib.rs`), and the graph validation loop, `vec_at`
and `neighbors_at` in `src/graph/src/diskann.rs`. `rg 'chunks_exact' src`
answers nothing. Check run literally on rustc 1.94.0: `just check` green
(fmt + `clippy --workspace --all-targets -D warnings`), `cargo test -p
store_core -p graph` 234 passed, 0 failed. No code change was needed.
