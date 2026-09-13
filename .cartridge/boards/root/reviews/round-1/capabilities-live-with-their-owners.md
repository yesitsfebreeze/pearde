---
state: open
origin: requested
priority: 80
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @mcp/clients-share-document-execution
footprint:
  - /Users/feb/dev/cartridge/memo.ctg/.cartridge/memos
  - /Users/feb/dev/cartridge/fs.ctg/.cartridge/memos
  - /Users/feb/dev/cartridge/gitfs.ctg/.cartridge/memos
  - /Users/feb/dev/cartridge/gitfs.ctg/service.rs
  - /Users/feb/dev/cartridge/gitfs.ctg/ship.rs
  - /Users/feb/dev/cartridge/pty.ctg/.cartridge/memos
  - /Users/feb/dev/cartridge/sessions.ctg/.cartridge/memos
  - /Users/feb/dev/cartridge/router.ctg/.cartridge/memos
  - /Users/feb/dev/cartridge/router.ctg/tests
---

# Each capability ships its own executable documentation

The remaining capability catalog should be owner-local documents over reusable domain services, not separate hand-maintained lists.

## Ownership and scope

Owner: `cartridge-system`. Participating repositories: `memo.ctg`, `fs.ctg`, `gitfs.ctg`, `pty.ctg`, `sessions.ctg`, `router.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Migrate one owner per implementation slice: memo validated writes; Git overlay/read/edit/materialize/ship; shell; sessions inspection; router status/model/launch commands. Development-tool documents belong to the separate developer-workflow PRD.
2. Preserve Git overlay versus direct filesystem semantics. Reconcile the older open fs-removal proposal with current consumers: keep it optional during parity work; retire only if replacement checks and a consumer census justify it.
3. Make gitfs cancellation honest and effective where interruptible; report completion/partial effects at non-interruptible boundaries. Expose optional router gating intentionally.
4. Add real command probes and documentation for each owner, including working directory, prerequisites, state ownership, failures, and reload behavior. Exercise router provider behavior with local protocol fixtures; keep live credentials out of offline gates.
5. Generate compatibility descriptions from documents and delete duplicate descriptions only after consumers have migrated.

## Acceptance contract

- Every enabled capability has an owner document and an isolated success/failure probe; a listing alone is insufficient.
- Git writes remain overlays until materialize; direct file edits retain freshness/overwrite guards; shipping touches only session-owned paths.
- A shell command uses the intended persistent PTY; a generic build recipe does not corrupt its interactive input.
- Memory/memo writes remain validated service operations; raw shell access is not substituted for integrity-sensitive APIs.
- No unused-wrapper deletion removes an actual consumer or its behavioral tests.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test memo
just test fs
just test gitfs
just test pty
just test sessions
just test router
just smoke
```

## Failure and recovery

A simplification changes write semantics or strips domain checks. Keep storage-mode parity tests in the owning repository.

Rollback: Retain optional legacy bindings per owner until equivalence is proved. Store/history formats remain owned by the original backends.

## Prior context

Related existing runtime memo leaf names: `the-tool-surface-is-search-and-shell`, `every-enabled-tool-ships-a-contract-probe`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
