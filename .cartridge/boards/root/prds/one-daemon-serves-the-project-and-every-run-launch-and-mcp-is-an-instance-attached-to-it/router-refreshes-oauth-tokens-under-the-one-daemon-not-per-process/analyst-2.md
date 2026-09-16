# analyst-2 — round-1 revision (87/100, no blocking findings)

Verdict: **SPECCED** (revised). Base router.ctg `65d22d7`, unchanged. Board
`root`. Scope, base, footprint, option chosen and both narrowings all kept.

Artifacts:
- `specs/spec01.md`, revised in place (frontmatter untouched, boxes still
  unticked).
- `.state/loop/…/attempt-2.patch` — **new file beside `attempt-1.patch`**, which
  is left as the round-1 record. `attempt-2.patch` is 2 files, +136/−1
  (`src/auth.rs` +26/−1, `.cartridge/tests/unit/auth/tests.rs` +110). `git apply
  --check` on a pristine `65d22d7` worktree: exit 0.
- `prd.md`: **not edited.** F1 was already closed by the coordinator's Outcome
  rewrite; nothing else in the review needed a body change.

## How each finding is closed

**F4 + F7 — the env seam is gone; the seam is now compile-time.** This is the
one that mattered and it is a security change, not a style one.
`codex_token_endpoint()` ships in the daemon and is read at refresh time, and the
POST it addresses carries the live refresh token, so a single environment
variable would divert that credential to any URL, silently, over the network.
The `CLAUDE_CODE_EXECPATH` precedent does not cover it: a binary override already
presupposes code execution, an env var does not.

The function is now two halves:

- `#[cfg(not(test))] fn codex_token_endpoint() -> String { CODEX_TOKEN.to_owned() }`
  — zero production surface. `grep -rn 'ROUTER_CODEX_TOKEN_URL' src .cartridge/tests`
  → **no match** (exit 1): the string does not exist anywhere in the crate.
- `#[cfg(test)] static CODEX_TOKEN_URL: std::sync::Mutex<Option<String>>` plus a
  `#[cfg(test)]` half reading it, reachable from the in-crate test module
  (`#[cfg(test)] #[path] mod tests` at `auth.rs:1238-1239`, which opens with
  `use super::*`).

F7 closes with it: the test sets `*CODEX_TOKEN_URL.lock().unwrap()` instead of
`std::env::set_var`, so nothing races the `std::env::vars()` scan that
`Auth::from_path` → `catalog.rs:126` performs in four concurrently-running
sibling tests. Both seam and race are gone, confirmed by grep (no `set_var` in
the test file, no `ROUTER_CODEX_TOKEN_URL` in the crate) and by a clean
non-test `cargo build` (exit 0 under `[lints.rust] warnings = "deny"`, so the
`#[cfg(test)]` static leaves no dead-code warning in a shipped build).
The reasoning is recorded in the spec's **"Option chosen"** under a heading that
says not to reinstate the variable, with both the production-surface argument and
the `set_var` race spelled out, so a later reader cannot undo it by accident.
Two new Verify guards pin it mechanically (below).

**F1 — already fixed by the coordinator; the spec now agrees with the Outcome.**
The new Outcome scopes the claim to "every refresh **that router.ctg performs**"
and states plainly that "one refresh token is never spent twice" is false while
the `codex` and `claude` CLIs exist. Box 2's parenthetical in the spec used to
carry that concession and argue against the PRD; it now defers to the Outcome and
keeps only the structural claim plus the not-delegable reason. No contradiction
remains in either direction.

**F2 — stale footprint instruction.** The spec's bold "Footprint change
requested … the coordinator must add that second path" is replaced with
"Footprint, settled", recording that the coordinator already added
`.cartridge/tests/unit/auth/tests.rs` and keeping the `:1238-1239` rationale.

**F3 — box 1's "working headers" is now checked by something a rotation
changes.** The server returns one fixed, pre-computed access token; the test
asserts `first["authorization"] == format!("Bearer {fresh}")` and
`second["authorization"] == first["authorization"]`. The old
`chatgpt-account-id == "test"` asserts stay (they are cheap and still true) but
are no longer load-bearing. Non-vacuity demonstrated, see nv3 below.

**F5 — guard 10 no longer counts a spelling.** The inert `grep -v 'pub async fn
start'` filter is dropped (it never matched `service::start(` anyway). Two
guards now: total `service::start(` count `= 1`, and
`grep -c '^src/module.rs:'` `= 1`, so the one call site must *be* the Lua module
entry. Demonstrated against a tree where `module.rs` stopped calling it and
`proxy.rs` started: the new guard exits **1**, the old one exits **0**.

**F6 — the `[[bin]]` guard can no longer go quiet.** `test -f Cargo.toml` added
before it. Demonstrated on a tree with `Cargo.toml` removed: the bare guard
exits **0** (reproduced), the guarded pair exits **1**.

Also carried, from the review's §1 and §5 remarks: the compare-and-write cites
are corrected from `:723`/`:731-736` to `:718`/`:732` (both places), and the
spec now says explicitly that the device-auth login at `:971` keeps the bare
`CODEX_TOKEN` const, so the seam can only ever redirect a *refresh*, never a
login. Remaining risk gains a note that box 2's greps pin spellings.

## The evidence-table correction the reviewer asked for

Round 1's analyst table recorded `101` for the two non-vacuity rows. That is
`cargo test`'s status, not the block's: block 1 pipes cargo into `tee`, so
`set -e` sees `tee` (0) and it is the summary `grep` that fails the block. **A
collector observes 1.** Every number in this report is the block's exit, as the
collector sees it, and the spec's block 1 now says so in a comment.

## Verify block 2 — every guard against a tree built to fail it

Each guard run alone, `sh -eu -c`, in a throwaway copy of the patched worktree
mutated to break exactly that guard. Guards are in block order.

| # | guard | tree built to fail it | exit |
| ---: | --- | --- | ---: |
| 1 | `test -f src/lib.rs` | `src/lib.rs` removed | **1** |
| 2 | `grep -q '^mod auth;' src/lib.rs` | renamed to `mod authx;` | **1** |
| 3 | `if grep -qn '^pub mod auth;' …; then exit 1; fi` | `pub mod auth;` | **1** |
| 4 | `test ! -d src/bin` | `src/bin/` created | **1** |
| 5 | `test -f Cargo.toml` *(new, F6)* | `Cargo.toml` removed | **1** |
| 6 | `if grep -qn '^\[\[bin\]\]' Cargo.toml; then exit 1; fi` | `[[bin]]` appended | **1** |
| 6b | same guard **alone** (round-1 form) | `Cargo.toml` removed | **0** — F6 reproduced |
| 6c | `test -f Cargo.toml` + that guard | `Cargo.toml` removed | **1** — F6 fixed |
| 7 | `test -f src/service.rs` | removed | **1** |
| 8 | `grep -q 'auth::Auth::from_path(' src/service.rs` | renamed to `Auth::make(` | **1** |
| 9 | `Auth::from_path(` count `= 1` | second site added in `proxy.rs` | **1** |
| 10 | `test -f src/module.rs` | removed | **1** |
| 11 | `service::start(` count `= 1` | second caller added in `proxy.rs` | **1** |
| 12 | `grep -c '^src/module.rs:'` `= 1` *(new, F5)* | call moved out of `module.rs` into `proxy.rs`, total still 1 | **1** |
| 12b | round-1 guard 10 (inert `grep -v`) | same tree | **0** — F5 reproduced |
| 13 | `test -f src/auth.rs` | removed | **1** |
| 14 | gate line present | per-caller gate substituted | **1** |
| 15 | `.post(codex_token_endpoint())` present | reverted to `.post(CODEX_TOKEN)` | **1** |
| 16 | `grep -A1 '^#\[cfg(not(test))\]' … \| grep -q 'fn codex_token_endpoint…'` *(new, F4)* | env-var seam restored verbatim | **1** |
| 17 | `grep -A2 '^#\[cfg(not(test))\]' … \| grep -q 'CODEX_TOKEN.to_owned()'` *(new, F4)* | env-var seam restored verbatim | **1** |
| 18 | `if grep -qn 'ROUTER_CODEX_TOKEN_URL' src/auth.rs; then exit 1; fi` *(new, F4)* | env-var seam restored verbatim | **1** |
| 19 | `test -f .cartridge/tests/unit/auth/tests.rs` | removed | **1** |
| 20 | test name present | test renamed | **1** |
| 21 | `if grep -qn 'env::set_var' …tests.rs; then exit 1; fi` *(new, F7)* | `std::env::set_var` restored | **1** |

**21 / 21 fire**, and the two round-1 holes reproduce at exit 0 before the fix.
No guard anywhere is `!`-prefixed; both negatives use `if …; then exit 1; fi`;
every path is preceded by `test -f` (or `test ! -d`).

## Commands and observed exit codes

`SP` = `/private/tmp/claude-501/-Users-feb-dev-cartridge/0b0c3ecc-…/scratchpad/analyst2`
(my own private subdirectory; extracted Verify blocks live in `$SP/blocks` and
`$SP/xblocks`, not in the shared scratchpad root). `$SP/wt` and `$SP/base` are my
own detached worktrees of `router.ctg` at `65d22d7`. Every cargo command ran with
an isolated `CARGO_TARGET_DIR` (`$SP/target`, `$SP/target-build`, or the block's
own `target/router-refresh-once-verify` inside a scratch worktree). The live
`router.ctg` checkout was never built in and never written.

| # | command | exit |
| ---: | --- | ---: |
| 1 | `git -C router.ctg log -1` → `65d22d7…`, working tree clean | 0 |
| 2 | `git worktree add --detach $SP/wt 65d22d7`; same for `$SP/base` | 0 |
| 3 | `git -C $SP/wt apply attempt-1.patch` → exactly the two footprint files | 0 |
| 4 | edit `src/auth.rs`: `#[cfg(not(test))]` / `#[cfg(test)]` split, `static CODEX_TOKEN_URL` | 0 |
| 5 | edit `tests.rs`: static override, fixed rotated token, F3 asserts, override cleared before the asserts | 0 |
| 6 | `CARGO_TARGET_DIR=$SP/target cargo test --lib two_concurrent_refreshes_spend_the_refresh_token_once` → `1 passed; 0 failed; 57 filtered out` | 0 |
| 7 | `CARGO_TARGET_DIR=$SP/target cargo test --lib` (full suite) → `58 passed; 0 failed` | 0 |
| 8 | full suite ×3 more → `58 passed; 0 failed` each, no flake | 0 |
| 9 | `CARGO_TARGET_DIR=$SP/target cargo fmt --check` | 0 |
| 10 | `CARGO_TARGET_DIR=$SP/target-build cargo build` (non-test cfg, `warnings = "deny"`) | 0 |
| 11 | `grep -rn 'ROUTER_CODEX_TOKEN_URL' src .cartridge/tests` → no match | 1 (no match) |
| 12 | `grep -rn 'cfg(not(test))' src --include=*.rs` → only `src/auth.rs:41` | 0 |
| 13 | `git -C $SP/wt diff > attempt-2.patch` (163 lines) | 0 |
| 14 | `git -C $SP/base apply --check attempt-2.patch` | 0 |
| 15 | 21 block-2 guards, each alone, each against a tree built to fail it | **1** ×21 |
| 16 | round-1 `[[bin]]` guard alone, `Cargo.toml` removed (F6) | **0** |
| 17 | round-1 guard 10 (inert `grep -v`), call moved out of `module.rs` (F5) | **0** |
| 18 | whole block 2, pristine `65d22d7` base | **1** |
| 19 | spec blocks 1/2/3 extracted verbatim from the revised `spec01.md`, run `sh -eu` on the patched tree | 0 / 0 / 0 |
| 20 | same three blocks on the pristine base | **1** / **1** / 0 (block 3 is a formatting gate, correctly green) |
| 21 | spec block 1, patched tree, **cold** `CARGO_TARGET_DIR` — 12 s wall | 0 |
| 22 | nv2 — each caller given its own gate (still reading `self.refresh`, so it compiles): `assertion left == right … exactly once / left: 2 / right: 1`, `FAILED. 0 passed; 1 failed` | **1** (cargo 101) |
| 23 | nv3 — server returns a token one character off the expected rotated one: `left: "Bearer e30.…x"` / `right: "Bearer e30.…"`, panic at the `authorization` assert *after* the `chatgpt-account-id` asserts passed — F3's check catches what the old one could not | **1** (cargo 101) |
| 24 | `git -C $SP/wt status --porcelain -uall` after every block — still exactly ` M .cartridge/tests/unit/auth/tests.rs`, ` M src/auth.rs` (`target/` is gitignored) | 0 |

Rows 22 and 23 are the block's exit as a collector sees it; cargo's own 101 is in
parentheses, per the correction above.

## How real credentials were kept out

No probe triggered a real OAuth refresh. Nothing here read, copied or printed
token material.

- **No real token endpoint was contacted.** `auth.openai.com`,
  `api.anthropic.com` and `github.com` were never reached. The only endpoint any
  test addressed was a local axum server on `127.0.0.1:0`, pointed at through the
  `#[cfg(test)]` static — which, being `#[cfg(test)]`, cannot even exist in a
  build that could reach a live provider.
- **The store was scratch, seeded with a dummy.** The login is written into
  `std::env::temp_dir()/router-refresh-once-<hex>/auth.json` with the refresh
  token literal `spend-me`, and `codex_auth` (`auth.rs:769-790`) prefers a store
  entry, so the `~/.codex/auth.json` fallback at `:778` is unreachable in this
  fixture. `~/.codex/auth.json` was never opened, read or listed.
- **The keychain was never touched.** No `security` invocation, no
  `CLAUDE_CODE_EXECPATH`, no Claude Code binary scan, and no test in the suite
  exercises `claude_code_token` / `claude_code_refresh`. I deliberately did not
  exercise the Claude Code subscription path at all, for exactly this reason.
- **Nothing ran against the live daemon.** No `daemon`, `launch`, `mcp`, `run`,
  `stop`, `--replace` or routing request; no `prd` state op; no `git add`, commit
  or push; no write to the live `router.ctg`, which is clean at `65d22d7`.
- **Every cargo command used an isolated `CARGO_TARGET_DIR`** under my own
  scratch directory or inside a scratch worktree, so no live cartridge
  hot-restarted.
- The one mutation that *could* have leaked a URL — an assertion failing while
  the override was set — is now impossible: the test clears
  `CODEX_TOKEN_URL` and aborts the server *before* its asserts.

## Remaining work / risk

- The `#[cfg(test)]` override is a process-global `static` within the test
  binary. Only one test refreshes today; the other `codex_headers` test holds a
  non-expired token (`exp = now + 3600`, `tests.rs:50`). A second refreshing test
  would need the two serialised, not a second seam. This is in the spec's
  Remaining risk.
- Box 2 is still checked by greps, so it pins spellings (`use crate::service::start;`
  then a bare `start(…)`, or an indented `[[bin]]`, would slip past). Noted in
  the spec; block 1 cannot build if the gate or the seam is actually gone.
- `.cartridge/config.lua:59` and the external `codex` / `claude` spenders are
  unchanged residuals, homed as in round 1.
