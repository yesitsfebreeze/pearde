---
state: "open"
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

### Second pass, 2026-09-16

Both follow-ups from the first pass are done. The outcome is still not met.

- memory.ctg `ec42389` deletes the cold cap. `COLD_MAX_ENTRIES`, `Store::cold_cap`,
  `Store::cold_cap_amortized` and `COLD_CAP_SLACK` had no caller outside tests. The
  eviction counter they fed could only read zero, so it went with them: the `evicted:`
  health line, `HealthStats::cold_evicted` and the `cold_evicted` health RPC field. That
  field was a `serde(default)` JSON key on a struct without `deny_unknown_fields`, so
  clients and daemons on either side of the change still read each other. The stale
  test doc comment and the store README bullet are gone. Net −254 lines.
- memory.ctg `a9ab81a` caches the cold access stamps. `Store::cold_visit_accesses`
  keeps the stamps after its first read and reuses them while `cold_generation` stands;
  all four cold writers (`cold_spill`, `cold_put_all`, `cold_rekey`, `import_snapshot`)
  move the generation after commit, and a scan that races a write declines to cache. The
  cold row count guards against another process's spills. The known gap, named in the
  code: another process's `cold_rekey` or overwriting import is not seen. Test
  `cached_cold_access_stamps_follow_every_write` pins the overwrite case, which keeps the
  row count and so can only be caught by the generation.

Release build, one test thread, 1024 dimensions, every fixture row carrying an access
stamp. "First" is a query on a freshly opened store; "repeat" is the next query, which is
the steady state of a running daemon.

| cold rows | at start of work | first | repeat |
| ---: | ---: | ---: | ---: |
| 1,000 | 15 ms | 8 ms | 3 ms |
| 10,000 | 126 ms | 54 ms | 13 ms |
| 50,000 | 520 ms | 212 ms | 62 ms |
| 100,000 | 1,018 ms | 413 ms | 119 ms |

At 50,000 rows `access_order` went from 133 ms to 0 ms once cached.

Gates: fmt and clippy clean; `cargo nextest run --workspace --no-fail-fast` 1416 passed,
3 failed, the three pre-existing `memory::cartridge` profile-trust failures.

### What is left

A repeated query is now dominated by the vector side-table scan, which costs about
1.1 µs per cold row (56 ms at 50,000). That is the floor for any design that compares the
query against every row. Going below it needs an approximate index over the cold vectors,
which is the first variant this PRD named, and it trades away the exactness that the
brute-force parity test currently holds. The `as_of` historical walk is still a full
flatten of the hot graph and was not measured. Whether roughly 120 ms at 100,000 cold
rows is good enough is a product decision, not a finding.
