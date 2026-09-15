---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: claimed
deferred-on: "2026-09-15"
superseded-by: "@root/the-profile-is-the-orchestration-service"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: rollup
needs:
- "@ui/copy-mode-interacts-with-the-text"
- "@root/pty-owns-the-terminal-grid"
- "@root/pty-encodes-input"
- "@ui/the-ui-paints-the-grid"
- "@ui/the-embedded-terminal-is-gone"
---

# The pty cartridge is the terminal emulator; the UI paints its grid and forwards input

## Outcome

Terminal emulation moves from OpenTUI's native embedded terminal into the `pty`
cartridge, under [[the-agent-surface-preserves-the-visible-shell]]. `pty` holds the grid, the
scrollback, the viewport and the row of every mark, and it turns key and mouse
events into shell bytes. The `ui` cartridge paints rows and forwards events. A
user notices nothing: every program that worked keeps working, the host theme
still shows through, and the shell still survives UI replacement, now with its
scrollback intact rather than replayed.

Scope is the emulator, its wire to the UI, the painter and the removal of the
old path. Indicators beside the grid belong to [the-gutter-is-the-boundary](../../../ui/prds/the-gutter-is-the-boundary/prd.md); the latest-tool footer, main/dynamic status and composer/full transcript stay. No tool means no placeholder, and agent output never enters the shell stream.

## Acceptance
- [ ] Every child work memo listed in `subwork:` is done.
- [ ] Every test in `core/tests/test_shell.py` passes against the painted grid,
      including the real `nvim` passage and the resize delta.
- [ ] Replacing the `ui` cartridge shows the same scrollback without `pty`
      replaying its output ring; the marker written before the swap is still on
      screen after it.
- [ ] `zirkle run pty '{"op":"screen"}'` returns the rows the user is looking at.
- [ ] No reference to `EmbeddedTerminalRenderable` remains under `builtin/ui`.

- [ ] Ctrl+G/Ctrl+F/Escape preserve the running editor's size and cursor, while the latest-tool footer and dynamic status remain usable.

## Approach

Children in order: the emulator and its ops, input encoding, the painter behind
the existing `term` service shape so the view swaps in one commit, then the
cleanup that deletes the old path and rewrites the documentation.
