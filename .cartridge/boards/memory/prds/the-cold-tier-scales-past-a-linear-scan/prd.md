---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge/memory.ctg"
---

# The cold tier scales past a linear scan

## Outcome

A query does not visit every cold row to consider it. Today `cold_candidates`
(`src/retrieval/piece/src/retrieval_query.rs:667`) walks the whole cold store per query,
computing a cosine on each row and maintaining a bounded insertion pool — O(cold_rows) no
matter the query — and the `as_of` historical walk flattens every memory's entities the
same way. At the current corpus this is nothing; at a corpus an OS-grade memory holds it
is the first wall the architecture hits. The cold tier either gains an ANN index or the
store names its scale assumption explicitly. DiskANN already exists in the tree
(`src/graph/src/diskann.rs`) and is not on this path.

## Acceptance

- [ ] The cold tier participates in queries through an ANN index (DiskANN or an equivalent), or the store documents and enforces a bounded working-set size — one of the two, stated in code and `.cartridge/help.md`, not silently assumed.
- [ ] A query against a corpus with at least 100k cold rows returns its top-k in time that scales with the index, not the corpus: a benchmark (new `just` recipe or existing bench target) shows cold-path latency at 10k and 100k cold rows, and the ratio is not linear in corpus size.
- [ ] Recall does not silently regress: the ANN cold path's top-10 overlaps the linear scan's top-10 on a fixture corpus above an explicit, documented threshold (an approximate index names its approximation).
- [ ] The `as_of` historical walk is bounded or indexed the same way, or explicitly documented as a point-in-time maintenance path with its cost named.
- [ ] From `/Users/feb/dev/cartridge/memory.ctg`: `just check` and `just test` exit 0.

## Notes for the analyst

The cold store's visitor interface (`store.cold_visit`) is the seam; an index answer keeps
the visitor for full scans (maintenance, migration) and adds an indexed search path. The
DiskANN build path already shards with epochs (`build_and_save_with_epoch`,
`src/graph/src/graph.rs:556`); check whether a cold-tier index can reuse that
infrastructure before inventing a second one. The existing pool-cap logic (insertion by
`cmp_rank`, truncate to `delivery_cap`) remains the tie-break for index results. Consider
whether the model-stamp PRD (`a-vector-carries-the-model-that-made-it`) lands first: an
index over mixed-model vectors is built on sand, so this PRD may need it as a `needs`
entry.