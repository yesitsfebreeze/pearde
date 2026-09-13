---
kind: note
memo: cartridge-development-entry
status: decided
subject: Development ownership for cartridge
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# cartridge development

Own runtime composition, SDK, calls, events, replacement and process lifetime; host generic execution machinery.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [cartridge assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Contributes to: [The memo cartridge supplies a Pearde-compatible project template](../../boards/memo/prds/memo-board-template/prd.md).
- Contributes to: [Memory owns its service and tool interface](../../boards/memory/prds/memory-owns-its-tool/prd.md).
- Contributes to: [Landscape answers across kernel, directories, memo, memory, and live state](../../boards/landscape/prds/landscape-composes-system-context/prd.md).
- Owns: [A shared execution path runs a selected just recipe](../../boards/runtime/prds/one-runner-executes-documents/prd.md).
- Contributes to: [A memory document is discovered, read, executed, and improved live](../../boards/root/prds/memory-document-works-end-to-end/prd.md).
- Owns: [Sidecars, event tools, and reload have explicit lifetimes](../../boards/runtime/prds/documents-own-live-processes/prd.md).
- Contributes to: [Development commands and verification have one owning implementation](../../boards/tools/prds/development-tooling-has-one-home/prd.md).
- Contributes to: [The composed system passes the complete workflow and retires redundant wrappers](../../boards/root/prds/the-composed-system-proves-the-plan/prd.md).
- Contributes to: [The root landscape searches every child cartridge's development record](../../boards/landscape/prds/recursive-development-graph/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build runtime`, `just check runtime`, and `just test runtime` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
