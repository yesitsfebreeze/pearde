---
complexity: small
footprint:
  - .mcp.json
  - .claude/settings.json
  - .gitignore
  - .ignore
  - ASP.md
  - .cartridge/memos/system/shell-tools.md
  - .cartridge/memos/routine/arena.md
  - .cartridge/tests/integration/asp-code-lookup.test.ts
---

# ASP is the code discovery interface

## Acceptance

- [x] A fresh MCP session answers outlines, callers and usages through ASP.
- [x] Configuration registers cartridge MCP and the composed prompt directs code lookup to ASP.
- [x] The superseded integration and branding are removed.

## Implementation

Register cartridge mcp in .mcp.json. Remove the obsolete integration's hook commands, helper scripts, skill and generated caches. Preserve unrelated session hooks. Update the shell-tools and arena records through memo. Use neutral ASP terminology in documentation and planning.

The integration fixture is its own temporary Rust crate. It randomizes symbol names, initializes a fresh MCP session and proves file containment, calls and references. A bounded indexing wait handles the first language-server pass; the fixture is removed afterward.

## Verify and Proof

```sh
set -eu
bun test ./.cartridge/tests/integration/asp-code-lookup.test.ts
python3 -c 'import json; d=json.load(open(".mcp.json")); assert d["mcpServers"]["cartridge"]["command"] == "cartridge"; assert d["mcpServers"]["cartridge"]["args"] == ["mcp"]'
just prompt
git diff --check
just isolation
```

## Independent verification

The root coordinator reviewed the configuration and fixture and independently reran the test successfully on 2026-09-19. All three questions passed through the real MCP transport. Repository source scans excluded generated build outputs, runtime histories and git history; active source and current authored records have no retired name.
