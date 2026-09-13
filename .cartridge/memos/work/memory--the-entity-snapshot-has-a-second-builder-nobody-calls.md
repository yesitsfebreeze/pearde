---

kind: work
level: 10
status: done
description: "`build_entity_disk_index` is a public epoch-unaware builder for one of the three DiskANN snapshots, writing to whatever directory it is handed — the live path is a private epoch-aware one that owns the layout, and nothing calls the public one"
read_when: "picking up work, or touching the DiskANN snapshots"
---

# the-entity-snapshot-has-a-second-builder-nobody-calls

## Do

`GraphGnn::build_entity_disk_index` (`src/graph/src/graph.rs:516-522`) calls
`diskann::build_and_save(dir, &self.collect_entity_items(), Params::default())`.
Nothing calls it — no production site, no test.

The live builder is `build_disk_snapshot` (`:526-545`), private, with five call
sites covering all three indexes (`:122`, `:575`, `:604`, `:614`, `:624`). It
differs from the dead one in both of its arguments:

- **The epoch.** It calls `build_and_save_with_epoch` and passes
  `store.read_epoch()`, which skips the rebuild when the snapshot already
  matches. That stamp is what `config.rs` credits with making an unchanged
  store load "in ~ms instead of rebuilding three HNSW indexes"
  ([[every-cli-invocation-pays-a-minute]]). `build_entity_disk_index` reaches
  `build_and_save`, whose whole difference is passing `None` for that epoch, so
  it rebuilds unconditionally.
- **The directory.** It composes `data_dir/diskann/<subdir>` itself, so the
  three snapshots have one layout. `build_entity_disk_index` writes wherever the
  caller points it, with no `entity` subdirectory implied.

Delete it. `build_and_save` stays: it is the base `build_and_save_with_epoch`
delegates to, and two root tests call it directly
(`tests/spill_memory.rs:137`, and `spill_transparency.rs` names it).

Second of the eight uncalled production functions the corrected sweep found
([[@prd/work/memory--the-walk-inlines-the-function-that-scores-a-neighbour.md]] carries the list),
and the same shape as [[binary-quantization-is-unreachable-and-in-memory-only]]
— a public path that is reachable in principle, differs from the live one in
exactly the property that matters, and has no caller to notice.

**Done 2026-09-06 — and "no test" was wrong.** The part says "Nothing calls it —
no production site, no test." `graph_test.rs:249` called it. That is the fourth
"no caller" claim tonight to be false on arrival, after `prune_missing` twice and
`score_neighbor` ([[a-sweep-needs-a-negative-control]] collects the mechanism).
I found it by running `rg` before deleting rather than by reading the part.

It changed the fix. The caller is
`disk_index_snapshot_mirrors_in_ram_membership_and_ranking`, and that test is
**not about the builder** — it asserts the snapshot mirrors RAM in membership
(superseded excluded), in ranking (`e40` first from both), and in overlap.
`build_entity_disk_index` was only its convenient way to get a snapshot out of a
`GraphGnn`. Deleting the method as the `Do` says, with nothing else, would have
taken that test with it.

So the method is gone and the test now calls the primitives it wrapped —
`diskann::build_and_save(dir, &g.collect_entity_items(), Params::default())` —
which it can, being inside the crate. The dead public path goes, the coverage
stays, and the test is now written in terms of what the live path actually uses.

## Check

`build_entity_disk_index` is gone, `build_and_save` keeps its callers — the two
root tests plus the crate tests and, now, the one this deletion rehomed — and
`just check` and `just test` are green at 1,255 passed.
