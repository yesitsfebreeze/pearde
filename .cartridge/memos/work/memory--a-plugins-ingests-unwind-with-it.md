---
kind: work
level: 10
status: open
estimate: 4h
needs: ["@prd/work/memory--memory-daemon-boots-a-root-context.md"]
description: explicitly retractable plugin projections unwind with their fiber while durable memory survives adapter disposal
read_when: "letting a plugin write memory, or asking what unloading a plugin does to the graph"
---

# a-plugins-ingests-unwind-with-it

## Do

- The `store` service of [[@prd/work/memory--memory-daemon-boots-a-root-context.md]] exposes an
  explicitly retractable ingest effect with ownership unique to that effect,
  not merely the plugin's display name. Disposal retracts only that projection
  through the existing source-retraction boundary and records the reason.
- The inverse runs when its owning effect is disposed, never before. A stale
  disposer cannot retract a successor generation's writes.
- Durable ingest through a plugin remains durable. Stopping a watcher or
  transport does not assert source deletion, and direct caller facts acquire
  no disposal inverse. [[plugin-disposal-is-not-durable-memory-retraction]]
  narrows the former blanket inverse rule.

## Check

A disposable store contains one retractable plugin projection and one durable
fact committed through the same plugin. Disposing the effect retracts only the
projection with its recorded reason; the durable fact remains recallable.
Remounting restores the projection according to content/source identity, and
running an old disposer cannot retract the new owner's data. No check assumes
identical content and origin receive new IDs.
