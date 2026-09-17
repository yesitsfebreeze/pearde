---
complexity: S
footprint:
  - cartridge.ctg/src/cli/host.rs
  - cartridge.ctg/.cartridge/tests/unit/stdio.rs
---

# spec01 — the attach wait ends on the caller's listener, not on a repeated picture

## The defect, at the tree this was written against

`cartridge.ctg` is at `63ff234` with uncommitted work from other PRDs in the
shared checkout (an idle-timeout change adds 44 lines to `src/cli/host.rs`
above `settle_remote`). **The behaviour this PRD asks for is not present in that
dirty tree.** Both defect lines are intact, at the working-tree line numbers:

- `attach` — `cartridge.ctg/src/cli/host.rs:59`, still `attach(project: &Project)`
- the settle call — `:74`, `settle_remote(&found.0, settings.verify_timeout())`
- `settle_remote` — `:182`
- the three-identical-poll return — `:215`, `if stable >= 3 && !empty { return; }`

(at clean `63ff234` the last two are `:147` and `:180`; only the dirty
idle-timeout hunk moved them.)

On a cold host the composition holds one identical status picture for a few
hundred milliseconds while cartridges are still starting, so `stable >= 3` fires,
`attach` hands back a peer that cannot serve `mcp`, and `client::bail` fails with
``service `mcp` unavailable: no active listener``. Measured across rounds 1 and
2 with a fresh project root per run: **31 failures of 108 cold runs (29 %)** on
an unpatched binary, **0 of 35** on the prototype.

**Which deadline is the real one.** `attach`'s own loop is bounded by
`host.startup_timeout_secs` (60 s), but the `Ok(Some(found))` arm returns from
inside itself after calling `settle_remote(…, settings.verify_timeout())`, so
`attach`'s deadline never binds the settle. The only bound today is
`verify_timeout_secs` (default 300 s), whose own documentation in
`cartridge.ctg/.cartridge/settings.json` calls it a `verify` budget. Acceptance
box 2's "documented startup deadline" is therefore `host.startup_timeout_secs`,
and this spec moves the settle onto it. `verify_timeout()` keeps its three
in-process callers (`src/host/run.rs:37`, `src/host/run.rs:166`,
`src/cli/setup.rs:649`) untouched.

## The change

One guard in the shared function, not four at the call sites. All four `attach`
callers already know the key they are about to send (`run` has `key`, `launch`
has `"proxy"`, `mcp` and the `Backend` re-attach have `"mcp"`), so `attach` takes
`key: &str` — which repairs `cartridge run` and `cartridge launch` on a cold host
at the same time.

The per-poll decision moves into **one pure function** and the `stable`/`last`
counter is **deleted**:

```rust
/// Whether the wait can end on this status: a cartridge serving `key` is
/// active, or nothing is left starting and waiting longer cannot change that.
fn settled(status: &Value, key: &str) -> bool
```

`settle_remote(peer, key, timeout)` becomes a thin loop over it. Because the
decision is a pure function of one status, the deleted regression is not merely
removed but **unrepresentable**: there is no state in which "the same picture
three times" could be an answer. That is what the unit test pins, and it is why
this spec does not carry a probabilistic 15-cold-start fixture as a gate (see
"What is gated and what is not").

`status` already carries `state` and `listen` (`Status`, `src/host/mod.rs:38-48`),
which `explain` (`src/cli/host.rs:~228`) already reads the same way; two
three-line readers do not get a shared helper.

**Why only the CLI path changes.** The in-process sibling of this wait is
`Host::settled` (`src/host/run.rs:11`), a lifecycle-event wait with no poll
shortcut of its own — it is already correct, and it is what `verify`, contracts
and `setup` use through `verify_timeout()`. `settle_remote` exists only because a
CLI attaching over a socket cannot await those events. So the defect is confined
to the remote poll, `Host::settled` needs no change, and `verify_timeout()` keeps
its three in-process callers untouched.

**Bounding the poll itself.** `settle_remote`'s deadline is only checked
*between* `peer.call("status", …)` awaits, and `Peer::call`
(`src/transport/rpc.rs:239-257`) awaits an untimed oneshot, so a daemon that
answers its socket but never its status hangs the loop regardless of the
deadline. This change strictly increases the number of status polls on a cold
host, so each call is wrapped in `tokio::time::timeout(left, …)` where `left` is
the remaining budget. Without it, Acceptance box 2 ("fails within the documented
startup deadline") is aspirational rather than true. See "Overlap".

**Accepted cost.** When the key is never served *and* something stays
`starting`/`waiting`, the old code answered in ~300 ms and the new code waits to
`startup_timeout_secs` (60 s) before letting the caller fail. That is the point —
a still picture is not an answer — and it is the same budget a cartridge already
has to serve. The degraded compositions measured in round 1 (trust-refused
cartridges) do not reach it: they go `failed`, nothing is left `starting`, and
`settled` returns `true` at once.

Rejected: raising the poll count — a cold plateau has no bounded length, so no
count is safe. Rejected: waiting only until nothing is `starting`/`waiting`
without the key — it still hands back a peer that cannot serve the caller.

## Steps

0. Check the landing precondition first: `git -C cartridge.ctg status
   --porcelain -- src/cli/host.rs` must print nothing. If it does not, stop and
   report — see "Landing hazard" below. Do not stash, revert or partially commit
   another session's lines.
1. `attach(project: &Project, key: &str)`; update the four call sites
   (`run` → `key`, `launch` → `"proxy"`, `mcp` → `"mcp"`, `Backend::call`
   re-attach → `"mcp"`).
2. In `attach`, call `settle_remote(&found.0, key, settings.startup_timeout())`.
3. Add `fn settled(status: &Value, key: &str) -> bool`: `true` when an entry with
   `state == "active"` lists `key` in `listen`; `true` when the array is
   non-empty and no entry is `starting` or `waiting`; `false` otherwise
   (including an empty or non-array status).
4. Rewrite `settle_remote(peer, key, timeout)` as a loop that computes the
   remaining budget, wraps `peer.call("status", Value::Null)` in
   `tokio::time::timeout(left, …)`, keeps the existing untrusted-reload branch
   unchanged, returns when `settled(&status, key)`, sleeps 100 ms otherwise —
   and no longer holds `stable` or `last`.
5. Add four `#[test]` cases to the existing
   `cartridge.ctg/.cartridge/tests/unit/stdio.rs` (already `#[path]`-included
   into `src/cli/host.rs` as `stdio_tests`, and already the home of the pure
   `untrusted` test — no new file, no new module wiring):
   - `settled_when_the_key_is_active`
   - `settled_not_while_the_key_is_starting` — the defect case: the key's
     cartridge is `starting` while others are `active`; asserted `false`, and
     asserted `false` again for the identical value, which is the deleted
     three-poll shortcut expressed as a property.
   - `settled_when_nothing_is_left_starting` — the key never appears and every
     entry is `active`/`failed`; `true`, so the caller fails fast and `explain`
     names the cause.
   - `settled_not_on_an_empty_composition`
6. Run the gates with an isolated `CARGO_TARGET_DIR`.

A validated prototype of steps 1, 2 and 4 is
`prd.ctg/.cartridge/boards/root/.state/loop/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls/attempt-1.patch`
(41 insertions, 19 deletions, one file; `cargo clippy --all-targets
--all-features -- -D warnings` exit 0; 0 cold failures of 35). It applies to the
clean `63ff234` blob. It spells the predicate `serves` and keeps the
`starting`/`empty` computation inline in the loop; step 3 folds the two into
`settled` so the decision is testable as a unit. Nothing else about it changes.

## Acceptance

- [x] `attach` takes the caller's listener key and settles on `settings.startup_timeout()`; `cartridge.ctg/src/cli/host.rs` contains no `stable >= 3` return and no `settle_remote(&found.0, settings.verify_timeout())`.
- [x] `settled(status, key)` is a pure function of one status picture, so a repeated identical picture cannot end the wait: the unit cases above run and pass under `cargo test --bin cartridge`.
- [x] Each `peer.call("status", …)` in `settle_remote` is bounded by the remaining budget, so a daemon that answers its socket but never its status cannot hang the wait past `host.startup_timeout_secs`.
- [x] PRD box 2: in a composition that declares an `mcp` listener which never becomes active, `cartridge mcp` answers inside `host.startup_timeout_secs` (60 s) with an error naming `mcp`, rather than waiting out the deadline — block 5, measured at 2 s.
- [x] `just check cartridge`, `just test cartridge` and `just test lifecycle` exit 0.

## What is gated and what is not

The Verify blocks gate the **structure** of the fix (block 1), its **decision**
(block 2, four unit cases over the pure predicate), the **failure path** (block 5,
a composition whose `mcp` listener never becomes active) and the **repository
gates** (blocks 3, 4 and 6).

**They do launch hosts, and that is part of the evidence.** Block 6
(`just test lifecycle`) is `bun test .cartridge/tests/integration/takeover.test.ts`,
which runs 13 real daemon lifecycles under scratch roots with two tiny
cartridges — among them `two runs with no daemon share one`
(`.cartridge/tests/integration/takeover.test.ts:303`), a genuinely **cold**
`cartridge run` pair with no daemon, straight through the changed `attach` →
`settle_remote`, asserting exit 0; `a run against a socket that errors reports it
and starts nothing` (`:259`) and `a run during --replace starts no host of its
own` (`:316`) cross the same path. That is live cold-start coverage of a
two-cartridge composition already inside the gate at 47 s. Block 5 launches one
more. What the blocks avoid is the **live project daemon**: every host they start
is under a scratch root with an `XDG_RUNTIME_DIR` of its own, and every cargo
invocation writes to an isolated `CARGO_TARGET_DIR`, so no `*.ctg/target/debug`
dylib of this composition is touched and the project's daemon is neither rebuilt
nor restarted.

What they do not do is re-run a probabilistic cold-start sample.
Round 2 built a 15-cold-start `bun` fixture (preserved in git at
`specs/spec01.md`, revision before this one, and reachable as
`git log -p -- …/specs/spec01.md`). It is sound evidence and the implementer
should run it once as a probe, but it is not a good permanent gate here: it
builds the host binary and two cartridge dylibs inside 120 s blocks, spawns
fifteen daemons, depends on `sessions.ctg/target/debug/libsessions.dylib` being
built in the live tree, and its measured 31-41 s per eight runs assumes this
machine's `rustc-wrapper = "kache"`, which lives in `~/.cargo/config.toml` and
not in this repo. Re-run on a shared, dirty checkout by every later collect, it
is a flake generator that gates a race the patched code no longer has. The
structural gate is what makes the regression unrepresentable; the fixture is
what proved the race existed.

**Cold-start evidence remains the implementer's obligation**, recorded in the
collect receipt, not a Verify block: run the round-2 fixture (or the equivalent)
against the built binary and report the failure count, which must be 0 of 15.

## Landing hazard: `src/cli/host.rs` is dirty with another session's work

**This PRD cannot land while `cartridge.ctg/src/cli/host.rs` carries anyone
else's uncommitted lines, and today it does** — 44 insertions and 1 deletion of
`stop_when_idle` / `--idle-timeout` work from another session, in the same file
this change edits, among 18 dirty files in the submodule. Neither obvious route
works:

- committing from a clean worktree of `cartridge.ctg` produces a commit that
  `git merge --ff-only` will refuse to fast-forward into the live submodule while
  that file is locally modified there;
- committing from the live checkout carries the foreign 44 lines into this PRD's
  submodule commit, and `feet(prd)` cannot exclude them: from the superproject the
  whole footprint collapses to the single gitlink entry ` M cartridge.ctg`
  (`prd.ctg/src/planner.ts:5-9`), so collect cannot see inside the submodule at
  all and the receipt certifies whatever the submodule HEAD holds.

**Precondition, checked before any edit:**

```sh
git -C cartridge.ctg status --porcelain -- src/cli/host.rs
```

must print nothing. If it prints anything, **stop and report** — this PRD waits
for that work to commit. A hunk-level commit (`git add -p`) is **not** an
acceptable substitute: it produces a submodule tree that no one has built or
gated, and the receipt would certify it. Do not stash, revert or commit another
session's lines; the remedy is its owner committing them, not this PRD working
around them.

The same reasoning limits what the spec's own footprint buys: `feet(prd)` is the
union of prd.md's footprint and every spec's, so narrowing the spec to two files
does not narrow what collect guards while prd.md lists `cartridge.ctg`, and from
the superproject it resolves to the one gitlink either way. Every superproject PRD
over a submodule shares that property. The two-file list is an honest statement of
what the implementer touches, not a protection the engine enforces.

## Landing shape

**Collect with no lane.** The whole footprint is inside the `cartridge.ctg`
submodule while the PRD is a superproject row, and a superproject lane worktree
has empty submodules, so Verify pass 1 cannot build there. The coordinator
fast-forwards the live submodule and collects with no lane; the blocks below
therefore run **once, with cwd = `repo`**. That also makes the owner gates
(`just check/test <owner>`, which always gate the live submodule and never a
lane) correct rather than misleading here. The implementer works in a worktree of
`cartridge.ctg` with the sibling `*.ctg` directories symlinked beside it, or
`cargo build` cannot resolve the `../<sibling>.ctg` path dependencies.

## Overlap with `@root/an-attach-gives-up-on-a-daemon-that-answers-its-socket-but-never-its-status`

They touch the same wait and do not fight. That PRD fixes `Peer::call`'s untimed
oneshot in `src/transport/rpc.rs`, which is in its footprint and not in this
one, and which fixes every caller. This spec adds a local
`tokio::time::timeout(left, …)` around the status call only, because this change
increases the poll count and would otherwise make that hang easier to reach. The
`rpc`-layer fix makes the local wrapper redundant but harmless, and it can be
deleted then. Ship both, this one first.

## Remaining work outside this PRD

`.cartridge/tests/integration/smoke.test.ts` still pre-starts the daemon for its
mcp case, with a comment naming this PRD as the owner of that workaround. It is a
repo-root path outside this footprint, and widening to it would break the no-lane
landing shape above, so removing the workaround is a follow-up PRD.

## Verify and Proof

<!--
Engine facts (src/lifecycle.ts collect/verify):
- Each block runs as `sh -eu -c`, 120 s limit, empty stdin.
- With no lane it runs once, with cwd = `repo`. Paths are relative to the repo
  root; never `cd` to an absolute checkout.
- Pass 2 runs in the live checkout, where the host hot-restarts a cartridge when
  its `target/debug` dylib changes, so every cargo command exports an isolated
  `CARGO_TARGET_DIR` first. `target/` is git-ignored at the repo root and is
  outside this footprint.
- A block must not write inside the footprint; scratch goes to `mktemp`.
- `! grep …` is inert under `set -e`, so every negative guard is an explicit
  `if grep -qF …; then exit 1; fi`.
- Measured on this machine, 2026-09-17, against the live dirty checkout: block 1
  <1 s, block 2 <1 s, block 3 `just check cartridge` 4 s, block 4 `just test
  cartridge` 18 s (176 tests), block 5 `just test lifecycle` 47 s (13 tests).
  All five share one target dir, so whichever cargo block runs first pays the
  build; with `target/cartridge-mcp-waits-verify` already populated that build is
  incremental. The *cold* build of that directory was not timed here and, on a
  host without this machine's `rustc-wrapper = "kache"` (it lives in
  `~/.cargo/config.toml`, not in this repo), it is a full dependency build that
  can exceed the 120 s block limit — pre-warm it outside the blocks there with
  the target set blocks 3 and 4 actually build (`clippy --workspace
  --all-targets`, `nextest run --workspace`), not just the bin's test target:
  `CARGO_TARGET_DIR=$PWD/target/cartridge-mcp-waits-verify cargo nextest run
  --locked --manifest-path cartridge.ctg/Cargo.toml --workspace --no-run`.
- **Blocks 5 and 6 consume what block 4 built.** Neither compiles anything:
  `takeover.test.ts` resolves its binary as `${CARGO_TARGET_DIR}/debug/cartridge`
  and throws "Build the runtime first" rather than building it, and block 5 uses
  the same path. `cargo nextest run --workspace` in block 4 has the bin in its
  build graph and uplifts it (verified by moving the binary aside and re-running
  block 4). Keep blocks 4, 5 and 6 in this order; both later blocks fail loudly
  with the binary's path if it is ever absent.
- Blocks 5 and 6 start hosts, always under a scratch root whose socket is
  separated per-descriptor (`src/host/socket.rs:64-66`), with a short
  `XDG_RUNTIME_DIR` of its own as belt-and-braces, never the project's.
  Observed across a full run:
  the project daemon pid is unchanged, no `*.ctg/target/debug` directory and no
  `*.dylib` in the composition is written, and the submodule's dirty set is
  unchanged.
- Block 5 runs the binary with its cwd inside its own `mktemp -d` project,
  because `loader::root()` finds the project by walking up from the working
  directory. That is a scratch fixture, not a checkout: no block ever `cd`s to an
  absolute checkout, and with no lane each block runs once.
- `just check/test <owner>` always gates the live submodule, never a lane. With
  no lane that is exactly right, and it is one more reason the landing shape
  above is not optional.
-->

```sh
f=cartridge.ctg/src/cli/host.rs
t=cartridge.ctg/.cartridge/tests/unit/stdio.rs
test -f "$f"
test -f "$t"
if grep -qF 'stable >= 3' "$f"; then
  echo "settle_remote still ends the wait on three identical polls" >&2; exit 1
fi
if grep -qF 'settle_remote(&found.0, settings.verify_timeout())' "$f"; then
  echo "the attach settle still runs on verify_timeout_secs, a verify budget" >&2; exit 1
fi
if grep -qF 'async fn attach(project: &Project) -> Result<Attached>' "$f"; then
  echo "attach still takes no listener key" >&2; exit 1
fi
grep -qF 'settle_remote(&found.0, key, settings.startup_timeout())' "$f"
grep -qF 'fn settled(status: &Value, key: &str) -> bool' "$f"
grep -qF 'tokio::time::timeout(left, peer.call("status", Value::Null))' "$f"
grep -qF 'attach(project, "mcp")' "$f"
grep -qF 'attach(project, "proxy")' "$f"
grep -qF 'attach(&self.project, "mcp")' "$f"
for case in settled_when_the_key_is_active settled_not_while_the_key_is_starting \
  settled_when_nothing_is_left_starting settled_not_on_an_empty_composition; do
  grep -qF "fn $case()" "$t" || { echo "missing unit case $case" >&2; exit 1; }
done
# Forbidding `stable >= 3` by name would let a differently spelled early return
# back into the loop, which four cases over a pure predicate could not see. The
# rewritten body has exactly two: the status call's timeout arm and `settled`.
returns=$(awk '/^async fn settle_remote\(/{b=1} b&&/^\}/{b=0} b' "$f" | grep -c 'return;' || true)
if [ "$returns" -ne 2 ]; then
  echo "settle_remote has $returns returns, expected 2 (the status timeout and settled)" >&2
  exit 1
fi
echo "source guards ok"
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/cartridge-mcp-waits-verify}"
out=$(mktemp)
trap 'rm -f "$out"' EXIT
cargo test --locked --manifest-path cartridge.ctg/Cargo.toml --bin cartridge \
  -- settled_ > "$out" 2>&1 || { cat "$out" >&2; exit 1; }
cat "$out"
# A filter that matches nothing also exits 0, so require all four to have run.
for case in settled_when_the_key_is_active settled_not_while_the_key_is_starting \
  settled_when_nothing_is_left_starting settled_not_on_an_empty_composition; do
  grep -qF "stdio_tests::$case ... ok" "$out" || {
    echo "unit case $case did not run" >&2; exit 1; }
done
grep -qE 'test result: ok\. 4 passed' "$out"
echo "settled unit cases ok"
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/cartridge-mcp-waits-verify}"
just check cartridge
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/cartridge-mcp-waits-verify}"
just test cartridge
```

```sh
# Acceptance box 3, the failure path: a composition that declares an mcp
# listener which never becomes active must fail inside the startup deadline with
# a message naming it — not wait out 60 s, and not answer. Deterministic and
# cheap (2 s measured): the listener's cartridge fails at load, so nothing is
# left starting and settled returns at once. This is the regression gate on
# the accepted cost of deleting the shortcut; blocks 1 and 2 are what
# discriminate a patched tree from an unpatched one.
# The message this composition produces is `` `mcp` is not provided ``
# (JSON-RPC -32603, `src/error/mod.rs:31`), not the Outcome's ``service `mcp`
# unavailable: no active listener``: a *failed* cartridge leaves the event out
# of the active directory entirely (`src/host/mod.rs:805-807`) while a
# *starting* one leaves it present with no listener (`:840-849`). Both name
# `mcp`, which is what the box asks for.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/cartridge-mcp-waits-verify}"
bin="$CARGO_TARGET_DIR/debug/cartridge"
test -x "$bin" || { echo "the cartridge test block has not uplifted $bin" >&2; exit 1; }
root=$(mktemp -d)
rt=$(mktemp -d /tmp/ctgmcp-XXXXXX)
out=$(mktemp)
state=$(mktemp)
# This host's socket cannot be the project's: the separation is per-descriptor
# (`src/host/socket.rs:64-66` tags the socket by the scratch project's own
# descriptor), and the short runtime directory is belt-and-braces —
# `socket.rs:47-55` drops `XDG_RUNTIME_DIR` unless `<dir>/cartridge` is under
# 48 characters, which a bare `mktemp -d` exceeds on this platform.
export XDG_RUNTIME_DIR="$rt" CARTRIDGE_YOLO=1
trap '(cd "$root" && "$bin" stop >/dev/null 2>&1) || true; rm -rf "$root" "$rt" "$out" "$state"' EXIT
mkdir -p "$root/.cartridge" "$root/deaf.ctg"
cat > "$root/deaf.ctg/cartridge.json" <<'JSON'
{ "name": "deaf", "entry": "init.lua", "events": { "mcp": { "description": "declared, never served" } }, "listen": ["mcp"] }
JSON
printf 'error("deaf never serves")\n' > "$root/deaf.ctg/init.lua"
printf 'return {\n\t{ id = "deaf", path = "deaf.ctg" },\n}\n' > "$root/.cartridge/init.lua"
printf 'return {}\n' > "$root/.cartridge/config.lua"
(cd "$root" && "$bin" trust "$root") >/dev/null 2>&1 || true
start=$(date +%s)
printf '%s\n' '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | (cd "$root" && "$bin" mcp) > "$out" 2>&1 || true
elapsed=$(( $(date +%s) - start ))
cat "$out"
(cd "$root" && "$bin" status) > "$state" 2>&1 || true
grep -qF '"listen":["mcp"]' "$state" || { echo "the fixture never declared an mcp listener" >&2; cat "$state" >&2; exit 1; }
grep -qF '"state":"failed"' "$state" || { echo "the mcp listener did not stay inactive" >&2; cat "$state" >&2; exit 1; }
grep -qF '"error"' "$out" || { echo "cartridge mcp answered tools/list with no active listener" >&2; exit 1; }
grep -qF 'mcp' "$out" || { echo "the failure does not name the missing listener" >&2; exit 1; }
[ "$elapsed" -lt 60 ] || { echo "took ${elapsed}s; host.startup_timeout_secs is 60" >&2; exit 1; }
echo "the missing mcp listener was named in ${elapsed}s, inside the 60 s startup deadline"
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/cartridge-mcp-waits-verify}"
just test lifecycle
```
