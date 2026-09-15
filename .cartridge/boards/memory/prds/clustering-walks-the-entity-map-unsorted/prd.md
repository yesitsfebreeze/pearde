---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# both callers of `vector_cluster` hand it `memory.entities.values().collect()` unsorted and it truncates to a sample, so which thoughts cluster, which seeds a cluster and which name a graviton gets all vary per process on identical data

## Do

`vector_cluster` (`src/tick_loop/src/tick_cluster.rs:17-28`) filters to
vectored thoughts, **truncates** to `max_sample`, then seeds clusters greedily
in the order it was given. Both callers give it a raw `HashMap` walk:

```
tick_tasks.rs:251   let entities: Vec<_> = memory.entities.values().collect();
tick.rs:309         let entities: Vec<_> = memory.entities.values().collect();
```

`HashMap` iteration order is randomised per process, so on one store and one
build:

- the truncation keeps a **different subset** each run — which thoughts cluster
  at all is decided by hash order;
- the seed of each cluster is whichever survivor comes first, so the
  partition differs;
- `graviton_prompt` (`:137-152`) picks the ten members nearest the centroid,
  and even without ties the centroid itself is a float sum whose value depends
  on summation order.

The output is a name. `do_name` embeds the model's answer as the memory's
`graviton_vec` ([[a-junk-name-becomes-a-junk-attractor]]), so a per-process
partition becomes a per-process attractor and every later arrival is routed
against it.

Sort before truncating, exactly as the GNN snapshot already does. That code
solves this problem two files away and names the reason
(`tick_gnn_propagate.rs:70-76`): "A HashMap walk put `ids`, the feature-matrix
rows, `dim`'s reference entity and every `pos_edges` index in per-process hash
order, which no seed can undo — item 29's defect in a second place (open-work
item 2)." This is the third place. `build_gnn_snapshot` sorts
`memory.entities.keys()`; `vector_cluster` should sort by `id` before the
`truncate`, which fixes both callers at once.

Determinism downstream of the sample is already fine: rayan's `collect`
preserves order, and the `sort_by` at `:147` is stable over a then-fixed input.
The sample is the only unordered step.

**Done 2026-09-06.** `vector_cluster` sorts by id before the truncate, which
fixes both callers at once and leaves everything downstream alone — the part is
right that the sample is the only unordered step, and sorting later would have
been a second change with nothing to fix.

Held by `the_sample_is_the_sorted_first_ids_whatever_order_they_arrive_in`: six
identical-vector entities, `max_sample` 3, offered forward and reversed. It
asserts the sample is `e0,e1,e2` — the first three **by id**, not the first
three offered — and that both orders give the same answer. The first assertion
is the load-bearing one: same-answer-both-ways would also pass if the code took
the last three, or the middle three, as long as it did so consistently.

Third instance of one defect. `build_gnn_snapshot` sorts for this reason two
files away and its comment says so; the distill prompt's kind list was the
fourth, fixed the same hour
([the-distill-prompt-lists-registered-kinds-in-hash-order](../the-distill-prompt-lists-registered-kinds-in-hash-order/prd.md)). All four are the
same shape: a `HashMap` walk feeding something whose output is kept — a
snapshot, a prompt, a cluster, a name.

## Acceptance
Two runs of the naming pass over one unchanged store select the same cluster
and build the same `graviton_prompt`. A unit test over a fixture memory with more
entities than `max_sample` asserts the sampled ids are the sorted-first ones.
`just test` green at 1,257 passed.

The unit half is held. The live half — two naming passes over one unchanged
store — was **not** run: it needs a store with an unnamed memory large enough to
cluster and two daemon passes over it, and this session has not had one
([[a-promoted-root-does-not-persist]] met the same wall from the other side).
The sort is what the store-level claim rests on, and it is proved at the unit
level only.
