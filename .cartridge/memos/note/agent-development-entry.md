---
kind: note
memo: agent-development-entry
status: decided
subject: Development ownership for agent
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# agent development

Own model/tool turn orchestration; consume shared context and execution.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [agent assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Contributes to: [Every currently exposed tool completes through its real consumers](../../boards/gitfs/prds/tool-results-interoperate/prd.md).
- Contributes to: [Harness builds model context from the shared landscape result](../../boards/harness/prds/harness-consumes-landscape/prd.md).
- Contributes to: [Agent, MCP, and proxy share discovery and execution behavior](../../boards/mcp/prds/clients-share-document-execution/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build agent`, `just check agent`, and `just test agent` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
