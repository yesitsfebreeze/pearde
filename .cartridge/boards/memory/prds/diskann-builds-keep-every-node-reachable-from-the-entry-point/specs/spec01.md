---
complexity: small
footprint:
  - src/graph/src/diskann.rs
  - .cartridge/tests/unit/src/graph/src/tests/diskann_test.rs
---

# spec01 — the Vamana prune escalates alpha over one occlusion factor

Base: memory.ctg a9ab81a. No `needs`. Evidence: analyst-1.md, `probe-vamana.diff`, and review.md round 1.

## Steps

1. **Red first.** In diskann_test.rs, add a clustered-corpus helper: 1024-d, 64 random
   centres in [-0.5,0.5], noise 0.6·(U−0.5), seed 3, rows assigned `i % 64`. Add non-ignored
   tests, both built with default `Params` on 64 × 40:
   - `diskann_build_reaches_every_node_on_clustered_corpus`: BFS from `medoid` over
     `build_adjacency` reaches all 2560 nodes.
   - `diskann_recall_on_clustered_corpus`: 20 queries around the centres,
     `DiskIndex::search(q, 10, 96)`, top-10 recall >= 0.90 against `brute_topk`.

   Run `cargo test --release -p graph --lib diskann_` at a9ab81a. Paste the failing
   output (about 40/2560 reachable, recall 0.000) and the build time into the implementer's
   report. 64 × 34 is the smaller fallback (102/2176, recall 0.100 at HEAD).
2. **Fix.** Rewrite `robust_prune` (diskann.rs:111) as microsoft/DiskANN `occlude_list`:
   - Dedupe through a BTreeSet, score once, and stable-sort by distance, as today.
   - Keep `occlude[j] = 0.0` for each candidate. For `cur_alpha` in `1.0`, then `alpha`
     (only `1.0` when `alpha <= 1.0`), scan in order. Pick j when `occlude[j] <= cur_alpha`
     and it is not yet chosen, and stop at `r`. For every later unchosen k, set
     `occlude[k] = max(occlude[k], d(p,k) / d(j,k))`. When `d(j,k) == 0`, set it to
     `+inf`.
   - Leave the callers (`:233`, `:241`) unchanged.
3. Add ignored `diskann_clustered_10k_measure`: 10,000 rows, same corpus shape. It eprintlns
   reachability, recall and build time. Run it once in release and paste the output into the
   implementer's report.

## Acceptance

- [x] Both new tests fail at a9ab81a (output in the implementer's report) and pass after step 2.
- [x] The 64 × 40 build after step 2 takes no more than 1.5× the a9ab81a build time recorded in step 1 (review probe: 8.1 s against 8.5 s).
- [x] `the_same_corpus_builds_a_byte_identical_index` and all existing diskann tests pass.
- [x] The ignored 10k measurement is recorded: 10000/10000 reachable, recall >= 0.90, build no more than 84 s.

## Verify and Proof

```sh
# The coordinator warms this release target before collection.
CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target cargo test --release -p graph --lib diskann
```
