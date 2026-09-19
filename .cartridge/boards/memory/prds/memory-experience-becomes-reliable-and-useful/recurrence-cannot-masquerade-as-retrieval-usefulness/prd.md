---
state: open
origin: requested
priority: 93
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
needs:
  - "@memory/heat-is-deposited-on-read-back-not-on-delivery"
  - "@memory/a-frozen-query-reads-the-bank-without-touching-it"
footprint:
  - "src/graph/src/experience/observe.rs"
  - "src/base/src/base_types.rs"
  - "src/graph/src/heat.rs"
  - ".cartridge/tests/unit/src/graph/src/tests/heat_test.rs"
  - "src/retrieval/piece/src/retrieval_score.rs"
  - "src/rpc/src/experience/view.rs"
  - ".cartridge/tests/unit/src/retrieval/piece/src/tests/retrieval_score_test.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Recurrence cannot masquerade as retrieval usefulness

Give recurrence and access reinforcement independent clocks and labelled signals. Reuse the existing read-back heat PRD for deciding when use is credited; this leaf does not redefine that decision. Keep confidence independent, and calibrate any ranking blend against held-out retrieval evidence.

## Evidence

Occurrence and access counts are already separate. The reproduced gap is shared heat and heat_updated_at: recurrence refreshes the access cooldown timestamp and suppresses an otherwise eligible retrieval increment. Existing access counts are throttled reinforcement, not literal every-read totals. See [investigation](../investigation.md).

## Acceptance

- [ ] A recurrence burst cannot suppress later read-back accounting or increase retrieval count or confidence.
- [ ] Recurrence heat and use heat decay independently and survive restart with explicitly labelled legacy values.
- [ ] ASP distinguishes offered candidates, read-back evidence and recurrence where measured; it never claims an agent used a result solely because it was returned.
- [ ] Ranking changes include a before/after frozen evaluation and do not promote irrelevant frequent errors over relevant evidence on the labelled fixture.

## Proof and recovery

Promote recurrence_timestamp_suppresses_old_retrieval_count, then add migration and relevance fixtures. Reuse graph/heat.rs for both decay signals; do not duplicate decay formulas. Run cargo test --locked -p retrieval-piece --lib, cargo test --locked -p graph heat --lib and cargo test --locked -p graph experience --lib from memory.ctg; run the existing replay instrument after the canonical frozen-query prerequisite reconciles read_only with its proposed spelling.

Do not estimate historical split heat or exact read counts. Preserve the aggregate as legacy data. Coordinate the shared scoring footprint after the read-back PRD; scope M.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
