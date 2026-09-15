---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "2h"
actual: "1h"
---

# `answer` reports an empty LSP result as `nothing found` whenever `vim.lsp.status()` is quiet, which it is long before the index fills — it must ask a pinned control query first and report `indexing:` when the control comes back empty too

**Done 2026-09-08** — `answer` in [[neovim-control]] now runs one
`workspace/symbol` query for `CONTROL`, pinned to `ChunkPartKind`, before it
reports an empty result, and `tests/terminal.py` pins `CONTROL` to a definition
this tree carries. `vim.lsp.status()` is no longer a condition anywhere; what is
left of it is trailing text on the `indexing:` line.

Measured on a headless Neovim on a private socket with one rust-analyzer of its
own, against this lane's cold worktree (no `target/`), sampled every 50 ms from
the moment the client attached. **At 0.96 s `vim.lsp.status()` was `''` while a
`workspace/symbol` query for `ChunkPartKind` — a symbol this tree defines at
`src/base/src/base_types.rs:16` — still returned zero hits: the old gate's
`nothing found`, and the new gate returned `indexing: control ChunkPartKind
answers nothing;`.** The index came up at 4.9 s, and from there the same call
answered in 1–2 ms with the real location while `vim.lsp.status()` stayed `''`.
A non-empty answer never reaches the control: at 0.0 s `document_symbols`
returned its 17 symbols unchanged while the same server's `index_status` read
`indexing:`. Renaming `ChunkPartKind` at its definition turned
`tests/terminal.py` red and the inverse edit turned it green again.

[[what-makes-an-empty-lsp-answer-trustworthy]] settled how an empty answer earns
belief, and [[an-empty-lsp-answer-is-not-a-no]] measured what happens without
it: 68 minutes of `attached, answering nothing` and an empty
`document_symbols` in 0.0 s for a 17 KB file full of functions. The gate that
should have said `indexing:` keys on `vim.lsp.status()`, which goes quiet when
the cargo build ends and not when the symbol index fills.

## Do

In `answer` (`memos/system/neovim-control.md`, the `answer` helper the generated
Lua cache carries), before returning an empty result as an answer: run one
control query whose result cannot be empty in this tree, and pin the symbol it
asks for in the gate itself so a rename fails loudly rather than silently
disarming the check. Non-empty control, report the empty answer. Empty control,
report `indexing:`. Leave the existing `unavailable:` timeout path alone — this
is about a server that answers quickly and wrongly, not one that does not
answer.

Do not keep the `vim.lsp.status()` condition as a second gate: it is what made
the false negative, and two gates where one is known-broken is worse than one.

## Acceptance
With a rust-analyzer that has attached but not finished indexing, `answer` for
a symbol that exists reports `indexing:` rather than an empty result — proved
the way [the-warm-lsp-times-out](../the-warm-lsp-times-out/prd.md) proved its measurement, a headless Neovim on
a private socket against a cold tree. With a warm server, the same call answers
normally and the control costs one extra round trip only on the empty path.
Renaming the pinned symbol turns the gate red.
