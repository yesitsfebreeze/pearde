---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "specced"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: attributed-outcome-report
needs: ["@runtime/native-tool-observation-adapter"]
footprint: ["src/roster.rs - src/main.rs - src/observations.rs - .cartridge/tests/unit/main/observation_tests.rs - .cartridge/tests/integration/observations.test.ts - .cartridge/docs/observations.md","Cargo.toml","src/lib.rs","src/change_record.rs","src/changes.rs",".cartridge/tests/unit/main/change_records_tests.rs"]
commit: "a306370f10b78d94365b7832ce22ce8d10c09487"
---

# Attributed outcome report

Expose a bounded native sessions report over the runtime's existing configured diagnostic source. Project observed evidence without a second ledger, transcript mutation, Memory service or invented historical outcomes. This child inherits two review rounds from [Reflex](../prd.md).

## Acceptance

- [x] An actual composed-process fixture reports agent, UI read, polling, discovery, error and interrupted work distinctly, with attempts separate from completion and explicit collection window/omissions.
- [x] Old rows keep missing actor, status, time, size and revision unknown; verdicts compare against latest observed provider/descriptor revisions and explicit expiry, never silently become current.
- [x] Reports allowlist metadata, cap source reads and response rows/bytes, identify malformed/truncated/rotated evidence and never read request-supplied paths or mutate evidence.
- [x] Observation disabled/unavailable/corrupt states are explicit; telemetry cannot change an already-completed tool result or produce productivity/billing claims.

## Baseline and proof

[Parent baseline](../baseline.json), sessions 965108d: native reflex_report and observations are unknown operations. Runtime baseline proves successful tool dispatch currently emits no observations. Runtime adapter must be verified before collection. Run public sessions tests/check and the real SDK/composed-runtime fixture; synthetic projection tests alone do not complete this work.

## Review

[Inherited review and round 3](review.md), two rounds already used; maximum five.

Named channel registration revalidation at 423ecd32: source footprint includes registered channels and its shared mailbox codec; acceptance and behavior gates remain unchanged.
