---
kind: note
memo: gitfs-development-entry
status: decided
subject: Development ownership for gitfs
description: Local responsibilities and links into the recursive cartridge development board
date: 2026-09-13
---

# gitfs development

Own Git overlay and ship operations; repair result envelopes before consolidation.

This cartridge owns its `.cartridge` memos and local PRDs. The [root board](../../boards/root/README.md) coordinates the whole tree; Landscape must eventually expose these records recursively without copying them. Source documentation alone does not establish a callable live capability.

Read the [gitfs assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for independence, observed test coverage, limitations and consolidation disposition.

## Work references

- Owns: [Every currently exposed tool completes through its real consumers](../../boards/gitfs/prds/tool-results-interoperate/prd.md).
- Contributes to: [Each capability ships its own executable documentation](../../boards/root/prds/capabilities-live-with-their-owners/prd.md).

## Development loop

Read owner instructions and current evidence; probe one contract; produce specs; implement; run scoped checks and real consumer probes; record source revisions and outcomes. See the [shared workflow](../../workflows/develop-one-cartridge.md). Preserve durable stores and unrelated changes. Run commands from the composed root; use `just build gitfs`, `just check gitfs`, and `just test gitfs` where the catalog supports them. Empty or absent suites are coverage gaps, not successful verification.
