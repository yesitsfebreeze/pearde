---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/fs.ctg"
needs: ["@memo/remove-native-context-collector","@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/fs-contributes-files-ranges-and-search-to-asp"]
footprint: ["src/source.rs","src/evidence.rs","src/lib.rs","init.lua","cartridge.json",".cartridge/tests/unit/source.rs","README.md",".cartridge/help.md",".cartridge/docs/context.md"]
---

# remove context file provider

## Outcome

remove context.file nomination, provider-only context_files configuration and old evidence transport while retaining independent fs.context and ASP file/range/read behavior.

## Acceptance

- [ ] event/listener/native export, provider-only settings, wire structs and old fixtures are absent. Named tests prove native reads, ASP file/range expansion/search and text read actions still work with existing owner/revision and stale behavior. Unrelated filesystem change-record Evidence remains.

## Proof and recovery

Footprint starts: `src/source.rs`, `src/evidence.rs`, `src/lib.rs`, `init.lua`, `cartridge.json`, `.cartridge/tests/unit/source.rs`, `README.md`, `.cartridge/help.md`, `.cartridge/docs/context.md`; resolve context_files configuration plumbing and source-test registration exactly during specification. `src/context.rs` is preservation evidence, not an automatic deletion target.

## Dependencies and review

This slice inherits two used rounds from the context-deletion decomposition: round 1 failed at 66/100 and round 2 passed at 94/100. Three remain. Decomposition approval does not approve an executable spec. Preserve every requirement in the linked split plan and independently review the executable specification before implementation.
