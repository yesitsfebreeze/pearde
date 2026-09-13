---
complexity: medium
footprint:
- Cargo.lock
- src/store/core/Cargo.toml
- src/cartridge.rs
- src/cartridge_status.rs
- src/commands/src/memory.rs
- src/transport/src/owner.rs
- src/transport/src/memory_rpc.rs
- src/store/core/src/lock.rs
- src/rpc/src/server.rs
- .cartridge/tests/unit/src/cartridge/status_test.rs
- .cartridge/tests/unit/src/cartridge/tests.rs
- .cartridge/tests/unit/src/store/core/src/tests/lock_test.rs
- .cartridge/tests/unit/src/transport/src/owner_test.rs
- .cartridge/tests/integration/cartridge.rs
- .cartridge/tests/integration/e2e/cli_surface.rs
- .cartridge/tests/integration/e2e/focus_routing.rs
- .cartridge/docs/owner-attachment.md
- .cartridge/docs/CARTRIDGE.md
---

# Native readiness without starting a writer

Baseline at f9759848c56255ee0607587970f58ccc087ade53: real SDK registration precedes storage creation, but native ready starts a writer in9.338ms; a second registered local client gets a writer refusal in101.604ms. No native status operation exists. After the original owner exits, ready opens a writer in the same second caller. Explicit attached missing-owner ready already fails bounded without creating storage. Preserve inherited rounds1–2 and owner-access behavior; request independent round3 before source edits.

## Additive status contract

Add native `{"op":"status","probe":false}`. Existing native ready/health and daemon CLI/RPC contracts retain their behavior. Status is dispatched locally before attachment's backend allowlist, never sent as an arbitrary daemon invoke. Only op, optional boolean probe and optional integer timeout_ms are accepted. timeout_ms is valid only with probe=true, range1..60000, default2000; attached probes also respect the smaller configured owner timeout. Reject unknown fields/nested routing/type/range errors before I/O. No new capability or runtime profile is needed.

Reply is a bounded object with schema=memory.status.v1, registered=true, mode=local|attached, view=cached|probe, observation=none|operation|probe, age_ms (null before observation), state=unknown|starting|ready|degraded|unavailable, static reason and retryable. It also separates store state and owner PID, exact-ID read availability, semantic-query availability, and model availability. Availability values are unknown|ready|degraded|unavailable. An uninitialized store is starting; registration alone is unknown. No raw config, endpoint, store path, writer label, model error or query text appears in status. The model section always says actively_probed=false and availability=unknown; bounded existing failure counters are observations, not current model reachability.

Default cached status only reads bounded in-process metadata. It never checks files, connects, starts a writer or calls a model. Its age is elapsed monotonic time since its underlying observation, not time since rendering. It does not disguise a cached probe as fresh. Cache is local to this applied service/configuration and contains only one latest store observation and one latest semantic-query result (PID, success/failure and timestamp), never payloads or errors. An observation may become stale between calls; all replies explicitly state their observation age.

Query readiness is evidence-qualified: an initialized local engine or verified live attached owner can establish store/exact-ID route readiness, not model or semantic-query readiness. Only a successful actually dispatched semantic query in this caller, on the same observed owner PID and within30seconds, establishes semantic-query ready. A dispatched semantic query failure within that window yields degraded with static last_query_failed; it makes no claim about whether the model caused the failure. Expired evidence or a changed PID yields unknown. Observe only query with nonempty text and without an ID selector; validation failures and get/search do not pretend to establish semantic readiness. No artificial query or model call is issued by status. Assign monotonically increasing observation tickets at probe/query admission; publish only if no newer observation has started, so an old transport completion cannot replace a successor probe. Overall ready requires current observed store readiness plus this same-PID recent semantic success; otherwise name unknown/degraded/unavailable/starting as appropriate. Existing lifetime failure counters are separately named and cannot promote readiness. This is a recent observation, never a guarantee that the next request succeeds.

## Explicit bounded probes

A local probe first checks the existing ENGINE cell without initializing it. If initialized, use the existing graph-free ready snapshot under CALLS admission, validate required ok/PID/draining fields, and retain only whitelisted booleans/counters. Do not load the graph, recompute health or expose raw last_llm_complete_failure. A draining owner is unavailable/retryable. The stored semantic evidence remains separately aged and is not refreshed by polling.

If local ENGINE is not initialized, call a small store-owned lock-availability observer. Open only an already-existing regular writer.lock, without create/truncate/write, and perform one immediate nonblocking try-lock then drop. Never call acquire(), holder(), read a label or turn a lock result into authority for a store mutation. A held lock means unavailable/writer_busy and retryable; missing/free means starting/local_uninitialized and query unknown. Unreadable/non-regular lock means unavailable/lock_unreadable, with static diagnostics. This momentary advisory-lock sample starts no writer, changes no label or inode, and is never authorization to load a graph. Existing holder/acquire semantics stay unchanged. When the other owner exits, a later explicit probe in the same caller observes the change to uninitialized; it still does not start an engine. Normal non-status work remains responsible for initialization.

An attached probe reuses owner-access's same-client health identity handshake plus ready invocation and its canonical store/PID validation. All connection, handshake and ready wait share the status deadline. Validate required ready ok, nonzero matching PID and boolean draining before accepting the snapshot; malformed fields fail explicitly. Do not infer readiness from the presence of an endpoint. Adapt static OwnerError fields directly; never parse or echo raw error strings. Missing/stale/wrong-store/refused/malformed/disconnected/timed-out owners yield unavailable with the existing retryability semantics and observed PID when available. There is no fallback to local Engine, socket deletion, automatic retry or daemon startup. Later explicit probes can observe a successor without restarting the caller, invalidate old-PID query evidence and report newly observed store state.

Expose a small metadata-returning owner read variant so the native caller records the PID validated on the same transport as a successful semantic request. Preserve existing read() callers with a value-only wrapper; no second connection or inferred PID. This metadata addition does not change wire data or backend dispatch semantics.

Status uses one bounded probe permit per service; a second concurrent probe returns starting/probe_in_progress without launching more work. Cached status remains available while a probe is blocked. One deadline covers CALLS admission and async wait; local filesystem probing runs in one blocking worker whose permit and CALLS guard remain held until it actually exits. If the caller times out, report timeout without claiming the worker stopped; do not detach an unbounded sequence of probes or publish its late result over a newer observation. Normal async transport clients drop within the deadline. Disposal retains existing call-drain behavior; an indefinitely blocked filesystem syscall is not promised cancellable. Status never starts model/background work, mutates store data or changes current formats.

## Acceptance

- [x] Actual SDK fresh local registration returns cached unknown with no store creation, lock, graph, endpoint connection or model request. Explicit status probe on a missing/free store reports starting/query unknown and preserves absence/lock bytes/inode; legacy ready/health behavior remains compatible.
- [x] With an actual owner holding a seeded store, a second registered native local client reports unavailable/writer_busy/retryable under probe. After owner exit, the same caller observes starting/uninitialized without creating a writer. Normal query can then initialize it and a successful semantic query establishes fresh readiness; cache age increases and probing alone never refreshes semantic success age.
- [x] Two actual attached SDK clients can observe the real daemon; disposal of one leaves the other/owner usable. Crash/absent/stale/wrong-store/malformed/draining/timeout results are bounded and named, preserve paths/lock state, and a later same-caller probe validates a successor PID and invalidates old query evidence. Model unknown and lifetime failure counters never masquerade as active model probing.
- [x] Deterministic status/transport fixtures prove cache has zero I/O, a single total deadline, at most one in-flight probe, concurrent cached responsiveness, late-result refusal, no raw credentials/error/query text, strict request validation, same-client PID metadata, and no inference/model requests. Synthetic credential-bearing config/backend errors remain absent from every serialized status path.
- [x] Public just test/check and existing owner-access, health, native local lifecycle, Graph, writer and legacy-format regression gates pass at the same revision. No protocol/profile/schema migration or persisted data rewrite is required; removing additive status restores the prior surface without touching storage.

## Verify

```sh
set -eu
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary cargo test -p memory --test cartridge readiness_status -- --nocapture
```

```sh
set -eu
readiness_proof_log=$(mktemp /tmp/memory-readiness-full.XXXXXX)
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just test > "$readiness_proof_log" 2>&1 || { tail -80 "$readiness_proof_log"; exit 1; }
tail -25 "$readiness_proof_log"
shasum -a 256 "$readiness_proof_log"
```

```sh
set -eu
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just check
```

Implementation uses an isolated Memory worktree after independent review and coordinator source release. Retain baseline, exact inputs, failed-gate diagnosis and final proof. Coordinator owns shared lifecycle/map/collection. Original acceptance and inherited review history remain intact.
