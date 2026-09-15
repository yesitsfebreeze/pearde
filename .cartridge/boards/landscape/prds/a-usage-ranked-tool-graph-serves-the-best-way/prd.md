---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: a-usage-ranked-tool-graph-serves-the-best-way
needs:
- "@root/tool-graph-engine-is-the-ranking-database"
- "@root/the-resolver-runs-on-the-tool-graph-engine"
- "@root/tool-dispatch-and-routines-are-graph-nodes"
- "@root/agents-query-the-tool-graph"
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

## From the retired work memo

Folded 2026-09-15 from `work/a-usage-ranked-tool-graph-serves-the-best-way.md` (status open). The PRD state above is authoritative.

> Tooling use, memos and routines are ranked in one searchable graph; how often a thing is used enforces its ranking

### Do

The ranking machinery inside the record — the memo resolver's usage matching,
observation events and usefulness feedback, and the memory crate's graph and
retrieval work — is scattered across cartridges. It should be its own tool: a
ranking database whose nodes are everything the system can reach for — tools,
memos, routines — with the connections between them.

How often a thing is used enforces its ranking: every dispatch, resolve and
outcome is an observation the graph counts. Searching it returns the best
tools and the best way to do things, with descriptions, consistently — not
per-session memory, one ranked surface that any dispatched agent consults
through the same tool.

Extraction means: the existing resolver behaviour (usage `when:` matching,
provenance, feedback events, [record-resolver-usefulness-feedback](../../../memo/prds/record-resolver-usefulness-feedback/prd.md)) keeps
working while its engine moves behind one service; the memo record, tool
dispatch and routines all consult it; and a query like "best tool for X" or
"how we do Y" answers from the graph, ranked by observed use.

### Check

- [ ] [tool-graph-engine-is-the-ranking-database](../../../root/prds/tool-graph-engine-is-the-ranking-database/prd.md) is done.
- [ ] [the-resolver-runs-on-the-tool-graph-engine](../../../root/prds/the-resolver-runs-on-the-tool-graph-engine/prd.md) is done.
- [ ] [tool-dispatch-and-routines-are-graph-nodes](../../../root/prds/tool-dispatch-and-routines-are-graph-nodes/prd.md) is done.
- [ ] [agents-query-the-tool-graph](../../../root/prds/agents-query-the-tool-graph/prd.md) is done.

### Probe

Analyst probe, 2026-09-12, committed on lane
`work/a-usage-ranked-tool-graph-serves-the-best-way` (f34ac50): the
`builtin/toolgraph` engine crate — `Node` (kind, key, description, when,
tags), `search` ranking by field-weighted token match times observed standing
(`1 + ln(1 + uses)`), `counts_from_journal` with stage weights, and an ignored
`real_record_search` smoke over a real record. Unit tests prove kinds are
searched with descriptions and observed use outranks an equally matched
unused entry; clippy and the crate tests are green. The extraction seam was
measured: `usage.rs` and `resolver.rs` depend on the record's namespace
through one glob (`Memo`, `Input`, `workspace`, `no_symlink`, `atomic_write`,
`digest`, `Names`), and the compatibility bar is the existing
`builtin/memo/tests/` suite.

User request, 2026-09-12: "We need a tool graph: how often a tool is used
enforces its ranking. We can search for tools and we get descriptions. It's a
ranking database for tools, memos, and routines for everything that we have,
and it gives us back the best tools and the best way to do things in a
consistent manner."
