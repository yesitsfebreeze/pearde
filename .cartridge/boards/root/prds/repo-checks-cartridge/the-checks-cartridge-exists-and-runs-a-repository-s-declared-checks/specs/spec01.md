---
complexity: large
footprint:
  - checks.ctg
---

# spec01 — checks.ctg: discover a repository's own checks, select the ones a change warrants, run them

Everything in this spec lives under `checks.ctg`. Nothing outside it is touched.
Registering the cartridge in the composition is the sibling child PRD
(`the-checks-cartridge-is-registered-in-the-composition`), and `just test checks`
only exists after it. This spec is gated by `cargo` against the manifest path
directly, which needs no registration.

## What the composition requires of any cartridge

Established by reading `tools.ctg` (the smallest) and `lsp.ctg` (one with real
ops), plus the three gates that judge a cartridge:

- `cartridge.json` declares the whole surface: `name`, `entry`, `source`,
  `description`, an `events` map where **every** event carries a `description`
  and a `schema`, a `listen` array, `commands` for `build`/`check`/`test`/`verify`
  delegating to `../cartridge.ctg/justfile` (the host is the platform, not a
  sibling, so this path is allowed by `just isolation`), a `grant` block, and —
  if any setting is declared — every setting with a `type` and a `doc` line.
  (`.cartridge/memos/routine/audit-cartridges.md` makes each of these a hard failure.)
- `init.lua` is three to five lines: `cartridge.load("<name>")` then one
  `cartridge.listen("<event>", …)` per declared event.
- The crate is a `cdylib` named for the cartridge, edition 2021, `mlua` 0.12 with
  `features = ["lua54","module","serde"]`, `[lints.rust] warnings = "deny"`,
  its own `[workspace]` stanza (no shared workspace), and `build.rs` emitting the
  macOS `-undefined dynamic_lookup` pair. **`module` plus dynamic lookup means no
  Lua is compiled at all** — the C API resolves lazily from the base binary that
  loads the module. There is no `vendored` feature anywhere in this composition.
  Copy the shape from `tools.ctg`, do not copy the file.
- `src/lib.rs` is the thin mlua boundary: `lua.from_value` in, `service::…`,
  `lua.to_value` out, errors as `LuaError::RuntimeError`.
- Unit tests live under `.cartridge/tests/unit/...` and are attached from the
  source module with `#[cfg(test)] #[path = "../.cartridge/tests/unit/<…>.rs"] mod tests;`
  — the pattern at `tools.ctg/src/service.rs:641`.
- `README.md` (≥10 non-blank lines) and `.cartridge/help.md` (non-empty) both
  exist and both describe the same surface.
- Only manifests, launchers and documented entry files at the cartridge root.
  No `TODO`/`FIXME`/`XXX`/`HACK` marker anywhere.

## Language and runtime: Rust

The composition holds eighteen cartridges with a `cartridge.json`, in three
shapes: fourteen Rust `cdylib` mlua modules (`agent`, `docs`, `fs`, `harness`,
`live`, `lsp`, `mcp`, `memo`, `memory`, `proxy`, `pty`, `router`, `sessions`,
`tools`), three bun/TypeScript (`auth`, `prd`, `web`), and one pure Lua —
`policy.ctg`, whose entire implementation is a 122-line `init.lua` with no crate.

So "a cartridge with real ops is Rust" is false, and `policy.ctg` is the
counterexample. The grounds that decide it for `checks.ctg` are two, both about
this cartridge's work rather than about the majority:

1. **The collect engine reads a test runner, and Lua has none here.** A `test`
   block is scored by the collector reading `test a::b::name ... ok` from cargo,
   `PASS` from nextest, or a JUnit report at `$PRD_TEST_REPORT`. `policy.ctg`
   ships no unit suite at all — `cartridge-development.md`'s `_cargo` recipe maps
   `policy)` straight to the smoke memo. This PRD demands named, executed,
   offline tests, so the cartridge must live in a language the gate can read.
2. **The work is filesystem walking, text parsing and bounded subprocess
   capture.** `policy.ctg` is a decision table over data the host hands it: no
   directory walk, no manifest parsing, no child process with a timeout and a
   stripped output tail. That is the difference in kind, not the language census.

## What upstream actually is, and what ports

`/Users/feb/dev/pi/packages/coding-agent/src/core/rigor/index.ts`, 542 lines, one
file, verified present. Read, not copied — no upstream file enters this repository.

Ports:

- `discover()` (lines ~140–230): `package.json` `scripts` for the keys
  `test`/`lint`/`typecheck`/`check`/`build`; `Makefile` and `justfile` targets
  matched at line start as `<name>:` or `<name> :` for `test`/`check`/`lint`;
  `Cargo.toml` → `cargo check` + `cargo test`; `go.mod` → `go vet ./...` +
  `go test ./...`; `pyproject.toml`/`pytest.ini`/`setup.cfg` **with** a `tests/`
  directory → `pytest`; a `probe.sh` in a directory or its child → `bash probe.sh`.
  One pass over the root, one over each non-dotted, non-`node_modules` child
  directory, deduplicated by check name. Upstream reads these files and never
  invokes the tool to enumerate them; that is the whole offline property, and
  test 7 executes it.
- The `Check` record: `name`, `cmd`, `cwd`, `scope`, `kind`. Keep all five and add
  `source` — the repo-relative file the check was discovered from — because the
  first acceptance demands it and upstream does not record it.
- `runOne()` (lines ~300–380): spawn through a shell, capture a bounded tail with
  ANSI and control bytes stripped, a per-check timeout, and a structured result
  carrying `passed`/`failed`/`timed_out`/`spawn_error`.
- The tier idea: upstream's `full ⊃ integration ⊃ fast <section>` becomes this
  cartridge's `gate` (everything) versus `post` (selected).

Does **not** port, deliberately:

- `.pi/rigor/checks.json`, `config.json`, `last.json` and the three generated
  `plan-*.md` files. The discovered set is recorded through this composition's
  own record ownership — a memo — not a second project-local store.
- `createVolatileChannel`, the status-line key, `EDIT_TOOLS`/`editedRelPath`
  post-edit hooking and the `auto` flag. Nothing in this cartridge triggers itself.
- The sub-agent dispatcher. The post-pass runs the checks in-process.
- `mistakes.md` and the pitfall injection. The composition already owns lessons
  through the memo record.

## How a Rust cartridge reaches the composition

There is no `cartridge.call`. The Lua global is assembled at
`cartridge.ctg/src/node/mod.rs:205-360` and carries `root`, `array_metatable`,
`trace`, `needs`, `events`, `listen`, `on_dispose`, `emit`, `notify`, `bail`,
`gather`, `publish`, `subscribe`, `host`, `load`, `pipe`, `spawn` — and nothing
named `call`. Two of those verbs matter here:

- **`cartridge.bail(name, data)`** — the first answer, nil when nobody answered
  (`cartridge.ctg/src/node/mod.rs:265-277`). This is how the record is written.
- **`cartridge.notify(name, data)`** — fire and forget
  (`cartridge.ctg/src/node/mod.rs:258-264`). This is how the selection is
  announced before the checks run.

Rust reaches both through a local `bridge.rs`, whose own header says "The same
file in every Rust cartridge; each uses its own subset"
(`harness.ctg/src/bridge.rs:1-8`). The working example:

- `harness.ctg/src/bridge.rs:105` — `pub fn call(&self, name, data) -> impl Future<Output = Result<Value>>`, body `Self::ask("bail", name, data)`, doc line `/// cartridge.bail(name, data)`.
- `harness.ctg/src/bridge.rs:126-133` — `ask_lua` performs
  `cartridge.call_function(function, (name, to_lua(lua, &data)?))` against the
  Lua global. `function` is a `&'static str`, so `ask("notify", …)` works through
  the same machinery as `ask("bail", …)`.
- `harness.ctg/src/bridge.rs:~250` — `drive(lua, future)` runs a future on the
  module runtime and answers the calls it makes on the handler's thread, which
  holds the base's Lua lock.

`harness`, `proxy` and `agent` all use this pattern while declaring
`needs: ["memo"]`. So does `checks`. Round 1's reason for avoiding it was void:
`memo.ctg` declares no `provide` keys, so `just isolation`'s reached-for-key
check cannot fire on `"memo"` from either side.

**The memo request shape**, read from `memo.ctg/src/service.rs:113-140`: the ops
are `list read write types index system resolve coverage observe resolver fabric`;
`write` requires `path` and `body`, `read` requires `path`, both take a trusted
absolute `cwd`. The record is
`{"op":"write","cwd":<absolute repository root>,"path":"checks/<name>.md","body":…}`
and the read-back is the matching `read`.

## Three seams, and why each exists

Every property this PRD demands was gated in an earlier round by reading the
source for a token. Each of those gates was defeated by code that did the wrong
thing without writing the token. So each property now has a **seam**: a trait the
production code implements against the composition and the test implements
against memory, so the property is observed by running the code rather than by
reading it.

| Seam | Production | Test observes |
| --- | --- | --- |
| `Records` | `bail("memo", …)` | the exact request, and the round trip |
| `Announce` | `notify("checks.selected", …)` | what had already run when the announcement arrived |
| `Shell` | `std::process::Command` in `run::spawn_one` | which commands were spawned, and by whom |

`discover` and `select` take **none** of the three. They cannot spawn, announce
or record, because they hold no capability to. That is the structural half; test
7 is the executed half.

## Steps

1. **`checks.ctg/Cargo.toml`** — package `checks`, edition 2021,
   `[lib] name = "checks"`, `crate-type = ["cdylib"]`, deps `mlua` (`0.12`,
   `["lua54","module","serde"]`), `serde`, `serde_json`, and `tokio`
   (`rt-multi-thread`, `sync`) for `bridge.rs`; own `[workspace]`;
   `[lints.rust] warnings = "deny"`. No `tempfile`: each test builds its own
   fixture directory (step 14).
   Add **`checks.ctg/clippy.toml`** containing
   `disallowed-types = ["std::process::Command"]`, and
   `#![deny(clippy::disallowed_types)]` at the top of `src/lib.rs`, with a single
   `#[allow(clippy::disallowed_types)]` on `run::spawn_one`. Clippy resolves the
   type rather than the token, so an aliased import is still flagged — measured,
   see "The lazy implementations" below. Add `checks.ctg/rustfmt.toml` and
   `checks.ctg/build.rs` in the shape `tools.ctg` uses, written fresh.

2. **`checks.ctg/src/bridge.rs`** — this cartridge's own copy of the shared
   bridge, written into this crate rather than referenced across the boundary.
   Only the subset used is kept: `runtime`, `wait`, `on_wake`, `submit`,
   `Ctx::call`, `Ctx::notify` (`Self::ask("notify", …)`), `ask_lua`, `to_lua`,
   `from_lua`, `pump`, `drive`. `warnings = "deny"` forbids leaving unused items
   in, so trim rather than `#![allow(dead_code)]`.

3. **`checks.ctg/src/check.rs`** — `pub struct Check { name, cmd, cwd, scope,
   source, kind }` with `pub enum Kind { Test, Lint, Typecheck, Build, Probe,
   Custom }`, both `Serialize`/`Deserialize`, `kind` serialized lowercase.
   `source` is repo-relative and never absolute.

4. **`checks.ctg/src/discover.rs`** — `pub fn discover(root: &Path) -> Vec<Check>`.
   Filesystem reads only. It takes no `Shell`, so it cannot spawn. Sources
   handled, each recording the file it came from:
   - `package.json` → `scripts` keys `test`, `lint`, `typecheck`, `check`, `build`;
     `cmd = "npm run <script>"`; `source` = that `package.json`.
   - `justfile` → targets `test`, `check`, `lint`; `cmd = "just <target>"`;
     `source` = `justfile`.
   - `Makefile` → same three targets; `cmd = "make <target>"`; `source` = `Makefile`.
   - `Cargo.toml` → `cargo check` (typecheck) and `cargo test` (test).
   - `go.mod` → `go vet ./...` (lint) and `go test ./...` (test).
   - `pyproject.toml` | `pytest.ini` | `setup.cfg`, **and** a `tests/` directory
     → `pytest` (test); `source` is whichever marker file was found.
   - `probe.sh` in a directory or one level below → `bash probe.sh` (probe).
   Root scope is `repo`; a child directory's scope is its own name. Deduplicate
   by `name`, first writer wins. A root with none of these yields an empty `Vec`
   — never a guessed command.

5. **`checks.ctg/src/record.rs`** — `pub trait Records { fn ask(&self, request:
   Value) -> Result<Value>; }`, with `impl Records for bridge::Ctx` performing the
   `bail("memo", …)`. `pub fn record(records: &dyn Records, root, checks)` sends
   the `write`; `pub fn recorded(records: &dyn Records, root) -> Result<Option<Vec<Check>>>`
   sends the `read` and parses the body back, returning `None` when memo answers
   nil.
   Ship the kind before its instances:
   `checks.ctg/.cartridge/memos/type/checks.md` declares the `checks` memo kind —
   a set of discovered checks for one repository root, with the frontmatter fields
   the instances carry. One instance per repository root holds the set, the root
   it was discovered at, and the ISO timestamp of the scan.

6. **`checks.ctg/src/select.rs`** — `pub fn select(checks: &[Check], changed:
   &[PathBuf], verify: Option<&str>) -> Selection`. A check is selected when its
   `scope` is the first path segment of a changed file, or when `scope == "repo"`
   **and** a changed file sits at the repository root. `verify`, when given, is
   selected as a `Custom` check named `change:verify` and is ordered first.
   Nothing else is selected. `Selection` carries the ordered checks and the reason
   each was selected. Takes no seam: pure, no `Command`, no filesystem.

7. **`checks.ctg/src/run.rs`** — the only module that spawns.
   `pub trait Shell { fn run(&self, cmd: &str, cwd: &Path, timeout_ms: u64) -> Outcome; }`
   with `pub struct Sh;` as the production implementation, whose `run` is the one
   `#[allow(clippy::disallowed_types)] fn spawn_one` in the crate: `sh -c` with
   cwd `root.join(check.cwd)`, environment forced to
   `NO_COLOR=1 FORCE_COLOR=0 TERM=dumb CI=1`, a bounded tail of merged
   stdout/stderr with ANSI escapes and control bytes stripped, and a per-check
   timeout. `pub fn run(shell: &dyn Shell, root, checks, timeout_ms, stop_on_fail)
   -> Report` drives it. Each `Outcome` carries `name`, `cmd`, `cwd`, `status`,
   `code`, `ms` and `tail`. With `stop_on_fail` the first non-passing outcome ends
   the run and every remaining check is reported with status `skipped` and is
   **not** handed to the shell.

8. **`checks.ctg/src/announce.rs`** — `pub trait Announce { fn selected(&self,
   root: &Path, selection: &Selection); }`, with `impl Announce for bridge::Ctx`
   sending `notify("checks.selected", {root, selection})`. This is the fix for
   "the selection is reported before anything runs": key order inside a returned
   object is not a happens-before, and a caller that only sees the final answer
   cannot act on the selection while the checks are still pending. A `notify` can
   be observed while the run is in flight.

9. **`checks.ctg/src/service.rs`** — the op boundary, `async` because the record
   ops are. `#[derive(Deserialize)] #[serde(tag = "op", rename_all = "kebab-case")] enum Action`
   with four variants. The seams are parameters, so the tests drive the same code
   the host drives:
   - `discover { root }` → `discover`, then `record::record`, returns the set. An
     empty set is `{"checks": [], "empty": true, "reason": "<root> declares no check"}`
     and is still recorded, so a later session reads "empty" rather than
     rediscovering.
   - `post { root, changed, verify? }` → `record::recorded`; on `None`, a fresh
     `discover` + `record`. Then `select`. Then **`announce.selected(...)`**, and
     only after it returns, `run(shell, …, stop_on_fail = true)`. The final answer
     still carries `{"selection", "skipped", "report"}` for the caller that wants
     it in one piece, but the announcement is the thing that happens first and it
     is what test 4 observes.
   - `gate { root }` → runs the entire recorded set with `stop_on_fail` false.
     Reachable only as this op: no code path in `discover`, `post` or `init.lua`
     constructs `Action::Gate`.
   - `recorded { root }` → returns the recorded set without running anything.
   Attach the tests here:
   `#[cfg(test)] #[path = "../.cartridge/tests/unit/service/tests.rs"] mod tests;`

10. **`checks.ctg/src/lib.rs`** — `#![deny(clippy::disallowed_types)]`, then
    `mod announce; mod bridge; mod check; mod discover; mod record; mod run;
    mod select; mod service;` and the `#[mlua::lua_module] fn checks(...)`
    exporting `dispatch` and `selftest`. `dispatch` is
    `bridge::drive(lua, async move { service::dispatch(request, &Ctx, &Ctx, &Sh).await })`,
    so the service's calls to memo are answered on the handler's thread while it
    holds the base's Lua lock — the `harness` pattern.

11. **`checks.ctg/init.lua`** — `local checks = cartridge.load("checks")`, then
    `cartridge.listen("checks", …)` and `cartridge.listen("checks.selftest", …)`.
    No listener here reaches the `gate` op on its own.

12. **`checks.ctg/cartridge.json`** — `name` `checks`, `entry` `init.lua`,
    `source` `https://github.com/yesitsfebreeze/checks.ctg`, a `description`,
    `"needs": ["memo"]`, `"contracts": ["checks.selftest"]`, and three declared
    events, each with a `description` and a real `schema`: `checks` (the four
    ops), `checks.selftest`, and **`checks.selected`** — defined and emitted, not
    listened to, carrying the root and the selection so any cartridge can see what
    is about to run. `listen` names the first two only. The four `commands`
    delegate to `../cartridge.ctg/justfile` with target `checks`. A `grant` block.
    `settings` — each with `type` and `doc` — for at least `timeout_ms` (per-check
    ceiling) and `tail_lines` (captured output lines). Settings arrive settled and
    may be `null`: read them with `?? undefined` semantics on the Lua side and
    never re-check a declared bound in Rust.

13. **`checks.ctg/README.md`** and **`checks.ctg/.cartridge/help.md`** — what the
    cartridge owns, the events it defines and listens to, that it needs `memo`,
    one line per op with its argument shape, that `checks.selected` is emitted
    before the post-pass runs anything, and that the full gate is an explicit
    operation the post-pass never triggers. README ≥10 non-blank lines. Both
    written in the same change as the behaviour, per
    [[cartridge-readme-stays-current]]. Plus `checks.ctg/.gitignore` with `target/`.

14. **`checks.ctg/.cartridge/tests/unit/service/tests.rs`** — the eight named
    tests below. **Every test's state is its own.** A `fixture(test_name)` helper
    builds a directory at
    `std::env::temp_dir().join(format!("checks-{test_name}-{pid}-{nonce}"))` with a
    process-local `AtomicUsize` nonce, and a `Drop` guard removes it. Fixtures are
    inline `fs::write` calls of string literals — nothing is fetched, cloned or
    installed. Marker files, witness files and injected seams all live inside that
    per-test directory, so two tests in the same binary under parallel
    `cargo test` cannot see each other's state. The single exception is `PATH`,
    which is process-global: test 7 rewrites it and every test that needs the real
    `PATH` takes the same `static PATH_LOCK: Mutex<()>` for the instant it needs
    it, with `unwrap_or_else(|e| e.into_inner())` so one failing test does not
    poison the rest.

## The lazy implementations, and what each gate does to them

For every gate below, the shortest wrong code that would make it pass was written
and run at `/tmp/rev3-experiment`. The result is recorded, not claimed.

**L1 — discovery that shells out through an aliased import.**
`use std::process::Command as Sh;` then `Sh::new("just").arg("--summary")`, with a
fallback that returns the correct names so the correctness assertions still pass.

- Against round 2's gate (`grep -c 'Command::new'` expecting ≤1):
  **`Command::new sites = 0`, exit 0 — the gate passed the defeat.** This is B1,
  reproduced.
- Against `#![deny(clippy::disallowed_types)]` + `clippy.toml`:
  **two errors, exit non-zero** — `use of a disallowed type std::process::Command`
  at the import *and* at the call site. Clippy resolves the path, so the alias
  does not help.
- Against test 7 (PATH shims + witness): **FAILED**,
  `discovery invoked a tool: just`, `left: "just\n"  right: ""` — while the same
  run's honest implementation passed. The lazy version returned the *right answer*
  and was still caught, which is the point: the gate is on the behaviour, not the
  result.

**L2 — announcing the selection after the run instead of before.**
Identical selection, identical final answer, `announce.selected(...)` moved below
the loop that runs the checks.

- Against round 2's claim (key order inside the returned object):
  **passes** — key order is not a happens-before, which is B3.
- Against test 4: **FAILED**,
  `checks had already run when the selection was announced: ["ran-change:verify", "ran-a:test"]`.
  The not-announced-at-all variant is caught separately by the
  `.expect("the selection was never announced")` on the recorder.

**L3 — the nondeterminism that made round 2's test 6 unattributable.**
Round 2 asserted a process-global `AtomicUsize` stayed constant while sibling
tests spawned in the same binary; the reviewer turned it red at `left: 5,
right: 0`. Replaced by a per-test witness file. Receipt: a
`a_spawning_test_beside_it_does_not_disturb_the_witness` test that spawns five
children was added to the same binary and the suite run three times — the witness
test passed in all three, in three different interleavings, while the L1 test
failed in all three for its own reason. Nothing process-global remains except
`PATH`, which is serialized.

## The eight tests, and the wrong implementation each rejects

1. `discovery_records_each_declared_check_with_its_command_and_source` — over a
   fixture carrying a `justfile`, a `package.json` scripts block, a `Makefile`, a
   `Cargo.toml` and a pytest layout, asserts the exact `(name, cmd, source)`
   triple for every expected check and that no unexpected name appears.
   **Rejects:** a `discover` that omits `source`; one that sets `source` to the
   root rather than the file; one that attributes the `just test` check to
   `Makefile`; an empty body.
2. `a_repository_declaring_no_check_records_an_empty_set` — over a root holding
   one unrelated file, asserts `discover` is empty and the op's answer carries
   `empty: true` with a reason naming the root.
   **Rejects:** a fallback default command for an unknown repository; reporting
   emptiness as an error rather than an answer. Paired with test 1, which an
   always-empty implementation fails.
3. `selection_names_only_checks_reaching_the_changed_files_and_the_declared_verify`
   — over a fixture with scopes `repo`, `a`, `b` and a change confined to `a/`,
   asserts set equality of the selected names against `{change:verify, a:…}`.
   **Rejects:** a `select` returning everything (the whole-suite behaviour this
   PRD exists to prevent); one returning only the verify; one dropping the verify;
   an empty body.
4. `the_selection_is_announced_before_any_check_runs` — injects an `Announce`
   recorder that, at the instant it is called, lists the marker files present.
   Asserts the announced selection is correct, that **no marker existed yet**, and
   that afterwards every selected check has run.
   **Rejects:** L2, announcing after the run (markers present at announcement);
   never announcing (the recorder is empty and the `expect` fires); announcing a
   selection different from the one executed. This is the executed happens-before
   the PRD asks for, and it is not satisfiable by key order in a return value.
5. `the_post_pass_runs_exactly_its_reported_selection_and_the_gate_runs_the_rest`
   — over the three-scope fixture with the change confined to `a/`: runs `post`,
   asserts (a) the markers equal the announced selection, (b) no marker exists for
   any `b`-scope check; then clears and runs `gate`, asserting (c) a marker exists
   for every check in the recorded set including `b`'s.
   **Rejects:** a `post` running the full set while reporting narrowly; any
   divergence between reported and executed; a `gate` that skips some; and — where
   a count could not — an all-but-one post-pass. `stop_on_fail` cannot truncate it
   because every fixture check in this test passes. (Survived round 2's attempts
   unchanged; 5(a) is self-consistency, and an under-running `post` is caught by
   test 6.)
6. `the_post_pass_stops_at_the_first_failing_check_and_reports_its_output` — the
   second selected check prints a sentinel and exits non-zero; a third follows.
   Asserts the failing outcome carries the name, the exact `cmd`, and a tail line
   containing the sentinel; that the third is `skipped`; and that the third left
   no marker.
   **Rejects:** running everything and reporting failures at the end (the third
   marker exists); a status without captured output; a name without its command;
   an empty body.
7. `discovery_and_selection_invoke_no_tool_from_the_path` — the fixture carries a
   `shims/` directory holding executables named `just`, `cargo`, `npm`, `go`,
   `make`, `pytest`, `python3` and `sh`, each of which appends its own name to the
   fixture's witness file and exits 1. Under `PATH_LOCK`, `PATH` is set to that
   directory alone, `discover` and `select` run, `PATH` is restored. Asserts the
   discovered set is complete and correct **and** the witness file is empty.
   **Rejects:** L1 and every variant of it — `std::process::Command`, an aliased
   import, a fully-qualified path, a helper crate, anything that ends in an
   `execve` of a tool by name. Measured against L1: FAILED with
   `discovery invoked a tool: just`. An empty body fails the first assertion. This
   replaces round 2's token grep, which L1 defeated.
8. `the_recorded_set_round_trips_through_the_record_owner` — injects an in-memory
   `Records` sink, calls `record`, asserts the captured request is `op: "write"`
   with an absolute `cwd`, a path under the `checks` kind and a non-empty body;
   then calls `recorded` against the same sink and asserts the returned
   `Vec<Check>` equals what went in, `source` included.
   **Rejects:** a `record` that writes nothing; one dropping `source` or `cwd`; a
   `recorded` returning `None` or empty for a populated record.

## Acceptance

- [ ] Discovery — test 1 passes: every declared check is recorded with the command
      that runs it and the repo-relative source file it was discovered from.
- [ ] Empty repository — test 2 passes: an empty set is recorded and reported, and
      no command is invented.
- [ ] Selection — test 3 and test 5(a)(b) pass: the post-pass selects only the
      checks reaching the changed files plus the declared verify, and executes
      exactly that selection.
- [ ] **Reported before anything runs** — test 4 passes: the selection is
      announced on `checks.selected` and observed while no check has yet run.
- [ ] First failure — test 6 passes: a failing check reports name, command and
      output, and every later check is skipped rather than run.
- [ ] Full gate — test 5(c) passes: the gate is reachable as its own op and runs
      the whole recorded set; no post-pass path reaches it.
- [ ] Offline — test 7 passes: discovery and selection invoke nothing from `PATH`,
      so no fixture path can reach the network; fixtures are inline `fs::write`
      calls under a per-test temporary directory.
- [ ] Record divergence — test 8 passes: the recorded set round-trips through the
      record owner with the memo `write`/`read` shape.
- [ ] `checks.ctg/README.md` and `checks.ctg/.cartridge/help.md` exist and describe
      the four ops, the `checks.selected` event and the needed `memo` key.
- [ ] `checks.ctg/cartridge.json` parses, declares `needs: ["memo"]`, and gives
      every declared event a `description` and a `schema`.

## Verify and Proof

<!--
Engine facts (prd.ctg/.cartridge/templates/spec.md): each block is `sh -eu -c`,
120 s, empty stdin, NO injected environment — a `${VAR:?}` reference aborts both
passes. Blocks run twice: pass 1 with cwd = the lane worktree, pass 2 with
cwd = /Users/feb/dev/cartridge. Paths stay relative to the repo root; never `cd`
to an absolute checkout. Pass 2 runs in the live checkout, so every cargo command
exports its own CARGO_TARGET_DIR. Blocks must not write inside the footprint: all
scratch goes to `target/checks-verify`, which is outside `checks.ctg`.

Build cost, measured three times, never estimated. Round 1's cold-build risk
paragraph rested on a false premise — it said "mlua with the vendored Lua 5.4",
but the features are ["lua54","module","serde"] with no `vendored`, and with
`module` plus `-undefined dynamic_lookup` no Lua compiles at all. Deleted.

  round-1 reviewer, no tokio, empty target dir:    exit 0,  7.46 s / —
  round-2 analyst, with tokio, fresh mktemp -d:    exit 0, 13.65 s / 17 s wall
  round-2 reviewer, with tokio, fresh mktemp -d:   exit 0,  9.07 s / 10 s wall

Three independent runs, the same conclusion: a twelve-fold margin under the 120 s
ceiling on a warm cache and sevenfold on a cold one. Confirmed in the same runs:
`cargo test --lib` builds a harness for a `crate-type = ["cdylib"]` library, and
the pinned names print as `test service::tests::<name> ... ok`, the form the
collector reads.

Round 2's `grep -c 'Command::new'` block is DELETED, not weakened. It was
defeated by `use std::process::Command as Sh;` at /tmp/rev3-experiment, printing
`Command::new sites = 0` and exiting 0 while the code shelled out. A token grep
cannot express "spawns no process"; test 7 executes the property and the clippy
block below enforces it at compile time.
-->

The cartridge's shape, independent of the build:

```sh
test -d checks.ctg
test -f checks.ctg/cartridge.json
test -f checks.ctg/init.lua
test -f checks.ctg/README.md
test -f checks.ctg/.cartridge/help.md
test -f checks.ctg/.cartridge/memos/type/checks.md
test -f checks.ctg/clippy.toml
test "$(grep -cv '^[[:space:]]*$' checks.ctg/README.md)" -ge 10
bun -e '
  const fs = require("node:fs");
  const m = JSON.parse(fs.readFileSync("checks.ctg/cartridge.json", "utf8"));
  const fail = [];
  if (m.name !== "checks") fail.push("the manifest does not name this cartridge");
  if (!m.description) fail.push("the manifest carries no description");
  if (!Array.isArray(m.needs) || !m.needs.includes("memo")) fail.push("the record owner is not declared as a need");
  const announced = Object.keys(m.events || {}).filter((k) => k !== "checks" && k !== "checks.selftest");
  if (announced.length === 0) fail.push("no event carries the selection to a caller before the run");
  for (const [key, ev] of Object.entries(m.events || {})) {
    if (!ev.description) fail.push("an event is declared without a description: " + key);
    if (ev.schema === undefined) fail.push("an event is declared without a schema: " + key);
  }
  for (const [key, s] of Object.entries(m.settings || {})) {
    if (!s.type || !s.doc) fail.push("a setting is declared without a type or a doc line: " + key);
  }
  if (fail.length) { console.error(fail.join("\n")); process.exit(1); }
  console.log("manifest declares its surface");
'
```

No sibling checkout is reached from inside the cartridge. Verified structurally in
round 1: planting `path = "../memo.ctg/evidence"` made this block exit 1 naming
file and line; a clean tree exits 0. The alternation lists the eighteen real
cartridges and omits `cartridge.ctg`, which is the platform, not a sibling:

```sh
if grep -rInE '\.\./(agent|auth|docs|fs|harness|live|lsp|mcp|memo|memory|policy|prd|proxy|pty|router|sessions|tools|web)\.ctg' \
    --include='*.rs' --include='*.lua' --include='*.toml' --include='*.json' --include='*.md' \
    checks.ctg; then
  echo "this cartridge reaches into another cartridge's checkout; it ships its own copy or asks over a declared event" >&2
  exit 1
fi
```

The compile-time half of the offline property. Clippy resolves the disallowed type
through any alias or qualified path, so this fails on a second place that can
spawn wherever it hides. Measured against L1: two errors, at the import and at the
call:

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/checks-verify}"
cargo clippy --manifest-path checks.ctg/Cargo.toml --all-targets -- -D warnings
```

The behaviour itself. One cargo invocation, its own target directory, outside
the footprint:

```test
run: sh -c 'export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/checks-verify}"; cargo test --manifest-path checks.ctg/Cargo.toml --lib'
pass: discovery_records_each_declared_check_with_its_command_and_source
pass: a_repository_declaring_no_check_records_an_empty_set
pass: selection_names_only_checks_reaching_the_changed_files_and_the_declared_verify
pass: the_selection_is_announced_before_any_check_runs
pass: the_post_pass_runs_exactly_its_reported_selection_and_the_gate_runs_the_rest
pass: the_post_pass_stops_at_the_first_failing_check_and_reports_its_output
pass: discovery_and_selection_invoke_no_tool_from_the_path
pass: the_recorded_set_round_trips_through_the_record_owner
```
