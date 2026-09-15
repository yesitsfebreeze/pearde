---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1d"
---

# Add bounded projections and pagination for direct-ID edges and history without hiding full content.

## Do

Extend direct-ID and history lookup arguments with a compact projection, explicit edge and history limits, and cursor-based continuation. Keep the complete thought text reachable and preserve the strongest-first default edge bound established by [query-caps-its-default-answer](../query-caps-its-default-answer/prd.md). Return truncation and continuation metadata so omission is visible. Use one shared projection for CLI and MCP paths rather than post-processing in each adapter.

**Done 2026-09-09.** `Projection` in `src/retrieval/src/id_detail.rs` — the one
resolver `memory get` and `query {id}`/`{ids}` both reach, so a cap in either
adapter could not leave the other unbounded. `edge_limit` (absent is
`QUERY_MAX_EDGES`, `0` is every edge), `edge_cursor`, `compact`; edges sorted
strongest-first with `util::cmp_rank` before the cut, the same order the ranked
path uses, so the cursor is total and walks each edge once. The row carries
`edges_total`, `edges_cursor` and `edges_more`, and `compact` — which omits
exactly the edge `text` and the thought text past 500 characters — says so with
`compact: true` and `text_truncated`. A default lookup still carries the whole
thought text.

`log` grew the same vocabulary through one `page` helper in `src/rpc/src/server.rs`:
`limit` (absent is `LOG_DEFAULT_LIMIT`, `0` is the whole record, as `memo list`
means it), `cursor`, and `total`/`cursor`/`more` on both the revision chain and
the machine feed, whose key is `id:change` because one thought enters it twice.
`total` beside `more` is what keeps an empty page from an exhausted cursor
distinguishable from an empty record.
`memory get --edges/--compact` and `memory log --cursor` reach the same projection,
and both printers show what was cut.

Five tests in `src/rpc/src/tests/server_bounded_test.rs` over one fixture — a
hub with thirty edges, a twenty-five deep Supersedes chain. `1489/1490` in the
lane; the one red is `memory::cited_paths`, which fails in every lane because
`src/rpc/src/plan.rs` cites a file only the trunk holds.

## Acceptance
Tests create a thought with enough edges and revisions to exceed one page. Default response remains bounded, compact mode omits only documented fields, cursors traverse every edge and revision exactly once, and an explicit full-content lookup still returns complete thought text. Serialized response size stays under a stated ceiling for default arguments.
