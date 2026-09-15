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
- "live.ctg/src/control.ts"
needs:
- the-gates-are-green-at-one-pinned-set-of-shas
---

# The orchestrator sees and talks to its workers

## Outcome

A running worker is observable and addressable from the orchestrator's run: its screen, its proxy activity, its PRD state, its posts; and text can be sent to it.

## Acceptance

- [ ] `live_agent status {id}` returns phase, the last 40 lines of `tmux capture-pane`, the proxy's last request time, the PRD state and claim, and the worker's own `sessions post` lines.
- [ ] `live_agent send {id, text}` types into the worker's window (`tmux send-keys`); `cancel` sends C-c, waits a bounded time, then kills the window.
- [ ] A worker's `sessions post` to the orchestrator's channel is drained into the orchestrator's next turn as a user-role message with sender and time, exactly once across a host restart.
- [ ] Test: a scripted worker in tmux echoes what it receives and posts once; the run sees both, under `just test live`.

## Folds

Deferred with `superseded-by` pointing here:

- @agent/sub-agents-share-the-terminal
- @agent/a-live-run-accepts-events-from-outside
- @sessions/the-agents-chat-through-one-tool

## Result

Not started.
