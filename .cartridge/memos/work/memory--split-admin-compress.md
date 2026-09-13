---
kind: work
description: move cmd_compress from commands_admin.rs into src/commands/src/commands_compress.rs; commands_admin.rs re-exports commands_compress; lib.rs declares the new sibling
read_when: "executing the commands_admin split, or moving the compress surface"
level: 10
status: done
estimate: 10m
---

# split-admin-compress

Fourth child of [[@prd/work/memory--the-commands-admin-split.md]]. The compress subject is one
function (`cmd_compress`, lines 20-48) over a `math::quant::QuantizationMode`
and a directory path. It is offline and synchronous, the only operator
command that takes a path that is not the project's `data_dir`.

## Do

- Create `src/commands/src/commands_compress.rs` carrying `cmd_compress`.
  Module header names the compress surface and notes the offline
  constraint.
- In `src/commands/src/commands_admin.rs`, remove the function and add
  `pub(crate) use commands_compress::*;` for re-export.
- In `src/commands/src/lib.rs` add `pub(crate) mod commands_compress;`.
  Dispatch unchanged: the `Commands::Compress { … } =>` arm still says
  `crate::commands_admin::cmd_compress(&src, &mode, out.as_deref())`.

## Check

`cargo test -p commands` is green,
`grep -n 'pub(crate) fn cmd_compress' src/commands/src/commands_admin.rs`
answers nothing, and `wc -l src/commands/src/commands_compress.rs`
is roughly 35 lines.

**Done 2026-09-08.** `cmd_compress` and its `//!` subject line live in
`src/commands/src/commands_compress.rs` (36 lines); `commands_admin.rs` keeps
`pub(crate) use crate::commands_compress::*;` so `lib.rs:1113`'s
`commands_admin::cmd_compress` still resolves, and `lib.rs` declares the sibling
in alphabetical place. Two agents stalled mid-edit and the coordinator finished
it: the re-export named a module `lib.rs` never declared, so the crate did not
compile (E0432) — one line closed it.

Check run literally: `grep -n 'pub(crate) fn cmd_compress' commands_admin.rs`
answers nothing, `wc -l commands_compress.rs` is 36, `cargo check -p commands`
is clean. `cargo test -p commands` is 126 of 127 — the one failure is
`commands_exit::tests::a_reported_failure_is_what_the_exit_status_reads`, which
passes alone and failed 1, 2 and 1 times across three identical runs of this
same unchanged worktree. That race is not this split's and has its own memo,
[[@prd/work/memory--the-exit-flag-tests-race-each-other.md]].

