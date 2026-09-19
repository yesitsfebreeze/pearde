---
state: open
origin: requested
priority: 94
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
footprint:
  - "src/rpc/src/experience/input.rs"
  - "src/graph/src/experience/metadata.rs"
  - "src/graph/src/experience/observe.rs"
  - "src/tick/loop/src/tick_cluster.rs"
  - ".cartridge/tests/unit/src/rpc/src/experience_test.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Every runtime reason identifies its evidence and certainty

Represent reported reasons, observed responses and inferred explanations distinctly inside the existing reason graph. Preserve bounded source identity, correlation and projection revision; missing or redacted context remains explicitly unknown. Inferred causes must cite evidence and never become verified merely through repetition.

## Evidence

The probe confirms response text becomes a Provenance reason when no explicit reason exists. Clustering averages provenance, question, ratification and rephrase vectors without a distinction between observation and inferred cause. See [investigation](../investigation.md).

## Acceptance

- [ ] An explicit reason retains its asserted origin; a response-only event is labelled observed evidence, not a verified causal explanation.
- [ ] A derived explanation retains source references and uncertainty; contradiction or source removal remains visible.
- [ ] Old provenance reasons migrate conservatively as unclassified evidence without reinterpreting them as verified causes.
- [ ] Reason-space clustering uses documented compatible evidence classes, preserves original content vectors, and labels unresolved mixed evidence.

## Proof and recovery

Promote response_is_used_as_provenance_without_reason from the linked probe into RPC regression coverage. Add reason-class serialization, migration and cluster fixtures. Run cargo test --locked -p rpc experience --lib and cargo test --locked -p tick_loop reason_cluster --lib from memory.ctg.

Keep original reason text and vectors during additive schema migration. No external causal model or source-copying subsystem is required. Scope M; extend the existing reason-space work rather than replacing it.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
