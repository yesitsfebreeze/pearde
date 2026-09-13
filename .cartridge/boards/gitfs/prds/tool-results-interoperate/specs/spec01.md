---
complexity: medium
footprint: ["src/push.rs","src/main.rs","src/service.rs","src/ship.rs","src/tool_result.rs",".cartridge/tests/unit/tool_result.rs",".cartridge/tests/integration/tool-result.test.ts","Cargo.toml","src/provenance.rs",".cartridge/tests/unit/provenance.rs",".cartridge/tests/integration/change-provenance.test.ts",".cartridge/docs/change-provenance.md"]
---

# spec01 — Produce the existing ToolResult contract once

Share success serialization for GitFS and ship: strings remain literal strings;
structured payloads become JSON text exactly once. SDK handlers translate ordinary
returned errors into content:string/error:true instead of transport failure.
Validate operation-specific input types and allowed fields before StoreConfig.at,
including relative paths, so malformed calls cannot initialize a store. Preserve
current valid operation shapes, cancellation acknowledgments and partial results.

## Acceptance

- [x] Actual direct SDK, MCP and proxy consumers decode identical GitFS read and ship scan payloads, including file content that itself contains JSON.
- [x] Invalid input reaches no filesystem backend; policy refusal executes no tool mutation; a deliberately malformed response after a counted fixture mutation fails without retry or a second mutation.
- [x] The native agent's ordinary-tool-failure and exact-cancellation fixtures pass; producer failures use its existing error envelope without changing invocation identity.

## Verify and Proof

```sh
cargo test --manifest-path Cargo.toml -p gitfs
```

The GitFS unit gate runs the shared Bun integration fixture, which builds the
current runtime/GitFS/MCP/proxy executables and uses an isolated Git repository
and profile. Real GitFS and protocol consumers run; deterministic Lua services
stand in only for sessions, policy, harness and the model router. No external
model, publish, push or user store is involved. The fixture also owns a malformed
tool with an observable mutation counter and records its exact request context.

Run `just test agent a_tool_error_is_visible_to_the_next_model_request` and
`just test agent cancel_during_cancellable_tool_invokes_exact_call_cancel_and_no_late_append`
from cartridge.ctg for the unchanged consumer compatibility gates.
