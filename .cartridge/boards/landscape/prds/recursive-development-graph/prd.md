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
canonical-scope: recursive-development-graph
needs:
- '@landscape/recursive-development-graph/recursive-source-census'
- '@landscape/recursive-development-graph/recursive-root-search'
- '@landscape/recursive-development-graph/recursive-source-refresh'
---

# Root search reads every child cartridge's development record

Coordinate the linked outcomes; claim and implement a leaf. The census and search now live in memo (`memo.ctg/src/sources/census.rs`, `memo.ctg/src/sources/search.rs`, transport in `memo.ctg/src/source_search.rs`); board records are reached only through the prd-provided `source.board` key injected into memo, per root decision `a-cartridge-brings-its-own-surface.md`. The census leaf is done; root search is specced; refresh is open.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] A three-level fixture composed at pinned memo and prd revisions returns distinct descendant facts, reads each back from its own owner, and reflects a child edit on the next query.
- [ ] With `source.board` absent from the profile, board roots report `unavailable` while cartridge roots still answer.

## Work items

- [Declared descendants have distinct source identities](recursive-source-census/prd.md)
- [Root search reads every permitted descendant record](recursive-root-search/prd.md)
- [A descendant edit refreshes only its derived rows](recursive-source-refresh/prd.md)

## Integration gate

From /Users/feb/dev/cartridge: `just test memo`, `just test prd`, `bun test memo.ctg/.cartridge/tests/integration/source-search.test.ts`; not run for this plan.

## Review

[Review history](review.md); rounds inherited, maximum five. Target board after rehoming: memo.
