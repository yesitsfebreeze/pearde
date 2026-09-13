---
kind: work
description: move cmd_claim_kind, claim_kind_at, print_claim_kind_added, print_claim_kind_removed from commands_admin.rs into src/commands/src/commands_claim_kind.rs; commands_admin.rs re-exports commands_claim_kind; lib.rs declares the new sibling
read_when: "executing the commands_admin split, or moving the claim-kind surface"
level: 10
status: done
estimate: 20m
---

# split-admin-claim-kind

Sixth child of [[@prd/work/memory--the-commands-admin-split.md]]. The claim-kind subject is
the registered-claim-type registry: `cmd_claim_kind` (956-1010)
dispatches the two `ClaimKindAction` arms (Add with optional parent,
Rm) to `claim_kind_at` (960-1010), and the two `print_*` helpers
confirm the round-trip. The shape mirrors [[@prd/work/memory--split-admin-focus.md]] and
lands in the same order the file's headers name.

## Do

- Create `src/commands/src/commands_claim_kind.rs` carrying
  `cmd_claim_kind`, `claim_kind_at`, `print_claim_kind_added`, and
  `print_claim_kind_removed`. Module header names the claim-kind
  registry and the parent-claim-kind DAG.
- In `src/commands/src/commands_admin.rs`, remove the four items and
  add `pub(crate) use commands_claim_kind::*;` for re-export.
- In `src/commands/src/lib.rs` add `pub(crate) mod
  commands_claim_kind;`. Dispatch unchanged: `Commands::ClaimKind {
  action } => crate::commands_admin::cmd_claim_kind(cfg, action).await`.

## Check

`cargo test -p commands` is green,
`grep -n 'pub(crate) async fn cmd_claim_kind\|async fn claim_kind_at\|fn
print_claim_kind_added\|fn print_claim_kind_removed' src/commands/src/commands_admin.rs`
answers nothing, and `wc -l src/commands/src/commands_claim_kind.rs`
is roughly 65 lines.

`cmd_claim_kind`, `claim_kind_at`, `print_claim_kind_added` and
`print_claim_kind_removed` now live in
`src/commands/src/commands_claim_kind.rs` (86 lines);
`commands_admin.rs` is 1,282 lines and reaches them through
`pub(crate) use crate::commands_claim_kind::*;`. `ClaimKindAction` is
re-exported from the sibling so the test module's `super::*` still
resolves.
