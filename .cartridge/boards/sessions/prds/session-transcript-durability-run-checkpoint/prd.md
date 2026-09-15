---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
needs:
- "@root/process-plugins-register-through-lua-lua-registration"
- "@sessions/session-transcript-durability-atomic-storage"
---

# Atomic transcript and agent-state checkpoints

## Do

Extend the sessions plugin, not the agent or core, to own durable session storage and one canonical transcript buffer per session. Preserve existing sessions/buffers APIs for general editor buffers. Add revision-checked atomic checkpointing so transcript records and session.agent state cannot disagree after a crash. Acknowledged writes must survive a process restart and explicit file/directory synchronization; errors must not leave silently mutated memory. Agent owns conversational semantics and recovery choices; sessions stores versioned records and run metadata.

Use `sessions {op:"checkpoint",id,expected_revision,records:[...],agent:{...}}`. On first checkpoint create and attach the canonical transcript; later checkpoints append complete JSONL records and shallow-merge agent state in one persisted session snapshot. Return `{revision,transcript}` with the numeric buffer ID. Get returns revision and transcript alongside existing fields. Revision mismatch changes nothing. Cwd changes during a running/awaiting-approval run are rejected. Do not automatically replay any tool on load.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/sessions/`.

Add checkpoint and revision fields as described in the PRD, with backward-compatible defaults on legacy sessions. Transcript records are versioned JSON objects `{v:1,kind,run,...}` serialized as one JSON object plus newline. Kind message holds a Chat message; lifecycle records include tool_started/tool_finished/run_started/run_finished. Enforce record object/version/size validity, but keep model/tool pairing logic in agent. Cap a checkpoint request at a configurable byte limit. Generic buffers get/list can read the canonical transcript; set/append/close on that protected buffer are rejected so no caller bypasses checkpoint revision checks. Other buffers retain existing behavior.

The transcript ID is persistent and unique, not found by taking the first buffer named transcript. Existing sessions without a canonical transcript start empty without deleting any old named buffers. Two concurrent checkpoint calls at one revision yield one success and one conflict. Revision increments on each checkpoint and any session metadata change that affects agent context. Do not mark an interrupted run completed at load or replay its pending side effects; expose saved state for the agent to recover.

## Acceptance
- [x] A first checkpoint creates exactly one attached transcript; later checkpoints reuse its ID across restart.
- [x] Transcript records and agent metadata persist atomically; injected failure produces neither half of a pre-rename checkpoint.
- [x] Concurrent expected_revision writes produce one winner and one unchanged conflict.
- [x] Malformed/oversized records and generic mutation of the canonical transcript fail without changing data.
- [x] Legacy sessions and ordinary buffers remain readable; interrupted tool/run state remains available without executing anything.
- [x] Cwd mutation while a run is active fails; permitted context changes advance the revision.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/sessions/Cargo.toml
cargo clippy --manifest-path plugins/sessions/Cargo.toml --all-targets -- -D warnings
```

Implemented as `8978ceb`, `d585839`, `7b9e3bf` on `work/session-checkpoint` (lane not landed; coordinator lands). Sixteen tests prove all six checks: transcript creation and ID reuse across restart, pre-rename checkpoint atomicity, concurrent revision conflict, malformed/oversized rejection, canonical transcript mutation guards, legacy readability, interrupted run state exposure, and cwd/agent revision advancement. Spec test/Clippy commands passed; combined `just check` and `just test` green (47/47).
