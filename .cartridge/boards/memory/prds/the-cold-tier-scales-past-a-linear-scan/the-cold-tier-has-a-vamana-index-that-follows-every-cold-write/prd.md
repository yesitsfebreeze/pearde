---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "open"
origin: requested
priority: 60
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
needs: ["@memory/diskann-builds-keep-every-node-reachable-from-the-entry-point"]
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

The Vamana build defect this depends on (graphs split into closed clusters, recall 0.000 at
10k clustered rows) is owned by `@memory/diskann-builds-keep-every-node-reachable-from-the-entry-point`.

No model-stamp prerequisite: `a-vector-carries-the-model-that-made-it` is deferred as
withdrawn; the per-store `EmbedStamp` plus the width check already gate mixed models,
and `memory reembed` rewrites every cold row through `cold_put_all`, which lands in the
since-build set.

## Acceptance

- [ ] After each of `cold_spill`, `cold_put_all`, `cold_rekey`, `cold_relocate` and `import_snapshot`, a second `Store::open` of the same dir reads a since-build set naming exactly the written and deleted ids.
- [ ] A build that fails before stamping leaves the previous snapshot and the since-build set intact (test injects a failing build dir).
- [ ] An ignored measurement records build time at 100,000 rows; no build runs inside a query or under the graph write lock.

## Verify

```sh
cargo nextest run -p graph cold
cargo nextest run -p store_core cold
```

Split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 (analyst-2). It inherits the parent's used review rounds: none.
