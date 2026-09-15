---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: the-agent-surface-is-usable
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
- '@memory/improve-memory-tool-get'
- '@memory/improve-memory-tool-errors'
- '@memory/improve-memory-readiness'
---

# An agent can recall, record, read back and diagnose memory through tool.memory

The old 22-tool `memory mcp` surface is gone. Agents now reach memory through `tool.memory`, which memory.ctg serves from its own cartridge (`src/cartridge.rs`). MCP and agent consumers relay it without any sibling knowledge (decision `a-cartridge-brings-its-own-surface`). This parent tracks the leaves that make that tool sufficient: its adapter, exact readback, actionable failures and readiness.

## Acceptance

- [ ] Each linked leaf is done with its own evidence at a single memory.ctg revision.
- [ ] Integration gate, run as the memory integration test at that revision: one `tool.memory` session calls describe, ingest, query, and get by the returned ID. It also triggers one invalid input and one unavailable embed. Every answer stays under 32,000 characters, and each failure carries its code.
- [ ] A live probe against an identified installed generation (`cartridge call memory`, with pid and build recorded) is kept apart from the isolated test. If the probe fails, record the failure and do not repair the production store.

## Work items

- [Memory serves query and ingest through its own adapter](../memory-owns-its-tool/memory-adapter-core/prd.md)
- [Agents read one recalled fact back by ID through tool.memory](../improve-memory-tool-get/prd.md)
- [tool.memory failures carry a stable code the agent can act on](../improve-memory-tool-errors/prd.md)
- [Report memory readiness separately from registration](../improve-memory-readiness/prd.md)

## Review

[Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--the-agent-surface-is-usable.md` (status open). The PRD state above is authoritative.

> parent — the MCP surface was probed end to end from an agent session on 2026-09-06 and three of its 22 tools cannot be called blind; twenty children carry what it found

### Do

One agent session called all 22 tools of `memory mcp` against the repo's own
store on 2026-09-06 and recorded the answer of each. What it found is not one
defect but twenty, and they fall into four groups. The surface declares
nothing about its own arguments. Three answers are larger than any context
window. The store underneath refills itself from an intake of parked captures
faster than a cleanup empties it, while the daemon that serves it exits every
few minutes. And every read
and every write funnels through a local embedding server that runs a single
slot and hangs rather than queues when asked for two at once, which is why a
`query` for one word can time out at 120 seconds.

The measurements are in the children; each carries its own `Do` and `Check`.

subwork:
[mcp-tools-declare-their-schema](../mcp-tools-declare-their-schema/prd.md),
[the-report-flag-reaches-the-binary](../the-report-flag-reaches-the-binary/prd.md),
[query-caps-its-default-answer](../query-caps-its-default-answer/prd.md),
[map-leaves-the-agent-surface](../map-leaves-the-agent-surface/prd.md),
[claim-kind-lists-without-a-name](../claim-kind-lists-without-a-name/prd.md),
[ingest-says-when-a-fact-lands](../ingest-says-when-a-fact-lands/prd.md),
[the-daemon-comes-back-after-the-watchdog](../the-daemon-comes-back-after-the-watchdog/prd.md),
[empty-entities-leave-the-graph](../empty-entities-leave-the-graph/prd.md),
[rename-the-memories-named-before-the-bound](../rename-the-memories-named-before-the-bound/prd.md),
[embeds-go-through-one-lane](../embeds-go-through-one-lane/prd.md),
[recall-does-not-queue-behind-ingest](../recall-does-not-queue-behind-ingest/prd.md),
[one-daemon-per-store](../one-daemon-per-store/prd.md),
[the-embed-server-outlives-the-idle-gap](../the-embed-server-outlives-the-idle-gap/prd.md),
[the-intake-drain-runs-a-batch](../the-intake-drain-runs-a-batch/prd.md),
[the-forget-cascade-leaves-no-dangling-edge](../the-forget-cascade-leaves-no-dangling-edge/prd.md),
[an-empty-memory-is-reaped](../an-empty-memory-is-reaped/prd.md),
[the-embed-lane-recovers-from-a-wedge](../the-embed-lane-recovers-from-a-wedge/prd.md),
[a-successor-inherits-every-descriptor](../a-successor-inherits-every-descriptor/prd.md),
[a-handover-generation-stops-on-a-signal](../a-handover-generation-stops-on-a-signal/prd.md),
[memory-integration-assessment](../memory-integration-assessment/prd.md),
[audit-mine-for-native-memory-integration](../../../router/prds/audit-mine-for-native-memory-integration/prd.md),
[provider-recovery-proves-its-authority-boundary](../../../router/prds/provider-recovery-proves-its-authority-boundary/prd.md),
[agent-availability-errors-name-the-failed-boundary](../agent-availability-errors-name-the-failed-boundary/prd.md),
[mcp-attachment-recovers-without-replaying-work](../mcp-attachment-recovers-without-replaying-work/prd.md),
[daemon-startup-cannot-remain-silently-unreachable](../daemon-startup-cannot-remain-silently-unreachable/prd.md),
[mcp-catalog-recovers-in-the-existing-session](../mcp-catalog-recovers-in-the-existing-session/prd.md),
[reflex-reports-attributed-tool-outcomes](../../../sessions/prds/reflex-reports-attributed-tool-outcomes/prd.md),
[degrade-corrects-the-retrieval-path-it-names](../degrade-corrects-the-retrieval-path-it-names/prd.md),
[semantic-tool-recovery-retires-failed-generations](../../../runtime/prds/semantic-tool-recovery-retires-failed-generations/prd.md)

### Check

Every child is `status: done`, and one agent session repeats the probe: each of
the 22 tools called with its documented minimum arguments, no answer over
32,000 characters, no argument rejected for its JSON type, and a fact written
with `ingest` readable back by the id that call returned. Use the current
declared tool catalogue rather than freezing the historical count of 22 as a
product limit. Native-agent execution, briefing, sampling and schema deferral
are not on this acceptance path. The core proxy's per-turn memory acceptance
remains in [proxy-turns-carry-recall-and-reflex-tools](../../../proxy/prds/proxy-turns-carry-recall-and-reflex-tools/prd.md).

**Check read 2026-09-07 and it is false, on four children of nineteen.** Fifteen
are `status: done`. The four open are [rename-the-memories-named-before-the-bound](../rename-the-memories-named-before-the-bound/prd.md),
[one-daemon-per-store](../one-daemon-per-store/prd.md), [the-embed-server-outlives-the-idle-gap](../the-embed-server-outlives-the-idle-gap/prd.md) and
[a-handover-generation-stops-on-a-signal](../a-handover-generation-stops-on-a-signal/prd.md) — every one of them a part whose own
sweep found the code half landed and the live half unrun, so this parent is
waiting on runs and not on work. The probe half of the Check (22 tools called
again, no answer over 32,000 characters) was not repeated: it is one agent
session's measurement and it cannot pass before the children do
([[the-eight-unread-work-checks]]).
