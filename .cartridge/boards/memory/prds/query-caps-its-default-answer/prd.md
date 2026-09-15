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

# `query` with no `k` falls back to `seed_k` and returns 25 entities carrying their whole text — 198,944 characters measured, past any context window, for the one read an agent makes most

## Do

`tool_query` takes `let k = if p.k == 0 { rcfg.seed_k } else { p.k };`
(`src/rpc/src/server.rs:564`), and `seed_k` is 25. Each answered entity carries
its full `text`, not a passage: measured 2026-09-06 over this repo's store,
`query {text: "why is the delivery floor default 0.0"}` answered 198,944
characters — 163,156 of them entity text, 6,526 per entity — which the agent
host refused and spilled to a file. The graph already holds the same complaint
from an earlier session: *"The `k` had to be sent: the tool defaults to
`seed_k`"*.

**The 6,526 figure is wrong, and the way it is wrong is the lesson**
(`one-reading-is-not-a-measurement`). The arithmetic was right — 198,944 over
25 really is 6,526 — but the referent was not: that is the whole entity object,
not its text. `base_entity_json` (`src/retrieval/src/id_detail.rs:137`) has
truncated `text` to 500 characters for as long as that file has existed, so no
entity can carry more.

Re-measured 2026-09-06 by piping two JSON-RPC lines through `memory mcp` and
reading the payload with a script, which is how a 202,901-character answer gets
counted without being read: 25 entities, **entity text 4,787 characters total**
— 191 average — chains 927, and **edges 150,062 across 477 of them**, one hub
entity carrying 394 edges and 124,325 characters by itself. Three quarters of
the answer is edges. There is no CLI path to this number; `memory query` prints
its own rendering, not the wire payload.

Two changes, both in `tool_query`: give the tool surface its own default `k`
— small, 5 — so the seed width of the walk stops being the answer width of the
read; and cap the `text` each entity carries to a leading window, with the full
text still reachable through `{id}`. `seed_k` keeps its meaning inside
retrieval; only what leaves through the socket is bounded.

The bound belongs to the operation, not the caller: the CLI and `memory mcp`
both reach `tool_query`, so a cap written in one adapter would leave the other
caller unbounded.

**Done 2026-09-06.** `QUERY_DEFAULT_K = 5` and `QUERY_MAX_EDGES = 12` in
`base_constants.rs`, both carrying the measurement as their comment. The edge
cap sorts strongest-first before it cuts — an unordered cut would drop the
evidence and keep the noise, which is the half a reviewer would not see in the
diff. Capping the per-entity text was not needed and would have changed
nothing.

Measured again through the same `memory mcp` path after installing: a bare query
answers **13,439 characters, 5 entities, 23 edges**, down from 202,901; `{k:
25}` still answers 25 entities at 52,285 characters. Held by
`a_default_query_bounds_both_its_width_and_its_edges`
(`src/rpc/src/tests/server_query_test.rs`) over a 30-neighbour hub fixture; the
suite read 1,233 passed.

## Acceptance
Against a live daemon, `query {text: "why is the delivery floor default 0.0"}`
with no other argument answers under 32,000 characters, and
`query {text: ..., k: 25}` still answers 25 entities. A test in
`src/rpc/src/tests/` asserts both the default count and the per-entity text
bound over a fixture whose entities are longer than the window.
