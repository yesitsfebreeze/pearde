---
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
review-round: 1
review-status: passed
---

# Memory reads work while another process holds the bank, without a writer-lock error

Reported: `cartridge_memory query` failed with `another memory writer holds this data dir (cartridge memory pid 72544)` because a second memory cartridge opened the same `dir` in local mode. memory.ctg already supports explicit read-only attachment (`owner = {endpoint, timeout_ms}`, `ServiceConfig::Attached`, `read_observed`), which by its [contract](../../../../../../memory.ctg/.cartridge/docs/owner-attachment.md) does not discover or start a daemon. Since the transport port (memory.ctg `9cc0f0b`) the cartridge serves `memory`, `context.memory` and `tool.memory` on its own cartridge socket but binds no memory-RPC endpoint, so attachment has nothing to reach. Owner: memory.ctg.

## Acceptance

- [ ] Probe first: with a disposable writer holding a temp bank, record which endpoint a second process can reach and whether the `read_observed` identity handshake works over it.
- [ ] Recommended default: the writing cartridge serves its read endpoint, and a second cartridge configured with an explicit `owner` returns `query` hits for facts the writer ingested instead of the lock error.
- [ ] A wrong-store or dead owner is refused with its static status and never falls back to opening the bank locally.
- [ ] Without `owner` and without a live writer, local reads and ingest behave as today; `ingest` through an attachment fails `readonly_attachment` before connecting.

## Proof and recovery

Start at `memory.ctg/src/cartridge.rs` (`service_configuration`, `memory`), `memory.ctg/src/transport/src/owner.rs`, `memory.ctg/src/transport/src/endpoint.rs` and `memory.ctg/src/store/core/src/lock.rs`. Extend `memory.ctg/.cartridge/tests/unit/src/transport/src/owner_test.rs` and `memory.ctg/.cartridge/tests/integration/cartridge.rs` with temp banks only. Gates from `/Users/feb/dev/cartridge`: `just test memory`, `just check memory`; not run for this plan. Stop condition: if the fix needs automatic owner discovery across compositions, stop and raise a question memo, because that reverses the documented explicit-attachment contract. Rehoming to the memory board is recommended.
