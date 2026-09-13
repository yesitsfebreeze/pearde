---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: root
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: memory-document-works-end-to-end
needs:
- '@memory/memory-owns-its-tool/memory-consumer-parity'
- '@landscape/landscape-composes-system-context'
- '@runtime/one-runner-executes-documents/document-artifact-result'
---

# A memory document is discovered, read, executed, and improved live

Prove the first memory document on a fixed disposable composition. Remove recursive-development-graph from this slice's proposed needs; retain it on the final composed-system gate. Template installation and arbitrary-depth traversal cannot block this first runtime proof.

## Acceptance

- [ ] A real host discovers and reads one memory-owned query/ingest document and performs exact-ID readback with fixture providers.
- [ ] The same fixture proves denial before effects, approved ingest, stale-revision refusal and a failed reload retaining the previous usable writer.
- [ ] Record explicitly that nested-board discovery is untested by this slice and link its remaining requirement to the final release gate.

## Proof and recovery

Start at [settings.md](../../settings.md), [justfile](../../../../../../justfile).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-document-works-end-to-end`; maximum five rounds.
