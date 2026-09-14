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
canonical-scope: the-ui-paints-the-grid
---

# The shell pane paints the PTY-owned grid

The shell pane is still OpenTUI's `EmbeddedTerminalRenderable`, fed raw bytes by `pump()` through `term` `read` (tui.ctg `ui/terminal.tsx`, `src/term.ts`), so the UI runs a second emulator. `pty` already serves `screen`, `viewport`, `frame` and `scroll` from its own grid (pty.ctg `src/main.rs`). This leaf paints those frames instead. Input forwarding (`key`/`mouse`/`paste`/`focus`) is unchanged; deleting the old renderer belongs to [the-embedded-terminal-is-gone](../the-embedded-terminal-is-gone/prd.md).

## Acceptance

- [ ] Row, style, palette, cursor and wide-character fixtures paint the same final cells as `pty` `screen`, including after resize; a skipped frame generation forces a full `screen` resync, never stale row reuse.
- [ ] Real nvim (alternate screen) and UI module replacement keep screen, cursor and input semantics; the chat/shell split, palette and handoff header described in `tui.ctg/.cartridge/docs/README.md` are unchanged.
- [ ] A 120x40 continuous-redraw fixture over five paired runs shows no wrong or missing final cells and at most 20% median throughput regression; the report names hardware, toolchain and all samples, and an unmeasured environment stays unmeasured.
- [ ] When `frame` is unavailable or errors, the pane keeps the embedded renderer and shows that it is degraded.

## Proof and recovery

Start at [terminal.tsx](../../../../../../tui.ctg/ui/terminal.tsx), [term.ts](../../../../../../tui.ctg/src/term.ts) and [pty main.rs](../../../../../../pty.ctg/src/main.rs). First probe: record tui/pty revisions and a `screen`/`frame` payload from the existing `fixtures/shell`. Add fixtures to `tui.ctg/.cartridge/tests/integration/term.test.ts` and `transcript.test.tsx`. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`, plus `just test pty` if a pty op changes. Not run for this plan. The embedded renderer stays as the fallback until acceptance passes; no durable data changes.

## Dependencies and review

No hard `needs`. [pty-owns-the-terminal-grid](../../../../memos/work/root--pty-owns-the-terminal-grid.md) is done; [pty-encodes-input](../../../../memos/work/root--pty-encodes-input.md) is still `active` under its analyst although its ops are served and consumed, so confirm it before claiming. Shared footprint: `ui/terminal.tsx` with every UI leaf. [Review history](review.md): rounds 1–4 used.
