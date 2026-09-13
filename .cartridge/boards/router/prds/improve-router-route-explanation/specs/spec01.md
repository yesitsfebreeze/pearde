---
complexity: medium
footprint:
  - Cargo.toml
  - src/main.rs
  - src/catalog.rs
  - src/requirements.rs
  - src/proxy.rs
  - src/decision.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
  - .cartridge/tests/unit/catalog/capabilities.rs
  - .cartridge/docs/decisions.md
---

# spec01 — Inspect actual route selection without exposing request data

Add an opt-in `cartridge_explain: true` router request field and remove it before
provider dispatch. A bounded request-owned decision record captures capability
rejections, ordered health/budget skips, attempted route/status and actual selected
route/model. Native request success adds `cartridge_routing`; HTTP responses expose
`x-cartridge-decision-id`, retrievable through trusted native `op: decision, id`.
The latest 128 finished/failed/cancelled reports remain in memory. Unknown/evicted
IDs fail explicitly; no trace replays a request or grants authority.

Bind reports to SHA-256 identities over the exact sanitized catalog/ranking policy
snapshot used for selection. Include only selection-relevant provider identity,
wire, capabilities, context and ranking inputs; never keys, OAuth objects, URLs,
headers, request bodies or raw upstream error messages. Capture health decisions
at their actual observation time with bounded structured reasons. Keep the existing
actual-route header. Stream reports say `stream_started` after first-output
selection, not completed delivery. Cancellation retains known attempts as incomplete.

Expand existing detailed route discovery with policy/catalog revisions and health
observations, clearly labelled preflight rather than actual execution. Health can
change afterwards. Reverting ranking rules produces the earlier semantic revision
without rewriting stored actual-attempt reports. Default request/response behavior
remains unchanged when explanation is absent. Bounded rows/bytes and omission
counts apply to the trace as well as discovery.

## Acceptance

- [x] A loopback fixture distinguishes health, capacity and capability skips, records the failed first attempt and selects the same fallback shown by execution headers.
- [x] Reordering equivalent configuration preserves revisions; changing and restoring policy changes/restores its revision while old actual traces remain unchanged.
- [x] Native/HTTP opt-in results expose matching IDs; disabled requests retain shape; unknown/evicted IDs, cancellation and stream-start state are explicit.
- [x] Synthetic credentials, headers, OAuth fields, request bodies and provider error payloads do not appear in reports; existing admission/wire/reload gates pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test router
```

Run public check router and existing proxy/MCP consumers. Add sha2 using the already
resolved workspace version; the runtime workspace lockfile update is integration
bookkeeping committed separately without other runtime edits. Baseline logs retain
the actual fallback with no decision receipt. Only loopback providers and synthetic
keys are used; no provider credentials or live profile rules are changed.
