---
complexity: medium
footprint:
  - src/catalog.rs
  - src/decision.rs
  - src/proxy.rs
  - src/telemetry.rs
  - src/main.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
  - .cartridge/tests/unit/telemetry.rs
  - .cartridge/docs/cost-latency.md
---

# spec01 — Attribute estimates and observed usage to each actual attempt

Extend opt-in decision records with bounded attempt observations. Capture monotonic
elapsed milliseconds, wall-clock observation time, raw provider token snapshots,
completion scope and per-route declared pricing. Usage snapshots replace prior
values; absent/invalid/decreasing counters remain explicitly unknown or invalid,
never invented zero. Observe before the existing lossy wire normalization and
avoid counting replay of buffered first-output events twice.

Optional `routing.pricing` is keyed by exact route ID. Each declaration supplies
nonnegative finite USD input/output rates per million tokens and positive
`observed_at` timestamp. Source is fixed `operator_declared`; record age and rate
snapshot, invalid/future declarations are unknown. Legacy model-level price tuples
have no provider/source attribution and are not used. Pricing participates in the
captured policy revision; no network price lookup or routing preference change.

Each actual attempt gets a preflight cost estimate only when explicit output
budget and heuristic input bound are available, and a separate observed-usage
cost estimate only when both valid counters and rates exist. These are approximate
estimates, never invoiced charges; cache/reasoning billing is not inferred. Failed
attempts retain observed usage if present, otherwise unknown. Totals count each
attempt once; any incomplete/unknown/omitted attempt makes total cost unknown,
while separately labelled known-cost subtotal remains useful. Skipped routes cost
nothing in this ledger because no attempt was made; that is not a billing claim.

At most 64 attempt observations are retained in the existing latest-128 archive.
Cancellation snapshots known active usage with incomplete status. Streaming
receipts remain immutable `stream_started` observations at first-output handoff,
with partial usage and latency-to-handoff; no final delivery/cost claim. Native
preflight discovery exposes pricing source/age and estimates, clearly without
observed attempt latency. Old stored records keep original timestamps and prices.

## Acceptance

- [x] Real fallback names two attempts with distinct durations, captured pricing/age and known/unknown observed usage; subtotal does not double count snapshots.
- [x] Missing, malformed, negative, future and stale pricing are explicit; estimates differ from measured usage; zero usage is distinct from absent and invalid/decreasing counters.
- [x] Equivalent/default wire behavior, failed and cancelled work, first-output buffering, all three wire usage schemas and streaming handoff remain honest and bounded.
- [x] Price change/rollback updates/restores policy revision without rewriting old records; attribution redaction, capability and existing consumer gates pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test router
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check router
```

Use loopback provider fixtures and synthetic declared rates. Deterministic token
snapshots and elapsed-time relationships avoid external billing claims or sleeping
to hit timing thresholds. Reverify both completed overlapping router receipts.
