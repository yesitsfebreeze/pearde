---
complexity: small
footprint:
  - .cartridge/tests/integration/smoke.test.ts
---

# spec01 — The composed smoke fixture matches the restructured composition

At committed HEAD (root 373ef5c, mcp 54e309c, proxy 1851ccf, cartridge cdd3124)
no product code blocks the smoke. Every failure is the stale fixture
`.cartridge/tests/integration/smoke.test.ts` plus stale dylibs. A patched copy
of the fixture passed policy, mcp and proxy against HEAD builds of mcp and proxy.

## Steps (all in `.cartridge/tests/integration/smoke.test.ts`)

1. Line 38: link `path.join(runtime, module)`, not `path.join(runtime, "builtin", module)`.
   There is no `<root>/builtin/`, so every target fails with ENOENT.
2. Line 23: the policy profile is `{{id="policy",path="policy.ctg"}}`.
3. Lines 32-36: delete the `name === "proxy" && module === "router"` stub branch.
   The module is now `router.ctg`, so the branch never runs, and its
   `apply=function(ctx)` stub uses an old API. The real router starts once step 4 is in.
4. Lines 43-50, config.lua: put every store under `.cartridge/`, like the root
   `.cartridge/config.lua`: sessions, memory, `router.config_dir=".cartridge/credentials"`,
   `router.data_dir=".cartridge/router"`, `auth={credentials_dir=".cartridge/credentials",router_data_dir=".cartridge/router"}`,
   both live dirs, and `fs={store_dir=".cartridge/gitfs"}` in place of the stale
   `gitfs={store_dir="gitfs"}`. Drop `workspace`. The router's grant only allows writes to
   `$PROJECT/.cartridge` and `$HOME/.cartridge`, so `credentials`/`router` at the
   project root fail with `router.ctg/init.lua:2 start: Operation not permitted (os error 1)`.
   That is the "sandbox" cause the 2026-09-15 attempt recorded. mcp and proxy both need the router.
5. Isolation: `fs.realpathSync` the mkdtemp root and pass `CARTRIDGE_HOME=<root>`
   to every spawn (`run()` and the proxy daemon). Before the first spawn, run
   `[binary, "trust", runtime]` with the same env (~60 ms). This writes a trust record
   in the scratch home only. Without it you get "is in no trusted project", and
   the real `~/.cartridge` is read.
6. mcp: `cartridge mcp` now attaches to a detached per-project daemon
   (cartridge.ctg `src/cli/host.rs:68-138`). The fixture never stops it, so each run leaks
   a `--dir <tmp>/mcp/builtin daemon` process. In a `finally`, run `[...command, "stop"]`
   with the same cwd and env *before* `rmSync`. The daemon takes ~16 s to exit after the stop.
7. policy: `run policy null` now fails at the host (exit 2, "`policy` payload rejected by its
   schema: null is not of type \"object\""). Assert a non-zero exit plus that text, instead of
   `decision == "deny"`.
8. mcp: also assert that `tools` includes `memo` (the PRD's "memo active").

Out of scope: "harness context injected" needs a model request, and the smoke
memo excludes model requests. The proxy check stays 401 without a key and 404 with it.

## Acceptance

- [ ] `just smoke policy`, `just smoke mcp` and `just smoke proxy` each exit 0 against clean, freshly built mcp.ctg and proxy.ctg.
- [ ] The mcp smoke lists a `memo` tool.
- [ ] The fixture uses no `builtin` root and sets `CARTRIDGE_HOME`. No smoke daemon is still running 30 s after the suite.

## Verify and Proof

Each block runs with cwd /Users/feb/dev/cartridge.

```sh
# 1 precondition: the smoke loads the dylibs in the submodules' own target/
test -z "$(git -C mcp.ctg status --porcelain --untracked-files=no)" || { echo "mcp.ctg dirty" >&2; exit 1; }
test -z "$(git -C proxy.ctg status --porcelain --untracked-files=no)" || { echo "proxy.ctg dirty" >&2; exit 1; }
```

```sh
# 2 fresh mcp dylib (a stale one rejects config key `band`). Not `just build`: that also relinks ~/.local/bin
cargo build --lib --manifest-path mcp.ctg/Cargo.toml
```

```sh
# 3 fresh proxy dylib
cargo build --lib --manifest-path proxy.ctg/Cargo.toml
```

```sh
just smoke policy
```

```sh
just smoke mcp
```

```sh
just smoke proxy
```

```sh
# fixture shape + no leaked daemon
f=.cartridge/tests/integration/smoke.test.ts
! grep -n '"builtin", module' "$f"
grep -q CARTRIDGE_HOME "$f"
grep -q '"memo"' "$f"
i=0; while pgrep -f 'cartridge-(mcp|proxy|policy)-smoke-.*daemon' >/dev/null; do i=$((i+1)); [ $i -lt 30 ] || { echo "leaked smoke daemon" >&2; exit 1; }; sleep 1; done
```
