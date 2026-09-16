---
complexity: small
footprint:
  - cartridge.ctg
  - cartridge.ctg/src/cli/client.rs
  - cartridge.ctg/src/cli/host.rs
  - cartridge.ctg/src/host/mod.rs
  - cartridge.ctg/src/host/socket.rs
  - cartridge.ctg/src/host/watch.rs
  - cartridge.ctg/docs/development.txt
  - cartridge.ctg/README.md
  - .cartridge/tests/integration/takeover.test.ts
---

# spec01 — `run` attaches through the swap, a losing daemon exits, a daemon outlives no project

Revision 3 (round 1: B1 smoke dropped, B2 swap-tolerant attach, B3
project-gone exit, N1–N6; round 2: B1 directory-only two-miss tick, B2
`--replace` exit-0 only after staging, N1–N3).

Base: cartridge.ctg cdd3124 (after d840064 "One host per project"). Already
delivered there: `call`/`send`/`status`/`stop` talk only to `host.sock`;
`launch`/`mcp` go through `host::attach` (`src/cli/host.rs:68-96`), which
spawns one detached daemon after a 1.5 s grace; `daemon` refuses when
`client::served` answers; `Host::unpublish` unlinks only the socket whose
(dev, ino) it published (`src/host/mod.rs:595-605`); private hosts bind inside
their own pid dir; `cartridge stop` stops the daemon.

The gap, probed at cdd3124 in an isolated `XDG_RUNTIME_DIR` and scratch
project:

- `run` with a socket that accepts and drops composed its own host and
  answered `{"ok":true}`, exit 0 (`host.rs:165-183`; `client::served` maps
  every error to `None`, `src/cli/client.rs:38-47`).
- Two `daemon`s started together: the loser logged `host.sock is already
  served` and stayed alive nodeless (`host.rs:344-348` logs the `reconcile`
  error, then waits on `stopped()`).
- During `daemon --replace` the old host stops and unlinks `host.sock` before
  the replacement renames its staged `host.sock.<pid>` into place
  (`Host::takeover`, `mod.rs:623-665`, waits up to 2 × shutdown timeout for the
  old pid). An instance in that window sees no socket; after the grace it
  spawns a competing daemon.
- Nothing stops a detached daemon whose project is deleted: `Host::watch`
  (`src/host/watch.rs:12-59`) only reconciles on changes, and there is no
  periodic tick. The review saw 32 such daemons on deleted temp dirs.

## Contract (for dependents, e.g. the live child)

An out-of-process tool reaches the project's host with `cartridge run <event>
'<json>'` (attaches, or starts the one daemon when none answers) or
`cartridge call` (attach only). It never runs `cartridge daemon` itself.

## Steps

1. `src/host/socket.rs`: rename the private `served(path)` to `pub fn
   answers(path)` (its `sweep` callers follow), so it does not shadow
   `client::served`. Add `pub fn takeover_pending(descriptor) -> Result<bool>`:
   true when the run dir holds a `host.sock.<pid>` whose pid is `alive` and
   which `answers`.
   Windows: both keep their current constants.
2. `src/cli/client.rs`: `served` returns `Result<Option<Attached>>`:
   `Ok(None)` when `socket::answers(&socket::path(..)?)` is false; otherwise
   the `socket::client` result (error kept). Windows keeps `.ok()`.
3. `src/cli/host.rs`, `attach`:
   - `Ok(Some)` → settle and return.
   - `Err(e)` → keep `e` as the last error and retry; never spawn while the
     socket answers. Once the 1.5 s grace has passed and it still errors,
     return `e` with the socket path and the recovery hint (step 7).
   - `Ok(None)` → spawn once after the grace, but only if
     `!socket::takeover_pending(..)`; while a takeover is pending keep polling
     until the startup deadline.
4. `run`: `let (peer, _incoming) = attach(project).await?;` then
   `client::bail`. Delete the private fallback and `serve_beside` (unused
   otherwise; `warnings = "deny"`).
5. `daemon`: `client::served(project).await?`; a plain `daemon` (no
   `--replace`) also refuses with the same message while
   `socket::takeover_pending(..)` is true. In the `None` branch call a new
   `Host::listen` (step 6) with `?` before `reconcile`, so a loser exits
   non-zero with "a host already serves <descriptor>; `cartridge daemon
   --replace` takes over from it". Other `reconcile` errors stay logged.
6. `src/host/mod.rs`: `pub async fn listen(self: &Arc<Self>) -> Result<()>`
   doing the `socket::listen` + `publish_listener` that `reconcile` does when
   `inner` is unset (`mod.rs:256-261`); `reconcile` keeps skipping it once set.
7. `src/host/watch.rs`: the watch task `select!`s on `rx.recv()` and a 2 s
   `tokio::time::interval`. Only the tick checks the project; file events
   never do. A tick is a miss when `host.dir.try_exists()` or
   `host.descriptor.try_exists()` returns `Ok(false)`. Directories only, never
   `init.lua`, and an `Err` (e.g. EACCES) counts as present. Two consecutive
   misses log `project gone, stopping` and `host.stop_signal().cancel()`; a hit
   resets the count. Worst case ≈ 6 s. `daemon` already exits on `stopped()`
   (`host.rs:361-366`). Both paths are canonicalized in `Host::new`
   (`mod.rs:132,137`): removing a symlink alias keeps the daemon, and moving or
   removing the real directory stops it (its socket tag names the old path).
   Only `daemon` calls `watch`; private hosts are unaffected. If this is more
   than ~20 lines in `src/host`, stop and report instead of widening.
8. Docs. `README.md`: the `run` line becomes "send on the project's host,
   starting it when none answers". `docs/development.txt`, beside `daemon`:
   `cartridge stop` is the one way to stop the host; a tool attaches with
   `cartridge run <event>` and never starts `daemon` itself; a daemon exits
   when its project is removed; a host that accepts but never answers is
   recovered by `cartridge stop`, else `kill <pid>` where the pid is the
   numeric directory beside `$(cartridge socket)` — never by process name.
9. `solo hosts`: `verify` and `doctor` stay private; gates never depend on a
   developer's daemon. `launch` keeps its agent process; its proxy listener is
   the daemon's.
10. `.cartridge/tests/integration/takeover.test.ts`: `afterAll` first runs
    `cli(root, ["stop"])` for every root (errors ignored), then SIGKILLs
    children and removes roots. Every test's own `stop` goes in `finally`.
    Reuse `profile`, `cli`, `daemon`, `active`, `sample`. New/extended tests:
    - "a run against a socket that errors reports it and starts nothing": a
      `net.Server` on `$(cartridge socket)` that destroys every connection;
      run `sample(runDir, 4000)` concurrently with `cli(root, ["run", "plain",
      "null"])`; expect exit ≠ 0, stderr names the socket, stderr lacks
      `starting the host`, no `.cartridge/daemon.log`, `samples.seen === 0`.
      (At HEAD the private host's pid dir holds `plain.sock` while it serves,
      so `seen > 0`.)
    - "a second daemon exits and the first still serves": extend the refusal
      test: `fs.statSync(sock).ino` unchanged, `call plain null` exits 0.
    - "two daemons started together leave one": spawn two `daemon(root)`;
      `await active(root)`; within 10 s exactly one child exited non-zero; the
      survivor serves `call plain null`; socket ino unchanged since both ran.
    - "two runs with no daemon share one": two concurrent `run plain null` in
      a fresh profile both exit 0; afterwards exactly one numeric pid dir with
      `.sock` files and `status` exits 0. No assertion on stderr or
      `daemon.log`: both instances may spawn, and the loser exits via step 5.
    - "a run during --replace starts no host of its own": first
      `daemon(root)`, `active`, `sample(runDir, …)` running over the window;
      start `daemon(root, ["--replace"])` and, concurrently, `run plain null`
      in a loop until the first daemon has exited plus 3 s, recording for each
      run whether `host.sock.<replacer pid>` existed (or the first daemon had
      exited) when it started. For every run: stderr lacks `starting the
      host`; afterwards no `.cartridge/daemon.log`, `both === 0`, the numeric
      pid dirs holding sockets are only the two daemons', and the replacing
      child is the one still running. Only runs started after staging must
      exit 0. A run already attached to the old host may fail when that host
      stops mid-`bail`; it is not retried, because `bail` is not idempotent
      and a resend could deliver the event twice.
    - "a daemon exits when its project is removed": `daemon(root)`, `active`,
      `fs.rmSync(root, {recursive: true})`; the child exits within 6.5 s.
    - "an editor save of init.lua keeps the daemon": `daemon(root)`, `active`;
      rename `.cartridge/init.lua` to `init.lua~`, wait 2.5 s (over one tick),
      rename it back, wait 5 s; the child is still running and `call plain
      null` exits 0.
    - "stop": `cli(root, ["stop"])` exits 0, the child exits, the socket file
      is gone.

## Acceptance

- [ ] `cartridge run` against a socket that keeps erroring exits non-zero,
      names the socket, and starts no host or node.
- [ ] A second or racing `cartridge daemon` exits non-zero; the first's socket
      inode is unchanged and it still serves.
- [ ] A losing daemon's exit leaves the winner's `host.sock`.
- [ ] Two `run` instances with no daemon leave one composed host.
- [ ] No `run` issued during `daemon --replace` starts a host or node of its
      own; every `run` started after the replacement is staged exits 0.
- [ ] A daemon whose project root is removed exits within ~6 s; removing and
      restoring `init.lua` leaves it serving.
- [ ] `cartridge stop` and the pid recovery are documented in
      `docs/development.txt`; no test or tool code kills daemons by name.

## Verify and Proof

```sh
test -z "$(git -C cartridge.ctg status --porcelain)"
```

```sh
just check cartridge
```

```sh
# 63 s with 2 contention-only failures under load at cdd3124 (see Remaining risk).
just test cartridge
```

```sh
cargo build --manifest-path cartridge.ctg/Cargo.toml --bin cartridge
```

```sh
# Isolated: each host has its own XDG_RUNTIME_DIR and scratch project; the
# live project daemon is never touched. 9 s for 4 tests at cdd3124.
just test lifecycle
```

```sh
grep -q 'cartridge stop' cartridge.ctg/docs/development.txt
grep -q 'cartridge run <event>' cartridge.ctg/docs/development.txt
# Code only, hidden dirs included. Prose that warns against `pkill -f`
# (prd.ctg/.cartridge/boards/root/PROGRESS.md, {.,memory.ctg/}.cartridge/memos/routine/proc-kill.md)
# is out of scope: it is advice, not a kill.
! rg -n --hidden 'pkill\s+-f|killall\s|pgrep[^|]*\|\s*xargs\s+kill' -g '*.ts' -g '*.rs' -g '*.sh' -g 'justfile' -g '*.lua' -g '!**/.git/**' -g '!**/node_modules/**' -g '!**/target/**' .
```

## Remaining risk

- `just test cartridge` at cdd3124 under load: 166/168 in 63 s, two
  `tests::host::…` hit `NotProvided` after 60 s and pass alone in 4 s
  (contention, owned by host-tests-hold-under-suite-contention). The block can
  go red at collection under load; rerun when idle.
- `bind_unix` removes an unanswering socket file then rebinds
  (`src/transport/typed.rs:916-918`); two daemons racing over a stale file can
  both bind. The staged-takeover check and `sweep` narrow it; a lock beside
  `host.sock` closes it if observed.
- Other owners' tests that `cartridge run` in temp projects
  (`tools.ctg …/lane.test.ts:48`, `prd.ctg/.cartridge/tests/{host,source-records}.test.ts`)
  now start a detached daemon there; step 7 ends it once the temp root is
  removed. `just smoke policy` gets the same; smoke is owned by
  @root/smoke-passes-mcp-and-proxy (note handed over, not changed here).
