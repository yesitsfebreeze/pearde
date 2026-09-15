---
kind: work
description: "Show token estimates alongside serialized bytes"
status: open
priority: P1
size: M
needs:
  - "[improve-router-capability-routing](../../../router/prds/improve-router-capability-routing/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["show token estimates alongside serialized bytes", "implementing harness cartridge improvements"]
---

# Show token estimates alongside serialized bytes

## Outcome

Context inspection reports model-specific estimates, observed provider usage and the source/uncertainty of each count while retaining byte safety limits.

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
- [ ] Fixtures include multilingual text, JSON/tool schemas and a large indivisible exchange; reported budgets remain honest and byte caps still apply.
- [ ] Unknown tokenizer/model yields an explicit unknown/estimate; inspection performs no inference or compaction.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Use configured tokenizer support where available and labelled estimates otherwise; reserve output capacity and preserve complete tool exchanges. Do not claim an estimate is provider acceptance or send a model request merely to inspect.
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

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-router-capability-routing](../../../router/prds/improve-router-capability-routing/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
