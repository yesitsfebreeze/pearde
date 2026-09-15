---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "20m"
---

# move cmd_unnamed and print_unnamed_promoted from commands_admin.rs into src/commands/src/commands_unnamed.rs; commands_admin.rs re-exports commands_unnamed; lib.rs declares the new sibling

Seventh child of [the-commands-admin-split](../the-commands-admin-split/prd.md). The unnamed-memory triage
subject is the operator's view of memories without a name: `cmd_unnamed`
(1047-1122) handles the two `UnnamedAction` arms (List prints every
unnamed memory other than the root, Promote embeds the seed and names
it), and `print_unnamed_promoted` (1124-1126) confirms the round-trip.
The Promote arm routes through the daemon before embedding for the
same reason `focus add` does.

## Do

- Create `src/commands/src/commands_unnamed.rs` carrying `cmd_unnamed`
  and `print_unnamed_promoted`. Module header names the unnamed-memory
  triage surface and the root-is-never-listed invariant.
- In `src/commands/src/commands_admin.rs`, remove the two items and add
  `pub(crate) use commands_unnamed::*;` for re-export.
- In `src/commands/src/lib.rs` add `pub(crate) mod commands_unnamed;`.
  Dispatch unchanged: `Commands::Unnamed { action } =>
  crate::commands_admin::cmd_unnamed(cfg, action).await`.

## Acceptance
`cargo test -p commands` is green,
`grep -n 'pub(crate) async fn cmd_unnamed\|fn print_unnamed_promoted' src/commands/src/commands_admin.rs`
answers nothing, and `wc -l src/commands/src/commands_unnamed.rs`
is roughly 80 lines.

`cmd_unnamed` and `print_unnamed_promoted` now live in
`src/commands/src/commands_unnamed.rs` (90 lines — the estimate counted
the moved lines and not the header and the `use` block);
`commands_admin.rs` is 1,200 lines and reaches them through
`pub(crate) use crate::commands_unnamed::*;`. `UnnamedAction` and
`with_graph` are re-exported from the sibling so the test module's
`super::*` still resolves, and the root-is-never-listed invariant moved
from a comment inside the `List` arm into the module header.
