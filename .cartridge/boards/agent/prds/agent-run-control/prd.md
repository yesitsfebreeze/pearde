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
- "@root/process-plugins-register-through-lua-lua-registration"
- "@sessions/session-transcript-durability-run-checkpoint"
- "@policy/policy-plugin"
- "@fs/fs-tool-plugin-file-search"
---

# Single-flight run lifecycle, approvals and cancellation

## Do

Create the independent `plugins/agent/` process and Lua wrapper providing agent, with sessions/buffers/policy injected. Own single-flight starts, durable run IDs, approval state, cancellation and interrupted-run recovery. This is the first bounded slice of the agent plugin, not a new run-control plugin or registry. Model iteration lands in agent-loop-plugin. During this slice tests inject a fake run driver; production start reports loop_unavailable until the model driver exists, never silently completes a prompt. Preserve the API and lifecycle semantics in the first specification below.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/agent/`, `plugins/agent.lua`, `Cargo.toml`, `Cargo.lock`.

Build an agent process with a per-session task map and run IDs derived from session ID plus its next checkpoint revision; the revision-checked initial checkpoint guarantees uniqueness across restart without a random-ID dependency. Validate model/prompt limits before checkpoint. Concurrent start handlers synchronize claim plus initial checkpoint; a losing start fails without appending a user message. Subscribe to nothing for approvals: expose `answer {session,run,call,decision}` on agent. Accept allow/deny only once for an exact pending immutable request. Timeout defaults to 300 s and denies. Late, duplicate, mismatched and post-cancel answers cannot authorize another call.

Implement status with running/awaiting_approval/terminal phase, current step and last durable error. Cancel sets token idempotently, denies pending approval and calls tool cancel for an active cancellable call. The run task reaches exactly one completed, failed, cancelled or interrupted terminal checkpoint before its done/error event. On startup inspect session agent state; persist interrupted for unfinished prior runs, with no tool invocation. Avoid holding map/session locks across RPC awaits.


Status includes the immutable pending approval (when present) so clients recover a missed event. Missing/unloaded policy refuses dispatch; it never defaults to allow. Lifecycle APIs use start {session?,prompt,model?}, status/cancel {session,run?}, answer {session,run,call,decision}; start returns {session,run} after the initial checkpoint. Run-control tests use a fake driver; production start fails loop_unavailable until the model driver is installed.

For source or tests substantially adapted from [[deepseek-plugin-port-map]], include package-local UPSTREAM.md naming source paths/revision and UPSTREAM_LICENSE containing the full MIT notice; package/distribution checks must retain them.

## Acceptance
- [x] Concurrent starts for one session produce one run and one error with one durable user/run_started pair.
- [x] Approval is bound to exact session/run/call/input; allow executes once while deny, timeout, stale and duplicate answers execute zero times.
- [x] Cancel while awaiting approval finishes cancelled; cancel during a fake cancellable tool invokes exact-call cancel and prevents late transcript append.
- [x] Restart converts a saved unfinished run to interrupted without calling its pending tool; a new prompt can start afterwards.
- [x] Every run emits correlated events only after matching checkpoints and reaches one terminal state.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/agent/Cargo.toml run_state
cargo clippy --manifest-path plugins/agent/Cargo.toml --all-targets -- -D warnings
```

## Result

2026-09-10 — agent-run-control landed 9db3432/24a8683/5cbbcac; 5/5 checks, 8 run_state tests + clippy green
