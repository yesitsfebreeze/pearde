---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: low
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - src/retrieval/piece/src/retrieval_query.rs
  - .cartridge/tests/unit/src/retrieval/piece/src/tests/retrieval_query_test.rs
  - .cartridge/help.md
---

# A point-in-time query names what it costs

An `as_of` query does two whole reads: every hot entity is cosined
(`retrieval_query.rs:290`, `g.memories.values().flat_map(entities)`), and the cold pass
admits superseded rows, which an index of current rows does not serve. Keep both exact
and say so: a comment at the walk and a `.cartridge/help.md` entry naming `as_of` and
`valid_at` as point-in-time maintenance queries, O(hot entities + cold rows), with the
measured cost. No history index.

## Acceptance

- [ ] An ignored measurement in `cold_scan_cost` prints `as_of` query latency at 10,000 hot entities with 10,000 and 100,000 cold rows; the numbers appear in the Result and in `.cartridge/help.md`.
- [ ] `.cartridge/help.md` names `as_of` and `valid_at` as exact, linear point-in-time queries.
- [ ] A unit test shows an `as_of` query still returns a superseded cold row valid at that time.

## Verify

```sh
cargo nextest run -p retrieval-piece as_of
grep -q "as_of" .cartridge/help.md
```

Split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 (analyst-2). It inherits the parent's used review rounds: none.
