---
state: "open"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
wave: 2
date: "2026-09-15"
needs:
- "@root/host-tests-hold-under-suite-contention"
---

# One daemon serves the project and every run, launch and mcp is an instance attached to it

## Why

The intended shape is one daemon per project running every composed cartridge
once, with many instances attached to it. This covers all 20 cartridges in
`.cartridge/init.lua`, not only the host. What ran on 2026-09-15 was one full
composition per command:

- `cartridge daemon` 74584, `cartridge launch claude` 58681 and
  `cartridge run memory …` 78693 each had their own socket directory under
  `/tmp/cartridge-501/69a3b8e0c7a1/`, and each started a node for every
  cartridge.
- Up to three `cartridge daemon` processes ran on the project at once, and
  `cartridge run` costs about 15 seconds of full composition start.
- Memory takes a single-writer lock (`store::lock::acquire`). The first host
  wins, and every other host's memory fails with `another memory writer holds
  this data dir`, including its ledger appends. Attached memory is read-only.
- Another session's lsp tests run `pkill -f "cartridge daemon"`, which killed
  the daemon condensing the ledger at 13:58. A shared daemon needs a stop path
  that tests and tools use instead.

## Findings (cartridge.ctg, 2026-09-15)

Attach-first exists, but every failure quietly starts a full composition:

- `run`, `launch` and `mcp` try `host.sock` first (`src/cli/host.rs:65`,
  `:89-91`, `:150-163`). `client::served` turns every connect or auth error into
  `None` (`src/cli/client.rs:44-46`), which starts their own composition
  (`host.rs:72-74`, `:98-110`; `src/host/run.rs:23-59`).
- A second `daemon` never checks for a first one. The bind returns
  `AlreadyRunning`, which it only logs, then keeps running with no nodes
  (`host.rs:240-269`; `src/transport/typed.rs:902-916`).
- `unpublish` deletes `host.sock` without checking ownership
  (`src/host/mod.rs:106-112`, `:567-569`). Any fallback host or losing daemon
  that exits removes the real daemon's socket path, and every later command
  starts its own composition. This is the main cause of the many compositions.
- Nothing in cartridge.ctg starts a daemon. `live.ctg/src/launch.ts:46-52`
  spawns `--yolo daemon` undetached when `status` fails.
- Profile edits reload nodes (`src/host/watch.rs:41-52`), but a rebuilt native
  module does not (`src/node/mod.rs:363-396`).
- mcp keeps one `session` and one `inflight` map per node
  (`mcp.ctg/src/service.rs:88-92`), so attached stdio clients would share one
  session today.

## Per-cartridge audit (2026-09-15, first pass)

**Must exist once per project.** Each of these breaks when two compositions
run on one project:

- **memory**: `writer.lock`. Every call on the second host fails.
- **sessions**: loads its store into memory once (`lib.rs:261`). The last rename
  wins, and buffer ids come from a counter in each process.
- **live**: marks in-flight tasks `interrupted` at start
  (`coordinator.ts:30-38`), which kills the other host's work.
- **prd**: the job journal shows the other host's jobs as `interrupted`, and the
  memory outbox is replayed twice (`service.ts:127`, `:176`).
- **router**: the OAuth refresh lock only works inside one process
  (`auth.rs:282`), so both hosts spend the same refresh token.
- **agent**: its single-flight guard only works inside one process, so two
  hosts can drive one session and overwrite its transcript.

**Belong with an instance, keyed inside the shared cartridge:**

- pty shells
- agent runs
- mcp stdio and in-flight calls. mcp keeps one session per node today.
- proxy continuations
- lsp servers, with an install lock that only works inside one process
- live connections
- auth sockets

**Safe to share as-is:**

- memo (file lock)
- fs refs (file locks)
- live-record (SQLite WAL)
- docs, policy and harness (no state)
- tools (cargo lock)

`gitfs.ctg` is not composed, because `fs.ctg` carries the same code.
`live/main.ts:9` hardcodes credential paths under `cartridge.ctg`.

## Outcome

One project has at most one daemon, and it runs each composed cartridge
exactly once. `run`, `call`, `launch` and `mcp` are instances. Each one:

- finds the daemon through the project's `host.sock`, or starts it when none
  answers;
- sends its events there;
- never starts nodes of its own.

Project-scoped state exists once, in the daemon. That covers stores and locks
(memory, sessions, gitfs, prd, docs), bound ports (router, proxy listener,
live), credentials (auth) and long-lived children (lsp servers). State that
belongs to one instance is keyed by that instance inside the shared cartridge:
a session, a pty shell, an agent run, an MCP stdio client, a launched worker's
proxy identity. It is never duplicated by starting another node.

## Analysis first

Split this with `prd refine` into same-board children before any
implementation. Done 2026-09-15; the children are:

1. **Host attach.** `an-instance-attaches-to-the-daemon-and-never-composes-silently`
   (cartridge.ctg): the attach/auto-start contract, socket exclusivity, second
   daemon refuses, `unpublish` ownership, one documented stop command.
2. **Per-cartridge children.** One per cartridge that breaks under many
   attached instances — memory (writer lock), sessions (store + buffer-id
   space), mcp (one session/inflight per node), router (OAuth refresh lock),
   live (spawns its own daemon; interrupted-marking), prd (journal + outbox
   replay), agent (single-flight guard) — each needs the host-attach child
   first.
   The audit's safe-to-share cartridges (memo file lock, fs refs, live-record
   WAL, docs, policy, harness, tools) and per-instance-keyed pty shells, auth
   sockets and lsp servers get no child: they need no change for the one
   daemon, unless the composed test disproves that.
3. **The composed test.**
   `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`
   (cartridge.ctg): this PRD's Acceptance made runnable; needs all children.

## Open questions

- `launch` keeps its agent process and tmux window. Does its proxy listener
  stay in the daemon, with the agent pointed at the daemon's proxy address?
- `run` for a solo host (`verify_one`) and a test host: do they stay
  self-contained, so gates never depend on a developer's live daemon?

## Acceptance

- [ ] With a daemon running, `cartridge run memory '{"op":"status"}'` answers
      without starting any node process (count `cartridge node` children before
      and after).
- [ ] Two `cartridge launch` instances and one `cartridge mcp` leave exactly
      one `cartridge daemon` and one node per composed cartridge.
- [ ] A memory `ingest` from one instance is returned by `query` from another,
      with no writer-lock error; two instances' sessions and pty shells stay
      separate.
- [ ] With no daemon running, two instances started concurrently end up
      sharing one daemon.
- [ ] Stopping the daemon uses one documented command, and no test kills
      daemons by process name.
