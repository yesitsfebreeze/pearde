# @root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process review history

Plan: `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process`,
`prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process/prd.md`.
Scope: executable leaf — the router's OAuth refresh single-flight gate is the
right lock under one daemon, and nothing inside `router.ctg` can refresh outside
a router node.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: superproject `308378b` (dirty in memos and submodule
gitlinks, none in this PRD's footprint); `router.ctg` `65d22d7` (= `main`,
working tree clean). Prototype `attempt-1.patch` (2 files, +103/-1).

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process/prd.md` SHA-256 `d7d582910d86578166f0d861a0f86b54799c6c8726f78e853e65553cd27d3b57` |
| Specs | `specs/spec01.md` SHA-256 `a8be48e16e68965e5856fc9cca292a50e21aff01403c3b413d3f696ec181deda` |
| Parent rollup | `.../one-daemon-.../prd.md` SHA-256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445` |
| Analyst report | `.state/loop/.../analyst-1.md` SHA-256 `8df17f29783ebee2e8af1a42257ff9a70b9fa5311a23750496ce3558f2283a4f` |
| Prototype | `.state/loop/.../attempt-1.patch` SHA-256 `f855f4e7799ea80de60b9af293edf43f20ffd65d982ca0c6da9fec68d2509b17` |
| Material dependency | `an-instance-attaches-to-the-daemon-and-never-composes-silently` state `done` |
| Material input | `.cartridge/config.lua` SHA-256 `322e1e99c99048d73ef1631866457dcee90e84944d1e3b777b12ac0dbd73f77a` |
| Base | `router.ctg` `65d22d76dc4dec15a0aed2da24b79fa4b500767e` |
| Audit revision | `router.ctg` `d5ce669` (the audit's `auth.rs:282`) |

### How real credentials were kept out of every probe

No probe triggered a real OAuth refresh, and nothing in this review read, copied
or printed token material.

- **The token endpoint was never real.** Every execution of the new test ran
  against the prototype's `ROUTER_CODEX_TOKEN_URL` seam pointed at a local
  `127.0.0.1:0` axum counter. `auth.openai.com`, `api.anthropic.com` and
  `github.com` were never contacted, and no request left the machine.
- **The credential store was scratch.** The test writes its login into
  `std::env::temp_dir()/router-refresh-once-<hex>/auth.json` with the refresh
  token literal `spend-me`. I re-derived why that is sufficient rather than
  taking it on trust: `codex_auth` (`src/auth.rs:769-790`) returns the store
  entry with `from_store = true` whenever one exists, so the
  `~/.codex/auth.json` fallback at `:778` is unreachable in this fixture.
- **The keychain was never touched.** No `security` invocation, no
  `CLAUDE_CODE_EXECPATH`, and no test in the suite exercises
  `claude_code_token` / `claude_code_refresh` (verified: the only `codex_headers`
  callers in `.cartridge/tests/` are `tests.rs:70`, `:83`, `:206`, `:211`).
- **Nothing was run against the live daemon.** No `daemon`, `launch`, `mcp`,
  `run`, `stop`, `--replace` or routing request. No `prd` state op, no `git add`,
  no commit, no push, and no write to the live `router.ctg` checkout — which was
  and remains clean at `65d22d7`.
- **Every cargo command used an isolated `CARGO_TARGET_DIR`**, inside my own
  scratch worktrees (`<scratchpad>/rev/{patched,base}/target/router-refresh-once-verify`)
  or under `<scratchpad>/target-full*`. The live `router.ctg/target/` was never
  written, so no cartridge hot-restarted.
- I made my **own** worktrees (`<scratchpad>/rev/patched`, `<scratchpad>/rev/base`,
  both `git worktree add --detach … 65d22d7`) rather than trusting the analyst's
  registered `<scratchpad>/wt/router.ctg`.

Two things I did **not** verify, deliberately, and they are findings about the
plan rather than gaps in the evidence: I did not confirm that a real
`auth.openai.com` refresh rotates the token (the code says so at `:708-712`;
confirming it would spend a live grant), and I did not exercise the Claude Code
subscription path at all (`:412-478` shells out to `security` and would rotate
the user's real keychain entry).

### 1. The premise, claimed to hold fully — confirmed, including the ordering

Re-derived at `65d22d7` rather than accepted:

- `src/auth.rs:686-687` is `let gate = self.refresh.lock().await.entry(key).or_default().clone();`
  / `let _refresh = gate.lock().await;`. `refresh` is
  `Mutex<BTreeMap<String, Arc<Mutex<()>>>>` on `Auth` (`:80`), constructed once
  per `Auth` (`:165`), `tokio::sync::Mutex` (`use tokio::sync::Mutex`, `:14`).
  In-process only. `git show d5ce669:src/auth.rs | sed -n '278,290p'` puts the
  identical line at `:282`, so the audit cites this gate and nothing else.
- **The key sub-claim holds.** The POST is at `:696-701`; the rotation writes the
  new triple into `auth["tokens"]` at `:708-712`; the compare-and-write runs at
  `:718` (`if map.get(&provider.name) == Some(&original_auth)`) and `:732`
  (`if current == original_auth`). Both compares are strictly *after* the POST
  has returned. A second node therefore does not lose a race and retry — it has
  already spent the refresh token by the time it discovers the file moved, and
  the loser's grant is dead. This is what makes it a double spend, and the spec
  states it correctly.
- Correctly scoped out: the Copilot path (`:602-655`) exchanges rather than
  rotates; and — a point the spec earns but does not make explicitly — the
  device-auth login at `:971` keeps the bare `CODEX_TOKEN` const, so the seam
  cannot redirect a login exchange, only a refresh.

Minor cite drift: the PRD's Planning note and the spec both call the
compare-and-write `:723` / `:731-736`. `:723` is the `.get()` inside the
*else* of that compare; the compares themselves are `:718` and `:732`. The
claim is right, the line is not.

### 2. Two router nodes coexist by configuration — confirmed

`.cartridge/config.lua:56-62` reads verbatim:

```
router = {
	-- Each foreground chat owns a router; let concurrent chats coexist.
	-- The router passes its assigned address to launched clients.
	listen = { "127.0.0.1:0" },
	config_dir = ".cartridge/credentials",
	data_dir = ".cartridge/router",
},
```

So neither a bound port nor the data dir excludes a second node, and both
`config_dir` (where `catalog::credentials` reads) and `data_dir` (where
`auth.json` lives, `auth.rs:162`) are shared. `.cartridge/init.lua:41-47` says
the same thing in prose ("two hosts of this one profile coexist instead of
fighting over an address"). The analyst's conclusion — only the attach contract
removes the second node — is correct, and its residual is homed correctly
(attach sibling or composed test, not here).

### 3. No out-of-node refresh path inside router.ctg — every leg checked

| Leg | Observed at `65d22d7` |
| --- | --- |
| `mod auth;` crate-private | `src/lib.rs:9`; only `limits` (`:17`) and `protocol` (`:19`) are `pub` |
| `Auth::from_path` call sites | exactly one: `src/service.rs:51` |
| that call site is `service::start` | `pub async fn start` at `src/service.rs:34`, `:51` inside it |
| `service::start`'s only caller | `src/module.rs:26`, inside `fn start(lua, config)`, reachable only from `#[mlua::lua_module] fn router` (`:58-74`) |
| no `[[bin]]`, no `src/bin` | `Cargo.toml` declares `[lib]` only; `ls src` has no `bin/` |
| no path dependencies | every dep is a crates.io version; `[workspace]` is empty — so the lane needs no sibling `*.ctg` symlinks, and a lone worktree does build (I built two) |

The PRD's file-lock branch is conditional on such a path existing. It does not,
so the spec is right to add none, and a `flock` on `data_dir` would in any case
not cover the two spenders that do remain.

### 4. The two narrowed boxes

**Box 1 — narrowing accepted.** Dropping "through the daemon" to the attach
sibling is the same move the `memory` sibling made and it is correct here: that
two attached instances' requests land on the *same* router node is a
cartridge.ctg property, its owner is `done`, and the composed test re-proves it.
What is left — given one node, one spend — is genuinely proven, and proven in the
direction that matters: the non-vacuity mutation that gives each caller its own
gate (the two-process shape the audit describes) fails the test with
`left: 2, right: 1`. See F3 for the one clause of box 1 that is checked more
weakly than it is claimed.

**Box 2 — the structural claim is worth asserting, and the concession is in the
wrong place.** Two separate judgements:

- *Assert the box.* It pins a real invariant that nothing else pins and that a
  future change could break silently — a `[[bin]]`, a second `Auth::from_path`,
  a `pub mod auth`. It is not decorative: all sixteen of its guards fire against
  a tree that should fail them (table below), including the four that pin the
  seam and the gate. Deleting the box would leave the crate's "only a node can
  refresh" property unchecked. The spec is also right that this is **not**
  delegable the way memory's daemon-wide clause was, and its reason is the
  correct one: a writer lock refuses a second holder, a token is spent by
  whoever POSTs it. I verified the two external spenders are real —
  `auth.rs:778` is the `~/.codex/auth.json` fallback the `codex` CLI rotates,
  and `:367-369` states in the shipped source that "spending the refresh token
  here rotates the credential out from under the CLI", which is the router
  conceding the point about `claude`.
- *But the concession belongs in the Outcome.* The spec says, correctly, that
  the original box "is unprovable and should not be claimed" — and the PRD's
  **Outcome still claims it**: "An attached instance never refreshes on its own
  path, so one refresh token is never spent twice." That is false while `codex`
  and `claude` exist, by the spec's own argument. The narrowing reached the two
  boxes and the Planning note and stopped there. A reader who ticks two true
  boxes will close a leaf whose stated outcome is untrue, and the Planning note
  is provenance, not the contract. This is **F1**, the main finding of the round.

### 5. The option chosen — the seam

The trade is right in direction and under-examined in one direction.

Right: eight lines, no file lock, no change to refresh logic, no touch to the
Claude Code or Copilot paths; it collapses the `:697` literal against the `:26`
const on the way; it is behaviour-identical when the variable is unset
(`.post(String)` and `.post(&str)` are the same `IntoUrl`; 58/58 green,
`cargo fmt --check` clean); and without it the acceptance box is unprovable
without spending a real grant, which is not an acceptable proof.

Under-examined: **the seam can itself be abused, and the spec never asks.**
`codex_token_endpoint()` is compiled into the shipped daemon and read at refresh
time (`auth.rs:41`). Anything that can set one environment variable on the
daemon redirects a POST whose body carries the *live* refresh token to an
arbitrary URL — silently, over the network. The `CLAUDE_CODE_EXECPATH`
precedent the spec leans on is not the same trade: that one overrides a binary
path, i.e. it already presupposes code execution. An env var reaches further
than code execution does (a launcher script, a shell profile, a `.envrc`, an
inherited environment when something else spawns the daemon). An attacker with
full local exec could read the credential file anyway, so this is not a new
capability — but it is a new, quiet, remote-exfiltrating path to a credential,
and closing it costs nothing: `#[cfg(test)]` / `#[cfg(not(test))]` on
`codex_token_endpoint()` is the same eight lines with zero production surface
(the test module is in-crate, `#[cfg(test)] #[path] mod tests` at `:1238-1239`,
so it works), and a loopback-only check is two more. The spec's paragraph
headed "Credential safety, which is the point of the seam" argues only that the
*probe* is safe — which it is — and never that the *product* is. This is **F4**.

### 6. Non-vacuity — both reproduced, one number corrected

| | reproduced | observed |
| --- | --- | --- |
| gate deleted outright | yes | `error: field 'refresh' is never read` (+ two unused-variable errors) under the crate's own `[lints.rust] warnings = "deny"`; **Verify block 1 exits 1** |
| each caller given its own gate (two processes simulated) | yes | `assertion 'left == right' failed: the refresh token is presented to the token endpoint exactly once` / `left: 2` / `right: 1`; `FAILED. 0 passed; 1 failed`; **block 1 exits 1** |
| `!`-prefix counter-demo | yes | on a tree with `pub mod auth;`, `sh -eu -c 'test -f src/lib.rs; ! grep -q "^pub mod auth;" src/lib.rs; echo reached-end'` printed `reached-end` and **exited 0** |

One correction to the analyst's table: rows 7 and 8 record `101`. That is
`cargo test`'s own status. Block 1 pipes cargo into `tee`, so `set -e` sees
`tee` (0) and it is the summary grep that fails the block — the block's exit is
**1** in both cases. The conclusion is unchanged and the block design is
actually the right one (the grep is what makes a missing, renamed or `#[ignore]`d
test fail), but the recorded number is not the number the collector sees.

Suite figures confirmed independently: **58 passed, 0 failed** patched;
**57 passed, 0 failed** at the base. Five consecutive full-suite runs on the
patched tree: 58/58 every time, no flake.

### Guard-by-guard non-vacuity of Verify block 2

Each guard run alone, `sh -eu`, against a tree constructed to fail it:

| # | guard | tree | exit |
| ---: | --- | --- | ---: |
| 1 | `test -f src/lib.rs` | `src/lib.rs` removed | 1 |
| 2 | `grep -q '^mod auth;' src/lib.rs` | renamed to `mod authx;` | 1 |
| 3 | `if grep -qn '^pub mod auth;' …; then exit 1; fi` | `pub mod auth;` | 1 |
| 4 | `test ! -d src/bin` | `src/bin/` created | 1 |
| 5 | `if grep -qn '^\[\[bin\]\]' Cargo.toml; then exit 1; fi` | `[[bin]]` appended | 1 |
| 6 | `test -f src/service.rs` | removed | 1 |
| 7 | `grep -q 'auth::Auth::from_path(' src/service.rs` | renamed to `Auth::make(` | 1 |
| 8 | `Auth::from_path(` count `= 1` | second site added in `proxy.rs` | 1 |
| 9 | `test -f src/module.rs` | removed | 1 |
| 10 | `service::start(` count `= 1` | second caller added in `proxy.rs` | 1 |
| 11 | `test -f src/auth.rs` | removed | 1 |
| 12 | gate line present | per-caller gate substituted | 1 |
| 13 | `fn codex_token_endpoint() -> String {` present | renamed | 1 |
| 14 | `.post(codex_token_endpoint())` present | reverted to `.post(CODEX_TOKEN)` | 1 |
| 15 | `test -f .cartridge/tests/unit/auth/tests.rs` | removed | 1 |
| 16 | test name present | test renamed | 1 |

**16 / 16 fire.** No guard in any block is `!`-prefixed (grepped all three
blocks); both negatives use `if …; then exit 1; fi`. Block 1 is non-vacuous in
the same way: run verbatim on the pristine base it prints
`running 0 tests … 57 filtered out`, cargo exits 0, and the block still exits 1.

One break in the `test -f` discipline: **`Cargo.toml` is the only path in block 2
with no `test -f`.** With `Cargo.toml` absent, `if grep -qn '^\[\[bin\]\]' Cargo.toml; then exit 1; fi`
exits **0** (grep exits 2, the condition is false, the block continues).
Reproduced. Bounded in practice because block 1 cannot build without it, but it
is the one guard that can go quiet. This is **F6**.

### Scorecard

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Real defect, re-derived at source rather than accepted: the POST at `:696-701` precedes both compares (`:718`, `:732`), so a second node double-spends rather than retries; `d5ce669:src/auth.rs:282` is the audited gate verbatim; `config.lua:56-62` makes two nodes the configured default. One outcome, two boxes, body well inside the length target. −2: **F1** — the narrowing reached the boxes and the Planning note but not the **Outcome**, which still asserts "one refresh token is never spent twice", the very claim the spec argues is false. −1: **F2** — the spec's bold "**Footprint change requested** … the coordinator must add that second path before this lands" is stale; the coordinator already added `.cartridge/tests/unit/auth/tests.rs` to both the PRD and the spec frontmatter, so a durable record now carries a pending instruction that is done. |
| Ownership and reuse | 18 | Correct owner and base (`65d22d7` = live `main`, clean); `needs` resolves to a `done` sibling; no duplicate scope (the only other router/OAuth leaf, `@root/claude-code-subscription-oauth-for-the-router` prio 50, is proxy passthrough). Genuinely minimal: 8 production lines, no file lock, no refresh-logic change, and it removes the `:697` literal/`:26` const duplication. The test reuses the file's existing scratch-dir + `Auth::from_path` + synthetic-JWT pattern from `valid_oauth_requests_do_not_wait_for_the_store_writer` and the already-wired `#[cfg(test)] #[path]` module (`:1238-1239`). The file-lock branch is correctly refused, with every leg independently checked (§3). −1: the seam is a **production** change for a test-only need; `#[cfg(test)]` / `#[cfg(not(test))]` is the same eight lines with no shipped surface — a rung the spec never climbed. −1: **F5** — guard 10 is the block's weakest leg: `grep -rn 'service::start('` counts a literal spelling and never checks the one hit is in `module.rs`, so a new `src/foo.rs` calling it while `module.rs` stopped still reads 1; the `grep -v 'pub async fn start'` filter is inert (`service.rs:34` reads `pub async fn start(`, which never matches `service::start(`). |
| Dependencies and implementable slices | 19 | `attempt-1.patch` `git apply --check` exit 0 on a pristine `65d22d7` worktree, applies clean, and touches exactly the two footprint files (`git status --porcelain -uall` → ` M .cartridge/tests/unit/auth/tests.rs`, ` M src/auth.rs`). Steps 1–3 match the prototype exactly. The Verify blocks follow the template's engine facts verbatim, including the prescribed `${CARGO_TARGET_DIR:-$PWD/target/<slug>-verify}` form; no `cd`, all paths repo-relative; the lane needs no sibling `*.ctg` (no path deps — confirmed by building a lone worktree). Budget: block 1 into a cold target dir with a warm registry ran in **7.2 s** wall (6.53 s cargo), blocks 2 and 3 under a second — far inside 120 s. No block writes inside the footprint: after all three, `git status --porcelain -uall` in the patched worktree is still exactly the two patched files, and `target/` is ignored (`git check-ignore -v` → `.gitignore:2:/target/`). −1: the leaf's Outcome is delivered across three PRDs but only the attach sibling is in `needs`; the composed test is named in prose and not linked, so nothing mechanically prevents this leaf closing while its other half is unproven. |
| Observable acceptance and baseline evidence | 17 | All three blocks pass verbatim on the patched tree (0 / 0 / 0) and blocks 1 and 2 fail on the pristine base (1 / 1); block 3 passes on base, correctly, since it is a formatting gate not a claim gate. **16 / 16 block-2 guards fire** against a failing tree (table above); no `!`-prefix anywhere; the `!` counter-demo reproduces at exit 0. Both non-vacuity demonstrations reproduce, including the one that is the test's whole point (`left: 2, right: 1`). Suite figures confirmed: 58 patched / 57 base, both 0 failed, 5/5 repeats green. −1: **F3** — box 1's third clause, "both callers get working headers back", is checked as `first.unwrap()["chatgpt-account-id"] == "test"`. That header is copied verbatim out of the stored login (`codex_header_values`, `:748-753`) and is identical before and after a rotation, so it cannot distinguish a working header from a stale one. The property the clause names — the waiter reuses the winner's *fresh* token instead of its own expired one — is one line away (assert the two `authorization` values are equal and carry the rotated access token). I could not construct a realistic regression that escapes the POST-count assertion, so this is a claim/check mismatch rather than a hole. −1: box 2 is checked by string greps, so it pins spellings and not semantics: `use crate::service::start;` then `start(…)` passes guard 10, and a `[[bin]]` declared with leading whitespace passes guard 5. −1: **F6** — `Cargo.toml` is the one path with no `test -f`, and without it the `[[bin]]` guard exits 0 (reproduced). |
| Failure, recovery and compatibility | 16 | `CARGO_TARGET_DIR` pinned per the template, so pass 2 in the live checkout writes `target/router-refresh-once-verify/` and never `target/debug/librouter.dylib` — the correct lesson from `verify-blocks-must-not-build-live-targets`, and I confirmed empirically that nothing outside `target/` changes. No behaviour change with the variable unset. Copilot correctly scoped out as an exchange, not a rotation (`:602-655`), and the device-auth login at `:971` correctly left on the bare const so the seam cannot redirect a login. Residuals honestly named and correctly homed (`config.lua:59` to the attach sibling or composed test; the external spenders to the existing compare-and-write and use-the-CLI's-token rules, which this spec neither improves nor weakens). −2: **F4** — the seam's production abuse surface is never considered (§5); `ROUTER_CODEX_TOKEN_URL` redirects a POST carrying the live refresh token to an arbitrary URL, and `#[cfg(test)]` closes it for free. −2: **F7** — `std::env::set_var` in a multi-threaded test binary. `Auth::from_path` (`:160`) calls `catalog::credentials`, which iterates `std::env::vars()` (`catalog.rs:126`); four other tests in this same binary construct an `Auth` (`tests.rs:16`, `:29`, `:49`, and `proxy/capabilities.rs`), and `cargo test` runs them concurrently. `setenv` racing `environ` iteration is exactly why Rust 2024 made `set_var` unsafe. Not observed (5/5 green), but it is a latent nondeterministic crash introduced into the one test guarding a credential path. Remaining risk covers only the *logical* collision — "the only other `codex_headers` test holds a non-expired token", which I verified is true (`exp = now + 3600`, `tests.rs:50`) — and not this one. The `#[cfg(test)]` fix in F4 removes the env var entirely and closes F7 with it. −0 (noted, not deducted): the test removes the variable only on the success path (`tests.rs:230`, after the asserts), so a failing assert leaks it for the rest of the process; benign here, since it points at an aborted loopback server. |
| **Reviewer total** | **87 / 100** | Below the 90 threshold. No blocking findings. |

### Findings

| # | Finding | Evidence | Recommendation |
| ---: | --- | --- | --- |
| **F1** | The PRD **Outcome** still asserts what the spec argues is false. | PRD Outcome: "An attached instance never refreshes on its own path, so one refresh token is never spent twice." Spec box 2: "The box as written is unprovable and should not be claimed." `auth.rs:367-369` concedes the `claude` CLI; `:778` is the `codex` CLI's file. | Edit the Outcome in place (body only, never the frontmatter): scope it to what router.ctg owns and name the two out-of-reach spenders in one sentence — e.g. "Every refresh router.ctg can initiate happens in the daemon's single router node, where the in-process lock is the right lock. The `codex` and `claude` CLIs rotate the same credentials from outside every composition; that is out of this board's reach and is mitigated only by the existing compare-and-write (`:718`, `:732`) and use-the-CLI's-token (`:365-377`) rules." Then box 2 carries only its structural claim and its parenthetical can shrink. |
| **F2** | The spec's "**Footprint change requested**" instruction is stale. | The PRD and spec frontmatter both already list `.cartridge/tests/unit/auth/tests.rs`. | One-line edit: change it to record that the coordinator made the change, keeping the `:1238-1239` rationale. |
| **F3** | Box 1's "both callers get working headers back" is checked by a rotation-invariant field. | `tests.rs:219-220` asserts `chatgpt-account-id == "test"`; that value comes from the stored login and is unchanged by a refresh (`:748-753`). | Two lines in the test: assert `first["authorization"] == second["authorization"]` and that it equals the rotated `Bearer e30.{exp}.`. |
| **F4** | The env seam ships in production and can redirect a real refresh POST — refresh token in the body — to any URL. | `auth.rs:41` reads `ROUTER_CODEX_TOKEN_URL` at refresh time in the shipped cdylib. The `CLAUDE_CODE_EXECPATH` precedent (`:293`) is a binary override and presupposes code execution. | Split `codex_token_endpoint()` into `#[cfg(test)]` / `#[cfg(not(test))]` halves — the same eight lines, zero production surface, and the test module is in-crate so it works. Failing that, restrict the override to a loopback host and say so in Remaining risk. |
| **F5** | Guard 10 does not check that the single `service::start(` hit is in `module.rs`; its `grep -v` filter is inert. | `service.rs:34` is `pub async fn start(`, which never matches `service::start(`. | Either `grep -rn 'service::start(' src --include=*.rs \| grep -c '^src/module.rs:'` `= 1`, or drop the inert filter and say what the count means. |
| **F6** | `Cargo.toml` is the one path in block 2 with no `test -f`, and the `[[bin]]` guard exits 0 without it. | Reproduced: guard alone on a tree with `Cargo.toml` removed → exit 0. | Add `test -f Cargo.toml` before it. |
| **F7** | `std::env::set_var` races `std::env::vars()` in four concurrently-running sibling tests. | `tests.rs:177`; `auth.rs:160` → `catalog.rs:126`; `Auth::from_path` at `tests.rs:16`, `:29`, `:49` and in `proxy/capabilities.rs`. | Closed for free by F4's `#[cfg(test)]` split if the override is a `static Mutex<Option<String>>` instead of an env var; otherwise name it in Remaining risk alongside the logical-collision note. |

None of F1–F7 blocks the gate: the boxes as written are true and checkable, the
prototype is correct, and every gate is non-vacuous. F1 and F4 are the two worth
the coordinator's attention — one is a false claim left in the contract, the
other is a shipped credential surface added for a test.

Findings and concrete revisions: see the table above. F1, F2, F3, F5 and F6 are
one-to-three-line edits; F4 and F7 are one shared eight-line change to
`codex_token_endpoint()` plus how the test sets it.

Disposition: **revise** — keep the scope, the base, the footprint, the option
chosen and both narrowings. This is a good plan with a false sentence in its
Outcome and one unexamined production surface.

Validation: all commands below. cwd is a scratch worktree of `router.ctg` at
`65d22d7` under `<scratchpad>/rev/{patched,base}` unless noted;
`<scratchpad>` = `/private/tmp/claude-501/-Users-feb-dev-cartridge/0b0c3ecc-.../scratchpad`.
Verify blocks were extracted verbatim from `specs/spec01.md` with a fenced-block
extractor and run as `sh -eu <block>`; none exceeded 120 s.

| # | command | exit |
| ---: | --- | ---: |
| 1 | `git -C router.ctg log -1 --format='%H %s'` → `65d22d7`; `git status --porcelain -uall` → clean | 0 |
| 2 | `git -C router.ctg worktree add --detach <scratchpad>/rev/patched 65d22d7`; same for `rev/base` | 0 |
| 3 | `git show d5ce669:src/auth.rs \| sed -n '278,290p'` — the gate at `:282` verbatim | 0 |
| 4 | `git -C rev/patched apply --check attempt-1.patch` | 0 |
| 5 | `git -C rev/patched apply attempt-1.patch`; `git status --porcelain -uall` → exactly the two footprint files | 0 |
| 6 | Verify block 1, patched, cold `CARGO_TARGET_DIR`, **7.2 s** — `1 passed; 0 failed; 57 filtered out` | 0 |
| 7 | Verify block 2, patched | 0 |
| 8 | Verify block 3, patched (`cargo fmt --check`) | 0 |
| 9 | Verify block 1, **pristine base** — `running 0 tests … 57 filtered out`, cargo 0, block fails on the summary grep | **1** |
| 10 | Verify block 2, **pristine base** | **1** |
| 11 | Verify block 3, pristine base (formatting gate, correctly green) | 0 |
| 12 | 16 block-2 guards, each alone, each against a tree built to fail it | **1** ×16 |
| 13 | `!` counter-demo on a `pub mod auth;` tree — printed `reached-end` | **0** |
| 14 | non-vacuity A: gate deleted → `error: field 'refresh' is never read` (`warnings = "deny"`), block 1 | **1** (cargo 101) |
| 15 | non-vacuity B: each caller its own gate → `left: 2, right: 1`, `FAILED. 0 passed; 1 failed`, block 1 | **1** (cargo 101) |
| 16 | `[[bin]]` guard alone with `Cargo.toml` removed — **guard goes quiet** (F6) | **0** |
| 17 | `cargo test --lib` full suite, patched, `CARGO_TARGET_DIR=<scratchpad>/target-full` — `58 passed; 0 failed` | 0 |
| 18 | `cargo test --lib` full suite, base, `CARGO_TARGET_DIR=<scratchpad>/target-full-base` — `57 passed; 0 failed` | 0 |
| 19 | full suite ×5 on patched — 58/58 every run, no flake | 0 |
| 20 | `git -C rev/patched status --porcelain -uall` after all blocks — still only the two patched files | 0 |
| 21 | `git -C rev/base check-ignore -v target/router-refresh-once-verify` → `.gitignore:2:/target/` | 0 |
| 22 | `grep -rn 'Auth::from_path(' src --include=*.rs` → one hit, `service.rs:51`; `grep -rn 'service::start('` → one hit, `module.rs:26` | 0 |
| 23 | `grep -rn 'env::var\|env::set_var' src --include=*.rs` → `auth.rs:41`, `:293`, `:1045`, `catalog.rs:106`, `:126`, `:141`, `:232`, `launch.rs:28` (evidence for F7) | 0 |
| 24 | sibling-state sweep of the parent's children; `grep -rln 'oauth' --include=prd.md` across all boards (duplicate check) | 0 |

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not supplied; not required under delegation.
User feedback/provenance: none for this revision.
Result: **FAIL — 87/100**.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision — F1 (rewrite the PRD Outcome in place, body
only), F2, F3, F5 and F6 as small edits, and F4/F7 as the single
`#[cfg(test)]` / `#[cfg(not(test))]` change to `codex_token_endpoint()` with the
test's override moved off the process environment. Then re-review in round 2 at
the same base.
