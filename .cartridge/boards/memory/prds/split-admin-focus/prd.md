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

# move cmd_focus, focus_at, print_focus_added, print_focus_removed from commands_admin.rs into src/commands/src/commands_focus.rs; commands_admin.rs re-exports commands_focus; lib.rs declares the new sibling

Fifth child of [the-commands-admin-split](../the-commands-admin-split/prd.md). The focus subject owns the
named-attractor CRUD: `cmd_focus` (865-947) dispatches the three
`FocusAction` arms (Add, List, Remove) to `focus_at` (872-947), which
embeds the seed text mean-pooled across lines, names the focus by
non-empty string, and stores mass.

## Do

- Create `src/commands/src/commands_focus.rs` carrying `cmd_focus`,
  `focus_at`, `print_focus_added`, and `print_focus_removed`. Module
  header names the focus-attractor surface and the embed-mean-pool
  convention.
- In `src/commands/src/commands_admin.rs`, remove the four items and
  add `pub(crate) use commands_focus::*;` for re-export.
- In `src/commands/src/lib.rs` add `pub(crate) mod commands_focus;`.
  Dispatch unchanged: `Commands::Focus { action } =>
  crate::commands_admin::cmd_focus(cfg, action).await`.

## Acceptance
`cargo test -p commands` is green,
`grep -n 'pub(crate) async fn cmd_focus\|async fn focus_at\|fn
print_focus_added\|fn print_focus_removed' src/commands/src/commands_admin.rs`
answers nothing, and `wc -l src/commands/src/commands_focus.rs`
is roughly 95 lines.

`cmd_focus`, `focus_at`, `print_focus_added` and `print_focus_removed`
now live in `src/commands/src/commands_focus.rs` (106 lines);
`commands_admin.rs` is 1,352 lines and reaches them through
`pub(crate) use crate::commands_focus::*;`. `focus_rows` and
`FocusAction` are re-exported from the sibling so the test module's
`super::*` still resolves.
