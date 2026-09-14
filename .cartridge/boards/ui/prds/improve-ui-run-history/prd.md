---
repo: /Users/feb/dev/cartridge/tui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: ui
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-ui-run-history
needs:
- '@sessions/improve-sessions-recovery'
footprint:
- /Users/feb/dev/cartridge/tui.ctg/ui/index.ts
- /Users/feb/dev/cartridge/tui.ctg/ui/palette.tsx
- /Users/feb/dev/cartridge/tui.ctg/ui/activity.ts
- /Users/feb/dev/cartridge/tui.ctg/src/chat.ts
- /Users/feb/dev/cartridge/tui.ctg/tests/transcript.test.tsx
- /Users/feb/dev/cartridge/tui.ctg/tests/palette.test.tsx
---

# Reopen completed run evidence after closing the panel

A user can reopen a completed run's transcript and tool outcomes while the foreground terminal remains intact.

## Acceptance

- [ ] Complete a fixture run, close/reopen its panel and reload the UI: transcript ordering and outcomes remain available.
- [ ] Opening history during nvim/alternate-screen use preserves terminal grid/cursor and works at a narrow terminal width.

- [ ] Keep session/PTY state in their existing owners. New UI features can be disabled/reverted without closing the PTY or deleting history. Check module replacement, keyboard navigation and supported terminal widths.

## Proof and recovery

Start at [index.ts](../../../../../../ui.ctg/ui/index.ts), [palette.tsx](../../../../../../ui.ctg/ui/palette.tsx), [activity.ts](../../../../../../ui.ctg/ui/activity.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-ui-run-history`; maximum five rounds.
