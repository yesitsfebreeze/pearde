---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/memo.ctg"
work-kind: leaf
capability-owner: memo
footprint:
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/docs/README.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/docs/context.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/docs/inventory.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/docs/source-search.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/memos/note/program-cartridge-contracts.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/memos/note/program-checks.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/memos/note/program-map.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/memos/system/program-entry.md
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/integration/inventory.test.ts
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/integration/source-search.test.ts
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/integration/tests.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/source_search.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/src/fabric_graph.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/src/graph.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/src/rank.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/src/sources/census.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/src/sources/inventory.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/src/sources/search.rs
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/unit/src/view.rs
  - /Users/feb/dev/cartridge/memo.ctg/README.md
  - /Users/feb/dev/cartridge/memo.ctg/cartridge.json
  - /Users/feb/dev/cartridge/memo.ctg/src/asp.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/document.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/fabric_graph.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/graph.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/host.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/inventory.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/limits.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/rank.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/record.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/service.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/settings.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/source_search.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/sources/census.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/sources/inventory.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/sources/limits.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/sources/mod.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/sources/search.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/view.rs
commit: "4f8903d56e191cc4bed192813cfa245e49de99f6"
---

# memo's fabric is deleted and every caller reads asp

## Outcome

memo has no fabric any more. The `fabric` op on `tool.memo` and on the native `memo` service, its `graph` alias, fabric v2 (the owner inventory) and v3 (source search), `fabric_graph.rs`, the git view and the `graph.announce` event are deleted, and so are the `tool.*` and `source.*` needs and the nine settings only the fabric read. ASP (`cartridge call asp`, `tool.asp`) is the one graph and the one search. What memo still needs of the old code, the record as nodes and edges and the journal-weighted match its `asp.memo` search uses, lives in `src/graph.rs` and `src/rank.rs`. No consumer of v2 or v3 existed anywhere in the workspace, so both are deleted, not ported.

## Acceptance

- [x] `tool.memo` and the native service refuse `op: "fabric"`, shown by a named test.
- [x] memo's ASP search still ranks by word match times observed use, shown by named tests.
- [x] memo's `cartridge.json` declares no `graph.announce`, needs only `context.*`, and carries none of the fabric's settings.
- [x] README, help, docs and the shipped program memos point at ASP.
