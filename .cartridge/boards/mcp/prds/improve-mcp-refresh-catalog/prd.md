---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: mcp
work-kind: leaf
review-round: 4
review-status: passed
canonical-scope: improve-mcp-refresh-catalog
needs:
- '@runtime/mcp-stdio-replies-during-replacement'
- '@gitfs/tool-results-interoperate'
footprint:
- src/service.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/tests/integration/refresh.test.ts
- .cartridge/docs/README.md
commit: "29b20b27b352ccb8df04cbc2ad9e4eefa20e7369"
---

# Refresh a live client's tool catalog after replacement

A connected MCP client can observe changed, added and removed tools without using a stale descriptor silently.

## Acceptance

- [x] An initialized fixture client observes replacement and removal; subsequent list/call use the current schema and generation.
- [x] A rejected replacement retains the old usable catalog; clients without notification support can re-list successfully.

- [x] Keep standard MCP negotiation and current client compatibility. New diagnostics must be additive or separately discoverable. Test configured grants in temporary profiles, never loosen live policy to make a check pass.

## Proof and recovery

Start at [service.rs](../../../service.rs), [tests.rs](../../../tests.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test mcp` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-mcp-refresh-catalog`; maximum five rounds.

## Current analysis

[Baseline](baseline.json) demonstrates mixed generations when replacement lands
during descriptor collection. Existing service-version invalidation and runtime
composition already provide ordinary re-listing. Validate the version vector
before and after collection, retry boundedly on churn, and publish only a stable
registry. Prove live addition/removal and rejected replacement over one actual
initialized stdio client. Preserve polling compatibility and do not advertise
unsupported push notifications.

## Discovered transport dependency

The actual client proved a missing runtime reply during replacement. Its bounded
runtime repair is a hard prerequisite; see the linked dependency and round 4.

## Verified result

Public `just test mcp` passes all 12 tests, including one actual initialized
stdio client across replacement, rejection, addition and removal. The discovery
race now returns coherent descriptors; persistent churn stops after three
attempts. Public formatting/clippy passes. The runtime reply dependency is
collected at f71b762fd839e6a2644f16565b1de10edf967c9e.
