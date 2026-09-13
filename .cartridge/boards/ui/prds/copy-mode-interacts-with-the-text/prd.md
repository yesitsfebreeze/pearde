---
repo: /Users/feb/dev/cartridge/ui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: ui
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: copy-mode-interacts-with-the-text
needs:
- '@ui/the-ui-paints-the-grid'
---

# copy-mode-interacts-with-the-text

Rebase the candidate onto ui.ctg and pty.ctg. Freeze a revision-bound view, not the running shell. Selection uses terminal cells with correct wide/combining-character handling; aged-out content is explicit. Opening a path validates an owner-qualified reference and passes literal argv to the intended editor through the owned shell. Corrections target memo and memory independently through their validated services.

## Acceptance

- [ ] Unicode selection and whole-command copying return exact selected text; scrollback expiry never silently substitutes current rows.
- [ ] A malicious path or link cannot append shell syntax, and opening a link while an editor owns input is refused or explicitly routed without corrupting it.
- [ ] Memo and memory correction fixtures each record anchored provenance and their own success/failure; one target failing cannot be reported as both saved.

## Proof and recovery

Start at [chat.ts](../../../../../../ui.ctg/src/chat.ts), [modules.ts](../../../../../../ui.ctg/src/modules.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `copy-mode-interacts-with-the-text`; maximum five rounds.
