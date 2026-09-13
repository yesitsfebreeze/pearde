---
kind: work
level: 10
status: done
description: a double-bracket record citation in a doc comment is a broken intra-doc link to rustdoc — decide the convention, then make `cargo doc` clean and give it a runner
read_when: "citing a part from code, or adding a lint runner"
---

# the-record-citation-breaks-rustdoc

## Do

Citing a record part from code is idiomatic here — the `operations` citation
in `commands_mcp.rs`, `persistence` in `graph/diskann.rs`, each written with
doubled brackets. Rustdoc parses the doubled brackets as an intra-doc link to
`persistence` and fails to resolve it, so `cargo doc` cannot be clean while the
convention stands as written.

Nothing noticed because nothing runs rustdoc's lints: `just test` runs
`cargo test --doc`, which executes doctests and never checks a link. Eight
unrelated broken links sat in `util` and the root crate until
`RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --keep-going` was
run for the first time (`24b60151`).

Decide the convention first, because it is a convention and not a bug:

- **Escape it** — backslash the brackets, or wrap the whole citation in
  backticks — keeps the record's syntax and stops rustdoc reading it as a link.
- **Drop the brackets in code** — "the `operations` part" — reads better in
  rendered docs and loses the grep-ability that makes a doubled-bracket name findable from
  either side.
- **Keep it and silence the lint** — `#![allow(rustdoc::broken_intra_doc_links)]`
  per crate, which turns the lint off for the real breakages too and is the
  option that costs the most later.

Then make the workspace clean under that flag and add the run to `just check`,
so the family that produced these eight has a runner
(`a-gate-that-walks-cannot-fail-short` — the lint existed, its subject list
was empty).

Settled by [[a-code-citation-is-backticked]] on 2026-09-06: backticks, all 22
citations in `src/**/*.rs` wrapped, the two real broken links behind them
repaired, and the rustdoc run added to `just check` in the `justfile`.

## Check

`RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --keep-going` is
clean, `just check` runs it, and `rg -n '\[\[[a-z-]+\]\]' src --glob '*.rs'`
agrees with whichever convention was chosen.
