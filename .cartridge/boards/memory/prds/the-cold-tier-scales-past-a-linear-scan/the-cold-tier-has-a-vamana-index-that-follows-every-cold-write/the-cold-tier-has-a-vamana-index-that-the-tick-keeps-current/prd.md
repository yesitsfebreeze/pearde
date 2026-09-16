---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 60
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
needs: ["@memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write/every-cold-write-is-recorded-in-a-sequenced-since-build-set"]
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

# The cold tier has a Vamana index that the tick keeps current

## Outcome

Build `<data_dir>/diskann/cold` from child A's `cold_snapshot_vectors`, stamped with its S.
Only vectors of the store's `EmbedStamp.dim` go in; wrong-width and empty rows are skipped
and counted. `DiskIndex::open` validates the result before it is used.

The `ColdIndexBuild` tick task runs with no graph lock held. Under `cold.lock` it builds,
takes `g.write()` only to swap `GraphGnn.cold_idx`, and only then clears the set. So no
reader's handle loses its since-build rows.

A handle is usable only when `S >= cold_since_floor()` and the `embed` file matches. When
another process's build raised the floor, the task reopens from disk instead of rebuilding.
`persist.rs::graph_from_store` opens the handle at load and reload.

The pulse enqueues through `claim_slot` on `cold_index_at_secs`. The runner rechecks the
trigger before building. On `Err` it calls `record_task_failure` and waits for the next slot.

A build occupies the single tick drain, so other tasks wait for it. If the 100k build
exceeds 10 minutes, a follow-up moves it to `spawn_blocking`. The hot
`consolidate_disk_index` path (`graph.rs:633`, `tick_tasks.rs:484`) is unchanged.

## Acceptance

- [ ] A graph holding a handle from an earlier build reads it as unusable once a newer build has cleared; the runner swaps before it clears (hook observation).
- [ ] A wrong-width and an empty row are skipped, and the snapshot opens; a failed build keeps the old snapshot and set; a second builder skips while `cold.lock` is held.
- [ ] The trigger rules hold (no snapshot, set ≥ snapshot, embed or width change, floor > S), a second enqueue waits for its cadence slot, and a failure is recorded.
- [ ] `g.try_write_for(5 s)` succeeds while a build is blocked in its hook.
- [ ] An ignored release test's 100k build time is recorded in the implementer's report.

## Proof and recovery

The tests are named in specs/spec01.md, and each block fails at 5097a83. Deleting
`diskann/cold` forces a rebuild. This leaf inherits 2 used review rounds from
`the-cold-tier-has-a-vamana-index-that-follows-every-cold-write`.
