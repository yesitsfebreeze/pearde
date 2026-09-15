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
canonical-scope: a-plugins-ingests-unwind-with-it
---

# a-plugins-ingests-unwind-with-it

Runtime owns disposal of transient adapters; memory owns an explicit source-retraction operation with durable provenance. A transient projection is identified by owner generation and effect ID, while ordinary ingest remains durable. Rehome only lifecycle orchestration and retain the engine integrity requirement as a referenced contract.

## Acceptance

- [ ] Disposing an old effect retracts only its own transient projection and cannot retract a successor generation.
- [ ] A durable fact ingested through the same adapter stays recallable after disposal/reload.
- [ ] Reattachment uses documented source/content identity and records retraction reasons; no plugin runtime is reintroduced inside memory.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-plugins-ingests-unwind-with-it`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--a-plugins-ingests-unwind-with-it.md` (status open, estimate 4h). The PRD state above is authoritative.

> explicitly retractable plugin projections unwind with their fiber while durable memory survives adapter disposal

### Do

- The `store` service of [memory-daemon-boots-a-root-context](../../../memory/prds/memory-daemon-boots-a-root-context/prd.md) exposes an
  explicitly retractable ingest effect with ownership unique to that effect,
  not merely the plugin's display name. Disposal retracts only that projection
  through the existing source-retraction boundary and records the reason.
- The inverse runs when its owning effect is disposed, never before. A stale
  disposer cannot retract a successor generation's writes.
- Durable ingest through a plugin remains durable. Stopping a watcher or
  transport does not assert source deletion, and direct caller facts acquire
  no disposal inverse. [[plugin-disposal-is-not-durable-memory-retraction]]
  narrows the former blanket inverse rule.

### Check

A disposable store contains one retractable plugin projection and one durable
fact committed through the same plugin. Disposing the effect retracts only the
projection with its recorded reason; the durable fact remains recallable.
Remounting restores the projection according to content/source identity, and
running an old disposer cannot retract the new owner's data. No check assumes
identical content and origin receive new IDs.
