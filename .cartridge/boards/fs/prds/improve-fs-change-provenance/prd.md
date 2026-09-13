---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
work-kind: "rollup"
review-round: 3
review-status: "passed"
canonical-scope: improve-fs-change-provenance
needs: ["@sessions/file-change-records-retain-reported-revisions","@fs/improve-fs-change-provenance/direct-file-mutations-report-revisions","@gitfs/overlay-mutations-report-revisions","@runtime/shipped-gitfs-profiles-grant-change-recording"]
capability-owner: "fs"
commit: "3a79023311b1a9b30c383ec8c71cf31c20a69ee7"
---

# Share change attribution between direct files and overlays

Touched-file records identify actor, operation, storage target and revisions so direct and GitFS changes can be reconciled.

## Acceptance

- [x] Direct edit and overlay edit of the same path produce distinct attributable records and a visible divergence.
- [x] External edits and unrelated files never become owned implicitly; legacy touched-file records remain readable.

- [x] Preserve direct filesystem semantics and keep GitFS overlay ownership distinct. New attribution is additive; never auto-import external edits into a session. Retain guarded write behavior and explicit partial failures.

## Proof and recovery

Start at [service.rs](../../../service.rs), [files.rs](../../../files.rs), [search.rs](../../../search.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test fs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-fs-change-provenance`; maximum five rounds.
