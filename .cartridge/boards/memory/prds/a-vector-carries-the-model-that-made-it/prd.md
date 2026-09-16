---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/memory.ctg"
---

# A vector carries the model that made it

## Outcome

A store whose vectors do not match the configured embedding model refuses to
pretend otherwise. A store-level stamp already exists
(`store_core::EmbedStamp`, `src/store/core/src/lib.rs:312`; written/checked in
`src/graph/src/persist.rs:73-95`, mismatch flag consumed by health
`src/health/src/lib.rs:199` and the RPC surface `src/transport/src/memory_rpc.rs:181`),
and a swap logs "recall stays near zero until `memory reembed`". But the guard is
fail-open and invisible in exactly the case it exists for, observed live
2026-09-16 on `memory.ctg/.memory`: health reports the stamp clean
(`qwen3-embedding:0.6b (dim 1024)`), `memory check` reports only LMDB bloat, while
363 cold rows are scanned by every query and **zero** enter the candidate pool
(`cold_candidates` skips on `vector.len() != qvec.len()`,
`src/retrieval/piece/src/retrieval_query.rs:253`), so every query returns empty
with no diagnostic. The dimension guard drops the rows silently; the stamp never
names them.

## Acceptance

- [ ] The dimension skip in `cold_candidates` (and the `as_of` walk's equivalent) is no longer silent: rows excluded for a dimension or model mismatch are counted, and the count surfaces in `memory check` (and `explain`, where `cold_rows_scanned` already reports) so a store whose rows are all invisible is diagnosed, not just empty-looking.
- [ ] A stamp mismatch between stored and configured model is a `check` finding, not only a throttled log line and a health flag: `memory check` on a mismatched or unreadable stamp reports it with the stored and current model names.
- [ ] Rows already persisted under a different model (the pre-existing-corpus case) are visible as a count in `check`'s manifest, so `memory reembed` has a number to converge to and `repair` can act on the manifest entry.
- [ ] From `/Users/feb/dev/cartridge/memory.ctg`: `just check` and `just test` exit 0, including a test that persists rows under one dimension, queries under another, and asserts the exclusion is counted and named rather than silent.

## Notes for the analyst

The `EmbedStamp` mechanism is the right foundation; do not build a second one. The
gaps are observability and refusal granularity, not absence: (1) the store-level
stamp cannot see per-row provenance, so mixed-dimension corpora (rows written by
an older build or another model before the stamp existed, or after a
`migrate`-skipping upgrade) have no owner; (2) the only per-row guard is the
length check, which drops silently. The observed fixture is
`memory.ctg/.memory` itself: 363 cold rows, 0 hot entities, every query empty,
`check` silent. Probe it with `memory query --explain` — `cold_rows_scanned: 363`
with `candidates: {}` is the signature. Decide whether per-row model identity is
worth a persisted-layout change (`Entity` is bincode-positional,
`src/base/src/base_types.rs:328`) or whether counted exclusion plus a store-level
stamp that refuses to adopt over unreadable rows is sufficient.