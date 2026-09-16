---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "analyzing"
origin: requested
priority: 60
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
needs: ["@memory/diskann-builds-keep-every-node-reachable-from-the-entry-point"]
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
claim: "coordinator-c4-14 2026-09-16T09:16:53.055Z"
---

# The cold tier has a Vamana index that follows every cold write

The cold tier is a vector side table with no index (`Store::cold_visit_vectors`,
`src/store/core/src/cold.rs:224`). Build a DiskANN snapshot of it under
`<data_dir>/diskann/cold`, and make every cold write since that build visible without a
rescan, across processes.

Every cold writer (`import_snapshot`, `cold_spill`, `cold_put_all`, and `cold_move`, which
serves `cold_rekey` and `cold_relocate`) bumps a persisted `cold_seq` in its own transaction.
It records `id -> (put|delete, seq)` in a `cold_since` table. A build captures S in the same
read transaction as its vector scan and stamps the snapshot with S. After reading the stamp
back, it clears only entries with `seq <= S`, so writes during a build survive.

The build runs in a tick task, `ColdIndexBuild`. The task clones the store and data dir under
a read guard and builds with no graph lock held. It takes the write lock only to swap
`GraphGnn.cold_idx`, the handle the sibling query reads. A flock on `diskann/cold.lock` keeps a
daemon and a CLI from sharing `cold.staging`.

A rebuild is triggered when:
- there is no snapshot;
- the since-build set is at least the snapshot's size;
- the `EmbedStamp` changed;
- the width changed.

The hot `outgrown`/`consolidate_disk_index` path still builds under the write lock
(`graph.rs:633`, `tick_tasks.rs:484`); this PRD does not change it. The contract, steps and
scoped-out points are in specs/spec01.md.

The prerequisite `@memory/diskann-builds-keep-every-node-reachable-from-the-entry-point` has
landed (5097a83). No model-stamp prerequisite: the per-store `EmbedStamp` and the width check
gate mixed models.

## Acceptance

- [ ] After each of `cold_spill`, `cold_put_all`, `cold_rekey`, `cold_relocate` and `import_snapshot`, a reopened store (first handle dropped) reads a since-build set naming exactly the ids put and deleted.
- [ ] A write that lands during a build (after the captured sequence) keeps its since-build entry after the clear.
- [ ] A build that fails before stamping leaves the previous snapshot and the since-build set intact (the test injects a failing build dir), and a second builder skips while `cold.lock` is held.
- [ ] The graph write lock can be taken while a cold build is in progress (tick-task test), and the builder takes no `GraphGnn`.
- [ ] An ignored release test records build time at 100,000 rows in the implementer's report.

Verify blocks live in specs/spec01.md; each names its new tests and fails at 5097a83.

Split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 (analyst-2). It inherits the parent's used review rounds: none.
