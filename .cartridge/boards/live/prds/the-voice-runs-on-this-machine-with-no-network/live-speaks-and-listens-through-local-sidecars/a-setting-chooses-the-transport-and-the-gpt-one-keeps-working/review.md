# A setting chooses the transport, and the GPT one keeps working — review history

Plan: `@live/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars/a-setting-chooses-the-transport-and-the-gpt-one-keeps-working`, `prd.ctg/.cartridge/boards/live/prds/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars/a-setting-chooses-the-transport-and-the-gpt-one-keeps-working/prd.md`.
Scope: leaf. One observable outcome — `live` gains a `provider` setting that selects the transport, with `gpt` the only shipped value and today's behaviour unchanged.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../../../workflows/review-plan.md) in the root board.
When copying this template, resolve that link relative to the actual owner board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: `live.ctg` at `ea3c16ea888bef0c946842749d1e333e355440aa` (working tree clean, `git status --porcelain` empty); superproject `cartridge` at `fd68eae` with `.cartridge/config.lua` dirty (outside this footprint). `prd.md` carries the coordinator's corrected census line ("three, five and ten, eighteen in all"); `specs/spec01.md` is the analyst's first draft, unedited.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `7f177e0749c605370d04aec9231150596c29c52efc7bb67097ba9f25f47fdbeb` |
| Specs | `specs/spec01.md` — `549419e90e4743ae139f9bc9de5229158d75f3df98bfeb3db3b83bbd865c4e58` |
| Material contracts/dependencies | `live.ctg` @ `ea3c16e` (`src/service.rs`, `src/socket.rs`, `src/lib.rs`, `cartridge.json`, `README.md`, `.cartridge/help.md`); `cartridge.ctg/src/transport/settings.rs` — `f82c8b056ee08fb2246e1aba01ca4287b7218cc396f68f6b18465df456561fc8` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | One outcome, one cartridge, footprint identical in PRD and spec, second transport explicitly excluded ("`PROVIDERS` stays a one-element list"). PRD is ~300 words. −3: the only user-visible behaviour this slice delivers is the rejection of an unknown `provider`, and that is the box with the weakest gate (see F1); the `PROVIDERS: [&str; 1]` const plus a `map/collect/join` to render a one-item list is scaffolding for a value the next child adds. |
| Ownership and reuse | 18 | Sole owner `live.ctg`; `src/socket.rs` stays untouched and keeps `URL` (`src/socket.rs:16`, verified); the existing loopback fixture `service::tests::voice_runs_a_session_on_the_wire_and_puts_both_devices_down_before_it_returns` (`src/service.rs:1303`) is correctly named as the proof that the GPT branch is unchanged; struct-level `#[serde(default)]` at `src/service.rs:18-19` plus the `Default` impl is reused instead of a new migration path. −2: a third crate-local `pub type Result<T> = …, String>` alias beside `src/socket.rs:12` and `src/service.rs:12`, and the `PROVIDERS` join where a literal error string is one line. |
| Dependencies and implementable slices | 18 | Base sha pinned and verified: `git rev-parse HEAD` in `live.ctg` = `ea3c16ea888…`. No new crate; `Cargo.toml`/`Cargo.lock` correctly declared out of footprint. Every call site the spec enumerates was checked and is accurate: `src/service.rs:5,50,63,95,268,274`, id field reads at `172,281,294,297`, `.audio()` `285`, `.send()` `308`/`778`, `.close()` `335`, `socket::pcm` `553`. The load-bearing host fact is confirmed: `cartridge.ctg/src/transport/settings.rs:38-53` is `#[serde(deny_unknown_fields)] pub struct Spec { type, default, optional, min, max, doc }` with `Kind` limited to integer/number/boolean/string/list/table (`:5-14`) — there is no `enum` key, so the Rust-side rejection is the only option. Type-checked the sketch against reality: `socket::connect` (`src/socket.rs:95-102`) is `async fn connect<F>(destination, key, session: Value, on_event: F) -> Result<Session> where F: Fn(Value) + Send + 'static`, which matches `Transport::open`'s signature and error type exactly, so `?` composes. −2: step 5 cites `start_voice (:264-287)`; the function runs `264-317` and the dial/id assignment ends at `281`. |
| Observable acceptance and baseline evidence | 12 | Baseline reproduced independently: `CARGO_TARGET_DIR=<scratch outside the repos> cargo test` in `/Users/feb/dev/cartridge/live.ctg` → `running 18 tests` … `test result: ok. 18 passed; 0 failed`, exit 0, 6.0 s compile + 0.79 s run. All four Verify blocks were run verbatim under `sh -eu -c` with cwd `/Users/feb/dev/cartridge/live.ctg` against the unmodified tree: block 1 exit 1 ("cartridge.json declares no `provider` setting"), block 2 exit 1, block 3 exit 1, block 4 exit 1 ("18 tests passed; 18 existed at ea3c16e and the seam owes at least one more"). No block passes before the change. No inert `! grep` guard anywhere: both `src/service.rs` guards use `if grep -qn …; then exit 1; fi`, and block 4's only negation is `if ! cargo test`, which is a real condition. `src/service.rs:1171` is indeed a doc comment naming `socket::connect`, and the spec flags it as the likeliest false failure — verified. −8 for two gate holes (F1, F2) and two weak greps (F3, F4). |
| Failure, recovery and compatibility | 14 | Default `"gpt"` plus `#[serde(default)]` keeps `wired()`'s `..Config::default()` (`src/service.rs:1159-1163`) and all 18 tests compiling unchanged; the unknown provider is rejected *before* `socket::credential`, so no key is read or spent for an invalid setting; the no-`enum` decision avoids making the manifest unloadable. −6: the spec never says that editing `cartridge.json` untrusts the cartridge and drops it from the running daemon until it is re-trusted, which is exactly what this change does to a live `live` node (F5); and `cargo clippy --all-targets`, the cartridge's own declared `check` command (`cartridge.json` `commands.check`), is not in any Verify block (F6). |
| Reviewer total | 79 / 100 | Below the 90 threshold, with two blocking findings. |

Findings and concrete revisions:

- **F1 (blocking) — nothing in Verify proves the setting is ever read.** `specs/spec01.md` Verify block 2 only asserts that `src/transport.rs` exists, names `enum Transport`/`socket::Session`/`socket::connect`/`socket::credential`, and that `src/service.rs` names neither symbol; block 1 only inspects `cartridge.json`. An implementation that adds the manifest key, creates `src/transport.rs` with `Transport::open` hardcoded to `Provider::Gpt`, and never adds `Config.provider` passes all four blocks green while delivering none of the PRD's headline outcome ("a setting chooses the transport", `prd.md` Outcome and Acceptance box 3/4). Remedy: add to block 2 `grep -q 'pub provider: String' src/service.rs` and `grep -q 'config.provider' src/transport.rs` (or `grep -q 'Provider::parse' src/transport.rs` together with a `grep -q '\.provider' src/transport.rs`), so the field and its single read site are both pinned.
- **F2 (blocking) — the census gate accepts a deleted test.** Block 4 asserts only `passed >= 19` and `grep -q '^transport::tests::' "$list"`. Deleting `service::tests::voice_runs_a_session_on_the_wire_and_puts_both_devices_down_before_it_returns` (`src/service.rs:1303`) — the spec's own stated proof that the GPT branch is unchanged — and adding two seam tests still yields 19 and still matches the grep, so PRD Acceptance box 5 ("the existing `mod tests` … pass unchanged") is unproven. This is the pattern the repo already recorded in `bun test names are not in its log`: pin the census *and* the titles. Remedy: after the `--list` capture, add `grep -q '^service::tests::voice_runs_a_session_on_the_wire_and_puts_both_devices_down_before_it_returns' "$list"` and, for the seam, a named test rather than a prefix, e.g. `grep -q '^transport::tests::an_unknown_provider_is_refused_before_any_dial' "$list"`.
- **F3 (non-blocking) — `grep -q '^transport::tests::' "$list"` accepts any test name.** Same line as F2. A test named `transport::tests::it_compiles` satisfies it; nothing requires the assertion that `Provider::parse("local")` is an `Err` whose message names `provider` and `gpt`, which is the spec's own Acceptance box 5. Remedy: fold into F2's named grep, and name the required assertion in the Implementation step so the title and the assertion travel together.
- **F4 (non-blocking) — the doc greps are substring-weak.** Verify block 3: `grep -q 'gpt' README.md` currently fails only because `README.md:3,16` spell it `GPT` uppercase; once the word `gpt` appears anywhere for any reason the check is vacuous, and `grep -q 'provider' .cartridge/help.md` matches any prose use. Remedy: grep the pair on one line, e.g. `grep -q '`provider`' README.md && grep -q 'default.*`gpt`' README.md`, or grep for the literal sentence the step writes.
- **F5 (non-blocking) — the manifest edit's operational cost is unstated.** `specs/spec01.md` step 1 changes `cartridge.json`, which untrusts the cartridge and makes the running daemon drop `live` until it is trusted again (repo memory: *Editing a manifest untrusts its cartridge*). The spec's "Nothing else changes" reads as if a reload suffices. Remedy: one line under *Base and dependencies* saying the manifest change requires re-trust plus `cartridge reload live` (or a `just launch`) before the setting is live, and that pass 2 of collect runs in the live checkout.
- **F6 (non-blocking) — the declared `check` command is not verified.** `live.ctg/cartridge.json` declares `check` = `cargo clippy --all-targets`, but no Verify block runs it; a new module with an unused `pub type Result` alias or an unused `PROVIDERS` const is exactly the kind of thing clippy reports. Remedy: append `cargo clippy --all-targets -- -D warnings` to block 4, reusing the same `CARGO_TARGET_DIR`; the cold compile measured 6.0 s, so the 120 s budget absorbs it.
- **F7 (non-blocking) — block 4 writes fixed `/tmp` paths.** `out=/tmp/live-transport-verify-test.txt` and `list=/tmp/live-transport-verify-list.txt` are shared between the lane pass and the repo pass and across any concurrent collect on this machine; a leftover file owned by another user makes the redirect fail. Remedy: `out="${TMPDIR:-/tmp}/live-transport-verify-$$.out"` (same for `list`).
- **F8 (non-blocking) — one-element ceremony.** `PROVIDERS: [&str; 1]` plus `.iter().map(|p| format!("`{p}`")).collect::<Vec<_>>().join(", ")` renders a single word. Remedy: a literal error message now; introduce the list in the child that adds the second transport, which is the commit that needs it.
- **F9 (non-blocking) — line-range drift.** `specs/spec01.md` step 5 says `start_voice (:264-287)`; the function is `src/service.rs:264-317` and the dial plus id assignment ends at `:281`. Remedy: cite `:264-281` for the replaced region.

Disposition: revise. No split — this is one mechanical seam across four source files and two doc pages, and the analyst's "no split needed" judgement holds. F1 and F2 are both closable by adding four greps to the existing blocks; no restructuring is required.

Validation: cwd `/Users/feb/dev/cartridge/live.ctg` throughout, `CARGO_TARGET_DIR` forced to `/private/tmp/claude-501/…/scratchpad/reviewer-live-transport/target` (outside every repo, so no live cartridge was hot-restarted). `git rev-parse HEAD` → `ea3c16ea888bef0c946842749d1e333e355440aa`, `git status --porcelain` empty. Verify blocks extracted verbatim from `specs/spec01.md` and run as `sh -eu -c "$(cat blockN.sh)"`: block 1 → exit 1; block 2 → exit 1; block 3 → exit 1; block 4 → exit 1 with `cargo test` itself exit 0 and `test result: ok. 18 passed; 0 failed; 0 ignored` (0.79 s; 6.0 s cold compile, well inside the 120 s block limit). Host fact re-read at `cartridge.ctg/src/transport/settings.rs:5-53`. No file in `live.ctg` or in the PRD directory other than this `review.md` was written.

Reviewer identity: independent reviewer subagent (Claude Opus 5, 1M context) for the `live` board loop, session `546d3989`; peer of `analyst-1`, not its author.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: F1 (Verify never proves `config.provider` is read), F2 (the `>= 19` census admits a deleted baseline test).
Rounds used / remaining: 1 / 4.
Next action: bounded revision of `specs/spec01.md` closing F1 and F2 (four added greps) and, cheaply, F3–F9; then round 2.

## Round 2 — 2026-09-17

Presented revision: `specs/spec01.md` rewritten in place by the analyst (its own "Revision 2, answering review round 1 (F1–F9)", `specs/spec01.md:15`); `prd.md` unchanged since round 1. `live.ctg` still at `ea3c16ea888bef0c946842749d1e333e355440aa`, `git status --porcelain` empty before and after this review. Superproject `cartridge` at `fd68eae` with six dirty submodule pointers plus `.cartridge/config.lua`, all outside this footprint.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `7f177e0749c605370d04aec9231150596c29c52efc7bb67097ba9f25f47fdbeb` (unchanged from round 1) |
| Specs | `specs/spec01.md` — `f4d8a348927c18534a0c8478b0d326ce13bf4c693c9ec45d38e973f31a2c5893` (round 1 reviewed `549419e9…`) |
| Material contracts/dependencies | `live.ctg` @ `ea3c16e`; `cartridge.ctg` @ `4b607ea`, `src/transport/settings.rs` — `f82c8b056ee08fb2246e1aba01ca4287b7218cc396f68f6b18465df456561fc8` (unchanged) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome, one cartridge, footprint identical in PRD and spec, second transport still excluded (`specs/spec01.md:271-274`). Round 1's −3 is half repaid: the `PROVIDERS: [&str; 1]` const and its `map/collect/join` are gone, replaced by a literal error string (`specs/spec01.md:73-75, 113-115`). −2: the slice's only user-visible behaviour is the rejection of an unknown `provider`, and no Verify block proves that behaviour exists — block 4 pins the test *name* `transport::tests::an_unknown_provider_is_refused_before_any_dial` (`specs/spec01.md:259`) and nothing else. I built the required module with both test bodies emptied to `{}` and block 4 exited **0**. |
| Ownership and reuse | 20 | Both round-1 reuse deductions closed. `src/transport.rs` now imports `crate::socket::Result` (`specs/spec01.md:60`) instead of declaring a third crate-local alias beside `src/socket.rs:12` and `src/service.rs:12`, and the spec says so explicitly at `:113-115`. `src/socket.rs` stays untouched with `URL` pinned verbatim by Verify block 2 (`specs/spec01.md:204`, matches `src/socket.rs:16`). The loopback fixture `service::tests::voice_runs_a_session_on_the_wire_and_puts_both_devices_down_before_it_returns` (`src/service.rs:1304`) is reused as the compatibility proof and is now pinned by name. Confirmed no other file in `live.ctg/src` names `socket::connect` or `socket::credential`, so guarding `src/service.rs` alone is sufficient. |
| Dependencies and implementable slices | 19 | Base sha re-verified: `git -C live.ctg rev-parse HEAD` = `ea3c16ea888…`. No new crate; `Cargo.toml`/`Cargo.lock` out of footprint (`live.ctg/Cargo.toml` has no path dependency, so a lane builds standalone). Every call site re-checked against the tree and correct: `src/service.rs:5,50,63,95,268,274`, id reads `172,281,294,297`, `.audio()` `285`, `.send()` `308`/`778`, `.close()` `335`, `socket::pcm` `553`, the doc-comment trap `1171`. `socket::connect` (`src/socket.rs:95-102`) and `Transport::open` share the error type, so `?` composes. Host fact re-read and still true. −1 for residual line drift (F12). |
| Observable acceptance and baseline evidence | 14 | Up from 12. The eighteen names in Verify block 4 are **exactly** the `cargo test -- --list` set at `ea3c16e` — I compared them as sets, symmetric difference empty. Renaming one baseline test away in a scratch copy made block 4 exit 1 with `missing test: service::tests::voice_runs_a_session_on_the_wire_…` while the tree stayed green at 20 tests, so F2 is genuinely closed. Clippy is in the block, `$TMPDIR`/`$$` replaces the fixed `/tmp` paths, the doc greps now require `` `provider` `` and `` `gpt` `` on one line, and all four blocks exit 1 verbatim on the clean tree. −6 for F10 (the gate is green on an implementation in which the setting is never read) and F13 (the spec asserts a compile-enforcement that does not exist). |
| Failure, recovery and compatibility | 19 | Both round-1 deductions closed. `specs/spec01.md:25` now carries the re-trust cost of the manifest edit in full, including that collect's pass 2 runs in the live checkout and that a live `status` is not evidence during that window. `cargo clippy --all-targets -- -D warnings` — the cartridge's declared `check` (`cartridge.json` `commands.check` = `cargo clippy --all-targets`) — is the last command of block 4, run under the same isolated `CARGO_TARGET_DIR`. `CARGO_TARGET_DIR` defaults to `$PWD/target/<slug>-verify`, which `live.ctg/.gitignore` already ignores (`target`) and which is not `target/debug`, so pass 2 writes nothing in the footprint and hot-restarts nothing. Default `"gpt"` plus `#[serde(default)]` keeps `wired()`'s `..Config::default()` compiling. −1 for F14. |
| Reviewer total | 90 / 100 | At the threshold on points, but FAIL: one blocking finding is unresolved. |

### Verdict on each round-1 finding

- **F1 — closed as written; the defect it named survives as F10.** I built the exact implementation the round-1 reviewer described in a scratch copy of `live.ctg` (`git archive ea3c16e`, outside every repository): manifest key added, `src/transport.rs` with `Transport::open` matching on a hardcoded `Provider::Gpt`, no `provider` field on `Config` at all, `src/service.rs` fully rewired, both doc pages updated. Blocks 1 and 3 exit 0; **block 2 exits 1**, and `sh -eux` shows it dying on the new `grep -q 'pub provider: String' src/service.rs` (`specs/spec01.md:201`). The round-1 cheat no longer passes. But see F10: a slightly different implementation that adds the field and never reads it passes all four.
- **F2 — closed.** Counting is gone; block 4 (`specs/spec01.md:239-262`) greps twenty names out of `cargo test -- --list`. The eighteen baseline names are exact against `ea3c16e` (set comparison, no difference either way). Renaming `service::tests::voice_runs_a_session_on_the_wire_and_puts_both_devices_down_before_it_returns` to `voice_runs_a_session` in a scratch copy that was otherwise green at 20 tests made block 4 exit 1 naming the missing test. The loop is `grep -q … || { echo …; exit 1; }` — no inert guard.
- **F3 — closed.** The `^transport::tests::` prefix grep is gone; both seam tests are named (`specs/spec01.md:258-259`) and step 4 (`:117-125`) states the assertion each owes. The assertions are still not enforced (F10/F13), but the finding as written is addressed.
- **F4 — closed.** Block 3 (`specs/spec01.md:218-222`) loops both pages and requires `` `provider` `` and `` `provider`.*`gpt` `` on one line; step 8 (`:138-139`) writes the sentence. Verified it fails on the clean tree and passes on a scratch tree carrying the suggested line.
- **F5 — closed.** `specs/spec01.md:25`.
- **F6 — closed.** `specs/spec01.md:263`, and the base is measured clean.
- **F7 — closed.** `specs/spec01.md:227-228`, `"${TMPDIR:-/tmp}/live-transport-verify-$$.out"` / `.list`.
- **F8 — closed.** `specs/spec01.md:113-115`.
- **F9 — closed, and round 1 was itself wrong.** The replaced region is now cited `:268-281` with the function at `:264-317`; both are correct. The analyst is right about `wired()`: it is `src/service.rs:1280-1293` (`fn wired` at `:1280`, closing brace at `:1293`), and its `Config` literal with `..Config::default()` is `:1282-1286` (the spread itself at `:1285`). Round 1's `src/service.rs:1159-1163` is the *other* helper, `fn service()` at `:1157` with its `..Config::default()` at `:1162`. **Round 1 cited the wrong function; the analyst's correction stands.**

### New findings

- **F10 (blocking) — the gate is still green on an implementation that never reads the setting.** `specs/spec01.md:201-203` pins `pub provider: String` in `src/service.rs`, `config.provider` in `src/transport.rs` and `Provider::parse` in `src/transport.rs` as three *independent* greps. I built a scratch implementation in which `Config` carries `pub provider: String` with a `"gpt"` default that nothing ever reads, `src/transport.rs` calls `Provider::parse("gpt")?` on a literal, and the string `config.provider` appears only inside a `//` comment one line above it. All four blocks exit **0, 0, 0, 0** — green collect, 20 tests, clippy clean — and the PRD's headline outcome ("it asks a seam which transport to build", `prd.md` Outcome; Acceptance boxes 3 and 4) is delivered by none of it. The compiler does not catch the dead field either: `#[derive(Debug)]` on `Config` (`src/service.rs:19`) counts as a read, so `[lints.rust] warnings = "deny"` never fires. Remedy — one line, replacing the two weak greps at `specs/spec01.md:202-203`: `grep -q 'Provider::parse(&config.provider)' src/transport.rs`. That pins the expression rather than two symbols that can sit in a comment and a literal, and it cannot be satisfied without the field being read. Pair it with `grep -q 'Config::default().provider' src/transport.rs` so the required test's body — not just its name — is on the gate.
- **F11 (non-blocking) — a required test's body is unpinned, so the behaviour in PRD Acceptance box 4 is unproven.** Block 4 greps only names out of `--list`. I replaced both seam test bodies with `{}` in an otherwise-correct scratch implementation and block 4 exited 0. "Selecting an unknown provider fails the `voice` call with a message naming the setting and the values it accepts" (`prd.md` Acceptance box 4) therefore has no gate. Remedy: `grep -q 'Provider::parse("local")' src/transport.rs` next to F10's greps, or fold the assertion into the same grep pair; the F10 remedy covers half of this already.
- **F12 (non-blocking) — residual line drift, three places.** `specs/spec01.md:31` says `wired()` "overwrites it with the fixture at `:1291`"; `service.endpoint = fixture.endpoint.clone();` is at `src/service.rs:1290` and `:1291` is `service.opener = opener;`. `specs/spec01.md:53` cites "the struct-level `#[serde(default)]` (`:19`)"; `#[serde(default)]` is `src/service.rs:20` and `:19` is the `#[derive]`. The same line cites the `Default` impl as `:32-44`; it is `:32-45`. Remedy: `:1290`, `:20`, `:32-45`.
- **F13 (non-blocking) — the spec states a compile-enforcement it does not have.** `specs/spec01.md:119-121`: "Reading `Config::default().provider` is what makes step 2's field compile-enforced: the test cannot build if `Config` has no `provider`." The analyst's report repeats this as its answer to F1 ("fails the build, not just a grep"). It is true only of the body the spec *suggests*; Verify pins the name, so an implementation that writes the name with any body compiles and collects green (proved above). Remedy: either delete the sentence or make it true with F10's `Config::default().provider` grep. As written it is the kind of claim a later reader trusts instead of re-deriving.
- **F14 (non-blocking) — block 4 leaks its scratch files on every failure path.** `rm -f "$out" "$list"` (`specs/spec01.md:264`) is the last line, so under `sh -eu` a failing `cargo test`, a missing test name or a clippy warning leaves both files in `$TMPDIR`. Harmless but unbounded across reruns. Remedy: `trap 'rm -f "$out" "$list"' EXIT` right after the assignments.

Disposition: revise. F10 is one grep line; F11–F14 are one line each. No restructuring, no split — the spec is otherwise the strongest artifact this board has produced, and its round-1 repairs are real.

Validation: cwd `/Users/feb/dev/cartridge/live.ctg` for the clean-tree runs; scratch copies at `/private/tmp/claude-501/…/scratchpad/reviewer-live-transport-r2/cheat{A,B,D,E}`, each `git archive ea3c16e | tar -x`, never the live tree. `CARGO_TARGET_DIR` forced to `…/scratchpad/reviewer-live-transport-r2/target{,-cheat,-cheat2}`, outside every repository, so no cartridge was hot-restarted. Blocks extracted by fence from `specs/spec01.md` (four ```sh fences after `## Verify and Proof`) and run as `sh -eu -c "$(cat blockN.sh)"`.

| Tree | B1 | B2 | B3 | B4 | note |
| --- | ---: | ---: | ---: | ---: | --- |
| clean `live.ctg` @ `ea3c16e` | 1 | 1 | 1 | 1 | matches the analyst's report; B4 walked all eighteen baseline names then failed on `missing test: transport::tests::the_default_provider_builds_the_gpt_transport`; `cargo test` itself exit 0, `18 passed; 0 failed`, 0.78 s |
| cheatA — round-1 cheat, no `Config.provider` | 0 | **1** | 0 | 101 | B2 dies on `grep -q 'pub provider: String' src/service.rs`; F1's described cheat is caught |
| cheatB — field present, never read, `Provider::parse("gpt")` literal | 0 | 0 | 0 | **0** | **F10**: green collect, 20 tests, clippy clean, setting never read |
| cheatD — cheatB with one baseline test renamed away | — | — | — | **1** | `missing test: service::tests::voice_runs_a_session_on_the_wire_…`; F2 closed |
| cheatE — cheatB with both seam test bodies emptied | — | — | — | **0** | **F11**: names satisfy the gate, assertions are not required |

Inert-guard scan: `grep -n '!\s*grep'` over `specs/spec01.md` returns nothing. Block 4's only `!` is `if ! cargo test`, a real condition inside an `if`. Block 3's loop is `grep -q … || { echo …; exit 1; }`.

Post-conditions: `git -C /Users/feb/dev/cartridge/live.ctg status --porcelain` empty and `rev-parse HEAD` = `ea3c16ea888bef0c946842749d1e333e355440aa` after every experiment. No file in `live.ctg`, no spec and no `prd.md` was written; only this `review.md` and the loop's `reviewer-2.md`. No `prd` transition, no commit.

Reviewer identity: independent reviewer subagent (Claude Opus 5, 1M context) for the `live` board loop, session `546d3989`, round 2. Not the author of the plan, the spec or the round-1 review.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (90/100 on points, one unresolved blocking finding).
Unresolved blocking findings: F10 (Verify is green on an implementation in which `config.provider` is never read).
Rounds used / remaining: 2 / 3.
Next action: one-line revision of `specs/spec01.md` — replace the `config.provider` and `Provider::parse` greps at `:202-203` with `grep -q 'Provider::parse(&config.provider)' src/transport.rs` and `grep -q 'Config::default().provider' src/transport.rs`; fold in F11–F14; then round 3.

## Round 3 — 2026-09-17

Presented revision: `specs/spec01.md` republished in place by the analyst as its revision 3 (`specs/spec01.md:15`, "answering review rounds 1 (F1–F9) and 2 (F10–F14)"); `prd.md` unchanged since round 1. `live.ctg` at `ea3c16ea888bef0c946842749d1e333e355440aa`, `git status --porcelain` empty before and after this review.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `7f177e0749c605370d04aec9231150596c29c52efc7bb67097ba9f25f47fdbeb` (unchanged from rounds 1–2) |
| Specs | `specs/spec01.md` — `f6dbc9008ce0e767d04c8e9aae792a462669f7becaef67856a20193f8f4e02f3` (round 2 reviewed `f4d8a348…`) |
| Material contracts/dependencies | `live.ctg` @ `ea3c16e`; `cartridge.ctg/src/transport/settings.rs` — `f82c8b056ee08fb2246e1aba01ca4287b7218cc396f68f6b18465df456561fc8` (unchanged) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome, one cartridge, footprint identical in PRD and spec, second transport still excluded (`specs/spec01.md:179-182`). −2, unchanged from round 2: the slice's only user-visible behaviour is the refusal of an unknown `provider`, and no block executes that behaviour — block 4 runs `cargo test`, but the two seam tests that would prove it are gated on their *text*, and I passed that gate with two assertions that are true of any tree (F18). |
| Ownership and reuse | 20 | Unchanged and still correct. `crate::socket::Result` reused (`specs/spec01.md:60,113`), `src/socket.rs` untouched with `URL` pinned verbatim (block 2, matches `src/socket.rs:16`), the loopback fixture at `src/service.rs:1304` reused as the compatibility proof and pinned by name in block 4. |
| Dependencies and implementable slices | 19 | Base sha re-verified (`git -C live.ctg rev-parse HEAD` = `ea3c16ea888…`). Every call site re-checked against `ea3c16e`: `:268` credential, `:274` dial, `:281` id, `:1290` fixture endpoint, `:1282-1286` the `..Config::default()` literal, `:32-45` the `Default` impl, `:1171` the doc-comment trap, `src/socket.rs:95-102`. −1 for residual drift (F19). The honest tree confirms the steps are sufficient and complete: applied verbatim they compile, test and lint (see Validation). |
| Observable acceptance and baseline evidence | 13 | Down 1 from round 2. The round-2 cheat is genuinely dead: against the analyst's own `r3/cheat` block 2 exits 1 with seven named reasons, and an empty `{}` seam body is refused. But **I wrote two new half-implementations that pass all four blocks, clippy-clean, 20 tests green, with the setting still not choosing anything** (F15, F16) — and one of them is three lines away from the honest tree. At the same time the new python gate produces a false red on a *correct* implementation that merely writes `"gpt".to_string()` and wraps the parse call over two lines (F17). A gate that is both bypassable and brittle has bought machinery, not assurance. Clean-tree baseline re-measured independently: blocks 1–4 all exit 1 at `ea3c16e`. |
| Failure, recovery and compatibility | 19 | Unchanged from round 2 and now with F14 closed: `trap 'rm -f "$out" "$list"' EXIT` is block 4 line 4 (`specs/spec01.md:250`), and after a failing clean-tree run `${TMPDIR}/live-transport-verify-*` does not exist (checked, no matches). Re-trust cost of the manifest edit still stated in full (`specs/spec01.md:25`), clippy still the last command of block 4 under an isolated `CARGO_TARGET_DIR` that is not `target/debug`. −1: `specs/spec01.md:148` asserts "the body of `Transport::open` parses `config.provider` — not a string literal. The setting is chosen, not assumed", which the gate does not carry (F15) — the same over-claim shape as the withdrawn F13. |
| Reviewer total | 89 / 100 | Below the 90 threshold, with two blocking findings. |

### Verdict on each earlier finding

- **F1 (r1) — closed.** Superseded by F10/F15; the round-1 cheat (no `Config.provider` at all) dies on `pub provider: String` in block 2.
- **F2 (r1) — closed.** Block 4 greps twenty names out of `cargo test -- --list`; I re-ran it on the clean tree and it walked all eighteen baseline names before failing on `transport::tests::the_default_provider_builds_the_gpt_transport`.
- **F3, F4, F5, F6, F7, F8 (r1) — closed**, as round 2 found; re-checked, all still present in revision 3 (`specs/spec01.md:22,25,113-115,222-224,249-250,262`).
- **F9 (r1) — closed.** `:268-281` / `:264-317` cited at `specs/spec01.md:133`; the region is right (see F19 for the function's end line).
- **F10 (r2, blocking) — closed as written, not in substance.** The exact cheat round 2 built — field declared and never read, `Provider::parse("gpt")` on a literal, `config.provider` only in a `//` comment — now exits 1 from block 2 with seven named reasons; I ran the analyst's `r3/cheat` myself and reproduce that output. But the defect class it named (Verify green on a tree where the setting does not choose anything) is alive: see F15 and F16, both built from scratch by me.
- **F11 (r2, non-blocking) — half closed.** `{}` bodies are refused (brace-matched, verified). The behaviour is still unproven: see F18.
- **F12 (r2, non-blocking) — partly closed.** `:1291`→`:1290` and `:32-44`→`:32-45` are fixed and now correct against `ea3c16e`. `:19`→`:20` is **not** fixed: `specs/spec01.md:53` still reads "The struct-level `#[serde(default)]` (`:19`)" while `#[serde(default)]` is `src/service.rs:20` and `:19` is the `#[derive]`. See F19.
- **F13 (r2, non-blocking) — closed.** The "cannot compile without the field" claim is gone. `specs/spec01.md:125-129` now says the block enforces the *text* of a compiled non-comment body and cannot prove semantics, and `specs/spec01.md:165-173` adds *What these blocks do not prove*. That paragraph is the most honest thing in the spec — and F15 is exactly the hole it half-admits to.
- **F14 (r2, non-blocking) — closed.** `trap … EXIT` verified; no leftovers after a failing run.

### New findings

- **F15 (blocking) — block 2's `fn open` gate is satisfied by a parse whose result is thrown away.** `specs/spec01.md:199-206` requires the literal text `Provider::parse(&config.provider)` inside the brace-matched body of `fn open` and refuses `Provider::parse("…")` there. I took the honest tree and changed three lines of `src/transport.rs`: `let _ = Provider::parse(&config.provider);` followed by `match Provider::Gpt {`. The required text is present, no literal parse appears, so **blocks 1–4 exit 0, 0, 0, 0**, `cargo test` reports `20 passed; 0 failed`, `cargo clippy --all-targets -- -D warnings` is clean (`Result` is `#[must_use]`, but `let _ =` silences it). A runtime probe in that tree shows the consequence: `Transport::open` with `provider: "local"` does not refuse — it walks straight into the GPT branch and fails with `No OpenAI API key…`, i.e. it *dialled*. PRD Acceptance box 4 ("Selecting an unknown provider fails the `voice` call with a message naming the setting") is delivered by nothing, and collect is green. Remedy — stop grepping for the read and execute it. Add one required name to block 4's census, e.g. `service::tests::an_unknown_provider_fails_the_voice_call_before_any_dial`, and an implementation step for it: build the service through the existing `wired()` fixture (`src/service.rs:1280-1293`) with `provider: "local"`, call `voice`, assert the returned error contains `` `provider` `` and `` `gpt` `` and that the fixture saw no connection. A test that *runs* cannot be satisfied by text; it closes F10, F15, F16 and F18 at once, and it lets most of the python go (see F17).
- **F16 (blocking) — `body(transport, 'fn open')` matches the first substring `fn open`, not the function `open`.** `specs/spec01.md:191,199` (`start = text.find(head)` with `head = 'fn open'`). Any earlier item whose name merely *begins* with `open` captures the gate. I added `pub fn open_is_possible(config: &Config) -> bool { Provider::parse(&config.provider).is_ok() }` above `impl Transport`'s real `open`, left the real `open` matching on `Provider::parse("gpt")?`, called the probe from the first seam test and marked it `#[allow(dead_code)]`: **blocks 1–4 exit 0, 0, 0, 0**, 20 tests, clippy clean. Remedy: F15's executed test makes this moot. If the python stays, anchor on the real signature — `re.search(r'\bfn\s+open\s*(<|\()', text)` — and scan *every* match rather than the first, failing if any body hands the parse a literal.
- **F17 (non-blocking, but the reason to cut the machinery) — the gate false-reds on a correct implementation.** From the honest tree I changed two things no reviewer would question: `provider: "gpt".to_string()` instead of `.into()`, and the parse call wrapped over two lines the way rustfmt wraps a long one. `cargo test` still reports `20 passed`; **block 2 exits 1** with `src/service.rs: Config::default does not set provider to "gpt"` and `src/transport.rs: \`fn open\` does not parse \`config.provider\``. Forty lines of python that a correct diff trips over and two wrong diffs walk through is a bad trade. What I would keep from block 2: `test -f src/transport.rs`, the four structural greps, the `URL` pin, both `if grep -qn … ; then exit 1; fi` negative guards on `src/service.rs`, the comment stripper, and `pub provider: String`. What I would cut: the `fn open` body machinery and the seam-test body machinery, replaced by F15's executed test. If any textual check survives, normalise first — compare on `re.sub(r'\s+', '', body)` and accept `"gpt".into()`, `"gpt".to_string()` and `String::from("gpt")` through one regex on the brace-matched `fn default` body.
- **F18 (non-blocking) — the seam-test body gate is satisfied by assertions that are true of every tree.** `specs/spec01.md:207-212` requires each body to contain `assert` plus fixed text. In my cheat the bodies are `assert!(!Config::default().provider.is_empty());` and `let text = "\`provider\` is set to \`local\`; live accepts \`gpt\`."; assert_eq!(text.trim(), text);`. Both pass block 2, both pass `cargo test`, neither touches `Provider::parse`. This is F11 in its next shape and it dies with F15's remedy.
- **F19 (non-blocking) — residual line drift, two places.** `specs/spec01.md:53` cites `#[serde(default)]` as `:19`; it is `src/service.rs:20` (F12's unfixed third item). `specs/spec01.md:133` says `start_voice` "runs `:264-317`"; the function closes at `src/service.rs:315` and `:317` is the next item's doc comment. Remedy: `:20` and `:264-315`.

Disposition: revise. One substantive change — replace block 2's `fn open` and seam-test python with a required *executed* test in block 4's census, and write the step that produces it — plus two one-word line fixes. The spec's structure, its steps, its operational notes and its *What these blocks do not prove* paragraph are all sound and should survive the edit intact.

Validation: blocks extracted by fence from `specs/spec01.md` (four ```sh fences after `## Verify and Proof`) and run as `sh -eu -c "$(cat blockN.sh)"`. Clean-tree runs with cwd `/Users/feb/dev/cartridge/live.ctg`; every scratch tree is `git archive ea3c16e | tar -x` (or a copy of one) under `…/scratchpad/reviewer-live-transport-r3/`, never the live tree. `CARGO_TARGET_DIR` forced to a per-tree directory under that scratchpad, outside every repository, for every cargo invocation, so no cartridge was hot-restarted.

| Tree | B1 | B2 | B3 | B4 | note |
| --- | ---: | ---: | ---: | ---: | --- |
| clean `live.ctg` @ `ea3c16e` | 1 | 1 | 1 | 1 | B1 "declares no `provider` setting"; B4 walks all eighteen baseline names, then `missing test: transport::tests::the_default_provider_builds_the_gpt_transport`; `cargo test` itself exit 0 |
| `honest` — every step applied verbatim (analyst's tree, diffed against `ea3c16e` line by line and confirmed to be the spec's steps and nothing else) | 0 | 0 | 0 | 0 | `20 passed; 0 failed`, clippy clean. The gate is satisfiable as written. |
| analyst's `r3/cheat` — the round-2 defect | — | **1** | — | — | seven named reasons, covering F10 and F11 as reported |
| **`cheatX` (mine)** — honest, then `let _ = Provider::parse(&config.provider);` + `match Provider::Gpt` + two trivially-true seam assertions | **0** | **0** | **0** | **0** | **F15/F18**: 20 tests, clippy clean, and a runtime probe prints `No OpenAI API key…` for `provider: "local"` — it dialled instead of refusing |
| **`cheatY` (mine)** — decoy `pub fn open_is_possible` before the real `open`, which parses the literal `"gpt"` | **0** | **0** | **0** | **0** | **F16**: the gate reads the first `fn open` substring, never the real function |
| `reformat` — honest with `"gpt".to_string()` and the parse call wrapped over two lines | — | **1** | — | — | **F17**: false red on a correct tree; `cargo test` still `20 passed` |

Inert-guard scan: `grep -n '!\s*grep'` over `specs/spec01.md` returns nothing; there is no statement-level `! grep` anywhere. No `grep 'a\|b'` alternation in any block (the only `|` characters are shell `||`), so nothing depends on GNU grep. Block 3's loop and block 4's census both use `grep -q … || { echo …; exit 1; }`; block 2's negatives are `if grep -qn …; then exit 1; fi`. `trap … EXIT` confirmed to leave no `${TMPDIR}/live-transport-verify-*` behind after a failing run.

Post-conditions: `git -C /Users/feb/dev/cartridge/live.ctg status --porcelain` empty and `rev-parse HEAD` = `ea3c16ea888bef0c946842749d1e333e355440aa` after every experiment. No file in `live.ctg`, no spec and no `prd.md` was written; only this `review.md` and the loop's `reviewer-3.md`. No `prd` transition, no commit.

Reviewer identity: independent reviewer subagent (Claude Opus 5, 1M context) for the `live` board loop, session `546d3989`, round 3. Not the author of the plan, the spec, or the round-1 or round-2 reviews.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (89/100, two unresolved blocking findings).
Unresolved blocking findings: F15 (a discarded parse satisfies the `fn open` gate; unknown provider still dials), F16 (the gate inspects the first `fn open` substring, so a decoy captures it).
Rounds used / remaining: 3 / 2.
Next action: one substantive revision — replace block 2's `fn open` / seam-test python with an executed test (`service::tests::an_unknown_provider_fails_the_voice_call_before_any_dial` through the `wired()` fixture) added to block 4's census and written as an implementation step; keep the structural greps, the comment stripper and both negative guards; fix `:20` and `:264-315`. Then round 4.


## Round 4 — 2026-09-17

Presented revision: `specs/spec01.md` revision 4, published in place (analyst's
`spec04.md` draft). `live.ctg` at `ea3c16ea888bef0c946842749d1e333e355440aa`,
`git -C live.ctg status --porcelain` empty before and after this review.
`prd.md` unchanged since round 1.

| Input | Content digest |
| --- | --- |
| Plan | `prds/…/a-setting-chooses-the-transport-and-the-gpt-one-keeps-working/prd.md` — SHA-256 `7f177e0749c605370d04aec9231150596c29c52efc7bb67097ba9f25f47fdbeb` |
| Specs | `specs/spec01.md` — SHA-256 `867b64884d6504b3e9d5123f8e7f2f5cb55d5f3d79e542451d3c83226a96b0d4` |
| Material contracts/dependencies | `live.ctg@ea3c16e` (`src/service.rs`, `src/socket.rs`, `src/lib.rs`, `cartridge.json`, `README.md`, `.cartridge/help.md`); `cartridge.ctg/src/transport/settings.rs` `Spec` (`deny_unknown_fields`, no `enum` key) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Unchanged and still right. One observable outcome, one owner, the second transport explicitly deferred, and *Remaining work* tells the implementer not to widen `Transport::open` or add a provider list. −1 stands only because `prd.md` Acceptance box 5 still carries the stale "three, three and five" census inline; the spec corrects it, the PRD text does not. |
| Ownership and reuse | 19 | `crate::socket::Result` reused rather than a third alias; `socket::URL` unmoved; `Session` stays `socket`'s; no new crate dependency; the loopback fixture and `only_the_dummy_key` are reused rather than reinvented, and step 5 refuses to change `wired()`'s signature because three baseline tests call it — correct call, and I confirmed those three call sites survive untouched in my build. |
| Dependencies and implementable slices | 19 | I built the spec from its own text, without the analyst's tree: every anchor in steps 1–9 matched first time (patch anchors asserted, not assumed), the result compiles, `cargo test` → **21 passed**, `cargo clippy --all-targets -- -D warnings` exit 0. The `:1171` doc-comment trap, `socket::pcm` keeping `use crate::socket;` alive, and the four `.id` → `.id()` conversions are all called out in advance and all four were exactly what the compiler asked for. This is a spec an implementer can execute. |
| Observable acceptance and baseline evidence | 13 | Down from 14. The executed test is a real advance over three rounds of text matching, and it is genuinely independent (see F15 and the shared-fixture ruling). But **the gate is still beaten, by F20**: block 4 pins the test's *name* and nothing else, block 2 no longer inspects any test body, so a tree that keeps the name and swaps the body for the cheap unit-test assertion passes 0,0,0,0 while `Transport::open` throws the setting away. Built it; see F20. The spec's own sentence "It cannot be written around by shaping the source" is false of the test's own source. |
| Failure, recovery and compatibility | 19 | Unchanged. All eighteen baseline names verified present by name in my honest build's `--list`; the wire test green; clippy last in block 4 under an isolated `CARGO_TARGET_DIR` that is never `target/debug`; `trap … EXIT` on the scratch files; the manifest re-trust cost and the pass-2 hot-restart hazard both stated. No statement-level `! grep` anywhere in the four blocks (scanned), no `grep 'a\|b'` alternation (scanned). |
| Reviewer total | **89 / 100** | |

### The five trees, my own, every block run as `sh -eu -c "$(cat blockN.sh)"`

Blocks extracted verbatim from `specs/spec01.md` by fence after `## Verify and Proof`.
cwd = each tree's root; `CARGO_TARGET_DIR` per tree under
`/private/tmp/…/scratchpad/reviewer-live-transport-r4/target-*`, outside every repository.
Trees are `git -C live.ctg archive ea3c16e` copies; nothing in `live.ctg` was written.

| Tree | b1 | b2 | b3 | b4 | `cargo test` |
| --- | ---: | ---: | ---: | ---: | --- |
| `clean` — `ea3c16e` untouched | **1** | **1** | **1** | **1** | 18 passed |
| `honest` — steps 1–9 applied verbatim by me | 0 | 0 | 0 | 0 | 21 passed, ×3 runs, no flake |
| `honest3` — F17 probe: `provider: "gpt".to_string()` and `Provider::parse(config.provider.as_str())` | 0 | 0 | 0 | 0 | 21 passed |
| `cheatA` — F15 rebuilt: `let _ = Provider::parse(&config.provider);` then `match Provider::Gpt` | 0 | 0 | 0 | **1** | 19 passed, 2 failed |
| `cheatC` — **F20**: `cheatA`'s transport + the gating test's name kept, body swapped | 0 | 0 | 0 | **0** | 21 passed, clippy clean |

`honest2`, a fourth probe, is reported under F21.

### Findings

- **F20 (blocking, new) — the executed gate pins a name, not a test; swap the body and the setting is unread again.** Block 4 greps `service::tests::an_unknown_provider_fails_the_voice_call_before_any_dial` out of `cargo test -- --list`. Nothing in any block looks at that function's body — round 3's body matcher was removed with the rest of the python, and block 2's two survivors only touch `Config` and `src/transport.rs`. I took `cheatA` — `Transport::open` parses `config.provider`, discards the result, and dials GPT whatever the setting says — and replaced the body of the named test with the cheap assertion a tired implementer would reach for anyway:

  ```rust
  #[tokio::test(flavor = "multi_thread")]
  async fn an_unknown_provider_fails_the_voice_call_before_any_dial() {
      let refused = crate::transport::Provider::parse("local").expect_err("refused");
      assert!(refused.contains("provider") && refused.contains("gpt"));
  }
  ```

  **Blocks 1–4 exit 0, 0, 0, 0**, `cargo test` reports 21 passed, clippy is clean. In that tree `provider: "local"` still dials GPT Live, which is precisely PRD Acceptance box 4 unimplemented. This is F11 in its fourth costume: the gate has moved from "a name with an empty body" to "a name with an honest-looking body that tests the wrong function", and the test-body defect class is the one this PRD has failed on in every round. Note this cheat is not adversarial — it is the *cheaper* test to write, and the spec's step 5 code block is the only thing telling the implementer otherwise.

  Remedy, and it is one small loose check, not a parser: block 2's surviving python already reads `src/service.rs` with comments stripped. Add to its `fail` list that the non-comment text of `src/service.rs` must contain all four of `provider: "local"`, `.voice(`, `expect_err` and `fixture.received` — the tokens that make the step-5 body the body it is. These compose only inside a test that actually drives `voice` against the fixture and expects a refusal, so a tree that keeps them and still dials returns `Ok` and dies at `expect_err`. It cannot false-red the spec's own step 5 (verified: my `honest` and `honest3` trees both contain all four verbatim), it adds no matching of expressions, and it leaves the "weak by design" character of block 2 intact. Tighten it to a sliced test region only if a cheaper form proves insufficient.

- **F21 (non-blocking) — block 2's `config.provider` check is a literal substring, so a line break between `config` and `.provider` reds a correct tree.** Fourth probe `honest2`: the honest tree with the parse hand-wrapped as `Provider::parse(\n &config\n .provider,\n)?` — block 2 exits 1 with ``src/transport.rs: the seam never reads `config.provider` ``. rustfmt does not produce that wrap from the spec's own one-line call, and the spec dictates the shape, so this is a paper cut rather than a trap; it is recorded because it is the residue of F17 and because a destructuring implementation (`let Config { provider, .. } = config;`) would hit it for real. No remedy required this round; if one is wanted, accept `\.provider` with a preceding `config` on either of the two adjacent lines, or drop the check and rely on the executed test.

### Verdicts on every earlier finding

- **F1–F9 (r1)** — remain closed; nothing in revision 4 disturbed them. The `:1171` doc-comment trap is still flagged in the spec and it is still the thing that will fail a correct first attempt.
- **F10 (r2, blocking) — closed.** The cheat it named (field declared, never read, `config.provider` only in a comment) fails: block 2's comment stripper refuses the comment-only read, and the executed test refuses the literal parse. Confirmed against `cheatA`, which is strictly stronger.
- **F11 (r2, non-blocking) — NOT closed; reopened as F20, now blocking.** Round 3 half-closed it by matching bodies; round 4 removed the matcher and moved the behaviour into an executed test whose body is again unpinned. The "named but not meant" shape survives.
- **F12, F13, F14 (r2) — closed**, verified unchanged from round 3's verdict.
- **F15 (r3, blocking) — closed.** I rebuilt it myself (`cheatA`) and block 4 exits 1. The failure is the new test's own `expect_err`, not a side effect: run alone, `cargo test an_unknown_provider_fails_the_voice_call_before_any_dial` FAILS in `cheatA` (`panicked … an unknown provider is refused: Object {"conversation": …}` — `voice` returned `Ok`), and passes in `honest`.
- **F16 (r3, blocking) — closed.** The defect was `text.find('fn open')` capturing a decoy; that python no longer exists anywhere in the spec, so there is no substring to capture. A decoy tree's runtime behaviour is `cheatA`'s — the real `open` parses a literal and dials — so block 4's executed test kills it on the same assertion. Closed by removal of the mechanism plus the `cheatA` result; I did not rebuild the decoy separately, and say so.
- **F17 (r3, non-blocking) — closed.** `honest3` is the realistic reshaping (`"gpt".to_string()`, `config.provider.as_str()`) and exits 0, 0, 0, 0. Nothing in block 2 pattern-matches an expression any more. The residual literal-substring edge is recorded as F21.
- **F18 (r3, non-blocking) — closed in its own terms.** The seam-test bodies are no longer any gate; step 4 says so in the spec, plainly. The defect class did not die, it migrated to step 5's test — that is F20, not F18.
- **F19 (r3, non-blocking) — closed.** Verified against `ea3c16e`: `#[serde(default)]` is `src/service.rs:20` and the spec now cites `:20`; `start_voice` closes at `:315` and the spec now cites `:264-315`. `wired()` at `:1280` also checks out.

### Ruling: is the new test independent, or does it only fail by polluting a shared fixture?

**Independent. The analyst's account is correct, and the direction of the pollution is the harmless one.** Each test calls `fixture()`, which binds its own `127.0.0.1:0` listener and owns its own `received` vector — nothing about the fixture is shared. What is shared is `crate::socket::TEST` (the mutex serialising the process env and the fake devices) and `OPENAI_API_KEY`. Decisive evidence, in `cheatA`:

- `cargo test an_unknown_provider_fails_the_voice_call_before_any_dial` **alone → FAILED**, on its own `expect_err`, with the whole rest of the binary filtered out.
- `cargo test voice_runs_a_session_on_the_wire` **alone → ok.**

So the new test fails on its own assertion with no other test in the run, and the wire test's collateral failure in the full run is caused *by* the new test's stray session, not the other way round. The gate is not an accident. It also does not cost the honest tree anything: `honest` has no stray session (nothing is dialled) and ran 21/21 three times with no flake.

### Ruling: is the spec honest about its ceiling?

**Mostly, and the improvement is real — but it overclaims in exactly one sentence, and that sentence is the one this round disproves.** *Where the gate actually lives* is the right instinct: it says block 2 is deliberately loose, says why a tighter matcher would false-red a correct tree (which F17/`honest3` bears out), and names what is not proved (the second transport's selectability). A spec that states its ceiling is worth more than one that overclaims, and three rounds of the opposite make this worth crediting. The one false line is "It cannot be written around by shaping the source": `cheatC` writes around it by shaping the source of the test itself. Whatever else round 5 does, that sentence must either become true or say "the body of that test is the backstop the reviewer reads".

Findings and concrete revisions: F20 (blocking) — add the four-token body check to block 2's existing python, as written above; F21 (non-blocking) — optional. Everything else from rounds 1–3 is closed.
Disposition: revise. One bounded edit to one python block and one sentence; no restructuring, no split. The spec's implementation steps are correct as written and should not be touched.
Validation: cwd = each scratch tree under `/private/tmp/claude-501/-Users-feb-dev-cartridge/546d3989-73ec-4315-89f3-a5bc45a8211e/scratchpad/reviewer-live-transport-r4/{clean,honest,honest2,honest3,cheatA,cheatC}`, each a `git -C live.ctg archive ea3c16e` copy; blocks run as `sh -eu -c "$(cat blockN.sh)"` with `CARGO_TARGET_DIR` per tree outside every repository; exit codes in the table above; `cargo test`/`cargo clippy --all-targets -- -D warnings` as reported. `git -C live.ctg status --porcelain` empty and `git -C live.ctg rev-parse HEAD` = `ea3c16ea888bef0c946842749d1e333e355440aa` after every step. No `prd` command run, nothing committed, no file in `live.ctg`, `prd.md` or `specs/` written.
Reviewer identity: independent reviewer agent, round 4 (did not write the plan, did not review rounds 1–3).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: **FAIL (89/100)**.
Unresolved blocking findings: F20 — block 4 pins the gating test's name and nothing pins its body, so `cheatC` (setting parsed and discarded, name kept, body swapped for a `Provider::parse` assertion) exits 0, 0, 0, 0 with 21 green tests and clean clippy.
Rounds used / remaining: 4 / 1.
Next action: one bounded revision closing F20, then round 5. **This is the last available round** — if round 5 fails, the allowance is exhausted and the PRD must go to `question`.

## Round 5 — 2026-09-17 — **final round**

Presented revision: `specs/spec01.md` revision 5, published in place, answering
F20 and F21. `live.ctg` at `ea3c16ea888bef0c946842749d1e333e355440aa`,
`git -C live.ctg status --porcelain` empty before and after this review.
`prd.md` unchanged since round 1. **This is round 5 of 5: the allowance is now
exhausted.**

| Input | Content digest |
| --- | --- |
| Plan | `prds/…/a-setting-chooses-the-transport-and-the-gpt-one-keeps-working/prd.md` — SHA-256 `7f177e0749c605370d04aec9231150596c29c52efc7bb67097ba9f25f47fdbeb` |
| Specs | `specs/spec01.md` — SHA-256 `b1ac74ccb0eba47f30baf312e4f97f3ca39aba5bc7a3e8987ce3635ad207e710` |
| Material contracts/dependencies | `live.ctg@ea3c16e` (`src/service.rs`, `src/socket.rs`, `src/lib.rs`, `cartridge.json`, `README.md`, `.cartridge/help.md`); `cartridge.ctg/src/transport/settings.rs` `Spec` (`deny_unknown_fields`, no `enum` key) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Unchanged from rounds 3–4 and still right: one observable outcome, one owner, the second transport explicitly deferred, *Remaining work* forbidding a provider list or a wider `Transport::open`. −1 stands only for `prd.md` Acceptance box 5 still carrying the planning-time census inline. |
| Ownership and reuse | 19 | Unchanged. `crate::socket::Result` reused, `socket::URL` unmoved, `Session` left in `socket`, no new crate dependency, the loopback fixture and `only_the_dummy_key` reused, `wired()`'s signature deliberately untouched so the three baseline callers stay unedited. |
| Dependencies and implementable slices | 19 | Verified again this round: two independently-shaped honest trees (`honest`, `honest3`) compile, run `21 passed; 0 failed`, are clippy-clean and exit 0 on all four blocks. Every step anchor still matches `ea3c16e`; the `:1171` doc-comment trap, `socket::pcm` keeping `use crate::socket;` alive and the four `.id` → `.id()` conversions are all called out in advance. |
| Observable acceptance and baseline evidence | 14 | Up 1 from round 4. Real gains: the round-4 cheat is dead (`cheatC` → block 2 exit 1), the false sentence "It cannot be written around by shaping the source" is withdrawn rather than patched, and *What none of this guarantees* is an accurate ceiling statement rather than an overclaim. Still deducted 6 because **the gate is beaten again**, by a one-step derivative of `cheatC` that block 2's own failure message dictates — see F22. |
| Failure, recovery and compatibility | 19 | Unchanged and re-scanned. No statement-level `! grep` (the only `!` in any block is `if ! cargo test`, a real condition inside an `if`); no `grep 'a\|b'` alternation; no `test -n "$X" && test "$X" -ge N` shape; no `-ge`/`-gt` numeric guard of any kind; no `cd`; `trap … EXIT` on `$$`-suffixed `${TMPDIR}` scratch files; `CARGO_TARGET_DIR` defaulted away from `target/debug` in the one cargo block; manifest re-trust cost and the pass-2 hot-restart hazard both stated. |
| Reviewer total | **90 / 100** | At the threshold on points; **FAIL** — one blocking finding is unresolved. |

### The seven trees, all mine, every block run as `sh -eu -c "$(cat blockN.sh)"`

Blocks extracted verbatim by fence from revision 5's `## Verify and Proof` (four
`sh` fences). `clean` is a fresh `git -C live.ctg archive ea3c16e | tar -x`.
`honest`, `honest3`, `cheatA` and `cheatC` are round 4's trees, copied into this
round's scratch, their `target/` removed, and each one diffed against `clean`
before use: `honest` touches exactly the seven footprint paths and nothing else,
`cheatA` differs from `honest` by two lines of `src/transport.rs`, `cheatC`
differs from `cheatA` by the gating test's body alone. `cheatD` and `cheatE` are
mine. cwd = each tree's root; `CARGO_TARGET_DIR` per tree under
`…/scratchpad/reviewer-live-transport-r5/target-*`, outside every repository.

| Tree | b1 | b2 | b3 | b4 | `cargo test` | note |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `clean` — `ea3c16e` untouched | **1** | **1** | **1** | **1** | 18 passed | b1 "declares no `provider` setting"; b4 walks the list then `missing test: service::tests::an_unknown_provider_fails_the_voice_call_before_any_dial` |
| `honest` — every step applied verbatim | 0 | 0 | 0 | 0 | 21 passed | clippy clean |
| `honest3` — F17 probe (`"gpt".to_string()`, `config.provider.as_str()`) | 0 | 0 | 0 | 0 | 21 passed | no false red |
| `cheatA` — F15: `let _ = Provider::parse(&config.provider);` then `match Provider::Gpt` | 0 | 0 | 0 | **1** | 19 passed, 2 failed | dies on the executed test's own `expect_err` (`panicked at src/service.rs:1415`) |
| `cheatC` — F20: `cheatA` + gating test body swapped for `Provider::parse` | 0 | **1** | 0 | 0 | 21 passed | b2 names the two missing tokens: `provider: "local"` and `fixture.received` |
| **`cheatD` (mine)** — `cheatC` + one harmless extra test carrying those two tokens | **0** | **0** | **0** | **0** | 22 passed | **F22**: green collect, `provider: "local"` still dials |
| **`cheatE` (mine)** — `cheatA` + a natural gating-test body that never calls `voice` | **0** | **0** | **0** | **0** | 21 passed | **F22**: green collect, clippy clean, `provider: "local"` still dials |

The analyst's reported table is reproduced exactly: clean 1,1,1,1; the honest
trees 0,0,0,0; the F15 cheat killed at block 4; the round-4 cheat killed at
block 2. Its claim that the two cheats die in *different* blocks, so neither
layer is carrying the gate alone, is correct and is the round's real advance.

### Ruling on task 2 — can the four-substring condition be beaten?

**Yes, and cheaply. This is F20's fifth costume.** The condition is weaker than
it looks for one measurable reason: two of the four tokens are already present
in the untouched baseline. Counted on `ea3c16e`'s comment-stripped
`src/service.rs`: `.voice(` **6 occurrences**, `expect_err` **1**,
`provider: "local"` 0, `fixture.received` 0. Block 2 greps the whole file, not
the test, so it is in practice a *two*-token condition, and neither token has to
appear inside the named test.

`cheatE` is the natural form. `Transport::open` is `cheatA`'s — the setting is
parsed, discarded, and GPT is dialled whatever `provider` says (`src/transport.rs`
byte-identical to `cheatA`'s, and round 4 proved that tree dials; `cheatA`'s own
block-4 failure above is the same proof). The gating test keeps its name and
reads:

```rust
async fn an_unknown_provider_fails_the_voice_call_before_any_dial() {
    let fixture = fixture().await;
    let config = Config { provider: "local".into(), ..Config::default() };
    let refused = crate::transport::Provider::parse(&config.provider)
        .expect_err("an unknown provider is refused");
    assert!(refused.contains("provider") && refused.contains("gpt"), "…: {refused}");
    let dialled = fixture.received.lock().expect("received").clone();
    assert!(dialled.is_empty(), "nothing reached the endpoint: {dialled:?}");
}
```

It configures the unknown provider, demands a refusal, and checks the fixture is
quiet — and it never calls `voice`, so the "quiet fixture" assertion is
vacuously true and nothing observes `Transport::open` at all. Blocks 1–4 exit
**0, 0, 0, 0**, `cargo test` reports 21 passed, clippy is clean, and in that
tree `provider: "local"` dials GPT Live. PRD Acceptance box 4 is delivered by
nothing.

The aggravating property is that **block 2's failure message is the recipe.**
Run block 2 on `cheatC` and it prints exactly `'provider: "local"' appears in no
code line` and `'fixture.received' appears in no code line`. Pasting those two
strings anywhere in the file — into the cheap test, as in `cheatE`, or into an
unrelated one, as in `cheatD` — turns 1 into 0. The distance from the round-4
cheat to the round-5 cheat is one error message.

### Finding

- **F22 (blocking, new; F11/F20 in its fifth costume) — the four required
  substrings are a file-level condition, two of them already satisfied by the
  untouched baseline, so a test that never calls `voice` passes them.**
  Evidence: the token census above; `cheatD` and `cheatE` at 0,0,0,0 with 21–22
  green tests and clean clippy while `provider: "local"` dials. Scope note: this
  is the same defect class that failed rounds 2, 3 and 4 — the gate names a
  test and does not bound what that test does.

  **Remedy, verified here, and it is the one round 4 pre-authorised** ("tighten
  it to a sliced test region only if a cheaper form proves insufficient" — it
  has). Keep block 2 exactly as it is, but slice before testing the four tokens:
  take `src/service.rs`'s stripped text from `fn
  an_unknown_provider_fails_the_voice_call_before_any_dial` to the next
  attribute at test indentation (`\n\t#[`), and require the four tokens inside
  that slice rather than in the file. Measured across every tree in this round:

  | tree | slice | tokens missing from the slice |
  | --- | ---: | --- |
  | `honest` | 1098 b | none |
  | `honest3` | 1098 b | none |
  | `cheatC` | 217 b | `provider: "local"`, `.voice(`, `fixture.received` |
  | `cheatD` | 219 b | `provider: "local"`, `.voice(`, `fixture.received` |
  | `cheatE` | 591 b | `.voice(` |

  Both honest trees pass; all three cheats die. `cheatA` passes the slice check
  and is killed by block 4's executed test, so slice + executed test between
  them cover every cheat built in five rounds. This is four lines of python
  inside the block that already exists, no new mechanism, and it does not
  false-red either honest shape. It remains a text check and does not close the
  ceiling in F23; it closes the cheats that have actually been built.

- **F23 (non-blocking, and correctly stated by the spec itself) — no text check
  can prove a test means what its name says.** The spec's *What none of this
  guarantees* says exactly this, and it is accurate. Worth recording that the
  analyst's proposed closure — a mutation check that flips the provider and
  requires `cargo test` to go red — **cannot be written the obvious way**: the
  mutation edits `src/service.rs` or `src/transport.rs`, both inside the
  footprint, and the engine aborts pass 2 with "source footprint changed during
  integrated verification". It would have to `cp -R` the tree to `${TMPDIR}`,
  mutate there and build twice. That is a real mechanism with a real false-red
  surface, and declining to introduce it untested in the final round was the
  right call (see the ruling below).

### Ruling on task 3 — the analyst's stated ceiling

**Right call, and the ceiling is accurate, not merely present.** Three separate
judgements, all of which I endorse:

1. *Withdrawing the sentence instead of patching it.* "It cannot be written
   around by shaping the source" is gone from the spec (`grep` confirms zero
   occurrences), and nothing weaker was slipped in to replace it. Round 4 asked
   for that sentence to "become true or say the reviewer is the backstop"; the
   spec chose the second and said it plainly.
2. *The replacement is correct.* "Four substrings can all be present in a test
   that still asserts nothing useful — they are composable only inside something
   that looks like the real test, not only inside the real test" is a precise,
   in-advance description of `cheatD` and `cheatE`. I built both before reading
   that paragraph closely, and it predicts them. A spec that names the hole a
   reviewer then finds is doing its job; three rounds of this PRD did the
   opposite.
3. *Not adding the mutation check.* Correct, and more so than the analyst knew —
   see F23: the obvious implementation is forbidden by the engine, and the legal
   one needs a tree copy and a second build. Shipping that untested in round 5
   risks F17 all over again, which is the other kind of blocker.

One residual inaccuracy, non-blocking: step 5's sentence says a test asserting
on `Provider::parse("local")` "carries none of them". `cheatE` is that test and
carries three of the four directly, with the fourth free from the baseline. The
*ceiling* paragraph is right; this *step* sentence is not, and it is the sentence
an implementer reads.

### Verdicts on every earlier finding

- **F1 (r1, blocking) — closed.** `clean` and any tree without `Config.provider`
  die in block 2 on `pub provider: String`. Re-run: `clean` b2 exit 1.
- **F2 (r1, blocking) — closed.** Block 4 greps 21 names out of `cargo test --
  --list`; on `clean` it walks the eighteen baseline names and then fails on
  `missing test: service::tests::an_unknown_provider_fails_…`. Deleting the wire
  test fails by name.
- **F3 (r1) — closed.** Named greps, no `^transport::tests::` prefix anywhere.
- **F4 (r1) — closed.** Block 3 requires `` `provider` `` and `` `provider`.*`gpt` `` on
  one line in both pages; `clean` b3 exit 1, `honest` b3 exit 0.
- **F5 (r1) — closed.** The re-trust / `cartridge reload live` / pass-2 paragraph
  is in *Base and dependencies*.
- **F6 (r1) — closed.** `cargo clippy --all-targets -- -D warnings` is the last
  line of block 4 and ran in every tree above.
- **F7 (r1) — closed.** `${TMPDIR:-/tmp}/live-transport-verify-$$.{out,list}`
  with `trap … EXIT`; no leftovers after the failing runs.
- **F8 (r1) — closed.** Literal error message; the spec forbids a `PROVIDERS`
  list until the second transport.
- **F9 (r1) — closed.** `:268-281` / `:264-315` both correct against `ea3c16e`.
- **F10 (r2, blocking) — closed.** The comment-stripped read defeats the
  comment-only `config.provider`; `cheatA`, strictly stronger, dies at block 4.
- **F11 (r2) — NOT closed. Fifth costume, now F22.** Round 3 matched bodies,
  round 4 removed the matcher, round 5 constrained the file instead of the body.
  The "named but not meant" shape survives each time.
- **F12, F13, F14 (r2) — closed**, re-verified.
- **F15 (r3, blocking) — closed.** `cheatA` b4 exit 1, failing on the gating
  test's own `expect_err` at `src/service.rs:1415` (`voice` returned `Ok`).
- **F16 (r3, blocking) — closed.** The `text.find('fn open')` machinery no longer
  exists; there is no substring to capture, and such a tree's runtime behaviour
  is `cheatA`'s, which block 4 kills.
- **F17 (r3) — closed.** `honest3` (`"gpt".to_string()`, `config.provider.as_str()`)
  exits 0,0,0,0 with 21 green.
- **F18 (r3) — closed in its own terms.** The seam-test bodies gate nothing and
  the spec says so.
- **F19 (r3) — closed.** Checked against `ea3c16e`: `#[serde(default)]` is
  `src/service.rs:20` and `start_voice` closes at `:315`; the spec cites both.
- **F20 (r4, blocking) — closed as written, not in substance.** `cheatC` exits 1
  from block 2 naming its two missing tokens. The class it named is alive as F22,
  one error message away.
- **F21 (r4) — closed.** `re.search(r'config\s*\.\s*provider', transport)` matches
  the hand-wrapped `&config\n.provider` form. The destructuring form
  (`let Config { provider, .. } = config;`) still reds; the spec dictates the
  one-line shape, so this stays a paper cut.

Findings and concrete revisions: F22 (blocking) — slice block 2's four-token test
to the gating test's own region, as measured above; F23 (non-blocking) — record
that the mutation check must copy the tree, because the footprint is
write-protected during verification; and one sentence in step 5 to correct.
Disposition: keep the plan and the implementation steps — they are correct,
executable and twice built green. Revise block 2 by the four-line slice. The
five-round allowance is spent, so this needs a user decision, not another
automatic revision.
Validation: cwd = each tree under
`/private/tmp/claude-501/-Users-feb-dev-cartridge/546d3989-73ec-4315-89f3-a5bc45a8211e/scratchpad/reviewer-live-transport-r5/trees/{clean,honest,honest3,cheatA,cheatC,cheatD,cheatE}`;
blocks run as `sh -eu -c "$(cat blockN.sh)"`; `CARGO_TARGET_DIR` per tree outside
every repository; exit codes in the table above. Inert-guard scan: no
statement-level `! grep`, no `grep 'a\|b'` alternation, no
`test -n "$X" && test "$X" -ge N` shape, no numeric `-ge`/`-gt` guard at all.
`git -C /Users/feb/dev/cartridge/live.ctg status --porcelain` empty and
`rev-parse HEAD` = `ea3c16ea888bef0c946842749d1e333e355440aa` after every
experiment. No file in `live.ctg`, no spec and no `prd.md` written; only this
`review.md` and the loop's `reviewer-5.md`. No `prd` command run, nothing
committed.
Reviewer identity: independent reviewer agent, round 5 (did not write the plan,
did not review rounds 1–4).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: **FAIL (90/100 on points, one unresolved blocking finding). Round 5 of 5
— the allowance is exhausted.**
Unresolved blocking findings: F22 — block 2's four required substrings are
tested against the whole of `src/service.rs`, where `.voice(` and `expect_err`
already occur 6 and 1 times at `ea3c16e`, so a gating test that never calls
`voice` satisfies them; `cheatD` and `cheatE` exit 0,0,0,0 with green tests and
clean clippy while `provider: "local"` still dials GPT.
Rounds used / remaining: 5 / 0.
Next action: **stop automatic revisions.** Move the PRD to `question` and put the
F22 remedy in front of the user: it is a four-line slice inside the block that
already exists, verified here to kill `cheatC`, `cheatD` and `cheatE` while both
honest trees stay green. If the user grants a further allowance, that one edit is
the whole of it — the plan, the steps and the other three blocks should not be
touched.

## Gate round (not counted) — 2026-09-19 — sliced token test, per the Decision of 2026-09-17

Presented revision: spec01 revision 6 (analyst round 6), `prd.ctg` HEAD `0a9c0e83`
with the PRD's planning files uncommitted; code base `live.ctg` `ea3c16ea888bef0c946842749d1e333e355440aa`, clean.
Counting: this round only redesigns the gate, which the coordinator's Decision
authorised under `review-plan.md` step 4. It is not a substantive revision and is
not counted.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `4d52957df07754e4ea857f31bb379711967f8372be71e5b88ba8a3dadde0ae47` |
| Specs | `specs/spec01.md` (rev 6) SHA-256 `574e5c4a27719aead55842977efccca080b1b3a3f67210aade297ce5fc3e9373`; extracted blocks b1 `1073f4fd…`, b2 `4d77827c…`, b3 `d728ead5…`, b4 `b82ab3f4…` |
| Material contracts/dependencies | `live.ctg` `ea3c16e`; `cartridge.ctg/src/transport/settings.rs` `Spec` (unchanged since round 5); `review-plan.md` step 4 ceiling rule |

Method: eight `git clone --local` copies of `live.ctg` under
`scratchpad/reviewer-transport-6/trees/`. `honest`, `cheatA`, `cheatC`, `cheatD`,
`cheatE` take their footprint files from the analyst's trees after I read each
diff against the base (each is what analyst-6 says it is). `cheatF` and `cheatG`
are new, built here. The four `sh` blocks were extracted by script from
spec01 and run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "$(cat blockN.sh)"`
with cwd = each tree's root and the block's own per-tree `CARGO_TARGET_DIR` default.

| Tree | b1 | b2 | b3 | b4 | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `clean` (base) | 1 | 1 | 1 | 1 | b4: 18 tests listed, then `missing test: …an_unknown_provider_fails…`; b2 exits 1 on `test -f src/transport.rs` with no message |
| `honest` | 0 | 0 | 0 | 0 | `21 passed; 0 failed`, clippy clean |
| `cheatA` (parse discarded, always dials) | 0 | 0 | 0 | **1** | gating test panics at `src/service.rs:1412`: `voice` returned `Ok` |
| `cheatC` (round-4 body swap) | 0 | **1** | 0 | 0 | "does not satisfy the required condition" |
| `cheatD` (round-5 decoy test elsewhere) | 0 | **1** | 0 | 0 | same message |
| `cheatE` (round-5 live defect, never calls `.voice(`) | 0 | **1** | 0 | 0 | same message; the case that beat revision 5 is now dead |
| `cheatF` (new: cheatA's transport; gating body is `Provider::parse("local")` plus a raw-string literal carrying the four tokens) | 0 | 0 | 0 | 0 | **the slice is beaten**: 21 green, clippy clean, `provider: "local"` still dials GPT |
| `cheatG` (new: honest body, `voice` on a nonexistent conversation, message assertion loosened) | 0 | 0 | 0 | **1** | killed at runtime: `voice` auto-creates the conversation and dials, so `expect_err` panics |

Longest block: b4, 5–9 s per tree with a warm `kache`; nothing near 120 s.

### Findings

- **F24 (non-blocking; the recorded ceiling) — the sliced gate falls to a string literal.**
  Block 2 strips comments but not string literals, so
  `let _shape = r#"provider: "local" .voice( expect_err fixture.received"#;`
  inside the gating test satisfies the slice, and a body that only tests
  `Provider::parse` passes block 4. That is `cheatF`, 0/0/0/0. It is deliberate,
  not an accident: a raw string holding exactly the gate's tokens does not look
  like a natural mistake. The likely accidental failures (the round-4 body swap
  `cheatC`, the round-5 test that never calls `voice` `cheatE`, discarding the
  parse `cheatA`, a mistaken conversation id `cheatG`) all die. Per the Decision
  and step 4, this is the ceiling. Stripping string literals as well would
  close `cheatF`, but the next costume (a dead helper closure, a `#[cfg(any())]`
  item in the body) is equally cheap, so nothing more should be spent on the
  gate. **The backstop is the diff reading:** at collect, a reviewer reads the
  body of `an_unknown_provider_fails_the_voice_call_before_any_dial` and
  `Transport::open`, and checks that the test calls `voice` on the conversation
  it just opened, and that `open` returns from `Provider::parse(&config.provider)?`.
- **F25 (non-blocking) — the ceiling paragraph is accurate and does not overclaim.**
  It says the slice "closes that specific bypass" (true: `cheatE` dies). It also
  says four substrings can "in principle all sit inside a body that satisfies
  the slice without the test proving anything useful" (`cheatF` is exactly that).
  And it names "the named executed test plus a reviewer reading the diff" as the
  backstop. The spec does not say that any text check closes the gap. The round-5
  step-5 inaccuracy ("carries none of them") is gone (0 occurrences), and
  block 2's failure message no longer lists the missing tokens.
- **F26 (non-blocking, cosmetic).** *Reusable attempt artifacts* still says the
  round-3 honest tree reported `20 passed`. The current reference shape reports
  21. On the base, block 2 fails silently, because `test -f` exits under `-e`
  before any message is printed. Neither changes a verdict.

All earlier findings (F1–F23) stay as ruled in round 5. F22 is closed by the
slice (`cheatC`/`cheatD`/`cheatE` b2 = 1; both honest shapes stay green).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One seam, the default is unchanged, and the second transport is explicitly deferred. −1: the value to users only arrives with the next child. |
| Ownership and reuse | 19 | One cartridge and footprint; reuses `socket::Result`, the existing fixture and the `TEST` lock; no new dependency. −1: the manifest re-trust cost falls on the live daemon. |
| Dependencies and implementable slices | 19 | Steps are line-cited against `ea3c16e` and were built green twice, here and by the analyst. −1: step 7's closure is elided (`…`), though the reference tree shows it. |
| Observable acceptance and baseline evidence | 17 | Base fails all four blocks; honest passes all four; 21 names are pinned and clippy runs. −2: the gate ceiling (`cheatF`), which per step 4 is not blocking, with the diff reading named. −1: F26. |
| Failure, recovery and compatibility | 18 | The wire test is pinned by name, an unknown provider is refused before the credential is fetched, and the re-trust/reload window is documented. −2: no rollback note for a manifest that is untrusted mid-collect beyond "re-trust". |
| Reviewer total | **92 / 100** | |

Disposition: keep. Implement spec01 revision 6 as written.
Validation: the table above. The runner is
`env -i PATH="$PATH" HOME="$HOME" sh -eu -c "$(cat blockN.sh)"`, cwd = each
`trees/<name>` root, one run per tree and block. `git -C /Users/feb/dev/cartridge/live.ctg status --porcelain`
was empty and `rev-parse HEAD` was `ea3c16e` afterwards. Nothing was written in
`live.ctg`. No `prd` command was run and nothing was committed. Only this section
was appended.
Reviewer identity: reviewer-transport-6 (independent review sub-agent, Opus 5).
It did not write the plan and did not review rounds 1–5.
User rating: not required under delegation; none supplied.
User feedback/provenance: the coordinator's Decision of 2026-09-17 in `prd.md`, which authorises this gate-only round.
Result: **PASS, 92/100.** The gate ceiling is recorded (F24) and is not blocking under step 4.
Unresolved blocking findings: none.
Rounds used / remaining: 5 / 0 counted. This gate round is not counted.
Next action: proceed to implementation of spec01 revision 6. At collect, the
reviewer reads the gating test body and `Transport::open` as the backstop named
in F24. Do not spend further rounds on the gate.
