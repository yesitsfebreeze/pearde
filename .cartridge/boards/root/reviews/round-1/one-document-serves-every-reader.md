---
state: open
origin: requested
priority: 94
blast-radius: high
workflow: develop-one-cartridge
footprint:
  - /Users/feb/dev/cartridge/memo.ctg/src/record.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/usage.rs
  - /Users/feb/dev/cartridge/memo.ctg/src/service.rs
  - /Users/feb/dev/cartridge/memo.ctg/seeds/type
  - /Users/feb/dev/cartridge/memo.ctg/tests
  - /Users/feb/dev/cartridge/landscape.ctg/src/surface.rs
---

# One Markdown document supplies discovery, commands, and readable guidance

Capability descriptions currently live in Rust, JSON manifests, and prose. The same source document must provide the indexed metadata, executable recipe, agent documentation, and human view.

## Ownership and scope

Owner: `memo`. Participating repositories: `memo.ctg`, `landscape.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Define the project dialect in the contracts note: canonical owner/path identity, byte revision, kind, description, default recipe, invocation mode, and explicit execution base. Preserve current routine memos; accept .jd as a format alias only when it does not create duplicate identities.
2. Build one parser for frontmatter and fenced just blocks. Support multiple recipes with one declared default; reject malformed/duplicate executable definitions. Never extract prose or psaido blocks.
3. Return commands/docs/human projections from the same parsed revision. Index only tool-document frontmatter; do not silently change legacy memo resolve's body scoring.
4. Implement exact linked-document resolution with cycle/depth/byte limits, owner boundaries, and named-section checks. References in executable blocks remain literal and are not hydrated.

## Acceptance contract

- Changing one fixture's description, prose, and recipe updates the corresponding projections with one new revision and no synchronization operation.
- Discovery reads only frontmatter for tool matching; a word occurring only in the recipe/body cannot make that tool a metadata match.
- Malformed fences, missing default recipes, duplicate names, ambiguous links, and missing sections return source-located errors.
- A read of any projection starts no process, subscribes to no event, and writes no observation implicitly.
- Existing memo read/resolve and revision-conflict tests continue to pass.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test memo
just test landscape
just check memo
just check landscape
```

## Failure and recovery

A code sample becomes executable, or one filename resolves to two owners. Bind every result to its canonical owner/path/revision.

Rollback: Introduce document support additively; retain existing native tool descriptors until migrated. Existing authored memos keep their syntax and behavior.

## Prior context

Related existing runtime memo leaf names: `the-tool-contract-is-a-memo`, `a-tool-is-declared-by-its-memo`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
