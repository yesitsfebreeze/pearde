---
kind: work
level: 10
status: open
claim: session-adcf486f 2026-09-09 02:52
estimate: 1d
description: retrieval becomes a hot piece — its boundary types (`QueryOptions`, `ScoredEntity`, `seed::Mode`, `Weights`, `SortField`) move to `base`, its twelve generic entry points get monomorphic `#[no_mangle]` twins, and `just piece retrieval` swaps the ranking under a running daemon
read_when: "making retrieval hot, or asking where its boundary types went"
---

# retrieval-is-a-piece

Second child of [[@prd/work/memory--every-compute-crate-is-a-piece.md]], the shape of
[[@prd/work/memory--hygiene-is-the-first-piece.md]].

## Do

Move the five types callers name (`retrieval::score::QueryOptions` 13
uses, `expand::ScoredEntity` 8, `seed::Mode` 5, `seed::Weights`,
`score::SortField`) to `base`, since a piece's types cannot change layout
under a running daemon and `base` is never a piece. Give the twelve generic
functions monomorphic `#[no_mangle]` entry points over the concrete types
the daemon calls with; the generic bodies stay in the piece behind them.
`retrieval::LlmFunc` — a boxed closure — stays host-side. Add `retrieval`
to `pieces` in `justfile`.

## Check

`just dev` in a lane; a `memory query` ranks; a scoring constant in
`retrieval-piece` is changed and `just piece-build retrieval` runs; the same
query re-ranks under the same daemon pid. `just check` and `just test` green.
