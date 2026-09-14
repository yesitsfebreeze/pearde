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
canonical-scope: copy-mode-interacts-with-the-text
needs:
- '@ui/the-ui-paints-the-grid'
---

# Copy mode acts on exactly the selected terminal text

Today a mouse drag copies OpenTUI's own selection through OSC 52 and `pbcopy` (`useSelectionHandler` in tui.ctg `ui/terminal.tsx`); there is no copy mode. This leaf adds one: it freezes a `pty` `screen`/`viewport` snapshot tagged with its frame generation, selects by grid cell with wide and combining characters handled, and offers three actions: copy, open a path, send a correction. Per [a-cartridge-brings-its-own-surface](../../../../../../.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md), tui names no memo or memory protocol: a correction is an event tui defines and any cartridge may answer.

## Acceptance

- [ ] Unicode and whole-command selections copy exact text; when scrollback has aged out part of the snapshot, copy mode says so instead of substituting current rows.
- [ ] Opening a path sends one shell-quoted literal argument through `pty` only while the user holds terminal control; shell syntax in the path runs nothing extra, and opening while a foreground program owns input is refused.
- [ ] A correction is sent with `gather` as one tui-defined event carrying the selected text and its snapshot anchor; each listener's outcome (answered, declined, failed, timed_out, unavailable) is shown under its cartridge name, and no listener shows "not delivered", never "saved".
- [ ] Escape leaves copy mode with the shell grid, cursor and input untouched; drag-to-copy still works.

## Proof and recovery

Start at [terminal.tsx](../../../../../../tui.ctg/ui/terminal.tsx), [wire.ts](../../../../../../tui.ctg/src/wire.ts) (`gather`) and [pty main.rs](../../../../../../pty.ctg/src/main.rs). First probe: confirm how a node defines an event and receives per-listener outcomes since cartridge.ctg `c9ef10b`; tui's `wire.ts` `gather` currently drops non-answers. Create `copy.test.tsx` in `tui.ctg/.cartridge/tests/integration/` with a fixture listener that answers and one that fails. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`, `just isolation`. Not run for this plan. Copy mode is additive and writes no data itself.

## Dependencies and review

Hard need: [the-ui-paints-the-grid](../the-ui-paints-the-grid/prd.md). Memo or memory listeners are their owners' work. Shared footprint: `ui/terminal.tsx`. [Review history](review.md): rounds 1–4 used.
