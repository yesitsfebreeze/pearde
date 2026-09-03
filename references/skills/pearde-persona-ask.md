---
name: pearde-persona-ask
description: Put one problem to one persona and talk to it until the question is settled — a named colleague with a field, a bias and a way of reading, answering in their own voice and writing nothing. Use for "/pearde-persona-ask", "ask <id> <question>", "what would the skeptic say", "get a second opinion on this", "review this as a designer", "poke holes in this", "sanity check this decision".
---

Read @references/parts/consult.md — the unprompted-call table, never the one
you are wearing, why a call is a conversation and not a form, what a call
cannot do, and how to relay it. The roster is @references/personas/INDEX.md,
the scope is `@@consult`.

```bash
python3 @resources/pearde.py brief --consult <id> --question "<q>" [--transcript <path>]
```

Call one on your own judgment, not only when the user asks — reaching a
colleague is ordinary work, the way dispatching a worker is.

No board is needed: a call is a conversation, not a state change. No persona
for the field? Run `pearde-persona-create` first, then ask.
