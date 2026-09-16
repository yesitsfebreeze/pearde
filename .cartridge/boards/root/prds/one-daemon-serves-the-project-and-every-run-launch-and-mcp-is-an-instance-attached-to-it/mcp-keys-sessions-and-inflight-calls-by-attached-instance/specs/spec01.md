---
complexity: small
footprint:
  - mcp.ctg
  - mcp.ctg/src/service.rs
  - mcp.ctg/src/lib.rs
  - mcp.ctg/cartridge.json
  - mcp.ctg/.cartridge/tests/unit/tests.rs
  - mcp.ctg/.cartridge/tests/integration/instances.test.ts
  - cartridge.ctg
  - cartridge.ctg/src/cli/host.rs
---

# spec01 — the bridge names its instance, and the one mcp node keys every client's state by it

Base: mcp.ctg `345871e` ("Leave out a tool whose describe hangs, not the whole
list"), cartridge.ctg `04aae7f` ("Trust a file edited after the record under
`--yolo`") — both submodules' `main` as of 2026-09-16 11:14 UTC. The design was
traced at mcp.ctg `54e309c` / cartridge.ctg `4b13113`; both submodules moved
under the plan during review, so the prototype was rebased onto the two heads
above (`attempt-2.patch`). Nothing in the option or the steps changed with the
move; the only conflict was `tests.rs`, where `345871e` appends a test whose
one `message(&line(…))` call site now names an instance like every other.

**This spec needs the PRD retargeted**, the way the done sibling
`an-instance-attaches-to-the-daemon-and-never-composes-silently` was: `repo`
to the superproject `/Users/feb/dev/cartridge`, and the footprint above. The
reason is in "Option chosen": no instance identity exists anywhere in the
runtime today, and only the bridge can mint one, so the change cannot live in
`mcp.ctg/src/service.rs` alone. Code commits inside each submodule, and
collection commits the two gitlinks.

## Option chosen

**The audit's premise holds, unlike the agent sibling's.** Traced at the bases
above:

- `Service` keeps exactly one `session: tokio::sync::OnceCell<String>`, one
  `inflight: Mutex<BTreeMap<String, (String, Value)>>` and one
  `restored: Mutex<BTreeSet<String>>` per node
  (`mcp.ctg/src/service.rs:100-113`). `session()` (`:396-411`) creates one
  `sessions` record on first use and `get_or_try_init` hands every later caller
  that same id, so every attached client's calls are recorded against one
  workspace session.
- `inflight` is keyed by the client's own JSON-RPC id alone
  (`invoke`, `:552-562`), and every MCP client counts from 1. Two attached
  clients collide on `"1"`: B's `notifications/cancelled {"requestId":1}`
  reaches A's running tool call through `notified` (`:228-239`), and whichever
  call finishes first removes the other's entry.
- Nothing above the cartridge disambiguates them. `cartridge mcp` sends
  `{"op":"message","line"}` and nothing else
  (`cartridge.ctg/src/cli/host.rs:283-317`); `handle`/`answer` pass `data`
  through verbatim (`cartridge.ctg/src/host/socket.rs:437-441`), `Host::bail`
  adds nothing (`src/host/mod.rs:798-814`), and the only caller identity the
  host has is the `Caller::{Host,Cartridge}` grant check
  (`socket.rs:424-430`), not a connection id. `mcp.ctg/src/base.rs` exposes no
  caller either. The stdio protocol carries no session header, so the node
  cannot derive the client from the line: the producer of the key has to be
  the bridge.

So: the bridge names itself, the node keys everything a client owns by that
name, and nothing else changes. Rejected alternatives: a general per-connection
caller identity in the host event protocol (a runtime-wide contract change for
one consumer); splitting the bridge and the node into two PRDs (neither half is
observable alone).

Deliberately **not** in this spec, and why:

- No `closed` event. The acceptance only asks that one client closing leaves
  the other's session and calls alone, which per-instance keying gives for
  free; a killed bridge never sends a notice anyway. The cost is one small map
  entry (a session id and two empty collections) per `cartridge mcp` ever
  attached, the same trade the agent sibling took for `Agent.runs`. Add a
  close notice only if a long-lived daemon's instance map is ever measured as
  a problem, or if disconnect-cancels a tool call becomes wanted behaviour.
- `sequence` stays node-wide (`service.rs:106`, `:508`). It only numbers
  `run`/`call` in the observation context; one counter keeps those unique
  across instances instead of two counters colliding on `call: "0"`.

## Steps

1. `cartridge.ctg/src/cli/host.rs`: `Backend` gains `instance: String`;
   `Backend::message` sends `{"op":"message","line":…,"instance":…}`. `mcp()`
   mints it once per bridge as `format!("{pid}-{nanos since epoch}")` — the
   nanos are what keeps a reused pid from inheriting a dead client's session.
   No other call site changes.
2. `mcp.ctg/cartridge.json`: document `instance` in the `mcp` event schema and
   description. Keep it optional (the schema sets no `additionalProperties`
   and the host validates against it, `cartridge.ctg/src/transport/cartridge.rs:240-277`),
   so the `{op:"ready"}` probe and any other sender stay valid.
3. `mcp.ctg/src/service.rs`: replace the three node-wide fields with
   `instances: Mutex<BTreeMap<String, Arc<Instance>>>`, where `Instance` holds
   the `session` cell, the `inflight` map and the `restored` set. Add
   `fn instance(&self, id: &str) -> Arc<Instance>` (entry/or_default/clone).
   `message` takes the instance id, resolves it once and hands `&Instance`
   down through `notified`, `request`, `invoke`, `restore`, `banded` and
   `inspect_policy`; `session` becomes
   `async fn session<'a>(&self, instance: &'a Instance) -> Result<&'a String, String>`
   (the `Arc` in `message` outlives the borrow). No lock is held across an
   await.
4. `mcp.ctg/src/lib.rs`: read `args["instance"].as_str().unwrap_or_default()`
   and pass it to `message`. Everything without an id is one instance, which
   is what a test or the readiness probe wants.
5. `mcp.ctg/.cartridge/tests/unit/tests.rs`: every existing call site names one
   instance `"a"` (`cargo fmt` reflows them; that is most of the diff). `Fake`
   answers `sessions create` with a fresh `mcp-session-{n}` per call, as the
   real cartridge does, and the existing `"mcp-session"` assertions become
   `"mcp-session-1"`. `band_list` splits into `band_list_as(service, instance)`.
   Two new tests:
   - `two_instances_keep_separate_sessions_and_in_flight_calls`: two held
     `tools/call`s under the **same** JSON-RPC id 1 from instances `a` and `b`;
     both reach the tool, their contexts carry `mcp-session-1` and
     `mcp-session-2`; `b`'s cancel of id 1 before it has anything in flight
     reaches no tool at all; `b`'s cancel once it does reaches exactly its own
     call's context and never `a`'s.
   - `a_restored_tool_stays_with_the_instance_that_restored_it`: with the band
     on, `a` restoring `memo` leaves `b`'s listing deferring it.
6. `mcp.ctg/.cartridge/tests/integration/instances.test.ts` (new): two real
   `cartridge mcp` children on one temp project, so the id the bridge mints is
   under test and not only the node. Built from `approval.test.ts`'s fixture
   (same `CARTRIDGE_BIN`/`MCP_MODULE` discovery, same stdio pump, a `client()`
   helper per child). The profile's `sessions` answers `session-<n>` per
   create and a `tool.echo` returns `args.context.session`, so the client reads
   its own session id back. It asserts: both initialize; their sessions differ
   and each stays its own across calls; a cross-instance
   `notifications/cancelled` leaves the other's calls alone; killing one leaves
   the other serving; and — asked of the daemon that is still serving the
   surviving bridge — `cartridge --dir profile status` lists exactly one `mcp`
   node in state `active`, while the run directory `cartridge --dir profile
   socket` points into holds exactly one pid directory with exactly one
   `mcp.sock`. `finally` closes both children and runs `cartridge stop`.
   `initialize` is retried while the reply carries no `result`, at most 50
   times, 200 ms apart: the daemon composes the node while the first bridge is
   already talking, and a cold start answers `service mcp unavailable: no
   active listener` once. Observed, and the bound observed too — see the
   report.
7. Prototype in `attempt-2.patch` (applies from the superproject root, `-p1`;
   from either submodule with `-p2` and the matching `--include`/`--exclude`),
   rebased onto the bases above, which is what was probed below.
   `attempt-1.patch` is the round-1 prototype and no longer applies: `345871e`
   moved `tests.rs` under it.

## Acceptance

- [ ] Two `cartridge mcp` stdio clients attached to one daemon keep separate
      sessions (each sees only its own initialization and history), and one
      closing does not affect the other's session or calls.
      (`instances.test.ts`: the two echoed session ids differ, each is stable
      across that client's calls, and killing one leaves the other's
      unchanged.)
- [ ] An in-flight call from one instance is not visible in or cancellable
      from the other. (`two_instances_keep_separate_sessions_and_in_flight_calls`:
      both clients hold a call under id 1; a cancel from one reaches only its
      own call's context, and never the other's.)
- [ ] Exactly one mcp node exists with the daemon running, proven at composed
      scope inside this PRD's own fixture. `instances.test.ts`, with two bridges
      attached to one daemon, asserts
      `status.filter(n => n.id === 'mcp' && n.state === 'active').length === 1`
      and that `path.dirname(cartridge socket)` holds exactly one pid directory
      containing exactly one `mcp.sock`. `state` is load-bearing: a cartridge
      present in the profile but left out of the composition is still listed, as
      `disabled` (measured). The dead `run.length <= 1` assertion is gone — it
      looked under the project's `.cartridge`, where run directories never
      appear (`cartridge.ctg/src/host/socket.rs:46-84` puts them at
      `base()/tag(descriptor)/<pid>`), and it passed at zero. Structurally,
      mcp.ctg starts no host, node or child process of its own: a standing
      property, guarded against regression by block 4 rather than introduced
      here — the guard is green at the base too, and scans `mcp.ctg/src/` only,
      so `build.rs`, `init.lua` and `cartridge.json` are outside its scope
      (checked by hand: none of them spawns anything). For the live project, the
      daemon-wide count is delivered by the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` and
      re-proven composed by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`,
      which is still `open` — that re-proof has not landed yet.

## Verify and Proof

**How this collects: from `specced`, with no lane, so every block below runs
exactly once — in `repo`, the superproject, where the submodules are real
checkouts.** Do not `prd claim` this PRD into a lane first. The template's
"first the lane, then `repo`" does not hold here, and the reason is mechanical:
`claim` on a `specced` PRD creates the lane with a plain
`git worktree add -b <branch> <dir> HEAD` on `repo`
(`prd.ctg/src/lifecycle.ts:225`), `repo` is the superproject, and a
superproject worktree does not populate submodules — `submodule.recurse` is
unset (`git config --get submodule.recurse` exits 1), so `mcp.ctg` and
`cartridge.ctg` are **empty directories** in a lane. Measured in a lane-shaped
worktree of `fb44521`, all four blocks verbatim: block 1 exits 101 (`manifest
path mcp.ctg/Cargo.toml does not exist`), block 2 exits 1 for the same reason,
block 3 exits 101, and block 4 exits 1 on its first `test -f`. Collection
through a lane would therefore abort at pass 1 before it reached anything.

With no lane there is one pass: `collect` verifies in `tree`, which is the lane
only when the lane exists and otherwise `repo` itself (`lifecycle.ts:125`,
`:137`), and it re-verifies in `repo` (`:167`) only after fast-forwarding a
lane into it. `specced` is an accepted collect state (`:112`). The done sibling
`an-instance-attaches-to-the-daemon-and-never-composes-silently` collected
exactly this way — its `collection.md` records each of its six blocks once. If
the PRD is claimed into a lane by mistake, nothing is lost: collection fails at
the first block (101) before the footprint sweep and before any commit, so
remove the lane worktree and its branch (`git worktree remove <lane>`,
`git branch -D lane/root-<slug>`) and collect from `claimed`, which
`lifecycle.ts:112` accepts and `:125` then resolves to `repo`.

So the only pass runs in the live checkout, and every rule the template states
for pass 2 is the rule for the only pass: no block writes inside the footprint,
and every cargo command keeps `CARGO_TARGET_DIR` outside both repos so no live
cartridge is hot-restarted.

```sh
# Isolated and outside every repo, so no live cartridge is rebuilt and no
# block writes inside the footprint; shared by the blocks below, so the later
# blocks reuse the earlier ones' artifacts.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/mcp-instances-verify}"
# The two `initialized_live_*` tests shell out to the bun fixtures, which the
# composed block below runs directly with the artifacts they need.
cargo test --manifest-path mcp.ctg/Cargo.toml --lib -- --skip initialized_live
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/mcp-instances-verify}"
cargo fmt --manifest-path mcp.ctg/Cargo.toml --check
cargo clippy --manifest-path mcp.ctg/Cargo.toml --all-targets
cargo fmt --manifest-path cartridge.ctg/Cargo.toml --all --check
cargo check --manifest-path cartridge.ctg/Cargo.toml --bin cartridge
```

```sh
# The composed proof: two real bridges, one daemon, in a temp project of its
# own. ~30 s once the two crates are built.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/mcp-instances-verify}"
cargo build --manifest-path cartridge.ctg/Cargo.toml --bin cartridge
cargo build --manifest-path mcp.ctg/Cargo.toml
CARTRIDGE_BIN="$CARGO_TARGET_DIR/debug/cartridge"
MCP_MODULE="$CARGO_TARGET_DIR/debug/libmcp.dylib"
[ -f "$MCP_MODULE" ] || MCP_MODULE="$CARGO_TARGET_DIR/debug/libmcp.so"
export CARTRIDGE_BIN MCP_MODULE
cd mcp.ctg && bun test ./.cartridge/tests/integration/instances.test.ts
```

```sh
# Static guards. Two shapes matter here, both learned the hard way:
#   * a negation must be its own gating statement. `sh -e` explicitly ignores
#     the status of a `!`-prefixed command, so `! grep …` never fails a block;
#     only the last such line gates, as the script's own exit status.
#   * every guard names its paths first. grep exits 2 on a missing file and
#     prints nothing, which a bare negation reads as "no match" and passes.
test -f mcp.ctg/src/service.rs
test -f mcp.ctg/src/lib.rs
test -f cartridge.ctg/src/cli/host.rs
test -d mcp.ctg/src
# The keying is per instance, and the bridge is what names it.
grep -q 'instances: Mutex<BTreeMap<String, Arc<Instance>>>' mcp.ctg/src/service.rs
grep -q '"instance": self.instance' cartridge.ctg/src/cli/host.rs
# No node-wide client state left behind: `inflight` and `restored` are only
# ever reached through an `&Instance`, never off the node.
if grep -n 'self\.inflight\|self\.restored' mcp.ctg/src/service.rs; then exit 1; fi
# `self.session(instance)` is the method and stays; a bare `self.session` is
# the node-wide OnceCell coming back, which is the regression this guards.
if grep -n 'self\.session' mcp.ctg/src/service.rs | grep -v 'self\.session('; then exit 1; fi
# mcp.ctg starts no host, node or child process of its own.
if grep -rn 'Command::new\|std::process\|cartridge daemon' mcp.ctg/src/; then exit 1; fi
```

## Remaining risk

- The fixture's bounded `initialize` retry masks a real cold-start race that
  **this slice does not own**: the daemon composes the mcp node while the first
  bridge is already talking, so a cold start answers `initialize` with an error
  once, and a real MCP client does not retry `initialize` — it would see the
  failure. That is a defect of the attach path (the parent's audit, the
  `closed`-and-readiness territory, sibling
  `an-instance-attaches-to-the-daemon-and-never-composes-silently`), not of
  per-instance keying, and nothing here makes it worse. It has no owner today;
  it belongs to a readiness PRD under the parent. The retry is a fixture fix
  and the bound is honest — measured at 11.8 s to a real assertion failure with
  no listener ever appearing, no hang.
- `mcp.ctg/.cartridge/tests/integration/refresh.test.ts` is **red at the base**,
  before any of this: it fails after ~22 s at its catalog-settle `until(…)`
  with the unpatched binary and the unpatched module as well as with the
  patched pair. That is why the first block skips the `initialized_live_*`
  drivers and the third names `instances.test.ts` rather than the directory. It
  is a pre-existing failure this spec neither causes nor fixes. It has a named
  owner: `@mcp/the-mcp-live-catalog-tests-settle-at-base` (open, prio 50),
  whose acceptance is "`just test mcp` exits 0 on two consecutive runs" and
  which names these same `initialized_live_*` drivers. This PRD does not wait
  on it.
- The cargo blocks build both crates **cold on the one and only pass**, into
  the shared target dir outside both repos — there is no lane pass to warm it
  (see "How this collects"). cartridge.ctg is large, and the collector allows
  120 s per block. The blocks are ordered so each one warms the next and the
  expensive composed build runs last; on a cold cache the middle block is the
  one at risk. If it times out, the target dir survives between blocks and a
  re-run is warm.
- Collection commits from the live checkout, because there is no lane.
  `collect` sweeps `git status --porcelain -- <footprint>` (`lifecycle.ts:145`)
  and the footprint names the two submodule directories, so **whatever is dirty
  or committed inside `mcp.ctg` or `cartridge.ctg` at that moment rides in on
  this receipt** — a gitlink can only be staged by the submodule's own path, so
  the footprint cannot be narrowed to files. Precondition, to be checked
  immediately before collecting and not when the footprint was widened: both
  submodules clean in the footprint, and each submodule's HEAD recorded in the
  collection. Not hypothetical: at review time `cartridge.ctg` was dirty with
  unrelated work in `src/cli/host.rs`, the very file step 1 edits; at the time
  of this revision that has landed and `mcp.ctg` is the dirty one, with
  unrelated integration-test work. Check at collection time, every time.
- `.cartridge/tests/unit/tests.rs`'s `in_flight(n)` helper spin-waits on
  `tokio::task::yield_now()` with **no deadline**. A regression where a call
  never reaches the tool hangs the unit suite instead of failing it, and the
  block's 120 s becomes the only bound. One `tokio::time::timeout` around the
  wait fixes it; out of this slice because it is not a one-line change.
- The `instances` map is never pruned, and nothing detaches an instance: the
  entry is not "cleared on disconnect", it is never released at all, until the
  daemon stops. The `Instance` doc comment must say that rather than "never
  cleared while the instance is attached", which implies a release that does
  not exist.
- The composed block needs `policy.ctg` beside `mcp.ctg`, because the fixture
  composes the real policy cartridge from `../policy.ctg`. That holds in `repo`
  and is another reason the lane (empty submodule directories) cannot run this.
- Both submodules moved during review (mcp.ctg `54e309c` → `345871e`,
  cartridge.ctg `906b39a` → `04aae7f`) and mcp.ctg is being worked on right
  now. `attempt-2.patch` applies at both current heads, checked; it will need
  rebasing again if `tests.rs` or `src/service.rs` move before implementation.
- `sequence` staying node-wide has one observable consequence: `run` is
  `mcp-{n/1024}` and `call` is `n`, both node-wide, so one client's ids advance
  with the other's traffic and the gaps disclose the other client's call
  volume. Small, and the fix (put the instance in the run id) can wait.
- Two instances that deliberately send the same `instance` id share one
  session. Only the bridge mints ids, and it mints one per process.
- The one-node assertion counts `active` nodes named `mcp`, which is the count
  the host can actually reach. Measured against this fixture: composing the mcp
  cartridge a second time under another id leaves that second slot `failed` with
  no socket (the assertions stay green, and correctly so — no second node runs);
  composing it twice under the *same* id `mcp` breaks the daemon outright, so
  every client times out on `initialize` and the fixture fails earlier. Neither
  is the regression the box guards; both were run.
- The `instance` field is optional in the schema, so an older `cartridge` binary
  against a newer module silently shares one instance again. They ship from one
  superproject commit; `instances.test.ts` fails loudly in that pairing (it was
  run that way, see the report).
- `restored` moving into the instance changes band behaviour: a tool one client
  restored no longer appears in another client's listing. That is the acceptance
  box's "each sees only its own … history"; before the one daemon it could not
  be observed, because each client had a node of its own.
