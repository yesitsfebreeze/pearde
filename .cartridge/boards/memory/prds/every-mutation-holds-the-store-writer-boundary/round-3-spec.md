---
complexity: high
footprint:
- .cartridge/tests/integration/e2e/lifecycle.rs
- Cargo.lock
- src/commands/src/lib.rs
- src/commands/src/commands_graph_ops.rs
- src/commands/src/commands_focus.rs
- src/commands/src/commands_claim_kind.rs
- src/commands/src/commands_unnamed.rs
- src/commands/src/commands_check.rs
- src/commands/src/commands_hub.rs
- src/commands/src/commands_ingest_cmd.rs
- src/commands/src/commands_queue_cmd.rs
- src/bootstrap/src/lib.rs
- src/store/src/registry.rs
- .cartridge/tests/unit/src/commands/src/tests/commands_graph_ops_test.rs
- .cartridge/tests/unit/src/commands/src/tests/commands_writer_boundary_test.rs
- .cartridge/tests/unit/src/commands/src/tests/commands_hub_test.rs
- .cartridge/tests/unit/src/commands/src/tests/commands_queue_cmd_test.rs
- .cartridge/tests/unit/src/commands/src/commands_serve/entry_point_tests.rs
- .cartridge/docs/writer-boundary.md
---

# Hold the existing writer claim through every graph mutation

Measured baseline at 09bfaaefdcbe2fb3705bece2fcc643c9a95da478: with_graph executes its mutation closure while another writer lock is held. The retained commands-unit probe fails its no-entry assertion; the probe was removed after measurement. Work in the isolated Memory lane, preserving all original checkout edits. No store format, tombstone, CRDT, model routing or daemon handover redesign.

## Existing authority and census

The existing store::lock::acquire takes writer.lock before changing its informational label; its bounded inherited-fork patience remains unchanged. The actual file claim, not holder(), socket absence or an epoch observation, authorizes offline mutation. Claim before graph load/attach and retain through all direct writes, final flush and related maintenance/queue effects. Failure returns through existing CLI failure status without invoking mutation, opening the graph or reporting successful persistence. Read-only report/list/check/query paths preserve their current contract.

The checked source census must map every dispatch mutation to the following proven boundary, with exact symbols and regression coverage:

- Shared with_graph: focus add/remove, claim-kind add/remove, unnamed promote, forget, promote, move and degrade. Return an explicit Result and propagate refusal/final save errors; mutation callbacks never run without ownership. Use try_load_graph so unreadable data cannot become an empty replacement. Callback success output must not escape before a known save failure is reported as failure.
- Direct offline paths: prune, audit --apply, repair, link, ingest and queue drain. Replace holder-only checks with retained acquisition and add missing claims before load. Dry audit/report remains read-only. Queue drain acquires before archive/dequeue changes; failed claims cannot report a successful drain. Existing routed success/refusal semantics remain unchanged, and no model retry is added.
- Cross-store register and hub merge: protect the destination and acquire the source for a consistent offline operation. Resolve actual canonical data directories, refuse aliases of the same store, acquire in deterministic path order before opening either graph, and retain both through publication. Hub shutdown/probe remains assistance, never a claim substitute. Existing explicit merge semantics remain; this does not extend automatic stale flush merging.
- Clean --yes: acquire before deleting data. Retain the data directory and the exact writer.lock inode while removing its other contents, so a contender cannot claim a replacement inode during cleanup. Reject auxiliary cleanup paths that are ancestors of the protected directory/lock before any removal; deduplicate equal/nested targets and handle symlinks without following them for recursive deletion. Report partial IO failure without claiming rollback. Dry preview remains observational and describes the retained claim file accurately.
- Existing claimed paths: gc, consolidate/compact, migrate, reembed, rekey/relocate, export/import; daemon bootstrap claims before self-heal/registry open and keeps ownership in EngineHandle; native Memory Engine claims before registry/background tasks and keeps ownership through shutdown flush. Their nested ingest/RPC/watch/queue/tick and direct graph deregister/unload/cold writes inherit this live claim. Verify these call paths and existing tests rather than adding redundant reentrant acquisition. Derived index/cache materialization is distinct from graph entity mutation; do not add a writer requirement to read-only graph loads.

## Stale snapshot safety

A guarded flush remains an independent last defense. On RefusedStale, return an explicit failure and preserve the committed store and unflushed RAM for diagnosis. Do not absorb the newer store into a stale graph and retry: missing disk rows may have been deliberately deleted. Do not silently advance flushed_epoch or mark a failed snapshot clean. Propagate the result to direct callers and log it in the existing void background save closure; snapshot_if_dirty records a clean epoch only after success. Existing guarded CLI retry retains its explicit fresh-state redo semantics under its newly held lock, with no new retry policy.

The historical guarded-flush test currently requires automatic union of externally added rows with stale RAM. Replace that unsafe contract assertion with refusal/unchanged durable bytes and preservation of RAM; document this intentional behavior correction. Retain the existing link test's stronger useful result: a supplied stale graph with an externally added memory still links successfully and preserves both. In the narrow link helper, refresh stale state before applying the explicit link intent, without copying stale rows into fresh state; resolve missing endpoints against that fresh graph and refuse if deleted. The public link path holds ownership before its initial load. No automatic replay of arbitrary graph mutations.

## Acceptance / proof

- [ ] Maintained Rust subprocess barrier fixture releases two writer contenders together, holds the winner through the loser outcome, and proves exactly one mutation/commit. The loser changes no store bytes, including claim label; alias paths hit the same boundary. A killed owner releases the OS claim and a fresh process can continue.
- [ ] Seed a row, retain an old snapshot, delete and commit through the owner, then attempt stale guarded flush. Deletion survives unchanged, including reopening after an abrupt owner exit; RAM is retained and failure stays explicit. Link fresh-intent replay cannot resurrect deleted endpoints; the existing additive interleaving test remains passing.
- [ ] Table-driven held-writer fixtures exercise every newly protected direct entry or its shared helper, including no mutation callback, no queue archive, no cleanup, cross-store source/destination refusal and same-store aliases. Clean retains the claim inode and refuses a contender while clearing contents. Read-only inspection still works with the owner held.
- [ ] Mutation census names source revisions, exact symbols and inherited daemon/cartridge/maintenance boundaries. Public Memory test/check gates pass in the isolated lane; original unrelated files remain byte-identical.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary cargo test -p commands writer_boundary -- --nocapture
```

```sh
set -eu
cd /Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just test
```

```sh
set -eu
cd /Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just check
```

Use disposable stores and owned subprocesses only, with bounded waits and cleanup. Retain baseline/proof logs and source hash. Review round3 is pending; no implementation before independent review. Dependency-only Cargo.lock changes reflect the current optional runtime dependency resolving SHA2, not new Memory dependencies. If public full workspace gates exceed per-block execution limits, retain the exact public results and split proof commands without changing tested scope.
