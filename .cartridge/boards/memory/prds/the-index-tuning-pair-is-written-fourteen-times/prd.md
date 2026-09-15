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

# HNSW's M and ef_construction are the literals `16, 200` at fourteen call sites, thirteen of them in one file, so tuning the index means finding all fourteen and a partial edit leaves indexes built to two different shapes

## Do

`VectorBackend::resident(16, 200, …)` appears thirteen times in
`src/graph/src/graph.rs` — in `new`, in `disk_or_resident`, in the reload
path, in the three per-index rebuild arms, and in the second constructor — and
`HnswIndex::with_mode(16, 200, …)` once more in
`src/graph/src/vector_backend.rs` for the disk backend's delta index. The two
numbers are HNSW's graph degree and its construction beam width, and nothing
names them.

The hazard is not the repetition, it is that the sites are reachable
independently. The three rebuild arms each construct one index, so an edit that
misses one leaves a store whose entity index was built at one shape and whose
reason index was built at another, with no error and no gate. The cold tier's
delta index in the other file is the one most easily missed.

Give them names in `src/base/src/base_constants.rs` beside `DEDUP_EF`, which is
already the home for exactly this kind of index-tuning number, and use them at
all fourteen sites. Test literals stay as they are: `hnsw_test.rs` deliberately
builds at `8, 64` and `24, 200` to exercise the structure, and those numbers are
the test's subject rather than the production shape.

Done 2026-09-06: `HNSW_M` and `HNSW_EF_CONSTRUCTION` are declared once in
`base_constants.rs` and all fourteen sites read them, so the count is zero and
tuning the index is one edit.

## Acceptance
`rg -n 'resident\(16, 200|with_mode\(16, 200' src` returns nothing, the two
constants are declared once in `base_constants.rs`, and `just check` and
`cargo test -p graph` are green.

**Done in `662cd6a0`, 2026-09-06.** `rg '16, 200' src` answers nothing. The
pair is `HNSW_M` and `HNSW_EF_CONSTRUCTION` in `base_constants`, imported
where the indexes are built — `graph.rs:276-278` is the three resident
backends taking them by name — so the three separately reachable rebuild arms
can no longer drift into two index shapes in one store.

