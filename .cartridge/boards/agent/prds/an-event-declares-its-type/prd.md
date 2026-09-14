---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 3
review-status: failed
canonical-scope: an-event-declares-its-type
footprint:
- /Users/feb/dev/cartridge/agent.ctg/cartridge.json
- /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
- /Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
---

# an-event-declares-its-type

Every journal record kind the agent writes is a declared event in its own `cartridge.json` (name, description, JSON Schema), so the host's directory — not a sibling's catalog — says what a run can contain. Each declaration carries a projection frame with a fixed ceiling: `message`, labelled `data`, or `none`; nothing an ordinary type declares can request system or developer authority. Version-1 records stay valid. Honouring those frames when context is assembled is harness-owned and needs its own harness PRD; this leaf only declares and enforces at write time.

## Acceptance

- [ ] Every kind written today (`message`, `run_started`, `tool_started`, `tool_finished`, `model_turn_*` and any others the probe finds) resolves to a declaration listed by `cartridge help agent`.
- [ ] The agent refuses to journal an undeclared kind or a payload its schema rejects, and leaves the checkpoint revision unchanged.
- [ ] A declaration requesting a frame other than `message` for `message`, or above `data` for any other kind, stops the agent's start with that kind named; the existing role check keeps refusing non user/assistant/tool history.
- [ ] Existing `v:1` transcripts load and recover unchanged under a fixed fixture.

## Proof and recovery

Baseline (agent `fad6d3b`, harness `336f2d1`, cartridge `c9ef10b`): `record()` mints untyped `{"v":1,"kind":…}` (`agent.ctg/src/lib.rs:198`); harness `project_messages` keeps only `kind == "message"` and drops the rest silently (`harness.ctg/src/main.rs:407`); the agent refuses other roles (`agent.ctg/src/model_loop.rs:186-194`). Manifests accept `events` with schemas and refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). Bounded investigation: whether a schema annotation can carry the frame; stop and record a question if the host rejects it.

Precondition without a PRD: agent still targets the host API removed in cartridge `ee7e295`; no agent gate builds until it is ported to declared events.

Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run. Failure: a declaration error refuses start with the offending kind named; no record is rewritten.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
