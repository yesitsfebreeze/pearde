---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/memory.ctg"
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
---

# Activity recording drains into memory and retires calendar history

The existing trace ingress becomes a bounded durable memory inbox. A background batch embeds novel observations, crystallizes them into the graph, and atomically persists changed memories, delivery receipts and inbox removal. Calendar summaries and the second history search disappear. Historical trace rows migrate through the same path before removal.

## Acceptance

- [ ] Append acknowledges durable intake without an embedding or reasoning request; retries use a stable delivery identity.
- [ ] A bounded background batch commits graph changes, receipts and inbox removal atomically; failures retain input and do not double-count after restart.
- [ ] Existing raw and condensed rows migrate without calendar re-summarization. The calendar processing implementation and its superseded fixtures are deleted.
- [ ] ASP trace compatibility views expose graph experiences, counts, reasons and sub-memories with bounded descriptions; normal search queries the memory graph once.
- [ ] Isolated real service calls demonstrate repeated errors, separate success, recall after restart and non-mutating observation; release measurements report append and drain costs.

## Proof and recovery

Start at src/rpc/src/trace, src/store/core/src/trace.rs, src/cartridge/src/asp and src/commands/src/memory.rs. Preserve the current trace ingress as a transport adapter so independently evolving host/proxy callers remain compatible. The physical legacy table becomes an inbox and compact delivery receipts, not another history. Keep historical rows until their graph transaction succeeds. Limit batches to 64 and payloads to 64 KiB; return explicit refusal on capacity or malformed payload. Preserve credential redaction upstream. Snapshot only changed memories for commits, never the entire graph per event. Run cargo test -p rpc experience, cargo test -p store_core experience, cargo test -p memory-cartridge, then just audit memory and just isolation from the composition root. Use disposable stores.

## Concurrency and bounds

Hold the graph write guard only for the bounded apply and commit, after embedding outside it. Clone only touched memories as an undo set. Commit touched memories, receipts and inbox removal under the store epoch guard; advance the graph flush epoch on success. Restore the undo set and rebuild affected indexes on any refusal or I/O failure before releasing the guard. A concurrent older full-snapshot flush must be refused by the advanced disk epoch. Test this interleaving and failed-commit retry explicitly.

The inbox admits at most 4096 pending rows and 64 MiB of payload. Delivery receipts are hashes retained for seven days, capped at 1000000; receipt capacity exhaustion refuses new arrivals until expiry rather than silently forgetting retries. New delivery timestamps older than seven days are refused, so receipt expiry cannot recount stale deliveries. Historical migration uses deterministic identities and atomic removal of each old row instead of the live delivery age policy. Pruning is bounded per batch. Capacity and age refusals are explicit and leave stored input unchanged.

## Dependencies and review

Requires the graph experience contract. Independent review is recorded in review.md. Live data migration runs only through tested automatic code, with no manual deletion. Runtime in-memory viewer buffers are projections; unrelated diagnostic logging and the installed-cartridge catalog remain separate responsibilities.

## Implementation checkpoint

Implemented in the current memory.ctg working tree. [Shared verification evidence](../implementation.md) records integration, tests and remaining limits. This checkpoint does not replace formal PRD collection.
