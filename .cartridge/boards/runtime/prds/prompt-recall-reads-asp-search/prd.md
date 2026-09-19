---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
needs: ["@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memo-contributes-documents-to-asp","@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memory-contributes-its-entities-to-asp","@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-host-s-cartridge-entities-carry-state-and-generation","@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/fs-contributes-files-ranges-and-search-to-asp","@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on"]
footprint: ["src/cli/prompt-recall.sh","src/cli/setup.rs",".cartridge/tests/unit/src/cli/setup.rs",".cartridge/tests/integration/prompt-recall.test.ts","README.md",".cartridge/help.md"]
---

# prompt recall reads asp search

## Outcome

the shipped UserPromptSubmit hook queries ASP search and renders bounded whole attributed results as untrusted additional context. Template and a newly installed copy behave identically. No memo context call or `.block` result dependency remains.

## Acceptance

- [ ] disposable executable probes show nonempty ASP hits produce the expected hookSpecificOutput envelope, preserve provenance and result boundaries, and cannot escape the untrusted framing. Empty input/results, absent binary/jq, failed/late/malformed ASP response emit no stdout and exit zero; the prompt is untouched. Apply an explicit total deadline and byte/row cap. Test a newly installed hook, not only template text. Setup preserves unrelated user hooks/settings and installation behavior. The root integration slice refreshes/proves the already installed checkout hook before memo deletion is activated there.

## Proof and recovery

Footprint starts: `src/cli/prompt-recall.sh`, `src/cli/setup.rs`, `.cartridge/tests/unit/src/cli/setup.rs`, a new focused hook test `.cartridge/tests/integration/prompt-recall.test.ts`, `README.md`, `.cartridge/help.md`. Confirm the repository's integration registration before finalizing the spec. Scope excludes root generated files.

## Dependencies and review

This slice inherits two used rounds from the context-deletion decomposition: round 1 failed at 66/100 and round 2 passed at 94/100. Three remain. Decomposition approval does not approve an executable spec. Preserve every requirement in the linked split plan and independently review the executable specification before implementation.
