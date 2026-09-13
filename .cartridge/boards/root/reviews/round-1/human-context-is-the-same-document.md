---
state: open
origin: requested
priority: 75
blast-radius: mid
workflow: develop-one-cartridge
needs:
  - memory-document-works-end-to-end
footprint:
  - /Users/feb/dev/cartridge/ui.ctg/src/chat.ts
  - /Users/feb/dev/cartridge/ui.ctg/src/modules.ts
  - /Users/feb/dev/cartridge/ui.ctg/src/registry.ts
  - /Users/feb/dev/cartridge/ui.ctg/ui
  - /Users/feb/dev/cartridge/ui.ctg/tests
  - /Users/feb/dev/cartridge/harness.ctg/inspection.rs
---

# The UI presents the human view of the same landscape context

People should be able to understand the same capability and evidence the agent selected, without a separately authored UI catalog.

## Ownership and scope

Owner: `ui`. Participating repositories: `ui.ctg`, `harness.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Add a landscape result/detail flow with commands, documentation, and human views; make mode switches preserve selected identity/revision.
2. Show source ownership, why selected, related references, availability, and partial-context notices. Render source Markdown instead of copying descriptions into UI code.
3. Reuse existing input/palette/context-inspector interactions for explicit execution and approval. Preserve drafts, terminal state, and keyboard focus across refresh.
4. Cover empty/loading/error/stale states and narrow-terminal layout with rendering tests and a recorded interactive walkthrough.

## Acceptance contract

- An edit to the owner document updates human/docs/commands views consistently without a UI rebuild.
- Reading and switching views never executes a recipe; an explicit action shows its owner, arguments, and outcome.
- Unavailable source and stale revision are understandable states; keyboard navigation, escape/back, and focus survive refresh.
- Replacing UI leaves the PTY/shell and existing input draft usable; narrow terminal contents remain readable.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test ui
just check ui
just test harness
```

## Failure and recovery

A view refresh loses input or executes a default recipe. Test state preservation and read-versus-run behavior.

Rollback: Keep the existing inspector/palette accessible until the new flow matches its behavior. Revert rendering without changing documents or sessions.

## Prior context

Related existing runtime memo leaf names: `the-context-inspector-opens-from-the-chat-editor`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
