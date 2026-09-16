---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
canonical-scope: ingestion-distiller-seam
---

# Digested ingest output lands in memory with provenance

The flow engine's ingest walk offers every committed item to a distiller seam and declares it without filling it. Fill that seam from `memory.ctg`, so a flow that pulls and transforms external data lands its digested result in the memory bank the composition already has, rather than in a second store built beside it.

The property worth carrying over from the upstream design is that a distilled claim backlinks to the source it came from, so a conclusion can be checked against its source instead of trusted. `memory.ctg` already stores facts with provenance; this work makes the ingest path write through that, and makes the backlink resolvable — a stored claim can be asked for its sources and answers with them, or reports the source as gone.

Whatever the distiller does not accept is named on the ingest attempt record with a reason. A digest step that silently dropped an item is the failure this seam exists to prevent.

## Acceptance

- [ ] An ingest run whose items are offered to the distiller stores each accepted result in `memory.ctg` with the source item recorded as its provenance.
- [ ] A stored result answers a query for its sources with the source items it came from; a result whose source has since been removed reports that, rather than answering with no sources.
- [ ] Every item the distiller did not accept is named on the attempt record with its reason, and the count of stored plus rejected equals the count offered.
- [ ] An unavailable memory store suspends the run with the reason named and stores nothing partial, rather than dropping the digest half of the walk.
- [ ] The seam is exercised offline in `just test memory` against a disposable store, with the flow engine's walk driven by fixture items.

## Proof and recovery

Depends on `@root/ctrl-flow-engine-cartridge`, whose ingest-walk child declares the `Distiller` seam this fills. Upstream `ctrl` fills the same seam with an external knowledge tool through a separate adapter crate; that adapter is dropped in the port and this child replaces it.

Baseline to re-verify at implementation: `memory.ctg` stores facts with provenance today, and whether a stored fact can already be asked for its sources decides whether the backlink is new work or a read of what exists.

Gates, cwd `/Users/feb/dev/cartridge`: `just test memory`, `just check memory`. Not run for this plan.
