---
repo: /Users/feb/dev/cartridge/fs.ctg
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-gitfs-snapshot-selection.md` (status open). The PRD state above is authoritative.

### Outcome

snapshot.paths captures only the caller-selected owned files and reports inaccessible files instead of silently claiming success.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

### Footprint

GitFS and ship; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `gitfs.ctg/service.rs`
- `gitfs.ctg/store.rs`
- `gitfs.ctg/ship.rs`
- `gitfs.ctg/secrets.rs`
- `gitfs.ctg/cartridge.json`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Own A and B, edit both on disk, snapshot only A: overlay B remains unchanged; an empty selection snapshots nothing.
- [ ] Unowned/invalid paths are rejected, read failures are reported, and guarded edits and materialization conflict tests still pass.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Reproduce the current ignored filter in a temporary Git repo. Validate all selections; preserve execute bits and session ownership, distinguish empty selection from omitted paths, and report partial failures explicitly.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test gitfs
just check gitfs
just smoke mcp
```


### Compatibility and recovery

Use temporary Git repos/remotes for checks. Preserve unrelated index/worktree/ref changes. Roll back API additions before applying migrations; committed/pushed mutations require a recorded reconciliation/revert, not an assertion that cancellation undid them.

### Handoff

Priority P0; scope size S (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
