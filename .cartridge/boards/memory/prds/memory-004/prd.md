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
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: MEMORY-004
---

# Decide how ranking treats cold rows on a spilled store

`.cartridge/tests/integration/bench/RESULTS.md` shows the gap. Under the full pipeline, `linked_evidence` MRR is 0.967 hot, but only 0.532 mixed and 0.511 cold. Plain hybrid fusion scores about 0.92 on the same questions. Cold rows have no resident edges, yet graph-leg candidates still enter fusion (`cold_candidates` and fusion in `src/retrieval/piece/src/retrieval_query.rs`). The replay harness already reports per-category metrics in the hot, mixed and cold layouts (`bench/src/replay.rs`, run by `just eval-mature` and `just eval-replay`). Outcome, owned by memory: a written decision among three options (expansion credit for cold rows, residency-aware fusion weighting, or neither), backed by candidate measurements. The default does not change.

## Acceptance

- [ ] Before any candidate runs, RESULTS.md records regression thresholds per layout and category. `current_fact` and `historical_fact` may not drop, and multi-evidence is read from `recall_all@k`.
- [ ] Each candidate is measured on `mature.json` and `replay.json` in all three layouts, and the results are appended with source revision and exact commands.
- [ ] The decision and its reasoning are recorded in `.cartridge/docs/WORK_ITEMS.md` MEMORY-004 or a memory decision memo. The default pipeline is unchanged, and a rejected candidate leaves no code on `main`.

## Proof and recovery

First probe: from /Users/feb/dev/cartridge/memory.ctg at `c25af4d`, rerun `just eval-mature` and `just eval-replay`. Confirm they need no live model endpoint (record it if they do), and stop if the baseline does not reproduce RESULTS.md within the stated noise. Candidates sit behind a config knob that is off by default. Gates: `just check`, `just test`. Nothing was run in planning. Partial status for cold reads belongs to parked-memory-remains-recallable, not here.

## Dependencies and review

No hard needs. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
