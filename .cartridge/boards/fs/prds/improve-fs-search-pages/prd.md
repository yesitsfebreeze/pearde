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
footprint:
- src/main.rs
- src/context.rs
- src/search.rs
- src/service.rs
- .cartridge/tests/unit/search/tests.rs
- .cartridge/docs/search-pages.md
commit: "de1406682a33c5b12cb472787178e2570e5ed0f8"
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
