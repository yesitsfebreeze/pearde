---
kind: note
memo: memory-development-entry
status: decided
subject: Development ownership for memory
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# memory development

Own durable knowledge, ingestion, retrieval and provenance; absorb its tool adapter without hosting generic execution.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [memory assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Owns: [Memory owns its service and tool interface](../../boards/memory/prds/memory-owns-its-tool/prd.md).
- Contributes to: [Landscape answers across kernel, directories, memo, memory, and live state](../../boards/landscape/prds/landscape-composes-system-context/prd.md).
- Contributes to: [A memory document is discovered, read, executed, and improved live](../../boards/root/prds/memory-document-works-end-to-end/prd.md).
- Contributes to: [Landscape quality and cost are tested against a versioned corpus](../../boards/landscape/prds/context-quality-is-measured/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build memory`, `just check memory`, and `just test memory` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
