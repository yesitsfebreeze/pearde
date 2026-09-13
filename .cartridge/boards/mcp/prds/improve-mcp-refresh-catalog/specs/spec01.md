---
complexity: medium
footprint:
  - src/service.rs
  - .cartridge/tests/unit/tests.rs
  - .cartridge/tests/integration/refresh.test.ts
  - .cartridge/docs/README.md
---

# spec01 — Publish a coherent tool registry across live replacement

Reuse the runtime's service-version vector and profile-owned injected tool set.
Read versions under the cache lock; on a miss collect descriptors, then compare
versions again. Retry up to three times if the vector changed, including a
failed describe during replacement. Do not publish partially described or mixed
generations. Persistent churn returns an explicit retryable discovery error.
A stable invalid descriptor remains an error, and the previous cache is retained
for a runtime rollback rather than returned for an incompatible new generation.

Keep initialize negotiation and tools capabilities unchanged: connected clients
refresh with standard tools/list. The composition updates injected keys after
addition/removal; calls use the resulting registry. Older runtimes without
version queries retain uncached discovery. No notification capability is claimed.

## Acceptance

- [x] The deterministic replacement-during-describe baseline returns only generation 2; persistent churn fails after bounded retries without tool effects.
- [x] One initialized real stdio MCP client sees schema replacement, addition and removal; a subsequent call runs the current provider and removed tools fail explicitly.
- [x] A failed provider replacement leaves the old usable catalog/call generation; re-list requires no notification support. Existing protocol, policy and cancellation tests pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test mcp
```

The owner unit gate invokes the live Bun test. Run `just check mcp` as well.
All profiles and source edits for live replacement occur in disposable fixtures;
configured real policy grants apply only to the fixture tools.
