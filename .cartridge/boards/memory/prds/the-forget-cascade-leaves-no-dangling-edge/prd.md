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

# a prefix forget of 11,222 thoughts took 22,503 edges with it and left the store with 910 dangling reason edges where it had 110 — the cascade removes the entity and not every edge that points at it

## Do

Measured 2026-09-06 by the session that ran the cleanup:
`memory forget --source "file://Users/feb/dev/memory/memos/.claude/" --prefix
--force` removed 11,222 thoughts and 22,503 edges in 3.7 s, taking the store
from 14,744 entities to 3,557. `memory doctor` reported **110** dangling reason
edges before the removal and **910** after. So the cascade misses edges whose
other endpoint is gone: 800 new dangling edges out of 22,503 removed, about one
in twenty-eight.

A dangling edge is not inert. The walk follows reason edges to score
neighbours (`recall-pipeline`), and an edge to a missing entity is weight
spent on nothing — the same cost `a-floor-cuts-the-linked-neighbour` measures
from the other side. `doctor` finds them, which means the fix is a caller, not
a detector.

Remove the edge with the entity in the same commit, whichever endpoint is
being deleted, and have the bulk path assert the invariant once at the end
rather than per row. The cleanup that exposed this is a real corpus and the
first case to test against.

**Done 2026-09-06.** `remove_entity` (`src/graph/src/reason.rs:169`) collects
`reasons_touching` across every memory rather than the one that owned the entity,
then removes each edge from the memory that holds it and deindexes it —
`an-edge-lives-in-one-memory-so-removal-scans-them-all` is why there is nothing
cheaper to consult. The second half was in the reporting: `forget_entity`
(`src/graph/src/graph_ops.rs:63`) measured its edge delta as the owning memory's
`reasons.len()` before and after, so a cross-memory cascade would have been
invisible in the count even once it worked; it sums across every memory now,
which means the 22,503 edges the cleanup reported were themselves an
undercount. Held by
`forget_by_source_takes_the_edge_that_points_in_from_another_memory`
(`src/commands/src/tests/commands_graph_ops_test.rs`): two memories, the edge in
the surviving one, the target removed by source prefix, asserting the count and
that the survivor keeps neither the reason nor its adjacency entry.

## Acceptance
A fixture where a removed entity is the target of an edge from an entity that
stays leaves no edge behind — the unit test above, rather than a `memory doctor`
run: the live store's dangling count is moving under
`a-refused-flush-undoes-another-writers-removals` and cannot be held still
long enough to be a before-and-after.
