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

# a wedged embedding slot never heals on its own — every call after it times out until the model is unloaded by hand, and memory reports that as nothing at all

## Do

Measured 2026-09-06: after one round of concurrent embeds aborted
([embeds-go-through-one-lane](../embeds-go-through-one-lane/prd.md)), every subsequent embed against
`qwen3-embedding:0.6b` timed out — 60 s, then 120 s, from a single caller on an
idle machine with the model resident on GPU. `ollama stop
qwen3-embedding:0.6b` cleared it and the next embed answered in 1.08 s, the one
after in **0.018 s**. The service was never slow; it was holding a slot for a
request whose client had gone.

memory says nothing while this happens. A `query` blocks on
`llm::block_on_in_place(llm.embed(...))` and the caller waits; `health` reports
no LLM state at all, so the surface an agent checks first shows a healthy graph
while every read is dead. An agent session spent minutes concluding the store
was slow when the embedder had been wedged the whole time.

Two parts. Give the embed call a deadline — seconds, not none — so a wedged
slot fails a read instead of hanging it. And when a call passes that deadline,
recover the way the hand does: `POST /api/generate` with `keep_alive: 0` for
the embed model unloads it, and the next call reloads a clean slot. Count both
on the `degraded:` line beside the panics and failures, so a wedge that
happened is a number someone can read afterwards.

Landed. The deadline was not none, which is what made this invisible: every
embed post carried the same 120 s ceiling, read and bulk batch alike, and 120 s
of nothing is a hang to whoever asked. A read now gets `EMBED_READ_SECS` = 20
and a bulk batch keeps the 120 s a many-text post honestly needs
(`src/llm/src/llm.rs`). One funnel, `Client::embed_post`, carries all four embed
posts, so the recovery runs wherever the breach is first seen rather than on
the one path a ticket named: it counts the wedge, calls `unload_embed_model`
(`POST /api/generate`, `keep_alive: 0`, ollama-native only — `/v1` has no
unload verb), warns once naming the model, and returns `LlmError::EmbedWedged`,
which is transient, so `embed_one`'s existing single-text retry is the reload
of the clean slot.

The count rides the LLM leg's own chain, not the graph's: `Client::embed_wedges`
-> `health_stats` (`src/rpc/src/server.rs`) -> `HealthRes.llm_embed_wedges`
(`src/transport/src/memory_rpc.rs`) -> its own quiet-at-zero line in
`llm_health_lines` (`src/commands/src/commands_admin.rs`), beside the failed
completions. `graph.rs` Counters and `health/src/lib.rs` were left alone for the
reason `llm_complete_failed` already gives at its call site — a wedged embedder
is a property of this daemon's LLM leg, not of the graph.

## Acceptance
With a deliberately wedged slot, a `query` returns an error naming the
embedder within its deadline instead of hanging, the following `query` answers
normally, and `health` shows a non-zero embed-wedge count.

Run against a stub wedged the way the box was, not against the shared ollama —
wedging the real slot would have wedged every sibling lane and the running
daemon with it. `a_wedged_embedding_slot_is_unloaded_counted_and_named`
(`src/llm/src/tests/llm_test.rs`) serves an `/api/embed` that accepts the post
and answers nothing: `embed` comes back with `EmbedWedged` naming
`qwen3-embedding:0.6b` instead of hanging, and both breaches — the batch and
its single-text retry — are counted. The clock is paused, so the deadline
passes without the test spending it; that same pause is why the unload's own
round trip cannot land inside that test, and
`the_recovery_unloads_the_embed_model_with_keep_alive_zero` reads the body the
recovery posts instead. `llm_embed_wedges` round-trips through `HealthRes`
(`every_health_field_round_trips_through_json`) to the line `memory health`
prints.
