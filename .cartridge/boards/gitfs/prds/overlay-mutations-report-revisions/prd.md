---
repo: /Users/feb/dev/cartridge/gitfs.ctg
state: "done"
workflow: develop-one-cartridge
capability-owner: gitfs
work-kind: leaf
review-round: 3
review-status: "passed"
needs:
- '@sessions/file-change-records-retain-reported-revisions'
- '@gitfs/improve-gitfs-readable-diff'
commit: "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36"
---

# Report actual overlay and materialized changes

Emit Sessions-owned evidence for successful GitFS write/edit/snapshot/materialize
changes, using receipts captured at the existing mutation boundary. The current
GitFS diff already exposes divergence; reuse it without creating a second
inspection or ownership engine. Native context identifies a reported session/run/
call, not an authenticated human or client.

## Acceptance

- [x] Overlay write/edit and selected snapshot record actual before/after blob and commit revisions; unchanged/refused paths produce no invented publication.
- [x] Materialization records only known applied direct targets; mixed failures preserve applied receipts and explicit partial outcomes.
- [x] With Sessions granted, records survive through the real owner; missing grants preserve standalone behavior with unavailable attribution, while recording failure never rolls back or retries mutations.
- [x] Existing list/diff/read, ownership guards, snapshot selection, reviewed ship/push and policy compatibility tests remain green; unrelated/external files gain no ownership.

Use the current locks, refs and materialization result, adding structured evidence
rather than parsing human output. Do not add required Sessions injection, global
logging, automatic import or cross-owner transactions. Inherit two review rounds.
