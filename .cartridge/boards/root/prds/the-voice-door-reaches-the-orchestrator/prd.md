---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 4
date: "2026-09-15"
footprint:
- "live.ctg/src/server.ts"
- "auth.ctg"
needs:
- the-repository-answers-by-text
---

# The voice door reaches the orchestrator

## Outcome

Speaking to the page live serves produces the same delegation the text door does.

## Acceptance

- [ ] The page at `/?conversation=` holds the microphone, opens `auth.live` on the discovered OpenAI credential, and a spoken request produces a `delegate`; transcript fragments land in the store.
- [ ] `auth.ctg` test: a fake realtime endpoint replays a scripted event stream and one delegation results; one manual run against real GPT Live is recorded in Result with date and model.

## Result

Not started.
