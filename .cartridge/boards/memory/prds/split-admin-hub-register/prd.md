---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1h"
---

# move cmd_register, cmd_rekey, rekey_stops_at_the_plan, cmd_stop, cmd_clean, cmd_hub, cmd_hub_merge, cmd_pulse, default_root, spawn_detached, connect_hub_or_start, register_with_hub, HUB_IDLE_EXIT_SECS, REKEY_UNRECOGNIZED_SHOWN from commands_admin.rs into src/commands/src/commands_hub.rs (the hub control + store registration subject — these two are the eighth and ninth subjects in the file's own header and are inseparable: cmd_register writes through cmd_hub's lock probe, cmd_hub_merge loads both stores, cmd_clean and cmd_stop both reach the hub registry); commands_admin.rs re-exports commands_hub; lib.rs declares the new sibling

Eighth child of [the-commands-admin-split](../the-commands-admin-split/prd.md). The file's own `//!`
header names "hub control, and store registration" as a single phrase,
so they land together: `cmd_register` (1012-1045) imports a store into
the project's, `cmd_rekey` (564-644) and `rekey_stops_at_the_plan`
(531-562) re-key every id by its origin, `cmd_stop` (650-659) and
`cmd_clean` (666-721) stop and remove the daemon's footprint, `cmd_hub`
(1242-1328) and `cmd_hub_merge` (1333-1413) run the machine hub, and
`cmd_pulse` (141-157) enqueues the clustering pass. The detached-spawn
helpers (`spawn_detached` 1138-1171, `connect_hub_or_start` 1175-1206,
`register_with_hub` 1212-1240, `default_root` 1128-1131) and the
constants `HUB_IDLE_EXIT_SECS` (1135) and `REKEY_UNRECOGNIZED_SHOWN` (8)
feed every one of these. The existing `// ==== hub link ====` banner
(1133) is the file's own acknowledgement that they share a subject;
that banner moves with them.

## Do

- Create `src/commands/src/commands_hub.rs` carrying every item in
  the file's "hub control, and store registration" subject: the
  eight `cmd_*` entry points, the seven private helpers, and the two
  constants. Module header names the hub control + store registration
  surface, the `HUB_IDLE_EXIT_SECS` rationale, and the
  `REKEY_UNRECOGNIZED_SHOWN` report cap.
- In `src/commands/src/commands_admin.rs`, remove the moved items
  (the existing `// ==== hub link ====` banner, the seven functions
  and the two `cmd_*` entry points above it, and the `use
  transport::memory_rpc::MemoryRpcClient;` line 1415 that is now unused)
  and add `pub(crate) use commands_hub::*;` so the test file's
  `super::cmd_hub_merge`, `super::cmd_rekey`, and the rest keep
  resolving. The `cmd_status` and `probe` at lines 1417-1511 stay
  in `commands_admin.rs` — they belong to the health subject, which
  moves in [split-admin-health](../split-admin-health/prd.md).
- In `src/commands/src/lib.rs` add `pub(crate) mod commands_hub;`.
  Dispatch unchanged: every arm that said
  `crate::commands_admin::cmd_register` /
  `cmd_rekey` / `cmd_stop` / `cmd_clean` / `cmd_hub` / `cmd_pulse`
  resolves through the re-export, and the external
  `crate::commands_admin::spawn_detached` callers in
  `commands_launch.rs:42,122`, the `connect_hub_or_start` callers
  in `commands_query.rs:160` and `commands_mcp.rs:113`, and the
  `register_with_hub` caller in `commands_serve.rs:387` all resolve
  the same way.
- If [split-admin-gc](../split-admin-gc/prd.md) has already landed, this child imports
  `use crate::commands_gc::human_bytes;` for the `cmd_hub` "known
  memories" status list. If not, `human_bytes` stays in
  `commands_admin.rs` temporarily; whichever child lands second
  imports it from the first.

## Acceptance
`cargo test -p commands` is green, `cargo test -p commands hub_merge_tests`
is green, `cargo test -p commands rekey_tests` is green, and
`grep -n 'pub(crate) (async )?fn cmd_\|REKEY_UNRECOGNIZED_SHOWN\|HUB_IDLE_EXIT_SECS' src/commands/src/commands_admin.rs`
answers nothing (every `cmd_*` entry point is gone, both constants
are gone). `wc -l src/commands/src/commands_hub.rs` is roughly 400
lines.

The whole "hub control, and store registration" subject now lives in
`src/commands/src/commands_hub.rs` (570 lines — the estimate counted the
moved lines and not the header and the `use` block): `cmd_pulse`,
`cmd_rekey` with `rekey_stops_at_the_plan`, `cmd_stop`, `cmd_clean`,
`cmd_register`, `default_root`, the `// ==== hub link ====` section
whole, `cmd_hub` and `cmd_hub_merge`, and both constants.
`commands_admin.rs` is 645 lines and reaches them through
`pub(crate) use crate::commands_hub::*;`. `rekey_stops_at_the_plan` and
`cmd_hub_merge` were private and are now `pub(crate)` so the glob
carries them to the test module's `super::`; `human_bytes` is imported
from `commands_gc` for the "known memories" list, as [split-admin-gc](../split-admin-gc/prd.md)
left it. Admin's own `use` block shrank to `Endpoint` and `load_graph`,
and the orphaned reap-then-compact comment that `gc` left behind went
with the strip.

Two corrections to the Check above, recorded rather than faked. The
`use transport::memory_rpc::MemoryRpcClient;` line the `Do` calls unused is
`probe`'s, and `probe` stays with the health subject — it is still
there. And the grep does not answer nothing: `cmd_health`, `cmd_status`
and `cmd_app` remain, exactly as the `Do` says they should. It answers
nothing for `REKEY_UNRECOGNIZED_SHOWN`, `HUB_IDLE_EXIT_SECS`, and every
`cmd_*` this memo moved; the three that stay leave with
[split-admin-health](../split-admin-health/prd.md).
