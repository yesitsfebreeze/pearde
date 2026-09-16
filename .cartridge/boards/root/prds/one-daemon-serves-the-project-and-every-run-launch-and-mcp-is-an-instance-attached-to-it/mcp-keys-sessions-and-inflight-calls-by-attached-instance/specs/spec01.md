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

Base: mcp.ctg `54e309c` ("Withhold deferred tool schemas behind a tools
meta-tool"), cartridge.ctg `4b13113` ("Write a pipe's answers to a FIFO the
module reads without Lua").

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
   the other serving; at most one numeric run directory under the project's
   `.cartridge`. `finally` closes both children and runs `cartridge stop`.
7. Prototype in `attempt-1.patch` (applies from the superproject root, `-p1`),
   which is what was probed below.

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
- [ ] Exactly one mcp node exists with the daemon running: mcp.ctg starts no
      host, node or child process of its own, checked below, and the composed
      fixture leaves at most one run directory. The daemon-wide count is not
      observable from this cartridge; it is delivered by the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` and
      re-proven by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.

## Verify and Proof

```sh
# Isolated and outside every repo, so no live cartridge is rebuilt and no
# block writes inside the footprint; shared by the blocks below, so the
# integrated pass reuses the lane pass's artifacts.
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
# The keying is per instance, and the bridge is what names it.
grep -q 'instances: Mutex<BTreeMap<String, Arc<Instance>>>' mcp.ctg/src/service.rs
grep -q '"instance": self.instance' cartridge.ctg/src/cli/host.rs
# No node-wide client state left behind.
! grep -n 'self\.session\b\|self\.inflight\|self\.restored' mcp.ctg/src/service.rs
# mcp.ctg starts no host, node or child process of its own.
! grep -rn 'Command::new\|std::process\|cartridge daemon' mcp.ctg/src/
```

## Remaining risk

- `mcp.ctg/.cartridge/tests/integration/refresh.test.ts` is **red at the base**,
  before any of this: it fails after ~22 s at its catalog-settle `until(…)`
  with the unpatched binary and the unpatched module as well as with the
  patched pair. That is why the first block skips the `initialized_live_*`
  drivers and the third names `instances.test.ts` rather than the directory. It
  is a pre-existing failure this spec neither causes nor fixes; if it is
  someone's open PRD, this one does not wait on it.
- The two cargo blocks build both crates cold into the shared target dir on
  the lane pass. cartridge.ctg is large; if the collector's per-block limit
  bites, the artifacts still survive for the integrated pass, and the blocks
  are ordered so the expensive one runs last.
- Two instances that deliberately send the same `instance` id share one
  session. Only the bridge mints ids, and it mints one per process.
- The `instance` field is optional in the schema, so an older `cartridge` binary
  against a newer module silently shares one instance again. They ship from one
  superproject commit; `instances.test.ts` fails loudly in that pairing (it was
  run that way, see the report).
- `restored` moving into the instance changes band behaviour: a tool one client
  restored no longer appears in another client's listing. That is the acceptance
  box's "each sees only its own … history"; before the one daemon it could not
  be observed, because each client had a node of its own.
