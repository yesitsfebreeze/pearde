---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/memo.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
footprint:
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/memo.ctg/README.md
  - /Users/feb/dev/cartridge/memo.ctg/cartridge.json
  - /Users/feb/dev/cartridge/memo.ctg/init.lua
  - /Users/feb/dev/cartridge/memo.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/record.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/service.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/asp.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/src/asp.rs
commit: "3155a06a194c2dd761a36d12f48de34b58c9c4e6"
---

# memos are ASP entities and memo kinds are ASP types

## Outcome

Every memo is a `memo:` entity in ASP. Memo kinds (the `type` memos that
declare a kind before its instances can exist) are registered as ASP types,
so ASP's registry and memo's kind registry are one mechanism, not two. A memo
that names a file, a symbol or another memo contributes an edge to it. memo
keeps authoring, validating and resolving memos. It stops being the place
agents go to search, because ASP `search` covers memos next to code.

## Start at

- `memo.ctg/src/record.rs:690-734`: `validate`, where a kind must be declared
  before its instances (`undeclared kind`).
- `memo.ctg/src/graph.rs:9-34`: `memo_node`, the memo-to-node mapping that
  `graph.announce` uses today.
- `memo.ctg/src/source_search.rs` and `memo.ctg/src/usage.rs`: memo search
  and the resolver.

## Decision (2026-09-19, ASP coordinator)

- **Kinds are data, not registry entries.** ASP's registry holds what a
  cartridge declares in its manifest, and memo declares one scheme, `memo`. A
  memo kind reaches ASP as the node's first tag, as `memo.kind`, and as a
  `kind` edge to the `type/` memo that declares it, which is itself a searchable
  `memo:` entity. `a_newly_declared_kind_reaches_asp_with_no_manifest_change`
  proves a new kind reaches ASP with no change anywhere else. Registering kinds
  in the host registry as well would give ASP two sources for one fact.
- **Search across providers was verified live**, not by a memo test, because
  it needs a second provider under a host: `asp search "fabric"` on the live
  daemon returned 7 memo hits and 53 fs hits, each attributed to its provider,
  and 30 `matches` edges.
- memo's `file:` expand asserts only `mentions` edges and no node, because
  memo does not own files and its own revision would read as stale.

## Acceptance

- [x] A named test expands a `memo:` entity through ASP and gets its kind,
      description, `uses` situations and edges to the entities it names.
- [x] A named test declares a new memo kind. ASP then lists it as a type
      without any further change.
- [x] An ASP `search` for a word that appears in both a memo and a source file
      returns both, each attributed to its provider.
- [x] memo's `cartridge.json` declares the `memo` scheme. The README and help
      page are updated.
