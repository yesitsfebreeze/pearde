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

# the entity-rescue block inside evict_empty_children is unreachable — the branch it sits in is only entered when the child holds no entities

## Do

`evict_empty_children` (`src/tick_loop/src/tick.rs:408-429`) reads
`(named, has_thoughts, exists)` off the child, where
`has_thoughts = !c.entities.is_empty()`, and enters its eviction branch on
`!exists || (!named && !has_thoughts)`. Inside that branch it guards
`if exists` and moves every entity of the child into the parent before calling
`graph.deregister(child_id)`.

That move can never carry a row. Reaching it with `exists == true` requires
`!has_thoughts`, which is exactly `c.entities.is_empty()`; nothing mutates the
child between the read and the move. So `stray_ids` is always empty and the
loop body never executes — dead code by the tree's own law, which keeps no code
without a caller.

The rescue is also wrong where it would matter, which is why deleting it is the
whole change and not half of one. It writes into `parent.entities` directly and
never calls `GraphGnn::index_entity` (`src/graph/src/graph.rs:759`), so a moved
entity would keep `entity_memory[tid]` pointing at the child — a memory
`deregister` (`graph.rs:817`) then removes from `memories` and deletes from the
store. Every id-to-memory resolution goes through `memory_of_entity`
(`graph.rs:780`), so the row would survive in the ANN index and resolve to
nothing, which is the shape [[@prd/note/memory--open-work.md]] item 4 already names for
`deregister`. [[@prd/note/memory--open-work.md]] item 14 names that staleness for a reparented stray
from the other direction, without knowing the rescue cannot run
([[@prd/insight/memory--the-record-plans-work-in-two-places.md]]). Delete the block; keep the
`is_unloaded` guard above it, which does real work.

**Done 2026-09-06.** The unreachability was re-derived before the cut rather
than taken from this part: reaching the move with `exists == true` requires the
second disjunct, `!named && !has_thoughts`, and `has_thoughts` is
`!c.entities.is_empty()` read from the same `graph.memories.get` — so
`stray_ids` was collected from a map already known to be empty, with nothing
mutating the child in between. The whole `if exists { … }` block is gone; the
`is_unloaded` guard above it and `graph.deregister(child_id)` below it stay.

No test came with it. The branch was dead, so nothing observable changed, and a
test asserting a behaviour that never occurred would be a second thing to
maintain and no evidence at all.

## Acceptance
`rg -n 'stray_ids' src/` returns nothing, `just check` and `just test` are
green, and `evict_empty_children`'s eviction branch reads
`graph.deregister(child_id)` with no entity move before it. All three hold: `rg` answers
nothing, `check` is green, and the suite reads 1,237 passed in 27.7 s.

The run before it read 640 passed with three `memory::e2e retention::…` failures
at 144 s each under four concurrent sessions — the same three that failed the
same way before any change in this session, passing 24 of 24 in 6 s each in
isolation. Recorded because it is the second time tonight the same three tests
answered load rather than correctness, which is what
[[e2e-bounds-are-exec-latency]] describes and what makes a single red run on
this box uninformative on its own.
