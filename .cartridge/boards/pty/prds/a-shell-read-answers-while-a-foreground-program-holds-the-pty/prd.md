---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/pty.ctg"
---

# A shell read answers while a foreground program holds the pty

## Outcome

While a foreground program holds the wrapped shell's pty (an interactive picker,
a pager, a REPL), a concurrent `tool.shell` read of that session answers within
its timeout with the current screen. It never reports "mcp did not answer in
time".

## Evidence

Coordinator sessions saw the failure on 2026-09-16 and 2026-09-17: while
`cartridge help <id>` held the picker open, the next shell tool call returned
"mcp did not answer in time". On 2026-09-19 the analyst of
`@pty/a-wedging-help-picker-must-not-hold-the-pty-node` read `pty.ctg/src/tool.rs`
and `src/lib.rs` and judged the concurrent-read path correct at HEAD. The two
accounts disagree, and only a test can settle which is true. The host-side
picker fix is that sibling's work; this PRD owns the pty side. The earlier
failure may also have come from the host serializing events on a node, which is
`@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node`.

## Acceptance

- [ ] A named test in `pty.ctg` runs a foreground program that reads the terminal and never exits, then performs a concurrent read of the same session. The read answers within its timeout with the screen contents.
- [ ] If the test fails at HEAD, the fix makes it pass. If it passes at HEAD, the report says so, and the test stays as a regression lock.
