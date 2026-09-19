---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/memo.ctg"
needs: ["@runtime/prompt-recall-reads-asp-search","@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memo-contributes-documents-to-asp","@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memory-contributes-its-entities-to-asp","@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-host-s-cartridge-entities-carry-state-and-generation","@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-prompt-recall-and-the-proxy-read-asp-search","@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on"]
footprint: ["src/context.rs","src/sources","src/lib.rs","src/service.rs","Cargo.toml","Cargo.lock","cartridge.json","evidence","README.md",".cartridge/help.md",".cartridge/docs/context.md",".cartridge/tests"]
---

# remove native context collector

## Outcome

memo's context operation, injection, recall-only settings, source state machine and evidence crate disappear while record and public document behavior remain.

## Acceptance

- [ ] the old native context request fails explicitly without mutations or provider calls; ordinary tool invocation context and document operations work; memo/document ASP search/expand retain owner/revision checks; obsolete tests/docs/settings/workspace dependency and lockfile references are absent. Run the surviving named tests, not only grep.

## Proof and recovery

Footprint starts: `src/context.rs`, `src/sources/`, `src/lib.rs`, `src/service.rs`, `Cargo.toml`, `Cargo.lock`, `cartridge.json`, `evidence/`, `README.md`, `.cartridge/help.md`, `.cartridge/docs/context.md`, `.cartridge/tests/integration/context.test.ts`, `.cartridge/tests/integration/kernel-context.test.ts`, `.cartridge/tests/unit/src/sources/kernel.rs`, and registrations/configuration tests found by the leaf analyst. Existing manifest/docs/context-test dirt must be reconciled before a lane. Do not remove unrelated invocation `context` or resolver evidence fields.

## Dependencies and review

This slice inherits two used rounds from the context-deletion decomposition: round 1 failed at 66/100 and round 2 passed at 94/100. Three remain. Decomposition approval does not approve an executable spec. Preserve every requirement in the linked split plan and independently review the executable specification before implementation.
