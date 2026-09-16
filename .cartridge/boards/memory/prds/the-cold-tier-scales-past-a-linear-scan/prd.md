---
state: "analyzing"
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge/memory.ctg"
claim: "claude-main 2026-09-16T08:16:27.642Z"
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
## Result

Partial. One of the two whole-tier reads on the query path is roughly halved; the
outcome is not met, because a query still visits every cold row.

### Landed

memory.ctg `36478df`. `cold_candidates` now ranks the tier by query cosine from the
vector side table (new `Store::cold_visit_vectors`), then walks that order decoding
rows and applying the unchanged gates and boosts, stopping once
`COLD_OVERFETCH = 8` rows per delivered slot have passed the gates. The side table
existed for exactly this read (`ColdRow::of` strips the vector out "so scoring the tier
never decodes the row it belongs to"), but the query path had never used it.

The first version truncated the shortlist before the gates ran, and
`memory_contract::cold_filters_precede_the_delivery_cut_and_expired_rows_stay_stored`
failed: twenty pending rows and one expired row at cosine 1.0 crowded out the eligible
row at 0.9. The budget now counts only admitted rows, so a filter cannot spend it and a
heavily filtered query degrades toward a whole-tier decode instead of toward a wrong
answer. Boosts remain the stated approximation.

New test `the_two_stage_cold_scan_matches_a_brute_force_ranking` asserts delivered order
equals a brute-force cosine ranking over 400 rows. Two ignored measurement tests live
beside it in `cold_scan_cost`.

### Measured

Release build, one test thread, same machine, same fixture; "before" is the parent commit
with only `retrieval_query.rs` reverted.

| cold rows | before | after |
| ---: | ---: | ---: |
| 1,000 | 15 ms | 8 ms |
| 10,000 | 126 ms | 54 ms |
| 50,000 | 520 ms | 312 ms |
| 100,000 | 1,018 ms | 549 ms |

At 50,000 rows, decoding every row body to score it cost 313 ms and streaming the vector
side table for the identical scores cost 56 ms.

Gates: `cargo fmt --all -- --check` and `cargo clippy --workspace --all-targets -- -D warnings`
clean; `cargo nextest run --workspace --no-fail-fast` 1420 passed and 3 failed, the three
being the pre-existing `memory::cartridge` profile-trust failures.

### Found along the way

- `score::access_order` is now the larger whole-tier read. It calls
  `cold_visit_accesses`, which decodes every cold row body to read `accessed_at`. At
  50,000 rows it took 171 ms and returned zero stamps, because no fixture row had ever been
  accessed. Fixing it needs either an access-time side table beside the vector one or an
  access order cached against the mutation epoch.
- `COLD_MAX_ENTRIES = 50_000` (`src/base/src/base_constants.rs`) and `Store::cold_cap_amortized`
  are called from nowhere in `src/`, and a doc comment in the store unit tests still claims
  `cold_put_all` calls the latter. The tier is unbounded on purpose: both write paths say
  "Heat changes residency, not retention. Permanent trimming is explicit", and
  `spilling_past_the_old_cap_preserves_every_row` pins it. Wiring the cap would silently
  delete stored memories, so it was not done. The constant and the stale comment are
  candidates for deletion.

### Remaining against Acceptance

- Sublinear query cost: not met. Both remaining reads are linear.
- The `as_of` historical walk: untouched.
- Recall parity: met for the cosine ordering; boosts are approximated beyond the
  admitted budget, as the `COLD_OVERFETCH` comment states.
