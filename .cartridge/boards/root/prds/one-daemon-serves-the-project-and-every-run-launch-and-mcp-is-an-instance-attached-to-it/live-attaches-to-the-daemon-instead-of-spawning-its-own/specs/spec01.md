---
complexity: small
footprint:
  - src/launch.ts
  - .cartridge/tests/integration/launch.test.ts
---

# spec01 — the live launcher attaches with `run` and starts no daemon

Base: live.ctg at `4cbb053` (the gitlink, unchanged since the spec was drafted
at the superproject's `0e3916c`; both footprint files are clean at it).
**Implemented against `780dd89`**: `live.ctg` HEAD moved on 2026-09-16 with
"Speak from the host itself and drop the HTTP surface", which touched both
footprint files, so the lane was rebased onto it. Live's `status`/`open` no
longer report a URL, and the launcher takes that contract; nothing else in this
spec is affected — that commit touched neither the `status` probe, the
`--yolo daemon` spawn, the signal bookkeeping nor the kill timer. Depends on
`an-instance-attaches-to-the-daemon-and-never-composes-silently` (done,
`f364f46`), which delivered the attach contract this spec consumes.

## Option chosen

**`launch.ts` becomes a pure instance: it attaches with `cartridge run` and
deletes its own daemon spawn and the child-ownership it existed for.
`coordinator.ts` does not change.**

Traced end to end:

- `live.ctg/src/launch.ts:46-55` runs `cartridge status` and, on any non-zero
  exit, spawns `["--yolo","daemon"]` **undetached** as its own child, with
  `host.kill("SIGTERM")` wired to `exit`/`SIGINT`/`SIGTERM`/`SIGHUP`
  (`:36-39`). That is the whole "runtime is a child, not a daemon" comment at
  `:5-8` — and it is exactly the shape the parent reverses.
- The attach contract already does all of it, better. `cartridge run`
  (`cartridge.ctg/src/cli/host.rs:222-230`) calls `host::attach`
  (`:59-101`): it polls `client::served`, waits a 1.5 s grace for a staged
  takeover (`socket::takeover_pending`), spawns **one detached** daemon
  (`spawn_daemon`, `:110-140`, `process_group(0)`, log in
  `<root>/.cartridge/daemon.log`) only when nothing answers, and then blocks in
  `settle_remote` (`:144-183`) until no cartridge is `starting` before handing
  the connection back. The race in Acceptance box 3 is settled there, not
  here: a second `daemon` exits non-zero on the bind (`host.rs:379-401`), and
  the loser's `unpublish` only unlinks a socket whose (dev, ino) it published.
  Re-deriving any of that in a Bun script would be a second implementation of
  a contract that is already tested in
  `<superproject>/.cartridge/tests/integration/takeover.test.ts` — the
  superproject's suite, not live.ctg's own
  `.cartridge/tests/integration/`.
- So the entire change on the live side is: stop probing with `status` (which
  talks only to `host.sock` and cannot start anything), attach with `run`, and
  drop the child-ownership bookkeeping that only existed for a host this
  process owned.
- The readiness loop at `:56-66` already polls `live {"op":"status"}` for
  `running && url`. Switching its command from `call` to `run` **is** the
  attach — one changed word replaces the spawn block.

**The launcher keeps no deadline of its own over an attach.** Re-derived from
the code (round 1 F2: the first draft sized the timer from
`startup_timeout_secs`, which is not the bound that governs). One cold
`cartridge run live {"op":"status"}` passes through three settings in series:

1. `attach`'s own loop deadline is `startup_timeout` — default **60 s**
   (`cartridge.ctg/.cartridge/settings.json:12-18`) — and it bounds only the
   wait for a socket to answer (`cartridge.ctg/src/cli/host.rs:63-101`).
2. The moment one answers, `attach` calls
   `settle_remote(&found.0, settings.verify_timeout())` and returns **from
   inside that branch** (`host.rs:72-76`), never re-checking its own deadline.
   `settle_remote` (`host.rs:144-183`) blocks while any cartridge is
   `starting`/`waiting` or the status list is empty, bounded by
   `verify_timeout_secs` — default **300 s**
   (`settings.json:33-39`).
3. Only then does `run` deliver the event: `client::bail`
   (`host.rs:222-228` → `src/cli/client.rs:91-99`) → `Host::bail`
   (`src/host/mod.rs:798-814`), bounded per listener by `event_timeout_ms` —
   default **60 000 ms** (`settings.json:19-25`).

So one cold attach is bounded at roughly **60 + 300 + 60 ≈ 420 s**, not 60, and
the settle alone is 300. None of the three is a constant either:
`settings::host()` settles them from `~/.cartridge/config.lua` and the
project's `.cartridge/config.lua` over the declaration
(`cartridge.ctg/src/settings/host.rs:69-94`, `src/settings/files.rs:31-35`).
Neither file declares a `host` section in this project today, so the declared
defaults are what is in force — and any number written into the launcher would
have to be re-derived the day one does.

That rules out every fixed per-command timer, including 90 s: below the real
bound it kills an attach that is still making progress, which is the one
failure this PRD cannot afford (a half-composed daemon left behind, reported to
the user as "the local coworker did not become ready"). So `command()` **drops
its `setTimeout(kill)` rather than raising it**. Every invocation already ends
by itself; where it times out waiting for the socket it says so with the host's
own message naming `<root>/.cartridge/daemon.log` (`host.rs:92-99`), and where
`settle_remote` runs out of `verify_timeout_secs` it returns **silently** and
the command carries on to the event — so the log is named by the host in the
first case and by the launcher's own not-ready error in the rest (round 2 F8).
Either way the authority on how long an attach may take stays with the process
that knows the settings. What the launcher still bounds
is the wait it actually owns — Live's own node answering `status` inside a
composition that `settle_remote` has already reported as settled — so the readiness
deadline starts **after the first attach returns** and is 60 s of polling from
there. A side effect worth having: an attach that keeps failing is now retried
at most once *when each attach is itself slow*, rather than every 250 ms until a
wall-clock deadline; a fast failure (a socket that answers but does not serve,
`client::unanswered`) still retries every ~1.75 s for the deadline's 60 s
(round 2 F7).

**`coordinator.ts` needs no change.** The interrupted-marking
(`coordinator.ts:31-42`) lives in `Coordinator`'s constructor. The only
constructor call is `startServer` (`src/server.ts`), and the only call of that
is `wire.on("apply", …)` in `src/main.ts:17-21`. The host sends `apply` exactly
once per cartridge process, in `Host::start` right after the node connects
(`cartridge.ctg/src/host/process.rs:207-224`) — it is not a repeatable event.
An attaching instance sends `live` events over the existing wire and
constructs nothing itself — with one boundary worth naming (round 1 F5): when
`settle_remote` sees a trust refusal it issues a single
`reload {"cartridge": null}` (`host.rs:152-165`) → `Host::reconcile`
(`src/host/mod.rs:294-327`), which keeps healthy running slots but does start
`waiting`/failed ones. So an attach can indirectly *start* a live node, and
that node start fires the marking — which is exactly when it is meant to fire.
The marking therefore fires only on a node's own startup, never on an attach to
a node already running, which is the PRD's requirement verbatim. What made it
destructive was a *second live node* in a second composition sharing one store;
removing the spawn removes the second node, and with it the symptom. Adding an
"is this an attach?" flag to the constructor would be a second name for
"did this node just start" — rejected, same shape as the done sibling
`agent-runs-key-per-attached-instance-not-per-process`.

**Answer to the PRD's open question: yes — and it already works that way.**
`cartridge launch <agent>` keeps the agent process and its tmux window in the
launching command, while the proxy listener stays in the daemon and the agent
is pointed at the daemon's proxy address. `host::launch`
(`cartridge.ctg/src/cli/host.rs:231-247`) attaches, asks the daemon's `proxy`
cartridge for `{"op":"launch",…}`; proxy answers from **its own bound
listener** — `let (base, key) = proxy.front…; args["base"] = json!(base)`
(`proxy.ctg/src/lib.rs:394-403`) — and router renders the command from it. The
CLI then spawns that `{program, args, cwd, env, unset}` locally, in the
foreground, with `kill_on_drop` (`host.rs:249-282`), after `ignore_interrupt`
so the terminal's Ctrl-C reaches the agent and not the launcher. Nothing in
live.ctg's footprint decides this, and the code admits no second design: the
proxy port is bound once, in the daemon, by design (`.cartridge/init.lua:41-47`
— "Nothing here binds a port on its own: the proxy listens only when a key
names it"). The live launcher is the same shape one level up: Live's own
surfaces stay in the daemon's live node, and `launch.ts` prints the session and
exits. (`live.ctg@780dd89` has since dropped Live's HTTP server entirely and
speaks from the host; the shape is unchanged, only the URL is gone.)

## Steps

1. `src/launch.ts` — prototyped in `attempt-2.patch` (round 2; supersedes
   `attempt-1.patch`, which is kept for the diff of the F2 change), which
   applies to live.ctg unmodified (`git apply --check` → 0):
   - Imports: `spawn`, `ChildProcess`, `closeSync`, `mkdirSync`, `openSync`
     become unused; keep `spawnSync` (the trust gate) and `existsSync`.
   - Delete `host`, `stop`, the `exit` handler and the signal loop (`:33-39`).
     No host is this process's child any more, so there is nothing to take
     down; the daemon is left to the project.
   - Delete the `status` probe and the `--yolo daemon` spawn (`:46-55`),
     including the `.cartridge/live-service` log directory it created.
   - Delete `command`'s `setTimeout(()=>child.kill(),10000)` and its
     `try/finally` — no timeout parameter replaces it; the comment above
     `command` records the three settings that bound a `cartridge run`
     instead. Its poll becomes
     `["run","live",JSON.stringify({op:"status"})]`. Keep the `{op:"open"}`
     mutation on `call`, once, after readiness — by then a daemon answers.
   - Readiness deadline: `let deadline=Infinity`, set to `Date.now()+60000`
     after the first reply is in, so the loop never bounds the first attach
     and bounds only the polling after it.
   - Carry the last non-zero attach stderr into the not-ready error and point
     it at `<root>/.cartridge/daemon.log`, which is where `spawn_daemon`
     writes now; `.cartridge/live-service/runtime.log` no longer exists.
   - Rewrite the `:5-8` header comment and the closing line of the success
     message: the daemon outlives this terminal, and `cartridge stop` stops it.
2. `.cartridge/tests/integration/launch.test.ts` — rewrite. **It is red at
   HEAD** (`bun test` → `expect(ui).toBeDefined()` fails): it still asserts a
   `tui` call and a `pty` handoff that `the-profile-is-the-orchestration-service`
   removed, and its fake `status` exits 0, so it never reached the spawn it
   claims to forbid. The replacement drives the launcher against a fake
   `cartridge` that logs its argv, refuses a bare `status` (exit 1 — the old
   probe's failure), **answers a `daemon` argv with exit 0** and answers
   `run`/`call live`. Answering the daemon rather than refusing it is what
   makes the assertion that names the outcome the one that fails: against
   unpatched `launch.ts` the run now reaches
   `expect(calls.filter(args=>args.includes("daemon"))).toHaveLength(0)` and
   fails there (`Expected length: 0, Received length: 1`), instead of dying
   earlier on `The local coworker stopped (2)` — round 1's note (b) on the
   acceptance dimension. Two cases, `cold=false`
   and `cold=true` (first attach reports `{running:false}`, the next
   `{running:true,url}`), both asserting: zero calls containing `daemon`, zero
   bare `status` calls, the attach went through `["run","live",{"op":"status"}]`,
   `trust` still ran first, exactly one `{"op":"open"}`, exit 0. The child is
   spawned with `cwd` = a temp project holding `.cartridge/init.lua`, so the
   launcher's project walk lands inside the fixture in both the lane and the
   live checkout. `script`/pty wrapping is dropped with the terminal.
3. Nothing under `src/coordinator.ts`. If a step wants to touch it, stop and
   report: the marking is already node-startup-only and the diff would be
   churn.

## Acceptance

- [x] `cartridge launch claude` with a daemon running starts no
      `cartridge daemon` process and no second composition; the agent talks
      through the daemon's proxy. live.ctg's share: the launcher spawns no
      daemon and composes nothing — the fake-binary test records zero `daemon`
      argv in both the warm and the cold case, and `src/launch.ts` contains no
      `"daemon"` argument. The composed process count is not observable from
      this repo; it is delivered by
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` (done)
      and re-proven by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.
- [x] Work in flight on the daemon is not marked `interrupted` by a new
      `launch` attaching. An attach constructs no `Coordinator`: the marking is
      reachable only from `startServer` ← `wire.on("apply")`, and the host
      sends `apply` once per node start
      (`cartridge.ctg/src/host/process.rs:207-224`). The launcher no longer
      starts a node at all, which is what the test pins; the constructor's
      recovery marking stays where it is, checked below.
- [x] With no daemon, `launch` results in exactly one daemon being started
      (concurrent launches included). The launcher delegates it wholly to
      `host::attach`, which spawns at most one detached daemon and loses the
      race safely; the cold case proves the launcher goes through `run` and
      never spawns. The concurrency itself is the done sibling's Acceptance
      box 6, proven in
      `<superproject>/.cartridge/tests/integration/takeover.test.ts:303`
      ("two runs with no daemon share one") — the superproject's suite, not
      live.ctg's own `.cartridge/tests/integration/`.

## Verify and Proof

```sh
bun test ./.cartridge/tests/integration/launch.test.ts
```

```sh
# The launcher passes no `daemon` (or `--yolo`) argument to the runtime: it is
# an instance, not a host. Red at HEAD (src/launch.ts:52).
! grep -nE '"(--yolo|daemon)"' src/launch.ts
# It attaches through `run`, the CLI's attach-or-start-one path.
grep -q '"run","live"' src/launch.ts
# The recovery marking stays in the node's own startup, unflagged.
grep -q "phase='interrupted'" src/coordinator.ts
# The proof still forbids a daemon call rather than only a terminal.
grep -q "args.includes(\"daemon\")" .cartridge/tests/integration/launch.test.ts
```

## Remaining risk

- `src/main.ts:9` still hardcodes `../../cartridge.ctg/.cartridge/credentials`
  and `/router` for `--standalone`. It does not block attach (the branch is
  unreachable under a host, `main.ts:7`), so per the PRD it is noted, not
  fixed.
- `just live` now prints the session URL and exits instead of blocking on its
  child host. That was already true whenever a daemon answered; it is now
  always true, and it is the attached-instance shape. The daemon is stopped
  with `cartridge stop`, which the success message names.
- `bun run check` (tsc) is not in Verify: it needs `node_modules` and the
  `auth.ctg` sibling, neither of which a bare lane worktree has. `just check
  live` covers it in the checkout; it passes on the prototype with the
  siblings present.
- **The bound on a cold `just live` is `verify_timeout_secs`, not anything in
  this repo.** The launcher no longer times an attach, so a cold `just live`
  can now sit for as long as the host allows: up to `startup_timeout_secs`
  (60) waiting for a socket, then up to `verify_timeout_secs` (**300**,
  `cartridge.ctg/.cartridge/settings.json:33-39`) inside `settle_remote`, then
  `event_timeout_ms` (60 s) for the event — ≈420 s for one attach, and
  **~13 minutes** for the command: the readiness loop checks its deadline only
  between attempts and sets it only *after* the first attach returns, so one
  further (warm, ≤360 s) attach always runs after that — ≤420 + ≤360 ≈ 780 s
  (round 2 F7), against ~10 s of visible silence before. That bound also holds
  only for as long as the daemon answers its own RPCs: `peer.call`
  (`cartridge.ctg/src/transport/rpc.rs:239-257`) awaits an untimed oneshot and
  `settle_remote` checks its deadline only between calls, so a daemon wedged
  with an open socket that never answers `status` hangs the attach, and now the
  launcher, indefinitely. That hole is upstream's — every `run`, `launch` and
  `mcp` has it — and closing it with a re-added launcher timer would undo the
  bullet above, so it belongs in `cartridge run` (round 2 F9).
  A composition that is genuinely stuck now
  looks like a hung `just live` until the host gives up with its own message in
  `<root>/.cartridge/daemon.log`. That is the deliberate trade: killing a
  settle that is still making progress leaves a half-composed daemon behind,
  and this way the one number that governs is tunable in
  `.cartridge/config.lua` under `host` rather than pinned in a Bun script.
  Anyone who wants `just live` to give up sooner lowers `verify_timeout_secs`
  there, which lowers it for `cartridge run`, `launch` and `mcp` at the same
  time.
- The 60 s readiness deadline still in the launcher bounds only the wait
  *after* the first attach has returned — Live's own node answering `status`
  inside an already-settled composition. It is a launcher-side number with no
  setting behind it; if Live ever takes longer than that to answer after the
  host reports it running, this is the line to raise.
- **`--yolo` no longer reaches the project daemon** (round 1 F3). Today
  `launch.ts:52` spawns `["--yolo","daemon"]`; `--yolo` sets `YOLO_ENV`
  (`cartridge.ctg/src/cli/mod.rs:87-89`) and `settings::apply` merges
  `{"yolo": true}` into every cartridge declaring it —
  `agent.ctg/cartridge.json:100`, `proxy.ctg/cartridge.json:75`,
  `memo.ctg/cartridge.json:129`. `spawn_daemon` passes `--dir <project> daemon`
  and adds `--yolo` only when `settings::yolo()` reads `CARTRIDGE_YOLO` from the
  environment it inherited (`host.rs:110-140`, corrected from "only `--dir
  <project> daemon`" — verifier-1 nit 6), and the launcher's `Bun.spawn` passes
  no such environment; an instance also "cannot change an existing daemon"
  (`src/cli/args.rs:164-170`). So a `just live`
  composition stops running agent/proxy/memo in automatic-execution mode: a
  policy bypass is **lost, not gained**, and a launched agent may start asking
  the policy where it used to be granted. This is a consequence of the parent's
  one-daemon shape, not a regression to fix here — the one daemon serves every
  instance, so no instance may set its mode. It is **not** that restoring it
  would be expensive: `spawn_daemon` builds a plain `std::process::Command` and
  inherits the environment, and `yolo()` is a bare `CARTRIDGE_YOLO` read
  (`cartridge.ctg/src/transport/settings.rs:188-191`), so
  `env:{...process.env,CARTRIDGE_YOLO:"1"}` on `command()`'s `Bun.spawn` would
  do it in one line inside this footprint — `spawn_daemon` would then hand the
  flag on explicitly. That path exists and is deliberately
  not taken (round 2 F6): it would let whichever instance happens to start the
  daemon first decide the policy mode for every later one. The `trust --ask` gate with
  `CARTRIDGE_YOLO=1` is a separate pre-attach `spawnSync` and is unchanged.
  Whoever wants the old behaviour sets `yolo` per cartridge in
  `.cartridge/config.lua`, or starts the project daemon with `--yolo`; that
  belongs to a settings slice, not to this one.
