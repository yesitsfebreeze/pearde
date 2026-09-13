---
state: open
origin: requested
priority: 93
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @memo/one-document-serves-every-reader
footprint:
  - /Users/feb/dev/cartridge/landscape.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/landscape.ctg/src/surface.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/service.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/record.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/landscape.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/tests/landscape.rs
---

# Landscape answers across kernel, directories, memo, memory, and live state

Landscape is the whole relevant system pressed into context. Today it graphs composition, descriptors, memo rows, and observations, while memory recall and other live context remain separate.

## Ownership and scope

Owner: `landscape`. Participating repositories: `landscape.ctg`, `memo.ctg`, `memory.ctg`, `cartridge.ctg`, `sessions.ctg`, `pty.ctg`, `router.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Retain the existing in-process landscape library and memo landscape facade. Put graph/query ownership in landscape and supply source adapters from the facade; do not create a new daemon or another durable database.
2. Define contributor rows and status envelopes. Add query-bounded memory candidates and exact memory readback; collect kernel generations, directory/file metadata, document metadata, session/terminal state, and redacted router capabilities through their existing owners.
3. Namespace nodes by owner and kind, join stable references, and preserve source revisions/freshness. Separate disabled, absent, unavailable, and empty contributors.
4. Implement one deterministic selection/ranking stage over candidates with per-source budgets, query deadlines, deduplication, and bounded linked-context expansion. Keep body hydration after selection.
5. Keep old landscape/resolve callers compatible while adding explicit views. Report missing contributors instead of silently claiming a complete context.

## Acceptance contract

- One query returns a memo-only hit, a memory-only hit, a file/directory hit, and a kernel capability with usable source references.
- Reading a memory hit retrieves the exact fact by ID rather than running a guessed second semantic query.
- A profile without memory remains useful; a timed-out configured memory contributor produces partial=true and a named status.
- Directory ownership and two cartridges with identical leaf filenames do not collide; disabled/private contributions do not leak into another scope.
- Identical source snapshots yield stable ordering/revisions; an edited document or reloaded generation invalidates affected cached results/cursors.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test landscape
just test memo
just test runtime landscape
just test memory --test cartridge
```

## Failure and recovery

One unavailable source stalls all context, or successful empty results conceal failed scans. Bound each contributor and expose completeness.

Rollback: Keep the original projection path behind the facade during rollout and preserve result fields. Drop derived caches to recover; leave source records untouched.

## Prior context

Related existing runtime memo leaf names: `the-landscape-owns-the-graph`, `one-search-covers-the-record-and-memory`, `context-is-living-not-per-session`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
