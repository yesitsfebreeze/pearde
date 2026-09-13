---
complexity: medium
footprint:
- src/commands/src/commands_health.rs
- src/commands/src/commands_admin.rs
- src/commands/src/lib.rs
- src/store/core/src/lib.rs
- src/store/core/src/cold.rs
- src/store/core/src/health.rs
- src/health/src/lib.rs
- src/transport/src/typed.rs
- src/transport/src/memory_rpc.rs
- src/rpc/src/server.rs
- .cartridge/tests/unit/src/commands/src/tests/commands_health_owner_test.rs
- .cartridge/tests/unit/src/commands/src/tests/commands_admin_test.rs
- .cartridge/tests/unit/src/store/core/src/health_test.rs
- .cartridge/tests/unit/src/health/src/lib/tests.rs
- .cartridge/tests/integration/e2e/cli_surface.rs
- .cartridge/docs/health-owner.md
- src/health/Cargo.toml
- .cartridge/tests/integration/e2e/health_surface.rs
- .cartridge/tests/unit/src/store/core/src/tests/legacy_test.rs
- .cartridge/tests/integration/e2e/focus_routing.rs
---

# Ask the selected store owner for bounded health

Measured source0a8736c already asks the daemon before graph bootstrap. The retained real CLI/socket baseline demonstrates the remaining gaps: accepts wrong-store777-thought reply; malformed reply creates a local empty store; absent and stale listeners also initialize local data; a stalled health reply exceeds an external1.5s cutoff. These are actual results, not completed acceptance. Retain inherited rounds1–2; request independent round3 before source edits. No owner-access/query adapter, readiness rewrite, daemon startup, event framework or storage format migration.

## Owner selection and deadline

Keep existing configured endpoint authority: MEMORY_DIR pins the endpoint root when set, otherwise the CLI cwd. Use the maintained Endpoint canonical path tagging and existing per-user endpoint trust checks. Resolve the expected store from Config.data_dir, not from the returned reply. Canonicalize both existing expected and returned data directories; a symlink alias of one existing store is equal. A returned path must be absolute, nonempty and exist; inability to resolve or different canonical identity is explicit incompatible/wrong_store, never a local-read fallback. Do not search arbitrary sockets or infer a store from path suffixes. Existing configurations with custom data_dir retain their daemon endpoint selection.

Add `memory health --timeout-ms N` only to this verb, default2000, accepted1..60000. Bound the entire connect + one health request + reply validation by one Tokio deadline; drop that one client on expiration. No automatic reconnect/retry and no new process. The underlying existing local socket wire remains unchanged; this deadline is a CLI RPC bound, not a universal filesystem or server-work cancellation guarantee. No claim that dropping the client stops daemon graph work. Config/canonical filesystem calls remain normal local calls; deterministic fixtures verify the RPC wait bound with scheduling margin.

Return a typed health outcome before printing any store gauges. Successful owner reply must have ok=true, compatible required identity, and a nonzero PID; zero/missing PID from a historical daemon is explicitly incompatible because generation cannot be named. The already-existing HealthRes additive fields remain tolerant for nonessential gauges. Print source=daemon, its PID and canonical store identity. An actual newly started successor answers with its own PID; EOF/disconnect during restart is unavailable/retryable and never fabricates successor completion. One invocation consumes exactly one reply.

Only a truly absent socket (NotFound) enters local inspection. ConnectionRefused at a present stale socket is unavailable/retryable, not absence. Authentication/untrusted endpoint, malformed/unknown-operation/not-ok reply, timeout and closed transport return nonzero `memory health:` diagnostics with stable status and retryable=true/false. Wrong identity/incompatible/malformed are not automatically retryable; stale/timeout/disconnect are retryable by the caller. No raw store contents in errors. No deletion of socket/lock, no writer claim, no mutation replay. Keep existing generic route behavior untouched.

## Local readonly snapshot

The prior fallback bootstrap calls Store::open and may create/migrate/stamp data, contrary to the leaf's stated readonly intent. Replace only health's fallback with a typed store-owned readonly snapshot reader. Reuse/extract the reviewed READ_ONLY LMDB open and maintained memory/kern decoder; normal reader lock-file coordination stays enabled. Read hot persisted memory rows and embedding metadata in one read transaction, preserving legacy table/row decoding without writes or repair. Return typed Memory rows plus EmbedRead using current formats; no graph bootstrap/index creation, cold-tier loading, model calls, background worker or watcher. Missing data, unknown tables, corrupt rows and nonempty graph without root fail explicitly; a valid empty database retains prior in-memory empty-root counting semantics without persisting that root.

Compute local counts, root focus labels, claim kinds, per-memory rows, largest memory and Gini using the same maintained health aggregation helper as the daemon over an equivalent resident row set. Refactor only that pure aggregation to share semantics, leaving daemon lifetime counters and normal dynamic gauges as currently implemented. Local max-memory cap comes from config; embedding stamp missing/corrupt/model/dimension mismatch stays explicit and does not adopt a stamp. Local dynamic daemon counters stay unavailable/zero according to existing printer behavior, and source=local identifies the reading. Preserve all existing health gauges and legacy recency rendering.

Hot persisted rows represent the offline snapshot; served rows represent the owner's current resident snapshot. Do not promise equal counts when the daemon has dirty/unloaded state. Equivalence proof uses the same seeded persisted/resident set and separately documents this boundary. Cold storage enumeration remains Graph CLI's distinct inspection view. Local read cost scales with persisted hot rows and has no machine-wide latency promise or speculative paging. Snapshot read errors never become successful empty health.

## Acceptance

- [x] Actual owner RPC and absent-listener readonly fixtures report equal memory/entity/reason counts for an identical seeded snapshot with root, child, edges and legacy rows; health rendering remains complete.
- [x] Instrumented injected local snapshot-loader counter is zero for successful served, wrong-store, malformed, timeout, EOF and stale endpoint paths; local path runs once only after absent endpoint. A loader that panics proves it cannot be reached on served paths. Real CLI custom endpoint fixtures exercise the same branch.
- [x] One configured RPC deadline bounds stalled response, no retry is observed, and timeout produces nonzero explicit retryable status. Record small fixture timings separately. Actual owner restart yields an explicit failed in-flight attempt or the new successful PID; the next invocation can succeed without lock/socket deletion.
- [x] Canonical aliases match, different stores refuse, missing identity/PID is incompatible, and hostile/malformed reply does not print its counters or initialize a local store. No serving failure falls back.
- [x] Existing store data bytes/stamp and writer.lock identity/content are unchanged by both served and local paths, including held-writer readonly inspection. Missing store stays missing, legacy readonly decoding works, corruption remains explicit. Normal LMDB reader coordination is allowed; no no-filesystem-activity claim.
- [x] Public Memory test/check pass together with existing Graph, writer-boundary and CLI ingestion regressions. No formats or other verb semantics change.

## Verify

```sh
set -eu
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary cargo test -p commands health_owner -- --nocapture
```

```sh
set -eu
health_proof_log=$(mktemp /tmp/memory-health-full.XXXXXX)
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just test > "$health_proof_log" 2>&1 || { tail -80 "$health_proof_log"; exit 1; }
tail -25 "$health_proof_log"
shasum -a 256 "$health_proof_log"
```

```sh
set -eu
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just check
```

Use disposable stores and owned subprocesses; retain exact fixture source, logs, source revision and input hashes. Coordinator owns lifecycle/collection. Reverting this health-only adapter requires no store rewrite. Source implementation waits for writer leaf collection and independent round3 review.
