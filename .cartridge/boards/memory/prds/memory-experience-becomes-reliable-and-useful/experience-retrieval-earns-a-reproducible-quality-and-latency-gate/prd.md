---
state: open
origin: requested
priority: 92
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
needs:
  - "@memory/a-frozen-query-reads-the-bank-without-touching-it"
footprint:
  - ".cartridge/tests/integration/bench/src/replay.rs"
  - ".cartridge/tests/integration/bench/src/score.rs"
  - ".cartridge/tests/integration/bench/src/main.rs"
  - ".cartridge/tests/integration/bench/REPLAY.md"
  - ".cartridge/tests/integration/e2e/recall.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Experience retrieval earns a reproducible quality and latency gate

Extend the existing replay instrument with a versioned experience corpus and a paired live consumer probe. Freeze labels before tuning. Measure harmful merges, useful evidence retrieval and end-to-end latency separately, including recurrence bursts, changed conditions and cold memory.

## Evidence

The repository already has labelled replay, mature-store, noise and retention benches. The 10,000-repeat microbenchmark excludes model and storage costs. Eight new deterministic probes establish structural behavior, not actual embedding merge quality or improved agent decisions. See [investigation](../investigation.md).

## Acceptance

- [ ] A checked-in labelled corpus covers equivalent reasons, opposite outcomes, different scopes, noisy repetition, changed truth, retirement and cold groups.
- [ ] Reports pin code, fixture, model/vector hashes, thresholds and seed; held-out hard-boundary cases have zero harmful merges and relevant-evidence recall@5 is at least 0.90.
- [ ] Candidate defaults meet the hard-boundary gate, lose no more than two percentage points of recall against baseline and report confidence intervals and sample counts.
- [ ] An isolated consumer run traces nominated, read-back and injected references and reports timeouts; p50/p95 includes embedding, commit and transport separately. Fake-model runs are marked structural only.

## Proof and recovery

Reuse REPLAY.md and existing runner arguments rather than inventing another benchmark. First add fixture and a runner entry, document its exact command, then run twice with frozen queries. Initial latency budget: no more than 10% p95 regression under the same warmed workload; report absolute latency and hardware as well.

Use disposable banks and synthetic public fixtures. Do not learn from evaluation queries or tune against held-out labels. Quality gates block default threshold changes, not fixture creation. Scope M.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
