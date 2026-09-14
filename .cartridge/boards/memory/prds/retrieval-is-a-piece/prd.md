---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
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
