---
kind: routine
description: Check and exercise the native planning engine without Python or an external model
---

# Develop the planner

Run this memo through the runtime's `memo-run` adapter. Native planning lives in
`src/`; tests and worker fixtures live in `.cartridge/tests/`. The CLI and service
share the same engine. No installed Pearde process is required.

```just
set positional-arguments

check:
    bun run check
    bun run test

records:
    bun test ./.cartridge/tests/records.test.ts

plan *args:
    bun src/cli.ts plan "$@"
```

Tests use temporary repositories, local stand-in workers and fake memory replies.
They cover claims across aliases, dependency and footprint gates, isolated code
integration, committed verification receipts, rolling dispatch, cancellation,
bounded transport, session ownership and memory acknowledgment/replay.

External runs require an explicit trusted adapter. A worker exit alone never
proves completion. Failed or cancelled work retains its claim and evidence for
inspection. Generated jobs, locks and logs stay in ignored `.state/` directories.
