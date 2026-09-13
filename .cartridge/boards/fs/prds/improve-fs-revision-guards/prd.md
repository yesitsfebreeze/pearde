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
