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
canonical-scope: documents-own-live-processes
needs:
- '@runtime/documents-own-live-processes/document-sidecar-lifecycle'
- '@runtime/documents-own-live-processes/document-event-activation'
---

# Sidecars, event tools, and reload have explicit lifetimes

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [A sidecar belongs to one ready owner generation](document-sidecar-lifecycle/prd.md)
- [Event activation resumes from a durable cursor](document-event-activation/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `documents-own-live-processes`; maximum five rounds.
