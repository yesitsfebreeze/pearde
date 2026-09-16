---
complexity: small
footprint:
  - src/lib.rs
  - .cartridge/tests/integration/native.ts
  - .cartridge/tests/integration/instances.test.ts
---

# spec01 — prove the one sessions node's single store and single id space, and guard it

Base: sessions.ctg `b896162` ("Keep test daemons out of the real cartridge home
and let mailbox credentials through"), the PRD's source HEAD. `repo` is
`sessions.ctg` and stays that way; nothing outside this submodule changes.

**This spec needs the footprint widened** to the two paths above, both under
`.cartridge/tests/integration/`. No Rust changes — the whole delivery is a
regression test plus a static guard, and the PRD's declared footprint is
`src/lib.rs` alone, which a test cannot live in (sessions' unit modules are
`#[path]`-attributed out to `.cartridge/tests/unit/main/`, also outside it).
`collect` refuses a change outside the declared footprint, so the coordinator
must widen it before this lands.

## Option chosen

**Both of the audit's findings dissolve under one daemon, and neither needs a
code change.** Traced at `b896162`:

- The buffer-id counter is **not** "local to each process". It is `Store.next`
  (`src/lib.rs:101`), a field of the in-memory store, seeded from what is on
  disk at load — `install` does `self.next = self.next.max(b.id + 1)` for every
  persisted buffer (`:344`) — and reserved once per operation under the store's
  own write lock, before the operation runs and whether or not it succeeds
  (`execute`, `:1061-1064`). One store, one counter. The counter was only ever
  per-process because the *store* was per-process.
- "The last rename wins" is not a rename op: **sessions has no rename op at
  all.** The only `rename` in `lib.rs` is `std::fs::rename` (`:394`), the
  atomic snapshot commit in `Store::save` (`:359-403`), which replaces
  `<session>.json` unconditionally (the `expected` compare-and-swap is passed
  only by `repair_empty`, `:465`). The audit's finding is really: two processes
  each hold a full in-memory copy loaded once at start, so each one's snapshot
  commit clobbers the other's. The nearest thing an instance can actually call
  is `sessions update {id, name}` (`:695-700`), and that is what box 2 means.
- What makes both of them one-daemon problems and nothing else: the store is
  opened exactly once per process — `Store::load` has one call site (`:1214`),
  inside `start`, which installs it in `static STORE: OnceLock<Arc<SharedStore>>`
  (`:1185`) and refuses a second `start` with "sessions already started"
  (`:1226`). Two copies require two processes, which required two compositions.
  With the attach contract in force (sibling
  `an-instance-attaches-to-the-daemon-and-never-composes-silently`, done) there
  is one sessions node, so there is one `Store`, one `next` and one copy of
  every session. **Nothing per-process is left to remove.**

**Measured, not assumed.** Two daemons over one store dir, at this base, with
the fixture below: they handed out buffer id **2** for two different sessions,
and the second daemon's copy of the first's session still read `name: "alpha"`
with `buffers: []` after the first had renamed it and opened a buffer in it.
Exit 1. Under one daemon, the same calls give six distinct ids and read the
rename back. Both worlds are in `analyst-1.md`.

**Box 1's second half is not an instance-keying problem, and cannot be made
into one here.** No instance identity reaches this layer, or any cartridge
except mcp. `cartridge call` is `client::ask(project, "bail", …)`
(`cartridge.ctg/src/cli/mod.rs:108-114`); the host passes `data` through
verbatim and the only caller identity it holds is the `Caller::{Host,Cartridge}`
grant check, not a connection id — traced and written up by the specced sibling
`mcp-keys-sessions-and-inflight-calls-by-attached-instance`, which had to make
the mcp *bridge* mint its own id precisely because nothing above it has one, and
which put that id only in mcp's own event payload. Sessions' ops arrive as
`store.sessions(args)` / `store.buffers(args)` with caller-supplied JSON
(`init.lua:11-12`, `lib.rs:1236`, `:1260`) and nothing else.

That is fine, because sessions already scopes by the thing that outlives an
instance: the **session record**. A buffer carries `session: Option<String>`
(`:55`), `buffers list {session}` filters on it (`:594-604`, `:846-856`), and
a session is created by whoever asks and named by id from then on. An attached
instance works under whatever session id it names.

Note what is **not** true at this base (round 1, F1): `mcp` creates one `"MCP"`
session per **node**, not per instance (`mcp.ctg/src/service.rs:419-433`, a
`OnceCell` on `Service`; the per-instance sibling
`mcp-keys-sessions-and-inflight-calls-by-attached-instance` is still `specced`),
and `launch`/`run` name no session at all — the per-run `sessions create` lives
in `agent.ctg/src/lib.rs:273-278`. So per-instance session separation does not
exist today; the session scope this spec proves is the mechanism that would
carry it once callers pass distinct session ids.
Keying a second, parallel per-instance scope inside the node would need an
instance identity in the host call protocol (a runtime-wide contract change the
mcp sibling explicitly rejected for one consumer) and would duplicate the
session scope that already exists. Rejected.

**Proposed narrowing of box 1, said out loud rather than done silently.** The
literal wording — "do not see each other's buffers unless they ask for them" —
is true of *sessions*, not of *instances*, and an unfiltered `buffers list`
(no `session` key) returns every buffer in the store, as it always has: before
the one daemon both compositions read the same directory and listed the same
buffers, so this is not a regression the one daemon introduces, and it is not
something this PRD's outcome ("one counter, one in-memory copy") asks to
change. Proposed wording:

> Two attached instances calling sessions draw buffer ids from one space (no id
> is handed out twice), and a buffer opened under one session is never returned
> by a listing that names another session; an instance reaches another session's
> buffers only by asking — by that session's id, or by an unfiltered
> `buffers list`.

The test asserts all three clauses, including the unfiltered listing, so the
current behaviour is recorded rather than hidden. If the board wants instances
isolated from each other *without* asking — i.e. an unfiltered list scoped to
the caller — that is a new outcome needing caller identity in the host
protocol, and it should be its own PRD under the parent, not a silent extension
of this one.

**Box 3 is provable here, and the fixture that proves it is already in the
repo.** `.cartridge/tests/integration/native.ts` starts a real
`cartridge daemon` in a temp project and cartridge home (`:67-70`), settles on
`cartridge status` (`:81-95`) and sends every request as its own
`cartridge call` child (`:123-136`). So this is not "unobservable from this
cartridge": one daemon, real attached instance processes, and a real `status`.

## Steps

1. `.cartridge/tests/integration/native.ts`: drop `private` from `cli(args)`
   (`:78`) so a test can reach the base CLI in that daemon's own project and
   home. One word; no behaviour changes.
2. `.cartridge/tests/integration/instances.test.ts` (new, one test): one
   daemon, many `cartridge call` instances.
   - Two sessions, then six `buffers open` across them — two serial, four
     concurrent through `Promise.all` — and assert all six ids are distinct
     integers. Serial opens catch the two-compositions world (each node loads
     the store once at start and counts from the same seed, so each one's first
     buffer is the same id); the concurrent four catch a regression in the
     reservation under `state.next` (`lib.rs:1061-1064`).
   - `buffers list {session}` for each session returns exactly that session's
     ids and none of the other's; an unfiltered `buffers list` contains both.
   - `sessions update {id, name: "renamed"}` through one instance, then
     `sessions get` and `sessions list` through later instances read `renamed`
     back.
   - `cartridge status` with the daemon running holds exactly one entry with
     `id === "sessions"`, and its `state` is `"active"`. Both halves are
     load-bearing: a cartridge left out of the composition is still listed, in
     another state, so the count alone would pass with no node — and the count
     alone would also miss a second slot.
3. No change to `src/lib.rs`. Block 1 below pins the four lines that make the
   single store and single id space true, so a later edit that reintroduces a
   per-caller counter or a second `Store::load` fails collection.
4. Prototype: `attempt-1.patch`, both files, applies at `b896162` with `-p1`
   from the repo root. Validated in a clean detached worktree of `b896162`
   (`git apply --check` 0, `git apply` 0, test 0).

## Acceptance

- [x] Two attached instances calling sessions draw buffer ids from one space
      (no id is handed out twice), and a buffer opened under one session is
      never returned by a listing that names another session; an instance
      reaches another session's buffers only by asking — by that session's id,
      or by an unfiltered `buffers list`. (`instances.test.ts`: six ids across
      two sessions and six `cartridge call` processes, `new Set(ids).size ===
      ids.length`; each filtered listing equals its own session's ids; the
      unfiltered listing contains both. Proposed wording — see "Option
      chosen"; the PRD's literal second clause is about sessions, not
      instances, and no instance identity reaches this cartridge.)
- [x] A rename made through one instance is visible through the other.
      (`instances.test.ts`: `sessions update {name}` through one `cartridge
      call`, read back as `renamed` by `sessions get` and `sessions list`
      through later ones. "Rename" is `sessions update {id, name}`; sessions
      has no `rename` op, and the audit's "last rename wins" was the
      `std::fs::rename` snapshot commit at `lib.rs:394`.)
- [x] Exactly one sessions node exists with the daemon running.
      (`instances.test.ts`: `cartridge status` against the fixture's real
      daemon holds exactly one `id === "sessions"` entry, in state `"active"`.
      This is the count at this cartridge's own composed scope — one daemon,
      one profile, real instance processes. The whole-project count over all 20
      cartridges is the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` and is
      re-proven by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`,
      as the PRD's own box already says.)

## Verify and Proof

Both blocks were run verbatim as `sh -eu -c` in a clean worktree of `b896162`
with `attempt-1.patch` applied: block 1 exit 0, block 2 exit 0 (3.4 s cold
cargo build with a warm registry, 0.43 s test). Block 1 was also run in the two
worlds it denies — `STORE` replaced by a per-caller map, and a second
`Store::load` added — exit 1 in both.

Nothing here writes inside the footprint: `CARGO_TARGET_DIR` is outside the
repo, and the fixture builds its temp project under `$TMPDIR`.

```sh
# Static guards on the single store and the single id space. A negation is its
# own gating `if`, because `sh -e` ignores the status of a `!`-prefixed
# command; and every path is named by `test -f` first, because grep exits 2 on
# a missing file and a bare negation reads that as "no match".
test -f src/lib.rs
test -f .cartridge/tests/integration/instances.test.ts
test -f .cartridge/tests/integration/native.ts
# One store, opened once, and a second `start` is refused.
grep -qF 'static STORE: OnceLock<Arc<SharedStore>> = OnceLock::new();' src/lib.rs
grep -qF '.map_err(|_| "sessions already started".to_owned())?' src/lib.rs
# The counter is the store's, seeded from disk, reserved under its write lock.
grep -qF 'self.next = self.next.max(b.id + 1);' src/lib.rs
grep -qF 'state.next = state.next.checked_add(1).ok_or("buffer IDs exhausted")?;' src/lib.rs
# Exactly one call site loads the store. A second is a second in-memory copy.
test "$(grep -cF 'Store::load' src/lib.rs)" = 1
# sessions starts no host, node or child process of its own.
if grep -rn 'std::process::Command\|Command::new\|cartridge daemon' src/; then exit 1; fi
```

```sh
# One daemon, real attached `cartridge call` instances. ~4 s warm.
# The target dir is outside the repo, so no live cartridge is hot-restarted.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/sessions-one-id-space-verify}"
# `../cartridge.ctg` does not resolve from a lane, so the base binary is named
# absolutely with an env default, per the template.
CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}"
[ -x "$CARTRIDGE_BIN" ] || CARTRIDGE_BIN=/Users/feb/dev/cartridge/cartridge.ctg/target/debug/cartridge
test -x "$CARTRIDGE_BIN"
export CARTRIDGE_BIN
cargo build
SESSIONS_MODULE="$CARGO_TARGET_DIR/debug/libsessions.dylib"
[ -f "$SESSIONS_MODULE" ] || SESSIONS_MODULE="$CARGO_TARGET_DIR/debug/libsessions.so"
export SESSIONS_MODULE
bun test ./.cartridge/tests/integration/instances.test.ts
```

## Remaining risk

- `CARTRIDGE_BIN` falls back to an absolute path in the developer's checkout
  because the sibling cannot be reached from a lane. If neither build exists
  the block fails loudly on `test -x` rather than silently testing nothing.
  The binary must be new enough to carry the attach contract (`04aae7f` or
  later); an older one composes its own host per `call` and the test then fails
  on the id assertions, which is the right failure.
- `next` is recomputed as `max(buffer id) + 1` over what is *persisted*
  (`lib.rs:344`), so closing the highest-id buffer and restarting the daemon
  reuses that id. Pre-existing, unchanged by the one daemon, and outside these
  boxes ("no id reused across instances" is within one daemon's life). Worth
  its own PRD only if a buffer id is ever used as a durable reference.
- The one-node assertion is measured against this fixture's profile, which
  enables `sessions` once. A second *slot* was not constructed here: the mcp
  sibling measured that composing the same cartridge twice under one id breaks
  the daemon outright and under a different id leaves the second slot `failed`,
  so neither is the regression the box guards. `state === "active"` is what
  keeps the assertion from passing with the node absent.
- `native.ts` is shared by nine integration tests; making `cli` public changes
  nothing for them, but the file is now in this PRD's footprint, so anything
  else dirty in it at collection time rides in on the receipt.
- Two instances that deliberately name the same session id share its buffers.
  That is the design — the session is the scope — and it is what the proposed
  box-1 wording says.
