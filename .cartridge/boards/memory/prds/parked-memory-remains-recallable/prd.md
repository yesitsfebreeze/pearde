---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: parked-memory-remains-recallable
---

# A parked fact stays findable in every layout, and a failed cold read is partial

Cold rows already join fusion before the top-k cut (`cold_candidates` in `src/retrieval/piece/src/retrieval_query.rs`). Exact reads fall back to cold (`src/retrieval/piece/src/id_detail.rs`), and `.cartridge/tests/integration/memory_contract.rs` proves several per-tier invariants.

Two gaps remain:

- No test takes one indispensable fact through hot, half-cold and all-cold layouts for both search and get.
- A failed cold read fails the whole query (`src/rpc/src/server.rs`, `src/commands/src/commands_query.rs`). `cold_candidates` also scans every cold row; only the size of the pool it keeps is bounded.

Outcome, owned by memory: the three-layout invariant test, plus partial results under a cold-scan budget.

## Acceptance

- [ ] In hot, half-cold and all-cold fixtures, the same fact appears in the query top-k with the score it resolves to, and `get` returns identical text and source.
- [ ] An injected cold-read error or an exhausted scan budget returns the resident results with `partial: {cold: "unavailable"|"budget"}` and `cold_rows_scanned`. The query calls no model and finishes within its deadline.
- [ ] Without a fault, results on the replay fixture match `c25af4d`. The default does not change, and no parked row is filtered out.

## Proof and recovery

First probe: write the three-layout test against `c25af4d`. If it already passes, keep it and continue with partial status. Budget default: a `retrieval.cold_scan_max` key, where unset keeps today's unbounded scan. Tests go in `memory_contract.rs`. Gates, run from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test` (not run). Rollback: revert the partial arm. Queries do not write to the store.

## Dependencies and review

No hard needs. The fixtures already exist, so memory-004's ranking decision is linked context, not a prerequisite. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
