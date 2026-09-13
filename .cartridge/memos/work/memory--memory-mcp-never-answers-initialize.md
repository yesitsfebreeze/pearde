---

kind: work
level: 10
status: done
estimate: 4h
description: "`memory mcp` answers no JSON-RPC `initialize` for at least 30 s because `cmd_mcp` attaches to the hub before it reads stdin, and that attach has no timeout — every `mcp__memory__*` tool is unavailable to the agent host."
read_when: approving or running the bounded investigation into the unanswered memory MCP handshake
---

# memory-mcp-never-answers-initialize

## Do

Approved 2026-09-08 as "Approve + allow the fix" [[approve-memory-mcp-handshake-investigation]]. The measurement below is authorized, and so is the fix it points to — a timeout on `hub.resolve`, answering `initialize` before attaching, or a hub-side repair — in the same run, without a second approval.

Observed defect, measured 2026-09-08 in `/Users/feb/dev/memory` on macOS 25.2.0, `memory 2.0.0` at `/Users/feb/.cargo/bin/memory`, code revision `36d6def6`. The agent host reported `memory (CONNECT_TIMEOUT): "MCP server memory connection timed out after 30000ms"`, so `mcp__memory__query` (required by [[@prd/routine/plan-cartridge-work.md]] step 1) and `mcp__memory__routine_self-improve` (the primary path of every `.agents/skills/*/SKILL.md` after [[one-skill-file-per-routine-under-two-harness-names]]) were both unreachable and this run used the documented fallback. Reproduced read-only outside the host: a single valid `initialize` line piped into `memory mcp` produced 0 bytes on stdout and 0 bytes on stderr over 30 s, with a hub already running (`memory hub --idle-exit-secs 300`, started 09:23).

The blocking site is visible in source but its cause is not established. `cmd_mcp` (`src/commands/src/commands_mcp.rs:81-83`) awaits `attach(cfg)` before it constructs the stdin reader, so no message is read until the attach returns; its doc comment states that ordering deliberately. Inside `attach` (`:108-127`), `connect_hub_or_start` (`src/commands/src/commands_hub.rs:332-363`) is bounded — one connect, then at most six 150 ms retries — while `hub.resolve(ResolveReq { root })` is awaited with no timeout and no fallback to `Endpoint::memory()` on a slow answer. That an unbounded `resolve` is what hung here is a hypothesis reached by elimination, not a measurement.

Scope of the proposed run: measure only. Time `connect_hub_or_start` and `hub.resolve` separately for this root with the smallest read-only means (a tracing-level run of `memory mcp`, or `memory hub status` and a direct hub `resolve` probe), record which await does not return and what the hub is doing while it does not, and land the finding as one memo. Then apply the fix that measurement names — a timeout on `resolve`, answering `initialize` before attaching, or a hub-side repair — in a lane per [[git-policy]]. The measurement is written down before the fix lands, so the record shows which await hung and why that fix followed.

Benefit: the whole declared MCP surface — `routine:<leaf>`, `query`, `reflex` — is currently unusable from an agent host, and the reflex ledger records nothing while it is ([[every-routine-and-persona-scores-zero-in-this-repos-ledger]]). Tradeoff: the fix is authorized before its shape is known, so the run must state the measurement that chose it. Preserve what works: `just memo <leaf>` resolves a leaf correctly, and each SKILL.md fallback line carried this run to completion without the daemon — that fallback must not be removed by whatever fix lands. The memos repository is dirty with another session's compaction and none of its files are owned here.

## Check

Already run, 2026-09-08: `( printf initialize-request; sleep 30 ) | memory mcp` wrote 0 bytes to stdout and 0 bytes to stderr; `ps` showed `memory hub --idle-exit-secs 300` alive as pid 19788 throughout. Repeat it as the reproduction; require either an `initialize` result within 5 s, or the same silence confirming the defect still stands. Confirmed again at 10:45 the same day from a restarted agent session: the host reported the identical `CONNECT_TIMEOUT` after 30000 ms with the same hub still alive, so the failure survives a client restart and is not one session's stuck process.

Unrun: the per-await timing that names which of `connect_hub_or_start` and `hub.resolve` does not return, and a one-line record of the hub's state during it. Then, after the fix: one valid `initialize` piped into `memory mcp` answers within 5 s, an agent host reaches `mcp__memory__query`, and `just check` and `just test` pass in the lane before it lands.

Run `just memos-check` once after the finding memo lands and require success. A green memo gate does not prove the measurement; the timing observation above is required.

Ran 2026-09-08. The measurement landed as [[the-hub-waits-sixty-seconds-for-a-node]]: `connect_hub_or_start` returns in 179 µs warm and 198 µs cold, `hub.resolve` in 1.2 ms warm and 259 ms against an empty cold root, so `resolve` carries the whole cost and its ceiling is the hub's own 60 s readiness loop — twice the host's 30 s. The fix is one bound at the caller with the shorter deadline: `ATTACH_BUDGET` of three seconds around `attach` in `src/commands/src/commands_mcp.rs`, falling back to `Endpoint::memory()`, with `a_hub_that_never_answers_does_not_hold_the_handshake` in `src/commands/src/tests/commands_mcp_test.rs` holding it. One valid `initialize` piped into the built binary answered in 0.257 s with 975 bytes of instructions; `just check`, `just memos-check` and the mcp suite pass in the lane; `just test` carries one red this lane did not cause and cannot fix inside its `Do` — `declared_dependencies::the_workspace_catalogue_lists_nothing_no_member_inherits`, because `extension` entered `[workspace.dependencies]` in `7b4df428` with no member inheriting it. It reproduces on `main` with this lane's two files reverted. The SKILL.md fallback lines are untouched. One clause of the Check is unverifiable from inside a running session — an agent host reaches `mcp__memory__query` only after `just install` and a host restart, which no session can do to itself; the next session that starts against the installed binary is the witness.
