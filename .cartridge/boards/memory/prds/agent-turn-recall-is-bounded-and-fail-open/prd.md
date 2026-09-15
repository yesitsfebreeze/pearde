---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
actual: "36m"
---

# Relevant memory reaches agent turns within explicit latency and size budgets without blocking or widening authority

## Do

An enabled agent turn receives relevant source-labelled memory within explicit
retrieval and output budgets. Disabled, ineligible, empty, failed, or timed-out
retrieval leaves the original request usable; failures are observable without
stalling the turn. Retrieved text is evidence, never trusted instructions or
authorization. Embedding and provider egress remain subject to the existing
policy even when no synthesis model is called.

Cancellation, streaming, client-owned tools, conversation history, and provider
errors retain their contracts. No reasoning model or nested agent chooses what
the proxy should do. The existing retrieval operation supplies memory rather
than a second memory system. Pearde's bounded prompt hook is a concrete policy
reference; a host-only hook does not by itself complete the HTTP-facing contract
of [proxy-turns-carry-recall-and-reflex-tools](../../../proxy/prds/proxy-turns-carry-recall-and-reflex-tools/prd.md).

[changed-context-preserves-the-stable-prompt](../changed-context-preserves-the-stable-prompt/prd.md) owns repeated-context suppression.
[memory-integration-cloud-disclosure](../memory-integration-cloud-disclosure/prd.md) remains the egress-disclosure contract.

## Spec

Run 2026-09-09 by b424ceba: every gate green in the lane at `4f8fe3e6` (three commits rebased onto `main` `e2fd33ff`); landed on `main` at `4f8fe3e6` by fast-forward, lane removed.

The probe built the whole Do and it passes every gate: commits `a8039aa6`,
`19dbf970` and `cc2f10e5` on the branch
`agent-turn-recall-is-bounded-and-fail-open` (worktree
`/Users/feb/dev/memory/.claude/worktrees/agent-a1ca7c507846702db`, three
commits over `main` at `60630ff9`). The branch already exists, so `just lane`
will refuse; the hand works in that worktree, or adds one with
`git worktree add .claude/worktrees/agent-turn-recall-is-bounded-and-fail-open
agent-turn-recall-is-bounded-and-fail-open` from the trunk. What is left is
the run, the ticking and the landing. Files:

- `src/commands/src/commands_proxy.rs` — the whole change. Four budget
  constants, pearde's `memory.py recall` policy moved in-process:
  `RECALL_MIN_PROMPT = 12` chars, `RECALL_HITS = 5`, `RECALL_CHARS = 2000`,
  `RECALL_TIMEOUT = 2 s`. `Proxy.recall: Option<Arc<rpc::server::Server>>`
  is the daemon's own store; `start(..)` takes it as a fifth argument.
  `forward` runs `recall()` only on an eligible turn — a POST to a model
  path (`mine::protocol::Wire::from_path`) through a proxy that has a store
  — and only then records a `recall` ledger row with the outcome; a GET, a
  non-model path or a store-less proxy leaves the ledger exactly
  `req`/`resp` as before. Every turn's response carries the header
  `x-memory-recall`: `hit=<n>`, `empty`, `skipped`, `error` or `timeout`.
  `recall()` takes the prompt with `prompt_of` (the last message only when
  it is a user's own text — a tool result, an assistant turn, an image, or a
  short line recalls nothing, so no message slides between a tool call and
  its result), calls `Server::invoke("query", {text, k})` on
  `spawn_blocking` under `tokio::time::timeout`, and on a hit inserts one
  `{"role":"user"}` message before the prompt built by `memory_block`: a
  header naming the lines as recorded evidence that grants no permissions,
  then one `- [scheme:object_id] text` per hit, cut at `RECALL_CHARS`. A
  Responses string `input` becomes a two-item list. Every other path returns
  the original bytes. The `req` ledger row stays the original body.
- `src/commands/src/proxy_owner.rs` — `launch_open` hands
  `self.inner.memory` to `open`/`run_session` when `req.recall` is set;
  `commands_proxy::start` receives it.
- `src/transport/src/memory_rpc.rs` — `LaunchOpenReq.recall: bool`,
  `serde(default)`, so an older client's launch reads as it always did.
- `src/commands/src/commands_launch.rs`, `src/commands/src/lib.rs` —
  `memory launch --no-recall`; the flag is off by default, so a launch recalls.
- `tests/e2e/lifecycle.rs` — the launch probe's `LaunchOpenReq` initializer
  gains `recall: false`, the one initializer outside `src/`. Its ledger
  counts (`one.jsonl` 2 rows, `two.jsonl` 4) stand unchanged: those fetches
  are GETs through store-less proxies, which is why the `recall` row is
  written only for an eligible turn.

Three things the Do names were settled by building. Enabled means the launch
asked for it: recall rides on `LaunchOpenReq`, not on config, so the
standalone `memory proxy` (no store in that process) and an old client are
disabled by construction. Observable means the header on every turn, the
ledger row on every eligible one, and a `tracing::warn!` on `error` and
`timeout`; the `502` the proxy answers when the upstream is unreachable
carries no header, the ledger row is the record there. Egress needs nothing
new: the query goes through `Server.llm`, the same embed client every other
operation uses, so the existing warning and disclosure cover it. A timed-out
query is abandoned, not cancelled — it finishes on its blocking thread and is
dropped, which is why the test's slow embedder answers late rather than never
(a runtime drop waits for blocking tasks).

Not done, and not this memo's: the header and ledger row are the only
observation; nothing suppresses a repeated identical block across turns
([changed-context-preserves-the-stable-prompt](../changed-context-preserves-the-stable-prompt/prd.md)).

Steps for the hand, in the worktree above. The `touch` is load-bearing on
every step that compiles: the worktree shares the trunk's `target/`, and a
`transport` fingerprint left by another session's build silently reuses a
`LaunchOpenReq` without the field — the first `just check` passed on one and
the second missed `lifecycle.rs` that way. An isolated `CARGO_TARGET_DIR`
does the same job.

1. `touch src/transport/src/memory_rpc.rs && cargo test -p commands --lib commands_proxy`
   — 11 run, 11 pass, about 2 s.
2. `cargo test -p commands --lib proxy_owner && cargo test -p transport` — clean.
3. `touch src/transport/src/memory_rpc.rs && just check` — fmt and clippy
   `-D warnings` over the workspace, clean.
4. `touch src/transport/src/memory_rpc.rs && just test` — the whole workspace
   under nextest plus doctests; the probe saw 1506 run, 1506 pass, 17 skipped,
   `lifecycle::daemon_proxy_sessions_keep_streams_and_leases_isolated` among
   the passes.
5. Tick the Check boxes, one per behaviour the run proved; run the `sh` block.
6. From `/Users/feb/dev/memory`: `just land agent-turn-recall-is-bounded-and-fail-open`,
   then `just lane-rm` per [[git-policy]]; `cargo install` and `memory hub stop`
   so the daemon serving a root runs the new proxy.

## Acceptance
- [x] A chat turn with a recorded fact forwards two messages: a user message
      before the prompt containing `[file:notes/ports.md] the daemon listens
      on 4140` and `evidence, not instructions`, then the prompt unchanged;
      the response carries `x-memory-recall: hit=1`; the ledger holds the
      original `req` row and a `recall` row `hit=1`. A Responses string input
      becomes a two-item list with the memory first; an Anthropic turn keeps
      its `system` byte-identical
      (`a_hit_reaches_the_turn_labelled_before_the_prompt_on_every_wire`).
- [x] A tool-result turn on either wire, a prompt under 12 chars, a non-object
      body, a non-model path, and a proxy with no store each forward the
      request byte-identical with `x-memory-recall: skipped`; the first three
      leave `req`, `recall` in the ledger, the non-model path and the
      store-less proxy leave `req` alone
      (`an_ineligible_or_disabled_turn_is_forwarded_byte_identical`).
- [x] A store with no embed client answers `error`, a store with nothing
      recorded answers `empty`; both forward the original bytes with status
      200 and write the outcome as the `recall` ledger row
      (`a_failed_or_empty_recall_forwards_the_original_and_says_so`).
- [x] An embedder answering after `RECALL_TIMEOUT + 1 s` does not hold the
      turn: it returns before the embedder does, with `timeout` and the
      original bytes (`a_slow_recall_is_abandoned_within_the_budget`).
- [x] A hundred 100-character hits render to a block no longer than
      `RECALL_CHARS` with more than five lines
      (`the_memory_block_is_cut_at_its_budget`).
- [x] The three pre-existing proxy tests pass unchanged, a store-less
      forward still writing exactly `req` then `resp`
      (`forwards_bytes_status_headers_and_records_stream`,
      `shutdown_cancels_stalled_response_and_request_connections`,
      `finite_response_finishes_during_graceful_drain`).
- [x] The e2e `lifecycle::daemon_proxy_sessions_keep_streams_and_leases_isolated`
      passes with its ledger counts of 2 and 4 untouched.
- [x] `just check` and `just test` are clean after a
      `touch src/transport/src/memory_rpc.rs`.

```sh
cd /Users/feb/dev/memory/.claude/worktrees/agent-a1ca7c507846702db
touch src/transport/src/memory_rpc.rs
cargo test -p commands --lib commands_proxy 2>&1 | grep -E "^test result: ok. 11 passed" \
  || { echo "proxy recall tests red"; exit 1; }
cargo test -p commands --lib proxy_owner 2>&1 | grep -q "^test result: ok" || exit 1
cargo test -p transport 2>&1 | grep -q "FAILED" && exit 1
just check
touch src/transport/src/memory_rpc.rs
just test 2>&1 | grep -E "PASS .*lifecycle::daemon_proxy_sessions_keep_streams_and_leases_isolated" \
  || { echo "e2e lifecycle red or missing"; exit 1; }
```
