---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/live.ctg"
needs: ["voice-runs-headless-on-the-microphone"]
footprint: ["src/**", "mcp/**", ".cartridge/**", "cartridge.json", "init.lua"]
---

# A Claude session is the voice delegate

## Outcome

GPT Live and a Claude Code session work as one coworker in one conversation.
GPT Live hears and speaks; when it delegates, the task goes to an attached
Claude session instead of `agent.ctg`, carrying the transcript that led to it.
The Claude session answers a task, or speaks up on its own (a PRD finished, a
question), and GPT Live says it. With no Claude session attached, delegation
falls back to `agent.ctg` as today.

## Acceptance

- [ ] `live {op:"watch", conversation}` streams one line per delegated task (`task <id>: <user words> (live said: …)`) and marks the conversation as having an attached delegate while the stream is open.
- [x] `live {op:"reply", conversation, text, task?, quiet?}` sends `session.commentary.append` (or `thinking` when quiet) tied to the task, or unprompted when `task` is absent; the task is recorded done with that text.
- [x] Delegations arriving with no watcher attached run on `agent.ctg` exactly as before; a watcher detaching mid-task hands pending tasks back to `agent.ctg`.
- [ ] `live-mcp` exposes `watch`/`reply`; an offline test runs a mock voice session, a watcher, and a reply end to end.
