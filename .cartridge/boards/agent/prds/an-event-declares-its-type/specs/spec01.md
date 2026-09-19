---
complexity: medium
footprint:
  - /Users/feb/dev/cartridge/agent.ctg/cartridge.json
  - /Users/feb/dev/cartridge/agent.ctg/Cargo.toml
  - /Users/feb/dev/cartridge/agent.ctg/Cargo.lock
  - /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs
  - /Users/feb/dev/cartridge/agent.ctg/src/base.rs
  - /Users/feb/dev/cartridge/agent.ctg/src/module.rs
  - /Users/feb/dev/cartridge/agent.ctg/src/journal.rs
  - /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
  - /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/integration/loop.rs
  - /Users/feb/dev/cartridge/agent.ctg/README.md
  - /Users/feb/dev/cartridge/agent.ctg/.cartridge/help.md
---

# spec01 — Validate journal batches against the agent's host declarations before checkpointing

This is a draft requiring the coordinator's footprint update and plan review. Base: agent `2ed4743b075976ebc255905b85688151d6ba8787`, with host prerequisite `8da102215640bedf9b11d4f3325abec34bf639a2` or a descendant exposing the same contract. The live manifest, README and help page contain foreign command-migration changes; reconcile ownership before implementation and preserve them. Do not collect foreign changes as this leaf's implementation.

The canonical PRD has used three of five review rounds. Its latest review failed at 86/100. This draft does not reset that allowance or clear that review.

## Acceptance

- [ ] Every newly written kind resolves to its own namespaced host event `agent.journal.<kind>` with a description, JSON Schema and explicit frame. The initial seven are `message`, `run_started`, `run_finished`, `tool_started`, `tool_finished`, `model_turn_started` and `model_turn_finished`. Journal wire kinds remain the existing short names and `v` remains 1. The mapping is a prefix rule, not a second catalog.
- [ ] Production startup obtains these declarations using `cartridge.host("declarations", nil)` before recovery or publication. It does not parse a disk manifest, substitute embedded declarations on host failure, or import another cartridge's source.
- [ ] Missing or invalid journal declarations, invalid schemas, missing frames, `message` with a frame other than `message`, and any other journal kind with a frame outside `data` or `none` refuse startup naming the offending kind. Host load still structurally rejects system/developer frames. Existing rejection of non-user/assistant/tool history remains effective.
- [ ] An undeclared kind, malformed envelope or schema-invalid payload in any position of a batch fails before a `sessions checkpoint` call. The transcript bytes, durable revision, Run revision/sequence and live snapshot remain unchanged. A subsequent valid batch succeeds from the same revision. This check covers ordinary records and the inline `tool_finished` envelope.
- [ ] A fixed v1 transcript loads and recovers without rewriting its existing bytes. It preserves unknown old kinds, closes unfinished tool calls once, and permits the next turn. Existing harness message projection and role authority do not change.
- [ ] The real-host integration probe proves that changed host manifest declarations govern startup even when the compiled module's embedded manifest differs. The live help directory points to the manifest and that help manifest contains all seven declarations.
- [ ] README and help describe the namespaced declaration mapping, fixed frame ceiling, write-time failure, host requirement and v1 compatibility. Unit, integration, lint, audit and isolation gates pass.

## Implementation order

1. Declare the seven events in `cartridge.json` without changing existing `agent` or `agent.event` schemas, listeners or notifications. Use `message` frame for `agent.journal.message`; use `none` for the six telemetry/lifecycle kinds to retain current projection behavior. Every schema validates the complete v1 record, requires `v`, `kind`, `run`, fixes the expected version and kind with `const`, and requires the payload fields the present writers supply. Message role is limited to user/assistant/tool; preserve null assistant content, tool-call arrays and provider extension fields. Require record-specific fields from the observed writers: `message`; `model`; `phase` and `telemetry`; tool `call`, `tool`, `tool_call_id` plus `input` or `result`; model-start `snapshot_error`, `http_body_bytes`, `model`, `messages`; model-finish `metrics`. Do not narrow arbitrary tool results or provider usage objects beyond the existing contract. Keep unknown extension properties compatible.
2. Add a focused `journal.rs` with a fallible declaration parser, closed frame enum and compiled JSON Schema validators. Add an ordinary `jsonschema` dependency, using the host's currently locked-compatible 0.56 series with default features disabled, and update only the agent lockfile. Compile schemas once at startup; reject unsupported or unresolved external references rather than fetching the network. Treat only `agent.journal.*` as journal declarations; unrelated API events do not need a frame. The module maps a record kind by prefix and validates complete batches without persistence effects.
3. Add the narrow native `base::host` accessor through the same entered Lua context used by `base::bail`. In module startup, fetch declarations on the base thread, construct the validated journal before `recover`, and pass it into Agent. Keep a clear test/standalone constructor that explicitly uses the same embedded manifest if needed to avoid rewriting all existing test fixtures; production must call the fallible host-backed constructor and must never fall back. The validated journal is immutable and shared with Runs.
4. Call batch validation at the start of `Run::save`, before constructing or sending the checkpoint and before mutating revisions or snapshots. `record()` is only an envelope constructor and cannot validate its incomplete payload. Preserve context.rs and stream.rs callers; all their complete records pass through save. Route the inline model_loop tool-finished envelope through the ordinary constructor for consistency if useful; correctness must not depend on that cleanup. Do not publish journal events as a side effect of validation.
5. Extend run-state tests with captured checkpoint-call counts and direct construction of a Run using injected declarations. Test undeclared kinds and rejected payloads in first, middle and last position with valid neighbors. Pin transcript bytes, durable revision, local revision/sequence and live snapshot before and after rejection, then successfully commit a valid batch. Exercise the existing model driver to cover real writes of all seven kinds, not only synthetic schema samples.
6. Add startup tests for missing declarations, malformed schemas, forbidden and missing frames, and role rejection. Add a literal old v1 fixture inside run_state.rs containing known records, an unknown kind and an unresolved tool call. Compare the exact preexisting byte prefix after recovery; verify the appended recovery records validate, no tool replays, and a second recovery is idempotent.
7. Extend the existing real-host integration harness. Copy the shipped manifest into its disposable agent cartridge, then mutate a journal declaration there without recompiling the module: a forbidden message frame must prevent publication, and a tighter user-message schema must reject a start without changing the session revision. A valid run must write all seven kinds, and `cartridge help agent/cartridge.json` in that fixture must expose their complete declaration entries. Restore no global state; use independent temp projects. Document behavior and preserve existing role checks and existing event stream semantics.

## Verify and Proof

These commands run first in the lane and then in the agent repository. Every path below is relative to that repository; the host binary is an absolute external tool, never a sibling-relative checkout. The named new tests are required deliverables, not tests already observed passing. `CARTRIDGE_BIN` must point to a binary containing host commit 8da1022; the default below is the executable observed in this analysis environment. All nested cargo commands in the integration harness inherit the isolated target directory.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/an-event-declares-its-type-verify}"
cargo fmt --all -- --check
cargo clippy --workspace --locked --all-targets -- -D warnings
```

```test
run: env -u CARTRIDGE_YOLO CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/an-event-declares-its-type-verify}" cargo test --locked --lib
pass: journal_declares_every_written_kind
pass: journal_rejects_entire_invalid_batch_without_checkpoint_or_revision_change
pass: journal_startup_rejects_invalid_declarations_and_frame_escalation
pass: journal_v1_recovery_preserves_original_bytes_and_unknown_records
pass: journal_history_still_refuses_privileged_roles
pass: model_driver_tool_call_then_answer_persists_ordered_messages_with_preserved_id
pass: recovery_closes_persisted_unresolved_tool_calls_without_replay
```

```test
run: env -u CARTRIDGE_YOLO CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/.local/bin/cartridge}" CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/an-event-declares-its-type-verify}" cargo test --locked --test loop
pass: host_journal_declarations_govern_startup_and_atomic_write_rejection
pass: host_help_exposes_every_journal_declaration
pass: scripted_tool_call_then_final_answer_is_ordered_and_preserves_id
pass: recovery_closes_unresolved_calls_then_a_new_turn_can_proceed
pass: harness_system_inserted_once_and_descriptor_schema_reaches_chat_unchanged
```

After integrated verification, the coordinator additionally runs composition-root `env -u CARTRIDGE_YOLO ./task test agent`, `env -u CARTRIDGE_YOLO ./task check agent`, `./task audit` and `./task isolation`, with an isolated CARGO_TARGET_DIR for commands that build Rust. These are composition gates rather than lane Verify blocks. Report unrelated preexisting findings accurately; do not claim a clean gate by silently omitting it.

## Failure and recovery

Declaration failure prevents agent startup before recovery changes existing journals. A rejected write leaves that checkpoint entirely unapplied; earlier valid checkpoints remain. No old journal is schema-revalidated or migrated on read. The usual runtime failure handling may subsequently append a valid terminal failure record; the invalid batch itself must never advance a revision. Preserve the existing behavior when even the terminal checkpoint fails, including checkpoint_error and no fabricated done event. Rollback is a code/manifest revert; stored v1 records need no migration.

Harness projection by declaration, unknown-kind inspection and subscription semantics are separately owned outcomes. This leaf must link the coordinator-created harness counterpart before review clears the historical blocker; it does not implement those behaviors here.
