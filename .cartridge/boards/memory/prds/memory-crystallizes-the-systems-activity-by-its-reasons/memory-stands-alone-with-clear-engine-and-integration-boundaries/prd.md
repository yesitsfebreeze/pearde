---
state: "done"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/memory.ctg"
commit: "d9161cd2f3a363915c7a7d642a4955e7a3836065"
---

# Memory stands alone with clear engine and integration boundaries

## Outcome

Memory is an independently understandable Rust project. Its domain model, graph operations, persistence and cartridge adapter have explicit ownership. Runtime observations use the same graph as other knowledge. The base host owns transport and dispatch; it does not own memory semantics.

## Design

Keep shared memory domain types in memory's base crate. Keep crystallization policy and recurrence in graph, durable input and receipts in store, batching in RPC, and ASP adaptation in cartridge. Split the crystallization module into observation metadata, matching, rollback and mutation responsibilities. Preserve serialized enum discriminants and existing stored fields. Remove the retired calendar implementation and its settings, fixtures and documentation together. Preserve the trace ingress name only as the existing transport contract.

Describe the standalone crate map, observation lifecycle, exact versus semantic consolidation, outcome separation, receipt horizon, failure recovery and bounded work in memory's documentation. Semantic crystallization preserves the representative output and bounded examples; it does not promise lossless reconstruction of discarded wording.

## Acceptance

- [x] Modules have one responsibility and use the project's rustfmt conventions.
- [x] Memory builds and its focused domain, persistence and RPC tests run independently of sibling cartridges.
- [x] The documented crate boundaries match Cargo dependencies; the domain graph has no host dependency.
- [x] Retired calendar modules and settings have no active callers.
- [x] README and help explain the actual API, recovery limits and storage behavior.
- [x] Persistence round trips, retry idempotency, outcome separation and stale-commit rollback remain tested.

## Validation

Run formatting and focused Rust tests in the isolated memory checkout. Review the diff against its recorded baseline before integration, preserving concurrent changes. Run the repository audit and isolation checks against the integrated result. Do not mark this PRD complete on documentation alone.

## Implementation checkpoint

Implemented in the current memory.ctg working tree. [Shared verification evidence](../implementation.md) records integration, tests and remaining limits. This checkpoint does not replace formal PRD collection.

## Authorized takeover (2026-09-19, memory-coordinator)

The user explicitly authorized takeover and scoped baseline collection in this session. Checked release moved codex-memory’s analysis claim to open; checked claim assigned memory-coordinator. The prior owner’s source and review history remain intact. The existing crystallization baseline is being verified independently of unrelated Scope detail, task migration, and body-readback changes. The baseline spans the original feature leaves; this structural leaf does not claim their behavioral acceptance or completion.
