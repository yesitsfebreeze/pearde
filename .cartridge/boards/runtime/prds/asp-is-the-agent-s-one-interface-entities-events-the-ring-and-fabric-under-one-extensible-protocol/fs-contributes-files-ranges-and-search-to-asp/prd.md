---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/fs.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
footprint:
  - /Users/feb/dev/cartridge/fs.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/fs.ctg/README.md
  - /Users/feb/dev/cartridge/fs.ctg/cartridge.json
  - /Users/feb/dev/cartridge/fs.ctg/init.lua
  - /Users/feb/dev/cartridge/fs.ctg/src/files.rs
  - /Users/feb/dev/cartridge/fs.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/fs.ctg/src/search.rs
  - /Users/feb/dev/cartridge/fs.ctg/src/asp
  - /Users/feb/dev/cartridge/fs.ctg/.cartridge/tests/unit/asp.rs
commit: "69ffb0f3ac4df7ddd4a63c7f42eafa947794fa36"
---

# fs contributes files ranges and search to ASP

## Outcome

fs is an ASP provider and the canonical owner of `file:` (a normalized
workspace-relative path) and `range:` (`<file>:<line>:<col>-<line>:<col>`).
It contributes `file:` nodes whose revision is the content SHA-256, and it
answers ASP `search` with `matches` edges to `range:` nodes. Every other
provider uses fs's canonical file key and never derives its own.

## Start at

- `fs.ctg/src/files.rs:140-152`: canonical path resolution, which refuses to
  escape the workspace.
- `fs.ctg/src/files.rs:630-663`: the content hash as a revision
  (`Version::Sha256`).
- `fs.ctg/src/source.rs:345-406`: today's `context.file` provider, which the
  migration child replaces.
- `fs.ctg/src/search.rs`: search, and the adapter that chains a result into a
  tool.

## Decision (2026-09-19, ASP coordinator)

- The provider's own tests cover identity, revision and search in fs.ctg; the
  host attributes and marks staleness, which the host's own tests cover. The
  live daemon shows both together: expanding `file:fs.ctg/src/asp/mod.rs`
  returns the node attributed to `fs` with a SHA-256 revision, the `symbol:`
  nodes from lsp with the same revision, and memo as a third source.
- The workspace is the directory the host runs nodes in. ASP carries no
  session, so in git mode a revision moves only once a change is materialized.
- The `read` action's `args` are `tool.read`'s input (host rule, collected as
  `an-asp-action-s-args-are-the-tool-s-input`).
- The provider is `src/asp/` with one file per responsibility: identity,
  expand and find.

## Acceptance

- [x] A named test expands a `file:` entity through ASP and gets its node with
      a SHA-256 revision attributed to `fs`.
- [x] A named test searches through ASP and gets `matches` edges to `range:`
      nodes whose lines and columns are exact.
- [x] A named test edits a file after fs has answered. The next expand shows
      the other providers' earlier facts about that file as `stale`.
- [x] fs's `cartridge.json` declares the `file` and `range` schemes, the
      `matches` edge and the `search` capability. The README and help page
      are updated.
