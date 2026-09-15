---
kind: work
description: "Measure multi-round context quality with real task outcomes"
status: open
priority: P2
size: M
needs:
  - "[improve-harness-compaction-diff](../../../harness/prds/improve-harness-compaction-diff/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["measure multi-round context quality with real task outcomes", "implementing harness cartridge improvements"]
---

# Measure multi-round context quality with real task outcomes

## Outcome

Repeated compaction is evaluated for constraints, corrections, evidence, abstention and task success, beyond fixed fixture correctness.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [rolling-context-retains-decision-evidence](../../prds/rolling-context-retains-decision-evidence/prd.md), [long-horizon-recall-benchmark](../../prds/long-horizon-recall-benchmark/prd.md).

## Footprint

Harness; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `harness.ctg/prompt.rs`
- `harness.ctg/working.rs`
- `harness.ctg/inspection.rs`
- `harness.ctg/inspection_tests.rs`
- `harness.ctg/eval/eval_compaction.py`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Known-good and adversarial summaries trigger the expected classes across at least three rounds; replay checks final task behavior as well as text needles.
- [ ] Opt-in reports include every failure, tokens, latency, model identity and revisions; offline gates explicitly say they do not establish model quality.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Extend the delivered compaction evaluator and coordinate with the existing long-horizon-recall-benchmark rather than duplicating it. Add an offline replay fixture runner and an opt-in model runner with immutable corpus, model and prompt revisions. Predeclare zero tolerance for invented permission/completion and report other losses individually.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test harness
just check harness
python3 harness.ctg/eval/eval_compaction.py --check
```


## Compatibility and recovery

Keep canonical transcripts intact. New metadata/inspection is additive; revert compaction settings without discarding old summaries or their source. Live evaluation requires separately configured models and a bounded budget.

## Handoff

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-harness-compaction-diff](../../../harness/prds/improve-harness-compaction-diff/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
