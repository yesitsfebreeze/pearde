---
state: "analyzing"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
needs:
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/lsp-contributes-symbols-usages-and-calls-to-asp'
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/fs-contributes-files-ranges-and-search-to-asp'
footprint:
  - .mcp.json
  - .claude/settings.json
  - .gitignore
  - .ignore
  - ASP.md
  - .cartridge/memos/system/shell-tools.md
  - .cartridge/memos/routine/arena.md
  - .cartridge/tests/integration/asp-code-lookup.test.ts
claim: "coordinator-e4-3 2026-09-19T14:53:52.391Z"
---

# Agents find code through ASP

## Outcome

ASP supplies code discovery through cartridge MCP: file outlines, symbol references, callers and callees. The former external tool's server, hooks, skill and generated cache are removed. The active system uses ASP terminology and retains the useful discovery method.

## Acceptance

- [x] A named probe in a fresh MCP session answers callers, file outline and usages through ASP alone.
- [x] Obsolete server, hooks, skill and cache are absent.
- [x] The shell-tools memo names ASP as the first lookup.
- [x] Active code, configuration, documentation, skills, prompts and current planning records no longer carry the retired branding.

## Evidence

The recovered spec's fixture sat outside a Cargo module graph and could not establish callers. A temporary standalone crate with randomized symbols now proves outlines, incoming calls and references through the real MCP transport. Independent rerun passed with 12 assertions. The user's 2026-09-19 naming clarification also applies to this record's title and identity; its existing coordinator attribution is retained through checked adoption.
