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
canonical-scope: the-gutter-shows-both-sides
needs:
- '@ui/the-ui-paints-the-grid'
---

# the-gutter-shows-both-sides

Rebase row wiring onto the current painter and PTY block model. Agent events retain the command ID observed at dispatch; the renderer derives sticky placement from visible block ranges. Keep a single glyph table with distinct no-color fallbacks.

## Acceptance

- [ ] Running/success/failure/alternate-screen and agent working/waiting/reply/error states remain distinct without color.
- [ ] Resize, mid-block scrolling and aged-out block starts never move an event onto the wrong command; missing block identity renders unknown/blank explicitly.
- [ ] Transcript and shell views share attribution without modifying PTY contents, and UI reload reconstructs the same indicators from owner state.

## Proof and recovery

Start at [chat.ts](../../../../../../ui.ctg/src/chat.ts), [modules.ts](../../../../../../ui.ctg/src/modules.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-gutter-shows-both-sides`; maximum five rounds.
