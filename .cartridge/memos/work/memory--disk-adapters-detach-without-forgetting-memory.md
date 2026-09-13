---
kind: work
level: 10
status: open
description: optional file and memo adapters can stop and restart while direct ingest and durable recall keep working
estimate: 1d
needs: '[[@prd/work/memory--memory-daemon-boots-a-root-context.md]] [[@prd/work/memory--plugins-from-memory-toml.md]]'
read_when: proving disk adapters are plugins rather than the memory engine
---

# disk-adapters-detach-without-forgetting-memory

## Do

File watching and memo/frontmatter reading are optional mounted adapters into
the existing ingest boundary. With them disabled, direct content ingest and
recall still operate; re-enabling uses the existing loader rather than a new
configuration mechanism. Durable decisions and facts survive adapter reload,
while explicitly retractable projections follow their owned source contract.

This proves [[plugin-disposal-is-not-durable-memory-retraction]] under
[[@prd/work/memory--memory-boots-as-a-plugin-tree.md]]. Store shutdown respects dependents and
preserves persistence; no real shared store is rekeyed or repaired by this
acceptance work.
