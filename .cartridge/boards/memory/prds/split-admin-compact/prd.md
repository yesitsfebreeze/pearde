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
actual: "20m"
---

# move cmd_consolidate and cmd_migrate from commands_admin.rs into src/commands/src/commands_admin_compact.rs; commands_admin.rs re-exports it; lib.rs declares the new sibling; named with the `admin_` prefix so it does not collide with the existing `commands_compact.rs` (the intake-folding subcommand)

Third child of [the-commands-admin-split](../the-commands-admin-split/prd.md). The "compact" subject here
is admin-side: `cmd_consolidate` (723-740) ratifies near-duplicates and
`cmd_migrate` (785-840) is the format-version hop. The crate already
has `src/commands/src/commands_compact.rs` (the `compact` subcommand
that folds the intake), so the new file is `commands_admin_compact.rs`
to keep both names searchable.

## Do

- Create `src/commands/src/commands_admin_compact.rs` carrying
  `cmd_consolidate` and `cmd_migrate`. Module header names the
  admin-side compaction (consolidate) and the format-version migration
  (migrate) and the order they are documented to run in.
- In `src/commands/src/commands_admin.rs`, remove the two functions and
  add `pub(crate) use commands_admin_compact::*;` for re-export.
- In `src/commands/src/lib.rs` add
  `pub(crate) mod commands_admin_compact;`. The dispatch is unchanged:
  `Commands::Consolidate => crate::commands_admin::cmd_consolidate(cfg)`
  and `Commands::Migrate => crate::commands_admin::cmd_migrate(cfg)`.

## Acceptance
`cargo test -p commands` is green,
`grep -n 'pub(crate) fn cmd_consolidate\|pub(crate) fn cmd_migrate' src/commands/src/commands_admin.rs`
answers nothing, and `wc -l src/commands/src/commands_admin_compact.rs`
is roughly 120 lines.

Done: `src/commands/src/commands_admin_compact.rs` carries both functions in
94 lines, `commands_admin.rs` re-exports it and is 1446 lines, `lib.rs`
declares `pub(crate) mod commands_admin_compact;`. `cargo test -p commands`
fails only `commands_exit::tests::a_reported_failure_is_what_the_exit_status_reads`,
which passes alone — the known process-global exit flag.
