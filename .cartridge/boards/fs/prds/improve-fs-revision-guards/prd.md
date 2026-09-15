---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: fs
work-kind: leaf
review-round: 4
review-status: passed
canonical-scope: improve-fs-revision-guards
footprint: ["src/main.rs","src/context.rs","src/files.rs","src/service.rs",".cartridge/tests/unit/service/tests.rs",".cartridge/docs/revision-guards.md","Cargo.toml"]
commit: "3a79023311b1a9b30c383ec8c71cf31c20a69ee7"
needs:
- "@fs/improve-fs-change-provenance"
---

# Use consistent stale-write checks for filesystem mutations

Remove improve-fs-change-provenance from the proposed hard needs: basic stale-write safety must work with current sessions. Reuse existing revision and atomic-write boundaries; attribution additions remain independent. A check-then-write race must be addressed at the actual mutation boundary, not only in request validation.

## Acceptance

- [x] A deterministic barrier changes the file after validation but before commit; newer bytes survive and the stale writer receives a conflict.
- [x] Two writers with the same expected revision cannot both overwrite successfully.
- [x] Direct and overlay APIs preserve executable modes, path validation, cancellation and explicitly reported partial success without importing external ownership.

## Proof and recovery

Start at [service.rs](../../../service.rs), [files.rs](../../../files.rs), [search.rs](../../../search.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test fs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-fs-revision-guards`; maximum five rounds.

## Current analysis

[Baseline](baseline.json) reproduces lost newer bytes at publication. The owner is
fs; gitfs remains a separate overlay owner and its existing compatibility gate
is retained. Two writers are tested through the shared fs service and existing
per-target serialization. Ordinary filesystem rename is not an atomic
compare-and-swap against uncooperative external processes: the final check
detects changes during preparation, with the remaining check/rename window
explicitly documented. No external ownership or automatic retry is introduced.

## Verified result

The controlled lost-write probe now passes. Public `just test fs` passes all
34 tests; `just check fs` passes formatting and clippy. Public `just test gitfs`
passes 22 tests, including real consumer interoperability, stale overlay edit,
materialization guard, selection and partial-error coverage. Source files remain
inside the reviewed footprint. See [verification-summary.json](verification-summary.json).

## Reverification after search paging

Search paging changes shared service.rs. The unchanged publication proof is
re-run against the integrated owner commit; its initial receipt is retained in
collection-475962d8.md. Product acceptance and specification are unchanged.

## From the retired work memo

Folded 2026-09-15 from `work/improve-fs-revision-guards.md` (status open). The PRD state above is authoritative.

### Outcome

Every applicable file mutation validates the expected source revision and reports a conflict before overwriting changed data.

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
- [ ] Change the file between read and write/edit: stale requests leave newer bytes intact and return the current revision.
- [ ] Executable mode, invalid context, missing target and cancellation cases remain correct across direct FS and overlay APIs.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Audit existing freshness guards and preserve what already works. Fill gaps across write/edit and ownership reconciliation with consistent revision semantics, path validation and explicit partial-success reporting.
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
Ready after [improve-fs-change-provenance](../improve-fs-change-provenance/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
