---
repo: /Users/feb/dev/cartridge/router.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: router
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: audit-mine-for-native-memory-integration
footprint:
  - .cartridge/docs/routing-handoff.md
  - .cartridge/docs/routing-handoff.json
  - .cartridge/tests/integration/routing-handoff.test.ts
commit: "fa23893bd5dfb3a7d5a801ac42d34b6a915bf81b"
---

# audit-mine-for-native-memory-integration

Convert this obsolete implementation proposal into a finite evidence handoff. Current memory excludes model routing and src/mine is absent; compare retained routing requirements with router.ctg and preserve the old audit/commit history. Produce a disposition for each requirement, not another native Memory router.

## Acceptance

- [x] Every old routing/login/recovery requirement maps to an existing router/provider boundary, a bounded current gap or an explicitly obsolete requirement.
- [x] Memory startup/ingest/query retains configured endpoint use without requiring a revived mine, LiteLLM tree or agent launcher.
- [x] No credential relocation, service restart or source deletion occurs during this reconciliation; any actual migration is a separately reviewed owner task.

## Proof and recovery

Start at [lib.rs](../../../lib.rs), [catalog.rs](../../../catalog.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test router` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `audit-mine-for-native-memory-integration`; maximum five rounds.
