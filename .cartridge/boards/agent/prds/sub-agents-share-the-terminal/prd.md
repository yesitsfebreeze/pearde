---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: sub-agents-share-the-terminal
needs:
- '@sessions/sub-agent-sessions-record-parent-and-mailbox'
- '@agent/the-agent-spawns-wakes-and-owns-sub-agents'
- '@ui/the-panel-switches-to-a-sub-agent'
- '@sessions/the-swarm-talks-on-a-board'
- '@agent/the-run-is-a-stream-of-typed-events'
---

# sub-agents-share-the-terminal

The agent spawns sub-agents that report back through a mailbox, the terminal view shows and switches between them, and the visible shell stays owned. Per decision `the-agent-surface-preserves-the-visible-shell`, collaboration is exposed through discoverable declared events, never hidden execution tools. This parent coordinates the children; it is not implementation work.

## Acceptance

- [ ] Each linked child passes its own review and acceptance.
- [ ] Integration: in a disposable profile a parent spawns two children that run concurrently, a child's shell request routes through the parent's PTY input lease, the panel switches between them, and both reports land in the parent transcript; the user's PTY and editor stay intact.
- [ ] Two children editing one workspace are serialized by their owner, or the gap is recorded as a named limitation with its reproducing fixture.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [sub-agent-sessions-record-parent-and-mailbox](../../../sessions/prds/sub-agent-sessions-record-parent-and-mailbox/prd.md) — done
- [the-agent-spawns-wakes-and-owns-sub-agents](../the-agent-spawns-wakes-and-owns-sub-agents/prd.md) — carries the `@pty/improve-pty-input-ownership` lease prerequisite
- [the-panel-switches-to-a-sub-agent](../../../ui/prds/the-panel-switches-to-a-sub-agent/prd.md) — `ui` board, source now `tui.ctg`
- [the-swarm-talks-on-a-board](../../../sessions/prds/the-swarm-talks-on-a-board/prd.md)
- [the-run-is-a-stream-of-typed-events](../the-run-is-a-stream-of-typed-events/prd.md)

## Integration gate

After the children pass and the agent is ported to declared events (no PRD yet), from `/Users/feb/dev/cartridge`: `just test agent`, `just test sessions`, `just test tui`, `just smoke`. Not run for this plan.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
