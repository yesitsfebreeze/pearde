---
repo: /Users/feb/dev/cartridge/agent.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
needs:
- "@agent/agent-loop-plugin"
---

# Parse fragmented SSE and release routing sessions

## Do

Extend only the separate agent plugin. Acquire `{key,base}` with `router {op:"session",routing?}` per run and POST `${base}/v1/chat/completions` using `Authorization: Bearer <key>`, stream=true. Parse Chat SSE incrementally; release key on success, failure, cancellation and disposal. Never write credentials to logs, events or transcript.

Emit correlated text deltas as visible provisional output and assemble one complete assistant message, including fragmented tool calls. Persist that message only after a valid terminal stream; execute no tool until assembly validates. If failure occurs before any response bytes become visible and before any tool call, one fresh streaming retry may use a new router session within configured attempt limit. After any visible delta or tool-call fragment, do not automatically replay. Emit stream_error and fail the run, preserving a diagnostic lifecycle record but no incomplete assistant message. Client prints deltas and does not print final text twice. No streaming tool output.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/agent/`.

Add streaming HTTP to agent using already-installed reqwest. Build an incremental SSE parser supporting arbitrary network chunk boundaries, CRLF/LF frames, comments and multiple data lines; recognize [DONE]. Bound one event and assembled response. Parse Chat delta choices and accumulate content plus tool calls by choice/index while preserving provider call IDs and concatenating function argument fragments. Reject invalid UTF-8/JSON, unexpected indices, conflicting names/IDs, incomplete JSON arguments, missing terminal marker and unsupported multiple choices. Do not dispatch during parsing.

Emit each content fragment with monotonically increasing seq and provisional=true. On complete validation checkpoint one assistant response and continue existing sequential tool execution. Cancellation closes response and releases credentials. Maintain a guard that releases exactly once on all return paths. Before-visible failure retry is capped at one and obtains/releases a distinct key; after-visible failure never calls router request or replays. Tests use local fake HTTP and fake router service, inspect Authorization without retaining its value.

## Acceptance
- [x] Fragmenting every SSE byte boundary still produces identical deltas and assembled text/tool arguments.
- [x] Interleaved indexed tool fragments assemble correctly and execute only after valid [DONE]; malformed/incomplete streams execute nothing.
- [x] Routing base comes from session response, Bearer key is sent, and release occurs exactly once on success/error/cancel/disposal.
- [x] A pre-visible disconnect retries at most once; a post-delta disconnect emits stream_error and performs no retry or transcript assistant append.
- [x] Event seq/session/run are stable and credentials never appear in recorded outputs.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/agent/Cargo.toml streaming
cargo clippy --manifest-path plugins/agent/Cargo.toml --all-targets -- -D warnings
```

## Result

2026-09-10 06:15 — streaming-agent-output landed 711a795/0c8221b/662b7ce (memo close on trunk); 16 lib + 12 loop + 5 streaming tests green
