---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge"
needs: ["@runtime/prompt-recall-reads-asp-search","@memo/remove-native-context-collector","@fs/remove-context-file-provider","@lsp/remove-context-lsp-provider","@memory/asp-projection-without-context-contract","@harness/roster-without-context-evidence-contract"]
footprint: [".cartridge/tests/integration/context-path-retirement.test.ts",".cartridge/tests/integration/asp-system.test.ts",".cartridge/hooks/prompt-recall"]
---

# composition without legacy context path

## Outcome

the integrated enabled composition has no obsolete discovery transport or wire-contract copies and every retained consumer demonstrably works.

## Acceptance

- [ ] current manifest/listener/need census is empty for context.*; owner source census finds no old schema/state-machine copies, including harness (ordinary fs/sessions change-record Evidence is preserved). Through the actual host, query and expand document, memory, file and cartridge-state entities with known owner/revisions; exercise the installed prompt hook and authenticated roster. Refresh the generated root hook from the reviewed shipped artifact before the integrated memo removal becomes active. Prove optional empty/failure behavior and that proxy still uses ASP. Unit suites alone cannot establish composition.

## Proof and recovery

Exact integration footprint starts: new `.cartridge/tests/integration/context-path-retirement.test.ts`, existing `.cartridge/tests/integration/asp-system.test.ts` only if fixture helpers must be shared, `.cartridge/hooks/prompt-recall`. The task launcher reads `.cartridge/memos/routine/workspace-tasks.md`; its system target runs only asp-system.test.ts. The new spec must invoke `bun test .cartridge/tests/integration/context-path-retirement.test.ts` explicitly in its named test gate, so this slice needs no task-runner or memo registration edit. The new integration fixture must use disposable data and public provider events, not sibling private fixtures. The existing asp-system test is opt-in and exercises durable memory/JEV; it is precedent, not automatically sufficient proof. Do not expand this worker footprint to submodule source trees or root settings; pointer landing and settings registration are separately serialized coordinator actions.

Run affected owner checks/tests/audits, `./task isolation`, and `./task prd check --board root`; prove named behavioral tests and no skipped proof. Record the root/submodule revisions. Deferred landscape records must have unchanged bytes. No retirement or other transition of deferred plans is included.

## Dependencies and review

This slice inherits two used rounds from the context-deletion decomposition: round 1 failed at 66/100 and round 2 passed at 94/100. Three remain. Decomposition approval does not approve an executable spec. Preserve every requirement in the linked split plan and independently review the executable specification before implementation.
