---
kind: note
memo: tools-development-entry
status: decided
subject: Development ownership for tools
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# tools development

Own current development/bundling/worktree commands until migration into runtime-owned development tooling.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [tools assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Owns: [Development commands and verification have one owning implementation](../../boards/tools/prds/development-tooling-has-one-home/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build tools`, `just check tools`, and `just test tools` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
