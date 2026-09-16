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
canonical-scope: tool-results-interoperate
footprint: ["src/main.rs","src/service.rs","src/ship.rs","src/tool_result.rs",".cartridge/tests/unit/tool_result.rs",".cartridge/tests/integration/tool-result.test.ts","Cargo.toml","src/provenance.rs",".cartridge/tests/unit/provenance.rs",".cartridge/tests/integration/change-provenance.test.ts",".cartridge/docs/change-provenance.md"]
commit: "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36"
---

# Every currently exposed tool completes through its real consumers

This PRD owns the immediate interoperability fix; the older improve-tool-result-contract becomes its coverage reference. Keep the current content:string/error:boolean wire. Serialize structured domain payloads exactly once at the producing tool boundary; consumers share fixtures and reject malformed results without guessing a second operation. A later richer negotiated protocol is outside this repair.

## Acceptance

- [x] Real direct, MCP and proxy GitFS read/ship scan return equivalent decoded payloads; a string that itself contains JSON is not double-normalized.
- [x] Invalid request input and policy refusal cause zero backend calls. A malformed response discovered after a fixture mutation reports an explicit failed/unknown outcome and causes no retry or follow-on mutation.
- [x] Native agent resumes after ordinary tool failure, while cancellation and partial effects retain the original invocation identity.

## Proof and recovery

Start at [service.rs](../../../service.rs), [ship.rs](../../../ship.rs), [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `tool-results-interoperate`, `improve-tool-result-contract`; maximum five rounds.

## Verified implementation — 2026-09-13

`cargo test --manifest-path ../gitfs.ctg/Cargo.toml -p gitfs` passed all 19 tests.
The real daemon/socket fixture passed 188 assertions through direct SDK, MCP and
proxy read/scan, zero-effect rejection, malformed-result no-replay and ordinary
error recovery. The fixture isolates its compiler target and disables wrappers;
the first shared-target run exposed read-only cached artifacts and was rejected.
The native agent ordinary-error and exact-cancellation gates both passed.
Cancellation acknowledgments and partial-effect behavior are unchanged.

## Reverification — 2026-09-13

The snapshot-selection change 21be1528 touches the producer service footprint.
Reopened for fresh execution of the unchanged interoperability specification;
the original proof remains in collection-cf18e856.md. No acceptance is waived.

## Reverification after read-only inspection

Inspection changes shared GitFS source. Re-run this unchanged specification
against the integrated owner commit. Prior receipt is collection-21be1528.md.

Recorded-push revalidation at b4b95bb: shared native registration and new registered module are bound; original acceptance and executable gates are unchanged.
