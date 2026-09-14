---
repo: /Users/feb/dev/cartridge/tui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: ui
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: the-panel-switches-to-a-sub-agent
needs:
- '@agent/the-agent-spawns-wakes-and-owns-sub-agents'
---

# the-panel-switches-to-a-sub-agent

Bind the selected transcript/composer and unsent draft to an explicit session ID. Switching never transfers approval authority or shell ownership. A child ending or disappearing while selected yields a readable terminal state and an explicit route back to the root.

## Acceptance

- [ ] Two children retain separate drafts/transcripts across repeated selection and UI reload.
- [ ] A message or approval submitted after a switch targets the visible session and exact invocation, or is refused if stale.
- [ ] Child completion/removal and narrow keyboard navigation preserve focus and the foreground editor's grid/cursor/size.

## Proof and recovery

Start at [chat.ts](../../../../../../ui.ctg/src/chat.ts), [modules.ts](../../../../../../ui.ctg/src/modules.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [the-sidebar-slides-over-the-shell](../../../../memos/work/root--the-sidebar-slides-over-the-shell.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-panel-switches-to-a-sub-agent`; maximum five rounds.
