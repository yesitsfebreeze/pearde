---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: improve-memory-owner-access
footprint: [".cartridge/tests/integration/e2e/cli_surface.rs","Cargo.toml","src/cartridge.rs","src/transport/src/lib.rs","src/transport/src/owner.rs","src/transport/src/typed.rs","src/transport/src/memory_rpc.rs","src/commands/src/commands_health.rs",".cartridge/tests/unit/src/cartridge/tests.rs",".cartridge/tests/unit/src/transport/src/owner_test.rs",".cartridge/tests/unit/src/commands/src/tests/commands_health_owner_test.rs",".cartridge/tests/integration/cartridge.rs",".cartridge/docs/owner-attachment.md"]
capability-owner: "memory"
needs: ["@memory/memory-health-loads-its-own-graph-beside-the-daemon"]
commit: "f9759848c56255ee0607587970f58ccc087ade53"
---

# Query a memory store through its existing owner

Two legitimate cartridge clients can query one store without acquiring competing writer locks or stopping the owner.

## Acceptance

- [x] With one process owning a temporary store, a second authorized client retrieves a seeded fact; no second writer starts.
- [x] Owner crash, stale endpoint, canonical path alias and mismatched store identity produce bounded, explicit outcomes without deleting locks or replaying uncertain ingestion.

- [x] Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [cartridge.rs](../../../../../../memory.ctg/.cartridge/tests/integration/cartridge.rs), [CARTRIDGE.md](../../../../../../memory.ctg/.cartridge/docs/owner-attachment.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. Verified source f9759848c56255ee0607587970f58ccc087ade53 passes public just test (1388 passed, 17 existing skips; documentation tests passed) and just check. Exact commands, hashes, fixture diagnosis and independent review are retained in [implementation-proof.json](implementation-proof.json).
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-owner-access`; maximum five rounds.
