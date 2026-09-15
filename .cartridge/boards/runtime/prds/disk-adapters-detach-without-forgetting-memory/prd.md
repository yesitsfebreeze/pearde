---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: disk-adapters-detach-without-forgetting-memory
needs:
- "@memory/memory-daemon-boots-a-root-context"
- "@runtime/plugins-from-memory-toml"
---

# disk-adapters-detach-without-forgetting-memory

Keep watcher/memo interpretation and mounted-adapter lifecycle with the host owners. Memory exposes ordinary validated ingest and explicit source retraction, remaining usable with every adapter absent. This candidate preserves the engine invariant while superseding the old memory plugin-loader prerequisite.

## Acceptance

- [ ] With adapters disabled, direct ingest/query/get still work in a disposable store.
- [ ] Stopping a watcher or reloading memo does not delete durable facts; only an explicitly owned retractable source can be retracted.
- [ ] Reattachment does not duplicate a writer or silently change source identity, and failed optional adapters produce visible status while memory remains usable.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `disk-adapters-detach-without-forgetting-memory`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--disk-adapters-detach-without-forgetting-memory.md` (status open, estimate 1d). The PRD state above is authoritative.

> optional file and memo adapters can stop and restart while direct ingest and durable recall keep working

### Do

File watching and memo/frontmatter reading are optional mounted adapters into
the existing ingest boundary. With them disabled, direct content ingest and
recall still operate; re-enabling uses the existing loader rather than a new
configuration mechanism. Durable decisions and facts survive adapter reload,
while explicitly retractable projections follow their owned source contract.

This proves [[plugin-disposal-is-not-durable-memory-retraction]] under
[memory-boots-as-a-plugin-tree](../../../memory/prds/memory-boots-as-a-plugin-tree/prd.md). Store shutdown respects dependents and
preserves persistence; no real shared store is rekeyed or repaired by this
acceptance work.
