---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
actual: "3h"
---

# hygiene becomes the first hot piece — `hygiene-piece` the dylib, `hygiene` the seam, `just dev` and `just piece hygiene` the loop — and a new rule reaches the running daemon in about two seconds

First child of [every-compute-crate-is-a-piece](../every-compute-crate-is-a-piece/prd.md). Done 2026-09-07 in the
lane of the same name: `src/hygiene/piece/` is `hygiene-piece`
(rlib + dylib, seven `#[no_mangle]` entry points), `src/hygiene/src/lib.rs`
is the seam with `compile_patterns` kept host-side, `Vec<&'static str>`
labels became `Vec<String>` in the piece and in `graph::AuditCandidate`,
and `justfile` gained `pieces`, `dev`, `piece`, `piece-build` beside a
`piece` bacon job. The Check ran against the lane's own store: a daemon
built with `hygiene/hot` rejected `probe-5678` under a pattern that did not
exist when it started, 2.1 s after the edit, pid unchanged.

## Do

Cut `hygiene` along [[crates-are-hot-pieces]]: move the code to a
`hygiene-piece` crate built as rlib and dylib, keep `hygiene` as the seam
that is static by default and a `hot-lib-reloader` module under a `hot`
feature, own every returned label, build user regexes in the seam. Add the
dev-mode recipes and prove the swap under a running daemon.

## Acceptance
In a lane with `[hygiene] gate = "strict"`, `just dev` serves; an ingest
carrying a fresh pattern's text commits; the pattern is added to
`hygiene-piece`, `just piece-build hygiene` runs; the same text is now
rejected by the same daemon pid, and `just check` and `just test` are green.
