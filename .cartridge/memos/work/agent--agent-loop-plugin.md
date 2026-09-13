---
kind: work
description: "Drive Chat tool calls to one final answer"
status: done
needs:
  - "[[@prd/work/agent--agent-run-control.md]]"
  - "[[fs-tool-plugin-file-search]]"
  - "[[shell-tool-plugin]]"
  - "[[policy-plugin]]"
  - "[[harness-plugin]]"
  - "[[session-transcript-durability-run-checkpoint]]"
uses:
  - usage: "[[read-usage]]"
    when: ["Driving model responses through tool dispatch and back to the model, preserving tool-result IDs, or recovering incomplete tool-call groups without replay"]
---

# agent-loop-plugin

## Do

Extend the independent agent process from agent-run-control with its model driver. Run control owns start/status/cancel/answer, single-flight state, approval waiting and basic recovery; this unit owns model iteration and closing model tool-call groups. It provides agent and injects router, sessions, buffers, harness, policy and exact configured tool keys. Loader/runtime contain no agent behavior. Start is asynchronous: `start {session?,prompt,model?}` validates or creates a session, persists user/run_started records, starts one run task and promptly returns `{session,run}`. Completion arrives through correlated events and status; it is not held in the start reply. One active run per session.

The loop asks each configured tool for describe, passes descriptors to harness, prepends returned system text exactly once, calls router non-streaming, checkpoints assistant/tool records and run state through sessions, and dispatches only configured exact keys. Preserve Chat tool_call_id and multiple tool call order. Before every execution call synchronous Lua policy. For ask, the agent emits approval_requested and stores an immutable pending proposal keyed by session/run/call, then waits with timeout; answer is an agent operation and never a general Lua event. Direct socket callers remain trusted and can bypass cooperative policy by calling tool services themselves; no sandbox claim.

Cancellation is cooperative but bounded. While awaiting approval or a tool implementing exact-call cancel, request cleanup and wait; router request has no remote cancel and may finish before cancellation takes effect. No detached call result may append after terminal run state. Restart marks an unfinished run interrupted and requires an explicit new user start; never automatically replay an uncertain tool. Streaming is a later PRD. Terminal UI changes remain terminal-agent-client.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/agent/`.

Implement the non-streaming model loop. Use one configured ordered tool-key list for injections, dispatch and descriptors; reject duplicate descriptor names and model calls to absent tools. Build Chat body from harness system/messages/tools and selected model, with stream=false. Validate router responses and finish reasons. A response with tool calls is checkpointed before execution; each tool_started precedes call and tool_finished plus Chat tool message follows it. Policy denial becomes a normal error=true tool result with matching tool_call_id. Transport failures fail run; tool failures are model-visible and may continue. Multiple returned tool calls execute sequentially in response order for deterministic side effects.

Before each next model request, rebuild harness context from durable journal. Stop at configured max_steps (default 50) and max_tool_calls with failed terminal state. Final assistant text is checkpointed, then emit `{event:"agent",data:{session,run,seq,kind:"text",text}}` and done. Sequence is monotonic per run; never include provider credentials or full sensitive tool input in outward events beyond approval/tool summaries configured for the client. Fake router, fake tools, sessions and harness provide deterministic offline tests. The fake router must traverse the real process-to-host RPC path.

Port selected serial scheduling and cancellation regressions from [[deepseek-plugin-port-map]]; preserve source/license notices when adapting code. Cancellation stops new dispatch, drains started calls, records their actual outcomes, and appends matching cancelled-before-dispatch tool results for unstarted calls. A started call with unknown outcome receives an explicit interrupted-outcome-unknown tool result; this is not a rollback claim and never triggers automatic replay. On restart, close every unresolved persisted assistant tool call with one such result before a new model request. A crashed call that completed its external effect before checkpoint remains uncertain. These recovery records preserve valid Chat tool grouping so a later user turn can proceed.


For source or tests substantially adapted from [[deepseek-plugin-port-map]], include package-local UPSTREAM.md naming source paths/revision and UPSTREAM_LICENSE containing the full MIT notice; package/distribution checks must retain them.

## Check

- [x] Cancel/restart midway through multiple tools preserves completed outcomes, closes unresolved IDs without replay, and permits the next user turn with valid Chat messages.

- [x] Scripted router tool call then final answer yields ordered durable user, assistant tool call, tool result and assistant messages with preserved tool_call_id.
- [x] Configured keys alone are described and dispatched; unknown model tool names become recorded tool errors without arbitrary service calls.
- [x] Multiple tool calls execute and persist in response order; a tool error is visible to the next model request.
- [x] Malformed/router transport responses and step limits terminate once; final text and done events follow durable checkpoints.
- [x] Harness system is inserted exactly once and descriptor schemas reach Chat function parameters unchanged.
- [x] Offline integration exercises actual SDK process-to-host calls and needs no credentials.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/agent/Cargo.toml loop
cargo clippy --manifest-path plugins/agent/Cargo.toml --all-targets -- -D warnings
```

## Result

2026-09-10 — agent-loop plugin landed: durable Chat driver, tool group closing, recovery; 16 agent tests + 7-process loop suite green
