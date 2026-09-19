---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/lsp.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
footprint:
  - /Users/feb/dev/cartridge/lsp.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/lsp.ctg/README.md
  - /Users/feb/dev/cartridge/lsp.ctg/cartridge.json
  - /Users/feb/dev/cartridge/lsp.ctg/init.lua
  - /Users/feb/dev/cartridge/lsp.ctg/src/client.rs
  - /Users/feb/dev/cartridge/lsp.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/lsp.ctg/src/service.rs
  - /Users/feb/dev/cartridge/lsp.ctg/src/asp
  - /Users/feb/dev/cartridge/lsp.ctg/.cartridge/tests/unit/asp.rs
commit: "c5f3f4df58a0e6a7d64b5f1cf881f5a1764cb805"
---

# lsp contributes symbols usages and calls to ASP

## Outcome

lsp is an ASP provider. For a `file:` entity it contributes `symbol:` nodes,
each with its kind, name, signature and span, plus a `contains` edge from the
file. For a `symbol:` entity it contributes `references` edges from
`textDocument/references` and `calls` edges, in both directions, from
`callHierarchy/incomingCalls` and `callHierarchy/outgoingCalls`. An agent can
resolve a bare name to `symbol:` entities through `workspace/symbol`, so it
never needs a line and column to start. Every fact comes from the live
language server, and none from a prebuilt index.

## Start at

- `lsp.ctg/src/service.rs:83-156`: today's ops (`symbols`, `references`,
  `definition`, `hover`, `completion`, `diagnostics`, `status`, `install`).
- `lsp.ctg/src/client.rs:239-255`: `query` builds only
  `{textDocument, position}`. `textDocument/references` also needs
  `context: {includeDeclaration}`, and rust-analyzer rejects the call with
  `missing field 'context'` (reproduced 2026-09-19 through
  `cartridge call tool.lsp`).
- `lsp.ctg/src/service.rs:161-188`: `client_for` keys clients by server id
  only, so a second crate root reuses the first root's rust-analyzer. This
  monorepo has one crate root per cartridge, so without a fix, queries in
  every other crate go to the wrong server.
- `lsp.ctg/src/service.rs:285-303`: `workspace_root`.

## Decision (2026-09-19, ASP coordinator)

- A `file:` key is the path relative to the directory the host runs nodes in,
  canonicalized the way fs keys it, so lsp's facts land on fs's entities with
  the same revision (verified live on `file:lsp.ctg/src/client.rs`: 31 nodes,
  30 edges, fs and lsp both at the same revision).
- A `symbol:` key is `<file key>#<container>::<name>`, with `@<line>` on a
  repeated name. An expand starts an installed server but never downloads one;
  search asks only running clients.
- Attribution to `lsp` is the host's work and is covered by the host's tests.
- The provider is `src/asp/` with one file per responsibility: outline, edge
  ends, file expand, symbol expand and search.

## Acceptance

- [x] A named test calls `references` on a Rust function and gets its call
      sites. The request carries `context.includeDeclaration`. Delivered by
      [the first slice](../lsp-finds-references-and-keeps-one-client-per-crate-root/prd.md),
      lsp.ctg `c09ab1a`.
- [x] A named test queries two crates that have different roots and gets a
      separate client for each, each answering for its own crate. Delivered by
      the same slice.
- [x] A named test expands `file:` for a fixture Rust file through ASP and
      receives `symbol:` nodes with spans and signatures, plus `contains`
      edges, all attributed to `lsp`.
- [x] A named test resolves a bare name to its `symbol:` entity through
      `workspace/symbol`, then walks `calls` two levels deep.
- [x] The outline is compact: kinds are words, paths are relative to the
      workspace, and the answer holds one line per symbol, with no raw LSP
      JSON.
- [x] lsp's `cartridge.json` declares the `symbol` scheme and the `contains`,
      `references` and `calls` edges. The lsp README and help page are
      updated.
