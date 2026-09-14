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
canonical-scope: improve-ui-programme
needs:
- '@ui/improve-ui-run-history'
- '@ui/improve-ui-terminal-owner'
- '@ui/improve-ui-tool-availability'
---

# Terminal UI improvement plan

Roll-up of three terminal UI improvements in tui.ctg. It is not implementation work: claim a leaf. The leaves share `ui/palette.tsx`, `ui/index.ts` and `src/chat.ts`, so land them one at a time and rebase the next.

## Acceptance

- [ ] Each linked leaf is done with its own recorded acceptance evidence.
- [ ] After the last leaf lands, `just test tui` and `just check tui` (cwd `/Users/feb/dev/cartridge`) pass at one recorded tui.ctg revision, and the result lists tested mitigations and remaining limitations.

## Work items

- [Reopen completed run evidence after closing the panel](../improve-ui-run-history/prd.md)
- [Display shared terminal ownership and cwd](../improve-ui-terminal-owner/prd.md)
- [Explain tool readiness in the palette](../improve-ui-tool-availability/prd.md)

## Review

[Review history](review.md): rounds 1–4 used; maximum five.
