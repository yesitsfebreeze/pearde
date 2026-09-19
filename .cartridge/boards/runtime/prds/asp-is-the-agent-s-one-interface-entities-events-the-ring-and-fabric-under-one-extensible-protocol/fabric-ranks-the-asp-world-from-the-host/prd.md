---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/memos-are-asp-entities-and-memo-kinds-are-asp-types'
---

# fabric ranks the ASP world from the host

## Outcome

The fabric, the ranking engine memo serves today as `memo {op:"fabric"}`,
moves into the host as ASP's ranker. It ranks ASP entities for an agent's
situation. Its inputs are every provider's contributions, the ring's
recency and `touched` counts, and usage. It keeps the rule that current
guidance ranks above delivered history. `memo {op:"fabric"}` and its `graph`
alias are deleted in the same change, and every caller moves to ASP.

## Start at

- `memo.ctg/src/fabric_graph.rs`: nodes, edges and the stage weighting.
- `memo.ctg/src/service.rs:500-505`: the `fabric` op and its `graph` alias.
- `memo.ctg/src/graph.rs:133`: the `graph.announce` constant that
  contributors listen on. The announced graph becomes ASP contributions.
- Prior decisions: root memos `the-fabric-owns-the-graph.md` and
  `the-fabric-lives-in-core.md`, and host commit `939e7d1`.
- Ranking rules to keep:
  `@landscape/a-search-ranks-current-guidance-over-delivered-history` and
  `@landscape/a-usage-ranked-tool-graph-serves-the-best-way`.
- Known performance bug to avoid carrying over:
  `@root/fabric-landscape-ranked-fabric-query-times-out-isolate-and-fix`.

## Acceptance

- [ ] A named test ranks ASP `search` results for a situation. A current
      memo outranks a delivered one on the same subject.
- [ ] A named test shows that an entity touched recently in the ring ranks
      above an identical untouched one.
- [ ] `memo {op:"fabric"}`, `graph.announce` and `fabric_graph.rs` are gone
      from memo, and `rg -n 'op:"fabric"|graph.announce'` finds no caller.
- [ ] The memo system-prompt entry that names the fabric
      (`@memo/system/program-entry.md`) names ASP instead.

## Collection audit, 2026-09-19, coordinator codex

The engine dry collection exited 2 with `collect: open acceptance boxes remain`. All three child receipts exist, but that does not prove the two parent ranking comparisons. The current host test `search_ranks_what_the_providers_found_with_the_fabrics_formula` compares two file results and positive score; it does not compare current versus delivered memos or otherwise identical touched versus untouched entities. A targeted sweep of host and Memo tests found no named comparison for those requirements. This is missing acceptance evidence, not a claim that the runtime cannot rank correctly. The host search implementation and test have foreign uncommitted changes, so no acceptance box was ticked and no source was swept. Next analysis must inspect committed ranking behavior and provide the exact two required proofs before collection. Dry-run output is retained at `/tmp/codex-fabric-parent-dry.json`.
