---
repo: /Users/feb/dev/cartridge/gitfs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: gitfs
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: improve-gitfs-snapshot-selection
footprint: ["src/service.rs",".cartridge/tests/unit/snapshot.rs","Cargo.toml","src/provenance.rs",".cartridge/tests/unit/provenance.rs",".cartridge/tests/integration/change-provenance.test.ts",".cartridge/docs/change-provenance.md"]
commit: "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36"
---

# Snapshot exactly the selected owned paths

snapshot.paths captures only the caller-selected owned files and reports inaccessible files instead of silently claiming success.

## Acceptance

- [x] Own A and B, edit both on disk, snapshot only A: overlay B remains unchanged; an empty selection snapshots nothing.
- [x] Unowned/invalid paths are rejected, read failures are reported, and guarded edits and materialization conflict tests still pass.

- [x] Use temporary Git repos/remotes for checks. Preserve unrelated index/worktree/ref changes. Roll back API additions before applying migrations; committed/pushed mutations require a recorded reconciliation/revert, not an assertion that cancellation undid them.

## Proof and recovery

Start at [service.rs](../../../service.rs), [store.rs](../../../store.rs), [ship.rs](../../../ship.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-gitfs-snapshot-selection`; maximum five rounds.

## Verified implementation — 2026-09-13

The 22-test GitFS gate passes, including selected/empty/omitted/duplicate paths,
all-or-nothing selection validation, missing/directory read errors with partial
success, unchanged unrelated index/worktree/refs, executable overlay mode,
stale edit refusal, existing materialization conflict and real-consumer tests.
The pre-fix runtime probe is retained in baseline.json.

## Reverification after read-only inspection

Inspection changes shared GitFS source. Re-run this unchanged specification
against the integrated owner commit. Prior receipt is collection-21be1528.md.
