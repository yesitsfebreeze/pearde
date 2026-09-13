---
complexity: medium
footprint:
  - src/health.rs
  - src/proxy.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
  - .cartridge/docs/recovery.md
---

# spec01 — A route incident has one finite automatic recovery budget

Give each new incident a persisted recovery identity, at most three probes and
an absolute180-second lifetime from first failure. Repeated foreground failures
preserve that identity/budget. A later verified foreground success closes it;
a subsequent failure may create a new incident. Foreground user requests remain
separate work and do not replenish automatic recovery. A per-service exclusive
sweep guard coalesces concurrent recovery calls; at most four distinct eligible
routes are processed per sweep so terminal incidents cannot starve others.

Reserve and persist an attempt before any probe. Persistence failure refuses
probe dispatch and exposes degraded status. Each probe is bounded by15 seconds,
remaining incident lifetime and request limits, covering headers through complete
stream collection. Wall-clock rollback or malformed/legacy budget state is
explicitly degraded, never a fresh automatic allowance. Persisted in-flight work
on restart and abandoned work found by the next exclusive sweep become degraded
with unknown outcome; no automatic replay. One health-store writer is assumed,
not distributed recovery coordination between independent processes.

Missing route/credentials, quota/payment authority, request-specific context
failure or no safe compatibility adjustment is a visible degraded/exhausted
outcome. No diagnosis model is called when no supported diagnosis path exists.
Existing allowlisted compatibility rules are only candidates: full fixture
response completion and valid tool arguments on the exact affected route must
succeed before rules activate. Recovery collection suppresses normal health
side effects until the same incident identity is verified, so an obsolete probe
cannot overwrite newer foreground health. Raw caller conversation/tool work
is never replayed; only the existing synthetic structural probe is sent, and
probe tool calls are validated but never executed. No code/config changes,
credential changes, external agent launch or Memory routing are introduced.

## Acceptance

- [x] Repeated and concurrent sweeps use at most three persisted attempts for one incident; fresh failures and restart do not reset its budget; deadlines/persistence failure refuse further probes.
- [x] Missing route/auth/diagnosis and exhausted incidents expose explicit reasons; other eligible routes still receive bounded work.
- [x] Real exact-route SSE completion (including valid/invalid tool cases) controls recovery; partial stream/timeout/cancel remains unrecovered and an obsolete probe cannot overwrite newer incident state.
- [x] Foreground requests remain interrupted on failure, no caller/tool mutation is replayed, old health snapshots load explicitly, and existing admission/decision/cost/protocol/consumer gates pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test router
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check router
```

Loopback fixture providers, deterministic retry timestamps, semaphore-controlled
pending streams and temporary health files prove budgets/coalescing/failures.
No live model or user health store is touched. Refresh completed overlapping
router receipts after integration; historical audit remains pinned to its source.
