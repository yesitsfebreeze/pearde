---
repo: "/Users/feb/dev/cartridge/memory.ctg"
state: "done"
origin: requested
priority: 70
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - src/graph/src/diskann.rs
  - .cartridge/tests/unit/src/graph/src/tests/diskann_test.rs
commit: "5097a83cc0cece79bc4b0f804819a718a7bc976d"
---

# DiskANN builds keep every node reachable from the entry point

## Outcome

At default params (`r=32, build_l=64, alpha=1.2`), a Vamana build over a clustered 1024-d
corpus splits into closed clusters once a cluster has more than r+1 rows. Search from the
medoid entry then sees one cluster, and recall collapses (64 × 40: 40/2560 reachable,
recall@10 0.000).
Root cause: `robust_prune` (`src/graph/src/diskann.rs:148`) runs pass 2 as an independent
α=1.2 selection. With concentrated intra-cluster distances that selection degenerates to
the r nearest (`:137`), and the back-edge re-prune (`:239-241`) evicts the last cross edges.
`disk_threshold` defaults to 0 (`src/config/src/config.rs:717`), so every store-backed graph
builds and searches through this path today (`graph.rs:427`, `:559-563`).
Fix: the reference prune from microsoft/DiskANN (`occlude_list`). Raise `cur_alpha` from 1.0
to α over one running occlusion factor per candidate. Evidence: analyst-1.md and round 1 of
review.md.

## Acceptance

- [x] A non-ignored test on a 64 × 40, 1024-d clustered corpus asserts every node is reachable from `entry` by BFS over the built adjacency; its failing output at a9ab81a is recorded in the implementer's report.
- [x] A non-ignored test on the same corpus asserts top-10 recall >= 0.90 against brute force with `search(q, 10, 96)`; its failing output at a9ab81a is recorded in the implementer's report, and the build takes no more than 1.5× the a9ab81a build time in release.
- [x] `the_same_corpus_builds_a_byte_identical_index` and every existing diskann test still pass.
- [x] An ignored test records reachability, recall and build time at 10,000 rows (64 centres), and the build takes no more than 1.5× HEAD's 56 s.

## Proof and recovery

The on-disk format is unchanged. Recovery is limited: a snapshot whose epoch matches the
store is reused as-is (`diskann.rs:178-181`). A stale snapshot is reconciled through the
delta, not rebuilt (`graph.rs:587-622`). So a broken graph built before the fix persists
until one of these happens:
- a write stales it and `consolidate_disk_index` runs (`memory prune`, `memory audit`, a
  re-key, or check repair);
- the delta outgrows it;
- the operator removes `<data_dir>/diskann/`, and the next load does a full build
  (`graph.rs:624-628`).

No build-version marker is added; that would be a follow-up outside this footprint.

## Dependencies and review

No `needs`. The cold-tier Vamana child needs this PRD and shares `diskann.rs`, so this one
integrates first. Review: review.md.

## Coordinator evidence

2026-09-16 10:25Z, cartridge-c4. The coordinator reran the ignored 10k measurement at load 6.95, lane 5097a83: `reachable 10000/10000, recall@10 1.000, build_adjacency 51.58s`, within the 84 s bound. verifier-1.md is PASS on every other box.
