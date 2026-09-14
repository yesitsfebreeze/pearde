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
canonical-scope: improve-ui-tool-availability
footprint:
- /Users/feb/dev/cartridge/tui.ctg/ui/palette.tsx
- /Users/feb/dev/cartridge/tui.ctg/src/chat.ts
- /Users/feb/dev/cartridge/tui.ctg/src/wire.ts
- /Users/feb/dev/cartridge/tui.ctg/.cartridge/tests/integration/palette.test.tsx
---

# Explain tool readiness in the palette

The palette lists agent tools as bare names from `chat` `tools` (tui.ctg `ui/palette.tsx`, `src/chat.ts`) and offers every one as runnable. This leaf shows why a tool is or is not usable. The old plan read a Landscape readiness row with a policy revision; the landscape library is gone ([the-fabric-lives-in-core](../../../../../../.cartridge/memos/decision/the-fabric-lives-in-core.md)) and policy knows no tool ([a-cartridge-brings-its-own-surface](../../../../../../.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md)). So tui `gather`s one tui-defined readiness event for the listed tools; each cartridge answers for what it owns. Installed, allowed, dependency-ready and verified stay separate fields; a diagnostic never authorizes execution.

## Acceptance

- [ ] Ready, denied, dependency-unavailable and unverified fixture tools render distinct explanations, attributed to the answering cartridge, and only actions valid for that state are offered.
- [ ] A tool no listener answers for shows "readiness unknown" and stays in today's list.
- [ ] After a tool is replaced or removed, its old action is invalidated before dispatch; a stale selection shows a refresh or refusal without moving focus.
- [ ] Keyboard-only inspection works at 80 columns; opening the palette starts no provider or probe beyond the one event.

## Proof and recovery

Start at [palette.tsx](../../../../../../tui.ctg/ui/palette.tsx), [chat.ts](../../../../../../tui.ctg/src/chat.ts), [wire.ts](../../../../../../tui.ctg/src/wire.ts). First probe: confirm event definition, `timeout_ms` and per-listener outcomes since cartridge.ctg `c9ef10b`. Extend `palette.test.tsx` in `tui.ctg/.cartridge/tests/integration/` with fixture listeners. Gates, cwd `/Users/feb/dev/cartridge`: `just test tui`, `just check tui`, `just isolation`. Not run for this plan. The UI only reads answers; reverting restores the bare list.

## Dependencies and review

No hard `needs`; the former `@mcp/improve-mcp-tool-readiness` need targeted the dissolved Landscape row. MCP, policy and tool owners may answer the event in their own work. Shared footprint: `ui/palette.tsx` with [human-context-is-the-same-document](../human-context-is-the-same-document/prd.md). [Review history](review.md): rounds 1–4 used.
