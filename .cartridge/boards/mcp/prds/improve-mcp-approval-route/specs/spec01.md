---
complexity: medium
footprint:
  - src/service.rs
  - src/main.rs
  - .cartridge/tests/unit/tests.rs
  - .cartridge/tests/integration/approval.test.ts
  - .cartridge/docs/approval.md
---

# spec01 — Optional headless policy inspection

When the profile explicitly injects `policy.explain`, advertise the experimental
`cartridge/policy` method during initialization. Its name/arguments match
`tools/call`; only currently exposed tool names are inspectable. Construct trusted
context from this server's session and cwd, and report authorization_route=none.
Ignore client-supplied context, approval and route metadata. Return selected rule,
semantic revision and a concrete operator action for deny/ask. Inspection does not
invoke tools, emit approval events or record tool usage.

Actual tools/call keeps policy as its sole dispatch gate. A refusal keeps its
existing text/result shape and may add a diagnostic under `_meta.cartridge/policy`.
Obtain explanation only after refusal; require matching decision and revision
before attributing its selected rule to that refusal. On replacement mismatch or
unavailable explanation, keep the refusal and label diagnostics unavailable. Never
let explanatory metadata grant a tool call. Do not cache a prior approval.

Profiles without policy.explain retain existing negotiation, responses and dispatch.
The extension uses the existing protocol revision and experimental capability;
it does not advertise an interactive approval channel. Operator instructions point
to editing the matching rule in the selected profile's policy configuration and
retrying only after review; a whole-tool deny must be removed before an operation
allow can take effect. No live profile is changed by this implementation.

## Acceptance

- [x] A real temporary stdio profile exposes gitfs read=allow/write=deny and returns the matching rule/revision/operator action; only an allowed read reaches the tool.
- [x] Forged context/approval/route fields cannot change authority; inspection causes no tool call or usage observation; unknown/unexposed tools are refused.
- [x] Disabled profiles retain existing allow/ask/deny outputs; failed or mismatched diagnostics preserve refusal; replacement still uses fresh policy for execution.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test mcp
```

```sh
bun test ./.cartridge/tests/integration/approval.test.ts
```

Also run public check mcp and the existing initialized-client catalog replacement
fixture. Baseline-inputs.json and baseline-log.txt record the source-identical
missing-method probe. No live credentials/providers or policy changes are needed.
