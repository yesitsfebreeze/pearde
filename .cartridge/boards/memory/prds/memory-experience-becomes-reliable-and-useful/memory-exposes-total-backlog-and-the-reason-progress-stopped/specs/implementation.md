---
footprint:
  - "src/store/core/src/lib.rs"
  - "src/store/core/src/experience.rs"
  - "src/rpc/Cargo.toml"
  - "src/rpc/src/server.rs"
  - "src/rpc/src/experience/mod.rs"
  - "src/rpc/src/experience/drain.rs"
  - "src/rpc/src/crystallization_cycles.rs"
  - "src/commands/src/memory.rs"
  - "src/cartridge/src/status.rs"
  - "src/cartridge/src/asp/mod.rs"
  - "src/rpc/src/experience/view.rs"
  - "src/cartridge/build.rs"
  - "src/cartridge/build_identity.rs"
  - "src/cartridge/Cargo.toml"
  - "Cargo.lock"
  - "cartridge.json"
  - ".cartridge/tests/unit/src/store/core/src/experience_test.rs"
  - ".cartridge/tests/unit/src/rpc/src/experience_test.rs"
  - ".cartridge/tests/unit/src/cartridge/status_test.rs"
  - ".cartridge/tests/unit/src/cartridge/build_identity_test.rs"
  - ".cartridge/tests/unit/src/commands/src/memory_test.rs"
  - ".cartridge/tests/integration/asp.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Authoritative backlog and progress status

## Scope and evidence

The writer prerequisite is collected at memory source `d9161cd2f3a363915c7a7d642a4955e7a3836065`. Reuse its coordinator, guarded commit and explicit operator-required divergence. The completed investigation and round 1 review establish the historical-row undercount and the separation between successful semantic queries and writer progress. This leaf repairs those observations, not intake fairness, event acceptance, retrieval ranking or arbitrary graph reconciliation.

Only the exact footprint above is authorized. Store initialization and transactional metadata own durable progress; RPC projects it; the native status adapter and ASP consume the same projection. The small commands change records the scheduler's actual next attempt. The cartridge build script owns the native module's embedded input identity. No host/runtime API, sibling implementation, independent ledger or public alternate status endpoint is introduced. Preserve every earlier review. Start the implementation lane from the verified source HEAD, not the unrelated live dirty tree. The Scope owner handoff at /tmp/memory-stack-scope-readiness/owner-reply.md explicitly excludes memory-provider edits, so the reviewed memory HEAD remains d9161cd. Recheck HEAD and claims before lane creation; preserve unrelated dirty provider changes using committed verification. A later owner baseline change requires a provenance note and targeted contract review, not absorption of arbitrary dirty changes.

## Durable metadata and migration

Introduce one versioned progress metadata record in the existing experience intake database. It is the authoritative source for live rows/bytes, historical rows/bytes, delivery receipts, durable last successful experience commit time/epoch and cumulative processed rows since this metadata version was initialized. Total pending rows/bytes are the checked sum of live and historical. Historical means the six existing raw, part, day, week, month and year prefixes; live means the inbox prefix. Do not change pending selection order, quotas, receipts, acknowledgements or deduplication identity in this leaf.

Initialize the metadata once, transactionally, during writable Store::open before exposing the Store. An existing store is scanned once across the seven pending prefixes and receipt prefix. Replace the superseded intake-stats record in that same transaction; there is no permanently dual counter authority. A new empty store receives a known zero record. Existing metadata with unsupported version, invalid encoding or inconsistent arithmetic causes an explicit initialization error; do not overwrite corrupt authoritative metadata with an apparently empty store. Failed migration rolls back without changing inputs, receipts or graph data. On a retry after crash, absence of the committed version resumes the complete atomic migration. Read-only/status calls never initiate migration or repair. The previous legacy experience_stats return shape can project live counts and receipts from the new authority for compatibility.

All enqueue, import, commit and receipt-prune transactions update this metadata atomically. Imports handle exact overwrite byte deltas and must not increment row counts for an existing key. Duplicate delivery changes neither pending counters nor durable progress. Removal subtracts only existing selected inputs. Successful experience_commit records the wall-clock commit timestamp, returned graph epoch and actual removed row count in the same LMDB transaction as graph/receipts/input deletion. A stale refusal, failed transaction, ordinary graph flush or an empty pass cannot advance experience progress. Never fabricate historical last-commit time from current epoch or migration time. Report it as null until the first successful experience commit under this schema, with the explicit origin `since_progress_schema`.

Maintain a small ordered timestamp index in the same database and transaction, containing only timestamp and pending key, not a second copy of payload/evidence. The first index item gives the earliest known event time; deletion of the oldest item remains an indexed lookup. Use the inbox key's accepted event timestamp. For historical input use only an explicit valid original timestamp in the stored representation; condensed records without one are unknown. Never use the decoder's synthesized current time. Metadata counts rows with unknown timestamps. Define `oldest_pending_age_ms` as event age, not queue residence; it is null when the backlog is empty or any pending timestamp is unknown, accompanied by `oldest_known_event_at_ms` and `unknown_age_rows` so known partial evidence remains visible. Future timestamps produce age zero by saturating subtraction and remain unchanged in storage. Polling reads at most the metadata record and first timestamp index item; it never decodes pending payloads or enumerates receipts.

## Canonical observation contract

Extend the existing trace action `status` additively. Retain the existing pending:{rows,bytes} object and its live-inbox semantics, receipts, capacity, batch limit, storage and writer fields. Add an `experience` object with schema `memory.experience.status.v1`:

- `availability` is `available` or `unavailable`, with a bounded machine-readable reason when unavailable. Unknown counts/times are null, never zero.
- `backlog` contains live, historical and total objects with rows/bytes, plus oldest_pending_age_ms, oldest_known_event_at_ms, unknown_age_rows and age_basis `event_timestamp`.
- `progress` contains last_commit_at_ms, last_commit_epoch, processed_rows_since_initialization and origin `since_progress_schema`. Before a known commit, the first two fields are null.
- `writer` is the collected ready/coordinating/blocked contract; unavailable graph or metadata observations are explicitly unavailable and cannot become ready by default.
- `attempt` contains process-local generation, last_attempt_at_ms, last_error (bounded code/message or null), retry state and next_retry_at_ms (null unless actually scheduled). Retry states distinguish idle, running, scheduled, operator_required and unknown. Error messages are capped at 512 UTF-8 bytes without splitting characters; no payload text is included.
- `cycles` states process_local=true, generation, completed_retention=64 and event_retention=128. Summaries do not clone or enumerate the retained journal.
- `owner` reuses graph-free readiness_stats identity fields build_id, build_stamp, config_id, pid and uptime_ms, plus the additive graph-free experience_generation; those identify the serving process according to their existing semantics, not the native binary digest.

Use graph.try_read rather than waiting behind crystallization's graph write lock. Every graph acquisition and reacquisition in status helpers, including writer status, must be nonblocking; an initial try_read followed by a blocking helper read does not satisfy this contract. A busy graph produces bounded unavailable/graph_busy, while native serving/query state can remain independently known. Do not hold a graph guard while waiting for the store coordinator. Reuse the writer's nonblocking coordinator acquisition and fallible epoch read, preserving stale-snapshot protection. A corrupt progress record at read time yields unavailable, not a repair scan. If bootstrap fell back to a graph without a persistent Store, report unavailable/no_store rather than an empty durable backlog. No status path calls models, changes heat/recurrence, opens an engine, or emits intake activity.

Record attempts and errors for idle, early failure, blocked and completed paths in the existing process-local cycle journal. Keep attempt observation separate from durable progress. The background commands loop records its actual chosen retry deadline after each pass; manual trace/crystallize calls do not create a claimed scheduled retry and cannot erase a deadline independently owned by the background worker. Store attempt outcome separately from scheduler state; only that scheduler may set, consume or clear its own pending deadline. A manual success may clear its attempt error while preserving the still scheduled worker wakeup. Operator-required divergence has no promise of automatic repair even if the existing worker wakes to observe it again. A new successful ordinary or semantic query cannot clear a blocked writer or a remembered crystallization error. Restart resets attempts/journal with a new generation but preserves durable backlog/progress. A successful later experience attempt clears its own error; bounded observation errors do not rewrite the durable commit record.

## Native status and ASP

Keep `memory.status.v1` and existing store/query/models fields compatible. Add the canonical experience object with its own observation age and owner generation, and `module_identity` as defined below. Query success must not refresh or replace the experience observation. Preserve the existing 30-second semantic freshness window, cached versus probe modes, strict option validation, ticket ordering, deadline bounds and permit lifetime through completion of timed-out blocking workers. An uninitialized native service reports experience unavailable/not_observed without opening Store or Engine. A probe uses the existing owner transport to obtain readiness and trace status under one configured total deadline, including the attached health preflight and every subsequent read. The existing attached handshake may wait on graph-locking health_stats, so attached/native probes promise bounded timeout/unavailable by the configured deadline rather than the local 100-millisecond graph_busy result. Do not repair or broaden the transport handshake in this leaf. Tests hold the remote graph writer through the health preflight and prove the complete probe times out under that single deadline; no per-read deadline reset is allowed. Add experience_generation to the existing graph-free readiness_stats response using the same per-engine Cycles generation already projected by experience.owner and cycles. Detect owner PID or experience_generation changes between readiness and progress observations and report owner_changed unavailable rather than joining different engines, including replacement inside the same PID. Key the native experience observation by both PID and generation. Query success without generation information must neither refresh nor erase the previously observed experience generation. A wire-level native probe regression must exercise the same PID with different ready/progress generations; changed PID alone is insufficient. Attached mode never substitutes the adapter host identity for the remote serving owner.

Reserve `memory:status` in the native ASP dispatcher before generic memory fact expansion. The native adapter calls the existing observational `op:"status", probe:true` under its configured deadline and wraps the canonical experience payload, so an uninitialized service cannot fall through the lazy trace engine opener. Direct RPC trace/ASP expand retains its required nested `op:"expand"`; its answer branches before graph enumeration and projects the same canonical experience payload into a declared `memory.status` node attribute. The memory root advertises this status entity. Status expansion must not execute semantic/fact lookup or sort recent memory. Root expansion otherwise retains its existing behavior. This is an additive ASP entity/attribute; declare it in cartridge.json and document it. Preserve exact-query/readback behavior, the existing tool.memory query-deposition exception and the attached-owner read-only boundary. No broader transport policy or readback API changes belong here.

The native adapter adds its module_identity to the native status projection and ASP status node, while the canonical experience.owner remains the serving process. Raw RPC does not claim to know the adapter module identity. Thus Scope can consume one canonical status entity and distinguish its observing module from its local/attached owner.

## Honest embedded module identity

Generate `build_input_sha256` at compilation in src/cartridge/build.rs using one small pure helper in src/cartridge/build_identity.rs. Preserve existing platform Lua linker options. Embed the fingerprint in the native module; runtime never recomputes it from files currently on disk. Label scheme `memory-build-input-v1`, kind `build_input_sha256` and binary_digest=false. This identifies compiled memory inputs, not an assertion about the final dynamic library bytes.

Hash sorted repository-relative paths and bytes with unambiguous length framing: root Cargo.toml, Cargo.lock, actual cartridge.json embedded by the crate, all src/**/Cargo.toml and src/**/*.rs including the script/helper, and present .cargo configuration/rust-toolchain files. Include deterministic rustc -vV, target, profile, enabled features and relevant Rust compilation flags in a separately framed section. Exclude .git, .cartridge/tests, target/build outputs, absolute checkout paths, HEAD, mtimes, wall clock and OUT_DIR. Publish only the digest and scheme, not environment values. Emit rerun directives for every input and containing source directory so adding a source file invalidates the identity. A missing required input or failed hash fails compilation rather than silently publishing a dummy identifier. Add sha2 as a build dependency, reusing the workspace version.

Fixture tests prove reproducibility across differently named checkout directories, path/content framing, included source/config/manifest changes, excluded output/mtime changes and deterministic compilation inputs. A native test verifies the embedded value remains fixed while fixture source changes produce a different candidate identity. This is not proof of actual loaded dylib bytes: the parent's controlled final integration must separately hash the built artifact, verify its embedded identity after loading, then prove A-loaded/B-on-disk reports A until reload. This leaf does not activate or replace the currently loaded cartridge.

## Acceptance

- [ ] Historical-only fixtures report nonzero total backlog with zero live rows, correct bytes and explicit unknown historical age when applicable.
- [ ] One-time migration, overwrite, duplicate, receipt pruning, oldest deletion, failed/stale commits and crash/reopen preserve exact counters and commit progress. Missing/corrupt metadata is unavailable rather than fabricated empty.
- [ ] A real external epoch advance reports blocked/operator_required while a semantic query succeeds; the query does not clear the error or refresh progress. Ordinary saves do not impersonate successful crystallization.
- [ ] Actual worker scheduling is distinguished from manual attempts; bounded errors and process-local retention/generation are visible, and restart preserves only durable progress.
- [ ] Canonical local RPC and local ASP status projection under a held graph writer finish within 100 milliseconds with graph_busy, including every writer-helper graph reacquisition. Native/attached probes under the same contention instead honor one configured total deadline across health preflight, readiness and status; they may report timeout/unavailable. Existing native timeout, permit and late-completion tests remain green.
- [ ] Cached/uninitialized and ASP status reads do not open engines, decode pending payloads, call models, mutate graph heat or feed recursive intake. ASP status bypasses the generic fact route and preserves the tool.memory query-deposition exception and attached-owner read-only boundary.
- [ ] A named optimized release-profile RPC test measures the actual canonical status projection plus JSON serialization after migration on 1,000 and 100,000 pending rows: 20 warmups followed by 1,000 complete observations per size. Each p95 is at most 10 milliseconds; large p95 is at most three times max(small p95, 2 milliseconds). Each canonical serialized response is at most 8 KiB independent of backlog. Record sample count, p50/p95/max, response bytes, fixture bytes, migration duration, build profile and environment. The storage-only debug test is separately labelled diagnostic evidence and cannot establish the canonical polling gate. Exclude setup/migration from timed polling; do not claim these are retrieval quality/latency measurements.
- [ ] Build-input identity changes with relevant compiled inputs, stays reproducible across directories, and is described honestly as distinct from final artifact SHA256 and serving owner identity.
- [ ] Independent verifier runs named repaired-behavior tests, reviews the exact footprint and numeric output; root owner audit/isolation pass after integration. README/help explain durable versus process-local evidence and recovery.

## Verification fixture amendment

The canonical RPC benchmark uses a test-only heed 0.20 development dependency, matching store-core's existing pinned dependency. Seed the existing ledger database's historical rows in one fixture transaction, close that fixture environment, then open the actual Server/Store so production Store::open performs the real progress migration. This is necessary because 100,000 separately fsynced production import transactions would test fixture construction cost and exceed the checked block timeout before polling began. Record fixture setup and actual migration durations separately from the measured canonical RPC projection and JSON serialization. Do not add a public bulk import/test API or bypass production migration. The fixture owns a disposable directory and never touches a loaded store. Cargo.lock may only gain the existing heed package edge for rpc; versions remain pinned.

## Verify

Use an isolated external target for every command. Before the checked release measurement block, run this explicit foreground build setup and record its elapsed time separately. It does not establish any acceptance criterion. Cold compilation must not be hidden as a background task or reported as polling latency. Reuse its artifacts for the checked test run, whose normal verification timeout remains unchanged; if setup or verification cannot finish, report the actual failure rather than bypassing the limit.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-status-target}"
cargo test --release --locked -p rpc experience_status_canonical_polling_gate --lib --no-run
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-status-target}"; cargo test --locked -p store_core experience --lib -- --nocapture
pass: experience_status_historical_backlog_is_counted
pass: experience_status_migration_is_atomic_and_runs_once
pass: experience_status_overwrite_commit_restart_and_oldest_are_consistent
pass: experience_status_failed_commit_does_not_advance_progress
pass: experience_status_corrupt_metadata_is_unavailable
pass: experience_status_polling_cost_is_bounded_at_one_and_one_hundred_thousand
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-status-target}"; cargo test --locked -p rpc experience --lib
pass: experience_status_query_success_does_not_clear_stale_writer
pass: experience_status_graph_contention_is_bounded
pass: experience_status_attempts_and_durable_progress_are_distinct
pass: experience_status_poll_does_not_decode_or_mutate_inputs
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-status-target}"; cargo test --release --locked -p rpc experience_status_canonical_polling_gate --lib -- --nocapture
pass: experience_status_canonical_polling_gate
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-status-target}"; cargo test --locked -p commands memory_status --lib
pass: memory_status_retry_deadline_matches_worker_schedule
pass: memory_status_manual_attempt_preserves_worker_deadline
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-status-target}"; cargo test --locked -p memory_cartridge status --lib
pass: status_experience_cache_is_independent_of_query_success
pass: status_uninitialized_does_not_open_store
pass: status_owner_generation_change_is_unavailable
pass: status_attached_health_and_status_share_one_deadline
pass: status_build_input_identity_is_reproducible_and_sensitive
pass: status_embedded_identity_does_not_follow_changed_disk_inputs
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-status-target}"; cargo test --locked -p memory_cartridge asp --lib
pass: status_entity_is_declared_and_avoids_fact_expansion
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-status-target}"
cargo check --locked -p store_core -p rpc -p commands -p memory_cartridge
cargo fmt --all -- --check
```

Existing status/probe and writer regression suites must continue to pass. Record actual test names and counts, numeric measurement output and exact source hashes. Do not treat characterization-only passes as repair evidence. Collection waits for independent verification and uses checked committed verification if unrelated live changes remain.

## Recovery and limits

Migration uses one atomic database transaction and leaves old durable data intact on failure. Corrupt authority blocks migration/status explicitly; this leaf does not invent a destructive repair or downgrade routine. Runtime status is observational and cannot repair divergent dirty graphs, discard inputs or reset the writer guard. A fresh initialized owner reconstructs only process-local observations while reading persisted progress. Failed probes are bounded and cannot overwrite newer generation observations. Parent integrated recovery, model-outage tests, loaded artifact proof and retrieval measurements remain mandatory after the later in-scope leaves; this status leaf does not claim those outcomes from unit tests.
