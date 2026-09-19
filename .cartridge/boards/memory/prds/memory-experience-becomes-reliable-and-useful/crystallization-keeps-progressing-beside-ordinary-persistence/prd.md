---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
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
commit: "d9161cd2f3a363915c7a7d642a4955e7a3836065"
---

# Crystallization keeps progressing beside ordinary persistence

Coordinate ordinary persistence and crystallization through one engine-owned commit protocol. Establish the advancing writer with a deterministic interleaving before selecting locking or retry mechanics. Preserve the stale-writer guard.

## Evidence

Live cycle 22 refused a stale snapshot after 21 successful cycles. Inputs remained pending. Existing tests reproduce refusal and rollback, but do not prove concurrent recovery. The writer responsible for the live epoch advance is not established. See [investigation](../investigation.md).

## Acceptance

- [x] A barrier-controlled ordinary-save/crystallization race drains all acknowledged inputs exactly once and preserves unrelated dirty changes.
- [x] An external epoch advance refuses overwrite and reports recoverable versus operator-required state without discarding RAM.
- [x] Restart after a crash between commit and acknowledgement preserves graph rows and delivery receipts.
- [x] Background retry makes progress for engine-local races; permanent divergence is visibly blocked rather than an endless unexplained retry.

## Proof and recovery

Start with the existing stale-commit test, then add deterministic concurrent-save and crash fixtures in the same RPC suite. Run cargo test --locked -p rpc experience --lib and cargo test --locked -p bootstrap --lib from memory.ctg.

No force-flush, silent RAM replacement or second writer. Roll back the coordinator while retaining the store and intake. Scope M; memory ranking row 12.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.

## Specification decision (2026-09-19, memory-coordinator)

The controlled reproduction identifies an ordinary-save epoch-publication window, not the historical live writer. The specification adds the per-store coordinator initialization and bootstrap/RPC regression paths, and publishes writer state through existing trace status. No registry edit is necessary because its current save closure already reaches bootstrap. The footprint now names these actual source/test paths; existing epoch guards and the tool.memory readback policy are unchanged.
