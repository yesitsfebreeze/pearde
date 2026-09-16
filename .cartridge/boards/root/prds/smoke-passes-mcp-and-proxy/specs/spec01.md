---
complexity: small
footprint:
  - .cartridge/tests/integration/smoke.test.ts
---

# spec01 — The composed smoke fixture matches the restructured composition

Baseline (analyst-1, 2026-09-16 ~10:40, before review round 2). At root 373ef5c every smoke target fails in
the stale fixture `.cartridge/tests/integration/smoke.test.ts` (ENOENT `<root>/builtin/...`).
A patched copy of the fixture passed policy, mcp and proxy with **HEAD** worktree builds of mcp.ctg (54e309c)
and proxy.ctg (1851ccf). That proof did not use HEAD for router.ctg or the host: both were used as already built.
As of round 2, other sessions hold uncommitted edits in proxy.ctg (5 files), router.ctg (3) and cartridge.ctg (4),
and the host binary (10:45:33) was built from that dirt. mcp.ctg is clean. This spec changes no submodule.

## Steps (all in `.cartridge/tests/integration/smoke.test.ts`)

1. Line 38: link `path.join(runtime, module)`, not `path.join(runtime, "builtin", module)`.
   The scratch `<profile>/builtin/` link dir stays as it is.
2. Line 23: the policy profile is `{{id="policy",path="policy.ctg"}}`.
3. Lines 32-36: delete the `name === "proxy" && module === "router"` stub branch. It never runs
   (the module is `router.ctg`) and uses an old API. The real router starts once step 4 is in.
4. Lines 43-50, config.lua: put every store under `.cartridge/`, like the root `.cartridge/config.lua`:
   sessions, memory, `router={listen={"127.0.0.1:0"},config_dir=".cartridge/credentials",data_dir=".cartridge/router"}`,
   `auth={credentials_dir=".cartridge/credentials",router_data_dir=".cartridge/router"}`, both live dirs,
   and `fs={store_dir=".cartridge/gitfs"}` in place of `gitfs={...}`. Drop `workspace`. router.ctg only grants
   writes to `$PROJECT/.cartridge` and `$HOME/.cartridge`, so root-level `credentials`/`router` fail with
   `router.ctg/init.lua:2 start: Operation not permitted (os error 1)`, and mcp and proxy go down with the router.
5. Isolation: `fs.realpathSync` the mkdtemp root (still under `os.tmpdir()`, which honours `TMPDIR`)
   and pass `CARTRIDGE_HOME=<root>` to every spawn (`run()` and the proxy daemon). Before the first spawn,
   run `[binary, "trust", runtime]` with that env (~60 ms), so the real `~/.cartridge` is neither read nor written.
6. mcp: `cartridge mcp` attaches to a detached per-project daemon (cartridge.ctg `src/cli/host.rs:68-138`).
   In a `finally`: run `[...command, "stop"]` with the same cwd and env. Then poll up to 30 s
   (`Bun.spawnSync(["pgrep", "-f", root]).exitCode !== 0`, 250 ms sleeps) until no process names the root.
   Only then `rmSync`. If the daemon is still there at 30 s, `kill` those pids and fail the test.
   An observed stop took ~16 s, so the test timeout stays at 90 s.
7. policy: `run policy null` now exits 2 at the host ("`policy` payload rejected by its schema").
   Assert a non-zero exit plus that text, instead of `decision == "deny"`.
8. mcp: assert that `tools.map(t => t.name)` includes `"memo"`.

Out of scope: "harness context injected" needs a model request, and the smoke memo excludes model requests.
The proxy check stays 401 without a key and 404 with it.

## Acceptance

- [ ] With clean working trees in mcp.ctg, proxy.ctg, router.ctg and cartridge.ctg, and their artifacts rebuilt
      from those trees, `just smoke policy`, `just smoke mcp` and `just smoke proxy` each exit 0. The gate log prints
      each tree's HEAD sha, so a pass proves the fixture against the committed HEAD of those four trees.
      While any of them is dirty, the gate fails at block 1 and collection waits for the owning session to commit.
- [ ] The mcp smoke lists a `memo` tool. No process naming this run's smoke temp dir is left, and the
      temp dir is removed, whether the smoke passes or fails.
- [ ] The fixture no longer links `<runtime>/builtin`.

## Verify and Proof

Each block runs with cwd /Users/feb/dev/cartridge under `sh -eu -c`, 120 s each. No block touches the
project daemon: the smoke daemons are keyed to scratch roots and use a scratch `CARTRIDGE_HOME`. There is no
dirty-tree fallback and no smoking of an existing artifact. The builds rebuild each clean tree. cargo
fingerprints sources, so an artifact built from since-reverted dirt is rebuilt. Observed incremental builds:
mcp 8 s, proxy 13 s. A cold proxy, router or host build can exceed 120 s. **Recovery:** run the same `cargo build`
command outside the gate (it takes the same cargo lock other sessions use), then re-verify. The host build also refreshes the binary
that `~/.local/bin/cartridge` points at. That is normal `just build runtime` behaviour, and a running daemon keeps its old image.

```sh
# 1 committed HEAD only: every tree the smoke executes must be clean
for s in mcp.ctg proxy.ctg router.ctg cartridge.ctg; do
  if [ -n "$(git -C "$s" status --porcelain)" ]; then
    echo "$s has uncommitted changes: wait for the owning session to commit, then re-verify" >&2; exit 1; fi
done
```

```sh
cargo build --lib --manifest-path mcp.ctg/Cargo.toml
```

```sh
cargo build --lib --manifest-path proxy.ctg/Cargo.toml
```

```sh
cargo build --lib --manifest-path router.ctg/Cargo.toml
```

```sh
cargo build --bin cartridge --manifest-path cartridge.ctg/Cargo.toml
```

```sh
# record the revisions smoked (and re-assert they are still clean)
for s in mcp.ctg proxy.ctg router.ctg cartridge.ctg; do
  test -z "$(git -C "$s" status --porcelain)" || { echo "$s became dirty during the gate" >&2; exit 1; }
  echo "$s $(git -C "$s" rev-parse HEAD)"
done
```

```sh
just smoke policy
```

```sh
t=$(cd "$(mktemp -d)" && pwd -P)
trap 'i=0; while pgrep -f "$t" >/dev/null; do i=$((i+1)); if [ $i -ge 30 ]; then echo "leaked smoke daemon under $t" >&2; pkill -f "$t" || true; rm -rf "$t"; exit 1; fi; sleep 1; done; rm -rf "$t"' EXIT
TMPDIR=$t just smoke mcp
```

```sh
t=$(cd "$(mktemp -d)" && pwd -P)
trap 'i=0; while pgrep -f "$t" >/dev/null; do i=$((i+1)); if [ $i -ge 30 ]; then echo "leaked smoke daemon under $t" >&2; pkill -f "$t" || true; rm -rf "$t"; exit 1; fi; sleep 1; done; rm -rf "$t"' EXIT
TMPDIR=$t just smoke proxy
```

```sh
# fixture shape
f=.cartridge/tests/integration/smoke.test.ts
if grep -n 'runtime, "builtin"' "$f"; then echo "fixture links <runtime>/builtin again" >&2; exit 1; fi
if ! grep -q 'CARTRIDGE_HOME' "$f"; then echo "fixture sets no CARTRIDGE_HOME" >&2; exit 1; fi
```
