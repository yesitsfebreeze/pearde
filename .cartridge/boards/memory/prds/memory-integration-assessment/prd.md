---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: memory-integration-assessment
needs:
- '@memory/memory-002'
- '@memory/memory-004'
- '@memory/memory-owns-its-tool/memory-adapter-core'
- '@memory/every-mutation-holds-the-store-writer-boundary'
---

# memory-integration-assessment

Track the linked current outcomes as a finite scope snapshot. Historical framework and product proposals remain source history.

## Acceptance

- [ ] Each included leaf has its own current acceptance and owner.
- [ ] Close this snapshot only against observed child evidence; later enhancements get separate work items.

## Work items

- [Memory counts use consistent public terminology](../memory-002/prd.md)
- [Mixed and cold recall preserve per-ability ranking](../memory-004/prd.md)
- [Memory serves query and ingest through its own adapter](../memory-owns-its-tool/memory-adapter-core/prd.md)
- [every-mutation-holds-the-store-writer-boundary](../every-mutation-holds-the-store-writer-boundary/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-integration-assessment`, `memory/the-vision`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--memory-integration-assessment.md` (status open). The PRD state above is authoritative.

> Close the availability, diagnostic, retrieval-quality, and agent-interface gaps found in the 2026-09-07 Memory integration assessment.

### Do

Complete the children below in order, prioritizing availability and truthful diagnostics before retrieval quality and interface improvements. This continues [the-agent-surface-is-usable](../the-agent-surface-is-usable/prd.md) without reopening its completed fixes.

The 2026-09-07 assessment observed text queries returning `no tokio runtime`, vector query and report returning `daemon rpc: rpc adapter: eof`, question answering returning an endpoint-up hint, and a later CLI health request exceeding 20 seconds. Meanwhile 142 targeted Rust tests passed at `15761c01`, and the typed-work-field checks passed. The deployed binary's source revision was not established. Reproduce each finding against the current revision before changing code; these observations do not prove that every failure has the same cause.

subwork:
- [memory-integration-runtime-refusals](../memory-integration-runtime-refusals/prd.md)
- [memory-integration-fast-readiness](../memory-integration-fast-readiness/prd.md)
- [memory-integration-embedding-status](../memory-integration-embedding-status/prd.md)
- [memory-integration-provider-errors](../memory-integration-provider-errors/prd.md)
- [memory-integration-lifecycle-canary](../memory-integration-lifecycle-canary/prd.md)
- [memory-integration-template-hygiene](../memory-integration-template-hygiene/prd.md)
- [memory-integration-semantic-evaluation](../memory-integration-semantic-evaluation/prd.md)
- [memory-integration-bounded-history](../memory-integration-bounded-history/prd.md)
- [memory-integration-setup-contract](../memory-integration-setup-contract/prd.md)
- [memory-integration-cloud-disclosure](../memory-integration-cloud-disclosure/prd.md)

The implementation belongs in each child's lane. This parent does not authorize stopping the shared daemon, repairing the production store, deleting existing facts, sending private corpus material to a new provider, or performing a deployment without the relevant approval.

### Check

Every child is `status: done` with its acceptance evidence recorded. Repeat the live integration probe against an identified deployed generation and record query, answer, report, readiness, and direct-ID results separately from isolated test results. Record unavailable dependencies and any checks not run; passing unit tests alone does not complete this parent.
