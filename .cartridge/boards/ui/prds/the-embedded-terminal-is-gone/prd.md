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
canonical-scope: the-embedded-terminal-is-gone
needs:
- '@ui/the-ui-paints-the-grid'
---

# the-embedded-terminal-is-gone

Replace the old removal handoff with a consumer-by-consumer parity ledger. UI may lose its duplicate emulator only after the PTY grid serves every consumer; raw-output/history paths remain until equivalent shell readback, command evidence and reconnect are demonstrated. Old probe deletions are historical, not instructions to reapply.

## Acceptance

- [ ] Current code has one escape-sequence interpretation owner, with shell output/readback still available through documented APIs.
- [ ] Real nvim, UI replacement, latest-tool footer, main/dynamic status and transcript behavior pass on the candidate renderer.
- [ ] Each removed API names its migrated consumers and retained behavioral test; no test is deleted merely to satisfy a text search.

## Proof and recovery

Start at [chat.ts](../../../../../../ui.ctg/src/chat.ts), [modules.ts](../../../../../../ui.ctg/src/modules.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-embedded-terminal-is-gone`; maximum five rounds.
