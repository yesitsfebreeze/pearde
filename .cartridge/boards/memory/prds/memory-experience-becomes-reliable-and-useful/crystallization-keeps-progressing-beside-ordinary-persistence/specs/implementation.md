---
footprint:
  - src/store/core/src/lib.rs
  - src/bootstrap/src/lib.rs
  - src/commands/src/commands_serve.rs
  - src/bootstrap/Cargo.toml
  - Cargo.lock
  - src/rpc/src/experience/drain.rs
  - src/rpc/src/experience/mod.rs
  - .cartridge/tests/unit/src/bootstrap/src/writer_test.rs
  - .cartridge/tests/unit/src/rpc/src/experience_test.rs
  - README.md
  - .cartridge/help.md
  - ".cartridge/tests/unit/src/commands/src/commands_serve/entry_point_tests.rs"
  - "src/tick/loop/src/tick_tasks.rs"
  - ".cartridge/tests/unit/src/store/core/src/lib/tests.rs"
---

# Coordinated ordinary persistence and crystallization

## Evidence and scope

[The controlled reproduction](../writer-reproduction.md) establishes a transient local publication race using actual ordinary persistence and RPC commit paths. It does not establish the cause of historical live cycle 22. The preserved baseline probe and runner are in `../evidence/`. This change closes the proved local race while retaining refusal for genuinely divergent RAM. It does not claim automatic reconciliation of arbitrary dirty graphs.

The footprint adds store-core initialization, bootstrap unit tests and the minimal test dependency/lockfile changes to the original PRD footprint. No registry change is required: its existing save closure calls the coordinated bootstrap entry point. No new schema, serialized field, receipt key or public event is introduced. The existing LMDB stale-epoch comparison remains unchanged. Corrupt epoch decoding now fails the authoritative read and transaction rather than treating unreadable metadata as epoch zero; the legacy advisory accessor retains its compatibility behavior.

## Commit ownership and lock order

Add one process-local coordinator mutex to each `store_core::Store`, initialized by `Store::open`. Expose an RAII guard and nonblocking acquisition through this production store API. Recover a poisoned mutex only by continuing through the existing epoch checks; never copy the disk epoch into graph RAM to suppress a refusal. Distinct stores have independent gates.

Ordinary `save_graph_guarded` acquires the store gate before taking its snapshot and retains it through publishing the returned flushed epoch. It releases graph locks during serialization and durable I/O, preserving the existing short graph-lock behavior. Crystallization acquires the same gate before its graph write lock and retains it through graph mutation, durable graph/receipt commit, rollback or successful epoch publication. The order is always store gate then graph guard. Discovering the Store Arc may use a temporary graph read guard, which must be dropped before waiting for the gate.

Do not acquire the gate recursively from low-level `Store::flush_guarded` or `experience_commit`. Those methods keep transactional stale checking and remain usable by external/prepared-snapshot tests. Keep the existing per-engine crystallization pass mutex so duplicate passes cannot commit the same captured batch twice. Ordinary graph mutations may occur while a snapshot is flushing; they remain in RAM and are persisted by the next ordinary save. No graph replacement or reload occurs on local contention.

A private bootstrap helper may parameterize only the real snapshot flush operation for its unit test. The public production entry point delegates to this helper with the current real flush function. Test closures can pause after the real durable flush and before publication. No public test hook, environment switch, sleep barrier or runtime fault injection is added to production.

Maintenance `reconcile_if_stale` also takes the store coordinator before reading graph state. It reports divergence without replacing RAM, including when called by the loaded engine's maintenance tick. Its boolean continues to signal detected divergence; it no longer means that replacement occurred. The existing commands regression and maintenance comment are updated to this explicit preservation contract. New deterministic tests first reproduced dirty-RAM loss from this maintenance path, then prove corrected publication ordering and external-divergence preservation.

## Observable divergence contract

Expose a point-in-time `writer` object through the existing trace status response and include it in the existing cycle before/after snapshots. Its states are `ready`, `coordinating` and `blocked`. `coordinating` is returned when the store gate is busy, with `recovery:"automatic"`; it must not be called external divergence. Under an acquired gate, a disk epoch ahead of the graph epoch yields `state:"blocked", code:"stale_snapshot", recovery:"operator_required", expected_epoch, disk_epoch`. Ready has `recovery:"none"`. Authoritative epoch read failures return an unavailable error rather than `ready`; guarded writes also refuse corrupt epoch metadata without changing stored rows. This state is memory-owned and read-only; the subsequent backlog/status leaf consumes it without another API.

A background crystallization pass preflights divergence before embedding. A permanently divergent graph returns a bounded report with `processed:0`, nonempty `failed`, and the same blocked writer object, leaving all inputs and dirty RAM untouched. Existing direct commit stale errors remain errors. The worker's existing failure backoff continues to apply. Repeated blocked passes do not call the model or masquerade as progress. A fresh load or explicitly authorized reconciliation can restore ready state; this leaf never silently replaces dirty RAM.

## Acceptance

- [x] A bootstrap barrier test pauses the actual flush after disk commit. The competing coordinated commit waits until publication, then observes the new epoch; graph readers and unrelated dirty mutation remain available while the disk callback is paused.
- [x] A real RPC test starts ordinary `save_graph_guarded` and crystallization behind a held coordinator gate, releases them concurrently and proves both finish without false stale refusal. All acknowledged inputs commit exactly once; unrelated dirty RAM survives and becomes durable after a final save/reload.
- [x] A stale prepared snapshot still returns `RefusedStale` after crystallization. No test relaxes or replaces the existing guard assertions.
- [x] A genuine external epoch advance yields machine-readable operator-required state. Repeated background passes retain inputs and dirty RAM without model calls. A separately loaded fresh graph clears the blocked state and drains the retained input.
- [x] Concurrent duplicate delivery/pass attempts leave one committed delivery receipt and one recurrence increment. Existing per-engine pass exclusion remains in force.
- [x] Restart after durable commit but before the caller observes success replays the same delivery as duplicate, preserving graph rows and recurrence. A child-process fixture exits without normal cleanup after commit, so this is crash recovery rather than an in-process reload characterization.
- [x] Holding one store's coordinator does not prevent another store from persisting.
- [x] The named tests below execute, formatting passes, and README/help explain local automatic coordination versus operator-required divergence.

## Verify

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-writer-target}"; cargo test --locked -p bootstrap writer --lib
pass: writer_publication_is_coordinated_without_holding_graph_lock
pass: writer_gates_are_independent_between_stores
pass: writer_reconciliation_waits_for_publication_and_preserves_dirty_ram
pass: writer_external_advance_never_automatically_replaces_ram
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-writer-target}"; cargo test --locked -p rpc experience --lib
pass: experience_ordinary_save_and_crystallization_preserve_dirty_work
pass: experience_external_writer_blocks_without_discarding_ram
pass: experience_concurrent_passes_commit_each_delivery_once
pass: experience_crash_after_commit_preserves_receipts
pass: experience_commit_refuses_older_full_flush_and_migrates_history
pass: experience_failed_commit_restores_graph_and_retains_input
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-writer-target}"; cargo test --locked -p store_core writer_epoch --lib
pass: writer_epoch_corruption_is_not_ready_or_writable
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-writer-target}"; cargo test --locked -p commands reconcile_if_stale_preserves_ram_when_the_store_advanced --lib
pass: reconcile_if_stale_preserves_ram_when_the_store_advanced
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-writer-target}"
cargo check --locked -p bootstrap -p rpc
cargo fmt --all -- --check
```

## Recovery and verification limits

The coordinator is ephemeral and needs no migration. Process exit releases it. Durable acknowledgement remains the existing atomic graph, receipt and input-removal transaction. Rollback never force-flushes or changes receipt identity. Failed verification leaves runtime artifacts unchanged. Run only external targets, then independently verify the committed lane before collection. Root owner audit and isolation are required after integration. This leaf establishes correctness and preserves short graph lock duration; measured end-to-end quality/latency gates remain required by the parent.
