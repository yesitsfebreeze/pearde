---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: retrieval-is-a-piece
---

# An incompatible retrieval piece is refused before it is used

The retrieval hot swap works today. `hot_lib_reloader` loads `.memory/pieces/libretrieval_piece.dylib` (`src/retrieval/src/lib.rs`), and `.cartridge/tests/integration/retrieval-reload.test.ts` (`just test-reload`) proves that a rebuilt piece changes scores under the same PID and that the original returns on restore. What is missing is a check that a candidate dylib matches the host's boundary types (`base`) and the twelve `#[no_mangle]` entry points in `src/retrieval/piece/src/lib.rs` before the swap. Outcome, owned by memory: a compatibility stamp exported by the piece (ABI version plus a layout hash of the boundary types), checked at install by `piece-build` in `.cartridge/development/memos/routine/develop-memory.md` and again before the seam uses a newly loaded library.

## Acceptance

- [ ] A candidate built with an unchanged boundary installs, and the reload test still passes under the same PID.
- [ ] A candidate with a changed boundary type or a missing entry point is refused by `piece-build`. If copied into `.memory/pieces` directly, it is refused before first use, and the previous implementation keeps answering queries.
- [ ] The refusal is logged and visible in `health`. The static (non-`hot`) build is unaffected, and nothing is rewritten from generic to monomorphic only because a historical memo asked for it.

## Proof and recovery

First probe: find whether `hot_lib_reloader` can veto a load through its reload hooks. If it cannot, rely on the install-time check plus a stamp comparison that refuses to call the new symbols. Extend `retrieval-reload.test.ts` with an incompatible candidate. Gates, run from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test`, `MEMORY_RELOAD_TEST=1 just test-reload` (none has run yet). Rollback: remove the stamp check; the reload path is unchanged.

## Dependencies and review

No hard needs. Memory decision `crates-are-hot-pieces` applies. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--retrieval-is-a-piece.md` (status open, claim session-adcf486f 2026-09-09 02:52, estimate 1d). The PRD state above is authoritative.

> retrieval becomes a hot piece — its boundary types (`QueryOptions`, `ScoredEntity`, `seed::Mode`, `Weights`, `SortField`) move to `base`, its twelve generic entry points get monomorphic `#[no_mangle]` twins, and `just piece retrieval` swaps the ranking under a running daemon

Second child of [every-compute-crate-is-a-piece](../every-compute-crate-is-a-piece/prd.md), the shape of
[hygiene-is-the-first-piece](../hygiene-is-the-first-piece/prd.md).

### Do

Move the five types callers name (`retrieval::score::QueryOptions` 13
uses, `expand::ScoredEntity` 8, `seed::Mode` 5, `seed::Weights`,
`score::SortField`) to `base`, since a piece's types cannot change layout
under a running daemon and `base` is never a piece. Give the twelve generic
functions monomorphic `#[no_mangle]` entry points over the concrete types
the daemon calls with; the generic bodies stay in the piece behind them.
`retrieval::LlmFunc` — a boxed closure — stays host-side. Add `retrieval`
to `pieces` in `justfile`.

### Check

`just dev` in a lane; a `memory query` ranks; a scoring constant in
`retrieval-piece` is changed and `just piece-build retrieval` runs; the same
query re-ranks under the same daemon pid. `just check` and `just test` green.
