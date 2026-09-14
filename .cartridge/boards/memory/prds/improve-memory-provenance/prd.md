---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "specced"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: improve-memory-provenance
footprint: ["src/base/src/base_types.rs","src/retrieval/piece/src/id_detail.rs","src/retrieval/piece/src/lib.rs","src/retrieval/src/lib.rs","src/rpc/src/server.rs","src/cartridge.rs","src/transport/src/owner.rs","src/store/core/src/lib.rs",".cartridge/tests/unit/src/base/src/tests/base_types_test.rs",".cartridge/tests/unit/src/retrieval/piece/src/tests/id_detail_provenance_test.rs",".cartridge/tests/unit/src/rpc/src/tests/server_bounded_test.rs",".cartridge/tests/integration/cartridge.rs",".cartridge/docs/CARTRIDGE.md",".cartridge/docs/fact-provenance.md"]
needs: ["@memory/improve-memory-readiness"]
---

# Expose fact provenance freshness and conflicts consistently

Query and get responses identify source, observation/update time where known, lifecycle status and conflicting evidence so callers can assess a recalled fact.

## Acceptance

- [x] Seed an updated fact with its older conflicting source: query/get preserve both identities and explain status and provenance.
- [x] A legacy fact lacking dates returns unknown freshness and remains readable; unavailable evidence is not fabricated.

- [x] Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [cartridge.rs](../../../../../../memory.ctg/.cartridge/tests/integration/cartridge.rs), [CARTRIDGE.md](../../../../../../memory.ctg/.cartridge/docs/CARTRIDGE.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. Final public gates passed: 1408 tests, 17 existing skips, documentation tests and just check; see implementation-proof.json.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-provenance`; maximum five rounds.
