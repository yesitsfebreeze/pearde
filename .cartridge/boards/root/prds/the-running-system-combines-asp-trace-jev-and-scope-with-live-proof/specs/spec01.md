---
complexity: 1
footprint:
  - .cartridge/tests/integration/asp-system.test.ts
  - .cartridge/tests/integration/asp-code-lookup.test.ts
  - .cartridge/justfile
  - .cartridge/README.md
  - .cartridge/memos/routine/cartridge-development.md
  - .cartridge/memos/note/integration-needs-live-cross-cartridge-proof.md
  - .cartridge/memos/note/combined-asp-jev-scope-live-proof.md
  - jev.ctg
---

# Prove the combined running composition

Add an explicit `just test system` gate. It uses the actual running host and
stored auth, so it is separate from offline tests and documents its two model
requests. It checks root containment, real cycle telemetry, ASP retrieval
through JEV, both model passes, content withholding, and the exact decision
in the durable trace. It checks graph edges and renders all four scope views
from live responses. Unavailable capabilities or fallback reasons fail it.

The existing MCP lookup test waits for all expected outline, call and
reference evidence under one deadline; it also checks the activity schema
and result. The ordinary owner gates include JEV through the existing Bun
dispatch. Preserve concurrent runtime, memory and scope source changes.

The independent verifier reviewed the actual system gate and ran three
fresh-fixture MCP tests. JEV's independently verified implementation was
collected separately at 215007548e4d26907ba51893b8084aa63d662c90.

## Acceptance

- [x] The live gate passed with two actual model responses and a correlated durable trace record.
- [x] All four scope views rendered the live responses without unavailable warnings.
- [x] MCP discovery passed on three fresh fixtures.
- [x] JEV's standard check and test gates passed, and isolation passed for 20 cartridges.

## Verify and Proof

```sh
just test system
just test jev
just check jev
```

The live observation and model usage are recorded in the memo
`note/combined-asp-jev-scope-live-proof.md`. Runtime and UI source are being
developed in other panes; this gate verifies their combined behavior without
claiming their broader source work is complete.
