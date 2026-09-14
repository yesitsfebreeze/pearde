---
repo: /Users/feb/dev/cartridge/harness.ctg
state: open
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
