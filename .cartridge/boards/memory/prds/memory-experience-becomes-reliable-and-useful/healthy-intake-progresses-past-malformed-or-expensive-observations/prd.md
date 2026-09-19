---
state: open
origin: requested
priority: 98
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
needs:
  - "@memory/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence"
footprint:
  - "src/store/core/src/experience.rs"
  - "src/rpc/src/experience/drain.rs"
  - "src/rpc/src/experience/input.rs"
  - "src/commands/src/memory.rs"
  - ".cartridge/tests/unit/src/rpc/src/experience_test.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Healthy intake progresses past malformed or expensive observations

Make healthy acknowledged input progress under malformed rows, model context limits and sustained arrivals. Use bounded work scheduling, isolate invalid inputs with explicit evidence and keep temporary model failures retryable.

## Evidence

The pass decodes with an early-return error, embeds all missing texts in one request and prioritizes inbox rows before history. One malformed or rejected input can hold a batch; count limits do not bound embedding tokens or provide migration fairness. These are source findings requiring deterministic reproduction. See [investigation](../investigation.md).

## Acceptance

- [ ] A malformed legacy row followed by valid rows yields a visible retained failure and commits the valid rows without losing acknowledged input.
- [ ] An embedding limit on one row cannot indefinitely block valid neighbours; byte/token budgets and bounded retry avoid unbounded model requests.
- [ ] A continuously nonempty live inbox still allows historical backlog progress under a documented bounded fairness policy.
- [ ] Cancellation, model outage and restart preserve retry identity; partial successes keep atomic graph/input/receipt commits.

## Proof and recovery

Create malformed-head, context-limit, continuous-arrival and cancellation fixtures in the RPC experience suite. Run cargo test --locked -p rpc -p store_core experience --lib from memory.ctg. Benchmark append acknowledgement and drain throughput including model time, separately from graph-only cost.

A failed row remains durably inspectable with an error and retry policy; quarantine is memory-owned intake state, not another history. Land after writer coordination because both touch commit batching. Scope M.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
