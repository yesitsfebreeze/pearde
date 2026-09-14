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
canonical-scope: improve-ui-terminal-owner
needs:
- '@pty/improve-pty-input-ownership'
footprint:
- /Users/feb/dev/cartridge/tui.ctg/ui/index.ts
- /Users/feb/dev/cartridge/tui.ctg/ui/palette.tsx
- /Users/feb/dev/cartridge/tui.ctg/ui/terminal.tsx
- /Users/feb/dev/cartridge/tui.ctg/src/term.ts
- /Users/feb/dev/cartridge/tui.ctg/.cartridge/tests/integration/transcript.test.tsx
- /Users/feb/dev/cartridge/tui.ctg/.cartridge/tests/integration/palette.test.tsx
---

# Display shared terminal ownership and cwd

Today `pty` knows only a boolean user/agent control flag (`agent_control` in pty.ctg `src/main.rs`); the UI mirrors it through `term` `control` and the `control` field of `read` (`src/term.ts`, `ui/index.ts`), and cwd is fetched only when a session starts (`shellCwd` in `src/chat.ts`). Once the PTY lease contract lands, the UI shows lease ID and revision, owner, cwd and foreground phase, and submits commands against the revision it showed. A stale display is information, never permission.

## Acceptance

- [ ] Cwd change and lease transfer update the visible state; a command submitted against an old revision is refused even if that status was just painted.
- [ ] Disconnected or unknown foreground phase never appears ready; with nvim or a busy shell in front, preemption never delivers an unintended command.
- [ ] UI reload keeps the PTY and keyboard focus and reconnects to current ownership without replaying input.

## Proof and recovery

Start at [term.ts](../../../../../../tui.ctg/src/term.ts), [index.ts](../../../../../../tui.ctg/ui/index.ts), [palette.tsx](../../../../../../tui.ctg/ui/palette.tsx). First probe: record the lease fields `pty` returns at the dependency's landed revision. Extend `transcript.test.tsx` and `palette.test.tsx` in `tui.ctg/.cartridge/tests/integration/`. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`. Not run for this plan. If `pty` returns no lease fields, keep today's user/agent indicator; the UI holds no ownership state of its own.

## Dependencies and review

Hard need [@pty/improve-pty-input-ownership](../../../pty/prds/improve-pty-input-ownership/prd.md) is open and must pass its own review and land first. Shared footprint with the other [improve-ui-programme](../improve-ui-programme/prd.md) leaves. [Review history](review.md): rounds 1–4 used.
