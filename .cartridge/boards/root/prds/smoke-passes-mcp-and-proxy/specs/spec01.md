---
complexity: small
footprint:
  - .cartridge/tests/integration/smoke.test.ts
---

# spec01 — The composed smoke fixture matches the restructured composition

Baseline (refreshed 2026-09-16 ~11:00, review round 4). Superproject gitlinks equal the submodule HEADs, and every tree is clean:
mcp.ctg 54e309c, proxy.ctg 96ef23c, router.ctg 943eef3, cartridge.ctg 771e046, memo.ctg 1634651. At root HEAD every
smoke target fails in the stale fixture `.cartridge/tests/integration/smoke.test.ts` (ENOENT `<root>/builtin/...`).
A probe fixture with steps 1-8 passed policy (2 s), proxy (7 s) and mcp (17 s). It used modules *copied* into
the scratch project with dylibs built into an isolated target dir, and a host built there too
(analyst scratchpad `probe/smoke-iso2.test.ts`). No live `target/` was written. This spec changes no submodule.

## Option chosen: isolated builds and copied modules

- cartridge.ctg 771e046 restarts a cartridge in a running host when a file in `native_candidates(root, name)` changes
  (`src/loader/document.rs:305-311`). That list is `<root>/lib<name>.dylib`, `<root>/target/release/…` and
  `<root>/target/debug/…` (`src/loader/mod.rs:65-85`). A rebuild into `<module>/target` would restart the live
  daemon's mcp, proxy and router.
- The host loads a native module from whatever directory the cartridge root resolves to (`src/node/mod.rs:363-368`,
  same candidate list). A copied module dir with its dylib at `<copy>/target/debug/` therefore loads (probe above).
  The scratch daemon watches the copy, never the live module.
- So every build uses `--target-dir "$HOME/.cache/cartridge-smoke-target/<tree>"`, never the live dir. The fixture
  copies the rebuilt modules into the scratch project, and `CARGO_TARGET_DIR` points the fixture at the isolated host
  (`smoke.test.ts:9` already honours it).
- Shared state: only the cargo target cache is shared between gate runs. cargo takes an exclusive file lock on a target
  dir for the whole build ("Blocking waiting for file lock on build directory"), so concurrent builds are serialized.
  Each build block copies its artifact into this run's own dir the moment cargo returns, and the smokes use that
  snapshot, so a later build by another run can't swap the artifact under this run. Per-run state (heads, live mtimes,
  snapshots) lives in `R=$HOME/.cache/cartridge-smoke-target/run.$PPID`. `$PPID` is the prd gate process, which
  spawns every block of one run (prd.ctg `src/lifecycle.ts:45`, `src/process.ts:17`), so it is stable within a run and
  distinct between concurrent runs.
- Measured with that persistent target starting empty (the cargo config's `kache` wrapper active): memo 6 s, mcp 3 s,
  proxy 7 s, router 13 s, host 8 s. Later runs reuse the target. **Recovery:** without a warm wrapper cache a cold
  build may exceed 120 s. Run the same command outside the gate once (it only fills `~/.cache/cartridge-smoke-target`),
  then re-verify.

## Steps (all in `.cartridge/tests/integration/smoke.test.ts`)

1. Line 38, module source: if `CARTRIDGE_SMOKE_BUILT` is set and `<CARTRIDGE_SMOKE_BUILT>/<module>/debug` exists,
   `fs.cpSync` the real `<runtime>/<module>` to the destination. Skip any path whose basename is `target`, `.git` or
   `node_modules`. Then copy every `*.dylib` from that `debug` dir into `<destination>/target/debug/`. Otherwise
   symlink `path.join(runtime, module)`, not `path.join(runtime, "builtin", module)`. The scratch
   `<profile>/builtin/` link dir stays as it is.
2. Line 23: the policy profile is `{{id="policy",path="policy.ctg"}}`.
3. Lines 32-36: delete the `name === "proxy" && module === "router"` stub branch. It never runs and uses an old API.
4. Lines 43-50, config.lua: put every store under `.cartridge/`, like the root `.cartridge/config.lua`:
   sessions, memory, `router={listen={"127.0.0.1:0"},config_dir=".cartridge/credentials",data_dir=".cartridge/router"}`,
   `auth={credentials_dir=".cartridge/credentials",router_data_dir=".cartridge/router"}`, both live dirs,
   and `fs={store_dir=".cartridge/gitfs"}` in place of `gitfs={...}`. Drop `workspace`. router.ctg grants writes
   only to `$PROJECT/.cartridge` and `$HOME/.cartridge`; the old root-level dirs made router start fail with EPERM.
5. Isolation: `fs.realpathSync` the mkdtemp root (under `os.tmpdir()`, which honours `TMPDIR`) and pass
   `CARTRIDGE_HOME=<root>` to every spawn. Before the first spawn, run `[binary, "trust", runtime]` with that env. The
   copies sit under the home, so they count as the person's own files.
6. mcp: spawn `[...command, "daemon"]` as a tracked child first. Poll `Bun.spawnSync([...command, "status"], { cwd, env, timeout: 2000 })`
   every 100 ms until the reply parses as a non-empty list with no entry `starting` or `waiting`. A non-zero exit or
   unparsable output means "not ready yet", not a failure. Stop polling once 20 s have passed (checked with `Date.now()`)
   and fail if the list never settled. Also fail if the child exits. Then run `mcp` through `run(..., killAfter = 25_000)`;
   it attaches to that daemon. In a `finally`, send SIGTERM to the child, SIGKILL after 10 s, and `await exited` before `rmSync`.
   Why: `cartridge mcp`'s `settle_remote` (cartridge.ctg `src/cli/host.rs:157`) returns after 3 unchanged polls while
   cartridges are still `starting`. That is owned by
   @root/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls, and this smoke
   does not cover the cold-start `cartridge mcp` path. A tracked child also means no detached daemon leaks.
7. policy: `run policy null` exits 2 at the host ("`policy` payload rejected by its schema"). Assert a non-zero exit plus that text.
8. mcp: assert that `tools.map(t => t.name)` includes `"memo"`.
9. Bounded waits, so every `finally` finishes inside its own test timeout (`run()` gets a `killAfter` parameter):
   - policy: 5 `run` calls with `killAfter` 10 s, plus trust (<1 s): ≤ 51 s against a 60 s test timeout.
   - mcp: copies and trust (≤ 2 s), a 20 s status deadline plus one last 2 s status call, a 25 s `mcp` run, and the
     10 s SIGKILL fallback: 2 + 22 + 25 + 10 = 59 s against an **explicit 75 s** test timeout.
   - proxy: replace the 300-iteration ready loop with a 20 s `Date.now()` deadline (1 s per fetch), then the 3 s
     authenticated fetch and the 10 s SIGKILL fallback: 2 + 21 + 3 + 10 = 36 s against a 60 s test timeout.

Out of scope: "harness context injected" needs a model request, and the smoke memo excludes model requests.
The proxy check stays 401 without a key and 404 with it. Modules other than mcp, proxy, router and memo
(sessions, harness, agent, …) are linked from their live dirs and loaded as built there. Loading never writes.

## Acceptance

- [x] With clean working trees in mcp.ctg, proxy.ctg, router.ctg, memo.ctg and cartridge.ctg whose HEADs are unchanged
      from before the builds until after the last smoke, and with their artifacts built into
      `~/.cache/cartridge-smoke-target` and snapshotted per run, `just smoke policy`, `just smoke mcp` and
      `just smoke proxy` each exit 0. The gate log prints each tree's HEAD and superproject gitlink. A pass proves the
      fixture against the committed HEAD of those five trees; the other composed modules run as built in their live dirs.
      A dirty tree fails block 1, and collection waits for its owner to commit.
- [x] The mtimes of the live `{mcp,proxy,router,memo}.ctg/target/debug/lib*.dylib` and `cartridge.ctg/target/debug/cartridge`
      are the same after the gate as before it.
- [x] The mcp smoke lists a `memo` tool. No process naming this run's temp dir is left, and the dir is removed,
      whether the smoke passes or fails.
- [x] The fixture no longer links `<runtime>/builtin`.

## Verify and Proof

Each block runs with cwd /Users/feb/dev/cartridge under `sh -eu -c`, 120 s each. The smokes use scratch roots, a scratch
`CARTRIDGE_HOME` and a snapshot of the isolated build. Builds never touch a live `target/`, so the project daemon
does not restart anything (block 12 checks this).

```sh
# 1 committed HEAD only; record this run's HEADs, gitlinks and live artifact mtimes
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; rm -rf "$R"; mkdir -p "$R/built"
for s in mcp.ctg proxy.ctg router.ctg memo.ctg cartridge.ctg; do
  if [ -n "$(git -C "$s" status --porcelain)" ]; then
    echo "$s has uncommitted changes: wait for the owning session to commit, then re-verify" >&2; exit 1; fi
  echo "$s head=$(git -C "$s" rev-parse HEAD) gitlink=$(git ls-tree HEAD "$s" | awk '{print $3}')" | tee -a "$R/heads"
done
stat -f '%m %N' mcp.ctg/target/debug/lib*.dylib proxy.ctg/target/debug/lib*.dylib router.ctg/target/debug/lib*.dylib memo.ctg/target/debug/lib*.dylib cartridge.ctg/target/debug/cartridge > "$R/live-mtimes" 2>/dev/null || true
```

```sh
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; C=$HOME/.cache/cartridge-smoke-target/memo.ctg
cargo build --lib --manifest-path memo.ctg/Cargo.toml --target-dir "$C"
mkdir -p "$R/built/memo.ctg/debug"; cp "$C"/debug/lib*.dylib "$R/built/memo.ctg/debug/"
```

```sh
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; C=$HOME/.cache/cartridge-smoke-target/mcp.ctg
cargo build --lib --manifest-path mcp.ctg/Cargo.toml --target-dir "$C"
mkdir -p "$R/built/mcp.ctg/debug"; cp "$C"/debug/lib*.dylib "$R/built/mcp.ctg/debug/"
```

```sh
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; C=$HOME/.cache/cartridge-smoke-target/proxy.ctg
cargo build --lib --manifest-path proxy.ctg/Cargo.toml --target-dir "$C"
mkdir -p "$R/built/proxy.ctg/debug"; cp "$C"/debug/lib*.dylib "$R/built/proxy.ctg/debug/"
```

```sh
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; C=$HOME/.cache/cartridge-smoke-target/router.ctg
cargo build --lib --manifest-path router.ctg/Cargo.toml --target-dir "$C"
mkdir -p "$R/built/router.ctg/debug"; cp "$C"/debug/lib*.dylib "$R/built/router.ctg/debug/"
```

```sh
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; C=$HOME/.cache/cartridge-smoke-target/cartridge.ctg
cargo build --bin cartridge --manifest-path cartridge.ctg/Cargo.toml --target-dir "$C"
mkdir -p "$R/host/debug"; cp "$C/debug/cartridge" "$R/host/debug/cartridge"
```

```sh
# 7 before the smokes: HEADs unchanged and still clean since block 1
R=$HOME/.cache/cartridge-smoke-target/run.$PPID
for s in mcp.ctg proxy.ctg router.ctg memo.ctg cartridge.ctg; do
  test -z "$(git -C "$s" status --porcelain)" || { echo "$s became dirty during the gate: re-verify" >&2; exit 1; }
  grep -q "^$s head=$(git -C "$s" rev-parse HEAD) " "$R/heads" || { echo "$s HEAD moved during the gate: re-verify" >&2; exit 1; }
done
cat "$R/heads"
```

```sh
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; t=$(cd "$(mktemp -d)" && pwd -P)
trap 'i=0; while pgrep -f "$t" >/dev/null; do i=$((i+1)); if [ $i -ge 10 ]; then echo "leaked smoke process under $t" >&2; pkill -KILL -f "$t" || true; sleep 2; rm -rf "$t"; exit 1; fi; sleep 1; done; rm -rf "$t"' EXIT
TMPDIR=$t CARGO_TARGET_DIR=$R/host CARTRIDGE_SMOKE_BUILT=$R/built just smoke policy
```

```sh
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; t=$(cd "$(mktemp -d)" && pwd -P)
trap 'i=0; while pgrep -f "$t" >/dev/null; do i=$((i+1)); if [ $i -ge 10 ]; then echo "leaked smoke process under $t" >&2; pkill -KILL -f "$t" || true; sleep 2; rm -rf "$t"; exit 1; fi; sleep 1; done; rm -rf "$t"' EXIT
TMPDIR=$t CARGO_TARGET_DIR=$R/host CARTRIDGE_SMOKE_BUILT=$R/built just smoke mcp
```

```sh
R=$HOME/.cache/cartridge-smoke-target/run.$PPID; t=$(cd "$(mktemp -d)" && pwd -P)
trap 'i=0; while pgrep -f "$t" >/dev/null; do i=$((i+1)); if [ $i -ge 10 ]; then echo "leaked smoke process under $t" >&2; pkill -KILL -f "$t" || true; sleep 2; rm -rf "$t"; exit 1; fi; sleep 1; done; rm -rf "$t"' EXIT
TMPDIR=$t CARGO_TARGET_DIR=$R/host CARTRIDGE_SMOKE_BUILT=$R/built just smoke proxy
```

```sh
# 11 after the smokes: HEADs still unchanged and trees still clean
R=$HOME/.cache/cartridge-smoke-target/run.$PPID
for s in mcp.ctg proxy.ctg router.ctg memo.ctg cartridge.ctg; do
  test -z "$(git -C "$s" status --porcelain)" || { echo "$s became dirty during the smokes: re-verify" >&2; exit 1; }
  grep -q "^$s head=$(git -C "$s" rev-parse HEAD) " "$R/heads" || { echo "$s HEAD moved during the smokes: re-verify" >&2; exit 1; }
done
```

```sh
# 12 no live target written; then drop this run's state
R=$HOME/.cache/cartridge-smoke-target/run.$PPID
test -f "$R/live-mtimes" || { echo "block 1 recorded no live mtimes" >&2; exit 1; }
stat -f '%m %N' mcp.ctg/target/debug/lib*.dylib proxy.ctg/target/debug/lib*.dylib router.ctg/target/debug/lib*.dylib memo.ctg/target/debug/lib*.dylib cartridge.ctg/target/debug/cartridge > "$R/live-mtimes.after" 2>/dev/null || true
if ! diff "$R/live-mtimes" "$R/live-mtimes.after"; then
  echo "a live target artifact changed during the gate: this gate never writes one, but another session's build (just build) also does; re-verify when no other build runs" >&2; exit 1; fi
rm -rf "$R"
```

```sh
# fixture shape
f=.cartridge/tests/integration/smoke.test.ts
if grep -n 'runtime, "builtin"' "$f"; then echo "fixture links <runtime>/builtin again" >&2; exit 1; fi
if ! grep -q 'CARTRIDGE_HOME' "$f"; then echo "fixture sets no CARTRIDGE_HOME" >&2; exit 1; fi
if ! grep -q 'CARTRIDGE_SMOKE_BUILT' "$f"; then echo "fixture ignores the isolated build" >&2; exit 1; fi
```

Worst case per smoke block: the test timeout (≤ 75 s, and the fixture's own cleanup always finishes inside it; see step 9),
plus a 10 s trap poll, plus 2 s, plus the just/bun preamble (~1 s) = 88 s, under 120 s. The trap's `pkill -KILL -f "$t"` is
a last resort that catches only processes whose argv names `$t`. The fixture's SIGTERM/await is the real cleanup.
If the gate stops before block 12, `run.$PPID` stays behind: small and harmless, and a run with the same `$PPID` clears it in block 1.
