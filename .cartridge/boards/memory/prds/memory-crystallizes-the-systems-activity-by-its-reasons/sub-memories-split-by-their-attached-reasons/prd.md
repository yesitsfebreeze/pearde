---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/memory.ctg"
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
---

# Sub memories split by their attached reasons

Memory partitions accumulated experience by semantic reasons. Clustering, cohesion, core detection and naming use one consistent reason-space projection, while entities retain their original content embeddings for recall. The existing recursive split and ownership-safe move machinery remains responsible for graph structure.

## Acceptance

- [ ] Entities with identical content vectors but distinct reason vectors form separate clusters.
- [ ] Equivalent reasons group differently worded entities; missing semantic reasons fall back to content vectors.
- [ ] Entity vectors stay unchanged and all moved reason endpoints and ownership indexes remain valid.
- [ ] Unnamed memories cannot repeatedly spawn children, sampling stays bounded and stable, and a child can split after receiving a name and sufficiently distinct reason groups.

## Proof and recovery

Start at src/tick/loop/src/tick_cluster.rs, tick.rs and tick_tasks.rs. Add a projection helper that selects semantic reason vectors and excludes occurrence metadata and administrative relations. Pass projected vectors consistently through grouping and naming while moving original entities. Preserve existing minimum cluster sizes, deterministic sampling and recursion safety. Run cargo test -p tick_loop with new deterministic reason-space fixtures, then the memory audit and isolation gates. No external model is required for clustering tests; model-quality claims require separate evidence.

## Dependencies and review

The additive occurrence annotation kind is the shared contract with the graph leaf. Both leaves touch vocabulary only through that declared kind. Record independent review in review.md. Changing all ordinary query ranking or replacing the GNN is excluded.

## Implementation checkpoint

Implemented in the current memory.ctg working tree. [Shared verification evidence](../implementation.md) records integration, tests and remaining limits. This checkpoint does not replace formal PRD collection.
