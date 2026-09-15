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

# the health counters behind `memory health` moved onto the store they count — one `graph::graph::Counters` per `GraphGnn`, so one daemon over two stores reports each store's own numbers

## Do

Every per-store degradation count — `query_dim_rejected` (graph/search.rs),
`supersede_chain_depth_exceeded` (graph/accept.rs), `ingest_queue_refused`,
`ingest_hygiene_rejected`, `ingest_dropped_chunks`, `ingest_unresolved_replaces`
and `ingest_tombstoned` (ingest/ingest_worker.rs, ingest_place.rs),
`clock_skew_skips` and `unspilled_drops` (tick/tick_stigmergy.rs), and
`gnn_train_refused` (tick_loop/tick_trainer.rs) — was one `static COUNTERS`
per file with a `*_counting` entry point beside the production one. They now
live in `graph::graph::Counters`, one `Arc<Counters>` on every `GraphGnn`
(`g.counters`), never persisted: `GraphGnn` is rebuilt through
`from_saved_with_mode`, so no format byte moves. `search::dim_guard` and
`accept::bump_supersede_chain_depth` count on the graph in hand;
`Worker::new` and `Trainer::spawn` clone the graph's `Arc` so a refusal is
counted on the producer's thread without the graph lock; `run_gc` clones it
for the sweep; `place_document` bumps the unresolved-replaces count inside the
write lock it already holds; `health::graph_health_stats(g)` reads every
field off `g.counters`, and rpc reads health. The `*_counting` variants,
the statics, `process_counters()`, `with_counters`, `note_unresolved_replaces`
and every free `fn xxx() -> u64` reader are deleted; `health` no longer
depends on `tick` or `ingest`, and `rpc`'s `tick_loop` is a dev-dependency.
The below-floor counter the original Do named was deleted with the delivery
floor's zero cut and is not resurrected. The completion failures move off
their static onto the llm `Client` (`client.complete_failed()`,
`client.last_complete_failure()`, shared by clones; rpc reads `self.llm`):
the endpoint is the daemon's, not a store's. The one count still process-wide
is `llm::shutdown_refused()`, a bare static beside the process-wide latch it
reads. `store_core`'s sticky `MIGRATED_FROM` became a `Store` field noted only
where a versioned row is decoded (`get_with`, `scan_with`, `epoch_in`;
`cold_all` reads the raw vector table itself), read as `store.migrated_from()`
by doctor and migrate. Landed on main as merge `920bd2a9`
(2026-09-06).

## Acceptance
`rg 'static COUNTERS' src` prints nothing, and no former counter static
remains (`rg 'static (DIM_REJECTED|SUPERSEDE_CHAIN_DEPTH_EXCEEDED|BELOW_FLOOR|QUEUE_REFUSED|HYGIENE_REJECTED|INGEST_DROPPED|MIGRATED_FROM|COMPLETE_FAILED|CLOCK_SKEW|UNSPILLED|TRAIN_REFUSED)' src` is empty).
`rpc::server_admin_test::a_dropped_query_on_one_store_leaves_the_other_stores_health_at_zero`
opens two `Server`s over two stores, drives a 3-dim query against one's 4-dim
index, and asserts `query_dim_rejected` is 1 there and 0 on the other;
`health::tests::the_graphs_own_counters_reach_health_and_another_graphs_do_not`
pins all ten fields; `rpc::a_failed_completion_through_the_servers_client_reaches_health_stats`
drives a failed completion through the server's client and reads it off
`health_stats`; the worker, stigmergy, trainer and store_core tests read the
increment on the graph or store they drove. `cargo nextest run --workspace`:
1211 passed. The CLI's no-daemon `memory health` still prints its own zeros —
the freshly loaded graph's counters.

