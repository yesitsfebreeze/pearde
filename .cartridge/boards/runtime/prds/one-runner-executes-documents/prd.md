---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: one-runner-executes-documents
needs:
- '@runtime/one-runner-executes-documents/approved-document-launch'
- '@runtime/one-runner-executes-documents/document-command-result'
- '@runtime/one-runner-executes-documents/document-artifact-result'
---

# A shared execution path runs a selected just recipe

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [Only an approved frozen invocation reaches spawn](approved-document-launch/prd.md)
- [A document command reports its real completion](document-command-result/prd.md)
- [An artifact result reads only the approved output](document-artifact-result/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-runner-executes-documents`; maximum five rounds.
