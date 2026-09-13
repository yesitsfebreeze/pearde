---
complexity: medium
footprint:
  - src/file_kernel.rs
  - src/inventory.rs
  - src/lib.rs
  - src/context.rs
  - Cargo.toml
  - .cartridge/tests/unit/context.rs
  - .cartridge/docs/context.md
---

# A shared context snapshot retains bounded source evidence

Add the library context contract without changing legacy graph/search behavior.
Reference contains owner/kind/ID/revision and revision_kind (source_bytes or
observed_projection); Evidence adds source, text and selection_reason. Evidence
is untrusted data and has no callable descriptors or execution capability.
Candidate adds private visibility, filtered before validation, digest or diagnostics.
Contributor state distinguishes available, disabled, absent, unavailable, empty
and timeout; partial preserves valid rows with incomplete status. Source names are host-owned, not derived from private entity metadata.

An async Task owns one cancellation-safe producer future. Collect at most16 unique
contributors, sorted by name under one monotonic absolute deadline (1–2000ms),
including validation/selection. Never poll disabled/absent providers. Timeout drops
the future and names the partial source; no detached retry or process launch.
Producer adapters must bound transport/materialization themselves and avoid blocking
executor work; this library bounds accepted and retained evidence, not arbitrary
external provider allocation or interruption of blocking OS reads.

Accept at most128 candidates per contributor with at most8KiB text and bounded
identity/provenance fields. Exclude private rows before any public aggregation.
Invalid public rows and conflicting duplicate references fail that contributor
without copying its diagnostics. Canonically sort evidence by reference, deduplicate
identical rows and select at most64 rows within an exact serialized output budget
(4–64KiB including all metadata). Capacity omissions are explicit and incomplete.
Digest the final canonical public rows/statuses/limits; equivalent completed inputs
produce equal order/digest. Frozen readback requires the complete exact Reference;
a missing/stale identity returns no substitute and never performs another query.

The native memo adapter is an explicit memo-owned follow-up in the parent programme,
so each source change has its own owner receipt. This leaf proves the reusable
contract and cancellation deadline; the parent cannot finish before its real facade.

## Acceptance

- [x] Permuted equivalent completed contributions yield identical snapshots and exact frozen readback; changed evidence changes the derived revision and conflicting identities refuse.
- [x] Disabled, absent, unavailable, empty and timeout remain distinct; pending producer cancellation respects the one deadline and never dispatches disabled tasks.
- [x] Private bodies, IDs, metadata and digests cannot enter public output; output and candidate limits include metadata and preserve valid UTF-8.
- [x] Legacy graph suites remain unchanged; facade ownership and producer allocation/cancellation limits are documented without claiming integration not yet implemented.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test landscape
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check landscape
```

Use synthetic producers, paused/controlled asynchronous futures, private sentinels,
permuted snapshots and exact serialized byte assertions. No Memory store or model
is called by this contract suite.
