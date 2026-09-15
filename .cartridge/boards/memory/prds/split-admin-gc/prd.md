---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "15m"
---

# move cmd_gc from commands_admin.rs into src/commands/src/commands_gc.rs; commands_admin.rs re-exports commands_gc; lib.rs declares the new sibling; the `human_bytes` helper moves with it because only cmd_gc and cmd_hub's status output call it

Second child of [the-commands-admin-split](../the-commands-admin-split/prd.md). The smallest subject:
`cmd_gc` (lines 742-777) is the reap-then-compact loop and the only
caller of `human_bytes` in the file. `human_bytes` (842-855) also feeds
`cmd_hub`'s "known memories" status list, so it moves to the shared
crate or duplicates — see [split-admin-hub-register](../split-admin-hub-register/prd.md) for the
duplication path that is deliberately not taken.

## Do

- Create `src/commands/src/commands_gc.rs` carrying `cmd_gc` and the
  private `human_bytes` helper. Module header names the gc surface and
  the reap-then-compact ordering.
- In `src/commands/src/commands_admin.rs`, remove `cmd_gc` and
  `human_bytes` and add `pub(crate) use commands_gc::*;` so the test
  file's `super::*` keeps resolving. If [split-admin-hub-register](../split-admin-hub-register/prd.md)
  lands first, `human_bytes` is re-exported from the hub file under a
  shared name; this child leaves it to the gc module regardless and the
  hub child imports it as `use crate::commands_gc::human_bytes;` when
  it lands.
- In `src/commands/src/lib.rs` add `pub(crate) mod commands_gc;`. No
  call site moves: `Commands::Gc => crate::commands_admin::cmd_gc(cfg)`
  resolves through the re-export.

## Acceptance
`cargo test -p commands` is green, `wc -l src/commands/src/commands_gc.rs`
is roughly 45 lines, and
`grep -n 'pub(crate) fn cmd_gc\|fn human_bytes' src/commands/src/commands_admin.rs`
answers nothing.

Done: `cmd_gc` and `human_bytes` live in
`src/commands/src/commands_gc.rs` (59 lines); `commands_admin.rs` carries
`pub(crate) use crate::commands_gc::*;` and `lib.rs` declares
`pub(crate) mod commands_gc;`. `human_bytes` is `pub(crate)` so
`cmd_hub`'s status list keeps reaching it through the re-export.
