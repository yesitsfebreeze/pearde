---
kind: work
level: 9
status: open
estimate: 1d
description: the `extension` crate — Cordis's context, fiber, effects, services, events, config, loader, scope and inspector in Rust at L0, each a child memo with its own tests
read_when: "working any part of the compose crate, or asking what the crate must hold before the daemon can use it"
---

# the-extension-crate

## Do

Build `src/extension` (package `extension`, `//! Layer: L0 · No Memory imports.`,
workspace dependencies only: `tokio`, `parking_lot`, `serde`, `serde_json`,
`thiserror`, `tracing`) as the children below, in this order, each landing
on its own:

subwork: [[extension-context-and-fiber]] [[extension-services-provide-and-inject]] [[extension-events-four-dispatch-modes]] [[extension-plugin-config-and-update]] [[extension-loader-plugin-tree]] [[extension-scope-per-agent-registrations]] [[extension-inspect]]

The crate's public surface is the Table 2 column of
[[composition-is-a-pillar-of-memory]]; a name not in that table is not added
without a child memo naming it. Nothing in the crate awaits plugin code while
holding a lock: fiber and store state live behind `parking_lot` locks held
for a field read or write, and every `await` on a plugin's future happens
with no lock held ([[rust-harness-foundation]]).

## Check

Every child is done. `cargo nextest run -p extension` is green,
`cargo test --test layer_headers` accepts the crate at L0, and the crate's
`lib.rs` doc comment lists the Table 2 names it exports.
