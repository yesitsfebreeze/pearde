---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: function-index-cartridge
---

# A function-level index answers where code lives

`lsp.ctg` answers live semantic questions about an open file through a language server. Nothing answers the persistent question — what functions exist in this tree and where — without a server running, a file open, or a grep over the whole repository. Port `yesitsfebreeze/splinter` as `index.ctg`: a function-level index of the source tree, kept in sync with the files it indexes.

The index is the cheap half of code location: a name-to-location answer that costs no language server and no full-text scan. It does not replace `lsp.ctg`, which answers what a symbol means; it answers where symbols are, across a tree, including files nothing has opened. Sync is bidirectional in upstream: verify at port time what that costs and keep only the direction the composition needs.

## Acceptance

- [ ] Indexing a fixture tree records every function with its file and line, and a query by exact name and by prefix returns those locations.
- [ ] Editing a file updates that file's entries without reindexing the tree, and deleting a file removes its entries.
- [ ] A query against a tree that has never been indexed reports that, rather than answering empty as though the tree held no functions.
- [ ] The index reports its own staleness: a file changed on disk since it was indexed is named as stale in the query result, not answered as current.
- [ ] Index, query, incremental update and staleness are tested offline in `just test index` against a fixture tree.

## Proof and recovery

Port from `yesitsfebreeze/splinter`, which has no local checkout; clone at port time and record the revision. Survey observations to re-verify: Rust, described as an MCP server providing a function-level code index with bidirectional sync. Confirm at port time whether the MCP surface is the whole product or a wrapper over an indexing library — the composition wants the library and exposes it through `mcp.ctg`, not a second MCP server.

Sequencing note: `lsp.ctg` is already in the composition, so overlap is decided before implementation, not after. If the port's only advantage over the existing surface is persistence across sessions, record that as the reason and keep the surface minimal.

Gates, cwd `/Users/feb/dev/cartridge`: `just test index`, `just check index`. Not run for this plan.
