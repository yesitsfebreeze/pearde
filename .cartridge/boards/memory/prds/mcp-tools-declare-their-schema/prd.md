---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# every MCP tool ships `{"type":"object","additionalProperties":true}`, so a host with no property types sends numbers and booleans as strings — `k` is rejected and `counts_only` is silently ignored

## Do

`respond_static` (`src/commands/src/commands_mcp.rs:175`) answers `tools/list`
with the same schema for all 22 tools:

```
"inputSchema": { "type": "object", "additionalProperties": true },
```

No properties, no types, nothing required. The parameters exist only as prose
inside each description — `{text, k?, mode?: hybrid|content|reason|vector, ...}`
— which a reader can follow and a client cannot type against. Measured from an
agent host on 2026-09-06: `query {k: 5}` arrived as `{"k": "5"}` and was
refused with `invalid type: string "5", expected usize`, and
`report {counts_only: true}` arrived as `"true"`, was dropped, and the call
answered 817,904 characters. A typed argument is unreachable from that host for
every tool that takes one.

Give each row of `TOOLS` (`src/commands/src/commands_mcp.rs:23`) a real
`inputSchema`: the property names the description already lists, each with its
JSON type, and `required` where the server has no `#[serde(default)]`. The
argument structs in `src/rpc/src/server.rs` are the authority for both — the
schema is written beside the tool name, not derived, so a field added there
without its schema row is the same defect again and the check below catches it.

Landing this also removes the discoverability half of
[claim-kind-lists-without-a-name](../claim-kind-lists-without-a-name/prd.md): `required` states what the prose gets
wrong.

**Done 2026-09-06.** `TOOLS` is `&[(&str, &str, &str)]`, the third field a JSON
schema literal beside the name, parsed at `tools/list` time rather than shipped
as a string. All 22 carry `properties` with a type per field and `required`
where the arg struct has no `#[serde(default)]` — link, forget,
forget_by_source, degrade, move, promote, claim_kind.

Writing them found three more descriptions the structs prove wrong, corrected
in the same change: `forget` advertised a `force?` that `ForgetArgs` does not
have and `tool_forget` hardcodes to false; `degrade` advertised an `id` beside
`query_id` that `DegradeArgs` does not have; and `audit` omitted the `apply`
argument `tool_audit` reads and parses. `claim_kind`'s description is now
truthful to today's code — `{action: add|rm, name, description?, parent?}`,
both required, no `strength`, no list arm — which is truth-to-code and not the
fix [claim-kind-lists-without-a-name](../claim-kind-lists-without-a-name/prd.md) describes; that part stays open, and
the description test fails if a `list` arm lands without its schema.

## Acceptance
Held by `every_tool_declares_the_arguments_its_description_names` and
`a_typed_argument_reaches_the_operation`
(`src/commands/src/tests/commands_mcp_test.rs`); the suite read 1,231 passed.

`cargo test -p commands mcp` — a test walks `TOOLS`, asserts every row's
`inputSchema` carries a `properties` object with at least one entry and a
`type` on each, and that every name inside the description's `{...}` list
appears as a property. A second assertion sends `{"name":"query",
"arguments":{"text":"x","k":5}}` and `{"name":"report","arguments":
{"group":"kind","counts_only":true}}` through `respond` and expects no
`invalid arguments` in either answer.
