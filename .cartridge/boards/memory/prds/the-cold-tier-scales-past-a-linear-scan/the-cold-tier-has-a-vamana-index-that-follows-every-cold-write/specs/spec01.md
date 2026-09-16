---
complexity: large
footprint:
  - src/store/core/src/lib.rs
  - src/store/core/src/cold.rs
  - src/graph/src/lib.rs
  - src/graph/src/graph.rs
  - src/graph/src/cold_index.rs
  - src/tick/src/tick_queue.rs
  - src/tick/src/tick_pulse.rs
  - src/tick/loop/src/tick.rs
  - src/tick/loop/src/tick_tasks.rs
  - .cartridge/tests/unit/src/store/core/src/lib/tests.rs
  - .cartridge/tests/unit/src/graph/src/tests/cold_index_test.rs
  - .cartridge/tests/unit/src/tick/loop/src/tests/tick_tasks_test.rs
---

# spec01 — a cold Vamana snapshot, a sequenced since-build set, and a lock-free builder

Base: memory.ctg 5097a83 (the prerequisite DiskANN fix has landed). All names below are new
unless cited. Evidence: review.md round 1, analyst-1.md, analyst-2.md.

## Contract (what the sibling `a-query-reads-the-cold-tier-through-its-index` reads)

- **Sequence.** `meta` key `cold_seq` (u64) is bumped once in every cold writer's own
  write transaction. `Store::cold_seq()` reads it. `Store::read_epoch` is not used: cold
  writes never move it (`lib.rs:704` is its only writer).
- **Since-build set.** Add the LMDB table `cold_since`, raising `MAX_DBS` from 5 to 6
  (`lib.rs:36`). `read_graph` and compaction open through the same const (`cold.rs:629`), so
  that change covers them too. Each entry is `id -> (op: put|delete, seq)`, where `seq` is the
  transaction's new `cold_seq`, and the last write to an id wins.
- **Snapshot.** `<data_dir>/diskann/cold` is built by `build_and_save_with_epoch(.., Some(S))`,
  where S is the `cold_seq` read **in the same read transaction** as the vector scan
  (`Store::cold_snapshot_vectors(visit) -> S`). Beside the snapshot, the build writes an
  `embed` file (the encoded `EmbedStamp`).
- **Clear.** `Store::clear_cold_since_build(S)` deletes only entries with `seq <= S`, so any
  write that lands during a build keeps its entry. It runs only after
  `diskann::snapshot_epoch(dir) == Some(S)` reads back (the stamp write is best-effort,
  `diskann.rs:300`). A crash between swap and clear leaves a superset, which is harmless:
  the sibling rescored every since-build id from its live vector anyway.
- **Handle.** `GraphGnn.cold_idx: Option<Arc<DiskIndex>>` is exposed as
  `GraphGnn::cold_index() -> Option<(Arc<DiskIndex>, u64 /*S*/)>`. Load opens it if present;
  the runner swaps it.
- **Freshness, for the sibling.** The index answers for the tier as the snapshot ids,
  overridden by every since-build entry: `delete` is a tombstone, and `put` means rescore
  from the live vector. It is usable only when `cold_seq() >= S` and the `embed` file
  equals the store's `EmbedStamp`. Otherwise the sibling takes its exact scan.

## Steps

1. **store_core (lib.rs, cold.rs).** Add `cold_seq`, the `cold_since` table,
   `cold_since_build() -> Vec<(String, Op, u64)>`, `cold_snapshot_vectors` and
   `clear_cold_since_build`. In `import_snapshot` (`cold.rs:148`), `cold_spill` (`:175`),
   `cold_put_all` (`:310`) and `cold_move` (`:430`, which serves `cold_rekey` and
   `cold_relocate`), bump the sequence and write the entries inside the existing
   transaction: `cold_move` writes delete(old) and put(new).
2. **Builder (new `src/graph/src/cold_index.rs`, `mod` in `graph/src/lib.rs`).**
   `pub fn build(store: &Store, data_dir: &Path, hook: &dyn Fn(Phase)) -> io::Result<Option<(DiskIndex, u64)>>`.
   It takes no `GraphGnn`, so it cannot hold the graph lock. The steps are:
   1. Take a non-blocking flock on `<data_dir>/diskann/cold.lock` with
      `store_core::lock::try_lock_patiently`, the same pattern as cartridge.ctg a965d6e's
      run-dir lock. If the lock is held, return `Ok(None)`: another process is building.
   2. Scan with `cold_snapshot_vectors` to get S.
   3. `hook(Phase::Scanned)`.
   4. Call `build_and_save_with_epoch(dir, items, Params::default(), Some(S))` and write the `embed` file.
   5. Read back the stamp, `clear_cold_since_build(S)`, then `DiskIndex::open`.

   The lock is held across staging, swap and clear, so a daemon and a CLI can't clobber
   `cold.staging`. `hook` exists for tests; production passes `&|_| {}`.
3. **Runner (tick).** Add `TaskKind::ColdIndexBuild` in `tick_queue.rs` with rank 2. It is
   graph-global, keyed `""`, so at most one is pending. `tick.rs` dispatches it to
   `tick_tasks::do_cold_index_build(g)`:
   1. Under `g.read()`, clone `store()` and `data_dir`, then drop the guard.
   2. Call `cold_index::build` with no graph lock held.
   3. On `Some`, take `g.write()` only to assign `cold_idx`.

   `tick_pulse.rs` enqueues it when the store has cold rows and one of these holds:
   - there is no snapshot;
   - `cold_since_build().len() >= snapshot len` (`>=`, so a full `reembed` or `import`
     at equal size rebuilds);
   - the `embed` file differs from `embed_stamp()`;
   - the snapshot `dim` differs from the store width.
4. **Relation to the hot path.** `reconcile_disk`'s `outgrown` rebuild (`graph.rs:122-127`)
   and `consolidate_disk_index` both run the Vamana build under the write lock:
   `graph.rs:633` "COST: the Vamana build runs under the graph WRITE lock", and
   `tick_tasks.rs:484` calls `g.write().consolidate_disk_index()`. This PRD adds a separate
   cold path and **does not change** the hot path. Moving the hot build off the lock is a
   follow-up.
5. **Tests**, with exact names; none exist at 5097a83. In `store/core/src/lib/tests.rs`:
   - `cold_since_build_names_every_writer`: one case per writer (`cold_spill`,
     `cold_put_all`, `cold_rekey`, `cold_relocate`, `import_snapshot`). **Drop the first
     `Store`, then reopen** the dir. Assert the set names exactly the ids put and deleted,
     with rising `seq`.
   - `cold_since_build_clear_keeps_entries_after_the_stamp`: capture S, write id x again,
     `clear(S)`, and x remains.

   In `graph/src/tests/cold_index_test.rs`:
   - `cold_index_write_during_build_survives_the_clear`: the hook at `Phase::Scanned` does
     `cold_spill(y)` on an id already in the set. After the build, y's entry remains with
     seq > S, and the index does not contain y's new vector.
   - `cold_index_failed_build_keeps_snapshot_and_set`: build once, write, then create a
     regular file at `<data_dir>/diskann/cold.staging`. The build returns `Err`, the old
     snapshot opens with its old S, and the set is unchanged.
   - `cold_index_second_builder_skips_while_locked`: hold `cold.lock` and assert `Ok(None)`.

   In `tick/loop/src/tests/tick_tasks_test.rs`:
   - `cold_index_build_leaves_the_graph_write_lock_free`: run `do_cold_index_build` on a
     thread with a hook that blocks on a channel (5 s timeout). The main thread takes
     `g.write()` and drops it, then signals. Assert the write lock was taken before the build
     finished and that `cold_index()` is `Some` afterwards.

   A timed-out hook fails the test.
6. **Measurement.** Add an ignored `cold_index_build_100k_measure` (cold_index_test.rs), run
   once with `cargo test --release -p graph --lib cold_index_build_100k_measure -- --ignored --nocapture`.
   Paste its build time and peak RSS into the implementer's report (the Result section of
   collection.md). It is not part of Verify.

## Scoped out

- The `cold_move` chain-ordering bug: moves apply in key order, so A→B then B→C can carry
  A's vector to C. It is filed separately as `defect-cold-move-chain`; the set records
  whatever `cold_move` wrote.
- An older binary that writes cold rows bypasses the set. One host per project and
  `writer.lock` make this rare; a row-count guard is a follow-up.
- Moving the hot `consolidate_disk_index` build off the write lock (see step 4).

## Acceptance

- [ ] `cold_since_build_names_every_writer` passes. After each of the five writers, a reopened store (first handle dropped) reads a set naming exactly the ids put and deleted.
- [ ] `cold_since_build_clear_keeps_entries_after_the_stamp` and `cold_index_write_during_build_survives_the_clear` pass: a write after the captured sequence survives the clear.
- [ ] `cold_index_failed_build_keeps_snapshot_and_set` passes: the previous snapshot and the set are intact after an injected failure.
- [ ] `cold_index_second_builder_skips_while_locked` passes: a second builder does not touch `cold.staging`.
- [ ] `cold_index_build_leaves_the_graph_write_lock_free` passes, and `cold_index::build` takes no `GraphGnn`.
- [ ] The 100k build time is recorded in the implementer's report (ignored test, release).
- [ ] Every Verify block fails at 5097a83, because no test matches under `--no-tests=fail`.

## Verify and Proof

The isolated target dir is shared by both passes (lane root, then memory.ctg), so it stays
out of the watched `target/debug`. The coordinator warms it before collection by running
each block's command with `--no-run` added.

```sh
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/cold-index-verify
cargo nextest run --no-tests=fail -p store_core -E 'test(/::cold_since_build_names_every_writer$/) or test(/::cold_since_build_clear_keeps_entries_after_the_stamp$/)'
```

```sh
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/cold-index-verify
cargo nextest run --no-tests=fail -p graph -E 'test(/::cold_index_write_during_build_survives_the_clear$/) or test(/::cold_index_failed_build_keeps_snapshot_and_set$/) or test(/::cold_index_second_builder_skips_while_locked$/)'
```

```sh
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/cold-index-verify
cargo nextest run --no-tests=fail -p tick_loop -E 'test(/::cold_index_build_leaves_the_graph_write_lock_free$/)'
```
