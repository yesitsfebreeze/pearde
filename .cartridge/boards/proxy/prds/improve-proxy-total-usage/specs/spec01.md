---
complexity: medium
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/usage.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/usage.md
- Cargo.toml
- cartridge.json
- src/context.rs
- src/wire.rs
---

# spec01 — One bounded usage ledger across JSON and streaming rounds

Add opt-in `usage_accounting` configuration, default false. Keep existing native
wire fields and caller history semantics unchanged. The additive `cartridge_usage`
report is the consistent cumulative contract: provider-reported input/output
counts, separately identified final attempted round, completed/reported round
counts, completion state and bounded incomplete reasons. It reports token counts,
not prices or an invented provider billing total. Native provider-specific cache
and reasoning fields retain their existing meanings outside this extension.

Use one request-owned ledger for JSON and all three streaming protocols. Begin a
round before the router attempt, observe only real provider usage, merge repeated
cumulative snapshots instead of adding each event, and finalize a round once.
Missing/invalid counters remain unknown; observed zeros remain valid. Use checked
arithmetic and label overflow without presenting saturation as an exact total.
Capture usage from partial/error events before returning an error. No retry,
extra model request or source-history mutation is introduced.

Attach the same cumulative report to JSON success/error and the final native SSE
usage/completion or error event, exactly once. Preserve existing default wire
responses when disabled. Keep the latest 128 completed/error/cancelled reports in
memory, accessible to trusted native `proxy {op:"usage",id}` callers. A report
has an opaque request ID; expose it in enabled HTTP response headers/metadata so
cancellation can be inspected when the connection can no longer receive an error.
Unknown/evicted IDs fail explicitly. Reports contain counters/status only, not
request bodies, credentials or arbitrary provider objects. A request-owned drop
guard archives known counts as incomplete on cancellation. Restart loses this
bounded telemetry; no durable session or continuation mapping is changed.

## Acceptance

- [x] Three-round Chat, Anthropic and Responses fixtures produce matching cumulative JSON/SSE counts and distinct final-round counts, with exactly one final report and no double counting of repeated usage events.
- [x] Missing/invalid usage, zero counts, overflow, partial stream failure and deadline/client cancellation preserve known counts and label incomplete accounting. Cancellation still targets the exact active tool and releases router leases.
- [x] Disabled telemetry preserves current native responses; enabled success/errors expose a bounded report, missing/evicted IDs fail explicitly, and existing caller-history/private-tool/continuation fixtures pass unchanged.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test proxy
```

Also run public proxy check and the existing GitFS interoperability/real-policy
consumer gates after integration. Reuse the current loopback streaming fixture,
including chunk splitting and completion gates. No live model is needed for
usage accounting; source-bound baseline probe and expected/observed counts are
recorded in baseline-inputs.json and baseline-log.txt.
