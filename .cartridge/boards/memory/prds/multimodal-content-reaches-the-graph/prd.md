---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: multimodal-content-reaches-the-graph
---

# multimodal-content-reaches-the-graph

Start with text plus one explicitly supported image format and a mixed-content fixture at the existing typed ingest frontier. Record source/media identity and the extraction/embedding model revision. Reject unsupported media explicitly; index dimension/model compatibility is checked before storing vectors. This plan adds engine ingestion only, not a UI or second media store.

## Acceptance

- [ ] Text, image and mixed fixtures produce source-attributed claims that query/get can read back.
- [ ] Unsupported type, malformed media, incompatible embedding dimensions and failed extraction report explicit outcomes without partial unlabelled text substitution.
- [ ] Existing text ingest and persisted data remain compatible; configured offline fixtures make no request to an undeclared endpoint.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `multimodal-content-reaches-the-graph`; maximum five rounds.
