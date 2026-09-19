---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
needs:
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/lsp-contributes-symbols-usages-and-calls-to-asp'
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/fs-contributes-files-ranges-and-search-to-asp'
---

# agents find code through ASP and graft is removed

## Outcome

An agent finds code through ASP alone: a file's outline, a symbol's
definition and usages, callers and callees to any depth, and one search over
code and context. graft, the external code-graph tool, is then removed from
the workspace. On 2026-09-19 the user judged graft's deep LLM pass not worth
running, because the memo system and live tools cover it.

## Start at

- graft's wiring today: `/Users/feb/dev/cartridge/.mcp.json` (the `graft` MCP
  server); `/Users/feb/dev/cartridge/.claude/settings.json` (session-start,
  prompt, post-edit, tool-savings and stop hooks, plus `Bash(graft:*)`
  permissions); `.claude/helpers/graft-hooks.cjs` and `graft-statusline.cjs`;
  the skill `host/.claude/skills/graft/`; the `graft/` cache and its
  `.gitignore` lines; the `shell-tools` system memo
  (`host/.cartridge/memos/system/shell-tools.md`), which tells agents to use
  graft first.
- The user-global cld tools table lives outside this repository. Tell the
  user about it and do not edit it.

## Acceptance

- [ ] A named probe, run in a fresh agent session, answers "who calls X", "the
      outline of file Y" and "where is Z used" through `tool.asp` alone.
- [ ] Every graft item listed above is removed. `rg -n -i graft` over the
      repository's configuration, memos and skills finds nothing.
- [ ] The `shell-tools` memo names ASP as the first lookup.
