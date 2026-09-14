---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-memo-compact-landscape/bounded-inventory-snapshot
commit: "422c521aed170a4d098505c73469a1a59dccf49d"
---

# Capture one bounded inventory snapshot and page exact owner paths

One owner-local part of @landscape/improve-memo-compact-landscape. Reuse the existing Landscape and memo ownership boundary; the original acceptance and both inherited review rounds remain attached to the parent.

## Acceptance

- [x] A real 10,000 tracked-path fixture yields a default summary at most 16 KiB with explicit omitted counts; bounded pages reconstruct each permitted owner/path exactly once.
- [x] Replacement snapshot, changed filter, malformed or out-of-range cursor refuses explicitly without combining generations.
- [x] Contributor failure preserves usable owners with named partial status; disabled and directoryless owners remain distinct; source files and observation history are unchanged.

## Proof and recovery

Measured baseline precedes this specification. Preserve legacy behavior and source records. Run the public owner test/check and reviewed native or library acceptance fixtures. Named failures retain the last usable published snapshot; no automatic retries.

## Review

Inherits rounds 1–2 from [compact Landscape review](../review.md); maximum five rounds. Round 3 must independently score at least 90 before source edits.
