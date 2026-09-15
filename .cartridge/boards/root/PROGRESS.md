# Root board progress

Snapshot: 2026-09-15. The board was reset to one plan (see [BACKLOG](BACKLOG.md)).

- open: 19 (16 leaves, 3 milestones) — all new
- deferred: 236 across every board (223 by state, 13 with unclosed frontmatter), 28 of them `superseded-by` an item on this board
- done: 483, kept as history
- claimed: 0; lanes: 0 (two stale harness worktrees removed, both clean at their last commit)
- boards: `ui` removed with tui.ctg; the other member boards stay as archives

Wave 1 is dispatchable now: the profile becomes the orchestration service
(tui.ctg deleted, memory.ctg out of the profile), the record loses its
shadowed copies, and the gates run from the root justfile. Baseline on
2026-09-15: `just check` is red (rustfmt in cartridge.ctg), `just test` was red
in gitfs, sessions, pty, router, harness and mcp on 2026-09-14, `just smoke`
failed mcp and proxy, and `just --justfile .cartridge/justfile check` cannot find
`memo-run`.
