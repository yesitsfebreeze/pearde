---
repo: /Users/feb/dev/cartridge/tui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: ui
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: the-gutter-is-the-boundary
needs:
- '@ui/the-gutter-shows-both-sides'
---

# Command indicators coexist with the current terminal surface

Roll-up, not implementation work. Its superseded premise, a gutter as the only boundary ([the-terminal-grid-lives-in-pty](../../../../../../.cartridge/memos/decision/the-terminal-grid-lives-in-pty.md)), was replaced by [the-agent-surface-preserves-the-visible-shell](../../../../../../.cartridge/memos/decision/the-agent-surface-preserves-the-visible-shell.md): indicators are added beside the surface and replace nothing. The surface today is tui.ctg's chat/shell split with palette and handoff header (`tui.ctg/.cartridge/docs/README.md`). Its only leaf is the gutter; composer and transcript integration remain with [the-sidebar-slides-over-the-shell](../../../../memos/work/root--the-sidebar-slides-over-the-shell.md), which is claimed elsewhere.

## Acceptance

- [ ] [the-gutter-shows-both-sides](../the-gutter-shows-both-sides/prd.md) is done with its own evidence.
- [ ] At that tui.ctg revision, `just test tui` (cwd `/Users/feb/dev/cartridge`) shows the gutter together with the unchanged chat transcript, palette and handoff header; the result records remaining limitations.

## Work items

- [the-gutter-shows-both-sides](../the-gutter-shows-both-sides/prd.md)

## Review

[Review history](review.md): rounds 1–4 used. Disposition: recommend merging this one-child roll-up into [the-inline-agent](../the-inline-agent/prd.md).
