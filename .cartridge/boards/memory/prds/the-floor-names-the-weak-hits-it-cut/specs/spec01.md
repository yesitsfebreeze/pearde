---
footprint:
- "src/base/src/base_retrieval.rs"
- "src/retrieval/piece/src/retrieval_query.rs"
- "src/rpc/src/server.rs"
- "src/commands/src/commands_query.rs"
- ".cartridge/tests/unit/src/retrieval/piece/src/tests/retrieval_query_test.rs"
---

# Spec: carry the floor's cut band and the empty verdict to both surfaces

## Files and steps

1. `src/base/src/base_retrieval.rs` — add `weak_band: Vec<ScoredEntity>` and
   `empty_kind: Option<EmptyKind>` to `QueryResult`, and declare `EmptyKind` with
   `CandidatesEmpty { cold_rows_scanned: u64 }` and `PoolFiltered`. This struct is the
   retrieval boundary, so the fields live here and not in the hot piece.
2. `src/retrieval/piece/src/retrieval_query.rs` — extend `Retrieved` with `weak_band`,
   `cold_rows_scanned` and `pool_built`. Record `pool_built` once, after the cold-tier and
   `as_of` legs have merged into `results` and before any policy cut, so an emptied pool is
   distinguishable from one that never formed. At the floor, collect the cut ids into their
   own set for the existing chain-drop, and carry at most `WEAK_BAND_MAX` cut rows out as the
   band. Compute `empty_kind` in both `query_profiled` and `query_locked`.
3. `src/rpc/src/server.rs` — render `weak_band` and `empty` on the `tool_query` response,
   outside the `explain` gate. Reuse the moved `cold_ids` binding for the band's rendering.
4. `src/commands/src/commands_query.rs` — mirror both on the local path, and print a
   `--- Weak matches ---` section plus a reason on the empty line. The weak rows must NOT use
   the ranked-hit line shape `<rank>. [<score>] <id>  <text>`, because
   `.cartridge/tests/integration/e2e/ranking.rs::hits` parses that shape and every reader of
   ranked hits would otherwise count weak rows as delivered answers.
5. Tests — assert the cut row reaches `weak_band` in the existing floor test, and add
   `an_empty_result_names_which_empty_it_is` covering both verdicts. Note two constraints the
   code imposes on fixtures: a populated graph always builds a pool (the ANN returns nearest
   rows whatever they score), so `CandidatesEmpty` needs an empty corpus; and an active filter
   routes to the pre-filtered ANN path and so yields `CandidatesEmpty`, which means
   `PoolFiltered` must be reached through expiry.

## Acceptance

- [x] The floor's cut rows reach both surfaces, bounded, demarcated, never inside the ranked list.
- [x] An empty result names whether a pool formed.
- [x] The pollution guarantee holds unmodified.
- [x] Gates green.

## Verify

```sh
cd /Users/feb/dev/cartridge/memory.ctg
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo nextest run --workspace -E 'test(a_floor_in_the_band) or test(an_empty_result_names_which_empty_it_is) or test(an_entity_under_the_floor_does_not_leak_through_a_path_chain)'
```
