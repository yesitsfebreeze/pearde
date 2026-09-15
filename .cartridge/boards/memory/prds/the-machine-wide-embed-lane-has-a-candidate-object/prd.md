---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
---

# the hub's cross-root search is the one process that sees N daemons about to embed the same text, so the permit the machine-wide constraint asks for belongs in that handler — one `query` invoke at a time, resolve and connect still concurrent

## Do

[[the-embed-lane-bounds-one-client-not-the-machine]] left one fan-out
uncovered: the hub's `search` (`src/hub/src/lib.rs:433-470`) builds a `JoinSet`
with one task per registered root, and each task invokes `query` on that root's
daemon with the *same* `req.text`. Each node embeds it —
`tool_query` reads `query_cache.embed_get(&p.text)` and, on a miss, calls
`llm.embed` (`src/rpc/src/server.rs:527-533`) — and that cache is a field of
`Server` (`server.rs:26`), so N daemon processes miss N times and post N
identical embeds at a one-slot Ollama. No in-process semaphore reaches across
processes, so `llm::Client`'s lane (`src/llm/src/llm.rs:151,197,381`) is one
permit *per daemon*, N of them.

N is measured, not assumed. `~/.local/state/memory/hub-roots.json` read
2026-09-07 holds **34 roots**, 33 of whose directories still exist — up from
the sixteen [[the-hub-registry-is-the-machine-inventory]] counted two days
earlier, because nothing but the reaper's `prune_missing` removes one and every
e2e run adds more ([the-e2e-harness-writes-the-real-machine-registry](../the-e2e-harness-writes-the-real-machine-registry/prd.md)). So
one `memory query --all` is today a fan of up to 33 concurrent embeds of one
string, against a server that answers concurrency by wedging
([embeds-go-through-one-lane](../embeds-go-through-one-lane/prd.md): 8 concurrent embeds all timed out at 180 s and
poisoned the slot until the model was unloaded by hand).

Serialising them is nearly free. Against the resident `qwen3-embedding:0.6b` on
this box, three serial embeds took **1.42 s, 0.028 s, 0.021 s** — so 33 serial
embeds of one text cost under a second, where the concurrent version costs
every caller on the machine its embedder.

The change: one `tokio::sync::Semaphore` of one permit as a field on
`HubRpcHandler` (`src/hub/src/lib.rs:206-216`, minted in `with_registry` at
`:245`), acquired inside each fan-out task around `client.invoke(...)` (`:468`, and
inside `search_root` once the extraction the legible lane holds in
[[hub-search-fans-out-in-a-closure-that-shares-nothing]] lands) and released
before the task returns. Not around the `handler.resolve`
above it: that is the cold-boot wait `spawn_locks` already makes per-root, and
holding a global permit across it would make every root pay the slowest one's
60 s spawn.

It bounds what the hub issues and nothing else — not the boot scan each fresh
resolve starts, not the tick embedder, not another memory on the box. The hub
cannot be the machine-wide queue while it sits in no other call's path
([[the-hub-is-a-proxy-for-exactly-one-operation]]); it can be the queue for the
one operation it does proxy, which is the sharpest of the three fan-outs
[[three-places-choose-concurrency-against-one-slot]] names and the only one
[[there-is-no-object-that-could-hold-the-embed-lane]] said had no object.

The other candidate — the hub embeds once and passes the vector — is not this
item. The hub crate has no `llm` dependency (`src/hub/Cargo.toml`), `[embed]`
`url` and `model` are per-project keys any root may set and the e2e harness
writes into every project it makes (`tests/e2e/harness.rs:184`), and a store is
dimension-locked on the model it was ingested with
(`src/config/src/config.rs:531`). One vector for every root is therefore wrong
until the roots are grouped by `(url, model)`, and `query` has no vector
argument, so that version is a wire change plus a new dependency. The permit is
five lines and needs neither.

## Acceptance
A hub unit test: three temp roots, each with a stub `MemoryRpc` handler
(`serve_memory_rpc`, three methods) bound at `Endpoint::memory_for(root)`
(`src/transport/src/typed.rs:343`) whose `invoke` counts what is in flight
beside it, sleeps 20 ms and answers; a `Registry::open(<tempfile>)` carrying
the three (`src/hub/src/hub_registry.rs:63,80`) behind
`HubRpcHandler::with_registry`; one `search` with `root: ""`, so the
caller-registration leg is skipped. All three roots appear in `hits` and the
stubs' peak concurrent invokes is 1. Red-proof by widening the permit to 3 —
the test fails, so it is testing the lane and not the stub.

`just check` green. `just test` is red only on `cited_paths` — eight
memo-to-code line citations that drifted under other sessions
([the-citation-gate-reads-code-and-not-the-record](../the-citation-gate-reads-code-and-not-the-record/prd.md)). None of them is in this
lane's diff. Corrected by the coordinator: the lane's agent stalled after
writing this line and before it could amend it.
