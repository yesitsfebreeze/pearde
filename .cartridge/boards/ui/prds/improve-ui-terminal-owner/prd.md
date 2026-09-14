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
canonical-scope: improve-ui-terminal-owner
needs:
- '@pty/improve-pty-input-ownership'
footprint:
- /Users/feb/dev/cartridge/tui.ctg/ui/index.ts
- /Users/feb/dev/cartridge/tui.ctg/ui/palette.tsx
- /Users/feb/dev/cartridge/tui.ctg/ui/activity.ts
- /Users/feb/dev/cartridge/tui.ctg/src/chat.ts
- /Users/feb/dev/cartridge/tui.ctg/tests/transcript.test.tsx
- /Users/feb/dev/cartridge/tui.ctg/tests/palette.test.tsx
---

# Display shared terminal ownership and cwd

Render the PTY service's lease ID/revision, owner, cwd and foreground phase. At command submission, use the same revision in input admission; stale display is informational and never permission. Human preemption behavior follows the settled PTY contract.

## Acceptance

- [ ] Cwd and lease transfer update visible state; a command submitted against an old revision is refused even if the old status was just painted.
- [ ] Disconnection/unknown foreground phase cannot appear ready; nvim and busy-shell preemption never receive an unintended command.
- [ ] UI reload preserves the PTY and keyboard focus and reconnects to current ownership rather than replaying input.

## Proof and recovery

Start at [index.ts](../../../../../../ui.ctg/ui/index.ts), [palette.tsx](../../../../../../ui.ctg/ui/palette.tsx), [activity.ts](../../../../../../ui.ctg/ui/activity.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-ui-terminal-owner`; maximum five rounds.
