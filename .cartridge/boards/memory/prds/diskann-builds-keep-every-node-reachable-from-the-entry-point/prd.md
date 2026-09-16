---
repo: "/Users/feb/dev/cartridge/memory.ctg"
state: "analyzing"
origin: requested
priority: 70
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - src/graph/src/diskann.rs
  - .cartridge/tests/unit/src/graph/src/tests/diskann_test.rs
claim: "coordinator-c4-11 2026-09-16T08:43:51.717Z"
---

# DiskANN builds keep every node reachable from the entry point

## Outcome

The Vamana build can split into closed clusters. At default params (`r=32, build_l=64,
alpha=1.2`) on a 1024-d corpus clustered around 64 centres, 10,000 rows, only 156 of
10,000 nodes are reachable from the medoid entry, and top-10 recall is 0.000. At 2,000
rows (31 rows per cluster, fewer than r) recall is 1.000.
Root cause: `robust_prune` (`src/graph/src/diskann.rs:148`) never occludes intra-cluster
candidates when their distances are concentrated (1.2 × 0.26 > 0.26), so it keeps the r
nearest (`:137`). The back-edge re-prune (`:239-241`) then evicts every cross-cluster
edge, and search from the single entry (`:275`, `:477`) stays in the entry's cluster. The
hot tier uses this build above `disk_threshold` (`graph.rs`), so dense topics with more
than r+1 near neighbours can silently lose recall today. Fix inside `diskann.rs`: when
`alpha > 1`, keep the `alpha = 1.0` selection first and fill the remaining slots from the
`alpha` selection, scoring the candidates once. Probed, this gives 10000/10000 reachable
and recall 1.000 at 10k, with a build of 72 s against 56 s.

## Acceptance

- [ ] A non-ignored test builds a clustered 1024-d corpus with clusters larger than r+1 and asserts that every node is reachable from `entry` by BFS over the built adjacency; the implementer shows it failing at a9ab81a (recorded output).
- [ ] A non-ignored test on that small corpus asserts top-10 recall against brute force >= 0.90; the implementer shows it failing at a9ab81a (recorded output).
- [ ] `the_same_corpus_builds_a_byte_identical_index` and every existing diskann test still pass.
- [ ] An ignored test records reachability, top-10 recall and build time on the 10,000-row 1024-d 64-centre corpus.

## Proof and recovery

Probe patch (env-gated, not for landing):
`prd.ctg/.cartridge/boards/memory/.state/loop/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write/probe-vamana.diff`;
report `analyst-1.md` next to it. The small-corpus size (for example 64 × 40) is not
probed. Pick it so both new tests fail at a9ab81a in release. The existing on-disk
format is unchanged. Snapshots built before the fix stay readable, and they reconnect
at the next rebuild.

## Dependencies and review

No `needs`. `@memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write` needs this and shares `diskann.rs` and its test file, so this one integrates first.
