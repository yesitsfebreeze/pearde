---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
blast-radius: low
workflow: develop-one-cartridge
work-kind: leaf
review-round: 1
review-status: passed
---

# A ranked fabric query answers within its bound, or is retired as already fixed

Reported before the port: `cartridge_memo {op:"landscape", query}` hung until the 600000 ms MCP tool timeout while plain landscape and `op:"resolve"` returned. Since then the op is `fabric` (`memo.ctg/src/service.rs`; the host rewrite cartridge.ctg `939e7d1` removed the core graph, fabric and evidence modules) and memo.ctg `1d2fa92` ported memo to the transport protocol, moving graph assembly into memo (`src/fabric_graph.rs`); the rename item is delivered. In current source the query-only work is `fabric_graph::search` and the `view::view` filter, both linear; the announce gather in `graph` runs for every call. Owner: memo.ctg.

## Acceptance

- [ ] Reproduce first at the current memo.ctg revision: `fabric` with and without `query` against the stand-in host `memo.ctg/.cartridge/tests/integration/host.ts`, recording revision and elapsed time. If neither hangs, record that evidence and recommend retiring this item.
- [ ] If it reproduces: the query call returns `hits` within 5 s in that fixture, with the same `graph` node and edge counts as the plain call.
- [ ] A `graph.announce` listener that never answers makes both calls return or fail within the host's `event_timeout_ms`, never the MCP timeout; cancellation still yields `cancelled`.
- [ ] Cursor paging and the `fabric response exceeds output cap` refusal are unchanged.

## Proof and recovery

Start at `memo.ctg/src/service.rs` (`fabric`, `graph`), `memo.ctg/src/fabric_graph.rs` and `memo.ctg/src/view.rs`; add the case to a test in `memo.ctg/.cartridge/tests/integration/` that uses `host.ts`. Gates from `/Users/feb/dev/cartridge`: `just test memo`, `just check memo`; not run for this plan. Live MCP reproduction is blocked for now: [release-status](../../../../../../.cartridge/memos/note/release-status.md) records the mcp smoke failing with `memo inactive`. Plain `fabric` stays the fallback; no durable state changes. Rehoming to the memo board is recommended.
