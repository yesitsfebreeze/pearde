---
repo: /Users/feb/dev/cartridge/harness.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: harness
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-harness-quality-eval
needs:
- '@harness/improve-harness-compaction-diff'
footprint:
- /Users/feb/dev/cartridge/harness.ctg/src/compaction.rs
- /Users/feb/dev/cartridge/harness.ctg/src/inspection.rs
- /Users/feb/dev/cartridge/harness.ctg/.cartridge/tests/unit/compaction.rs
- /Users/feb/dev/cartridge/harness.ctg/.cartridge/tests/eval
---

# Measure multi-round context quality with real task outcomes

A three-round corpus already exists in `harness.ctg/.cartridge/tests/eval/corpus` (journals v1–v3,
`facts.json` with require/forbid facts, good and four adversarial summaries in
`summaries/manifest.json`), but nothing runs it: `eval/eval_compaction.py` was deleted in
harness 2364a43 under the no-Python repository decision. This leaf restores an offline check
over that corpus and adds an opt-in live report. Compaction-diff inspection (`compaction::comparisons`)
is delivered and reused, not rebuilt.

## Acceptance

- [ ] An offline Rust test in the existing compaction unit entry point scores every manifest summary: good rounds 1–3 pass; each bad summary reports exactly its `expect` class (lost fact, obsolete conclusion, invented completion, invented permission).
- [ ] A deliberately broken checker (require ignored) makes that test fail.
- [ ] Per-class results include abstention/unknown instead of silently passing when a fact cannot be evaluated; the corpus licence and revision are recorded beside the manifest.
- [ ] The opt-in live report replays the round-3 task from each compacted context, scores the task outcome as well as fact needles, and records every failure, tokens, latency, model identity and revisions, and states that the offline gate does not measure model quality.

## Proof and recovery

First step: run `just test harness` (cwd `/Users/feb/dev/cartridge`) and record the existing
baseline, including the known working.rs failure. Then add the test beside
`.cartridge/tests/unit/compaction.rs`. Offline gate: the same command. The live report needs a
separately configured model and bounded budget and never runs in that gate. Rollback: tests and
report are additive; transcripts, summaries and compaction settings are untouched.

## Dependencies and review

Ready: its only need is done. [Review history](review.md); rounds inherited from `improve-harness-quality-eval` and `long-horizon-recall-benchmark`; limit five.
