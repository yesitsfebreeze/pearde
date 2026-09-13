---
kind: note
memo: pty-development-entry
status: decided
subject: Development ownership for pty
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# pty development

Own terminal/shell process lifetime independently of UI replacement.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [pty assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Contributes to: [Landscape answers across kernel, directories, memo, memory, and live state](../../boards/landscape/prds/landscape-composes-system-context/prd.md).
- Contributes to: [Each capability ships its own executable documentation](../../boards/root/prds/capabilities-live-with-their-owners/prd.md).
- Contributes to: [Sidecars, event tools, and reload have explicit lifetimes](../../boards/runtime/prds/documents-own-live-processes/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build pty`, `just check pty`, and `just test pty` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
