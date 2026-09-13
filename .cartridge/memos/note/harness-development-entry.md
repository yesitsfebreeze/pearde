---
kind: note
memo: harness-development-entry
status: decided
subject: Development ownership for harness
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# harness development

Own conversation projection, compaction and budgets; consume Landscape context.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [harness assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Owns: [Harness builds model context from the shared landscape result](../../boards/harness/prds/harness-consumes-landscape/prd.md).
- Contributes to: [The UI presents the human view of the same landscape context](../../boards/ui/prds/human-context-is-the-same-document/prd.md).
- Contributes to: [Landscape quality and cost are tested against a versioned corpus](../../boards/landscape/prds/context-quality-is-measured/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build harness`, `just check harness`, and `just test harness` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
