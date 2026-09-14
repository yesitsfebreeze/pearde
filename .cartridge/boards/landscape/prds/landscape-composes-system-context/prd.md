---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: landscape-composes-system-context
needs:
- '@landscape/landscape-composes-system-context/context-contributor-contract'
- '@landscape/landscape-composes-system-context/memory-context-contributor'
- '@landscape/landscape-composes-system-context/live-file-context-contributors'
- '@memo/landscape-context-facade'
---

# One context query answers across kernel, documents, memory, files and live state

Coordinate the linked outcomes; claim and implement a leaf. The composition point is memo's `context` op (`memo.ctg/src/context.rs`): it serves `documents` and `kernel` itself and asks each injected `context.<kind>` provider for the rest, per root decision `a-cartridge-brings-its-own-surface.md` (memory ships `context.memory` in `memory.ctg/src/source.rs`, fs ships `context.file`). Contract, memory contributor and memo facade are done; only live-state and file contributors remain.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] One `context` prepare at a pinned revision set returns attributed rows from documents, kernel, memory, file and at least one live owner, each read back exactly.
- [ ] Removing any one provider from the profile changes only its own status (`absent`) and leaves other rows and memo source unchanged.

## Work items

- [Contributors return bounded attributable context rows](context-contributor-contract/prd.md)
- [Memory hits resolve to exact source evidence](memory-context-contributor/prd.md)
- [File and live context retain owner and freshness](live-file-context-contributors/prd.md)
- [Native context facade](../../../memo/prds/landscape-context-facade/prd.md)

## Integration gate

From /Users/feb/dev/cartridge: `just test memo`, `just test memory`, `bun test memo.ctg/.cartridge/tests/integration/context.test.ts`; not run for this plan.

## Review

[Review history](review.md); rounds inherited, maximum five. Target board after rehoming: memo.
