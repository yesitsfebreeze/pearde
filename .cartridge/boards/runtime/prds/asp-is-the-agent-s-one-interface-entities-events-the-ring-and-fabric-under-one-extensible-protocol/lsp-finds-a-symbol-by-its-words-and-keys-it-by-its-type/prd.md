---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/lsp.ctg"
work-kind: leaf
capability-owner: lsp
footprint:
  - /Users/feb/dev/cartridge/lsp.ctg/src/asp/outline.rs
  - /Users/feb/dev/cartridge/lsp.ctg/src/asp/search.rs
  - /Users/feb/dev/cartridge/lsp.ctg/src/asp/mod.rs
  - /Users/feb/dev/cartridge/lsp.ctg/README.md
  - /Users/feb/dev/cartridge/lsp.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/lsp.ctg/.cartridge/tests/unit/asp.rs
commit: "2e0e6edfceee1c605776fd37f14e334bd06160c9"
---

# lsp finds a symbol by its words and keys it by its type

## Outcome

An agent finds a symbol by the words it would type. ASP search asks `workspace/symbol` for the whole query and then for each of its first four words, merges the answers and ranks an exact name match first; before, `search "Host asp"` did not return the method at all. A method's key names its type, `symbol:<file>#Host::asp`, not rust-analyzer's container text `#impl Host::asp`, and `impl Trait for Type` keys by the type. Keys from `expand file:` and from search both expand.

## Acceptance

- [x] A named test finds `Counter::bump` by `Counter bump`, puts an exact-name match first, and expands keys from both an outline and a search (mutations of the word split and of the ranking each fail it).
- [x] The outline test expects the type-keyed names.
- [x] README and help describe the key rule and word search.
