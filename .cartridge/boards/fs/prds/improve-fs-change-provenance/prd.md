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
capability-owner: "fs"
commit: "3a79023311b1a9b30c383ec8c71cf31c20a69ee7"
needs:
- "@sessions/file-change-records-retain-reported-revisions"
- "@fs/improve-fs-change-provenance/direct-file-mutations-report-revisions"
- "@gitfs/overlay-mutations-report-revisions"
- "@runtime/shipped-gitfs-profiles-grant-change-recording"
- "@gitfs/improve-gitfs-readable-diff"
- "@sessions/improve-sessions-client-mapping"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-fs-change-provenance.md` (status open). The PRD state above is authoritative.

### Outcome

Touched-file records identify actor, operation, storage target and revisions so direct and GitFS changes can be reconciled.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

### Footprint

Filesystem tools; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `fs.ctg/service.rs`
- `fs.ctg/files.rs`
- `fs.ctg/search.rs`
- `fs.ctg/service/tests.rs`
- `sessions.ctg/main.rs`
- `gitfs.ctg/service.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Direct edit and overlay edit of the same path produce distinct attributable records and a visible divergence.
- [ ] External edits and unrelated files never become owned implicitly; legacy touched-file records remain readable.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Define one bounded change-evidence structure at the sessions boundary. Do not equate observation with ownership: direct edits acquire no GitFS ownership unless explicitly selected for snapshot/import. Avoid merging storage backends.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test fs
just check fs
just test gitfs
just test sessions
```


### Compatibility and recovery

Preserve direct filesystem semantics and keep GitFS overlay ownership distinct. New attribution is additive; never auto-import external edits into a session. Retain guarded write behavior and explicit partial failures.

### Handoff

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-gitfs-readable-diff](../../../gitfs/prds/improve-gitfs-readable-diff/prd.md), [improve-sessions-client-mapping](../../../sessions/prds/improve-sessions-client-mapping/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
