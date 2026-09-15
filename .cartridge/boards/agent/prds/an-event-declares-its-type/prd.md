---
repo: /Users/feb/dev/cartridge/agent.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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

## From the retired work memo

Folded 2026-09-15 from `work/an-event-declares-its-type.md` (status open, estimate 1d). The PRD state above is authoritative.

> The run journal's kinds become a declared vocabulary, each type stating whether it reaches the model and in what frame

### Outcome

The strings the run writes into its journal become a declared vocabulary. A type
declares its name and what it means for the model: `message` projects as the
conversation it already is; a type that carries no conversation — an
explanation, a memory, a notice from another agent — either projects in a
labelled frame of its own or does not project at all, and says which. The
projector asks the type. It does not carry a branch per kind, and adding a type
is a declaration rather than an edit to the harness.

A journal holding a type this build does not know still replays: the unknown type
is kept, skipped, and named as skipped where the run's context is inspected, so an
old session is never silently thinner than it was.

The vocabulary is the run's, beside the writer of the journal, so a cartridge
reading the stream and the harness projecting it agree on one list.

### Check

- [ ] Every kind the run writes today resolves to a declared type, and a fixture
      of existing sessions projects byte-identically before and after the change.
- [ ] A test adds one type with a projecting rule and one with a non-projecting
      rule, and neither requires an edit to the projector: the projecting one
      reaches the assembled request in its declared frame, the other is stored and
      absent from it.
- [ ] A journal line carrying an undeclared type projects the rest of the run
      unchanged, and `/context` names that type as skipped rather than omitting it.
- [ ] A run's inspected context attributes every journal record to a type, so the
      stream can be read by type without parsing messages.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. `record(kind, run)` mints `{"v":1,"kind":...,"run":...}`
(`builtin/agent/lib.rs:191`) and every stage adds its fields to it; the projection
keeps `kind == "message"` and drops the rest without comment
(`builtin/harness/working.rs:26`). The types therefore already exist as an
undeclared list split across two crates. This memo names them in one place and
moves the keep/drop decision onto the name.

Compatibility is the whole risk: `v:1` records are on disk, and the turn ring
still reads them (`builtin/harness/README.md`, "The turn ring"). Nothing about an
existing kind's meaning may change here — this is a declaration over what is
already written, and the behavioural changes belong to the memos that need them.
