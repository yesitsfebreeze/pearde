---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: improve-memory-programme
needs:
- '@memory/improve-memory-owner-access'
- '@memory/improve-memory-readiness'
- '@memory/improve-memory-provenance'
---

# Memory access, readiness and provenance improvements

This parent groups three memory outcomes from the access assessment. Owner access and readiness are done; both PRDs record commit `a124fd3`. Provenance is specced and passed its round-3 review. Claim that leaf to implement it; this parent adds no implementation of its own.

## Acceptance

- [ ] Each linked leaf is done with its own recorded acceptance evidence.
- [ ] Integration gate: at the memory.ctg revision that completes provenance, `just test` passes when run from /Users/feb/dev/cartridge/memory.ctg, and the memory `status`/`health` answers still report owner access and readiness as their leaves specify.
- [ ] Record tested mitigations and remaining limitations here. A failed gate reopens only the leaf it names; it never repairs a production store.

## Work items

- [Query a memory store through its existing owner](../improve-memory-owner-access/prd.md)
- [Report memory readiness separately from registration](../improve-memory-readiness/prd.md)
- [Expose fact provenance freshness and conflicts consistently](../improve-memory-provenance/prd.md)

## Review

[Review history](review.md): rounds 1–2 inherited; rounds 3–4 on 2026-09-14; maximum five.
