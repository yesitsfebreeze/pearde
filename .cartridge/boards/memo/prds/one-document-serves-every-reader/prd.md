---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memo
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: one-document-serves-every-reader
needs:
- '@memo/one-document-serves-every-reader/document-identity'
- '@memo/one-document-serves-every-reader/document-projections'
- '@memo/one-document-serves-every-reader/executable-document-validation'
---

# One Markdown document supplies discovery, commands, and readable guidance

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [Readers agree on document identity and revision](document-identity/prd.md)
- [Readable projections hydrate bounded linked prose](document-projections/prd.md)
- [Invalid executable documents refuse before launch](executable-document-validation/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-document-serves-every-reader`, `a-tool-is-declared-by-its-memo`; maximum five rounds.
