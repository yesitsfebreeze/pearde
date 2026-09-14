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
canonical-scope: the-gutter-shows-both-sides
needs:
- '@ui/the-ui-paints-the-grid'
---

# A two-column gutter marks each command block's shell and agent state

`pty` already records command blocks with absolute rows (`commands`, pty.ctg `src/marks.rs`), but the shell pane draws no per-command indicators; the only gutter in tui.ctg is the accent bar `markdownToAnsi` puts on agent text (`ui/markdown.ts`). This leaf paints a two-column gutter beside the painted grid: one column for the shell's result, one for the agent's work on that command. Agent events keep the command ID observed at dispatch; sticky placement is derived from visible block ranges. One glyph table with distinct no-colour glyphs.

## Acceptance

- [ ] Running, success, failure and alternate-screen shell states, and agent working, waiting, reply and error states, stay distinct with colour disabled.
- [ ] Resize, mid-block scrolling and aged-out block starts never move an indicator onto the wrong command; a block without identity renders an explicit unknown glyph.
- [ ] Transcript and shell views share the same attribution without writing into PTY contents, and UI reload rebuilds the same indicators from `pty` and `agent` state.

## Proof and recovery

Start at [terminal.tsx](../../../../../../tui.ctg/ui/terminal.tsx), [markdown.ts](../../../../../../tui.ctg/ui/markdown.ts), [pty marks.rs](../../../../../../pty.ctg/src/marks.rs). First probe: record a `commands` payload with rows for two fixture commands at the current pty revision. Extend `term.test.ts` and `transcript.test.tsx` in `tui.ctg/.cartridge/tests/integration/`. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`. Not run for this plan. The gutter is additive; hiding it restores today's pane with no state loss.

## Dependencies and review

Hard need: [the-ui-paints-the-grid](../the-ui-paints-the-grid/prd.md) for row-addressed painting. Parent: [the-gutter-is-the-boundary](../the-gutter-is-the-boundary/prd.md). Shared footprint: `ui/terminal.tsx`. [Review history](review.md): rounds 1–4 used.
