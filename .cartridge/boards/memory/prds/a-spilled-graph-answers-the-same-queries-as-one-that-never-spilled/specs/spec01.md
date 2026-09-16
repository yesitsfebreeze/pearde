---
complexity: small
footprint:
  - src/graph/src/diskann.rs
  - .cartridge/tests/integration/spill_transparency.rs
---

# spec01 — DiskIndex ranks its final beam exactly, ties broken by id

Cause (source evidence, memory.ctg 5097a83): `DiskIndex::search`
(src/graph/src/diskann.rs:482-494) truncates the greedy beam to k in the order of
the f32 `cos_dist` (:58) sorted by `total_cmp` alone (:101), with no id
tie-break. The test corpus (`sparse_vec_seeded`, 7 hashed ±1 words in 64 dims)
is tie-heavy: 173/200 queries have a tie at rank 10, and 1964/2000 spilled
scores are not bit-equal to the brute-force score, so float rounding, not the
graph, picks which tied id survives. Tie-aware recall (hit score >= brute 10th
score - 1e-5) is 1.0000 at both a9ab81a and 5097a83. The 5097a83 prune only
reshuffled which tied ids the beam holds (0.8410 -> 0.8370). The "Apple
Silicon" TEMPORARY floors (0.84 / 0.16 / 0.84) stem from the same cause: the
noise depends on the platform's float kernels.

Base: memory.ctg 5097a83 or later. No dependencies.

## Steps

1. In `DiskIndex::search` (src/graph/src/diskann.rs), after `greedy`, rescore
   each beam member with `math::cosine_distance(query, &self.vec_at(i))` (f64,
   the kernel the resident HNSW uses), sort by distance then `self.ids[i]`, then
   truncate to k. Leave `greedy` and `robust_prune` alone: the build bytes and
   the reachability tests depend on them. A probed diff is in
   `attempt-diskann-search-rerank.diff` next to this spec.
2. In .cartridge/tests/integration/spill_transparency.rs, restore the original
   floors and delete the three TEMPORARY comments: `cold_recall >= 0.99`,
   `hot_recall - cold_recall <= 0.01`, overlap `>= 0.99`. With step 1 applied
   the probe measured spilled 1.0000, overlap 1.0000, top1 1.0000.

## Acceptance

- [ ] `cargo nextest run -p memory --test spill_transparency` exits 0 on 3 consecutive runs.
- [ ] The spilled floors are back at 0.99: the file contains `cold_recall >= 0.99` and no `TEMPORARY` comment.
- [ ] `cargo test --release -p graph --lib diskann` exits 0, including `diskann_build_reaches_every_node_on_clustered_corpus`, `diskann_recall_on_clustered_corpus` and `recall_at_10_is_high_vs_brute_force`.

## Verify and Proof

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/spill-transparency-verify}"
grep -q "cold_recall >= 0.99" .cartridge/tests/integration/spill_transparency.rs
! grep -q "TEMPORARY" .cartridge/tests/integration/spill_transparency.rs
for n in 1 2 3; do
  cargo nextest run -p memory --test spill_transparency
done
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/spill-transparency-verify}"
log="${TMPDIR:-/tmp}/spill-diskann-verify.log"
cargo test --release -p graph --lib diskann > "$log" 2>&1
grep -q "diskann_build_reaches_every_node_on_clustered_corpus ... ok" "$log"
grep -q "diskann_recall_on_clustered_corpus ... ok" "$log"
grep -q "recall_at_10_is_high_vs_brute_force ... ok" "$log"
```
