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
canonical-scope: the-embedded-terminal-is-gone
needs:
- '@ui/the-ui-paints-the-grid'
---

# The UI's duplicate terminal emulator is removed with consumer parity

Once the grid painter lands, tui.ctg drops `EmbeddedTerminalRenderable` and its raw-byte pump, consumer by consumer. Current consumers: the shell pane and `pump()` in `ui/terminal.tsx`, the `term` `read` long-poll in `src/term.ts`, and tests that assert the embedded renderable in `.cartridge/tests/integration/transcript.test.tsx`. `pty` `read` and `commands` stay for tools and other callers; only the UI's use is removed. Old probe deletions are history, not instructions.

## Acceptance

- [ ] `rg EmbeddedTerminalRenderable tui.ctg/ui tui.ctg/src` is empty and the shell pane renders only through `pty` grid ops.
- [ ] Real nvim, UI replacement, the chat transcript, palette and terminal handoff header (per `tui.ctg/.cartridge/docs/README.md`) behave the same on the grid renderer.
- [ ] Each removed API or test names its migrated consumer and the behavioural test that replaces it; no test is deleted only to satisfy a text search.
- [ ] `pty` `read` and `commands` still answer non-UI callers (agent shell tool readback) unchanged.

## Proof and recovery

Start at [terminal.tsx](../../../../../../tui.ctg/ui/terminal.tsx), [term.ts](../../../../../../tui.ctg/src/term.ts), [transcript.test.tsx](../../../../../../tui.ctg/.cartridge/tests/integration/transcript.test.tsx). First step: at recorded revisions, list every caller of `term` `read` and `EmbeddedTerminalRenderable` with `rg` across the composed root and keep that ledger in the spec. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`, `just test pty`. Not run for this plan. Land as its own commit after the painter; reverting it restores the embedded renderer without touching PTY state or history.

## Dependencies and review

Hard need: [the-ui-paints-the-grid](../the-ui-paints-the-grid/prd.md); stop if its fallback renderer is still in use. Shared footprint: `ui/terminal.tsx`. [Review history](review.md): rounds 1–4 used.
