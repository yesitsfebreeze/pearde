---
complexity: large
footprint:
  - src/graph/src/graph.rs
  - src/store/core/src/cold.rs
  - src/store/core/src/lib.rs
  - .cartridge/tests/unit/src/store/core/src/tests
---

# spec01 — a cold Vamana snapshot with a persisted since-build set

Base: memory.ctg at or after the landing of
`@memory/diskann-builds-keep-every-node-reachable-from-the-entry-point` (needs).

## Steps

1. **Since-build table (store_core).** Add a table of (id, put|delete). `import_snapshot`,
   `cold_spill`, `cold_put_all` and `cold_move` (and so `cold_rekey` and `cold_relocate`)
   write it in their own transaction. Add a read API and a `clear_since_build(stamp)` that
   clears only under the stamp the build was taken at.
2. **Cold snapshot (graph.rs).** Build `<data_dir>/diskann/cold` with
   `build_and_save_with_epoch` from `cold_visit_vectors`. Trigger a rebuild with the
   `outgrown` rule of `reconcile_disk` (graph.rs:120). Run it off the query path and not under
   the graph write lock. On a failed build, keep the old snapshot and the since-build set.
3. Add an ignored test that records build time at 100,000 rows (build cost is about 56-72 s at 10k).

## Acceptance

- [ ] After each of `cold_spill`, `cold_put_all`, `cold_rekey`, `cold_relocate` and `import_snapshot`, a second `Store::open` of the same dir reads a since-build set naming exactly the ids written and deleted.
- [ ] A build that fails before stamping leaves the previous snapshot and the since-build set intact (the test injects a failing build dir).
- [ ] An ignored test records build time at 100,000 rows; no build runs inside a query or under the graph write lock.

## Verify and Proof

```sh
# The coordinator warms this release target before collection.
cd memory.ctg
CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target cargo nextest run -p store_core cold
```

```sh
# The coordinator warms this release target before collection.
cd memory.ctg
CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target cargo nextest run -p graph cold
```
