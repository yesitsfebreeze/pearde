---
kind: work
level: 10
status: done
description: the memories-map row is the only root copy production needs, so `GraphGnn.root` and `merged_root` are deletable and a write to the root stops being discarded at flush
read_when: "fixing the root write that never comes back from disk, or picking up the promote residue"
---

# the-root-memory-needs-one-authority

## Do

[[the-root-memory-exists-twice]] diagnoses the defect and stops there: `GraphGnn`
carries `pub root: Memory` (`src/graph/src/graph.rs:179`) and a clone of it in the
`memories` map (`:293`), and `merged_root` (`src/graph/src/persist.rs:105-124`)
makes each copy authoritative for a different set of fields, so a write to the
wrong copy is dropped at the next flush with no error and no log. The reason
nobody has fixed it is that neither copy looks removable. One is. Measured
against HEAD, the only root field production reads outside `merged_root` itself
is `id` — plus the claim-kind registry. Nothing anywhere reads
`g.root.focus_text`, `g.root.focus_vec`, `g.root.inner_radius` or
`g.root.outer_radius`: four of the six content overrides exist only to stamp
the map row from a field no other code writes, which is destruction with no
reader on the other side.

So the map row becomes the sole authority and the field goes.

- Delete `pub root: Memory` and `merged_root`, its three flush call sites
  (`persist.rs:132`, `:145`, `:173`), the root special case in
  `src/tick_loop/src/tick_tasks.rs:517-524`, and the same overlay in
  `src/commands/src/test_helpers.rs:45`. `GraphGnn::blank` stops storing a root
  and `from_saved_with_mode` stops taking one — `load_dir` already keys the map
  on it (`persist.rs:39`, `:56`).
- The root id is the literal `"root"` at every site (`Memory::new_root` is
  `Memory::new("root", "")`, `base_types.rs:596-597`), so each `g.root.id` read
  becomes one accessor on `GraphGnn`. Do not name a field `root_id`: `Memory`
  already has one and it holds the replica id, which is what makes
  `merged.root_id = g.root.root_id` at `persist.rs:113` read like identity when
  it is not.
- Move the claim-kind registry — the only root field besides `id` production
  touches — onto `root_memory()`/`root_memory_mut()` (`graph.rs:726-731`). Sixteen
  sites: `src/rpc/src/server.rs:253,1544,1548,2303,2310,2323,2331,2458,2629`,
  `src/commands/src/commands_health.rs:40`,
  `src/commands/src/commands_claim_kind.rs:50,78`,
  `src/commands/src/commands_insights.rs:181`,
  `src/commands/src/commands_intake_cmd.rs:128`,
  `src/commands/src/commands_serve.rs:684`,
  `src/ingest/src/ingest_worker.rs:121`.
- Delete the two claim-kind union loops in `absorb_graph`
  (`src/graph/src/merge.rs`). They are the whole reason `merged_root`
  replaces rather than unions — its comment at `persist.rs:118-120` records a
  `claim-kind rm` on `g.root` being resurrected from the stale map base — and
  absorb's own doc comment (`:208-211`) already promises that memory-shell fields
  stay local. Deleting them moves no persisted byte today: the retried flush
  writes `g.root`'s kinds, so a remote writer's claim-kind add is already
  discarded on this path ([[a-refused-flush-undoes-another-writers-removals]]
  is the general form). Without them the map row keeps a removal across a
  refused flush, which is what the replace was buying.
- Three comments exist only to warn about the split and go with it:
  `tick_tasks.rs:517-518`, `src/graph/src/accept.rs:1399`,
  `src/health/src/lib.rs:334-335`. So does the test that pins it,
  `merged_root_overlays_authoritative_fields_over_stale_map_entry`
  (`src/graph/src/tests/persist_test.rs:11-29`).

`promote_unnamed` (`src/graph/src/accept.rs:1350-1371`) then persists as
written: it sets `focus_text`, `focus_vec` and `mass` through `g.get_mut`, and
all three reach the only row there is. That closes the residue
[[@prd/work/memory--unnamed-promote-routes-to-the-daemon.md]] left open and the observed instance
[[a-promoted-root-does-not-persist]] measures.

## Check

A test beside the one it replaces, in `src/graph/src/tests/persist_test.rs`:
open a `GraphGnn` on a tempdir, and through `g.get_mut("root")` alone write all
six fields `merged_root` overrides — `focus_text`, `focus_vec`, `inner_radius`,
`outer_radius`, one `claim_kinds` entry, one `claim_kind_parents` entry — plus
`mass`, which the map already owns. Flush, `load_dir` the same directory, and
assert all seven come back. Today it is red on exactly the six and green on
`mass`, which is the defect stated as an assertion; after the change it is
green on all seven.

The write-to-`g.root` half of the split needs no assertion of its own, because
the change removes the expression: `g.root.focus_text = …` stops compiling.
Pin that, since a passing test cannot:

```
! git grep -n 'fn merged_root' -- src/ && ! git grep -n 'pub root: Memory' -- src/
```

Its exit code is the assertion — there is no second copy left to write to.

**Done 2026-09-08.** `GraphGnn.root` and `merged_root` are gone; the memories-map
row is the only root, and `save_graph_into`, `flush_guarded` and
`snapshot_for_flush` write `g.map()` with no overlay. The per-memory root special
case on the tick loop and the `test_helpers` overlay went with them, and
`GraphGnn::blank`/`from_saved_with_mode` no longer take a root — `load_dir`
already keyed the map on it.

The claim-kind registry reads through `root_memory`, and the four sites that
wanted the names alone share one `GraphGnn::claim_kind_names`. Every *write* to
it — `add_claim_kind`, `rm_claim_kind`, the `kind: type` declaration in
`ingest_worker` — goes through `get_mut` rather than `root_memory_mut`, so the
mutation epoch moves; `root_memory_mut` is still the no-epoch map access the test
setups want. `absorb_graph`'s two claim-kind union loops are deleted, and with
them the reason the merge replaced rather than unioned.

The `Check` test is green on all seven fields, and the grep pair exits 0. Two
strays outside this change: `cargo test -p commands --lib` and `-p rpc --lib`
each fail a pair of tests under parallel load on a process-global exit flag and
pass alone, and `tests/cited_paths.rs` reports `src/rpc/src/plan.rs:2` citing
a gitignored nested clone that exists in the trunk and in no worktree, so that
anchor is red from any lane.
