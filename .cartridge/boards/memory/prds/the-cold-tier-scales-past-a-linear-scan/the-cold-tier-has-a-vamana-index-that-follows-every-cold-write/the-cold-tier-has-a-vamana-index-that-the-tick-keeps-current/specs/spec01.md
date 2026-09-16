---
complexity: large
footprint:
  - src/graph/src/lib.rs
  - src/graph/src/graph.rs
  - src/graph/src/persist.rs
  - src/graph/src/cold_index.rs
  - src/tick/src/tick_queue.rs
  - src/tick/src/tick_pulse.rs
  - src/tick/loop/src/tick.rs
  - src/tick/loop/src/tick_tasks.rs
  - .cartridge/tests/unit/src/graph/src/tests/cold_index_test.rs
  - .cartridge/tests/unit/src/tick/src/tests/tick_pulse_test.rs
  - .cartridge/tests/unit/src/tick/loop/src/tests/tick_tasks_test.rs
---

# spec01 — cold index builder, handle and tick runner

Base: memory.ctg with child A landed.

## Steps

1. **`src/graph/src/cold_index.rs`** (with `mod` in lib.rs, and tests via `#[path]` to
   cold_index_test.rs):
   - `enum Phase { Scanned, Opened, Swapped }`, with `hook: &dyn Fn(Phase)` on every entry
     point.
   - `pub fn build(store, data_dir, hook) -> io::Result<Option<Built>>`, where
     `Built { index: DiskIndex, seq: u64, skipped: usize, _lock: File }`. It takes no
     `GraphGnn`. The steps are:
     1. Take a non-blocking `try_lock_patiently` on `diskann/cold.lock`. If it is held,
        return `Ok(None)`.
     2. Scan with `cold_snapshot_vectors`, keeping only `v.len() == embed dim` and non-empty
        vectors, and counting the rest as `skipped`.
     3. `hook(Scanned)`.
     4. Call `build_and_save_with_epoch(dir, items, default, Some(S))` and write the `embed`
        file.
     5. Read back `snapshot_epoch == Some(S)` and `DiskIndex::open`.
     6. `hook(Opened)`.
   - `pub fn open(store, data_dir) -> Option<(DiskIndex, u64)>` returns the handle when it is
     usable.
   - `pub fn usable(store, s, dim) -> bool` holds when `s >= cold_since_floor()`,
     `s <= cold_seq()`, and the `embed` file equals `embed_stamp()`.
   - `pub fn wanted(store, handle) -> bool` holds in any of these cases:
     - there is no handle and `cold_len() > 0`;
     - the handle is not `usable`;
     - `cold_since_len() >= handle len`;
     - the handle's dim differs from the embed dim.
2. **graph.rs.** Add `cold_idx: Option<(Arc<DiskIndex>, u64)>` and
   `pub fn cold_index(&self)`, which returns it only if it is `usable`. The sibling must not
   keep the `Arc` past its read guard. **persist.rs** `graph_from_store` (`:29`) sets it
   from `cold_index::open`, which covers both `load_dir` and `reload_from_disk`.
3. **Tick.**
   - `tick_queue.rs`: add `TaskKind::ColdIndexBuild` (rank 2) and
     `Cadence.cold_index_at_secs`.
   - `tick_pulse.rs`: `maybe_enqueue_cold_index`, gated by `claim_slot` with
     `COLD_INDEX_INTERVAL = 600 s` and `wanted`, enqueued with key `""`.
   - `tick.rs` dispatches to `tick_tasks::do_cold_index_build(g, q, hook)`:
     1. Under `g.read()`, clone the store, the data dir and the handle, then drop the guard.
     2. If `!wanted`, return. If the disk snapshot is usable and newer, reopen it and swap
        it in.
     3. Call `build`.
     4. On `Ok(Some(b))`, `g.write()` assigns `(Arc::new(b.index), b.seq)`, then drop the
        guard.
     5. `hook(Swapped)`, then `clear_cold_since_build(b.seq)`, then drop the lock.
     6. On `Err`, call `q.record_task_failure` (the cadence slot is the backoff).
4. **Measurement.** Add an ignored `cold_index_build_100k_measure`, run as
   `cargo test --release -p graph --lib cold_index_build_100k_measure -- --ignored --nocapture`,
   with the time pasted into the implementer's report. If it takes more than 10 minutes,
   file the `spawn_blocking` follow-up.

## Tests (exact names)

graph, cold_index_test.rs:
- `cold_index_skips_rows_of_another_width`: one wrong-width row and one empty row give
  `skipped == 2`, and the index opens with n−2 rows.
- `cold_index_failed_build_keeps_snapshot_and_set`: a regular file at `cold.staging` makes
  the build `Err`; the old handle is still usable and the set is unchanged.
- `cold_index_second_builder_skips_while_locked`
- `cold_index_old_handle_is_unusable_after_a_newer_build_clears`
- `cold_index_trigger_rules`: each `wanted` case is true, and a fresh handle is false.

tick, tick_pulse_test.rs:
- `cold_index_enqueue_waits_for_its_cadence_slot`

tick_loop, tick_tasks_test.rs:
- `cold_index_build_leaves_the_graph_write_lock_free`: the hook at `Scanned` blocks on a
  channel with a 5 s timeout. The main thread asserts `g.try_write_for(5 s).is_some()`,
  then signals and joins.
- `cold_index_runner_swaps_before_clearing`: at `Swapped`, `g.read().cold_index()` holds
  the new S and `cold_since_len() > 0`; after the run the set is cleared.
- `cold_index_runner_records_a_failure`: a `cold.staging` file makes the run record a
  failure and leave the handle unchanged.

## Acceptance

- [ ] Every named test passes.
- [ ] Each block exits non-zero at 5097a83 ("no tests to run").
- [ ] The 100k build time is recorded in the implementer's report.

## Verify

The reviewer measured these blocks at 11–21 s cold and 0 s warm; the coordinator warms them
with `--no-run`.

```sh
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/cold-index-verify
cargo nextest run --no-tests=fail -p graph -E 'test(/::cold_index_skips_rows_of_another_width$/) or test(/::cold_index_failed_build_keeps_snapshot_and_set$/) or test(/::cold_index_second_builder_skips_while_locked$/) or test(/::cold_index_old_handle_is_unusable_after_a_newer_build_clears$/) or test(/::cold_index_trigger_rules$/)'
```

```sh
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/cold-index-verify
cargo nextest run --no-tests=fail -p tick -E 'test(/::cold_index_enqueue_waits_for_its_cadence_slot$/)'
```

```sh
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/cold-index-verify
cargo nextest run --no-tests=fail -p tick_loop -E 'test(/::cold_index_build_leaves_the_graph_write_lock_free$/) or test(/::cold_index_runner_swaps_before_clearing$/) or test(/::cold_index_runner_records_a_failure$/)'
```
