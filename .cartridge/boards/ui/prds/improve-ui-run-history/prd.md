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
canonical-scope: improve-ui-run-history
needs:
- '@sessions/improve-sessions-recovery'
footprint:
- /Users/feb/dev/cartridge/tui.ctg/ui/index.ts
- /Users/feb/dev/cartridge/tui.ctg/ui/palette.tsx
- /Users/feb/dev/cartridge/tui.ctg/ui/activity.ts
- /Users/feb/dev/cartridge/tui.ctg/src/chat.ts
- /Users/feb/dev/cartridge/tui.ctg/.cartridge/tests/integration/transcript.test.tsx
- /Users/feb/dev/cartridge/tui.ctg/.cartridge/tests/integration/palette.test.tsx
---

# Reopen completed run evidence after closing the panel

The chat pane keeps one transcript in `ui.state("transcript.v1")` (tui.ctg `ui/index.ts`), which survives module replacement but is not read back from the `sessions` owner, so a past run cannot be reopened after a restart. This leaf lets a user pick a completed run and read its prompts, replies and tool outcomes from the session record while the shell stays in front.

## Acceptance

- [ ] After a fixture run completes, closing and reopening the panel and restarting the UI process show the same transcript order and tool outcomes, read from `sessions`.
- [ ] A run whose history the owner no longer retains shows an explicit "history unavailable" state, never an empty success.
- [ ] Opening history while nvim holds the alternate screen keeps the grid and cursor, and it works at 80 columns with keyboard only.
- [ ] Disabling the history view leaves the PTY open and deletes no session data.

## Proof and recovery

Start at [index.ts](../../../../../../tui.ctg/ui/index.ts), [palette.tsx](../../../../../../tui.ctg/ui/palette.tsx), [activity.ts](../../../../../../tui.ctg/ui/activity.ts), [chat.ts](../../../../../../tui.ctg/src/chat.ts). First probe: record which `sessions` op returns a completed run's events at the current sessions.ctg revision. Extend `transcript.test.tsx` and `palette.test.tsx` in `tui.ctg/.cartridge/tests/integration/`. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`. Not run for this plan. Session and PTY state stay with their owners; the UI only reads.

## Dependencies and review

Hard need [@sessions/improve-sessions-recovery](../../../sessions/prds/improve-sessions-recovery/prd.md) is done. Shared footprint with the other [improve-ui-programme](../improve-ui-programme/prd.md) leaves. [Review history](review.md): rounds 1–4 used.
