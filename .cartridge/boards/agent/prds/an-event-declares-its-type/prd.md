---
repo: /Users/feb/dev/cartridge/agent.ctg
state: "claimed"
origin: requested
priority: 100
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 4
review-status: "passed"
canonical-scope: an-event-declares-its-type
needs:
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/an-event-declaration-carries-a-host-validated-frame-and-a-cartridge-can-read-its-own-declared-events'
footprint: ["/Users/feb/dev/cartridge/agent.ctg/cartridge.json","/Users/feb/dev/cartridge/agent.ctg/Cargo.toml","/Users/feb/dev/cartridge/agent.ctg/Cargo.lock","/Users/feb/dev/cartridge/agent.ctg/src/lib.rs","/Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs","/Users/feb/dev/cartridge/agent.ctg/src/base.rs","/Users/feb/dev/cartridge/agent.ctg/src/module.rs","/Users/feb/dev/cartridge/agent.ctg/src/journal.rs","/Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs","/Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/integration/loop.rs","/Users/feb/dev/cartridge/agent.ctg/README.md","/Users/feb/dev/cartridge/agent.ctg/.cartridge/help.md"]
claim: "coordinator-codex-4 2026-09-19T17:40:15.226Z"
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

Precondition, struck 2026-09-19: the earlier note said the agent still targeted the host API removed in cartridge `ee7e295` and that no agent gate builds until it is ported. That is false at HEAD. With `agent.ctg` clean at `620857d`, `just check agent` exits 0 (`check agent pass`, `isolation composition pass`) and the crate compiles. The port has landed.

Gate correction, 2026-09-19, revised the same day: `just test agent` appeared to exit 1 at HEAD, with `multiple_tool_calls_execute_and_persist_in_response_order` failing at `.cartridge/tests/integration/loop.rs:798`, `assert_eq!(finished[0]["result"]["error"], true)`, observed `Bool(false)`. A second probe established that this is not a defect. `CARTRIDGE_YOLO=1` is exported by `just launch claude --yolo` and inherited by the test harness, the host merges `yolo: true` into the cartridge, and `agent.ctg/src/lib.rs:634` then skips the policy branch entirely, so the denied call simply runs and `error: false` is the correct journal entry. With the tree and the test unmodified, `env -u CARTRIDGE_YOLO cargo test -p agent --test loop` exits 0 with 13 passing, and `CARTRIDGE_YOLO=1` exits 1 with 12. **`just test agent` is green at HEAD when run without that variable.** The remaining work is to make the harness hermetic, which is `@agent/a-denied-tool-call-journals-its-error-flag` (retargeted; its slug is stale). This PRD's own tests also run under `cargo test -p agent --lib`, which exits 0 with 21 passing, because `.cartridge/tests/unit/run_state.rs` is wired as a module at `src/lib.rs:895` rather than as a `[[test]]` target (`autotests = false`, only `loop` declared).

Footprint note, 2026-09-19: journal kinds are minted from five files, and `src/context.rs:118` and `src/stream.rs:194,196` are outside this footprint. Both reach the journal through `record()` at `src/lib.rs:203`, so a single guard there covers them and the footprint holds. Only `src/model_loop.rs:44` builds its envelope inline, and that file is in the footprint. The implementer must put the guard in `record()` rather than scatter checks per call site. The probe also found `run_finished`, which Acceptance box 1 does not name; the full set written today is `message`, `run_started`, `run_finished`, `tool_started`, `tool_finished`, `model_turn_started` and `model_turn_finished`.

Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run. Failure: a declaration error refuses start with the offending kind named; no record is rewritten.

## Questions

Recorded 2026-09-19 after the analyst probe. This PRD named its own stop
condition — "Bounded investigation: whether a schema annotation can carry the
frame; stop and record a question if the host rejects it" — and the host rejects
it. Two decisions are needed, and both lie outside this footprint, so neither is
the analyst's or the coordinator's to take.

**Q1. Where does the projection frame live, given the host refuses a `frame`
field on an event declaration?**

`cartridge.ctg/src/loader/document.rs:41-50` declares `struct Event` with
`#[serde(deny_unknown_fields)]` and exactly three fields: `description`,
`schema` and `timeout_ms`. A declaration carrying `"frame": "message"` beside
`description` and `schema` fails to load. The only surviving carrier inside this
footprint is a custom keyword inside `schema`, which the host stores as an opaque
`serde_json::Value` and never interprets. That would make the frame an
agent-side convention the host neither validates nor renders, in tension with
this PRD's own sentence that the host's directory, not a sibling's catalog, says
what a run can contain.

**Q2. How does the agent read its own declarations at run time?**

Acceptance boxes 1 to 3 all require the agent to compare a kind against its
declared events. The host settles *settings* into a cartridge at start but keeps
`events` host-side, reaching them internally as `plan.events.keys()` in
`cartridge.ctg/src/host/mod.rs`, and it declares no event a cartridge could call
to retrieve them: `jq '.events | keys[]' cartridge.ctg/cartridge.json` returns
nothing. Enforcement therefore needs a host change to settle declared events at
start, a new host event to fetch them, or the agent re-reading its own
`cartridge.json` from disk.

**Recommended answer.** Split, smallest first. Add a child PRD against
`cartridge.ctg` that adds a declared, host-validated frame field to `struct
Event` with the fixed ceiling `message` / `data` / `none` and the rule that an
ordinary type may not request system or developer authority, and that hands a
cartridge its own declared events at start the same way settings are settled.
This leaf then becomes what it claims to be: a manifest edit plus one write-time
guard in `record()`, entirely inside its current footprint. Recommended because
it is the only option where the host, not the agent, enforces the ceiling that
Acceptance box 3 names.

**Alternatives.**

1. Carry the frame as a custom keyword inside `schema` (for example `x-frame`)
   and have the agent read its own `cartridge.json` from disk. Stays inside this
   footprint and needs no host change. Cost: the host never checks the ceiling,
   `cartridge help agent` shows the frame only as an uninterpreted schema key,
   and the manifest is parsed twice.
2. Declare the kinds now and defer the frame. Ship Acceptance boxes 1, 2 and 4
   and move box 3 to the harness-owned projection PRD this outcome already
   anticipates. Smallest diff, but leaves this PRD's headline unmet.
3. Reject the leaf as specified and fold the whole outcome into that harness PRD.
   Not recommended: write-time refusal is genuinely separable from context
   assembly, which is why this leaf exists.

Evidence added 2026-09-19 after the question was recorded, from the session building ASP: a cartridge can now reach the host method `asp` through `cartridge.host`, granted beside `status`, `snapshot` and `cartridges`. A `declarations` host method would be the same two-line grant. This does not decide Q2 — the choice between settling declared events at start and exposing a host method to fetch them is still open — but it makes the host-method option cheaper than the question implies. The same session reports that ASP's own types landed as a top-level `asp` block on the manifest `Cartridge` struct (cartridge.ctg `7af748a`), not as fields of `struct Event`, so ASP does not supply a frame field and has no consumer for the settle half either. Both halves stay as recommended.

Answered 2026-09-19 by the user (Claude Code session 5c846381, cartridge-e4): host child PRD, as recommended. Split into `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/an-event-declaration-carries-a-host-validated-frame-and-a-cartridge-can-read-its-own-declared-events`; this leaf keeps the manifest edit and the write-time guard in `record()`.

Note for whoever answers: this PRD is priority 100 and it gates
`@runtime/a-listener-subscribes-to-event-types`, also priority 100, whose `held`
reads `needs: not done — @agent/an-event-declares-its-type`. `needs` clears on
`done`, not on `specced`.

## Review

[Review history](review.md): round 4 passed at 96/100; four rounds used and one remains. Independent lane verification passed; integrated verification and collection remain pending.

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

### Historical checks and current owners

These are preserved scope from the retired memo, not additional agent acceptance
checks or claims of completion. The active agent Acceptance section owns write-time
declarations and fixed v1 recovery. The data/none projection, byte-identical message
projection and per-record inspection requirements are retained by
@harness/context-projection-honors-declared-frames-and-names-skipped-journal-kinds.
Each owner must pass its own current gates before collection.

- Historical criterion: Every kind the run writes today resolves to a declared type, and a fixture
      of existing sessions projects byte-identically before and after the change.
- Historical criterion: A test adds one type with a projecting rule and one with a non-projecting
      rule, and neither requires an edit to the projector: the projecting one
      reaches the assembled request in its declared frame, the other is stored and
      absent from it.
- Historical criterion: A journal line carrying an undeclared type projects the rest of the run
      unchanged, and `/context` names that type as skipped rather than omitting it.
- Historical criterion: A run's inspected context attributes every journal record to a type, so the
      stream can be read by type without parsing messages.
- Historical criterion: `just check` and `just test` pass.

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

## Incoming change to the same file

Recorded 2026-09-19 by the coordinator. Coordinator cartridge-4b has created
`@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/the-agent-asks-through-the-host-request-and-keeps-no-approval-of-its-own`,
a child on the runtime board whose footprint is in `agent.ctg`. It deletes the
agent's own approval path — `struct Approval` (`src/lib.rs:109`), the
`pending` field (`:124`), `load_pending` (`:229`), the `"answer"` dispatch arm
(`:246`), the pending/snapshot check (`:400-404`), the cancel path that answers
`false` on a dropped approval (`:421-422`), `live.pending = None` (`:581`) and
`approve` (`:854-869`) — and routes `ask` through a host `policy.request`.

It is open and unclaimed and it holds no claim, and this PRD is in `question`
and holds none either, so the engine will not stop either row on account of the
other. The consequence to watch is factual rather than procedural: this PRD's
Acceptance box 1 enumerates the kinds written today, and its footprint note
rests on `record()` at `src/lib.rs:203` being the single choke point every kind
flows through. If that deletion removes or renames any `tool_started` or
`tool_finished` record on the approval path, the enumerated kind set here goes
stale. cartridge-4b has been asked to report the final kind set when the child
lands, so this body can be corrected rather than left wrong.

The new host child, `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/an-event-declaration-carries-a-host-validated-frame-and-a-cartridge-can-read-its-own-declared-events`, also touches the kind set indirectly: it settles or exposes the declared events this leaf's write-time guard compares against. Acceptance box 1's enumeration must be re-checked against `record()` at `agent.ctg/src/lib.rs:203` when either that child or cartridge-4b's approval-path deletion lands.

## Current implementation boundary (Codex, 2026-09-19)

The host declaration prerequisite is collected at 8da1022. The downstream projection and skipped-kind outcome is now owned by @harness/context-projection-honors-declared-frames-and-names-skipped-journal-kinds, which depends on this leaf and inherits its three used review rounds. Historical missing-owner and frame-carrier questions above are resolved by those records.

The current analyst established that record() returns an incomplete envelope whose payload callers add later. Complete batch validation must occur in Run::save before checkpointing, covering every writer and inline envelope. The attached spec proposes the required expanded source, manifest, tests and documentation footprint for independent review. Historical instructions requiring payload validation inside record() are superseded by this evidence. No acceptance has yet been proved for the new behavior.
