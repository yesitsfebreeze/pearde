---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-memory-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Memory improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Memory, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Query a memory store through its existing owner | [improve-memory-owner-access](../improve-memory-owner-access/prd.md) |
| 2. Report memory readiness separately from registration | [improve-memory-readiness](../improve-memory-readiness/prd.md) |
| 3. Expose fact provenance freshness and conflicts consistently | [improve-memory-provenance](../improve-memory-provenance/prd.md) |

### Downside coverage

1. Writer ownership can block recall: attach to the legitimate owner, preserving single-writer integrity.
2. Model endpoints can fail: return bounded, attributable failures and test with local fixtures.
3. Facts can age or conflict: expose provenance and freshness without inventing truth.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Review current source and active ownership before implementation; the assessment does not reserve files.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Memory behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test memory --test cartridge
just check memory
just test memory
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
