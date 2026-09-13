---
kind: work
description: src/commands/src/commands_admin.rs is 1515 lines holding 9 subjects (health, gc, compact, compress, focuses, claim kinds, unnamed-memory triage, hub control, store registration) — every other verb in the commands crate already has its own commands_*.rs; the split moves each subject into a sibling file and leaves commands_admin as a re-export shim so the 16+2+1 call sites in lib.rs / commands_serve.rs / commands_launch.rs / commands_query.rs / commands_mcp.rs do not move
read_when: "splitting commands_admin.rs, or asking what the next legibility target in the commands crate is"
level: 9
status: done
estimate: 4h
---

# the-commands-admin-split

## Do

Carry [[a-reader-pays-per-unit-not-per-line]] into
`src/commands/src/commands_admin.rs`. The file's own `//!` header names
nine subjects; the file holds all of them; every other verb in the crate
already lives in a single-subject sibling. The helpers
(`print_focus_added`, `print_claim_kind_added`, `memory_cap_health_lines`,
`degradation_lines`, …) exist only because each subject is forced to
share one module, and the helpers die with the split.

`subwork:` [[@prd/work/memory--split-admin-health.md]], [[@prd/work/memory--split-admin-gc.md]],
[[@prd/work/memory--split-admin-compact.md]], [[@prd/work/memory--split-admin-compress.md]],
[[@prd/work/memory--split-admin-focus.md]], [[@prd/work/memory--split-admin-claim-kind.md]],
[[@prd/work/memory--split-admin-unnamed.md]], [[@prd/work/memory--split-admin-hub-register.md]],
[[@prd/work/memory--the-admin-split-left-rotted-citations.md]]

Each child moves one subject's `cmd_*` entry point(s) and its private
helpers into `src/commands/src/commands_<subject>.rs`, declares the new
sibling in `src/commands/src/lib.rs` next to the existing ones, and
removes the moved items from `commands_admin.rs` behind a
`pub(crate) use commands_<subject>::*;` re-export so the existing
callers in `lib.rs` / `commands_serve.rs` / `commands_launch.rs` /
`commands_query.rs` / `commands_mcp.rs` and the test file at
`src/commands/src/tests/commands_admin_test.rs` (which uses `super::*`
and `super::cmd_*`) keep resolving through the old path. The child is
`done` when `just check` is green, the test file's `super::cmd_hub_merge`,
`super::cmd_rekey`, `super::degradation_lines`, and the rest still
resolve, and the moved functions are gone from `commands_admin.rs`.

Order matters: the children that introduce no new helpers come first, so
the test file never carries a `super::` that lands in an empty module.
The health subject is largest and moves last — its `daemon_health`,
`*_health_lines`, `cmd_status`, and `probe` reach every other surface.

Not part of this: `src/commands/src/commands_compact.rs` (587 lines,
one subject, the `compact` subcommand that folds the intake — not the
admin-side `consolidate`/`migrate` this memo splits), the test file
itself (moves with the children that own its `super::` references),
or the `cmd_unnamed` `Promote` arm's embed call (stays with the
unnamed subject).

Every child runs in a lane ([[lanes-not-a-shared-tree]]); the parent
itself is not edited in a lane because the children own the diff.

## Check

`wc -l src/commands/src/commands_admin.rs` answers at most 80 lines
(the `//!` header, the `use` block, the `pub(crate) use
commands_<subject>::*;` re-exports, and the `#[cfg(test)]` line that
carries the test file), the eight files this split creates all
exist — `commands_health.rs`, `commands_gc.rs`, `commands_admin_compact.rs`,
`commands_compress.rs`, `commands_focus.rs`, `commands_claim_kind.rs`,
`commands_unnamed.rs`, `commands_hub.rs` (a ninth, `commands_app.rs`, left
with health) — `cargo test --test cited_paths` is green, and `grep -c '^pub(crate) (async )?fn
cmd_' src/commands/src/commands_admin.rs` answers `0`. Two clauses were wrong as written and are corrected above, measured
2026-09-08 by [[@prd/work/memory--split-admin-health.md]]: the `find` counted every
`commands_*.rs` in the crate and answered 26, seventeen of which predate this
split; and `cited_paths` lives in the `memory` package, so `-p commands` names
no such target. The probe that
flagged the file before — a 1515-line file with 9 subjects in one
`//!` — answers "no" after.

**Done 2026-09-08.** Nine children landed in one day and `commands_admin.rs`
is 20 lines — the `//!` header, nine `pub(crate) use commands_<subject>::*;`
re-exports and the `#[cfg(test)]` line — from 1,515 holding nine subjects.
Check read after the ninth child and it passes in full: 20 lines, `0` `cmd_*`
definitions, every named sibling present, `cargo test --test cited_paths`
green, every child `status: done`.

Two things the chain established that were not in this memo's plan. The
carry-back trap bit four times: an item that `commands_admin_test.rs` calls
unqualified through `use super::*` breaks the moment it moves, whether it is a
helper (`with_graph`, `human_bytes`, the twelve `*_health_lines`), a private
function (`rekey_stops_at_the_plan`, `cmd_hub_merge`) or an import whose last
caller left (`load_graph`) — each is answered by `pub(crate)` plus the glob, or
by carrying the type back with `pub(crate) use`. And every child's line
estimate was low, because each counted moved lines and not the header and
`use` block.

