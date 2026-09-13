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
[[mcp-tools-declare-their-schema]],
[[the-report-flag-reaches-the-binary]],
[[query-caps-its-default-answer]],
[[map-leaves-the-agent-surface]],
[[claim-kind-lists-without-a-name]],
[[ingest-says-when-a-fact-lands]],
[[the-daemon-comes-back-after-the-watchdog]],
[[empty-entities-leave-the-graph]],
[[rename-the-memories-named-before-the-bound]],
[[embeds-go-through-one-lane]],
[[recall-does-not-queue-behind-ingest]],
[[one-daemon-per-store]],
[[the-embed-server-outlives-the-idle-gap]],
[[the-intake-drain-runs-a-batch]],
[[the-forget-cascade-leaves-no-dangling-edge]],
[[an-empty-memory-is-reaped]],
[[the-embed-lane-recovers-from-a-wedge]],
[[a-successor-inherits-every-descriptor]],
[[a-handover-generation-stops-on-a-signal]],
[[memory-integration-assessment]],
[[audit-mine-for-native-memory-integration]],
[[provider-recovery-proves-its-authority-boundary]],
[[agent-availability-errors-name-the-failed-boundary]],
[[mcp-attachment-recovers-without-replaying-work]],
[[daemon-startup-cannot-remain-silently-unreachable]],
[[mcp-catalog-recovers-in-the-existing-session]],
[[reflex-reports-attributed-tool-outcomes]],
[[degrade-corrects-the-retrieval-path-it-names]],
[[semantic-tool-recovery-retires-failed-generations]]

## Check

Every child is `status: done`, and one agent session repeats the probe: each of
the 22 tools called with its documented minimum arguments, no answer over
32,000 characters, no argument rejected for its JSON type, and a fact written
with `ingest` readable back by the id that call returned. Use the current
declared tool catalogue rather than freezing the historical count of 22 as a
product limit. Native-agent execution, briefing, sampling and schema deferral
are not on this acceptance path. The core proxy's per-turn memory acceptance
remains in [[proxy-turns-carry-recall-and-reflex-tools]].

**Check read 2026-09-07 and it is false, on four children of nineteen.** Fifteen
are `status: done`. The four open are [[rename-the-memories-named-before-the-bound]],
[[one-daemon-per-store]], [[the-embed-server-outlives-the-idle-gap]] and
[[a-handover-generation-stops-on-a-signal]] — every one of them a part whose own
sweep found the code half landed and the live half unrun, so this parent is
waiting on runs and not on work. The probe half of the Check (22 tools called
again, no answer over 32,000 characters) was not repeated: it is one agent
session's measurement and it cannot pass before the children do
([[the-eight-unread-work-checks]]).
