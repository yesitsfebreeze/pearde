---
kind: note
memo: sessions-development-entry
status: decided
subject: Development ownership for sessions
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# sessions development

Own durable sessions, transcript and buffer state; contribute references to Landscape.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [sessions assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Contributes to: [Landscape answers across kernel, directories, memo, memory, and live state](../../boards/landscape/prds/landscape-composes-system-context/prd.md).
- Contributes to: [Each capability ships its own executable documentation](../../boards/root/prds/capabilities-live-with-their-owners/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build sessions`, `just check sessions`, and `just test sessions` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
