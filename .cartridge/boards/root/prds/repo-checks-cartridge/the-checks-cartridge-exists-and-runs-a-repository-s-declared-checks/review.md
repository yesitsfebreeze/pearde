# @root/repo-checks-cartridge/the-checks-cartridge-exists-and-runs-a-repository-s-declared-checks review history

Plan: `@root/repo-checks-cartridge/the-checks-cartridge-exists-and-runs-a-repository-s-declared-checks`,
`prd.ctg/.cartridge/boards/root/prds/repo-checks-cartridge/the-checks-cartridge-exists-and-runs-a-repository-s-declared-checks/prd.md`.
Scope: leaf. One observable outcome — `checks.ctg` exists as a cartridge in its own
right and runs a repository's declared checks. Footprint is the single directory
`checks.ctg`, which does not exist yet.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none. The parent `@root/repo-checks-cartridge` was refined into this
child and `the-checks-cartridge-is-registered-in-the-composition` on 2026-09-19; no
round had been scored against the parent.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-19

Presented revision: repository HEAD `801aa8eb460cc024d50211a53a2e69c0ffc529cb`, working
tree dirty (four other live sessions; none of the dirty paths are inputs to this
assessment). The spec is an untracked draft.

| Input | Content digest |
| --- | --- |
| Plan | `…/the-checks-cartridge-exists-and-runs-a-repository-s-declared-checks/prd.md` — `09a82b6c009bf2cc1fb3c9073c3fe62bc69dea701f20e5ea8f45256b85d4ec73` |
| Specs | `…/specs/spec01.md` — `07ab500fe127c7e3845c123c0e4732ebe0e678eb09bd3ef050ae767ab3c6b28c` |
| Parent index | `…/repo-checks-cartridge/prd.md` — `ef8664c8275fd40e097bbf2744f30a7855ae167cb9108f3f02b67814330ac67d` |
| Material contracts/dependencies | `cartridge.ctg/src/node/mod.rs:205-360` (the Lua `cartridge` global); `harness.ctg/src/bridge.rs:60-130` (`Ctx::call`); `.cartridge/memos/routine/check-cartridge-isolation.md`; `.cartridge/memos/routine/audit-cartridges.md`; `tools.ctg/cartridge.json` — `84e3eb5080bbf92aa7006ac574f71b98b27aa6a01b921e9d08a59e19bd457169`; `prd.ctg/.cartridge/templates/spec.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The outcome is one capability in one new directory and genuinely lands while the superproject's own files are held by the sibling child; the spec opens by saying exactly that and by naming what `just test checks` cannot do yet. −4: the "What the composition requires of any cartridge" census, presented as established by reading, is wrong in three places (F6), and it is the sole stated basis for the language decision. |
| Ownership and reuse | 9 | Footprint is `checks.ctg` exactly. The cartridge shape reproduces `tools.ctg` accurately — verified against `tools.ctg/Cargo.toml`, `build.rs`, `init.lua`, `cartridge.json` and the `#[path = "../.cartridge/tests/unit/service/tests.rs"]` attachment: `cdylib`, `mlua` 0.12 `["lua54","module","serde"]`, own `[workspace]`, `warnings = "deny"`, the macOS `-undefined dynamic_lookup` pair, `commands` delegating to `../cartridge.ctg/justfile`, README + `.cartridge/help.md`. −11: the record mechanism ignores the established one and names an API the host does not expose (F1). |
| Dependencies and implementable slices | 10 | Thirteen ordered steps, each concrete; the spec01/spec02 boundary is drawn in the right place and stated where an implementer will read it. −10: step 7's `post` op contradicts step 4's dispatch rule (F2), and step 1's dependency list omits everything reaching `memo` actually costs. |
| Observable acceptance and baseline evidence | 9 | Right instinct throughout: behaviour is pinned by a `test` block naming six tests, not by a text or count census, and the spec says so explicitly. Both `sh` blocks were executed by the reviewer and both behave: the `bun` manifest gate exits 1 on a missing `needs`, and the isolation grep exits 1 on a planted `../memo.ctg/evidence` line and 0 on a clean tree — it reads the cartridge's files, not the spec's own text. −11: two of the six pinned tests are defeatable, one trivially (F3, F4); the record module has no test at all (F5); the manifest gate accepts an empty schema (F8). |
| Failure, recovery and compatibility | 14 | Recovery is honest and trivial — the whole footprint is one directory that does not exist. Every engine fact in `templates/spec.md` is respected and was checked by execution: `sh -eu -c` clean, no `${VAR:?}`, no `$TMPDIR`, no `cd` to an absolute checkout, all paths repo-relative, guards written `if grep …; then exit 1; fi` rather than `!` or `a && b`, `CARGO_TARGET_DIR` exported in the template's own form, scratch at `target/checks-verify` which is outside the footprint and covered by the repo-root `/target/` ignore. −6: the "Cold build ceiling" section rests on a false premise and escalates a risk that does not exist (F7); the isolation grep passes vacuously on a missing directory and covers fewer file types than `just isolation` (F9). |
| Reviewer total | 58 / 100 | Below 90. FAIL. |

Findings and concrete revisions.

- **F1 — blocking. `cartridge.call` does not exist.** `specs/spec01.md:118-121` and
  `:170-172` build the PRD's first named deliberate divergence on
  `cartridge.call("memo", …)` called from `init.lua`. The Lua `cartridge` global is
  assembled at `cartridge.ctg/src/node/mod.rs:205-360` and exposes `name`, `config`,
  `root`, `array_metatable`, `trace`, `needs`, `events`, `listen`, `on_dispose`,
  `emit`, `notify`, `bail`, `gather`, `publish`, `subscribe`, `host`, `load`, `pipe`,
  `spawn`. There is no `call`. `grep -rn 'cartridge\.call' --include='*.lua'` over the
  whole composition returns nothing. The request-reply verb is `cartridge.bail(name,
  data)`; the established route for a Rust cartridge is a local `bridge.rs` whose
  `Ctx::call` submits an `Ask` that the base pumps back out as `cartridge.bail`
  (`harness.ctg/src/bridge.rs:105`), used by `harness`, `proxy` and `agent`, each of
  which declares `needs: ["memo"]` and passes `just isolation` today. The spec's stated
  reason for avoiding that route is also wrong: `memo.ctg/cartridge.json` declares no
  `provide` keys at all, so the isolation key check (`.cartridge/memos/routine/check-cartridge-isolation.md`)
  cannot fire on `"memo"` from Rust or from Lua. Recommendation: adopt the
  `bridge.rs`/`Ctx` pattern, or state the Lua route in terms of `cartridge.bail` and
  say how the answer returns into the op — and revise step 1's dependencies, which the
  bridge pattern changes.
- **F2 — blocking. The `post` op cannot do what step 7 says.** `specs/spec01.md:154-157`
  has `post` "load the recorded set (falling back to a fresh `discover` when none is
  recorded)", while `:118-120` requires that `record`/`recorded` "return the request
  shape and take the answer back, so the crate itself performs no dispatch". A single
  synchronous `dispatch(request)` cannot round-trip to `memo` in the middle of an op,
  and the spec specifies no protocol for it. The lazy resolution — always take the
  `discover` fallback — leaves `record.rs` unreachable, and since step 8 declares
  `mod record;` private and step 1 sets `[lints.rust] warnings = "deny"`, an
  unreferenced `pub fn record` is `dead_code` and the crate will not compile. Name the
  shape: either `init.lua` pre-fetches the recorded set and passes it into `post`, or
  Rust reaches `memo` through the bridge.
- **F3 — blocking. `discovery_and_selection_spawn_no_process` is vacuous as
  specified.** `specs/spec01.md:228-230` and `:314`. A test cannot observe "no child
  process was created" from inside its own process, and the spec's actual argument
  (`:198-203`) is structural — `discover` and `select` contain no
  `std::process::Command`. The pinned name therefore buys nothing: a body of
  `let _ = discover(&fixture); let _ = select(…);` with no assertion passes. The
  reviewer wrote exactly that body in a stand-in crate and cargo reported it `ok`.
  This is the only executed gate for PRD Acceptance 6's offline half. Replace it with a
  property a test can actually fail on — e.g. `discover` and `select` taking a sealed
  filesystem view, or a `#[test]` that reads the two source files and fails on
  `Command`, which at least fails when the property breaks.
- **F4 — blocking. `the_full_gate_is_never_selected_by_the_post_pass` pins the wrong
  property.** `specs/spec01.md:225-227` and `:313`. "Runs strictly fewer checks than
  `gate`" is satisfied by a `post` that runs every check but one, which is the opposite
  of the claim. Worse, `post` sets `stop_on_fail` true (`:157`), so a fixture with any
  failing check makes `post` run fewer for a reason unrelated to selection. Pin the
  claim the PRD makes: `post` over a change confined to one scope selects that scope's
  checks and the declared verify and nothing else, by name, with another scope's checks
  present and absent from the selection.
- **F5 — blocking. The record divergence ships with no executed proof.**
  `specs/spec01.md:115-126` adds `record.rs`, a `checks` memo kind and a `needs`
  declaration; the `test` block at `:307-315` pins nothing about any of it. One of the
  two divergences the PRD says "stand" is gated only by the manifest grep for the
  string `memo` in `needs`. Either pin a round-trip test for `record`/`recorded`, or
  move the record to spec02 and say here that this child ships discovery, selection and
  running only.
- **F6 — non-blocking. The cartridge census is wrong.** `specs/spec01.md:44-47`:
  "Fifteen of the seventeen cartridges are Rust cdylib mlua modules; only `auth.ctg`
  and `prd.ctg` are bun, and both are external CLI clients rather than event services."
  Measured: eighteen directories carry a `cartridge.json` (`cartridge.ctg` carries
  none — it is the host); fourteen carry a `Cargo.toml`; three are bun — `auth`, `prd`
  and **`web.ctg`**, which the count omits; and **`policy.ctg`** is neither, a
  122-line pure-Lua cartridge declaring the events `policy` and `policy.explain` —
  an event service that is not Rust, which is a direct counterexample to the sentence
  that carries the whole argument. The conclusion survives on its own merits
  (`checks.ctg` walks filesystems, spawns processes and enforces timeouts), but the
  stated basis must be corrected or replaced by that reasoning.
- **F7 — non-blocking, and it retires the analyst's headline risk. The "Cold build
  ceiling" is a false premise; measured 7.46 s.** `specs/spec01.md:248-259` and
  `analyst-1.md:98-115` treat a cold `mlua` build against the 120 s block ceiling as the
  one unmeasured risk, describing the dependency set as "`mlua` with the vendored Lua
  5.4". The feature set is `["lua54","module","serde"]` with no `vendored` feature; with
  `module` plus the macOS `-undefined dynamic_lookup` pair no Lua is built at all. The
  reviewer built a stand-in crate outside the repository with the spec's exact
  dependency set and its exact test attachment, and ran the spec's own gate shape
  (`cargo test --manifest-path … --lib`) against an empty `CARGO_TARGET_DIR`:
  **7.46 s wall clock**, exit 0, three tests reported `ok`. Delete the twelve-line
  hedge and the instruction to escalate.
- **F8 — non-blocking. The manifest gate does not enforce a real schema.**
  `specs/spec01.md:283-285` tests `ev.schema === undefined`, so `"schema": {}` passes,
  while `:178-180` asks for a schema that "enumerates the four ops and their fields".
  Demonstrated: a stand-in manifest with `"schema": {}` on both events printed
  "manifest declares its surface" and exited 0. This matches what `just audit` itself
  requires, so it is not a regression — but the spec should stop claiming the gate
  proves more than it does, or assert on the `checks` event's `op` enum specifically.
- **F9 — non-blocking. The isolation grep's edges.** `specs/spec01.md:296-301` exits 0
  when `checks.ctg` is absent (`grep` exits 2, the `if` reads it as false) — demonstrated;
  block 1's `test -d` covers this only while it runs first. Its `--include` set is
  `*.rs *.lua *.toml *.json *.md`, narrower than `just isolation`'s
  `rs|lua|ts|tsx|toml|json|sh|nu|justfile`, and `grep` does not report a symlink target,
  which the isolation memo names as a case. Add `--include='*.sh' --include='justfile'`
  and a `find checks.ctg -type l` guard, or say plainly that `just isolation` in spec02
  is the real gate and this is a fast pre-check.
- **F10 — non-blocking. "No upstream file is copied" has no gate.**
  `prd.md:47-49` and `specs/spec01.md:52-53` make this a named property; nothing in the
  Verify section tests it, and the isolation grep only looks for `../<sibling>.ctg`.
  The upstream is real and matches the claimed size —
  `/Users/feb/dev/pi/packages/coding-agent/src/core/rigor/index.ts`, one file, 542
  lines, verified. Since the port crosses TypeScript to Rust, literal copying is
  implausible and a gate would be theatre; name the diff reading as the backstop in the
  spec instead of leaving the property bare.

The two pinned tests the reviewer trusts least, and how a lazy implementation passes
them anyway: `discovery_and_selection_spawn_no_process` — an empty body with no
assertion (executed, passes; F3); and `the_full_gate_is_never_selected_by_the_post_pass`
— a `post` that runs every check except the last, or any fixture where `stop_on_fail`
truncates the run, both of which satisfy "strictly fewer" (F4).

Disposition: revise. The spec is well-built on the cartridge shape, the footprint, the
spec01/spec02 boundary and the Verify-block engine facts; the defects are concentrated
in the record mechanism (F1, F2, F5) and in two of six pinned tests (F3, F4). The
single largest correction is to reach `memo` the way the composition already reaches it.

Validation (actual commands, all run as `env -u CARTRIDGE_YOLO …`; cwd
`/Users/feb/dev/cartridge` unless noted):

- `just prompt` — the composed system prompt, read before anything else.
- `ls -d *.ctg`, then per directory a `Cargo.toml`/`package.json` probe — nineteen
  directories, eighteen with a `cartridge.json`, fourteen Rust, three bun, one pure
  Lua. `grep -c submodule .gitmodules` — 18. (F6)
- `for f in */cartridge.json; do jq -c '{needs,provide}' …` — `memo.ctg` declares no
  `provide`; `agent`, `harness`, `proxy` declare `needs: ["memo"]`. (F1)
- `grep -n 'global\.set' cartridge.ctg/src/node/mod.rs`, `sed -n '205,360p'` — the Lua
  API surface; no `call`. `grep -rn 'cartridge\.call' --include='*.lua' .` — no hits. (F1)
- `grep -rn '"memo"' --include='*.rs' harness.ctg/src proxy.ctg/src agent.ctg/src`,
  `sed -n '60,130p' harness.ctg/src/bridge.rs` — the real idiom. (F1)
- `sed -n '1,140p' .cartridge/memos/routine/check-cartridge-isolation.md` and
  `sed -n '1,90p' .cartridge/memos/routine/audit-cartridges.md` — what the two gates
  read; `cartridge.ctg` is excluded from `dirs` because it carries no `cartridge.json`,
  which is why the spec's alternation correctly omits it. (F9)
- Cold build, cwd `/tmp/rv78-timing/checks.ctg` (outside this repository; nothing was
  created under `/Users/feb/dev/cartridge`): a stand-in crate with the spec's exact
  `Cargo.toml` (`mlua` 0.12 `["lua54","module","serde"]`, `serde`, `serde_json`, no
  `tempfile`, own `[workspace]`, `warnings = "deny"`), the spec's `build.rs`, and the
  spec's `#[cfg(test)] #[path = "../.cartridge/tests/unit/service/tests.rs"] mod tests;`
  attachment carrying three of the six pinned names.
  `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=/tmp/rv78-timing/coldtarget /usr/bin/time -p
  cargo test --manifest-path /tmp/rv78-timing/checks.ctg/Cargo.toml --lib` against an
  empty target directory — exit 0, `Finished \`test\` profile … in 7.19s`,
  `real 7.46`, three tests `ok`. Warm crates.io registry, cold target directory, which
  is the collection-time condition. (F7). The same run also confirms `cargo test --lib`
  produces a test harness for a `crate-type = ["cdylib"]` crate, that the pinned names
  print as `service::tests::<name> … ok` and so match the template's last-`::`-segment
  rule, and that a no-assertion body passes (F3).
- Verify blocks, executed under `sh -eu -c` against a stand-in tree at `/tmp/rv78-vb`
  (again outside this repository): block 1 exits 0 on a complete stand-in and its `bun`
  gate prints "manifest declares its surface" — including with `"schema": {}` on both
  events (F8); block 2 exits 1 with the planted line
  `checks.ctg/src/bad.rs:1:path = "../memo.ctg/evidence"`, exits 0 once removed, and
  exits 0 when `checks.ctg` does not exist at all (F9).
- `wc -l /Users/feb/dev/pi/packages/coding-agent/src/core/rigor/index.ts` — 542, one
  file, as claimed. (F10)
- No `prd` operation was run, nothing was committed, no `git add`, and `checks.ctg` was
  not created. Only this file was written inside the repository.

Reviewer identity: reviewer agent, coordinator-78 session (independent of the analyst
and of the spec's author).
User rating: not supplied; none invented.
User feedback/provenance: none for this revision.
Result: **FAIL** — 58/100, below the 90 threshold, with five blocking findings.
Unresolved blocking findings: F1, F2, F3, F4, F5.
Rounds used / remaining: 1 / 4.
Next action: one coherent revision of `specs/spec01.md` addressing F1–F5 — reach `memo`
the way `harness`/`proxy`/`agent` reach it, resolve the `post` dispatch contradiction,
and repin the two defeatable tests and the record round-trip — then re-review at round 2.
F7's measurement is settled and needs no further work: delete the ceiling section.

## Round 2 — 2026-09-19

Presented revision: repository HEAD `c84b3a4126224af211de08f2e45fe06e705a5e99`, working
tree dirty (six other live sessions; none of the dirty paths are inputs here). The spec
is an untracked draft, replaced in full since round 1 (18465 → 29305 bytes).

| Input | Content digest |
| --- | --- |
| Plan | `…/prd.md` — `09a82b6c009bf2cc1fb3c9073c3fe62bc69dea701f20e5ea8f45256b85d4ec73` (unchanged from round 1) |
| Specs | `…/specs/spec01.md` — `eb96715d2d632b1c51cb6789eca3041a90201b895766af2ac5817b45628f25d1` |
| Material contracts/dependencies | `cartridge.ctg/src/node/mod.rs:204-278` (the Lua global; `bail` at :266-278); `harness.ctg/src/bridge.rs:35-51,85-133,248-301`; `memo.ctg/cartridge.json` (`events.memo` schema); `memo.ctg/src/service.rs:113-140` and `:470-528`; `memo.ctg/src/record.rs:932-935`; `live.ctg/src/service.rs:461`; `harness.ctg/src/lib.rs:283`; `tools.ctg/Cargo.toml`, `tools.ctg/build.rs`, `tools.ctg/src/service.rs:641`; `prd.ctg/.cartridge/templates/spec.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The language census is now exactly right — enumerated: 14 Rust, 3 bun (`auth`, `prd`, `web`), 1 pure Lua (`policy`, `init.lua` 122 lines), 18 with a `cartridge.json`. The two grounds given for Rust survive `policy.ctg`: the collect engine reads cargo/nextest/JUnit and `policy` ships no unit suite, and the work is walking, parsing and bounded subprocess capture. Scope split against the sibling child is correct and correctly placed. −2: the Acceptance section says "the PRD's six boxes" (there are seven) and claims a proof it does not have (B3). |
| Ownership and reuse | 18 | F1 is resolved and every cited line checks out: `bail` assembled at `cartridge.ctg/src/node/mod.rs:266-278` inside the global begun at :204; `harness.ctg/src/bridge.rs:105` is `pub fn call(&self, name, data)` = `Self::ask("bail", …)`, `ask_lua` at :126-133, `drive` at :257. `needs: ["memo"]` verified on `harness`, `proxy`, `agent`; `memo.ctg` declares no `provide` keys. The shape is live precedent: `live.ctg/src/service.rs:461` and `harness.ctg/src/lib.rs:283` both send `{"op":…,"cwd":…}` through `call("memo", …)`, and `memo.ctg/cartridge.json`'s `events.memo` schema declares exactly `{op, cwd}`. −2: N4 and N7 below. |
| Dependencies and implementable slices | 16 | The crate shape compiles as described — I built it (see Validation). −4: step 5 gives two incompatible signatures for the same two functions in one paragraph (async `record(ctx: &bridge::Ctx)` using `ctx.call`, versus a **synchronous** `trait Records { fn ask(&self, Value) -> Result<Value> }` that "both functions take"); the declared tokio features omit `macros`, so the async test 7 must hand-roll a runtime (N6); and `checks.ctg/Cargo.lock`, which the gate's own cargo invocation creates inside the footprint, is not among the files step 1 declares (N5). |
| Observable acceptance and baseline evidence | 8 | F4 and F5 are genuinely closed: the marker-file test 4 does reject an all-but-one post-pass, and `stop_on_fail` cannot satisfy it because every check in that fixture passes; test 7 pins the record round-trip the PRD's own divergence needed. But F3 is not closed — I defeated test 6 by execution (B1), test 6 is also nondeterministic by construction (B2), PRD Acceptance 3's "reported before anything runs" is claimed proved and is unobservable (B3), and round 1's F8 is unfixed: the manifest gate still passes `"schema": {}`. |
| Failure, recovery and compatibility | 15 | Recovery is still clean — one new directory, nothing else touched. `stop_on_fail` is specified precisely and test 5 pins name, exact command, sentinel output, `skipped` status and the absent third marker; that test is sound. No Verify block starts a host, so the shared-daemon hazard does not apply. −5: the gate collect must see green twice is nondeterministic (B2), and the record path cannot be exercised for real until the sibling child enables the cartridge (N7). |
| **Reviewer total** | **75 / 100** | Real progress from 58; three of five round-1 blockers closed; three blockers stand. |

### Blocking findings

**B1 — `specs/spec01.md:396-405` with `:524-531`: test 6 is still defeatable, and I defeated it.**
The offline property rests on a grep for the literal token `Command::new` in
`checks.ctg/src`. A `discover` that shells out through `use std::process::Command as Sh;`
never produces that token. Built at `/tmp/rev2-defeat`: `spawn_one` is the only
`Command::new` site, `discover` spawns `sh -c` through the alias. The spec's Verify
block printed `Command::new sites = 1` and exited 0, and
`test service::tests::discovery_and_selection_record_the_set_without_spawning ... ok`.
All three of test 6's assertions passed — the discovered set was non-empty, `SPAWNS` was
unchanged across `discover` and `select`, and `SPAWNS` rose after `run` — while discovery
had spawned a child process, which is the exact behaviour the spec says the test rejects.
The third assertion closes round 1's vacuity but not the property.

**B2 — `specs/spec01.md:279-280,341-346,537`: the pinned gate is nondeterministic.**
`run::SPAWNS` is one process-global `AtomicUsize` and test 6 asserts it constant, while
tests 4 and 5 spawn fixture checks in the same test binary. `cargo test --lib` runs tests
on parallel threads and the `run:` line sets no `--test-threads=1`. Executed at
`/tmp/rev2-defeat` with tests 4 and 5 present:
`assertion left == right failed: SPAWNS unchanged across discover and select, left: 5,
right: 0` — `test result: FAILED`. The same root cause hits the fixtures: step 1 specifies
"a process-unique directory name", so every test in the binary shares one fixture and one
marker directory, and test 4 clears the markers mid-run while test 5 is writing them.
Collect must see each pinned name pass, twice.

**B3 — `specs/spec01.md:426-428` against `prd.md:39`: "the selection is reported before
anything runs" is claimed as proved and cannot be observed.** `post` returns one answer
after the run completes; the spec's mechanism is the order of keys inside that object
(`:298-301`, "selection first, so the caller sees what will run … before anything runs").
Field order in a single synchronous response is not temporal order, and neither test 3 nor
test 4(a)(b) can fail on it. Nothing emits the selection before the run — and the
cartridge already declares events it could notify on.

### Non-blocking findings

- **N4 — `specs/spec01.md:199-203` cites the wrong door.** `memo.ctg/src/service.rs:113-140`
  is `describe()`'s **model tool** `input_schema`: `additionalProperties: false`, properties
  `op path body kind limit cursor usage query ref expected_revision event` — no `cwd`, which
  a request in the spec's shape would be rejected for. The op list quoted is from there
  (:122), but the trusted `cwd` comes from the native door at `:470-478`. The shape the spec
  writes down is right; only the citation is wrong.
- **N5 — `checks.ctg/Cargo.lock` is undeclared.** The `test` block's
  `cargo test --manifest-path checks.ctg/Cargo.toml` creates it inside the footprint. Every
  sibling Rust cartridge tracks one. Survivable — the lane pass commits it — but step 1
  should name it rather than leave collect to invent it.
- **N6 — tokio `macros` is missing.** `record`/`recorded` are `async`, so test 7 is async;
  `#[tokio::test]` does not compile under `["rt-multi-thread","sync"]`. Confirmed working
  with a hand-rolled `Builder::new_multi_thread().build().unwrap().block_on(…)`.
- **N7 — the `checks` memo kind is invisible until the sibling child lands.**
  `memo.ctg/src/record.rs:932-935` joins the records of **enabled** cartridges; `checks` is
  not enabled until spec02. Test 7 injects a sink, so nothing here notices, but the spec's
  "Memo validates on write against the kind, which is why the kind ships with the cartridge"
  is only true after registration. Say so, and let spec02 carry it.
- **Round 1's F8 is unfixed** (`specs/spec01.md:496`): `ev.schema === undefined` still passes
  `"schema": {}` while `:323-325` asks for a schema enumerating the four ops.
- **Round 1's F9 edges stand** (`:511-518`): the grep exits 0 when `checks.ctg` is absent
  (grep's exit 2 read as false), and its `--include` set is narrower than `just isolation`'s.

### What I re-checked and re-credit

The cartridge shape is accurate against `tools.ctg/Cargo.toml`, `tools.ctg/build.rs` and
the `#[path]` attachment at `tools.ctg/src/service.rs:641` — I compiled and ran that exact
shape. The isolation alternation lists exactly the eighteen cartridges carrying a
`cartridge.json` and correctly omits `cartridge.ctg`, verified by enumerating the tree. No
file is copied from upstream: `/Users/feb/dev/pi/packages/coding-agent/src/core/rigor/` is
still one 542-line `index.ts` and `checks.ctg` does not exist. Test 5 is sound. No block
starts a probe host, so the shared-socket hazard does not arise here.

Validation: all commands under `env -u CARTRIDGE_YOLO`, all writes under `/tmp`; nothing
created under `checks.ctg`, no `prd` operation, no commit, no `git add`, `prd.md` untouched.
Stand-in crate at `/tmp/rev2-checks-standin` with the spec's exact `Cargo.toml` (including
`tokio` `["rt-multi-thread","sync"]`), its `build.rs` and its `#[path]` attachment carrying
three pinned names, fresh `mktemp -d` `CARGO_TARGET_DIR`:
`cargo test --manifest-path … --lib` — exit 0, `Finished 'test' profile … in 9.07s`,
**10 s wall**, 3 tests ok, printed as `test service::tests::<name> ... ok`. Against the
120 s per-block ceiling that is a twelve-fold margin; the author's 13.65 s / 17 s is the
same conclusion on a colder cache. Defeat crate at `/tmp/rev2-defeat` as recorded in B1
and B2.

Reviewer identity: reviewer agent, coordinator-78 session (independent of the analyst, of
the spec's author and of the round-1 reviewer).
User rating: not supplied; none invented.
User feedback/provenance: none for this revision.
Result: **FAIL** — 75/100, below the 90 threshold, with three blocking findings.
Unresolved blocking findings: B1, B2, B3.
Rounds used / remaining: 2 / 3.
Next action: one revision replacing the token grep with a property a test can fail on
(a fixture whose only reachable tool is a `PATH` stub that records every invocation, so a
`discover` that shells out is caught however it spells `Command`), isolating the pinned
tests from each other (per-test fixture and marker directories, a per-run spawn count
rather than a process global, or `--test-threads=1` on the `run:` line), and either
emitting the selection before the run or restating PRD Acceptance 3. Then re-review at
round 3.
