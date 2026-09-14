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
canonical-scope: the-inline-agent
needs:
- '@ui/the-gutter-is-the-boundary'
- '@ui/the-panel-switches-to-a-sub-agent'
- '@ui/improve-ui-terminal-owner'
---

# The agent is reached and answered without leaving the terminal

Finite roll-up of the remaining terminal-agent outcomes, not implementation work. The base is delivered in tui.ctg: a persistent chat beside the shared shell, approvals, handoff and palette (`tui.ctg/.cartridge/docs/README.md`). Replies entering shell scrollback and the one-shot overlay are historical; later enhancements get separate items.

## Acceptance

- [ ] Each linked item is done with its own recorded evidence and owner.
- [ ] At the final integrated tui.ctg revision, `just test tui` and `just check tui` (cwd `/Users/feb/dev/cartridge`) pass, and the result lists remaining limitations.

## Work items

- [Command indicators coexist with the current terminal surface](../the-gutter-is-the-boundary/prd.md)
- [The panel switches to a sub-agent](../the-panel-switches-to-a-sub-agent/prd.md)
- [Display shared terminal ownership and cwd](../improve-ui-terminal-owner/prd.md)

## Review

[Review history](review.md): rounds 1–4 used; maximum five.
