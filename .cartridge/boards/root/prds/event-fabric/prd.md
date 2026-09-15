---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
description: "Design and implement a unified event fabric so tools, cartridges and memory flow as observable, memory-addressed, provenance-carrying events"
---

# Event fabric — memory-addressed, provenance-carrying events

## Outcome

Every meaningful runtime action — tool calls, task lifecycle, cartridge events, memory operations, UI interactions — fires as an observable event carrying stable memory references and provenance, so any agent consuming the stream can reconstruct *why* something happened, *where* it came from, *what* it touched, and can read the referenced memory/memo content without re-searching.

## Context

User: "open everything through the agent... integrate all the tools together, all the cartridges, all the things via events, so it works in harmony. Events get fired and they get a memory address attached for important memories based on the context, and when other agents consume those events they already have context of why this was fired, where it comes from, and all the meta information plus additional info from the memory and maybe from the memos."

See the durable note "Event fabric vision" for the full elaboration.

## Agent swarm — the room and the global status

The same event fabric is the agents' shared chat room. Agents post assignment and progress events into the fabric and consume each other's events; there is no parallel chat channel beyond the stream itself.

- Agents join a common room; assigning a task is a targeted event, progress updates are broadcast events.
- The orchestrator owns the global context held by no single worker.
- On the user's word "status", the orchestrator reads the whole swarm's in-flight task events and returns one compact, synthesized spoken summary — per agent who/what it is working on plus a global all-good/busy/blocked note. Never a raw transcript or message list; the voice cartridge renders the summary human-like.

Cross-conversation consumption is required so a status reader sees every agent regardless of which conversation spawned it (same defect as store.ts:178).

## Acceptance
- [ ] Design memo written: event envelope shape (origin, cause/trigger, timestamps, task/session/conversation/agent IDs, memory address references, memo/context references, provenance rationale).
- [ ] Current event paths mapped: what already fires events today (Wire.listen daemon events, Coordinator.event provider deltas, workspace cartridge:state, live_agent/live_note/live_work), and where events are lost (no addressing, no selective memory enrichment).
- [ ] Memory addressing mechanism identified — reuse the stable `memory:<id>` keying from `live.ctg`'s `memory-graph.ts` so event payloads carry addresses, not blobs.
- [ ] Cross-conversation event consumption design (addresses the store.ts:178 task-visibility defect).
- [ ] Swarm room + status aggregation shaped: room events, orchestrator-held global context, per-agent who/what + global "status" compaction, voice rendering.
- [ ] Decide scope with user before substantial implementation — this is the design record, execution is separate.

## Result

Design phase. Implementation not yet authorized.
