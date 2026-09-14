---
repo: /Users/feb/dev/cartridge/tui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: ui
work-kind: leaf
review-round: 4
review-status: passed
canonical-scope: the-panel-switches-to-a-sub-agent
needs:
- '@agent/the-agent-spawns-wakes-and-owns-sub-agents'
---

# The panel switches to a sub-agent

The chat pane binds one typed session in `ui.state("session.v1")` and one transcript (tui.ctg `ui/index.ts`); Ctrl+V already switches the pane between that session and the voice conversation without cancelling either (`channel`). Once the agent owns child sessions, this leaf extends that switch to children: the transcript and unsent draft bind to an explicit session ID. Switching never transfers approval authority or terminal control. A child ending or vanishing while selected shows a readable final state and a route back to the root.

## Acceptance

- [ ] Two fixture children keep separate drafts and transcripts across repeated switching and UI module replacement.
- [ ] A message or approval sent after a switch targets the visible session and exact run/call, or is refused as stale.
- [ ] Child completion or removal while selected keeps keyboard focus and the shell's grid, cursor and size; works at 80 columns with keyboard only.

## Proof and recovery

Start at [index.ts](../../../../../../tui.ctg/ui/index.ts), [chat.ts](../../../../../../tui.ctg/src/chat.ts), [terminal.tsx](../../../../../../tui.ctg/ui/terminal.tsx). First probe: record how `agent`/`sessions` expose child IDs and parent at the dependency's landed revision. Extend `transcript.test.tsx` in `tui.ctg/.cartridge/tests/integration/`. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`. Not run for this plan. Without child sessions the pane behaves as today; switching writes no session data.

## Dependencies and review

Hard need [@agent/the-agent-spawns-wakes-and-owns-sub-agents](../../../agent/prds/the-agent-spawns-wakes-and-owns-sub-agents/prd.md) is open. Context: [the-sidebar-slides-over-the-shell](../../../../memos/work/root--the-sidebar-slides-over-the-shell.md) is claimed by another worker. Shared footprint: `ui/index.ts`, `ui/terminal.tsx`. [Review history](review.md): rounds 1–4 used.
