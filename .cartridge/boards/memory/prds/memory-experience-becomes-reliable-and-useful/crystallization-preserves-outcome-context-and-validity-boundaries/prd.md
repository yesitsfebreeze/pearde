---
state: open
origin: requested
priority: 97
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
needs:
  - "@memory/memory-experience-becomes-reliable-and-useful/every-runtime-reason-identifies-its-evidence-and-certainty"
footprint:
  - "src/rpc/src/experience/input.rs"
  - "src/graph/src/experience/matching.rs"
  - "src/graph/src/experience/metadata.rs"
  - "src/graph/src/experience/observe.rs"
  - ".cartridge/tests/unit/src/graph/src/tests/experience_test.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Crystallization preserves outcome context and validity boundaries

Use typed outcome and semantic scope as mandatory eligibility checks before both exact and semantic merging. Join started and finished evidence using bounded correlation handling where necessary; correlation identifies occurrences but must not disable legitimate recurrence across runs.

## Evidence

Tests confirm explicit opposite outcomes remain separate, but error:true is classified as answered; outer context is discarded; expired active entities remain exact merge targets. Equal candidate vectors can merge distinct contexts. See [investigation](../investigation.md).

## Acceptance

- [ ] Identical vectors cannot merge success, failure, cancellation or unknown outcomes; native error:true and supported MCP error flags normalize correctly.
- [ ] The same error in incompatible project/resource/configuration scopes stays separate; same-scope paraphrases can merge.
- [ ] Expired, invalidated and superseded candidates are refused by exact and ANN paths, including unloaded owners.
- [ ] Absent context stays unknown; late, duplicate or missing lifecycle halves do not fabricate success or double-count completed occurrences.

## Proof and recovery

Promote the outcome, context and expired-target probes; add identical-vector adversarial and out-of-order lifecycle fixtures. Run cargo test --locked -p graph -p rpc experience --lib from memory.ctg. Pin failing assertions before implementation.

Keep old representatives readable and preserve ambiguous groups rather than automatically splitting unknowable historical occurrences. Version new identity rules. Scope M.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
