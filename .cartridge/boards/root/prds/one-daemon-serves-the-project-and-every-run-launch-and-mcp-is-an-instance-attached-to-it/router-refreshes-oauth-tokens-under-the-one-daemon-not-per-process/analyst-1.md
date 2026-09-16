# analyst-1 — router refreshes OAuth tokens under the one daemon

Verdict: **SPECCED**. Base router.ctg `65d22d7`. Board `root`.

Drafts:
- `.state/loop/one-daemon-…/router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process/spec01.md`
- `.state/loop/one-daemon-…/router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process/attempt-1.patch`

**Footprint change needed:** add `.cartridge/tests/unit/auth/tests.rs` to the
declared footprint (currently `src/auth.rs` only). That file is already part of
the crate's test build via `#[cfg(test)] #[path = "../.cartridge/tests/unit/auth/tests.rs"]`
at `router.ctg/src/auth.rs:1238-1239`; `collect` would refuse the write without it.

## Code traced

- `router.ctg/src/auth.rs:686-687` — the gate the audit cites. At the audit
  revision `d5ce669` this is line 282 verbatim
  (`let gate = self.refresh.lock().await.entry(key).or_default().clone();`),
  confirmed with `git show d5ce669:src/auth.rs | sed -n '270,292p'`.
  It is a per-provider `tokio::sync::Mutex` inside one `Auth`
  (`src/auth.rs:80`): in-process only.
- `router.ctg/src/auth.rs:667-737` — `codex_headers`, what the gate guards. It
  POSTs the stored refresh token to a hardcoded
  `https://auth.openai.com/oauth/token` (`:697`, duplicating the `CODEX_TOKEN`
  const at `:26`) and **rotates** it (`:708-712`). The store write is guarded by
  compare-and-write (`:715-727` for the router's own `auth.json`, `:728-737` for
  `~/.codex/auth.json`) — that protects the file from clobber, **not** the spend:
  the POST has already happened when the compare runs.
- `router.ctg/src/auth.rs:338-390`, `:405-478` — the Claude Code subscription
  path. Same shape: in-process gate `refresh_claude_code` (`:348`), rotating
  write-back into the keychain entry (`:456-478`).
- `router.ctg/src/auth.rs:602-655` — the Copilot path. **Not** a rotation: a
  long-lived GitHub token is exchanged for a short-lived Copilot token. A double
  exchange wastes a request, spends no credential. Out of scope.
- `router.ctg/src/auth.rs:769-790` — `codex_auth`. Prefers the router's own store
  entry (`from_store = true`) and only falls back to `~/.codex/auth.json` at
  `:778` when no store entry exists. This is what makes a scratch-store probe
  safe.
- `router.ctg/src/service.rs:51` — the **only** `Auth::from_path` call site in
  `src/`, inside `service::start`.
- `router.ctg/src/module.rs:19-38` — `service::start`'s only caller, the
  `#[mlua::lua_module]` entry. `router.ctg/src/lib.rs:9` keeps `mod auth;`
  private (only `limits` and `protocol` are `pub`); `Cargo.toml` declares no
  `[[bin]]` and there is no `src/bin/`. The one external consumer of the rlib is
  `proxy.ctg/src/service.rs` / `usage.rs`, which reach only `protocol` and
  `limits`.
- `/Users/feb/dev/cartridge/.cartridge/config.lua:56-62` — the finding that
  settles the premise: router is configured `listen = { "127.0.0.1:0" }`
  ("Each foreground chat owns a router; let concurrent chats coexist") over a
  shared `data_dir = ".cartridge/router"`. Echoed at `.cartridge/init.lua:43-47`.

## Did the audit premise hold?

**Yes, fully** — the `mcp` sibling's shape, not the `agent` sibling's.

The gate is genuinely in-process, and two router nodes on one project are not
prevented by anything: the port is 0 by project configuration, and the two nodes
share one `auth.json`. Two `Auth` instances, two independent gates, one stored
refresh token → both POST it, the loser's grant is dead. Only the one-daemon
attach contract removes the second node.

## Does any refresh path run outside the daemon's router node?

**Not from inside router.ctg.** The `auth` module is crate-private, `Auth` is
constructed exactly once (`service.rs:51`), that construction is reachable only
through the Lua module entry, and the crate ships no binary. There is no
CLI-side refresh to route through the daemon and nothing to wrap in a file lock.
The PRD makes the file lock conditional on such a path existing; it does not, so
the spec does not add one.

**But two spenders remain outside every composition**, which is why box 2 is not
delegable the way memory's daemon-wide clause was: the `codex` CLI rotates
`~/.codex/auth.json` (the fallback at `auth.rs:778`) and the `claude` CLI rotates
the same keychain entry the subscription path reads (`auth.rs:224-245`). Neither
composes, neither is reachable from any PRD on this board, and a token — unlike a
writer lock — is spent by whoever POSTs it. `auth.rs:365-377` already concedes
this in prose: the router deliberately uses the CLI's stored token untouched
while it works, "spending the refresh token here rotates the credential out from
under the CLI".

## Boxes unprovable as written / proposed narrowing

- **Box 1** ("two concurrent refresh-triggering requests *through the daemon*").
  The "through the daemon" leg — that two attached instances' requests land on
  the *same* router node — is a cartridge.ctg property, delivered by the done
  sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently` and
  re-proven by `the-composed-acceptance-test-…`. Proposed wording: *"Two
  concurrent refresh-triggering requests against one router node's `Auth` spend
  the refresh token exactly once: one POST to the token endpoint, one rotation of
  the stored refresh token, and both callers get working headers back."* Proven
  by the new test.
- **Box 2** ("no refresh code path runs outside the daemon's router node while a
  daemon is attached"). Unprovable as written, and **should not be claimed** —
  the `codex` and `claude` CLIs falsify it and no board PRD can reach them.
  Proposed wording: *"No refresh code path in router.ctg can run outside a router
  node: the `auth` module is private to the crate, `Auth::from_path` has exactly
  one call site, that call site is `service::start`, its only caller is the Lua
  module entry, and the crate ships no binary."* Proven by the structural Verify
  block.

## How real credentials were kept out of every probe

No probe triggered a real OAuth refresh, and none read, copied or printed token
material.

- **No live daemon was touched.** No `daemon`, `launch`, `mcp`, `run` or routing
  request was issued, and the live checkout was never built in.
- **All work in a scratch worktree.** `git worktree add --detach` of `router.ctg`
  at `65d22d7` under the session scratchpad, with `CARGO_TARGET_DIR` pinned to a
  scratchpad path — never the live `target/`, so no cartridge hot-restarted.
- **The token endpoint is fake.** The prototype's seam
  (`ROUTER_CODEX_TOKEN_URL`) points the refresh POST at a local
  `127.0.0.1:0` axum server that counts requests and returns a synthetic rotated
  pair. No request left the machine; `auth.openai.com`,
  `api.anthropic.com` and `github.com` were never contacted.
- **The credential store is scratch.** The login is written into
  `std::env::temp_dir()/router-refresh-once-<hex>/auth.json` with the refresh
  token literal `spend-me`. Because `codex_auth` (`:769-790`) prefers a store
  entry, the `~/.codex/auth.json` branch at `:778` is never taken.
- **The keychain was never read.** No `security find-generic-password`, no
  `dump-keychain`, and no test exercises `claude_code_token` /
  `claude_code_refresh`. `CLAUDE_CODE_EXECPATH` was not set and no Claude Code
  binary was scanned.
- **No real `CARTRIDGE_HOME` involvement.** The test's `Auth::from_path` is
  handed the scratch dir for both `credentials` and `state`; nothing under
  `/Users/feb/dev/cartridge/.cartridge/router` or `.cartridge/credentials` was
  opened.
- **No `git add`, commit, push or reset** in the shared checkout; no `prd`
  transition; `prd.md` untouched.

## Commands and observed exit codes

All in `<scratch>/wt/router.ctg` unless noted; `<scratch>` =
`/private/tmp/claude-501/-Users-feb-dev-cartridge/0b0c3ecc-.../scratchpad`.

| # | command | exit |
|---|---|---|
| 1 | `git -C router.ctg log -1 --format='%H %s'` → `65d22d7` | 0 |
| 2 | `git show d5ce669:src/auth.rs \| sed -n '270,292p'` (confirm `auth.rs:282`) | 0 |
| 3 | `grep -rn 'router::' --include=*.rs` outside router.ctg → only `proxy.ctg/src/{service,usage}.rs` | 0 |
| 4 | `git worktree add --detach <scratch>/wt/router.ctg 65d22d7` | 0 |
| 5 | apply prototype (python3 edit of `src/auth.rs` + append to `.cartridge/tests/unit/auth/tests.rs`) | 0 |
| 6 | `cargo test --lib two_concurrent_refreshes_spend_the_refresh_token_once`, `CARGO_TARGET_DIR=<scratch>/target-router-verify` → `1 passed; 0 failed` | 0 |
| 7 | **non-vacuity A**: delete the gate outright → `error: field 'refresh' is never read` (`-D warnings`) | 101 |
| 8 | **non-vacuity B**: give each caller its own gate (simulating two processes), rerun test → `the refresh token is presented to the token endpoint exactly once; left: 2, right: 1` | 101 |
| 9 | restore `src/auth.rs`; `cargo fmt --check` | 0 |
| 10 | `cargo test --lib` (whole suite) → `58 passed; 0 failed` (baseline 57 + this one) | 0 |
| 11 | `git diff > attempt-1.patch` (131 lines) | 0 |
| 12 | **Verify block 2** (structural guards) against the patched tree | 0 |
| 13 | **Verify block 2 guards** against a pristine `65d22d7` worktree (should fail) | **1** |
| 14 | **negative guard** `if grep -qn '^pub mod auth;' src/lib.rs; then exit 1; fi` against a tree edited to `pub mod auth;` (should fail) | **1** |
| 15 | **counter-demo** `sh -eu -c 'test -f src/lib.rs; ! grep -q "^pub mod auth;" src/lib.rs; echo reached-end'` on that same failing tree → printed `reached-end` | **0** (confirms `set -e` ignores `!`) |
| 16 | **Verify block 1** as written (`sh -eu -c`, lane-local `CARGO_TARGET_DIR`, summary grep) | 0 |
| 17 | **Verify block 3** as written (`cargo fmt --check`) | 0 |

Build timing for the collector's 120 s budget: the crate compiles in **8.5 s**
into a fresh `CARGO_TARGET_DIR` with a warm cargo registry; the first fully cold
build (all dependencies) finished in **12.3 s**. Well inside the limit.

## Remaining work / risk

- Coordinator must widen the footprint to include
  `.cartridge/tests/unit/auth/tests.rs` before this can collect.
- `.cartridge/config.lua:59` (`listen = { "127.0.0.1:0" }`, "let concurrent chats
  coexist") is what keeps the audited double spend reachable and is outside this
  repo. It belongs in the attach sibling or the composed test, not here.
- `ROUTER_CODEX_TOKEN_URL` is process-global; the one test sets and removes it,
  and the only other `codex_headers` test holds a non-expired token so it never
  reaches the endpoint. A second refreshing test would need a shared fixture.
- The Claude Code subscription refresh gets no test: its endpoint has no seam and
  its gate is the same in-process shape. Pinning it would be a second
  `*_token_endpoint()` and a second test, no new logic — say so if wanted.
