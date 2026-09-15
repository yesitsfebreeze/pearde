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
actual: "1h"
---

# Agent availability errors distinguish an unreachable endpoint from a missing daemon and retain the connection cause

## Do

An agent can distinguish discovery failure, missing endpoint, refused connection,
startup, draining, and an operation failure without being told to start another
daemon merely because a connection failed. The pinned root, selected endpoint,
generation when known, and underlying cause remain visible without exposing
credentials. Authentication and ownership refusals remain explicit refusals.

The 2026-09-09 observation established a running daemon process without an
observed conventional listener, not that reload caused the outage. Endpoint
selection overrides and the actual startup phase remain unknown. The diagnostic
must not turn either hypothesis into fact. Existing fast readiness from
[memory-integration-fast-readiness](../memory-integration-fast-readiness/prd.md) remains independent of graph locks.

This is the diagnostic counterpart of [mcp-attachment-recovers-without-replaying-work](../mcp-attachment-recovers-without-replaying-work/prd.md).

## Spec

Files: `src/commands/src/commands_route.rs` (the classifier and the payload),
`src/commands/src/commands_mcp.rs` (the session's discovery note, generation,
and the composed diagnostic), `src/commands/src/commands_plan.rs` and
`src/commands/src/commands_hub.rs` (the two CLI printers),
`src/commands/src/tests/commands_mcp_test.rs`, and `tests/e2e/focus_routing.rs`
(the pulse e2e asserts the new wording). Eight further files under
`src/commands/src/` carry only the mechanical `Routed::NoDaemon =>` to
`Routed::NoDaemon(_) =>` arm. Nothing under `src/transport`, `src/rpc` or
`src/hub` changes: the boundaries were already distinct on the wire
(`AdapterError::Io` with `NotFound` or `ConnectionRefused`, `Unauthenticated`,
`UntrustedEndpoint`; the daemon's own `shutting down:` refusal; `ready`'s `pid`),
and the whole defect was that the client folded them into one string.

The probe is on lane branch `agent-a4f92304e4f1ab0fd` (worktree
`/Users/feb/dev/memory/.claude/worktrees/agent-a4f92304e4f1ab0fd`, commits
`4601877a` and `e6741889`, rebased on main `39e77ca2`) and did all of the
following:

1. `commands_route::connect_failure(endpoint, &AdapterError)` renders one
   boundary per error: `no listener at E for root R: the socket is absent (…)`
   for ENOENT; `connection refused at E for root R: the socket is present but
   nothing accepts (…)` for ECONNREFUSED; `authentication refused by the daemon
   at E` and `endpoint E … refused by this client before speaking` for the two
   refusals. The unreachable pair say what a daemon process *may* be doing
   (starting, binds after bootstrap; exited without unlinking) and assert
   nothing, and no string carries `memory daemon`. `pinned_root()` is `MEMORY_DIR`
   when set, else the cwd, because `Endpoint::memory` tags the socket by it.
2. `Routed::NoDaemon(String)` carries that account. The sixteen fall-back
   callers ignore it as before; `memory plan` and `memory pulse` print it, and the
   pulse hint now says to look for a daemon process before starting another.
3. `invoke_at` takes `generation: Option<u64>` and an operation failure reads
   `operation <name> failed on the daemon for root R at E (last attached daemon
   pid P): …; operation outcome may be unknown; not replayed`. A daemon's own
   refusal — including `shutting down: the daemon refused this request` while
   draining — still crosses verbatim as `Routed::Refused`.
4. `McpSession` keeps `discovery` (the hub's answer with `spawned`, or `no hub
   at H (auto_start b); conventional endpoint E for MEMORY_DIR=… | the cwd`, or the
   3 s give-up) and `generation` (the `pid` of any `ready`/`health` answer;
   `refresh` asks `ready` first and stops there when nothing accepted, so a
   missing daemon costs one attach). A connect that fails after rediscovery
   returns `Routed::NoDaemon` reading `<first>; discovery: <how the standing
   endpoint was chosen>; rediscovery: <candidate's discovery>; <candidate's
   connect failure or the 3 s give-up>; last attached daemon pid P | no daemon
   generation known to this session; operation not sent: <name>`. The candidate
   becomes the node only after it answered a connect: main's `reattach` from
   [mcp-attachment-recovers-without-replaying-work](../mcp-attachment-recovers-without-replaying-work/prd.md) (`39e77ca2`) is kept as
   the commit-together helper and returns `(Attached, MemoryRpcClient)`, its
   failure carrying the candidate's discovery plus `connect_failure`.
5. Tests: `a_missing_socket_is_no_daemon_not_an_error` (rewritten),
   `a_stale_socket_is_refused_connection_not_a_missing_endpoint`,
   `a_draining_daemon_is_a_refusal_that_says_so` in `commands_route`;
   `a_failed_connect_names_every_boundary_and_never_says_start_one` and
   `a_failure_after_attachment_names_the_generation_last_heard_from` in
   `commands_mcp_tests`, both under a scratch `XDG_RUNTIME_DIR` so no machine
   hub or daemon is touched. `mcp_recovery` still passes unchanged: it asserts
   the literal `operation not sent`, which is why the name follows a colon.
6. `tests/e2e/focus_routing.rs::pulse_fails_loudly_with_no_daemon` asserts
   `no listener at ` — the one assertion anywhere on the old
   `no daemon is serving this store` line, found by `just test`, which was the
   first run of the whole workspace against the change.

Nothing is left to build. Steps for the hand, from the worktree above:

1. `cargo test -p commands --lib` — 140 pass. If `commands` fails to compile
   with a field missing on a `transport` type, the shared `target/` served
   another lane's rlib (workspace members hash by path relative to the
   workspace root, and every lane shares `/Users/feb/dev/memory/target`):
   `find src/transport -name '*.rs' -exec touch {} +` and rerun. The same
   applies to the `memory` binary before step 3.
2. `cargo test -p commands --test mcp_recovery` — passes.
3. `touch src/main.rs && cargo build --bin memory`, then the two hand runs in the
   Check against an isolated `MEMORY_DIR`. The binary is the shared
   `/Users/feb/dev/memory/target/debug/memory`, never a `target/` under the
   worktree; the endpoint printed is tagged by that root and collides with no
   daemon.
4. `find src tests -name '*.rs' -exec touch {} + && just test` — the whole
   workspace under nextest plus doc tests, every binary rebuilt from this lane (a bare `just test` twice ran another lane's e2e binary and reported tests this tree does not have); 1512 passed at
   `e6741889`. Then rebase onto main once its own `src/extension/src/plugin.rs`
   fmt fix lands and `just check` is clean, then land and `just install`, then
   `memory hub stop`.

Out of the Do and not touched: `attach` resolves the hub with the cwd while
`Endpoint::memory()` and `pinned_root()` honour `MEMORY_DIR`, so under `MEMORY_DIR` the
hub is asked about a different root than the socket is tagged by.

Landed on main at `d057b368` (three commits fast-forwarded over `4f8fe3e6`; `just check` clean, `just test` 1518 passed in the lane), lane removed.

## Acceptance
- [x] an absent socket is `Routed::NoDaemon` whose text starts `no listener at`, names the endpoint and the pinned root, keeps the io cause, and contains no `memory daemon`
- [x] a socket file nothing accepts is `Routed::NoDaemon` whose text starts `connection refused at` and says the socket is present — never reported as absent
- [x] a draining daemon's `ask` comes back `Routed::Refused` containing `shutting down`, not as an absence
- [x] a daemon tool error is still `Routed::Refused`; the `Unauthenticated`/`UntrustedEndpoint` arms are unchanged and never followed by rediscovery
- [x] an MCP call with nothing listening and no hub answers `isError: true` with `no listener at` for both endpoints tried, `rediscovery: no hub at … (auto_start false)`, `conventional endpoint`, `no daemon generation known`, and `operation not sent: <name>`; no `memory daemon`, `start it`, `start one`
- [x] after `refresh` against a serving daemon the session's `generation` is that daemon's pid, and a later failure names `last attached daemon pid <pid>`
- [x] a hub that never answers still leaves `initialize` on the conventional endpoint, with the give-up kept in `discovery`
- [x] `mcp_recovery` passes unchanged
- [x] the pulse e2e `pulse_fails_loudly_with_no_daemon` fails with exit 1 and `no listener at ` on stderr
- [x] `memory plan` under an isolated `MEMORY_DIR` prints `no listener at` with no socket and `connection refused at` with a stale one, exit 1 both times
- [x] no diff under `src/transport`, `src/rpc`, `src/hub`; fmt and clippy clean

```sh
cd /Users/feb/dev/memory/.claude/worktrees/agent-a4f92304e4f1ab0fd
git diff --quiet main -- src/transport src/rpc src/hub
cargo test -p commands --lib -- commands_route::tests commands_mcp_tests
cargo test -p commands --test mcp_recovery
cargo nextest run -p memory --test e2e pulse_fails_loudly_with_no_daemon
touch src/main.rs && cargo build --bin memory
memory=/Users/feb/dev/memory/target/debug/memory
root=$(mktemp -d)/root && mkdir -p "$root"
env MEMORY_DIR="$root" "$memory" plan 2>&1 | grep -q '^memory plan: no listener at '
sock=$(env MEMORY_DIR="$root" "$memory" plan 2>&1 | sed -n 's/^memory plan: no listener at \([^ ]*\) .*/\1/p')
python3 -c "import socket,sys; s=socket.socket(socket.AF_UNIX); s.bind(sys.argv[1]); s.close()" "$sock"
env MEMORY_DIR="$root" "$memory" plan 2>&1 | grep -q '^memory plan: connection refused at '
rm -f "$sock"
cargo fmt -p commands -- --check && cargo clippy -p commands --tests
find src tests -name '*.rs' -exec touch {} + && just test
```
