---
kind: work
level: 10
status: done
estimate: 1h
description: the vector decoder uses fixed-size byte arrays so the installed compiler's Clippy gate passes
read_when: "a workspace check fails on chunks_exact_to_as_chunks"
---

# the-vector-decoder-passes-the-current-lint

## Do

In `src/store_core/src/lib.rs` and `src/graph/src/diskann.rs`, decode each
complete four-byte chunk with
`as_chunks::<4>()` and pass its array directly to `f32::from_le_bytes` or `u32::from_le_bytes`.
The trailing incomplete bytes retain the existing behavior. Rust 1.98's
Clippy rejects the current `chunks_exact(4)` loop under `-D warnings`.

## Check

`just check` passes and `cargo test -p store_core -p graph` passes.

**Done 2026-09-08.** Already true in the tree: every four-byte decode site
uses `as_chunks::<4>()` and hands the array straight to `f32::from_le_bytes`
or `u32::from_le_bytes` — `decode_vec_into` in `src/store_core/src/cold.rs`
(the decoder moved out of `lib.rs`), and the graph validation loop, `vec_at`
and `neighbors_at` in `src/graph/src/diskann.rs`. `rg 'chunks_exact' src`
answers nothing. Check run literally on rustc 1.94.0: `just check` green
(fmt + `clippy --workspace --all-targets -D warnings`), `cargo test -p
store_core -p graph` 234 passed, 0 failed. No code change was needed.
