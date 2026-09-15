---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: fs
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-fs-search-pages
footprint: ["src/main.rs","src/context.rs","src/search.rs","src/service.rs",".cartridge/tests/unit/search/tests.rs",".cartridge/docs/search-pages.md","Cargo.toml","src/files.rs"]
commit: "3a79023311b1a9b30c383ec8c71cf31c20a69ee7"
---

# Bound and continue file search without losing result identity

Large filesystem searches return bounded results with stable continuation behavior and explicit truncation/change diagnostics.

## Acceptance

- [x] A large fixture paginates all matching paths without duplicates or silent omissions under the documented consistency model.
- [x] Tree changes, invalid/expired cursors and cancellation produce explicit outcomes; a bounded result never masquerades as complete.

- [x] Preserve direct filesystem semantics and keep GitFS overlay ownership distinct. New attribution is additive; never auto-import external edits into a session. Retain guarded write behavior and explicit partial failures.

## Proof and recovery

Start at [service.rs](../../../service.rs), [files.rs](../../../files.rs), [search.rs](../../../search.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test fs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-fs-search-pages`; maximum five rounds.

## Current analysis

[Baseline](baseline.json): seven real files yield two items without continuation.
Capture bounded results once, then page the captured result without rerunning
rg. This is a result snapshot, not an atomic tree snapshot. Changes after capture
do not alter its pages; every page explicitly says tree changes are not
revalidated and directs callers to start a new search for current state.
Oversized backend output or snapshot storage fails explicitly; it never claims
a complete partial scan. Keep fs mutation guards and GitFS ownership unchanged.

## Verified result

Public `just test fs` passes 43 tests, including 1,101 real paths, a newline
filename, 301 matches in one file, replay/refresh/expiry/cancellation, full refs,
backend floods, snapshot exhaustion and all mutation guards. Public
`just check fs` passes formatting and clippy. See verification-summary.json.

## From the retired work memo

Folded 2026-09-15 from `work/improve-fs-search-pages.md` (status open). The PRD state above is authoritative.

### Outcome

Large filesystem searches return bounded results with stable continuation behavior and explicit truncation/change diagnostics.

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
- [ ] A large fixture paginates all matching paths without duplicates or silent omissions under the documented consistency model.
- [ ] Tree changes, invalid/expired cursors and cancellation produce explicit outcomes; a bounded result never masquerades as complete.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Reuse existing search polling rather than build another worker system. Specify snapshot versus live continuation, cancellation, byte/row budgets and opaque cursor validation; include paths and match locations for drilldown.
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
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
