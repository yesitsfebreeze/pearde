---
repo: /Users/feb/dev/cartridge/tui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: ui
work-kind: leaf
review-round: 4
review-status: passed
canonical-scope: human-context-is-the-same-document
footprint:
- /Users/feb/dev/cartridge/tui.ctg/ui/palette.tsx
- /Users/feb/dev/cartridge/tui.ctg/ui/index.ts
- /Users/feb/dev/cartridge/tui.ctg/src/chat.ts
- /Users/feb/dev/cartridge/tui.ctg/src/wire.ts
- /Users/feb/dev/cartridge/tui.ctg/.cartridge/tests/integration
---

# The UI shows people the same owner documents the agent reads

The terminal UI has no context view: the palette lists `ui.actions()` and bare agent tool names (`ui/palette.tsx`, `chat` `tools`). This leaf adds a keyboard-opened inspector that shows each composed cartridge's own documents, with no UI-authored catalog. Per [a-cartridge-brings-its-own-surface](../../../../../../.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md) tui names no sibling: it `gather`s one tui-defined context event, and each answering cartridge supplies its documents (for example its `.cartridge/help.md`, or memo the records it gives the agent). It absorbs the older context-inspector entry-point scope.

## Acceptance

- [ ] Editing a fixture listener's document changes the inspector's human, docs and commands views after refresh, without rebuilding the UI.
- [ ] Opening, reading and switching views executes nothing; an explicit action shows its owner, arguments and outcome.
- [ ] A declined, failed, timed-out or stale answer renders as a named state under its cartridge; keyboard navigation, Escape/back and focus survive refresh.
- [ ] UI module replacement leaves the PTY, shell and unsent chat draft usable; an 80-column terminal stays readable.

## Proof and recovery

Start at [palette.tsx](../../../../../../tui.ctg/ui/palette.tsx), [chat.ts](../../../../../../tui.ctg/src/chat.ts), [wire.ts](../../../../../../tui.ctg/src/wire.ts). First probe: confirm event definition and per-listener outcomes since cartridge.ctg `c9ef10b`. Create `inspector.test.tsx` in `tui.ctg/.cartridge/tests/integration/` with two fixture listeners, one edited between reads and one failing. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`, `just isolation`. Not run for this plan. The inspector is additive; disabling it leaves the palette unchanged and writes nothing.

## Dependencies and review

No hard `needs`: the slice is proven with fixture listeners. Real memo/docs answers are their owners' work; [@root/memory-document-works-end-to-end](../../../root/prds/memory-document-works-end-to-end/prd.md) is context only. Shared footprint: `ui/palette.tsx` with [improve-ui-tool-availability](../improve-ui-tool-availability/prd.md). [Review history](review.md): rounds 1–4 used, inherited from both source IDs.
