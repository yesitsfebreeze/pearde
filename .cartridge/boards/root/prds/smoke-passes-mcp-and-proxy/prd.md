---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 2
date: "2026-09-15"
footprint:
- "mcp.ctg"
- "proxy.ctg"
- "memo.ctg"
- ".cartridge/memos/routine/cartridge-smoke.md"
needs:
- sessions-and-gitfs-tests-are-green
- pty-router-harness-mcp-tests-are-green
---

# Smoke passes mcp and proxy

## Outcome

The two doors a worker uses (MCP tools, proxied model requests) pass the composed smoke.

## Acceptance

- [ ] `just smoke` exits 0: mcp lists tools with memo active (2026-09-14: `memo inactive`); proxy answers an authenticated request inside its deadline with harness context injected (2026-09-14: timeout).

## Result

Not started.
