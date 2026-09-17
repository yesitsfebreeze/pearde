---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/health.rs"
- ".cartridge/tests"
---

# a route that refuses reasoning keeps answering without it

## Outcome

A route that does not support a reasoning control answers the turn without it
rather than refusing the turn. Every spelling of the control — `thinking`,
`reasoning`, `reasoning_effort`, `output_config.effort` — is dropped together,
because they are one request feature wearing three wire names.

## Evidence

Measured on 2026-09-16: 3 routes, two distinct failures that are the same
thing.

```
granite-router-latest@ollama   4 attempts   "granite-router:latest" does not
granite4-3b@ollama             4 attempts   support thinking
gpt-4.1-nano@openai            3 attempts   Unrecognized request argument
                                            supplied: reasoning_effort
```

The thinking half is already handled: `thinking_refused` matches the ollama
wording, `thinking` is in `DROPPABLE`, and `strip_refused` correctly clears
`reasoning` and `output_config.effort` alongside it. Those two routes still
carry an open incident, so the same-turn path is either not reached or the
rule is not persisted — the first thing this PRD establishes is which.

The effort half is unhandled outright. `reasoning_effort` is not in
`DROPPABLE`, and OpenAI's `Unrecognized request argument supplied: X` wording
is not one of the two forms `refused_field` parses. The value is also not the
caller's: `proxy.rs` `attempt` sets `reasoning_effort` itself, from the
policy's effort entry, on any `auto` request to a route whose caps claim
reasoning. So the router adds a parameter the route rejects and then cannot
learn to stop.

## Acceptance

- [ ] `refused_field` parses `Unrecognized request argument supplied: X`
      alongside the two forms it already parses.
- [ ] `reasoning_effort` and `reasoning` are droppable, and dropping any one of
      the reasoning spellings drops all of them, as `thinking` already does.
- [ ] The router stops adding an effort the route refuses, rather than
      re-learning the drop each turn. Answered by the recorded rule rather than
      by editing the route's caps: the rule removes the field on every later
      turn, and a second place that also decides whether a route reasons is
      exactly the drift the vision's fifth law forbids.
- [ ] A test reproduces the live state: the two ollama routes and the
      `gpt-4.1-nano` route each answer on retry after one refusal.
- [ ] The existing thinking path is proven end to end rather than by
      inspection — the open incident on both granite routes is explained.
      Answered: the same-turn strip worked and the durable rule did not. Once
      recovery persisted `drop: {thinking}`, the guard in `attempt` saw
      `thinking` change and refused the route with a 400 before the request
      left the process, so every later turn failed where the first had
      recovered. Fixed by
      [[an-adaptation-that-preserves-meaning-is-not-refused-as-a-waiver]].

## Planning note

2026-09-16. Filed from [[@router/system/vision.md]]. The effort case is the one
that indicts the router most directly: it rejects a parameter the router itself
added.
