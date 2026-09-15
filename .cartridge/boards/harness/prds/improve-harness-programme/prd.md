---
repo: /Users/feb/dev/cartridge/harness.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: harness
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: improve-harness-programme
needs:
- '@harness/improve-harness-token-accounting'
- '@harness/improve-harness-compaction-diff'
- '@harness/improve-harness-quality-eval'
---

# Harness improvement plan

Roll-up only; claim a leaf for implementation. Token accounting (harness ca7eeab) and
compaction diff (a282c87) are done; quality evaluation remains open and reuses the existing
compaction corpus rather than a second one.

## Acceptance

- [ ] Each linked leaf is done with its own revision-bound proof and passed review.
- [ ] At one pinned harness revision, `just test harness` (cwd `/Users/feb/dev/cartridge`) passes, or every remaining failure is named with its owner.
- [ ] Remaining limitations (offline corpus is not model quality) are recorded at that revision.

## Work items

- [Show token estimates alongside serialized bytes](../improve-harness-token-accounting/prd.md) — done
- [Inspect what each compaction retained and removed](../improve-harness-compaction-diff/prd.md) — done
- [Measure multi-round context quality with real task outcomes](../improve-harness-quality-eval/prd.md) — open

## Failure and review

If a leaf exhausts its review allowance, this parent stays open and records that leaf's gaps;
done leaves are not reopened. [Review history](review.md); limit five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-harness-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Harness improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Harness, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Show token estimates alongside serialized bytes | [improve-harness-token-accounting](../improve-harness-token-accounting/prd.md) |
| 2. Inspect what each compaction retained and removed | [improve-harness-compaction-diff](../improve-harness-compaction-diff/prd.md) |
| 3. Measure multi-round context quality with real task outcomes | [improve-harness-quality-eval](../improve-harness-quality-eval/prd.md) |

### Downside coverage

1. Summaries lose details: semantic regression corpus and before/after evidence.
2. Bytes do not equal tokens: show measured/estimated/unknown accounting explicitly.
3. Compaction costs time and inference: record usage and benchmark outcomes before tuning thresholds.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [rolling-context-retains-decision-evidence](../../../root/prds/rolling-context-retains-decision-evidence/prd.md), [long-horizon-recall-benchmark](../../../root/prds/long-horizon-recall-benchmark/prd.md). Their current source, status and owner take precedence over a stale assessment.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Harness behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test harness
just check harness
python3 harness.ctg/eval/eval_compaction.py --check
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
