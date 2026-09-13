---
complexity: medium
footprint: [".cartridge/tests/integration/e2e/cli_surface.rs","Cargo.toml","src/cartridge.rs","src/transport/src/lib.rs","src/transport/src/owner.rs","src/transport/src/typed.rs","src/transport/src/memory_rpc.rs","src/commands/src/commands_health.rs",".cartridge/tests/unit/src/cartridge/tests.rs",".cartridge/tests/unit/src/transport/src/owner_test.rs",".cartridge/tests/unit/src/commands/src/tests/commands_health_owner_test.rs",".cartridge/tests/integration/cartridge.rs",".cartridge/docs/owner-attachment.md","src/cartridge_status.rs",".cartridge/tests/unit/src/cartridge/status_test.rs","src/store/core/src/lock.rs",".cartridge/tests/unit/src/store/core/src/tests/lock_test.rs","src/store/core/Cargo.toml","Cargo.lock","src/rpc/src/server.rs",".cartridge/docs/CARTRIDGE.md"]
---

# Attach explicit native readers to the existing Memory owner

Measured baseline439bea5 with two real SDK Memory processes and an isolated deterministic embedding HTTP fixture: the first ingests and retrieves CEDARQUARTZ; a second configured to a canonical alias of the same store fails query in101ms with the existing writer refusal. The writer label remains unchanged. Source confirms native Engine is exclusively local and publishes no peer listener. Existing daemon MemoryRpc already supports the necessary owner reads. Preserve inherited rounds1–2; independent round3 precedes implementation.

## Bounded attachment scope

Add optional trusted native configuration `owner: {endpoint: string, timeout_ms: integer}` beside required `dir`. Its presence selects an explicitly attached reader; absence keeps the existing lazy local Engine and writer/replacement behavior unchanged. Defaults: timeout2000ms, permitted1..60000; endpoint nonempty<=4096bytes, absolute local Unix socket path or the maintained local Windows named-pipe shape. Reject extra owner keys, remote pipe names and malformed types at apply time. In attached mode accept only dir and owner configuration; reject explicitly supplied local-engine/model settings instead of silently ignoring them. The serving owner's existing model configuration governs retrieval.

Owner endpoint comes only from trusted native config, never an operation argument, store row, source reference or inferred filesystem scan. Apply validates configuration without connecting, creating a directory, opening the graph, loading models or taking a writer lock. Do not add a listener to a native cartridge, publish discovery metadata, spawn a daemon, alter installed profiles or change the CLI daemon protocol. Two cartridge clients may attach to one existing daemon. A caller who instead chooses the default local-owner mode retains exclusive-writer refusal while another owner holds the store.

Attached mode permits only query/search/get plus health/ready reads. Validate this strict allowlist before any backend connection or Engine initialization. Existing get-to-query normalization and query argument/result semantics remain; do not wrap a raw arbitrary InvokeReq or accept an alternate operation name in the payload. Explicit mutation/admin methods, including ingest/operator_ingest, link, forget/by-source, degrade, move, promote, focus, claim_kind, pulse, gc, audit, queue_drain, shutdown and idle_stop, fail with readonly_attachment before connection. Unknown operations also fail. Normal owner-side retrieval access/heat telemetry remains part of the existing query API and stays under the owner's writer authority; attached clients never mutate the store directly.

## One verified transport per read

Factor the health leaf's pure canonical store/PID validation into a small maintained transport-owned helper used by both health CLI and attached native reads. This avoids a divergent identity language. Preserve health CLI status/deadline/no-local-fallback behavior and its executable regressions. The helper takes the configured expected data directory and typed HealthRes, requires ok, nonzero PID and absolute existing directory identity, and compares canonical paths; aliases match, regular files and missing/wrong paths refuse. It does not choose capabilities or endpoints.

For each allowed attached call, create one client using the current endpoint ownership/peer checks. One absolute Tokio deadline covers connection, one health identity request, and one allowed read invocation on that same client. Health can return the verified handshake value directly; ready may invoke the existing narrower ready operation after the identity check. Do not hand off to a newly connected transport between validation and read, and do not cache a success across calls. Preserve the validated owner PID in failure context. Same-channel disconnect/restart returns explicit unavailable/retryable; a later explicit caller can connect to a successor and validate its own PID. Never retry a read automatically and never infer that a timed-out request did not run on the owner.

The helper exposes static bounded error status/retryability for absent/stale/refused/incompatible/wrong_store/malformed/timeout/disconnected/operation_failed. Keep backend/provider error bodies and configured credentials out of attachment diagnostics. All failure paths remain attached: no local Engine::open, writer claim, graph load, endpoint unlink, data rewrite or mutation replay. PID identifies the generation observed on the verified local transport; it is not independent authentication. Existing per-user socket ownership is the local authorization boundary. Deadline limits asynchronous RPC wait, not synchronous filesystem stalls or owner work after client drop; the existing codec remains unchanged.

Native admission/disposal keeps the existing CALLS guard. Attached calls release it after the bounded exchange and dropping their client. Disposing an attached cartridge does not call the daemon's shutdown or local Engine::shutdown; the owner and another attached client stay usable. Local-owner disposal retains its existing behavior. No readiness orchestration API or automatic recovery loop is added here; the separate readiness leaf owns registration-versus-readiness status.

## Acceptance

- [x] One actual daemon owns a seeded disposable store; two independent actual SDK cartridge processes in explicit attached mode retrieve the same seeded fact, including a canonical alias. Neither creates a second writer or a local engine; the owner's lock identity/label and PID remain unchanged.
- [x] Mutating/admin/unknown operations are rejected before connection with a zero-server-call assertion, including native operator_ingest and payload attempts to substitute operation/endpoint. No ingestion is forwarded or replayed. The default local mode's existing replacement/exclusive-writer and persistent-data tests remain unchanged and pass.
- [x] Exact transport fixture proves health then allowed invocation on one connection and at most one invocation; wrong-store, missing PID, non-directory identity, malformed/refused response, stale socket and blocked response yield explicit bounded outcomes without local fallback. Timeout's total budget includes handshake and read, not two full budgets.
- [x] Actual owner crash interrupts a client call explicitly; a later caller observes the successor only after new identity validation. Disposing one attached cartridge leaves the owner and the other reader available. Wrong-store and absent endpoints do not create storage or delete lock/socket paths.
- [x] Current formats, retained legacy reads, configured endpoint behavior, native local-owner lifecycle and health-owner regression fixtures pass at the same revision. No persisted schema changes or runtime profile installation are needed; removing owner config restores existing local-owner semantics, subject to the unchanged writer claim.

## Verify

```sh
set -eu
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary cargo test -p memory --test cartridge owner_attachment -- --nocapture
```

```sh
set -eu
owner_proof_log=$(mktemp /tmp/memory-owner-full.XXXXXX)
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just test > "$owner_proof_log" 2>&1 || { tail -80 "$owner_proof_log"; exit 1; }
tail -25 "$owner_proof_log"
shasum -a 256 "$owner_proof_log"
```

```sh
set -eu
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just check
```

Retain exact source/input hashes, baseline and executable fixtures. Use only disposable data and owned processes; no installed owner or user store is probed. Source is held until prior health/writer receipts settle and this plan passes independent review. Coordinator owns shared map, lifecycle and collection. No exception to ownership or accepted data compatibility is needed.
