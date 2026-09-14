---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: rollup
review-round: 3
review-status: failed
canonical-scope: one-runner-executes-documents
needs:
- '@runtime/one-runner-executes-documents/approved-document-launch'
- '@runtime/one-runner-executes-documents/document-command-result'
- '@runtime/one-runner-executes-documents/document-artifact-result'
---

# A shared execution path runs a selected just recipe

Coordinate the linked outcomes. Claim and implement a leaf; this parent records
only their combined acceptance.

Current route (2026-09-14): memo already validates a document and emits a frozen
invocation: source digest, recipe, argv, execution base and
`launch_authorized: false` (`memo.ctg/src/validation.rs`). Nothing executes that
invocation yet. The transport host no longer runs tool commands. Cartridges spawn
inside their own grant (`cartridge.spawn`, `src/sandbox.rs`), and behavior
belongs to cartridges (decisions `tui-and-tools-are-cartridges`,
`a-cartridge-brings-its-own-surface`, `the-tool-contract-is-a-memo`).
Recommended default: memo executes its own approved invocation inside its grant,
and the host supplies only the wall. The leaves still describe a host runner,
must be rebased to this route and may need rehoming to the memo board.
`.cartridge/tools/memo-run` stays the trusted local development adapter, not
this runner.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] At one pinned memo.ctg and cartridge.ctg revision, one validated fixture document runs end to end: validate, approve, execute, read the artifact. `just test memo` and `just test runtime` pass from `/Users/feb/dev/cartridge`.

## Work items

- [Only an approved frozen invocation reaches spawn](approved-document-launch/prd.md)
- [A document command reports its real completion](document-command-result/prd.md)
- [An artifact result reads only the approved output](document-artifact-result/prd.md)

## Review

[Review history](review.md): round 3/5.
