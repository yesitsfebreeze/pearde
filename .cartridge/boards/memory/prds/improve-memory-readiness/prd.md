---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: improve-memory-readiness
needs:
- '@memory/improve-memory-owner-access'
footprint: ["Cargo.lock","src/store/core/Cargo.toml","src/cartridge.rs","src/cartridge_status.rs","src/commands/src/memory.rs","src/transport/src/owner.rs","src/transport/src/memory_rpc.rs","src/store/core/src/lock.rs","src/rpc/src/server.rs",".cartridge/tests/unit/src/cartridge/status_test.rs",".cartridge/tests/unit/src/cartridge/tests.rs",".cartridge/tests/unit/src/store/core/src/tests/lock_test.rs",".cartridge/tests/unit/src/transport/src/owner_test.rs",".cartridge/tests/integration/cartridge.rs",".cartridge/tests/integration/e2e/cli_surface.rs",".cartridge/tests/integration/e2e/focus_routing.rs",".cartridge/docs/owner-attachment.md",".cartridge/docs/CARTRIDGE.md"]
capability-owner: "memory"
commit: "a124fd30d59bcd06062b5464810188a0288e461e"
---

# Report memory readiness separately from registration

A registered memory provider exposes store/model readiness and the reason it cannot currently serve a request.

## Acceptance

- [x] The contention fixture reports active registration and unavailable query readiness with retryability; it never reports ready from registration alone.
- [x] Status requests have a deadline, redact credentials, and do not start a writer; after owner recovery status updates without restarting the caller.

- [x] Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [cartridge.rs](../../../../../../memory.ctg/.cartridge/tests/integration/cartridge.rs), [CARTRIDGE.md](../../../../../../memory.ctg/.cartridge/docs/CARTRIDGE.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. Final public gates passed: 1402 tests, 17 existing skips, documentation tests and just check; see implementation-proof.json.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-readiness`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-memory-readiness.md` (status open). The PRD state above is authoritative.

### Outcome

A registered memory provider exposes store/model readiness and the reason it cannot currently serve a request.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

### Footprint

Memory; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `memory.ctg/src/cartridge.rs`
- `memory.ctg/src/transport/src`
- `memory.ctg/src/commands/src`
- `memory.ctg/tests/cartridge.rs`
- `memory.ctg/CARTRIDGE.md`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] The contention fixture reports active registration and unavailable query readiness with retryability; it never reports ready from registration alone.
- [ ] Status requests have a deadline, redact credentials, and do not start a writer; after owner recovery status updates without restarting the caller.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Reuse health/ready operations and define a bounded adapter status response: unknown, starting, ready, degraded, unavailable. Distinguish cached status from an explicitly requested probe; discovery itself must not open a database or call a model.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test memory --test cartridge
just check memory
just test memory
```

Implementation must use an isolated branch/worktree per memory.ctg/AGENTS.md. Run the memory repository's full required gates before landing; preserve databases, provenance and documents.

### Compatibility and recovery

Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

### Handoff

Priority P0; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-memory-owner-access](../improve-memory-owner-access/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
