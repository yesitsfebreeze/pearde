---
state: open
origin: requested
priority: 97
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @memo/memo-board-template
  - @memo/one-document-serves-every-reader
footprint:
  - /Users/feb/dev/cartridge/landscape.ctg/src/surface.rs
  - /Users/feb/dev/cartridge/landscape.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/record.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/service.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/landscape.rs
  - /Users/feb/dev/cartridge/.cartridge/settings.md
---

# The root landscape searches every child cartridge's development record

The root board coordinates the whole system, while every base/plugin cartridge owns its own .cartridge memos and local PRDs. A root query must recursively find those records without copying them or starting their providers.

## Ownership and scope

Owner: `landscape`. Participating repositories: `landscape.ctg`, `memo.ctg`, `cartridge.ctg`, `root`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Define a recursive source-tree census from declared root members/cartridge directories, distinct from the active runtime composition. Give every nested cartridge a canonical hierarchical owner ID.
2. Discover child .cartridge records, PRDs, specs, and workflows as references; include loaded, installed-but-inactive, and source-only states explicitly. Preserve current private runtime capability/export rules.
3. Join root and descendant documents into landscape with parent/child ownership edges, canonical paths, byte revisions, and availability. Resolve references relative to the document owner.
4. Bound traversal by declared roots, visited canonical directories, depth, document count, and bytes. Report unavailable/deleted children and prevent parent backlinks or symlinks from forming infinite loops.
5. Invalidate just the affected descendant's derived rows after an edit/move/reload. All views and exact reads must resolve the same owner-qualified source.

## Acceptance contract

- A three-level fixture root/base/plugin contains same-named memos with different facts; one root search returns all three with distinct identities and correct readback.
- A child document edit is visible from a fresh root query without copying files or restarting unrelated providers.
- An inactive child contributes allowed source documentation but is not advertised as a callable live service; discovery launches no process.
- A parent backlink, repeated mount, out-of-root symlink, unreadable child, and deleted record produce bounded, explicit results.
- Root and child boards keep one authoritative PRD each; root progress/search references local state rather than mirroring it.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test landscape
just test memo
just test runtime landscape
just board-check
```

## Failure and recovery

A recursive scan loops, merges identical basenames, or exposes inactive/private services as executable. Test ownership, traversal bounds, and documentation-versus-capability state independently.

Rollback: Keep current loaded-profile discovery available while enabling recursive source discovery additively. Drop derived rows on recovery; never move or delete child records.

## Prior context

Related existing runtime memo leaf names: `the-landscape-owns-the-graph`, `the-agent-can-discover-its-own-program`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
