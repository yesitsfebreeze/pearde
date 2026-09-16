---
complexity: small
footprint:
  - src/auth.rs
  - .cartridge/tests/unit/auth/tests.rs
---

# spec01 — pin the one refresh gate, and pin that only a router node can reach it

Base: router.ctg `65d22d7` ("Let a free route's payment refusal block its free
siblings").

**Footprint change requested.** The declared footprint is `src/auth.rs` alone.
The regression lives in `.cartridge/tests/unit/auth/tests.rs`, the file
`src/auth.rs:1238-1239` already pulls in with `#[cfg(test)] #[path = ...] mod
tests`. `collect` refuses a write outside the declared footprint, so the
coordinator must add that second path before this lands.

## Option chosen

**The audit's premise holds. The smallest honest answer is a seam plus the
regression it makes provable — not a file lock.**

Traced end to end at `65d22d7`:

- **The lock the audit names.** `auth.rs:282` at the audit revision (`d5ce669`)
  is `let gate = self.refresh.lock().await.entry(key).or_default().clone();`,
  now `src/auth.rs:686-687`. It is a `tokio::sync::Mutex` keyed per provider
  inside one `Auth` (`src/auth.rs:80`), so it serializes refreshes **inside one
  process and nowhere else**. What it guards is the Codex/ChatGPT refresh:
  `codex_headers` (`src/auth.rs:667-731`) POSTs the stored `refresh_token` to
  `https://auth.openai.com/oauth/token` (`:697`, a literal that duplicates the
  `CODEX_TOKEN` const at `:26`), then writes the rotated triple back — to the
  router's own `auth.json` under the write lock (`:715-727`), or to
  `~/.codex/auth.json` with a read-compare-write guard (`:728-737`).
- **What a refresh does to the stored token.** It **rotates** it:
  `auth["tokens"]["refresh_token"] = new["refresh_token"]` (`:708-712`). The old
  one is spent. The compare-and-write at `:723` / `:731-736` protects the *file*
  from being clobbered by a concurrent writer — it does **not** protect the
  *spend*, because the POST has already happened by the time the compare runs.
  Two processes therefore both spend, and the loser's grant is dead. The same
  shape holds for the Claude Code subscription path, gated by
  `refresh_claude_code` (`:348`), which rotates the keychain entry
  (`:456-478`). The Copilot path (`:602-655`) is **not** in scope: it exchanges a
  long-lived GitHub token for a short-lived Copilot token and rotates nothing, so
  a double exchange wastes a request and spends no credential.
- **The premise holds, and `config.lua` is why.** Two router nodes coexist on
  this project *by design today*: `.cartridge/config.lua:56-62` sets
  `listen = { "127.0.0.1:0" }` ("Each foreground chat owns a router; let
  concurrent chats coexist") over a shared `data_dir = ".cartridge/router"`. So
  neither a bound port nor the data dir stops a second node; two `Auth`s over one
  `auth.json`, each with its own in-process gate, is exactly the audited double
  spend. Only the one-daemon attach contract removes it.
- **No refresh path runs outside a router node — from inside this crate.**
  `mod auth;` is private in `src/lib.rs:9` (only `limits` and `protocol` are
  `pub`), so nothing outside the crate can construct an `Auth`; the one external
  consumer of the rlib, `proxy.ctg/src/{service,usage}.rs`, reaches only those
  two. `Auth::from_path` has exactly one call site in `src/`, `service.rs:51`,
  inside `service::start`, whose only caller is the Lua entry `module.rs:19-38`.
  `Cargo.toml` declares no `[[bin]]` and there is no `src/bin/`. There is no
  CLI-side refresh to route through the daemon and nothing to put a file lock
  around. `launch` (`service.rs` doc, `src/launch.rs`) hands an agent the
  proxy's address and a key; the agent speaks HTTP to the node, and the refresh
  stays server-side.
- **Why not the file lock the PRD offers as the alternative.** The PRD makes it
  conditional — "*If* any refresh path can still run outside the daemon". None
  does. A `flock` on `data_dir` would also not cover the two spenders that
  actually remain (the `codex` and `claude` CLIs, below), because they never look
  at the router's data dir. It would be code that buys nothing the attach
  contract does not already buy.

What is missing is the proof, and the proof is currently impossible: the token
endpoint at `:697` is a hardcoded literal, so there is no way to watch a refresh
without presenting a refresh token to OpenAI for real. One seam fixes that.

## Steps

1. `src/auth.rs`: add `codex_token_endpoint()` next to `CLAUDE_CODE_MARGIN_SECS`
   — `CODEX_TOKEN` unless `ROUTER_CODEX_TOKEN_URL` is set and non-empty — and use
   it at `:697` in place of the duplicated literal. This is the same env seam the
   file already uses for `CLAUDE_CODE_EXECPATH` (`:283`), and it collapses the
   literal/const duplication on the way. Eight lines; no behaviour change when
   the variable is unset.
2. `.cartridge/tests/unit/auth/tests.rs`: append
   `two_concurrent_refreshes_spend_the_refresh_token_once`
   (`#[tokio::test(flavor = "multi_thread", worker_threads = 4)]`), reusing the
   file's existing scratch-dir + `Auth::from_path` + synthetic-JWT pattern from
   `valid_oauth_requests_do_not_wait_for_the_store_writer`. A local axum server
   on `127.0.0.1:0` counts POSTs and returns a rotated pair; two `codex_headers`
   calls race on an expired stored token; the POST count must be **1**, both
   callers must get a usable header, and the stored `refresh_token` must be the
   rotated one. Prototype in `attempt-1.patch`, which applies and passes clean at
   `65d22d7`.
3. Nothing else. No file lock, no change to the refresh logic itself, no change
   to the Claude Code or Copilot paths.

**Credential safety, which is the point of the seam.** The test presents the
string `spend-me` to a loopback server. `codex_auth` (`:769-790`) prefers the
store entry when one exists, so writing the login into the scratch dir means the
`~/.codex/auth.json` branch at `:778` is never taken. Nothing reads the keychain,
nothing reads a real credential file, and no request leaves the machine.

## Acceptance

- [ ] Two concurrent refresh-triggering requests against one router node's
      `Auth` spend the refresh token exactly once: the token endpoint sees one
      POST, the stored `refresh_token` is rotated once, and both callers get
      working headers back.
      *(Narrowed, for the coordinator: the original box says "through the
      daemon". That two attached instances' requests both land on the daemon's
      one router node is a cartridge.ctg property — it belongs to the done
      sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently`
      and is re-proven composed by
      `the-composed-acceptance-test-…`. What router.ctg can prove, and what this
      box now says, is the other half: given one node, one spend.)*
- [ ] No refresh code path in router.ctg can run outside a router node: the
      `auth` module is private to the crate, `Auth::from_path` has exactly one
      call site, that call site is `service::start`, its only caller is the Lua
      module entry, and the crate ships no binary.
      *(Narrowed, for the coordinator: the original box says "no refresh code
      path runs outside the daemon's router node while a daemon is attached".
      This is **not** delegable to the attach sibling the way memory's
      daemon-wide clause was. A writer lock refuses a second holder; a refresh
      token is spent by whoever POSTs it, and two spenders here never compose at
      all — the `codex` CLI rotates `~/.codex/auth.json` (`auth.rs:778`) and the
      `claude` CLI rotates the same keychain entry the subscription path reads
      (`:224-245`). Neither is a cartridge instance and neither is reachable from
      any PRD on this board. `auth.rs:365-377` already concedes the point for
      Claude Code — it uses the CLI's stored token untouched while that token
      works, specifically so the router does not rotate the credential out from
      under the CLI. The box as written is unprovable and should not be claimed;
      the wording above is what is true and checkable.)*

## Verify and Proof

```sh
# The one refresh, watched. router.ctg has no path dependencies (Cargo.toml
# declares an empty [workspace] and every dep is from crates.io), so the lane
# needs no sibling *.ctg symlinks.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/router-refresh-once-verify}"
mkdir -p "$CARGO_TARGET_DIR"
cargo test --lib two_concurrent_refreshes_spend_the_refresh_token_once \
  2>&1 | tee "$CARGO_TARGET_DIR/refresh-once.log"
# A filter naming a missing, renamed or #[ignore]d test exits 0 with
# "running 0 tests"; only the summary proves this test ran. (The test's module
# path is `auth::tests::`, so `--exact` on the bare name filters everything out.)
grep -q 'test result: ok\. 1 passed; 0 failed' "$CARGO_TARGET_DIR/refresh-once.log"
```

```sh
# Box 2, structurally: nothing in this crate can refresh outside a router node.
# Every guard is positive — POSIX `set -e` ignores a `!`-prefixed command, so
# `! grep ...` can never fail a block (demonstrated: exit 0 on a tree that has
# the forbidden line).
test -f src/lib.rs
grep -q '^mod auth;' src/lib.rs
if grep -qn '^pub mod auth;' src/lib.rs; then exit 1; fi
test ! -d src/bin
if grep -qn '^\[\[bin\]\]' Cargo.toml; then exit 1; fi
test -f src/service.rs
grep -q 'auth::Auth::from_path(' src/service.rs
test "$(grep -rn 'Auth::from_path(' src --include=*.rs | wc -l | tr -d ' ')" = 1
test -f src/module.rs
test "$(grep -rn 'service::start(' src --include=*.rs | grep -v 'pub async fn start' | wc -l | tr -d ' ')" = 1
# The gate the audit named is still the single-flight gate, and the seam that
# makes it observable is still wired to the refresh POST.
test -f src/auth.rs
grep -q 'let gate = self.refresh.lock().await.entry(key).or_default().clone();' src/auth.rs
grep -q 'fn codex_token_endpoint() -> String {' src/auth.rs
grep -q '.post(codex_token_endpoint())' src/auth.rs
test -f .cartridge/tests/unit/auth/tests.rs
grep -q 'two_concurrent_refreshes_spend_the_refresh_token_once' .cartridge/tests/unit/auth/tests.rs
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/router-refresh-once-verify}"
cargo fmt --check
```

## Remaining risk

- **The `config.lua` contradiction is not fixed here and cannot be.**
  `.cartridge/config.lua:59` pins router to `127.0.0.1:0` precisely so
  "concurrent chats coexist". Under the one-daemon shape that setting is the last
  thing making the audited double spend reachable, and it is outside this PRD's
  repo entirely. Worth a line in the attach sibling or the composed test; not a
  router.ctg change.
- **External spenders stay out of reach.** `codex` and `claude` rotate the same
  credentials from outside any composition. The existing compare-and-write
  guards (`auth.rs:723`, `:731-736`) and the "use the CLI's token while it works"
  rule (`:365-377`) are the mitigation and they are already in place; this spec
  neither improves nor weakens them.
- **The env seam is process-global.** `ROUTER_CODEX_TOKEN_URL` is set and removed
  inside the one test. The only other test that calls `codex_headers`
  (`valid_oauth_requests_do_not_wait_for_the_store_writer`) holds a non-expired
  token and never reaches the endpoint, so a parallel run cannot collide; the
  whole `--lib` suite is green (58/58). If a future test refreshes, both will
  need one shared fixture endpoint instead.
- **The Claude Code subscription path gets no test.** Its refresh endpoint
  (`CLAUDE_CODE_TOKEN`, `:32`) has no seam, and its gate (`:348`) is the same
  in-process shape the Codex test now pins. Adding a second seam for a second
  provider would pin the same property twice; if the coordinator wants it, it is
  one more `*_token_endpoint()` and one more test, not new logic.
