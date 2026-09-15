---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "30m"
---

# move cmd_health, cmd_status, daemon_health, probe, and the eleven `*_health_lines` helpers from commands_admin.rs into src/commands/src/commands_health.rs; commands_admin.rs re-exports commands_health; lib.rs declares the new sibling

First child of [the-commands-admin-split](../the-commands-admin-split/prd.md). The health subject owns the
largest block — `cmd_health` (lines 50-136) prints every gauge, the
eleven `*_health_lines` helpers (178-512) build each block, and the
status half (`cmd_status` 1417-1497, `probe` 1503-1511, `daemon_health`
161-170) is the operator's "what does this machine look like right now".
Helpers exist only because the subject shared a module; once moved they
live with the only caller.

## Do

- Create `src/commands/src/commands_health.rs` carrying: `cmd_health`,
  `cmd_status`, `daemon_health`, `probe`, and the eleven
  `degradation_lines`, `tick_health_lines`, `ingest_health_lines`,
  `convergence_health_lines`, `heat_health_lines`, `retrieval_health_lines`,
  `source_trust_health_lines`, `dedup_health_lines`, `memory_cap_health_lines`,
  `llm_health_lines`, `reflex_health_lines` helpers. The `// ==== hub
  link ====` banner at line 1133 stays where it is; the new file gets
  its own `//!` header naming the health surface.
- In `src/commands/src/commands_admin.rs`, remove the moved items
  (functions and any `use` statements now unused) and add
  `pub(crate) use commands_health::*;` near the top so the test file at
  `src/commands/src/tests/commands_admin_test.rs` (which uses
  `super::degradation_lines`, `super::memory_cap_health_lines`,
  `super::tick_health_lines`, `super::heat_health_lines`,
  `super::source_trust_health_lines`, `super::dedup_health_lines`,
  `super::retrieval_health_lines`, `super::llm_health_lines`,
  `super::reflex_health_lines`, `super::ingest_health_lines`, and
  `super::cmd_health`) keeps resolving.
- In `src/commands/src/lib.rs` add `pub(crate) mod commands_health;` next
  to the existing `commands_admin` declaration. No caller moves: the
  `lib.rs` dispatch still says
  `Commands::Health => crate::commands_admin::cmd_health(cfg).await` and
  the same for `Status`, and the re-export keeps the path.

## Acceptance
`wc -l src/commands/src/commands_admin.rs` drops by the bytes of the
moved code (roughly 470 lines), `cargo test -p commands
degradation_lines_tests` is green, `cargo test -p commands
cmd_health_runs_on_a_fresh_graph_without_panicking` is green, and
`grep -n 'pub(crate) (async )?fn cmd_\|fn degradation_lines\|fn
tick_health_lines' src/commands/src/commands_admin.rs` answers nothing.

Landed on `split-admin-health`. `src/commands/src/commands_health.rs` is
574 lines and carries `cmd_health`, `cmd_status`, `daemon_health`, `probe`
and twelve `*_health_lines` helpers — the `Do` names eleven, but
`crossing_health_lines` is one too and `cmd_health` calls it, so it moved
with the rest. All twelve are `pub(crate)`: the test file calls them
unqualified through `use super::*`, so a private helper would not survive
the glob re-export. `load_graph` reached that file the same way, through
`commands_admin`'s own `use`, and now has its own import there.

`commands_admin.rs` is 19 lines, not the ~175 the `Do` implies: what the
parent asked for — a header, eight re-exports, and the test attachment.

`cargo test -p commands degradation_lines_tests` 11 passed,
`cmd_health_runs_on_a_fresh_graph_without_panicking` passed, `just check`
and `just memos-check` green.
