---
kind: work
description: "Inspect what each compaction retained and removed"
status: open
priority: P1
size: M
uses:
  - usage: "[[read-usage]]"
    when: ["inspect what each compaction retained and removed", "implementing harness cartridge improvements"]
---

# Inspect what each compaction retained and removed

## Outcome

The inspector shows original covered messages, resulting summary, retained tail and revision/time/usage evidence for a compaction.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [[@prd/work/root--rolling-context-retains-decision-evidence.md]], [[@prd/work/root--long-horizon-recall-benchmark.md]].

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
- [ ] After two compactions, inspection maps each summary to its exact covered prefix and shows corrected user constraints in source and result.
- [ ] A failed compaction retains the prior summary; requesting its comparison makes no model call and leaks no authorization headers.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Build on canonical transcript and prefix hashes. Store bounded summary metadata and provide source drilldown instead of duplicating whole transcripts; distinguish semantic judgments from literal differences.
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
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
