---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: gitfs
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-gitfs-reviewable-ship
needs:
- '@gitfs/improve-gitfs-readable-diff'
- '@gitfs/improve-gitfs-snapshot-selection'
- '@policy/improve-policy-operation-rules'
footprint: ["src/ship.rs","src/store.rs","src/tool_result.rs","src/main.rs",".cartridge/tests/unit/ship/tests.rs",".cartridge/tests/unit/store/tests.rs",".cartridge/tests/integration/reviewed-ship.test.ts",".cartridge/docs/ship.md","Cargo.toml","src/provenance.rs",".cartridge/tests/unit/provenance.rs",".cartridge/tests/integration/change-provenance.test.ts",".cartridge/docs/change-provenance.md"]
commit: "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36"
---

# A reviewed owned tree commits locally

Preview the exact session-owned tree, branch/base/index/overlay revisions,
canonical repository identity, author identity and required gate policy. Commit
revalidates that snapshot and publishes only that tree with an expected-head CAS.
A configured gate always runs, including when the caller supplies a message.
Commit and remote push are separate calls; preview or cancellation never launches
a remote push. Automation attribution is accurate and never invents a co-author.

## Acceptance

- [x] Stale base/index/overlay/root or changed reviewed inputs refuse publication; unrelated staged files and new trunk files stay unowned.
- [x] Required gate hold/error/timeout and cancellation before publication leave branch history unchanged; explicit messages cannot bypass gates.
- [x] Exact reviewed tree, parent, author and session attribution match the published commit; partial publication failure is named without automatic retry.
- [x] Public tool envelope and native fixture gates pass; preview/local commit never contacts a push remote.

## Proof and review lineage

Use disposable repositories and synthetic gates. Preserve the original parent
baseline, acceptance and inherited rounds1–2; maximum5 rounds apply to each child.
Concrete specs and independent round3 review precede source changes. Historical
parent review is [retained](../review.md); splitting does not reset its allowance.

Recorded-push revalidation at b4b95bb: shared native registration and new registered module are bound; original acceptance and executable gates are unchanged.
