---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 60
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
needs:
  - "@memory/the-cold-tier-scales-past-a-linear-scan/the-cold-tier-has-a-vamana-index-that-follows-every-cold-write"
footprint:
  - src/retrieval/piece/src/retrieval_query.rs
  - .cartridge/tests/unit/src/retrieval/piece/src/tests/retrieval_query_test.rs
  - .cartridge/help.md
---

# A query reads the cold tier through its index

Replace pass one of `cold_candidates` (`retrieval_query.rs:751`), the whole side-table
cosine, with an index search for `cap * COLD_OVERFETCH` ids unioned with the since-build
ids scored off their live vectors, then the unchanged pass two (gates, boosts,
`cmp_rank` pool). Every candidate is rescored from the vector `cold_get` returns, so a
rewritten row never carries its indexed score. When candidates run out before
`admitted` reaches the budget (a heavily filtered query), or no fresh index exists, fall
back to today's exact scan, so
`memory_contract::cold_filters_precede_the_delivery_cut_and_expired_rows_stay_stored`
still holds. `as_of`/`valid_at` queries keep the exact scan (sibling child 3). The
`scanned` count reports rows considered. Delete the uncalled `Store::cold_search`.

## Acceptance

- [ ] A unit test over a >= 2,000-row fixture asserts the indexed path's delivered top-10 overlaps the exact scan's top-10 at >= the threshold stated beside `COLD_OVERFETCH` and in `.cartridge/help.md`.
- [ ] A filtered query whose index candidates are all gated out still delivers the eligible row; the memory_contract cold-filter test passes.
- [ ] `just scale cold_scan_cost` prints repeat-query latency at 10,000 and 100,000 cold rows; the Result records it with 100k/10k < 5 (today about 9: 13 ms and 119 ms).
- [ ] `.cartridge/help.md` says the cold tier is queried through an approximate index, names its recall threshold and when the exact scan runs instead.

## Verify

```sh
cargo nextest run -p retrieval-piece cold_
grep -qi "approximate" .cartridge/help.md
```

Split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 (analyst-2). It inherits the parent's used review rounds: none.
