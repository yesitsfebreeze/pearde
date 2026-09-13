---
kind: work
description: "Deliver the three Harness improvements with explicit risk coverage"
status: open
subwork:
  - "[[@prd/work/root--improve-harness-token-accounting.md]]"
  - "[[@prd/work/root--improve-harness-compaction-diff.md]]"
  - "[[@prd/work/root--improve-harness-quality-eval.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["planning harness improvements", "reviewing harness cartridge readiness"]
---

# Harness improvement plan

## Outcome

Deliver the three improvements requested for Harness, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Show token estimates alongside serialized bytes | [[@prd/work/root--improve-harness-token-accounting.md]] |
| 2. Inspect what each compaction retained and removed | [[@prd/work/root--improve-harness-compaction-diff.md]] |
| 3. Measure multi-round context quality with real task outcomes | [[@prd/work/root--improve-harness-quality-eval.md]] |

## Downside coverage

1. Summaries lose details: semantic regression corpus and before/after evidence.
2. Bytes do not equal tokens: show measured/estimated/unknown accounting explicitly.
3. Compaction costs time and inference: record usage and benchmark outcomes before tuning thresholds.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [[@prd/work/root--rolling-context-retains-decision-evidence.md]], [[@prd/work/root--long-horizon-recall-benchmark.md]]. Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Harness behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test harness
just check harness
python3 harness.ctg/eval/eval_compaction.py --check
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
