---
kind: work
level: 10
status: done
description: the local embedding server runs one slot and hangs rather than queues — eight concurrent embeds all timed out at 180 s where eight serial ones took 12.15 s, so memory must hold the only queue
read_when: "touching any embed call, or debugging a hung read"
---

# embeds-go-through-one-lane

Landed 2026-09-06: one `tokio::sync::Semaphore` of one permit in `llm::Client`'s
`Inner` (`src/llm/src/llm.rs`), taken by `Client::lane()` and held across every
`/api/embed` post — `embed_batch` and `embed_single`, so both the OpenAI-compat
and the Ollama-native URL go through it, and `embed`'s single-text retry takes
its permit only after the batch released one, so the two never nest. The
permit lives behind the `Arc<Inner>` every clone of a client shares, so the
fourteen daemons' clones of one client queue against each other and not each
against itself. Width is the constant 1 and not a config key: the measurement
above is that the server forces `-np 1` for an embedding model and no setting
buys a second slot, so a knob here would be a knob for a value that never
changes. Making it configurable is two lines in `src/commands/` — the builder
chains at `lib.rs:723` and `commands_ingest_cmd.rs:69` that already pass
`[embed] num_ctx` and `keep_alive` — the day a server offers more.

`concurrent_embeds_queue_behind_one_lane` in `src/llm/src/tests/llm_test.rs` is
the Check: 8 `tokio::spawn`ed `embed` calls through one `Client` against an
axum stub that counts anything in flight beside itself and sleeps 20 ms to make
an overlap visible. All 8 answer, the stub counts zero overlaps, in 0.20 s.
Red-proofed by widening the permit to 8 — the test fails, so it is testing the
lane and not the stub.

## Do

Measured 2026-09-06 against `qwen3-embedding:0.6b` on this machine, model
resident, 100% GPU:

```
8 serial embeds:   12.15 s  -> 0.7 embeds/s
8 parallel embeds: all eight timed out at 180 s
```

The damage outlives the requests. After those eight aborted, every later embed
— one word, one caller, an idle box — timed out at 60 s and then at 120 s. The
slot never recovered on its own; `ollama stop qwen3-embedding:0.6b` cleared it,
and the very next embeds answered in **1.08 s cold and 0.018 s warm**. So the
server is not slow, it is wedged: one round of concurrency costs every caller
the embedding service until a human unloads the model.

Ollama 0.33.3 launches the embedding model as
`llama-server … -c 2048 -np 1 -b 2048 -ub 2048`. Setting
`OLLAMA_NUM_PARALLEL=8` does not change it: the server's own config line logs
`OLLAMA_NUM_PARALLEL:8` and the child still gets `-np 1`, so a single slot is
forced for embedding models and no machine setting buys a second one. A caller
that issues concurrent embeds does not get slower service, it gets none — the
requests wedge, and with one slot a wedged request stops every other caller of
the box, recall included. That is what an agent session measured earlier the
same night as `query` hanging past 120 s on the word `probe`.

memory issues embeds from many places at once: `commands_query.rs:80,129,289`,
`server.rs:526,2052`, `ingest_worker.rs:694,723`,
`src/commands/src/commands_focus.rs:59`,
`src/commands/src/commands_unnamed.rs:62`,
plus the keepalive at `lib.rs:1354` — and fourteen daemons were holding this
store at the time ([[@prd/work/memory--one-daemon-per-store.md]]), each with its own tick and drain.

Put one lane in `llm::Client` (`src/llm/src/llm.rs`): a `tokio::sync::Semaphore`
of one permit — width from config, so a server that ever offers more slots is a
config change and not a code change — held across every `/api/embed` call, both
`embed` and `embed_batch`. Every caller then queues inside memory, where a queue
is visible and bounded, instead of inside a server that answers a queue by
hanging. `embed_batch` already sends many inputs in one request
(`llm.rs:341`), so batching stays the way to go faster; the lane only stops
memory from asking for a concurrency the server does not have.

## Check

A test drives 8 concurrent `embed` calls through one `Client` against a stub
that fails if it ever sees two requests in flight, and all 8 answer. Against
the real box, 8 concurrent `query` calls all return, none past 30 s.
