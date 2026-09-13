---

kind: work
level: 9
status: open
estimate: 1d
needs: "[[@prd/work/memory--extension-services-provide-and-inject.md]] [[@prd/work/memory--extension-events-four-dispatch-modes.md]]"
description: the daemon boots a root `Context`, its subsystems become plugins providing services, its cross-crate signals become events, and `[[plugin]]` rows in memory.toml mount through the loader
read_when: "working the daemon side of the composition pillar, or asking how a plugin reaches the running memory"
---

# memory-boots-as-a-plugin-tree

## Do

Deliver [[memory-is-a-plugin-tree]] as the children below, in order:

subwork: [[@prd/work/memory--memory-daemon-boots-a-root-context.md]] [[@prd/work/memory--a-plugins-ingests-unwind-with-it.md]] [[@prd/work/memory--memory-signals-become-events.md]] [[@prd/work/memory--plugins-from-memory-toml.md]] [[@prd/work/memory--disk-adapters-detach-without-forgetting-memory.md]]

The plugins that wrap memory's crates live in `commands` (a composing crate
above the layered set); `extension` itself imports nothing of memory.

## Check

Every child is done. `just test` is green, and `memory plugins` on the
project daemon prints the built-in fibers `Active` with the rows of its
`memory.toml` under the loader.
