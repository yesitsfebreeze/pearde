---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 60
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - src/graph/src/diskann.rs
  - src/graph/src/graph.rs
  - src/store/core/src/cold.rs
  - src/store/core/src/lib.rs
  - .cartridge/tests/unit/src/graph/src/tests/diskann_test.rs
  - .cartridge/tests/unit/src/store/core/src/tests
---

# The cold tier has a Vamana index that follows every cold write

The cold tier is a vector side table with no index (`Store::cold_visit_vectors`,
`src/store/core/src/cold.rs:224`). Build a DiskANN snapshot of it under
`<data_dir>/diskann/cold`, reusing `build_and_save_with_epoch` and `DiskIndex`, and make
every write since that build visible without a rescan: the cold writers
(`import_snapshot`, `cold_spill`, `cold_put_all`, and `cold_move` behind `cold_rekey` and
`cold_relocate`) record the ids they put or delete in a persisted since-build side table
inside the same transaction, so another process's writes are seen too (closing the gap
the access-stamp cache names at `cold.rs:240`). A rebuild runs off the query path and the
graph write lock when the since-build set outgrows the snapshot (the `outgrown` rule of
`reconcile_disk`, `graph.rs:120`), and clears the set only with the new stamp.

Blocker found by probe, owned here: at default params (`r=32, build_l=64, alpha=1.2`),
a 1024-d corpus clustered around 64 centres gave top-10 recall 1.000 at 2,000 rows and
0.000 at 10,000 rows (release, one thread; build 5.7 s at 2k, 56 s at 10k). Reproduce
before building on it: either the probe or the Vamana build is wrong at that scale, and
the hot tier uses the same build above `disk_threshold`.

No model-stamp prerequisite: `a-vector-carries-the-model-that-made-it` is deferred as
withdrawn; the per-store `EmbedStamp` plus the width check already gate mixed models,
and `memory reembed` rewrites every cold row through `cold_put_all`, which lands in the
since-build set.

## Acceptance

- [ ] A (non-ignored) unit test indexes a 10,000-row 1024-d clustered corpus and asserts top-10 recall against brute force >= 0.90, the documented threshold; it fails at HEAD a9ab81a.
- [ ] After each of `cold_spill`, `cold_put_all`, `cold_rekey`, `cold_relocate` and `import_snapshot`, a second `Store::open` of the same dir reads a since-build set naming exactly the written and deleted ids.
- [ ] A build that fails before stamping leaves the previous snapshot and the since-build set intact (test injects a failing build dir).
- [ ] An ignored measurement records build time at 100,000 rows; no build runs inside a query or under the graph write lock.

## Verify

```sh
cargo nextest run -p graph diskann
cargo nextest run -p store_core cold
```

Split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 (analyst-2). It inherits the parent's used review rounds: none.
