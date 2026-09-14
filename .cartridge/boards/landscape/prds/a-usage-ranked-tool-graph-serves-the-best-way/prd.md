---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: a-usage-ranked-tool-graph-serves-the-best-way
---

# One usage-ranked graph answers which tool, memo or routine to use

The separate `toolgraph`/landscape ranking crate was dissolved (root decisions `the-fabric-owns-the-graph.md`, `the-fabric-lives-in-core.md`; host commit 939e7d1 removed core's copy). The single derived ranker is now `memo.ctg/src/fabric_graph.rs`, fed by `graph.announce` rows (`memo.ctg/src/graph.rs`) and the resolver observation journal (`memo.ctg/src/resolver.rs`). This leaf reconciles the four older children against that source and proves ranking through the real `fabric` op, adding no service or store.

## Acceptance

- [ ] A reconciliation note maps `tool-graph-engine-is-the-ranking-database`, `the-resolver-runs-on-the-tool-graph-engine`, `tool-dispatch-and-routines-are-graph-nodes` and `agents-query-the-tool-graph` each to a current symbol and test at a named memo revision, or to a residual gap; the resolver move reverted by the dissolution is recorded as such.
- [ ] Through `tool.memo {"op":"fabric","query":…}`, an `observe` event raises one of two equally matched nodes; a malformed journal line is skipped without failing the graph.
- [ ] The resolve/fabric boundary is stated with a default (resolve keeps situation matching; both read one journal standing) and a test proving they read the same counts.

## Proof and recovery

Start: `memo.ctg/src/fabric_graph.rs` (`search`, `counts_from_journal`, `grown`), `memo.ctg/src/service.rs` (fabric op), `memo.ctg/src/usage.rs`, tests `memo.ctg/.cartridge/tests/unit/src/fabric_graph.rs` (`observed_use_outranks_equal_match` covers only the pure function). Gates from /Users/feb/dev/cartridge: `just test memo`, `just check memo` (not run). `agents-query-the-tool-graph` is actively claimed elsewhere; do not reclaim it. Rollback: derived state only; journal and record are preserved.

## Dependencies and review

No hard prerequisites. Target board after rehoming: memo. [Review history](review.md); rounds inherited, maximum five.
