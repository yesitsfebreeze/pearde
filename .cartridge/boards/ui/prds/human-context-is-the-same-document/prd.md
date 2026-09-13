---
repo: /Users/feb/dev/cartridge/ui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: ui
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: human-context-is-the-same-document
needs:
- memory-document-works-end-to-end
footprint:
- /Users/feb/dev/cartridge/ui.ctg/src/chat.ts
- /Users/feb/dev/cartridge/ui.ctg/src/modules.ts
- /Users/feb/dev/cartridge/ui.ctg/src/registry.ts
- /Users/feb/dev/cartridge/ui.ctg/ui
- /Users/feb/dev/cartridge/ui.ctg/tests
---

# The UI presents the human view of the same landscape context

People should be able to understand the same capability and evidence the agent selected, without a separately authored UI catalog.

## Acceptance

- [ ] An edit to the owner document updates human/docs/commands views consistently without a UI rebuild.
- [ ] Reading and switching views never executes a recipe; an explicit action shows its owner, arguments, and outcome.
- [ ] Unavailable source and stale revision are understandable states; keyboard navigation, escape/back, and focus survive refresh.
- [ ] Replacing UI leaves the PTY/shell and existing input draft usable; narrow terminal contents remain readable.

## Proof and recovery

Start at [chat.ts](../../../../../../ui.ctg/src/chat.ts), [modules.ts](../../../../../../ui.ctg/src/modules.ts), [registry.ts](../../../../../../ui.ctg/src/registry.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `human-context-is-the-same-document`, `the-context-inspector-opens-from-the-chat-editor`; maximum five rounds.
