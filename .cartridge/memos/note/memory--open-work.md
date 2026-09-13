---
kind: documentation
description: what is left — every open defect and unbuilt half, ranked worst-first, with the file that carries it
read_when: "picking up work"
---

# Open work

**The only place in the repo that plans work.** Ordering is the content: the
topmost item is the most important open thing, and importance falls
monotonically from there. Rank is severity × reach, with sequencing as hard
edges — where B cannot be done before A, A sits above B and says so.

Folded 2026-09-05 from `docs/ROADMAP.md`'s nineteen live items and
`.pearde/prds/`'s thirteen live PRDs, both dissolved by
`the-registers-collapse`. Two PRDs did not survive the fold and are
named at the bottom. Every claim below carries the file it was measured
against; a line whose citation is dead is a bug, not a note.

## Retrieval — what memory returns and how it ranks

1. **The delivered top-5 is polluted and doc chunks outrank the facts that
   answer the question.** Measured 2026-09-03 by a 12-fact recall probe that
   no longer exists — `tests/memory_recall_probe.py` went with the rest of the
   Python ([[@prd/work/memory--port-the-benchmark-runners.md]]).
   `min_deliver_fraction` is the delivery floor, a fraction of the best hit's
   final score, cut last (`the-floor-is-a-fraction-of-the-top`). Measured
   2026-09-05 by `tests/e2e/pollution.rs` with the floor off: mean 3.76 / max 4
   unrelated facts in the top-5 over 72 probes, the gold fact ≥ 0.972 of the
   top, the best decoy ≤ 0.796. At 0.85 pollution is 0.00 / 0 and
   recall@1/@5/MRR hold at 0.9861 / 1.0000 / 0.9931; the test sets 0.85 in its
   own `memory.toml` and asserts both halves of the band. The default stays 0.0
   because any floor in the band also cuts the neighbour the walk reaches over
   a reason edge, and three tests hold it there
   (`a-floor-cuts-the-linked-neighbour`). `lexical_top_boost` is not the
   cause: at 0.0 recall@1 drops 71→66 and a decoy reaches the top, at 0.2 the
   band narrows; it stays at 0.5. `source_trust` is untouched — the corpus has
   no doc chunks, so the doc-chunk half of this item is still unmeasured. What
   is left is the walk: lift a linked neighbour above an unrelated seed, then
   flip the default. `recall-pipeline`.

2. **CLOSED 2026-09-07.** *The GNN re-embeds the same corpus differently in
   every process* — filed 2026-07-22 off a recall metric that moved
   0.9028 → 0.8611 across two runs of the *unchanged* suite against a 0.8500
   floor, with "non-determinism in the embedding is the only remaining
   explanation" and every measurement above it called unstable until it closed.
   Neither half survived. The metric was measured by a test that never runs the
   GNN — `recall.rs` goes through the CLI, which has no tick loop, so
   `do_gnn_propagate` is not called there at all
   (`the-recall-number-never-exercised-the-gnn`) — and the unseeded draws are
   gone: one `StdRng` seeded from SHA-256 over the snapshot's entity ids
   (`the-gnn-is-deterministic-per-corpus`). Measured 2026-09-07 on
   `tests/e2e/gnn_recall.rs`, the suite that lowers `min_thoughts` to 4 so the
   propagation does run: two runs on a65a28c7 printed the same block —
   `propagations 1, nodes=[36]`, recall@1 0.9861, recall@5 1.0000, MRR 0.9931
   (`the-gnn-recall-numbers-were-re-run`). Struck, not re-filed: the corpus the
   seed hashes cannot vary either, since an inline ingest's id is
   `content_hash(text)` over 36 `const` facts and no id on the mint path reads
   a clock (`tests/id_mint_reads_no_clock.rs`). What moved the 2026-07-22
   number is a question about `recall.rs`, not about the GNN.

2a. **CLOSED 2026-09-05, except the `memory mcp` half.** The e2e suite was red
   on main from 2026-09-03 for two distinct defects the memo-4 gate run
   exposed. Measured on clean HEAD (dc5e771, fake_llm's `_TURN_MARKER`
   restored): five tests red. Both are fixed; the suite is down to one
   failure, `test_memory_mcp_auto_starts_the_hub_and_routes_through_it`, which
   is item 22's other half and not a defect in anything built.
   (a) *The inline origin killed near-duplicate dedup* — d1c1768 minted
   `Source::Inline { hash: content_hash(&text) }`, so the origin hash of
   `Source::Inline` included the text, and two near-identical texts were
   different origins *by construction*; `accept::same_origin` refused the
   merge and `test_a_deduped_ingest_still_applies_its_retention` read
   `status=committed` where it expects `status=deduped`. Fixed in `2ab3db0`
   by `inline-names-no-origin`: `Source::origin_id()` answers the question
   the gates ask, and `Inline` answers None. `test_forget_source` was red for
   the other half of the same landing — the drain now stamps the whole
   canonical path, so the test's `file://notes.md` selector named nothing.
   (b) *One linked neighbour fell out of the top 5* —
   `test_a_reason_edge_makes_its_neighbour_reachable` failed on the
   deploy/Jenkins → bees/lavender pair (rank 8, no-chain) while the
   walk-credit invariant held for the other seven. Root cause was not the
   walk: `link_entities` vectored the edge by an embedding of its reason
   NOTE, so `expand::edge_evidence`'s `cosine(query, edge.vector)` term
   collapsed to zero for exactly the links that exist to bridge dissimilar
   texts. Fixed by `a-link-is-vectored-by-its-endpoints` — the edge carries
   the endpoint midpoint, as an automatic `Similarity` edge already did.
   Both were the same class as the `_TURN_MARKER` deletion and the
   `status=committed` expectations an earlier session repaired: the e2e gate
   was never re-run after the ingest changes that broke them, and CI could
   not catch it — `.github/workflows/ci.yml` triggers on `branches: [master]`
   against a repo whose branch is `main`.

3. **CLOSED 2026-09-05.** *A filtered search never terminated early when the
   predicate was rare* — the beam set `worst` only once `results` was full, and
   a rare predicate never filled it, so the walk covered the whole index.
   `beam_search_filtered` now counts its distance computations and, past
   `ef * VISIT_BUDGET_PER_EF`, discards the walk for an exact scan of the kept
   subset — cheaper than the walk it replaces and returning what brute force
   over the subset returns, so `search_filtered_matches_brute_force_over_subset`
   still holds. `filtered-search-termination`.

4. **The ANN keeps what the graph deregistered.** `GraphGnn::deregister`
   (`src/graph/src/graph.rs:856`) and `GraphGnn::unload` (`:874`) remove the memory
   from the maps and leave its entities in the vector index, so a forgotten
   entity is still a seed. **Reproduced 2026-09-06**, and the mechanism is
   narrower than this line said — the citations above were dead and the removal
   is per memory, not per entity (`the-ann-keeps-what-the-graph-deregistered`).
   A two-memory probe returns the victim's entity from `search_all_unlocked`
   unchanged after both calls while `find_entity` stops resolving it: the ghost
   costs a top-5 slot on the unfiltered seed path, and a filtered query does not
   pay it because `matches_keep` resolves through `memory_of_entity`. `deregister`
   is the half this line names and the half nothing reaches — both callers
   (`graph.rs:961`, `src/tick_loop/src/tick.rs:402`) only deregister memories with
   no entities. The reachable half is `unload`, which `tick_idle` runs on live
   memories, and there the entity is parked on disk rather than forgotten, so
   deleting its vector would make a parked memory unretrievable instead of fixing
   anything. Which side of that seam moves — `unload` drops the vectors, or
   `find_entity` learns to resolve through an unloaded memory — is undecided, and
   nothing below item 1 should be re-ranked against this until it is.
   The drill now holds it, both sides costed against `6f62546a`:
   `which-side-of-the-unload-resolve-seam-moves`.

5. **The importance scan is O(N) per retrieve.** `seed_important`
   (`src/retrieval/src/retrieval_seed.rs:131`) iterates every entity in the memory,
   once per retrieve, unconditionally. Narrowed 2026-07-21 after the
   parallelism bug was fixed — 1.9–3.9× faster and its share of retrieve
   roughly halved, but still linear. The index that would remove the walk is
   blocked; the blocker is the same structural debt as item 8.

6. **The scoring stack is unnormalised and re-founding it is one change, not
   three.** `apply_boosts` (`src/retrieval/src/retrieval_score.rs:138-158`,
   re-checked 2026-09-06 — the cited `:94-109` is now `qbst`'s tail and the
   lexical boost) reads
   `(score * confidence + boost + fact_bonus) * trust`, with no min-max
   normalisation. It is not "purely additive" as this item long said: source
   trust multiplies the whole expression, and confidence multiplies only the
   incoming score — so the recency boost and the Fact bonus bypass confidence
   while a per-scheme prior scales everything
   ([[the-confidence-multiplier-inverts-below-zero]] for what that multiply
   does below zero). The stemmer is hand-rolled
   (`src/graph/src/lexical.rs:244`), with no stopword list and no `rust-stemmers`
   in `Cargo.toml`; swapping it needs a BM25 rebuild. GNN reranking's only
   expression is the 0.6 blend in item 7, and it is unvalidated. Each of the
   three moves the other two, so they are judged together.

7. **`merge_hits` is a raw blend, not RRF.** `0.4·content + 0.6·GNN`
   (`src/graph/src/search.rs:60-61`, applied `:74`) is fragile across scales.
   `fuse::rrf` already fuses the seed layer and never reaches `merge_hits`.
   Record the cost before taking it: RRF keeps rank information only, so a dense
   hit overwhelmingly better than rank 2 gets no credit for the margin. This is
   a trade, not a strict win.

8. **Structural debt in the hot types.** What remains after two rounds of
   retirement is serialization shape and index shape. Per-parent fan-out is a
   real, unbounded cliff. It is what blocks item 5's index.

9. **Two freshness signals, different half-lives, neither ever tuned.** A
   24-hour one for ranking (`qbst_recency_half_life_secs`,
   `src/config/src/config.rs:835`, defaulted from `QBST_RECENCY_HALF_LIFE` in
   `src/base/src/base_constants.rs:12`) and the retention one on `HeatConfig`.
   The offline NDCG sweep meant to tune either was never run. A third input
   nobody reconciled derives a 1–2 day half-life.

10. **Spilling all three indexes was measured and refused.** `rebuild_index`
    hardcodes `gnn_entity_idx` and `reason_idx` to `VectorBackend::resident(...)`
    (`src/graph/src/graph.rs:367-368`) while only `entity_idx` takes the spill
    branch (`:296-297`). Spilling the other two costs 122 MB more, measured
    2026-07-21. Recorded so it is not re-proposed. `graph-store`.
    **False, checked 2026-09-07** (`the-second-half-of-the-ranked-list`):
    `rebuild_index` (`:415`) now sends all three indexes through
    `Self::disk_or_resident` on the spill branch (`:451-455`), under a comment
    reading "Disk snapshots (mmap) for all three indexes";
    `tests/spill_transparency.rs` gates it, and `tests/spill_memory.rs` — the
    instrument the 122 MB came from — is Linux-only and `#[ignore]`d, so
    nothing reruns that price. **Repaired 2026-09-07**
    (`the-spill-refusal-graph-store-still-records`): `graph-store` no longer
    says the two stay resident, and withdraws the 122 MB as a refusal. This
    item has no subject left.

## Lifecycle — what is kept and what is forgotten

11. **Nothing bounds memory deterministically: eviction and spill are both
    disarmed.** `MEMORY_CAP_DISABLED` (`src/base/src/base_constants.rs:30`) defaults
    both `max_memories` and `disk_threshold` to `usize::MAX`, so
    `enforce_memory_cap` (`src/graph/src/graph.rs:216`) never unloads a memory and
    the DiskANN spill branch (`:374`) never fires. A per-memory *entity* cap does
    not exist at all. `tick`.
    **False, checked 2026-09-07** (`the-second-half-of-the-ranked-list`): both
    caps are armed by config, not by the sentinel. `config::GraphConfig`
    defaults `max_memories: 128` and `disk_threshold: 0`
    (`src/config/src/config.rs:667-668`) and `bootstrap::apply_graph_config`
    (`src/bootstrap/src/lib.rs:16-21`) pushes both into the graph, so
    `enforce_memory_cap` (`graph.rs:337`) unloads and the spill branch
    (`:425`) fires from the first entity. `MEMORY_CAP_DISABLED`
    (`base_constants.rs:41`) is only what a bare `GraphGnn::new()` carries —
    and a graph loaded from a store does not wait for config either:
    `from_saved_with_mode` (`graph.rs:1019-1021`) sets `disk_threshold = 0`
    itself before the first `rebuild_index`.
    **Repaired 2026-09-07** (`the-spill-refusal-graph-store-still-records`)
    for the spill half; `graph-store` carried the same disarmed default and no
    longer does. The per-memory *entity* cap still does not exist — that clause
    stands, and is all this item is now.

12. **GC has no convergence gate.** The adopted design gated forgetting on
    `G ≥ 0.6` **and** heat below floor for `forget_ttl`. Shipped GC has no gate.
    Depends on the convergence metric existing, which is the open half of the
    stigmergy research note.

13. **Supersede chains are unbounded while contested.** Trigger #1 is
    instrumented as of 2026-07-22 — `supersede` and `supersede_by_contradiction`
    (`src/graph/src/accept.rs`) increment a counter when chain depth exceeds
    `SUPERSEDE_CHAIN_HOP_THRESHOLD` (default 5). The rate-limit, the
    `ReasonKind::Edit` decision and triggers #2 and #3 are open.

14. **CLOSED 2026-09-06.** *`entity_memory` goes stale for a reparented stray.*
    The reparenting block was unreachable and is deleted
    (`the-stray-entity-rescue-cannot-run`); nothing in the tick moves an
    entity between memories any more, so there is no stray for the index to
    miss. Eighteen files still read `memory_of_entity`, and item 4 carries the
    staleness that remains.

15. **Clustering is vector-only.** No semantic or structural features, and
    naming plus enrich are a cold LLM call per memory. The adopted-but-unbuilt
    upgrade is thought-level PageRank feeding the split heuristic: high-rank
    nodes become focuses, bridge nodes become sub-memories. Graph structure
    informs ranking today and never informs the tree shape routing depends on.

## Ingest

16. **An origin is not one string per file — the producers of
    `Source::File.path` disagree.** The file watcher sets the whole path
    (`ingest_file_watcher.rs:85`); the intake drain sets `path.file_name()`,
    the basename alone (`ingest_intake.rs:240-246`), and
    `drain_entry` mints `Source::Session` from `path.file_stem()` the same
    way (`ingest_intake.rs:192-203`; there is no `drain_claims`,
    `some-citations-were-never-true`). Since `source_id()` hashes `scheme + object_id + section` and an
    entity id is `hash(source_id + text)`, two different files sharing a
    basename, dropped into two stores' intake directories, carry *one* origin;
    the same file read by one store's watcher and another's intake carries
    two. Both halves of "same origin unions to one node, different origins
    stay two" are false at the channel boundary — exactly what hub merge
    joins across. Repairing the intake origin re-keys every intake-placed id,
    so it is coupled to the re-key migration; a separator-free path is the
    discriminator for that migration's discriminator test. `ingest-paths`.
    **False in the headline, checked 2026-09-07**
    (`the-second-half-of-the-ranked-list`): both file channels mint
    `Source::File.path` by one rule — `util::watcher::file_origin_path`, at
    `ingest_intake.rs:256` and `watcher.rs:344` — and the comment above the
    first restates this defect in order to say it is closed. `ingest-paths`
    already carried that rule when this line was folded. What survives is the
    `Source::Session` half: `drain_entry` still mints `session:{stem}` from
    `path.file_stem()` (`ingest_intake.rs:193`).

17. **Alias assertions at ingest** — landed 2026-09-04, listed here only
    because item 1's probe reads its output.

18. **A single-line focus seed truncates at the embed context window.**
    Chunk-plus-mean-pool shipped for the multi-line case — `seed_examples`
    (`src/graph/src/accept.rs:717-729`) splits on newlines and `mean_pool` (`:750`)
    averages — but a single line longer than the window is still cut.
    **Closed, checked 2026-09-06**: `seed_examples` is at `accept.rs:1159` and
    `mean_pool` at `:1196`, and the single-line branch splits on a
    `FOCUS_SEED_CHAR_CHUNK` budget at a code-point boundary for the caller to
    mean-pool, the same as the multi-line path
    (`a-third-of-the-ranked-list-no-longer-holds`).

19. **Speculative decode for the distill leg.** A 0.8b draft into a 4b
    generator. With the answer leg gone, distillation throughput is the only LLM
    latency that matters; there is no `draft` or `speculative` anywhere in
    `src/llm/src/llm.rs`. Latency is the one axis the metric does not gate, so
    the e2e harness can judge this.

## Store

20. **Crash consistency on the DiskANN path.** Half of this was verified false
    2026-07-21: per-segment atomic rename does exist — `atomic_write`
    (`src/graph/src/diskann.rs:333-337`) writes `<path>.tmp` then renames, and
    `build_and_save` uses it for meta (`:272`), vectors (`:280`) and graph
    (`:289`), with `DiskIndex::open` (`:310-355`) rejecting a divergent set. The
    residual risk is narrower than the note it was filed from claimed, and is
    the only memo still open.

## Surface

21. **The git surface becomes the command line.** memory's CLI carries git's
    lifecycle verbs, and every mutation it performs leaves a record that can be
    read back and undone. The four `visible_alias`es `grep`/`show`/`rm`/`note`
    and `memory log` + `memory blame` shipped 2026-08-16 and are the baseline, not
    the contract. **Half false, checked 2026-09-07**
    (`the-second-half-of-the-ranked-list`): the four aliases are at
    `src/commands/src/lib.rs:177/227/270/284` and `memory log` at `:238`, but
    `memory blame` is not a command — the only "blame" in `src/` or `tests/`
    is a prose comment in `tests/gnn_scale.rs`. The rule: **git verbs name the lifecycle, domain nouns name
    the physics** — a verb is renamed toward git only where it says what enters
    memory, what leaves it, what supersedes what.

22. **memory speaks MCP from the binary.** Filed 2026-09-05 by
    [[working-with-memory]]'s session, landed same day by another session
    (`commands_mcp.rs` + `.mcp.json`): kept here only until that lands on
    main. `dispatch`.
    **Landed, checked 2026-09-07** (`the-second-half-of-the-ranked-list`):
    `src/commands/src/commands_mcp.rs` and `.mcp.json` are both in
    `origin/main`, so the condition this line kept itself for is met and the
    line is spent.

23. **`memory intake drain` refuses the direct intake with no daemon.** Measured
    2026-09-05: `commands_intake_cmd::drain` early-returns "nothing pending"
    on `scan(dir).pending.is_empty()`, and `ingest_intake_status::scan`
    reads only the intake's top level — `direct/*.json` is invisible to it,
    though `drain_once` drains `direct/` fine and the daemon's loop does so
    every pass. A direct payload parked with the daemon down waits for a
    daemon forever. Fix: `scan` counts `direct/`, or `drain` drops the
    early-return and always runs one pass. `ingest-paths`.
    **Specced 2026-09-07**
    ([[@prd/work/memory--the-intake-status-scan-cannot-see-the-direct-queue.md]]): the early
    return sits before `route("intake_drain")`, so it fires with the daemon up
    too, and both parkers of `direct/` live inside the daemon; the work memo
    takes the `scan` fix, since `memory intake status` lies by the same read.

## Gates and process — none of it affects a running memory

24. **The removal gates can pass for the wrong reason.** `one-removal-policy`
    collapsed the drifted copies of "may this entity be removed" into one table
    in `base` and left three gates watching. Every gate was watched red before
    the verdict, and a skeptic found no false green today — the open half is
    that each must keep failing for the reason it was written, so a future edit
    that reintroduces the drift is refused rather than quietly tolerated.

25. **The dependency gates do not see everything they claim to.** The two gates
    `declared_dependencies.rs` and `tracked_artifacts.rs` left behind stop
    passing on declarations they cannot reach, and claim limits that run the
    other way. `layers` says outright that the first is a grep and a floor,
    not a proof. Narrowed 2026-09-05: the first now splits on any `#[cfg]` that
    gates on `test` (`all(test, unix)` had hidden `test_support` as a normal
    dependency of `commands`, and `axum` with it, in the release binary); the
    `tracked_artifacts.rs` half stands.

26. **`cmd_migrate` has no test at all.** Stale content-only identity claims sit
    in comments at `src/graph/src/merge.rs:96` and `src/graph/src/accept.rs:213`,
    both falsified by ids carrying their origin. `graph-store`.
    **False on both halves, checked 2026-09-06**
    (`cmd-migrate-is-tested-and-its-item-is-not`): the command has a
    store-backed test, and the two cited comments now say the corrected thing or
    have drifted off their anchors.

27. **A fixture re-implements the thing it tests.** A probe that builds the
    value itself agrees with itself; the defect lives in the disagreement
    between production sites, and only a probe driven through each real site can
    see it. [[method]] states the rule; this is the outstanding instance.
    **False, checked 2026-09-07** (`the-second-half-of-the-ranked-list`): the
    instance landed. `src/ingest/src/tests/origin_channel_probe.rs` drives
    `drain_once` and `MemoryFileWatcherSink::ingest` — the two real mints — and
    quotes this line's own sentence in its docstring; [[method]] records the
    mutation run that pinned it. No other instance is named here, so this item
    has no subject.

28. **A shared `target-dir` can report green on stale code.** Parallel worktrees
    pointing `build.target-dir` at one checkout serialize on cargo's exclusive
    lock — the named cost — but a second cost was not named: under concurrent
    access a run can execute a lib-test binary that predates the edit under
    test. Observed 2026-07-21, a cycle saw `873 passed` with its own three new
    tests absent from the run.

29. **Line anchors cannot survive a merge and no gate can see it.** Every
    citation of the form `` `FILE.md:422-423` `` bets that nothing is inserted
    above line 408. A file that only grows loses the bet on every merge that
    appends, and twice over when two branches each append and combine — four
    times in one day on 2026-07-21. A checker that verifies the line *exists* is
    green through all of it, correctly. The repeated hand re-pointing is a tax
    paid on every merge, not a fix. Reduced in scope by the collapse — far fewer
    documents now carry anchors — but not closed.

## Unranked, found 2026-09-06

The improve loop found these in one night and none is ranked above. They sit
here so the plan can reach them; ordering them against the twenty-nine is a
judgement nobody has made (`the-record-plans-work-in-two-places`).

Correctness, worst first as they look from here:

- A refused flush restores what another writer deleted; absorb is a union with
  no removal branch (`a-refused-flush-undoes-another-writers-removals`), and
  the same union drops a memory's identity
  (`absorb-carries-a-memory-s-contents-but-not-its-identity`). Both are one
  design fact (`memory-deletes-hard-and-merges-by-union`).
- Heat and its as-of stamp are max-joined independently, producing a row hotter
  than either side (`merging-heat-and-its-timestamp-separately-makes-heat-immortal`).
  **False, checked 2026-09-07** (`the-unranked-half-was-never-read`): closed by
  `420ff31a` the same day this bullet was filed. `merge_entity`
  (`src/graph/src/merge.rs:79-83`) moves `heat` and `heat_updated_at` together
  under one comparison and the independent `join_max_time` on the stamp is gone,
  so a merged row's pair is exactly one of the two inputs.
- `GraphGnn.root` and the memories-map root are two live copies with different
  fields authoritative (`the-root-memory-exists-twice`).
- The registry keys a new store by its uncanonical path, so one directory can
  get two graphs (`the-registry-keys-a-new-store-by-its-uncanonical-path`).
  **False, checked 2026-09-07** (`the-unranked-half-was-never-read`):
  `Registry::canon` (`src/store/src/registry.rs:63-74`) canonicalizes the
  *parent* and appends the leaf when the directory does not exist yet — the fix
  the memo proposed — and the doc comment above it (`:48-62`) states the rule and
  names `transport::typed::canonical_or_parent` as its deliberate twin.
- Three sites bypass an index their helper maintains
  (`every-derived-index-is-maintained-by-convention`).
  **Every named instance is dead, checked 2026-09-07**
  (`the-unranked-half-was-never-read`): `evict_empty_children`
  (`src/tick_loop/src/tick.rs:381-412`) no longer moves entities into the parent
  at all; the `Rephrase` repoint drops the edge, re-adds it under its new `from`
  with a recomputed id and re-derives both lexical documents
  (`src/graph/src/accept.rs:872-887`); and `do_resolve` does the same
  (`src/tick_loop/src/tick_tasks.rs:473-478`). The general claim stands —
  `Memory`'s fields are all still `pub` (`src/base/src/base_types.rs:555-585`) and
  `get_mut` (`src/graph/src/graph.rs:733`) still hands them out — but it has no
  instance left to point at.
- `math::cosine` truncates a dimension mismatch into a plausible score
  (`cosine-truncates-a-dimension-mismatch`).
  **False, checked 2026-09-07** (`the-unranked-half-was-never-read`): closed by
  `6e4af940` on 2026-09-06, the day this bullet was filed. `cosine` refuses at
  the top — `if a.len() != b.len() { return 0.0; }`
  (`src/math/src/math.rs:17-19`) — and the memo cited here already ends by
  saying so.

Ranking and retrieval:

- MMR mixes a cosine with a fused score (`mmr-mixes-a-cosine-with-a-fused-score`).
  **False, checked 2026-09-07** (`the-unranked-half-was-never-read`): closed by
  `e5589c39`. `sim_q` is one quantity —
  `cosine(query_vec, &cand.entity().vector)` for every candidate
  (`src/retrieval/src/retrieval_diversify.rs:74-77`) — with no `cand.score()`
  fallback, so a vectorless row scores 0 rather than 1.75.
- The index merge never penalises absence (`the-index-merge-never-penalises-absence`).
- Section dedup keys on the section alone (`section-dedup-keys-on-the-section-alone`).
- A prefix id lookup returns an arbitrary match
  (`a-prefix-id-lookup-returns-an-arbitrary-match`).
  **False, checked 2026-09-07** (`the-unranked-half-was-never-read`): closed by
  `9782bf66`. `find_entity_by_prefix` answers the lowest matching id
  (`src/graph/src/search.rs:176-184`), so two daemons over one store resolve one
  prefix the same way. Uniqueness is still unchecked, which is a smaller claim
  than "arbitrary".

Maintenance and lifecycle:

- The hourly slot is spent even when the task is shed
  (`the-hourly-slot-is-spent-even-when-the-task-is-shed`), beside two
  opposite enqueue policies (`the-pulse-has-two-enqueue-policies`).
  **False, checked 2026-09-07** (`the-unranked-half-was-never-read`):
  `claim_slot` now answers the stamp it replaced
  (`src/tick/src/tick_pulse.rs:51-57`) and all three gated sites store it back
  when the enqueue is shed (`:37`, `:76`, `:94`), so a shed delays the interval
  instead of spending it. The two policies do still differ —
  `maybe_enqueue_reembed` (`:97`) is ungated — but the harm the second memo
  names is exactly the one just removed.
- The reap drops edges it never counts (`the-reap-drops-edges-it-never-counts`).
  **False in its headline, checked 2026-09-07**
  (`the-unranked-half-was-never-read`): closed by `08b30e2a` — a victim's
  reasons drain to the nearest surviving ancestor, indexed there with
  `reason_memory` following, before `deregister` runs
  (`src/graph/src/graph.rs:926-957`). The counting half stands:
  `gc_empty_memories_counted` (`:971`) answers three counts of memories and `cmd_gc`
  (`src/commands/src/commands_gc.rs:9`) prints only those.
- Evidence decay would compound if it were on
  (`evidence-decay-would-compound-if-it-were-on`).
- Hot reload fingerprints mtime, not content
  (`hot-reload-fingerprints-mtime-not-content`).
- A junk name becomes a junk attractor (`a-junk-name-becomes-a-junk-attractor`).

Items 2, 18 and 26 above are false as written, and 29 is half true; each is
annotated in place (`a-third-of-the-ranked-list-no-longer-holds`). Items 10,
11, 22 and 27 are false too, and 16 and 21 are false in their headline
sentence; each is annotated in place
(`the-second-half-of-the-ranked-list`). The part items 10 and 11 falsified
with them, `graph-store`, is repaired
(`the-spill-refusal-graph-store-still-records`). All twenty-nine have now been read
against the tree: seven false, three false in the headline.

The unranked half above was read for the first time on 2026-09-07
(`the-unranked-half-was-never-read`), fifteen bullets in three groups: six
outright false, two false in the headline, seven standing. Five of the eight point
at a memo that already ends by closing itself, and every commit those notes name
is dated 2026-09-06 — the day the bullets were filed, so they were stale when
they were written and not since.

## Did not survive the fold

Two PRDs were open against trees this change removes, and close with them:

- **The docs tree becomes the board.** Its subject — a document registry
  describing a retired layout, a roadmap declaring itself the only planner, a
  prevention ledger whose harness cannot fail — is deleted rather than
  reorganised. This file is what it asked for.
- **The lanes reap their own build output.** `.pearde/.lanes/` is gone; nothing
  grows a `target/` per worktree any more.
