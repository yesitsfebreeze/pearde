---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/memory.ctg"
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
---

# Repeated activity becomes weighted graph knowledge

Activity becomes ordinary memory entities with semantic reason edges and an explicit occurrence annotation. Repeated compatible observations fold into one entity and increment occurrence count and heat. Opposite outcomes or incompatible reasons stay separate even when their content vectors match.

## Acceptance

- [ ] Distinct repetitions increment count; the same delivery retried does not.
- [ ] Matching content and reason vectors consolidate; differing outcomes and incompatible reasons remain distinct.
- [ ] Counts, first/last timestamps, bounded representative examples and reasons survive persistence and reload without changing the positional Entity layout.
- [ ] Candidate search is bounded, exact repeats avoid embedding, and observation reads do not mutate recurrence.

## Proof and recovery

Start at src/graph/src/accept.rs and src/base/src/base_types.rs. Add a graph experience module and an additive occurrence reason variant with metadata in its text. Keep semantic reasons separately embedded. Use the existing graph indexes and heat decay. Do not repurpose Bayesian confidence or access count as frequency. Test with deterministic embeddings and a disposable LMDB store using cargo test -p graph experience. Benchmark repeat bursts in release mode and report elapsed time, entity/reason counts and embedding calls. No private store or live model is needed for correctness.

## Dependencies and review

This is the graph contract prerequisite for the intake leaf. Record independent review in review.md. Exact occurrence deduplication belongs to the atomic intake receipt transaction in the dependent leaf; graph tests model accepted distinct occurrences. Runtime routing, installed-cartridge catalog and ordinary document deduplication are excluded.

## Implementation checkpoint

Implemented in the current memory.ctg working tree. [Shared verification evidence](../implementation.md) records integration, tests and remaining limits. This checkpoint does not replace formal PRD collection.
