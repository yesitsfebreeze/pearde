---
complexity: medium
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/continuation.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/continuations.md
---

# Recover synthetic Responses continuation mappings safely

Only the synthetic Responses IDs produced by the existing multi-round SSE adapter are mapped. Native JSON response IDs and non-proxy provider IDs retain their existing wire semantics. Conversation history stays caller-owned; there is no durable cache or automatic replay.

Use a random instance epoch in versioned synthetic IDs. Keep at most `continuation_capacity` live mappings (default 1024, maximum 1024), each with an absolute monotonic TTL (`continuation_ttl_secs`, default 3600). Remember upstream ID, original requested selector, exact final router route from the authenticated loopback response header, and trusted frontend principal. Each cached upstream ID, selector and route is at most 4 KiB; oversized/missing mapping inputs leave the ID unavailable. Keep a further capacity-sized set of expired/evicted IDs, so recent expiry is distinguishable without unbounded tombstones. Other epochs report `continuation_instance_lost` (restart or foreign instance, not a claim that restart was observed). Legacy/malformed and unknown current-epoch IDs report `continuation_invalid`; older evicted IDs beyond the bounded diagnostic window become invalid. Missing route evidence makes a completed synthetic ID explicitly unavailable for continuation; no guessed provider mapping is allowed.

The native injection is one trusted principal. The default HTTP key is a separate shared principal; multiple processes using that key share its authority and cannot be distinguished. Optional profile configuration `client_key_envs` maps at most 32 named principals to distinct environment-backed HTTP secrets. Startup rejects empty/missing/duplicate secrets, including reuse of the primary key. Request metadata and client-supplied scope headers never choose an identity. No secret values enter IDs/errors/cache. Cross-principal lookup returns generic invalid before routing; IDs are not authorization grants. Full-input recovery removes `previous_response_id` and resends caller-owned input explicitly; the proxy does not reconstruct or retry history.

A valid lookup requires the same original model selector, replaces the synthetic ID with its exact upstream ID, and pins `model` to the captured route with `cartridge_strict=true`. Missing/changed selector fails before router calls. Router rejection propagates with no fallback/replay. Profile or process recreation loses all mappings. No telemetry field is added to native success payloads.

## Acceptance

- [x] Actual streamed continuation creation/resume pins the final route and upstream ID; JSON and all three SSE wires retain their existing behavior.
- [x] TTL expiry, capacity eviction, bounded old-ID diagnostics, restart/foreign instance, malformed/legacy IDs and missing-route evidence fail with documented codes before dispatch; full-input recovery succeeds.
- [x] Authenticated distinct HTTP principals cannot use each other's IDs; metadata/header spoofing cannot change the principal; duplicate/missing key configuration fails. A shared key's limitation is documented.
- [x] Changed model/provider selection is rejected; router failure does not replay; no cache bodies or secrets, bounded retention, no durable data or history writes.

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-continuation" just test proxy
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-continuation" just check proxy
```

Tests use real loopback HTTP/SSE with deterministic provider replies, retain exact outgoing requests, and use monotonic-clock injection for expiry without sleeps. The fixture's upstream header is the same router contract emitted by `router.ctg/src/proxy.rs`; fixture keys never leave temporary test state. Restart is a fresh Service with a new epoch, and HTTP listeners are recreated for principal tests. Preserve the prior implementation on failure. Existing usage-accounting receipt footprints overlap and require coordinator revalidation after integration.
