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
canonical-scope: improve-ui-tool-availability
needs:
- '@mcp/improve-mcp-tool-readiness'
footprint:
- /Users/feb/dev/cartridge/ui.ctg/ui/index.ts
- /Users/feb/dev/cartridge/ui.ctg/ui/palette.tsx
- /Users/feb/dev/cartridge/ui.ctg/ui/activity.ts
- /Users/feb/dev/cartridge/ui.ctg/src/chat.ts
- /Users/feb/dev/cartridge/ui.ctg/tests/transcript.test.tsx
- /Users/feb/dev/cartridge/ui.ctg/tests/palette.test.tsx
---

# Explain tool readiness and policy in the palette

Consume Landscape's generic readiness row and the same policy revision used by MCP; share this source with the human-context view. Keep installed/exposed/allowed/dependency-ready/verified dimensions separate. A diagnostic status cannot authorize execution.

## Acceptance

- [ ] Ready, denied, dependency-unavailable and unverified fixture tools render distinct explanations and valid actions.
- [ ] Replacement/removal invalidates old actions before dispatch; stale selection returns a visible refresh/refusal without changing focus.
- [ ] Keyboard-only and narrow-terminal inspection remains usable and the view itself starts no provider or probe.

## Proof and recovery

Start at [index.ts](../../../../../../ui.ctg/ui/index.ts), [palette.tsx](../../../../../../ui.ctg/ui/palette.tsx), [activity.ts](../../../../../../ui.ctg/ui/activity.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-ui-tool-availability`; maximum five rounds.
