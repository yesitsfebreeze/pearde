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

# `ask` moves from a local CLI body into the dispatch table so any consumer reaches the reason model through the daemon — the think loop unchanged, `memory ask` a thin dispatch like every other verb

## Do

`src/commands/src/commands_ask.rs` runs the think loop locally — recall, the
alias turns, synthesis by `reason.model` (`dispatch`). The loop moves behind
a new `ask {question, context?}` arm in `rpc::Server::invoke`, where `context`
is an optional part body the answer must also cite; `memory ask` becomes a
dispatch to it and prints the same numbered facts. Refuses without a
`[reason]` model, as today. `who-writes-where` is not touched — `ask` writes
nothing.

## Acceptance
The existing `memory ask` canary (the BWS-abbreviation question cites the
Brackenwood facts or refuses) passes through the daemon; an `ask` frame with
a `context` body cites it as fact 0.

Done 2026-09-06: the think loop is `src/rpc/src/ask.rs` behind an `"ask" =>`
arm — recall through `tool_query`, the extract turns and the synthesis pass
through the daemon's own `llm::Client`, crossing to async with
`llm::block_on_in_place` as every other LLM-calling arm does. The prompt
builders, the variant parser and the union moved there too and
`commands_ask.rs` imports them, so the CLI's no-daemon body and the arm share
one prompt rather than two. `memory ask` now routes: `Done` prints the daemon's
answer, `Refused` prints the refusal, `NoDaemon` runs the local body. `context`
is fact `[0]`, ahead of recall, since it is the one fact the caller chose.
Checked by `tests/e2e/ask_loop.rs::the_ask_canary_answers_through_a_serving_daemon`
(the BWS canary against a daemon holding a store the CLI has been blinded to)
and two prompt tests in the rpc crate for the fact-0 numbering.
