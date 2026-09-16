---
complexity: small
footprint:
  - src/auth.rs
  - .cartridge/tests/unit/auth/tests.rs
---

# spec01 — pin the one refresh gate, and pin that only a router node can reach it

Base: router.ctg `65d22d7` ("Let a free route's payment refusal block its free
siblings").

**Footprint, settled.** The coordinator has added
`.cartridge/tests/unit/auth/tests.rs` to the PRD and to this spec's frontmatter.
That is the file `src/auth.rs:1238-1239` already pulls into the crate's test
build with `#[cfg(test)] #[path = ...] mod tests`, and the only file besides
`src/auth.rs` this spec writes; `collect` would have refused it otherwise.
Nothing further is needed here.

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
  one is spent. The compare-and-write at `:718` (`if map.get(&provider.name) ==
  Some(&original_auth)`) and `:732` (`if current == original_auth`) protects the
  *file* from being clobbered by a concurrent writer — it does **not** protect
  the *spend*, because the POST has already happened by the time the compare runs.
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
without presenting a refresh token to OpenAI for real. One seam fixes that — and
**which kind of seam is a security decision, not a style one.**

**The seam is compile-time (`#[cfg(test)]`), never an environment variable.**
Round 1 (F4) named the reason and it is decisive: `codex_token_endpoint()` is
called at refresh time inside the shipped cdylib, and the POST it addresses
carries the **live refresh token** in its body. A seam of the form
`std::env::var("ROUTER_CODEX_TOKEN_URL")` therefore lets anything that can set
one environment variable on the daemon — a launcher script, an `.envrc`, a shell
profile, an inherited environment when something else spawns the daemon — divert
that credential to an arbitrary URL, silently and over the network. The
`CLAUDE_CODE_EXECPATH` precedent (`:283`) is **not** the same trade: overriding a
binary path already presupposes code execution, while an env var reaches strictly
further. So:

- the shipped half is `#[cfg(not(test))] fn codex_token_endpoint() -> String {
  CODEX_TOKEN.to_owned() }` — **zero** production surface, and the string
  `ROUTER_CODEX_TOKEN_URL` does not exist anywhere in the crate;
- the test half is `#[cfg(test)]` over a
  `static CODEX_TOKEN_URL: std::sync::Mutex<Option<String>>`, reachable from the
  in-crate test module (`#[cfg(test)] #[path] mod tests`, `:1238-1239`, which
  opens with `use super::*`).

**Do not reinstate the environment variable.** Besides the production surface it
would reopen, `std::env::set_var` is what round 1 (F7) flagged as a latent
crash: `Auth::from_path` (`:160`) reaches `catalog::credentials`, which iterates
`std::env::vars()` (`catalog.rs:126`), and four sibling tests in this same binary
build an `Auth` concurrently (`tests.rs:16`, `:29`, `:49`, and
`proxy/capabilities.rs`). `setenv` racing `environ` iteration is exactly why Rust
2024 made `set_var` unsafe. The `static` has no such hazard: it is an ordinary
lock, the test holds it for the length of one refresh and clears it before its
asserts. Both findings close on this one change.

The seam also cannot redirect a **login**: the device-auth exchange at `:971`
keeps the bare `CODEX_TOKEN` const, so only the refresh path is observable.

## Steps

1. `src/auth.rs`: replace the duplicated literal at `:697` with
   `.post(codex_token_endpoint())`, and add `codex_token_endpoint()` next to
   `CLAUDE_CODE_MARGIN_SECS` as **two `cfg`-split halves**: `#[cfg(not(test))]`
   returning `CODEX_TOKEN.to_owned()`, and a `#[cfg(test)]` half reading a
   `#[cfg(test)] static CODEX_TOKEN_URL: std::sync::Mutex<Option<String>>` that
   falls back to the same const. `src/auth.rs` gains 26 lines and loses 1 (eight
   of them doc comment, three of them the test half's `static`); the shipped
   build is behaviour-identical to today, and the literal/const duplication is
   collapsed on the way. No environment variable is introduced — see "Option
   chosen".
2. `.cartridge/tests/unit/auth/tests.rs`: append
   `two_concurrent_refreshes_spend_the_refresh_token_once`
   (`#[tokio::test(flavor = "multi_thread", worker_threads = 4)]`), reusing the
   file's existing scratch-dir + `Auth::from_path` + synthetic-JWT pattern from
   `valid_oauth_requests_do_not_wait_for_the_store_writer`. A local axum server
   on `127.0.0.1:0` counts POSTs and returns one fixed, pre-computed rotated
   access token plus `refresh_token: "rotated-once"`; the test points
   `*CODEX_TOKEN_URL.lock().unwrap()` at it (and clears it, before the asserts,
   so a failure cannot leak the override); two `codex_headers` calls race on an
   expired stored token. Four assertions: the POST count is **1**; both callers'
   `authorization` header equals `Bearer <the rotated access token>` — not a
   rotation-invariant field such as `chatgpt-account-id`, which is copied
   verbatim out of the stored login (`codex_header_values`, `:748-753`) and
   cannot tell a fresh header from a stale one (round 1, F3); the two headers
   equal each other, which is the waiter reusing the winner's fresh token instead
   of its own expired one; and the stored `refresh_token` is the rotated one.
   Prototype in `attempt-2.patch`, which applies and passes clean at `65d22d7`.
3. Nothing else. No file lock, no change to the refresh logic itself, no change
   to the Claude Code or Copilot paths.

**Credential safety, both halves.** *The probe:* the test presents the string
`spend-me` to a loopback server. `codex_auth` (`:769-790`) prefers the store
entry when one exists, so writing the login into the scratch dir means the
`~/.codex/auth.json` branch at `:778` is never taken. Nothing reads the keychain,
nothing reads a real credential file, and no request leaves the machine.
*The product:* the override that makes the probe possible does not exist in a
shipped build at all — it is `#[cfg(test)]`, so the daemon's refresh POST can
only ever address `CODEX_TOKEN`. A test-only seam that redirects a live
credential in production would not be worth the proof it buys.

## Acceptance

- [x] Two concurrent refresh-triggering requests against one router node's
      `Auth` spend the refresh token exactly once: the token endpoint sees one
      POST, the stored `refresh_token` is rotated once, and both callers get
      working headers back.
      *(Narrowed, for the coordinator: the original box says "through the
      daemon". That two attached instances' requests both land on the daemon's
      one router node is a cartridge.ctg property — it belongs to the done
      sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently`
      and is re-proven composed by
      `the-composed-acceptance-test-…`. What router.ctg can prove, and what this
      box now says, is the other half: given one node, one spend. "Working
      headers" is checked as both callers' `authorization` carrying the rotated
      access token and equalling each other — not as `chatgpt-account-id`, which
      a rotation does not change.)*
- [x] No refresh code path in router.ctg can run outside a router node: the
      `auth` module is private to the crate, `Auth::from_path` has exactly one
      call site, that call site is `service::start`, its only caller is the Lua
      module entry, and the crate ships no binary.
      *(Narrowed, and the narrowing now matches the PRD: the Outcome says
      plainly that "one refresh token is never spent twice" is false while the
      `codex` and `claude` CLIs exist, so this box carries only the structural
      claim about router.ctg. It is **not** delegable to the attach sibling the
      way memory's daemon-wide clause was — a writer lock refuses a second
      holder, a refresh token is spent by whoever POSTs it, and the two spenders
      here never compose at all: the `codex` CLI rotates `~/.codex/auth.json`
      (`auth.rs:778`) and the `claude` CLI rotates the same keychain entry the
      subscription path reads (`:224-245`). `auth.rs:365-377` concedes it in
      shipped source.)*

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
# The pipe also means `set -e` sees `tee`, not cargo: this grep is what fails
# the block, so a collector observes exit 1 here, never cargo's 101.
grep -q 'test result: ok\. 1 passed; 0 failed' "$CARGO_TARGET_DIR/refresh-once.log"
```

```sh
# Box 2, structurally: nothing in this crate can refresh outside a router node.
# Every guard is positive and every path is proved present with `test -f` first.
# POSIX `set -e` ignores a `!`-prefixed command, so `! grep ...` can never fail
# a block (demonstrated: exit 0 on a tree that has the forbidden line); and
# `grep` on a missing file exits 2, which an `if` swallows — so a guard without
# its `test -f` passes on a deleted file (demonstrated for Cargo.toml).
test -f src/lib.rs
grep -q '^mod auth;' src/lib.rs
if grep -qn '^pub mod auth;' src/lib.rs; then exit 1; fi
test ! -d src/bin
test -f Cargo.toml
if grep -qn '^\[\[bin\]\]' Cargo.toml; then exit 1; fi
test -f src/service.rs
grep -q 'auth::Auth::from_path(' src/service.rs
test "$(grep -rn 'Auth::from_path(' src --include=*.rs | wc -l | tr -d ' ')" = 1
test -f src/module.rs
# One `service::start(` call site, and it is the Lua module entry — the count
# alone would accept a new caller elsewhere once `module.rs` stopped calling it.
test "$(grep -rn 'service::start(' src --include=*.rs | wc -l | tr -d ' ')" = 1
test "$(grep -rn 'service::start(' src --include=*.rs | grep -c '^src/module.rs:')" = 1
# The gate the audit named is still the single-flight gate, and the seam that
# makes it observable is compile-time: the shipped half returns the constant and
# no environment variable can redirect a POST that carries the refresh token.
test -f src/auth.rs
grep -q 'let gate = self.refresh.lock().await.entry(key).or_default().clone();' src/auth.rs
grep -q '.post(codex_token_endpoint())' src/auth.rs
grep -A1 '^#\[cfg(not(test))\]' src/auth.rs | grep -q 'fn codex_token_endpoint() -> String {'
# Anchored to the whole line, not a substring: a shipped half rewritten as
# `std::env::var("…").unwrap_or_else(|_| CODEX_TOKEN.to_owned())` keeps the
# const as a substring of its fallback and would otherwise pass (round 2, F8).
grep -A2 '^#\[cfg(not(test))\]' src/auth.rs | grep -qx '	CODEX_TOKEN.to_owned()'
if grep -qn 'ROUTER_CODEX_TOKEN_URL' src/auth.rs; then exit 1; fi
test -f .cartridge/tests/unit/auth/tests.rs
grep -q 'two_concurrent_refreshes_spend_the_refresh_token_once' .cartridge/tests/unit/auth/tests.rs
if grep -qn 'env::set_var' .cartridge/tests/unit/auth/tests.rs; then exit 1; fi
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
  guards (`auth.rs:718`, `:732`) and the "use the CLI's token while it works"
  rule (`:365-377`) are the mitigation and they are already in place; this spec
  neither improves nor weakens them.
- **The test override is process-global, but only within the test binary.**
  `CODEX_TOKEN_URL` is a `static`, set and cleared inside the one test. The only
  other test that calls `codex_headers`
  (`valid_oauth_requests_do_not_wait_for_the_store_writer`) holds a non-expired
  token (`exp = now + 3600`, `tests.rs:50`) and never reaches the endpoint, so a
  parallel run cannot collide; the whole `--lib` suite is green (58/58, five
  consecutive runs). If a future test refreshes, both will need one shared
  fixture endpoint — a `Mutex` serialising the two tests, not a second seam.
  Unlike the `std::env::set_var` form this replaced, a collision here would be a
  wrong URL, not a data race against `std::env::vars()`.
- **The Claude Code subscription path gets no test.** Its refresh endpoint
  (`CLAUDE_CODE_TOKEN`, `:32`) has no seam, and its gate (`:348`) is the same
  in-process shape the Codex test now pins. Adding a second seam for a second
  provider would pin the same property twice; if the coordinator wants it, it is
  one more `#[cfg(test)]`-split `*_token_endpoint()` and one more test, not new
  logic. It would also have to stay clear of `security` and the real keychain.
- **Box 2 is checked by greps, so it pins spellings.** `use crate::service::start;`
  followed by a bare `start(…)`, or a `[[bin]]` indented by a space, would slip
  past. What the guards pin is a spelling each, not the property behind it; they
  fire against the mutations they were built for (21/21, each against a tree
  built to fail it), and block 1 cannot even build if the seam or the gate is
  gone. The one guard that had to pin a *property* rather than a name — "the
  shipped half reads no environment" — is anchored to the whole line for that
  reason (round 2, F8); a substring match there passed a renamed-env-var mutant.
