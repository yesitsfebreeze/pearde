---
state: "specced"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
footprint:
- "src/cli/manual.rs"
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
- [ ] A regression test drives the picker path against a fake pty and fails
      when the picker consumes the exit key.

## Planning note

Filed by the fork answering "what do you think of this harness and proxy and
mcp?" after the user said "fix the known bugs". The tool-surface bugs recorded
in auto-memory (`memo types` overflow, `lsp status` invalid envelope) were
probed and both already answer cleanly at HEAD, so they are not re-filed.
## Decision (2026-09-19, coordinator)

**The fix goes in the host, as option (a).** The analyst found the picker in
`cartridge.ctg/src/cli/manual.rs`: the isatty gate in `help()` and the key
handling in `key()` and `browse()`. It reproduced the fault in a scratch pty: `q`
is taken as filter text and `Esc` needs three presses. The analyst also found
that `pty.ctg`'s concurrent-read path already answers correctly at HEAD. So
`repo` now names cartridge.ctg and the footprint is `src/cli/manual.rs`.

A single `q` or `Esc` quits the picker. That satisfies the first Acceptance
box's second alternative and needs no change in any other cartridge. The
analyst's option (b) would have had `pty.ctg` mark its shell so `help` renders
without a picker. It was not taken because it couples two cartridges through an
environment convention, and the Acceptance does not require it. If agents keep
opening the picker, (b) can be filed as its own PRD.

## Box 2 moved out (2026-09-19, coordinator, review round 1 finding B2)

The box "while the picker is open, a concurrent `tool.shell` read still answers
within its timeout" describes `pty.ctg`'s behaviour, not the host picker's. This
PRD's footprint is `cartridge.ctg/src/cli/manual.rs`. The analyst read
`pty.ctg`'s `tool.rs` and `lib.rs` and judged the path correct at HEAD, but a
reading is not a test, and the original report of "mcp did not answer in time"
argues against it. The box now belongs to
`@pty/a-shell-read-answers-while-a-foreground-program-holds-the-pty`, which owns
a test in `pty.ctg`.
