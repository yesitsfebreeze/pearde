---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# every [[name]] in a part's body becomes one link edge at fold time

From [fold-parts-into-the-graph](../fold-parts-into-the-graph/prd.md). Needs
[node-source-reads-frontmatter](../node-source-reads-frontmatter/prd.md).

## Do
At fold time, extract every `[[name]]` from a part's body and create one
`link` edge per link, reason text `wikilink`, at asserted confidence. The
edge is vectored by its endpoints, never by the reason text
(`a-link-is-vectored-by-its-endpoints`). A link whose target is not yet
folded resolves on the target's arrival, never as a dangling edge — the
`memos-check` gate already proves every `[[name]]` resolves to exactly one
file, so an unresolved link means the target has not been read yet, not that
it is missing.

## Acceptance
`just build && just check && just test` green. After a full fold,
`memory query` on a part that links another returns the target within the top
five through the edge alone, and the edge count matches the wikilink count
that `grep -o '\[\[' memos/` reports.

Landed 2026-09-05 in `1fc09cc`. `ingest_wikilinks.rs` holds the extractor,
the leaf-name rule (a part is named the same whether it arrived as a watched
path or a `memos/<rel>` intake session id) and the fold; `place_document`
calls it inside the write lock that placed the entity, on the fresh path and
on the dedup path both. Two things the drill did not foresee: a part chunks,
so only the entity carrying the whole body is an endpoint — before that rule
24 parts made 61 edges where 40 links exist — and the fold had to run on the
merge, or a record written before this existed could never be folded at all.
Measured in an isolated store over `durable/core`: 40 wikilink edges, 40
distinct endpoint pairs, against 40 in-subset pairs computed from the files
independently; a query naming one part returns the parts it links at ranks 2
and 4.

