---
kind: work
level: 9
status: open
description: parent — the MCP surface was probed end to end from an agent session on 2026-09-06 and three of its 22 tools cannot be called blind; twenty children carry what it found
read_when: "fixing the agent surface, or asking what the probe measured"
---

# the-agent-surface-is-usable

## Do

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
[[@prd/work/memory--mcp-tools-declare-their-schema.md]],
[[@prd/work/memory--the-report-flag-reaches-the-binary.md]],
[[@prd/work/memory--query-caps-its-default-answer.md]],
[[@prd/work/memory--map-leaves-the-agent-surface.md]],
[[@prd/work/memory--claim-kind-lists-without-a-name.md]],
[[@prd/work/memory--ingest-says-when-a-fact-lands.md]],
[[@prd/work/memory--the-daemon-comes-back-after-the-watchdog.md]],
[[@prd/work/memory--empty-entities-leave-the-graph.md]],
[[@prd/work/memory--rename-the-memories-named-before-the-bound.md]],
[[@prd/work/memory--embeds-go-through-one-lane.md]],
[[@prd/work/memory--recall-does-not-queue-behind-ingest.md]],
[[@prd/work/memory--one-daemon-per-store.md]],
[[@prd/work/memory--the-embed-server-outlives-the-idle-gap.md]],
[[@prd/work/memory--the-intake-drain-runs-a-batch.md]],
[[@prd/work/memory--the-forget-cascade-leaves-no-dangling-edge.md]],
[[@prd/work/memory--an-empty-memory-is-reaped.md]],
[[@prd/work/memory--the-embed-lane-recovers-from-a-wedge.md]],
[[@prd/work/memory--a-successor-inherits-every-descriptor.md]],
[[@prd/work/memory--a-handover-generation-stops-on-a-signal.md]],
[[@prd/work/memory--memory-integration-assessment.md]],
[[@prd/work/memory--audit-mine-for-native-memory-integration.md]],
[[@prd/work/memory--provider-recovery-proves-its-authority-boundary.md]],
[[@prd/work/memory--agent-availability-errors-name-the-failed-boundary.md]],
[[@prd/work/memory--mcp-attachment-recovers-without-replaying-work.md]],
[[@prd/work/memory--daemon-startup-cannot-remain-silently-unreachable.md]],
[[@prd/work/memory--mcp-catalog-recovers-in-the-existing-session.md]],
[[@prd/work/memory--reflex-reports-attributed-tool-outcomes.md]],
[[@prd/work/memory--degrade-corrects-the-retrieval-path-it-names.md]],
[[@prd/work/memory--semantic-tool-recovery-retires-failed-generations.md]]

## Check

Every child is `status: done`, and one agent session repeats the probe: each of
the 22 tools called with its documented minimum arguments, no answer over
32,000 characters, no argument rejected for its JSON type, and a fact written
with `ingest` readable back by the id that call returned. Use the current
declared tool catalogue rather than freezing the historical count of 22 as a
product limit. Native-agent execution, briefing, sampling and schema deferral
are not on this acceptance path. The core proxy's per-turn memory acceptance
remains in [[@prd/work/memory--proxy-turns-carry-recall-and-reflex-tools.md]].

**Check read 2026-09-07 and it is false, on four children of nineteen.** Fifteen
are `status: done`. The four open are [[@prd/work/memory--rename-the-memories-named-before-the-bound.md]],
[[@prd/work/memory--one-daemon-per-store.md]], [[@prd/work/memory--the-embed-server-outlives-the-idle-gap.md]] and
[[@prd/work/memory--a-handover-generation-stops-on-a-signal.md]] — every one of them a part whose own
sweep found the code half landed and the live half unrun, so this parent is
waiting on runs and not on work. The probe half of the Check (22 tools called
again, no answer over 32,000 characters) was not repeated: it is one agent
session's measurement and it cannot pass before the children do
([[the-eight-unread-work-checks]]).
