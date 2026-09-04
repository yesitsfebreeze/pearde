---
title: mcp-server-quality-is-measured-by-task-completion-not-protoc
date: 2026-09-04
type: conclusion
tags: [conclusion, evaluation, mcp, tool-design]
sources:
  - "[[260904-6a96]]"
  - "[[260904-0a6b]]"
derived_from: []
---

# mcp-server-quality-is-measured-by-task-completion-not-protocol-compliance

An MCP server is correct by spec long before it's useful — the actual bar is whether an agent, cold, can complete a realistic task through it, which is why coverage defaults to "comprehensive" rather than "curated" and why the deliverable includes ten hand-verified, read-only eval questions rather than a test-passing checklist. Both decisions push the same direction: optimize for what an agent can accomplish blind, not for how cleanly the interface maps to the underlying API.

Consequence: pearde worker contracts should carry the same bar — a tool or integration a worker will call is done when an unbriefed run of it against read-only, string-verifiable probes passes, not when its schema type-checks.
