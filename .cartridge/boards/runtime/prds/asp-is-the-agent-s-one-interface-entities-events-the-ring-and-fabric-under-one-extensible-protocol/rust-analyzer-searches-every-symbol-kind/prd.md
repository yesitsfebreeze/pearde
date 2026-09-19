---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/lsp.ctg"
work-kind: leaf
capability-owner: lsp
footprint:
  - /Users/feb/dev/cartridge/lsp.ctg/src/client.rs
commit: "6f3ee0dabbf6bd82a325fb32f7442f9d41244485"
---

# rust-analyzer searches every symbol kind

## Outcome

ASP search finds methods in a large Rust workspace. rust-analyzer's `workspace/symbol` defaults to types only and cuts fuzzy matches at 128, so in this workspace `search "Host asp"` never returned `Host::asp` even after word search landed. lsp now starts rust-analyzer with `workspace.symbol.search.kind = all_symbols` and a limit of 1024. Verified live on 2026-09-19: `Host asp` ranks `symbol:cartridge.ctg/src/asp/mod.rs#Host::asp` first, and `asp_expand` finds `Host::asp_expand`.

## Acceptance

- [x] lsp's suite still passes, including the live word-search test.
- [x] Live: `Host asp` returns the method first (recorded above).
