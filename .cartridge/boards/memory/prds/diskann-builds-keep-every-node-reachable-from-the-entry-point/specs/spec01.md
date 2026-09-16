---
complexity: small
footprint:
  - src/graph/src/diskann.rs
  - .cartridge/tests/unit/src/graph/src/tests/diskann_test.rs
---

# spec01 — the Vamana prune keeps diverse edges so the graph stays connected

Base: memory.ctg a9ab81a. No `needs`. Probe: analyst dir `probe-vamana.diff` (`PDIVERSE` branch).

## Steps

1. In `robust_prune` (diskann.rs:111), score and sort the deduped candidates once. When
   `alpha > 1.0`, first run the occlusion selection with `alpha = 1.0`. Then append entries
   from the `alpha` selection that are not already chosen, up to `r`. Keep the ordering
   deterministic: BTreeSet dedupe and stable sort as today.
2. In diskann_test.rs, add a clustered-corpus helper: 1024-d, noise 0.6 around random
   centres, clusters larger than r+1, sized to run in seconds in release (start at 64 × 40).
   Add non-ignored `diskann_build_reaches_every_node_on_clustered_corpus` (BFS from `entry`
   over `build_adjacency`) and `diskann_recall_on_clustered_corpus` (top-10 recall >= 0.90
   against `brute_topk`). **Before step 1, run both at a9ab81a, confirm they fail, and
   record the output in the report.** If they don't fail, grow the clusters until they do.
3. Add ignored `diskann_clustered_10k_measure`: 10,000 rows, 64 centres, eprintln
   reachability, recall and build time. Run it once in release and record the numbers.

## Acceptance

- [ ] Both new small-corpus tests fail at a9ab81a (output recorded) and pass after step 1.
- [ ] `the_same_corpus_builds_a_byte_identical_index` and all existing diskann tests pass.
- [ ] The ignored 10k measurement is recorded: 10000/10000 reachable, recall >= 0.90, build time.

## Verify and Proof

```sh
# The coordinator warms this release target before collection.
cd memory.ctg
CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target cargo test --release -p graph --lib diskann
```
