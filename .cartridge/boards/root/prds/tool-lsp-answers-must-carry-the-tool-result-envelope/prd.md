---
state: "specced"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/lsp.ctg"
---

# tool.lsp answers must carry the tool result envelope

## Outcome

Every `tool.lsp` `call` reply carries the shared tool result envelope
`{"content": <string>, "error": <bool>}`, so `status` and `diagnostics` answers
pass the MCP bridge and the inline agent's dispatch check instead of failing
with `invalid tool result envelope`.

## Reason

`lsp.ctg/src/service.rs` `dispatch` returns bare JSON objects from the `call`
arm (`{state, ...}`, `{installed: [...]}`, `{state, result}`) while the
envelope is checked in `mcp.ctg/src/service.rs:457`, `proxy.ctg/src/service.rs:880`
and `agent.ctg/src/lib.rs:755`. Only the `cancel` branch emits the envelope.
The cartridge therefore registers over MCP (its descriptor passes) but every
model call fails, from any harness. Confirmed 2026-09-16: `status` and
`diagnostics` both return `invalid tool result envelope` while the composed
lsp cartridge is Active and even spawns its rust-analyzer.

## Acceptance

- [x] `tool.lsp` `call` replies are `{"content": "<json string>", "error": false}` on success, matching memo's `success()` shape (`memo.ctg/src/service.rs:508`); errors surface as `{"content": "<message>", "error": true}` or as a service error the MCP bridge already wraps at `mcp.ctg/src/service.rs:456`.
- [ ] `mcp__cartridge__lsp` `status` returns catalog JSON through a Claude MCP session.
- [ ] `mcp__cartridge__lsp` `diagnostics` on a touched Rust file returns the `state`-carrying body (an empty diagnostic list still reports `state`, never "no findings").
- [x] `describe` and `cancel` behaviour unchanged; the `context.lsp` evidence provider was untouched by that delivered envelope change (historical proof; its later removal belongs exclusively to @lsp/remove-context-lsp-provider).
- [x] lsp unit tests cover the envelope shape of one query reply.

## Observed 2026-09-16

Code, unit test and both gates verified: `just check lsp` and `just test lsp`
pass (13 tests), committed at lsp.ctg 82ea783. The two MCP-session boxes stay
open: the composed host still serves the pre-change snapshot, so `tool.lsp`
resolves as not provided from the CLI and this session has no cartridge MCP
server to call. They close after a host reload with the rebuilt lsp module.

## Context retirement coordination (2026-09-19, Codex coordinator)

@lsp/remove-context-lsp-provider intentionally removes the historical provider after memo no longer consumes it. This does not alter tool result envelopes, describe/cancel requirements or the two pending MCP-session proofs above. Preserve this leaf's review history and checked historical evidence; do not infer missing MCP success from cleanup. Serialize overlapping source/manifest/docs work with any live claim and review changed executable contracts before dispatch.
