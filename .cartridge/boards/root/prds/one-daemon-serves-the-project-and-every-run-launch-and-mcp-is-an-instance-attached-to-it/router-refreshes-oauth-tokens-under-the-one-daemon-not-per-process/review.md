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

## Round 2 — 2026-09-16

Presented revision: superproject `d721262` (dirty in memos and submodule
gitlinks, none in this PRD's footprint); `router.ctg` `65d22d7` — **HEAD has not
moved** since round 1 (`= main`, `git status --porcelain -uall` → 0 lines).
Prototype `attempt-2.patch` (2 files, +136/−1), `attempt-1.patch` retained as the
round-1 record. `prd.md` body was rewritten by the coordinator (Outcome +
Planning note) before this round; the spec was revised in place.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process/prd.md` SHA-256 `1255e04e623be0db6bfe6cd0432d66646cda934987953dca923fd9c1028f906e` (round 1: `d7d5829…` — changed, F1) |
| Specs | `specs/spec01.md` SHA-256 `7c4a79c07bf24821023cbdb72bff1cbe285fb3537bb7afdeec5bcc2bba4bcf63` (round 1: `a8be48e…`) |
| Parent rollup | `.../one-daemon-.../prd.md` SHA-256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445` (unchanged) |
| Revision report | `.state/loop/.../analyst-2.md` SHA-256 `67afa543a4b9b35dfbaf32c575236130683fc1d77c3909c1ab1f1062aee6305f` |
| Prototype | `.state/loop/.../attempt-2.patch` SHA-256 `814dc404d6f00947b33e80112fadcee501d209104ccfc47ba98256851664e547` |
| Prior prototype | `.state/loop/.../attempt-1.patch` SHA-256 `f855f4e7799ea80de60b9af293edf43f20ffd65d982ca0c6da9fec68d2509b17` (used as the "env seam restored verbatim" mutant) |
| Material dependency | `an-instance-attaches-to-the-daemon-and-never-composes-silently` SHA-256 `f0ebad6d1f91936f7cfe3cf202cce3304c6dab61c70d1b89ecc6551a50ad5cb6`, state `done` |
| Material input | `.cartridge/config.lua` SHA-256 `58497aea44bcbcdafa477858a51fab32f5b2c5a0a5c13c3ca05181c7527fb651` (round 1: `322e1e9…`). **Changed, but not materially**: the diff is in `live` / `live-record`; the `router = { … listen = { "127.0.0.1:0" }, config_dir = …, data_dir = … }` block is still exactly `:56-62`, `listen` still `:59`, byte-identical to round 1's quote. |
| Base | `router.ctg` `65d22d76dc4dec15a0aed2da24b79fa4b500767e` |

Reviewed independently: I did not author the plan, the spec, either prototype or
the revision, and I re-derived every claim below in my own worktrees rather than
accepting `analyst-2.md`.

### How real credentials were kept out of every probe

No probe triggered a real OAuth refresh; nothing here read, copied or printed
token material. **No refresh token was spent.**

- **No real token endpoint was contacted.** `auth.openai.com`,
  `api.anthropic.com` and `github.com` were never reached. The only endpoint any
  execution addressed was the test's own axum server on `127.0.0.1:0`, pointed at
  through the `#[cfg(test)]` `static CODEX_TOKEN_URL`. I re-derived why that is
  now *structurally* safe rather than merely conventional: the override is
  `#[cfg(test)]`, and I proved (probe P3 below) that the `cfg(test)` half is not
  compiled into a normal build at all.
- **The store was scratch, seeded with a dummy.** The test writes its login into
  `std::env::temp_dir()/router-refresh-once-<hex>/auth.json` with the refresh
  token literal `spend-me`. `codex_auth` (`auth.rs:769-790` at base) prefers the
  store entry, so the `~/.codex/auth.json` fallback at `:778` is unreachable in
  this fixture. `~/.codex/auth.json` was never opened, read or listed.
- **The keychain was never touched.** No `security` invocation, no
  `CLAUDE_CODE_EXECPATH`, no Claude Code binary scan. I deliberately did not
  exercise the Claude Code subscription path (`:412-478` shells out to `security`
  and would rotate the user's real keychain entry).
- **Nothing ran against the live daemon.** No `daemon`, `launch`, `mcp`, `run`,
  `stop`, `--replace` or routing request; no `prd` state op; no `git add`, commit
  or push; no write to the live `router.ctg` checkout, which is clean at
  `65d22d7`.
- **Every cargo command used an isolated `CARGO_TARGET_DIR`** — either my own
  `<scratchpad>/rev2/t-*` directories or the block's own
  `target/router-refresh-once-verify` inside a scratch worktree. The live
  `router.ctg/target/` was never written, so no cartridge hot-restarted.
- **My own trees, my own scratch subdirectory.** Two fresh
  `git worktree add --detach … 65d22d7` at `<scratchpad>/rev2/{patched,base}`,
  plus seven throwaway `rsync` copies for mutants. Every extracted block script
  lives in `<scratchpad>/rev2/blocks/`, a private subdirectory — not the shared
  scratchpad root, which is contended.
- One thing I deliberately did **not** verify, and it is a finding about the
  world rather than a gap in the evidence: I did not confirm that a real
  `auth.openai.com` refresh rotates the token. The code says so (`:708-712`);
  confirming it would spend a live grant.

### 1. The security fix (F4 + F7) — closed, and verified four ways

This is the heart of the round, so I checked the property itself rather than the
analyst's assertions about it.

**(a) No environment variable can reach the token endpoint in a shipped build.**
`grep -rn 'ROUTER_CODEX_TOKEN_URL' .` over the whole patched crate (excluding
`target/` and `.git/`) → **no match, exit 1**. The string exists nowhere. The
complete set of environment reads left in `src/` is `auth.rs:308`
(`CLAUDE_CODE_EXECPATH`, pre-existing), `auth.rs:1060` (`var_os(declared)` inside
`Auth::status`, a key-source *report*, not an endpoint), `catalog.rs:106/126/141/232`
and `launch.rs:28` — none of them reachable from `codex_token_endpoint()`.
`codex_token_endpoint()` has exactly one call site, `auth.rs:722` (the refresh
POST), and the device-auth login at `auth.rs:996` patched / **`:971` base** keeps
the bare `CODEX_TOKEN` const, so the seam can only ever be a *refresh*, never a
login — the spec now states this explicitly and it is true.

**(b) The `#[cfg]` split really excludes the test half — proved, not assumed.**
I injected `compile_error!("the cfg(test) half was compiled")` into the body of
the `#[cfg(test)] fn codex_token_endpoint()` in a throwaway copy:

| build | result |
| --- | --- |
| `cargo build` (non-test) | **exit 0**, `Finished dev profile` — the poisoned half was never compiled |
| `cargo test --lib --no-run` | **exit 101**, `error: the cfg(test) half was compiled` at `src/auth.rs:55` |

That is a positive proof of exclusion, not an inference from the attribute. In a
shipped cdylib `codex_token_endpoint()` is `CODEX_TOKEN.to_owned()` and nothing
else. F4 is closed at the level it needed to be closed.

**(c) The non-test build is clean under `warnings = "deny"`, and the suite is
green.** `Cargo.toml:28-29` is `[lints.rust] warnings = "deny"`. `cargo build`
with an isolated target dir → **exit 0**, no warning emitted (so the
`#[cfg(test)] static` leaves no dead-code residue in a shipped build, as
claimed). `cargo test --lib` → **58 passed; 0 failed; 0 ignored**, exit 0.

**(d) F7 is genuinely closed.** `grep -rn 'set_var' .cartridge/tests src` returns
exactly one hit and it is the doc comment at `src/auth.rs:48` explaining why
`set_var` was *not* used. `grep -n 'env::' .cartridge/tests/unit/auth/tests.rs`
returns only four `std::env::temp_dir()` calls (`:13`, `:26`, `:45`, `:148`).
There is no `setenv` left to race the `std::env::vars()` scan that
`Auth::from_path` → `catalog.rs:126` performs in the concurrently-running sibling
tests. The replacement is an ordinary `std::sync::Mutex` whose guard is dropped
inside `codex_token_endpoint()` before any `.await`, so it introduces no new
hazard of its own.

**(e) The three new guards fire against a tree with the env seam restored
verbatim.** I rebuilt that tree by applying `attempt-1.patch` (the round-1
prototype, which *is* the env seam verbatim, `set_var` included) to a pristine
`65d22d7` copy, then ran each guard alone under `sh -eu -c`:

| guard | exit |
| --- | ---: |
| `grep -A1 '^#\[cfg(not(test))\]' src/auth.rs \| grep -q 'fn codex_token_endpoint() -> String {'` | **1** |
| `grep -A2 '^#\[cfg(not(test))\]' src/auth.rs \| grep -q 'CODEX_TOKEN.to_owned()'` | **1** |
| `if grep -qn 'ROUTER_CODEX_TOKEN_URL' src/auth.rs; then exit 1; fi` | **1** |
| `if grep -qn 'env::set_var' .cartridge/tests/unit/auth/tests.rs; then exit 1; fi` (F7) | **1** |
| whole Verify block 2 on that tree | **1** |

All four, and the block as a whole, reject the env seam. Reproduced, as asked.

**(f) What the guards do *not* pin — see F8.** They pin the *spelling*
`ROUTER_CODEX_TOKEN_URL` and the *presence* of `CODEX_TOKEN.to_owned()` within
two lines of the attribute. I mutated the shipped half to
`std::env::var("ROUTER_TOKEN_ENDPOINT").unwrap_or_else(|_| CODEX_TOKEN.to_owned())`
— a differently-named environment variable with exactly the F4 capability — and
**the whole of Verify block 2 exited 0**, all three new guards included (guard 17
passes because `CODEX_TOKEN.to_owned()` survives as a substring of the fallback).
The reviewed revision is secure; its *gate* pins one name rather than the
property. Non-blocking, and one character away from closed — see F8.

### 2. F6, the vacuity fix — reproduced both ways

On a patched copy with `Cargo.toml` deleted:

| form | exit |
| --- | ---: |
| round-1 bare guard `if grep -qn '^\[\[bin\]\]' Cargo.toml; then exit 1; fi` | **0** — vacuity reproduced (`grep: Cargo.toml: No such file or directory`, grep exits 2, the `if` swallows it) |
| revised pair `test -f Cargo.toml` + that guard | **1** — fixed |

### 3. F5's replacement — reproduced both ways

On a tree where `module.rs` stopped calling `service::start(` and a new
`src/proxy.rs` call site appeared (total hits still 1):

| form | exit |
| --- | ---: |
| round-1 guard 10, `grep -rn 'service::start(' src --include=*.rs \| grep -v 'pub async fn start' \| wc -l` `= 1` | **0** — F5 reproduced; the `grep -v` was inert and the count alone accepts a moved call site |
| revised count guard alone | **0** (correctly — the count *is* still 1) |
| revised anchored guard `grep -c '^src/module.rs:'` `= 1` | **1** — the call site must now *be* the Lua module entry |

### 4. Guard-by-guard spot-check of Verify block 2

Beyond the seven guards above I re-ran twelve more individually, each `sh -eu -c`
in a fresh copy of the patched tree mutated to break exactly that guard:

| guard | tree built to fail it | exit |
| --- | --- | ---: |
| `test -f src/lib.rs` | `src/lib.rs` removed | **1** |
| `grep -q '^mod auth;' src/lib.rs` | renamed `mod authx;` | **1** |
| negative `^pub mod auth;` | `pub mod auth;` | **1** |
| `test ! -d src/bin` | `src/bin/` created | **1** |
| negative `^\[\[bin\]\]` (with its `test -f`) | `[[bin]]` appended | **1** |
| `grep -q 'auth::Auth::from_path(' src/service.rs` | renamed `Auth::make(` | **1** |
| `Auth::from_path(` count `= 1` | second site in `proxy.rs` | **1** |
| `service::start(` count `= 1` | second caller in `proxy.rs` | **1** |
| gate line present | per-caller gate substituted | **1** |
| `.post(codex_token_endpoint())` present | reverted to `.post(CODEX_TOKEN)` | **1** |
| `test -f .cartridge/tests/unit/auth/tests.rs` | removed | **1** |
| test name present | test renamed | **1** |

**18 of the 21 guards reproduced directly at exit 1** (the twelve above, plus the
four in §1(e), plus the F6 pair and the F5 replacement); the three I did not
re-run individually are the remaining bare `test -f` existence checks
(`src/service.rs`, `src/module.rs`, `src/auth.rs`), whose behaviour is settled by
the four `test -f` mutants I did run. Both round-1 holes reproduce at exit 0
before the fix. No guard anywhere is `!`-prefixed; both negatives use
`if …; then exit 1; fi`; every path is now preceded by `test -f` or `test ! -d`.
The analyst's 21/21 claim is corroborated; the one qualification is F8.

### 5. F3 — the "working headers" check is now load-bearing

The test asserts `first["authorization"] == format!("Bearer {fresh}")` and
`second["authorization"] == first["authorization"]`. I made the fixture server
return a token **one character different** from the expected one (`let rotated =
format!("{fresh}x")`):

```
assertion `left == right` failed: the winner's header carries the rotated access token
  left: "Bearer e30.eyJleHAiOjE3ODk1NjU2ODF9.x"
 right: "Bearer e30.eyJleHAiOjE3ODk1NjU2ODF9."
test result: FAILED. 0 passed; 1 failed
```

The panic is at `tests.rs:233`, the `authorization` assert — *after* the two
`chatgpt-account-id` asserts at `:230-231` passed. That is exactly F3's point:
the rotation-invariant field cannot tell a fresh header from a stale one, and the
new assert can. The block's exit on that mutant is **1** (see §7).

The core non-vacuity still holds on the *revised* test (round 1's evidence was
against the old one, so I re-ran it): giving each caller its own gate — the
two-process shape the audit describes — produces
`assertion left == right failed: the refresh token is presented to the token
endpoint exactly once / left: 2 / right: 1`, `FAILED. 0 passed; 1 failed`.

### 6. F1 and F2 — the contract no longer argues with itself

The coordinator's rewritten Outcome now reads "Every refresh **that router.ctg
performs** …" and states plainly that the stronger claim "one refresh token is
never spent twice" is false while the `codex` and `claude` CLIs exist, citing
`src/auth.rs:367-369`. The spec's box-2 parenthetical no longer carries that
argument against the PRD; it opens "the narrowing now matches the PRD: the
Outcome says plainly that …" and keeps only the structural claim plus the
not-delegable reason. **The spec now defers to the Outcome rather than arguing
with it.** F1 is closed. F2 is closed: the bold "Footprint change requested …"
instruction is replaced by "Footprint, settled", recording what the coordinator
already did and keeping the `:1238-1239` rationale, which I confirmed
(`#[cfg(test)] #[path = "../.cartridge/tests/unit/auth/tests.rs"] mod tests` at
patched `:1264-1265` = base `:1238-1239`, and `tests.rs:1` is `use super::*`, so
the `static` is reachable).

Citations: the spec's compare-and-write cites are corrected to `:718` and `:732`
in **both** of its occurrences, and I verified them at base — `:718` is
`if map.get(&provider.name) == Some(&original_auth)`, `:732` is
`if current == original_auth`, and `:723` is the `.get()` inside the else, as
round 1 said. The device-auth exemption at `:971` is now stated. **But the PRD's
Planning note still says `:723`/`:731-736`** — see F9.

### 7. Exit-code discipline — the revised table reports collector-visible codes

Confirmed empirically rather than read. Running Verify block 1 verbatim on the
F3 mutant (where `cargo test` itself exits **101**), the block's exit as a
collector sees it is **1**: the pipe into `tee` means `set -e` observes `tee`, and
the summary `grep -q 'test result: ok\. 1 passed; 0 failed'` is what fails the
block. The same holds on the pristine base (cargo exits 0 with
`running 0 tests … 57 filtered out`; the block exits 1). `analyst-2.md` records
`**1** (cargo 101)` for both non-vacuity rows and states the correction
explicitly, and spec block 1 now carries the comment. Correct.

### Scorecard

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | F1 closed: the Outcome no longer asserts what the spec argues is false, and the spec now defers to it instead of arguing with it (§6). F2 closed. The defect itself re-confirmed at base: the POST (`:696-701`) precedes both compares (`:718`, `:732`); `config.lua:56-62` still pins `listen = { "127.0.0.1:0" }` byte-identically, so two nodes remain the configured default and the premise still holds. One outcome, two boxes, body inside the length target. −1: **F9** — the PRD Planning note still cites the compare-and-write as `:723`/`:731-736`, the exact drift round 1 flagged; `analyst-2.md` reports it "corrected … (both places)", which is true of the spec but not of `prd.md`, which the report also says was deliberately not edited. A durable record now carries a corrected cite in one file and the stale cite in the other. |
| Ownership and reuse | 20 | Round 1's two deductions are both closed. The seam now has **zero** production surface, proved by exclusion (§1b) rather than asserted, and F5's guard is replaced with one that anchors the call site to `module.rs` (§3). Still genuinely minimal: +26/−1 in `src/auth.rs`, no file lock, no change to refresh logic, no touch to the Claude Code or Copilot paths, and the `:697` literal / `:26` const duplication collapsed on the way. The test reuses the file's existing scratch-dir + `Auth::from_path` + synthetic-JWT pattern and the already-wired `#[cfg(test)] #[path]` module. Correct owner, correct base, `needs` resolves to a `done` sibling, no duplicate scope. |
| Dependencies and implementable slices | 20 | `git apply --check attempt-2.patch` on a pristine `65d22d7` worktree → **exit 0**; applied, it touches exactly the two footprint files (`git status --porcelain -uall` → ` M .cartridge/tests/unit/auth/tests.rs`, ` M src/auth.rs`) and nothing else after all three blocks have run. `router.ctg` HEAD has **not** moved (`65d22d7` = `main`, clean), so the base is still live. Blocks follow the template's engine facts verbatim: `${CARGO_TARGET_DIR:-$PWD/target/<slug>-verify}` on every cargo block, no `cd`, all paths repo-relative, no sibling `*.ctg` needed (no path deps — a lone worktree builds, I built four). Budget: block 1 **5 s** wall, blocks 2 and 3 under a second, far inside 120 s. Round 1's −1 (the composed test named in prose, not in `needs`) I do not carry forward, and I say why rather than dropping it silently: the F1 rewrite removed the daemon-wide claim from the Outcome, so this leaf's only true prerequisite is the attach sibling — which *is* in `needs` and *is* `done`; the composed test (`…proves-one-daemon-one-node-per-cartridge…`, prio 85, open) re-proves this downstream, and putting a downstream re-prover in `needs` would invert the dependency. |
| Observable acceptance and baseline evidence | 18 | All three blocks pass verbatim on the patched tree (**0 / 0 / 0**) and blocks 1 and 2 fail on the pristine base (**1 / 1**); block 3 passes on base, correctly, being a formatting gate. 18 of 21 block-2 guards reproduced individually at exit 1 (§1e, §2, §3, §4); both round-1 holes reproduce at 0 before their fixes. F3's new assert is load-bearing — a one-character-different rotated token fails it at `tests.rs:233` *after* the old `chatgpt-account-id` asserts have passed (§5) — and the audit's own shape (per-caller gate) still fails with `left: 2 / right: 1`. Suite 58/58 green, `cargo fmt --check` clean. Exit-code discipline verified empirically (§7). −2: **F8** — the guard set pins the *name* `ROUTER_CODEX_TOKEN_URL` and the *presence* of `CODEX_TOKEN.to_owned()` within two lines, not the property "the shipped half reads no environment". A shipped half rewritten as `std::env::var("ROUTER_TOKEN_ENDPOINT").unwrap_or_else(\|_\| CODEX_TOKEN.to_owned())` — the full F4 capability under another name — passes **the whole of block 2 at exit 0** (reproduced). For the security property this round exists to establish, a gate that only recognises one spelling is the weak leg, and the spec's "non-vacuous against the mutations that matter" overstates it by exactly that much. |
| Failure, recovery and compatibility | 20 | F4 and F7 both closed and independently proved, not accepted: the string `ROUTER_CODEX_TOKEN_URL` exists nowhere in the crate (exit 1); the `#[cfg(test)]` half is provably not compiled into a normal build (`compile_error!` probe: build 0, test build 101); the non-test build is clean under `warnings = "deny"` (exit 0, no warnings); no `set_var` survives anywhere, so nothing races `std::env::vars()` via `catalog.rs:126` in the four concurrent sibling `Auth::from_path` tests; the replacement `std::sync::Mutex` guard is dropped before any `.await`. The reasoning is recorded in the spec under a heading that tells a later reader not to reinstate the variable, with both the production-surface and the `set_var` arguments. `CARGO_TARGET_DIR` still pinned per the template, so pass 2 in the live checkout cannot hot-restart a cartridge. The seam cannot redirect a login (`:971` keeps the bare const), Copilot correctly scoped out as an exchange. Residuals honestly named and correctly homed (`config.lua:59` to the attach sibling or composed test; the external `codex` / `claude` spenders to the existing compare-and-write and use-the-CLI's-token rules). F8's durability point is deducted once, above, not twice. |
| **Reviewer total** | **97 / 100** | At or above the 90 threshold, with no blocking finding. |

### Findings

| # | Finding | Evidence | Recommendation |
| ---: | --- | --- | --- |
| **F8** (new, non-blocking) | Block 2 pins the env-var *name*, not the security property. A shipped `codex_token_endpoint()` that reads a differently-named environment variable passes every guard. | Reproduced: with the non-test half rewritten as `std::env::var("ROUTER_TOKEN_ENDPOINT").unwrap_or_else(\|_\| CODEX_TOKEN.to_owned())`, guard 16 → 0, guard 17 → 0 (the fallback keeps `CODEX_TOKEN.to_owned()` as a substring), guard 18 → 0, **whole block 2 → 0**. | One character. Anchor guard 17 to the whole line instead of a substring: `grep -A2 '^#\[cfg(not(test))\]' src/auth.rs \| grep -qx '<TAB>CODEX_TOKEN.to_owned()'`. Verified: that form exits **1** on the renamed-env-var mutant and **0** on the patched tree. Then soften the Remaining-risk sentence "non-vacuous against the mutations that matter" to say what the guards pin. |
| **F9** (new, non-blocking, cosmetic) | The PRD Planning note keeps the stale compare-and-write cite round 1 flagged. | `prd.md:67` still reads "the compare-and-write guards at `:723`/`:731-736`". At base, `:718` and `:732` are the compares; `:723` is the `.get()` in the else. The spec is corrected in both its places; `analyst-2.md` reports "both places" while also recording that `prd.md` was not edited. | One-line body edit to the Planning note (body only, never the frontmatter): `:723`/`:731-736` → `:718`/`:732`. |
| F1–F7 | All closed. | F1 §6; F2 §6; F3 §5; F4 §1(a)(b)(c)(e); F5 §3; F6 §2; F7 §1(d). | None. |

Neither F8 nor F9 blocks the gate. Nothing the plan claims is false, the
prototype is correct, every block is non-vacuous, and the security property F4
named holds in the reviewed revision — F8 is about how durably the *gate* pins
it, not about whether it holds.

Disposition: **keep** — scope, base, footprint, option chosen and both narrowings
all preserved; proceed to implementation. F8 and F9 are two small edits that can
ride along with the implementation rather than gate it.

Validation: cwd is a scratch worktree or throwaway copy of `router.ctg` at
`65d22d7` under `<scratchpad>/rev2/` unless noted;
`<scratchpad>` = `/private/tmp/claude-501/-Users-feb-dev-cartridge/0b0c3ecc-.../scratchpad`.
Verify blocks were extracted verbatim from `specs/spec01.md` with a fenced-block
extractor into `<scratchpad>/rev2/blocks/` (a private subdirectory) and run as
`sh -eu <block>` under a 120 s alarm; none came close to the limit.

| # | command | exit |
| ---: | --- | ---: |
| 1 | `git -C router.ctg log -1 --format=%H` → `65d22d7…` = `main`; `git status --porcelain -uall` → 0 lines (**HEAD has not moved**) | 0 |
| 2 | `git -C router.ctg worktree add --detach <scratchpad>/rev2/patched 65d22d7`; same for `rev2/base` | 0 |
| 3 | `git -C rev2/base apply --check attempt-2.patch` (pristine `65d22d7`) | **0** |
| 4 | `git -C rev2/patched apply attempt-2.patch`; `git diff --stat` → 2 files, +136/−1 | 0 |
| 5 | Verify block 1, patched, **5 s** wall — `1 passed; 0 failed; 57 filtered out` | 0 |
| 6 | Verify block 2, patched | 0 |
| 7 | Verify block 3, patched (`cargo fmt --check`) | 0 |
| 8 | Verify block 1, **pristine base** — `running 0 tests`, cargo 0, block fails on the summary grep | **1** |
| 9 | Verify block 2, **pristine base** | **1** |
| 10 | Verify block 3, pristine base (formatting gate, correctly green) | 0 |
| 11 | `grep -rn 'ROUTER_CODEX_TOKEN_URL' .` over the whole patched crate → no match | **1** (no match) |
| 12 | `grep -rn 'set_var' .cartridge/tests src` → one hit, the doc comment at `auth.rs:48` (F7) | 0 |
| 13 | `grep -n 'env::' .cartridge/tests/unit/auth/tests.rs` → four `temp_dir()` calls only | 0 |
| 14 | `grep -rn 'codex_token_endpoint\|CODEX_TOKEN' src --include=*.rs` → const `:26`, two `cfg`-split halves `:42`/`:54`, `static` `:51`, one call site `:722`, bare const at the device-auth `:996` (= base `:971`) | 0 |
| 15 | `CARGO_TARGET_DIR=<scratchpad>/rev2/t-build cargo build` (non-test, `warnings = "deny"`) — no warnings | **0** |
| 16 | `CARGO_TARGET_DIR=<scratchpad>/rev2/t-test cargo test --lib` → `58 passed; 0 failed` | **0** |
| 17 | **P3** `compile_error!` injected into the `#[cfg(test)]` half → `cargo build` | **0** (half excluded) |
| 18 | **P3** same tree → `cargo test --lib --no-run` → `error: the cfg(test) half was compiled` at `auth.rs:55` | **101** (half compiled only under `cfg(test)`) |
| 19 | env-seam tree = pristine `65d22d7` + `attempt-1.patch`; guards 16 / 17 / 18 / 21 each alone | **1** ×4 |
| 20 | whole block 2 on that env-seam tree | **1** |
| 21 | **F6** round-1 bare `[[bin]]` guard, `Cargo.toml` removed | **0** (vacuity reproduced) |
| 22 | **F6** revised `test -f Cargo.toml` + guard, same tree | **1** |
| 23 | **F5** round-1 guard 10 (inert `grep -v`), call site moved `module.rs` → `proxy.rs` | **0** (reproduced) |
| 24 | **F5** revised count guard, same tree | 0 (count is still 1 — correctly) |
| 25 | **F5** revised `grep -c '^src/module.rs:'` `= 1`, same tree | **1** |
| 26 | twelve further block-2 guards, each alone, each against a tree built to fail it (§4) | **1** ×12 |
| 27 | **F3** fixture returns a token one character off → panic at `tests.rs:233`, the `authorization` assert, *after* the `chatgpt-account-id` asserts passed | **101** cargo |
| 28 | same F3 mutant, run as Verify block 1 — the collector-visible exit | **1** |
| 29 | non-vacuity, revised test: each caller its own gate → `left: 2 / right: 1`, `FAILED. 0 passed; 1 failed` | **101** cargo / **1** as the block |
| 30 | **F8** shipped half rewritten to read `ROUTER_TOKEN_ENDPOINT`; guards 16 / 17 / 18 and **whole block 2** | **0** ×4 (gap reproduced) |
| 31 | **F8** candidate fix `grep -qx '<TAB>CODEX_TOKEN.to_owned()'` — on the mutant / on the patched tree | **1** / **0** |
| 32 | `git -C rev2/patched status --porcelain -uall` after all blocks → still exactly the two patched files | 0 |
| 33 | `sed -n '714,740p' base/src/auth.rs` — compares at `:718` and `:732`, `.get()` at `:723` (F9 evidence) | 0 |
| 34 | `sed -n '50,70p' .cartridge/config.lua` — `router` block still `:56-62`, `listen` still `:59`; `git diff` confines the change to `live` / `live-record` | 0 |
| 35 | sibling-state sweep of the parent's nine children; `an-instance-attaches-…` still `done`, composed test still `open` prio 85 | 0 |

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not supplied; not required under delegation.
User feedback/provenance: none for this revision.
Result: **PASS — 97/100**.
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to authorized implementation at `router.ctg` `65d22d7`,
carrying F8 (one-character guard anchor plus the Remaining-risk wording) and F9
(the `:718`/`:732` cite in the PRD Planning note, body only) along with it. If
either edit changes a Verify block, that is a formatting-level change to a gate
and should be re-run, not re-reviewed; any substantive change to the option,
footprint or boxes makes this rating stale and needs round 3.
