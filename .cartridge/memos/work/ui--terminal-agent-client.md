---
kind: work
description: "Multiplex prompts, approvals, events and cancellation"
status: done
needs:
  - "[[agent-loop-plugin]]"
uses:
  - usage: "[[read-usage]]"
    when: ["Routing terminal input, approval prompts, replies and agent events, especially events arriving before the start reply"]
---

# terminal-agent-client

## Do

Replace TUI-owned router history with a client of agent and sessions services over the existing socket. It chooses/creates a session, sends agent start/status/cancel/answer calls and renders agent events. It performs no provider request, tool dispatch, policy classification, transcript mutation or project instruction loading. Multiplex socket reads continuously so replies and events can interleave. Filter events by selected session and run; match replies by request ID. Keep one stdin reader and a small explicit state machine. This is line-oriented terminal UX, not a full-screen framework.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/tui/main.rs`, `plugins/tui/Cargo.toml`.

Refactor the current TUI around a single socket reader task routing replies to pending request IDs and events to the active run. At startup use an optional session argument or create one with current cwd. Each prompt starts agent and tracks returned run. Render deltas directly; render final text only when no deltas were printed for that response. Approval_requested displays tool name and bounded input summary, reads y/n, and calls agent answer with exact IDs. Ctrl-C/EOF during a run sends cancel and waits a bounded period for terminal status; second interrupt exits. Socket loss reports that remote run may continue and exits nonzero rather than pretending cancellation.

Ignore events for other sessions/runs and stale sequence numbers. Show tool start/result summaries and terminal error. Never print authorization keys, hidden system prompt or raw transcript by default. Use an in-memory fake socket server for tests; no live daemon, model credentials or PTY library. Preserve just-run behavior through coding-profile-integration rather than editing launcher here.


While start is awaiting its reply, buffer events for the selected session in a bounded queue; reconcile against returned run ID before filtering. On sequence gaps/overflow, query status including pending approval and recover persisted conversation instead of silently waiting forever.

## Check

- [x] Approval and completion arriving before start reply are buffered and rendered after run reconciliation; a sequence gap triggers status recovery.


- [x] Interleaved events and out-of-order replies route to correct pending calls while foreign session/run events remain hidden.
- [x] Streaming deltas render once; final assistant text is not duplicated.
- [x] An approval response carries exact session/run/call and y/n maps only to allow/deny.
- [x] EOF and first interrupt request cancellation; disconnect states uncertainty and returns failure.
- [x] Session selection/creation and a second prompt after done use server transcript, not local message history.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/tui/Cargo.toml
cargo clippy --manifest-path plugins/tui/Cargo.toml --all-targets -- -D warnings
```

## Result

2026-09-10 05:55 — terminal-agent-client landed 4b400ff/2380cbd (memo close on trunk); 8 tui tests green, clippy clean
