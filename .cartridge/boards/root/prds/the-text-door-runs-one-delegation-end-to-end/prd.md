---
state: open
origin: requested
priority: 88
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 3
date: "2026-09-15"
footprint:
- "live.ctg tests"
- ".cartridge/memos/routine/cartridge-smoke.md"
needs:
- a-worker-launches-in-tmux-through-the-proxy
- the-orchestrator-sees-and-talks-to-its-workers
- the-orchestrator-knows-what-is-in-the-works
---

# The text door runs one delegation end to end

## Outcome

One sentence to the host becomes one worker, one result and one report, with no UI.

## Acceptance

- [ ] `cartridge call live '{"op":"delegate","prompt":"work PRD X"}'` starts an orchestrator run that spawns one tmux Claude worker for X, waits, reads its result, and `live state` shows the task `completed` with the worker's output; the same through the `live` MCP tool from a Claude Code client.
- [ ] Runs under `just test live` with the fake provider and a scripted worker; no network.

## Result

Not started.
