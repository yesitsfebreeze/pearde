---
state: open
origin: requested
priority: 91
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @memory/memory-owns-its-tool
  - @landscape/landscape-composes-system-context
  - @runtime/one-runner-executes-documents
  - @landscape/recursive-development-graph
footprint:
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/memos
  - /Users/feb/dev/cartridge/memory.ctg/tests/cartridge.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/tests
  - /Users/feb/dev/cartridge/memo.ctg/tests
---

# A memory document is discovered, read, executed, and improved live

This is the first complete proof of the product model, before migrating the remaining capabilities.

## Ownership and scope

Owner: `cartridge-system`. Participating repositories: `memory.ctg`, `memo.ctg`, `landscape.ctg`, `cartridge.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Author memory-owned query and ingest recipes using the established dialect and existing native memory service. Keep the generic runner out of memory.
2. Create a disposable composition with the real owner cartridges and a deterministic local embedding/provider fixture.
3. Drive discovery, all read views, policy, execution, exact fact readback, and attributed outcome capture through production entry points.
4. Edit the document and rebuild/reload a fixture backend; prove that subsequent discovery and execution use the new revision while an invalid candidate retains the old working implementation.

## Acceptance contract

- A memory-only fact is found by the common landscape query and read back by its returned reference.
- Commands, docs, and human views identify the same source revision and corresponding recipe.
- An authorized ingest is committed and recallable by a later session; a denied ingest leaves the store unchanged.
- A document edit becomes visible without restarting unrelated cartridges; stale invocation fails before running.
- An invalid reload leaves committed knowledge and the previous service usable; observed results name document/backend revisions.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test memory --test cartridge
just test memo
just test landscape
just test runtime reload
just smoke
```

## Failure and recovery

A unit-only demonstration hides transport, cwd, or writer-lock failures. Use real binaries and separate sessions with temporary state.

Rollback: Return the test profile to legacy memory-tool compatibility while preserving stores and documents. No global profile cutover until the fixture proves equivalence.

## Prior context

Related existing runtime memo leaf names: `the-agent-can-extend-and-verify-a-cartridge`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
