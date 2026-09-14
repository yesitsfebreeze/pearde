---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: keep-the-tree-and-record-true
needs:
- '@memory/memory-002'
- '@memory/memory-004'
- '@memory/the-graph-converges'
---

# What memory reports about its store stays true

This is a finite parent for three memory outcomes: status counts use one vocabulary, ranking on a spilled store is measured and decided, and repeated ingest converges to stable counts. It replaces the historical standing maintenance terminal, which was never meant to finish and which the small-PRD rule retired. Later hygiene findings get their own leaves.

## Acceptance

- [ ] Each linked leaf is done, with its own evidence, at one memory.ctg revision.
- [ ] Integration gate: at that revision, run `just all` from /Users/feb/dev/cartridge/memory.ctg. On the graph-converges fixture store, `memory health` and the `health` RPC must report equal counts under the terms memory-002 defines, and `memory check --json` must report no `dangling_reasons`.
- [ ] If a leaf or the gate fails, record it here and leave the parent open.

## Work items

- [CLI and RPC name the same memory counts](../memory-002/prd.md)
- [Decide how ranking treats cold rows on a spilled store](../memory-004/prd.md)
- [Repeating a multi-document ingest converges to stable counts](../the-graph-converges/prd.md)

## Review

[Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
