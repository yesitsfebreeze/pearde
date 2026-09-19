---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/lsp.ctg"
needs: ["@memo/remove-native-context-collector"]
footprint: ["src/source.rs","src/evidence.rs","src/lib.rs","init.lua","cartridge.json",".cartridge/tests/unit/source.rs","README.md",".cartridge/help.md"]
---

# remove context lsp provider

## Outcome

remove only the obsolete catalog evidence transport; keep tool status, diagnostics, envelopes, cancellation and ASP symbol/reference behavior.

## Acceptance

- [ ] no context.lsp event/listener/export or old source/evidence protocol/test remains. Named tests prove tool status and diagnostics retain result envelopes and ASP symbol/reference behavior survives. The existing root envelope PRD still owns its two outstanding MCP-session proofs.

## Proof and recovery

Footprint starts: `src/source.rs`, `src/evidence.rs`, `src/lib.rs`, `init.lua`, `cartridge.json`, `.cartridge/tests/unit/source.rs`, `README.md`, `.cartridge/help.md`, plus actual registration references.

Before dispatch, coordinator reconciles `@root/tool-lsp-answers-must-carry-the-tool-result-envelope` in place: retain all envelope/MCP/cancel requirements and historical checked evidence, but qualify its historical context-provider preservation clause as true for that earlier change and superseded only by this deletion leaf. Do not tick its remaining MCP boxes or reset its review count. Serialize any shared lib/manifest/docs footprint with a live owner; this reconciliation is not a hard requirement to complete unrelated MCP proofs before deletion and adds no dependency cycle.

## Dependencies and review

This slice inherits two used rounds from the context-deletion decomposition: round 1 failed at 66/100 and round 2 passed at 94/100. Three remain. Decomposition approval does not approve an executable spec. Preserve every requirement in the linked split plan and independently review the executable specification before implementation.
