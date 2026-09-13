---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: landscape-inventory-facade
needs:
- "@landscape/improve-memo-compact-landscape/bounded-inventory-snapshot"
commit: "45d5a54ab9da1a798cd9997af9a8c19bed8a1812"
---

# Expose versioned compact Landscape through native memo

One owner-local part of @landscape/improve-memo-compact-landscape. Reuse the existing Landscape and memo ownership boundary; the original acceptance and both inherited review rounds remain attached to the parent.

## Acceptance

- [x] Native version 2 summary and explicit inventory pages share the exact frozen Landscape snapshot and bounded responses; legacy requests retain their contract.
- [x] Refresh, service restart, owner filter changes and concurrent captures cannot silently mix old cursors or publish an older snapshot.
- [x] One host snapshot call and bounded readonly library collection produce partial diagnostics; inventory reads require no new host calls or source reads and never activate tools or rewrite memos.

## Proof and recovery

Measured baseline precedes this specification. Preserve legacy behavior and source records. Run the public owner test/check and reviewed native or library acceptance fixtures. Named failures retain the last usable published snapshot; no automatic retries.

## Review

Inherits rounds 1–2 from [compact Landscape review](../../../landscape/prds/improve-memo-compact-landscape/review.md); maximum five rounds. Round 3 must independently score at least 90 before source edits.
