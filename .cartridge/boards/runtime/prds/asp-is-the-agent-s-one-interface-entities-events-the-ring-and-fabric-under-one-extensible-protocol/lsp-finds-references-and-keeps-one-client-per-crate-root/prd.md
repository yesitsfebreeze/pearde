---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/lsp.ctg"
work-kind: leaf
capability-owner: lsp
footprint:
  - /Users/feb/dev/cartridge/lsp.ctg/src
  - /Users/feb/dev/cartridge/lsp.ctg/.cartridge/tests/unit
  - /Users/feb/dev/cartridge/lsp.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/lsp.ctg/README.md
commit: "c09ab1a92c375b5ef0e5db495ef6b49227d45c78"
---

# lsp finds references and keeps one client per crate root

## Outcome

`tool.lsp` answers `references` with the call sites of a Rust function, and a
query in a second crate root is answered by that root's own language server.
This is the first slice of
[lsp contributes symbols usages and calls to ASP](../lsp-contributes-symbols-usages-and-calls-to-asp/prd.md).
It carries that PRD's first two acceptance items and none of its ASP surface,
so it does not wait for the ASP core.

Both defects were observed on 2026-09-19. rust-analyzer rejected
`textDocument/references` with `missing field 'context'`, because
`Client::query` sent only `{textDocument, position}`. `Service::client_for`
keyed clients by server id alone, so every crate after the first was served by
the first crate's rust-analyzer.

## Acceptance

- [x] A named test calls `references` on a Rust function through
      `Service::dispatch` and gets its call site. The request carries
      `context.includeDeclaration`.
- [x] The same test queries two crates with different roots. Each answer names
      only its own crate's files, and `status` lists one running root per crate.
- [x] The lsp README and help page describe the per-root servers and the
      `roots` field of `status`.

## Decision (2026-09-19, coordinator)

The slice is its own leaf because the parent lsp PRD needs the ASP core, which
is held by a footprint overlap in cartridge.ctg. `status` gains a `roots` list
per server, so the per-root behavior is observable without reaching into the
service. A cache hit now refreshes the client's LRU stamp, because with one
server per crate root `max_servers` evicts by use and no longer by start order.
