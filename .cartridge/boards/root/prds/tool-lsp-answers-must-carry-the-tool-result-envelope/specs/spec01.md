---
complexity: low
footprint:
- src/service.rs
- .cartridge/tests/unit/wire.rs
---

# tool.lsp answers carry the tool result envelope

`dispatch` returned bare JSON bodies from the `call` arm while the envelope is
checked in `mcp.ctg/src/service.rs`, `proxy.ctg/src/service.rs` and
`agent.ctg/src/lib.rs`. Only `cancel` emitted it, so the cartridge registered
over MCP but every model call failed with `invalid tool result envelope`.

The `call` arm now answers `{"content": <json string>, "error": false}`,
the shape memo's `success()` gives its answers. Errors stay `Err` and the MCP
bridge wraps them. `describe` and `cancel` are unchanged, and the native
`context.lsp` evidence path is untouched.

## Acceptance

- [x] `tool.lsp` `call` replies are `{"content": "<json string>", "error": false}`
  on success; errors surface as a service error the bridge wraps.
- [x] `describe` and `cancel` behaviour unchanged; `context.lsp` untouched.
- [x] An lsp unit test covers the envelope shape of one query reply.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge
just check lsp
just test lsp
```

Both gates pass; `call_answers_carry_the_tool_result_envelope` asserts
`content` is a string, `error` is false, and the inner JSON carries the
catalog body.
