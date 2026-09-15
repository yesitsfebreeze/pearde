---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "2h"
actual: "1h — verified on lane agent-a6b3699c330ca340c at 39e77ca2 (commands_mcp.rs + mcp_recovery.rs only); just test 1502 passed; landed on main"
---

# An existing MCP session recovers daemon attachment after startup or replacement without replaying uncertain operations

## Do

Landed on main at `39e77ca2`: the session commits endpoint and client together, and the cold-start test proves late attachment, one hub move, and return to the verified socket after a failed rediscovery.

The same initialized MCP process remains usable when its daemon becomes available
late, is replaced, or is rediscovered at another valid endpoint for the pinned
root. Recovery is bounded and cancellable; failure is visible and does not demand
an agent restart. A late attachment result cannot displace a newer successful
attachment. Authentication, root ownership, and authorization are unchanged.

An operation not yet sent may proceed after recovery. An operation whose delivery
or completion is uncertain is never automatically replayed, especially a mutation
whose reply was lost. Continuity is demonstrated with one persistent adapter,
not a fresh client after each replacement. Existing listener handover and the
host's MCP reconnect lifecycle remain intact; a second general supervisor is
not the goal.

Pi's reconnect-and-reacquire behavior and the existing harness's generation-owned
reconnection are the implementation references. Current Memory reconnects per call
but discovers its endpoint only at initialization; a stale RPC client is not the
established defect. [agent-availability-errors-name-the-failed-boundary](../agent-availability-errors-name-the-failed-boundary/prd.md) owns
truthful diagnostics. [mcp-catalog-recovers-in-the-existing-session](../mcp-catalog-recovers-in-the-existing-session/prd.md) owns tool
rediscovery after connection recovery.

## Spec

Files: `src/commands/src/commands_mcp.rs`, `src/commands/tests/mcp_recovery.rs`.
Nothing under `src/transport`, `src/rpc` or `src/hub` changes.

The probe found the Do mostly landed already: commit `3001bed6` gave
`McpSession::route` per-call connect, hub rediscovery on a failed connect bounded
by `ATTACH_BUDGET` (3 s), the `operation not sent` diagnostic, and a reply loss
reported as `outcome may be unknown; not replayed`; `mcp_recovery.rs` proves
replacement at another endpoint, same-endpoint handover, the lost mutation, and
the absent endpoint against one child pid. The sentence "discovers its endpoint
only at initialization" in the Do predates that commit.

Two gaps were real, and the probe closed both on the lane branch
`agent-a6b3699c330ca340c` (worktree
`/Users/feb/dev/memory/.claude/worktrees/agent-a6b3699c330ca340c`, commit
`39e77ca2`):

1. `route` wrote `self.node` before the candidate had answered a connect, so a
   hub answer nothing listened on displaced the last verified endpoint and the
   daemon returning there was unreachable until the hub agreed. Now `reattach`
   returns `(Endpoint, MemoryRpcClient)` and the session commits both or neither;
   a timed-out or failed rediscovery is dropped whole. This is the reading of
   "cancellable" the probe settled on: the recovery future is dropped without
   side effects. The stdin loop is serial, so a host `notifications/cancelled`
   cannot interrupt an in-flight request; making it so would be the second
   supervisor the Do rules out.
2. The cold path had no proof. The child now writes `Endpoint::memory().display()`
   to `$MEMORY_DIR/own-endpoint`, and a second test starts with nothing listening:
   `initialize` answers, `health` refuses with `operation not sent`, a daemon on
   the root's own socket is reached by the same process with no hub, a hub that
   appears later moves it once, and after a failed rediscovery the daemon back at
   the verified socket is reached with no further resolve. Without the guard in 1
   the last step fails (red-proofed by reverting the guard alone).

Steps for the hand, in order, from the worktree above:

1. `cargo test -p commands --test mcp_recovery` — 3 tests pass.
2. `cargo test -p commands commands_mcp` — the in-crate MCP tests pass.
3. `just check` — fmt and clippy clean across the workspace.
4. `just test` — the workspace, per [[git-policy]] before landing.
5. Land: `just land agent-a6b3699c330ca340c`, then `just install`, then
   `memory hub stop` so the detached hub does not keep the old binary.

## Acceptance
- [x] `initialize` answers with nothing listening, and the same process reaches a daemon that arrives later on the root's own socket without a hub — `late_daemon_attaches_and_a_failed_rediscovery_keeps_the_verified_endpoint ... ok`
- [x] a hub that appears later moves the session to the endpoint it resolves, asked exactly once — same test: `health_text(&rediscovered).contains("moved")`, `resolves == 1`
- [x] a failed rediscovery keeps the last verified endpoint: the daemon back there is reached with no further resolve — same test: `contains("back")`, `resolves == 2` after the absent candidate
- [x] a call whose reply is lost is reported with `not replayed`, sends no second mutation, and triggers no discovery — `one_stdio_process_rediscovers_daemon_and_never_replays_a_lost_reply ... ok`; wording from `commands_route.rs:71` via `invoke_at`; `mutations == 1`, `resolves == before`
- [x] replacement at another endpoint and same-endpoint handover keep one child pid alive — same test: `mcp.child.id() == pid`, `try_wait().is_none()`
- [x] an absent endpoint refuses within the budget, naming the root, the previous endpoint, the candidate, and `operation not sent` — both tests: diagnostic holds `second.sock`/`moved.sock`, `absent.sock`, `root`, `operation not sent`; `ATTACH_BUDGET` 3 s
- [x] authentication, ownership and authorization paths are untouched: no diff under `src/transport`, `src/rpc`, `src/hub` — `git diff --quiet main -- src/transport src/rpc src/hub` → exit 0; lane diff is `commands_mcp.rs` + `mcp_recovery.rs` only
- [x] fmt and clippy are clean — `just check` → `Finished dev profile`, no warnings; `just test` → `1502 tests run: 1502 passed, 17 skipped`, doc tests ok

```sh
cd /Users/feb/dev/memory/.claude/worktrees/agent-a6b3699c330ca340c
git diff --quiet main -- src/transport src/rpc src/hub
cargo test -p commands --test mcp_recovery
cargo test -p commands commands_mcp
just check
```
