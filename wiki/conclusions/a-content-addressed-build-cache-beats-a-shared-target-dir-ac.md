---
title: a-content-addressed-build-cache-beats-a-shared-target-dir-ac
date: 2026-09-03
type: conclusion
tags: [build-cache, cargo, conclusion, rust, worktrees]
sources:
  - "[[260903-f241]]"
  - "[[260903-1eef]]"
derived_from: []
---

# a-content-addressed-build-cache-beats-a-shared-target-dir-across-worktrees

A content-addressed RUSTC_WRAPPER cache beats a shared CARGO_TARGET_DIR for parallel Rust builds across git worktrees: cargo's exclusive lock on the build directory serializes concurrent builds under a shared target dir and risks corruption, while a wrapper keeps each worktree's target/ private and dedupes only the artifact bytes through a content-addressed store, restored by hardlink or reflink depending on filesystem. sccache does not substitute for this — it skips proc-macro/bin/dylib crates and does no target-dir dedup — and cargo's own native shared cache (#5931) is not shipped yet. The tradeoff is incremental compilation, which the wrapper disables, so a changed workspace crate always recompiles fully even with a warm store.

Consequence: validate a wrapper globally before trusting it — run cargo check/test/clippy with and without RUSTC_WRAPPER set and diff the results; if anything changes, removing rustc-wrapper from the cargo config is a full, side-effect-free revert.
