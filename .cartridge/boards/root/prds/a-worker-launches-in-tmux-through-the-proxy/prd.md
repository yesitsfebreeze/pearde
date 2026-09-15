---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 3
date: "2026-09-15"
footprint:
- "live.ctg/src/store.ts"
- "live.ctg/src/coordinator.ts"
- "live.ctg/src/workers.ts"
- "router.ctg agents.claude preset"
- ".mcp.json"
- ".cartridge/memos/routine/tmux-*.md"
needs:
- the-gates-are-green-at-one-pinned-set-of-shas
---

# A worker launches in tmux through the proxy

## Outcome

The orchestrator can start a Claude Code worker in a tmux window, routed through this host's proxy, with cartridge tools over MCP, and keep a registry row for it.

## Acceptance

- [ ] `live_agent spawn {kind:"claude", task, prd?, cwd?}` runs `tmux new-window -d -n <task-id>` in the `cartridge` tmux session and starts `cartridge launch claude` there with `ANTHROPIC_BASE_URL` = this host's proxy and cwd = the PRD lane or the repo; the registry row holds tmux target, proxy session id, prd ref and phase.
- [ ] `.mcp.json` at the repo root gives every launched worker `cartridge mcp`; the worker's first request reaches the proxy with the injected context and the router's fake provider answers it, under `just test live`.
- [ ] Without tmux on PATH, spawn refuses by name; a worker whose window dies is `failed` with the window's last 40 lines in `error`.

## Folds

Deferred with `superseded-by` pointing here:

- @agent/the-agent-spawns-wakes-and-owns-sub-agents (external half)
- @root/zirkles-tools-serve-any-agent
- @root/an-mcp-server-carries-the-tools

## Result

Not started.
