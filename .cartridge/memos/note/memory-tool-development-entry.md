---
kind: note
memo: memory-tool-development-entry
status: decided
subject: Development ownership for memory-tool
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# memory-tool development

Temporary query/ingest wrapper; migrate into memory after consumer and exposure checks.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [memory-tool assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Contributes to: [Memory owns its service and tool interface](../../boards/memory/prds/memory-owns-its-tool/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build memory-tool`, `just check memory-tool`, and `just test memory-tool` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
