---
complexity: medium
footprint:
  - src/main.rs
  - src/catalog.rs
  - src/requirements.rs
  - src/proxy.rs
  - src/sync.rs
  - .cartridge/tests/unit/catalog/capabilities.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
  - .cartridge/tests/unit/sync/tests.rs
  - .cartridge/docs/capabilities.md
---

# spec01 — Capability requirements precede ranking

Use one pure compatibility gate for discovery and actual attempts. Every route,
including explicitly named, strict and local-last-resort routes, must satisfy the
same requirements before ranking/fallback. Required tools need explicit true;
modalities need explicit membership. Unknown, false, malformed and expired claims
have distinct rejection reasons. Per-hop missing context/capabilities must not
inherit another provider's values. Sync refreshes each hop independently.

Context admission includes the existing serialized-input estimate, explicitly
labelled heuristic, plus the requested output budget. An optional positive
cartridge_requirements.context_tokens supplies a caller-known input bound; use
the greater value. Checked arithmetic prevents overflow. Unknown context fails
admission; a named route cannot override it. This does not claim exact provider
billing or tokenizer measurement.

Retain per-hop evidence source/observation time and optional valid_until. Expired
claims refuse selection. Live inventory claims expire after 24 hours; bundled or
explicit configured declarations remain labelled declarations, never live
verification. A failed inventory refresh retains prior evidence/expiry instead of
refreshing its timestamp from bundled defaults. Missing live fields stay unknown
rather than borrowing the preceding hop's data. A read-only detailed routes query
reports these evidence states and rejection reasons without credentials.

For request fields outside the supported common translation contract, require
explicit per-hop wire_features and the same native wire. Cover structured output,
forced/parallel tools, strict tool schemas, reasoning, server-native tools and
stateful continuation. Unsupported conversion fails before network dispatch.
Preserve native Anthropic requests directly instead of round-tripping through Chat.
Codex normalization may not silently override an explicitly required field.
Keep plain text/basic function tool translation and existing response formats.
Do not send cartridge_requirements to providers or start extra model probes.

## Acceptance

- [x] Named, strict and local-last routes refuse unsupported/unknown tools, modalities, stale claims and insufficient context; absent compatible routes return an explicit no-compatible-route error.
- [x] Separate provider hops cannot inherit capability/context claims; old/new/unknown evidence is distinguishable and failed refresh does not renew stale evidence.
- [x] A loopback failing compatible provider falls back only to another compatible provider; incompatible fixture endpoints receive zero requests and required wire fields arrive unchanged.
- [x] Native/common wire behavior, credentials, reload leases and prior protocol tests pass; all rejection output is bounded metadata without secrets or request bodies.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test router
```

Run public check router and proxy/MCP consumer gates after integration. Use only
loopback fixture providers and synthetic keys. Baseline-inputs.json and
baseline-log.txt retain the named/strict/local bypass: observed [1,1,1] candidates
when [0,0,0] are required. Preserve ordinary caller history and actual attempted
route headers; no health recovery or replay redesign belongs to this slice.
