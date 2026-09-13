---
repo: /Users/feb/dev/cartridge/gitfs.ctg
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
- '@gitfs/improve-gitfs-reviewable-ship/reviewed-owned-tree-commits-locally'
commit: "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36"
---

# A recorded push reconciles the exact remote head

Push an explicitly named reviewed local commit to a bound remote/ref only after
checking the expected remote head. Never force, fetch/rebase or retry a rejected
push automatically. Persist the attempt identity before network dispatch and
reconcile uncertain outcomes by reading the exact recorded remote/ref/commit.

## Acceptance

- [x] Remote advance refuses without force or local history rewrite; unrelated refs remain unchanged.
- [x] Disconnect or cancellation after dispatch returns unknown until exact remote readback proves completion or refusal; reconciliation sends no push.
- [x] A repeated request cannot silently replay an uncertain mutation; local commit and durable attempt evidence remain available.
- [x] Disposable bare-remote fixtures prove accepted, rejected, lost-response and bounded network failure behavior.

## Proof and review lineage

Use disposable repositories and synthetic gates. Preserve the original parent
baseline, acceptance and inherited rounds1–2; maximum5 rounds apply to each child.
Concrete specs and independent round3 review precede source changes. Historical
parent review is [retained](../review.md); splitting does not reset its allowance.
