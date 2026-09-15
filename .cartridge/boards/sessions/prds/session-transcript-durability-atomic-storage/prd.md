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
---

# Acknowledge only persisted session state

## Do

Extend the sessions plugin, not the agent or core, to own durable session storage and one canonical transcript buffer per session. Preserve existing sessions/buffers APIs for general editor buffers. Add revision-checked atomic checkpointing so transcript records and session.agent state cannot disagree after a crash. Acknowledged writes must survive a process restart and explicit file/directory synchronization; errors must not leave silently mutated memory. Agent owns conversational semantics and recovery choices; sessions stores versioned records and run metadata.

Use `sessions {op:"checkpoint",id,expected_revision,records:[...],agent:{...}}`. On first checkpoint create and attach the canonical transcript; later checkpoints append complete JSONL records and shallow-merge agent state in one persisted session snapshot. Return `{revision,transcript}` with the numeric buffer ID. Get returns revision and transcript alongside existing fields. Revision mismatch changes nothing. Cwd changes during a running/awaiting-approval run are rejected. Do not automatically replay any tool on load.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/sessions/`.

Refactor existing save-backed mutations to prepare a candidate session snapshot, write a unique temporary file in the same directory, sync it, rename over the destination, then sync the parent directory before publishing memory and notifying listeners. Preserve the old snapshot on failures before rename and clean temporary files. A failure after rename is a distinct uncertain-durability outcome: reload the renamed snapshot into memory, report persistence uncertainty and do not claim rollback or retry automatically. Serialize writes per store using existing locking; no new database.

Deletion must surface filesystem failures and avoid silently reappearing after restart. Corrupt existing session files remain on disk and generate a discoverable load diagnostic rather than appearing as an empty/new session; do not overwrite them under the same ID. Use fault injection around write/sync/rename, not reliance on platform permission accidents in tests. Preserve unattached memory-only buffers and existing event shapes.

## Acceptance
- [x] Acknowledged session/buffer changes survive plugin restart, including Unicode transcript text.
- [x] Injected pre-rename write/sync failures preserve old disk and memory state and emit no success event.
- [x] Injected post-rename directory-sync failure is reported as uncertain durability with memory matching the renamed data.
- [x] Delete failures are visible and do not report success; corrupt files are preserved and diagnosed.
- [x] Existing generic session and unattached-buffer tests remain compatible.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/sessions/Cargo.toml
cargo clippy --manifest-path plugins/sessions/Cargo.toml --all-targets -- -D warnings
```

Landed as `1db861d` into `snapshot/plugin-workspace`. Eight focused tests prove all five checks, including 21 pre-rename fault/mutation combinations, post-rename uncertainty, corrupt-file preservation, Unicode restart, and ordinary buffers. Spec test/Clippy commands passed. Combined `just all`: 39/39, fmt/Clippy/docs passed. Lane closed after owner release, ancestry verification, and generated Cargo output cleanup.
