---
state: open
origin: requested
priority: 76
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 4
date: "2026-09-15"
footprint:
- "harness.ctg"
- "live.ctg/src/ring.ts"
needs:
- "long-horizon-recall-benchmark"
- the-repository-answers-by-text
---

# Context holds across a long orchestration

## Outcome

A day-long orchestration keeps its decisions and its workers' results without the recall engine.

## Acceptance

- [ ] A synthetic 200-turn orchestrator session with 20 worker results stays under `harness.max_bytes`; a decision stated in turn 5 and every worker's final line are still in working memory at turn 200.
- [ ] `harness.selftest` covers it under `just test harness`.

## Deferred by name

- @root/long-horizon-recall-benchmark

## Result

Not started.
