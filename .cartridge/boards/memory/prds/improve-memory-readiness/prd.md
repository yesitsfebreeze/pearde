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
canonical-scope: improve-memory-readiness
needs:
- '@memory/improve-memory-owner-access'
footprint: ["Cargo.lock","src/store/core/Cargo.toml","src/cartridge.rs","src/cartridge_status.rs","src/commands/src/memory.rs","src/transport/src/owner.rs","src/transport/src/memory_rpc.rs","src/store/core/src/lock.rs","src/rpc/src/server.rs",".cartridge/tests/unit/src/cartridge/status_test.rs",".cartridge/tests/unit/src/cartridge/tests.rs",".cartridge/tests/unit/src/store/core/src/tests/lock_test.rs",".cartridge/tests/unit/src/transport/src/owner_test.rs",".cartridge/tests/integration/cartridge.rs",".cartridge/tests/integration/e2e/cli_surface.rs",".cartridge/tests/integration/e2e/focus_routing.rs",".cartridge/docs/owner-attachment.md",".cartridge/docs/CARTRIDGE.md"]
capability-owner: "memory"
commit: "a124fd30d59bcd06062b5464810188a0288e461e"
---

# Report memory readiness separately from registration

A registered memory provider exposes store/model readiness and the reason it cannot currently serve a request.

## Acceptance

- [x] The contention fixture reports active registration and unavailable query readiness with retryability; it never reports ready from registration alone.
- [x] Status requests have a deadline, redact credentials, and do not start a writer; after owner recovery status updates without restarting the caller.

- [x] Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [cartridge.rs](../../../../../../memory.ctg/.cartridge/tests/integration/cartridge.rs), [CARTRIDGE.md](../../../../../../memory.ctg/.cartridge/docs/CARTRIDGE.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. Final public gates passed: 1402 tests, 17 existing skips, documentation tests and just check; see implementation-proof.json.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-readiness`; maximum five rounds.
