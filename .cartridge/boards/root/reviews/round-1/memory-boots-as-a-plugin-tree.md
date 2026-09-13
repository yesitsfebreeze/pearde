---

kind: work
level: 9
status: open
estimate: 1d
needs: "[[extension-services-provide-and-inject]] [[extension-events-four-dispatch-modes]]"
description: the daemon boots a root `Context`, its subsystems become plugins providing services, its cross-crate signals become events, and `[[plugin]]` rows in memory.toml mount through the loader
read_when: "working the daemon side of the composition pillar, or asking how a plugin reaches the running memory"
---

# memory-boots-as-a-plugin-tree

## Do

Deliver [[memory-is-a-plugin-tree]] as the children below, in order:

subwork: [[memory-daemon-boots-a-root-context]] [[a-plugins-ingests-unwind-with-it]] [[memory-signals-become-events]] [[plugins-from-memory-toml]] [[disk-adapters-detach-without-forgetting-memory]]

The plugins that wrap memory's crates live in `commands` (a composing crate
above the layered set); `extension` itself imports nothing of memory.

## Check

Every child is done. `just test` is green, and `memory plugins` on the
project daemon prints the built-in fibers `Active` with the rows of its
`memory.toml` under the loader.
