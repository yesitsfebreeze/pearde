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

# wire `Client::for_eval` and `with_temperature` to a real setting so completions stop sampling at the server default, or delete them

## Do

`nothing-seeds-the-completion-client` measured it: `seed` and `temperature`
are carried on `Client`, put on the wire on both the native-Ollama and
OpenAI paths, and set by `for_eval(seed)` and `with_temperature(t)` — which
nothing calls. Every completion this repo makes is a draw at the server's
default, which is why `insights-prompts-are-the-experiment`'s two fixed
prompts vary between runs and [reconcile-the-ground-number](../reconcile-the-ground-number/prd.md) had to reproduce
0.735 by repetition rather than by construction.

Two uncalled exported functions are a frontier-law deletion
([[SYSTEM]]). Deleting is the wrong half here: the knob is built, plumbed to
both wire formats and named `for_eval` for exactly this. The work is to call it.

Decide first, because the answer sets where the edit lands: a `[reason]` config
key beside `timeout_secs`, an env var, or a CLI flag. A key is the shape
`with_timeout_secs` already uses, and `config.rs` is where the other reason
settings live.

Then apply it at every construction site or none — a seed on four of six paths
is worse than no seed, because a run would be reproducible only when it happened
to take the right path. `rg -n 'Client::new\(' src` gives them:
`src/commands/src/lib.rs`, `commands_graph_ops.rs`, `commands_ingest_cmd.rs`,
`commands_ask.rs`, `commands_intake_cmd.rs`, `commands_query.rs`.

`memory-bench` is not one of them: it posts chat over its own `chat()` helper
rather than through `llm::Client`, so the answer LLM and the judge need their
own pass and are not in this item's scope.

## Acceptance
`rg -n 'for_eval|with_temperature' src` shows a caller for each outside
`llm.rs`, every `Client::new(` site routes through it, and `just all` is green.

**Done 2026-09-06.** `ReasonConfig` gains `seed: i64` and `temperature: f64`,
the `[reason]` key shape the `Do` recommended and the one `timeout_secs`,
`num_ctx` and `keep_alive` already use. All six sites route through one
`with_reason_sampling(client, cfg)` (`src/commands/src/lib.rs:669`) — reached
from `server_llm_client` and from the five direct constructions in
`commands_ingest_cmd`, `commands_query`, `commands_intake_cmd`,
`commands_graph_ops` and `commands_ask` — so it is all six or none, never four.

The two sentinels differ, and that is the one design decision inside what looked
like plumbing. `seed = 0` is unset, one lost value out of 2^63, matching the
convention above it. `temperature` is unset **below** zero rather than at it,
because 0.0 is exactly what a caller wanting determinism asks for: making 0.0
the sentinel would have put the single most useful setting out of reach. Held by
`reason_sampling_is_unset_by_default_and_zero_temperature_is_a_real_setting`,
which parses `temperature = 0.0` from a toml and asserts it survives as a
setting rather than an absence. Suite 1,242 passed.

Nothing surfaces the setting. `health` and `doctor` report neither, so a seeded
run and an unseeded one are indistinguishable from outside — the fourth question
of `should-the-reasoner-be-seeded-by-default`, and true of this wiring as it
stands rather than only of the default.

The Check first written here also asked that two runs of `memory insights` over an
unchanged store produce identical text. That was wrong for this item: it holds
only if seeding is on by default, and defaulting it is a product decision about
what memory does out of the box, which nothing in the `Do` authorises. Wiring a
knob and choosing its default are two pieces of work; the second is
`should-the-reasoner-be-seeded-by-default`.
