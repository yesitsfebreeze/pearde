---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/pty.ctg"
---

# A wedging help picker must not hold the pty node

## Outcome

`cartridge help <id>` run through the shell tool opens an interactive picker
that seizes the pty node: it holds the terminal, ignores `q` (treated as
filter text), needs repeated Ctrl-C to exit, and blocks every later shell
command. A help lookup is documentation, not a session — it must never wedge
the pty.

## Evidence

Observed repeatedly on 2026-09-16/17 by coordinator sessions cartridge-ea,
cartridge-8e (this one) and recorded in auto-memory
(`help-in-the-wrapped-shell-wedges-pty`): `cartridge help memory` /
`cartridge help live` / `cartridge help memo` through `tool.shell` opened the
picker, the shell tool then returned "mcp did not answer in time" for the next
command, and the running-command state showed the picker holding the node.
Escape returned to the list rather than exiting; only Ctrl-C (sometimes twice)
released it, after which the shell answered normally. The trap also
historically killed every model request while held.

## Acceptance

- [ ] `cartridge help <id>` in the wrapped shell renders non-interactively or
      opens a picker that exits on `q` and never blocks the shell tool's next
      command.
- [ ] While the picker is open, a concurrent `tool.shell` read still answers
      within its timeout.
- [ ] A regression test drives the picker path against a fake pty and fails
      when the picker consumes the exit key.

## Planning note

Filed by the fork answering "what do you think of this harness and proxy and
mcp?" after the user said "fix the known bugs". The tool-surface bugs recorded
in auto-memory (`memo types` overflow, `lsp status` invalid envelope) were
probed and both already answer cleanly at HEAD, so they are not re-filed.