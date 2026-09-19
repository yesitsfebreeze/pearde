# @root/one-daemon.../the-composed-acceptance-test... review history

Plan: `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`, `prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances/prd.md`.
Scope: one composed Rust test in `cartridge.ctg` proving the parent's four acceptance boxes; executable leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: `cartridge.ctg` d1692932449c89106bb1928b717146ee8b0083a8, clean tree
(`git -C cartridge.ctg status --porcelain` empty at start and end of this review).
No dirty files in `repo`. Specs dir contains `spec01.md` only.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../prd.md` — `b5f47656e02fe2f659eee49dafdf64dca350f75a80ab9dbcd55b44047883f5a3` |
| Specs | `specs/spec01.md` — `56a4a927c147cf08e100b236875d723f494f836ca81256ebb8532f51edb29bee` |
| Material contracts/dependencies | analyst-1.md `f62d69674abaaa64a1e00d05f30cbea9c8c98430b4d0e1e169e8ec87b016cd86`; `cartridge.ctg` d169293 (`justfile:5-7`, `Cargo.toml:8`, `src/lib.rs:15-17`, `.cartridge/tests/unit/src/tests/mod.rs:1-4`, `src/host/socket.rs:47-86`, `src/cli/host.rs:289-307,341-349,379`, `src/cli/mod.rs:137`, `src/host/process.rs:106-110`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | The PRD is the parent's Acceptance made runnable; one fixture + four bodies is the right slice and SPECCED-not-SPLIT is correctly argued (all four claims share one fixture). −3: the toy three-cartridge profile is not the real composed profile, so the test proves the *shape* and not the product's composition; disclosed honestly in Remaining risk and unavoidable from a `cartridge.ctg` lane. |
| Ownership and reuse | 19 | Every structural claim verified independently and all hold. `cartridge.ctg/justfile:5-7` is exactly `cargo nextest run --workspace`, so Rust-not-bun is correct and a `.test.ts` under `cartridge.ctg/.cartridge/tests/` would indeed be run by no gate. `Cargo.toml:8` `autotests = false`; `src/lib.rs:15-17` `#[path = "../.cartridge/tests/unit/src/tests/mod.rs"] mod tests;`; `mod.rs:1-4` is `mod host; mod ledger; mod node; mod settings;` — adding `mod composed;` needs **no `src/` edit**, so the two-file footprint is right and needs no widening. `run_dir = base()/tag(descriptor)` (`socket.rs:71-79`), nodes in `run_dir/<pid>` (`:80-86`), `host.sock` in `run_dir` (`:69-73`) — the counting rule is correct and is the fix for this board's recurring defect. `launch`/`mcp` need no tmux and no agent (`cli/host.rs:289-307`, `:341-349`, `:379`); node argv is `<binary> node` (`process.rs:106-110`); `cartridge stop` is a real documented command (`cli/mod.rs:137`). Reuses `built()`, `trust()` and takeover.test.ts's `sample()` shape. −1: no citation for a panic-safe teardown, see B3. |
| Dependencies and implementable slices | 17 | All eight `needs` siblings are `done`. Lane is a plain worktree: no `.gitmodules`, no path deps in `Cargo.toml` — nothing to be empty, pass 1 can build. Budget risk **measured and dissolved**: `cartridge.ctg/.cargo/config.toml` sets `rustc-wrapper = "kache"`, and a from-empty `CARGO_TARGET_DIR` `cargo nextest run --workspace --no-run` finished in **9.6 s wall** (188 lock packages), so block 1's compile is not the 120 s threat the spec treats as its first risk. −3: Step 1 pins four `#[tokio::test]` names but never says where the fixture lives relative to the bodies, which is the structural gap B1 exploits. |
| Observable acceptance and baseline evidence | 6 | The gate does not gate. A 28-line vacuous `composed.rs` that starts no host, composes nothing and asserts nothing about the four claims **passed all four Verify blocks, exit 0 each**, measured in a scratch worktree (see Validation). −10 for B1. −2: the analyst's cheat table is a simulation of the blocks' arithmetic, and its row (a) contradicts its own prose (table says (a)'s plain census is `4 passed`; the prose says (a) "is rejected twice over, once by block 1", i.e. red in the plain run). −2: Verify block 4 (`cargo fmt --all --check`) exits **0 on the clean tree** — it is hygiene, not a gate on this deliverable. Credit where due: the four blocks are otherwise well built — `Starting 4 tests` + `4 tests run: 4 passed` are the exactly correct nextest strings (verified against the real tool: `Starting 0 tests across 2 binaries (180 tests skipped)` / `Summary [ 0.000s] 0 tests run: 0 passed, 180 skipped`), every static guard is a positive `if grep -qn ...; then exit 1; fi`, there is no statement-level `! grep`, no `a\|b` alternation, and no `test -n "$X" && test "$X" -ge N` AND-OR list. `<=` is banned outright and exact positive equalities are required — the sibling's `0 <= 1` defect is properly closed. |
| Failure, recovery and compatibility | 9 | −7 for B2: `socket::base()` (`src/host/socket.rs:49-53`) applies `.filter(\|dir\| dir.as_os_str().len() < 48)` **after** `.join("cartridge")`, so an `XDG_RUNTIME_DIR` longer than 37 chars is silently discarded and the host falls back to `/tmp/cartridge-<uid>`. `tempfile::tempdir()` on this machine returns a 60-char path (`TMPDIR=/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/`), 70 after the join. The spec's stated isolation ("this suite can never see, count or disturb the machine's live project daemon") therefore does not hold as written, and its own acceptance box ("every host it starts is under a scratch `XDG_RUNTIME_DIR`") would be false while block 3's `grep -q 'XDG_RUNTIME_DIR'` still passes. `/tmp/cartridge-501` currently holds 229 run directories from the live project and other sessions. −4 for B3: the fault run is *designed* to panic 3–4 tests, and a Rust panic skips the explicit `cartridge stop` teardown the spec describes; pass 2 runs in the live checkout, so every collect would leak daemons and their `sleep 120` children. Credit: per-descriptor `tag()` scoping means the *counts* stay correct even under the fallback base, and `pgrep -P <daemon pid>` is correctly scoped so other sessions' daemons are invisible. |
| Reviewer total | 68 / 100 | Three blocking findings; the gate is defeated by a measured 28-line non-implementation. |

Findings and concrete revisions:

- **B1 (blocking) — the fault switch is in-band, so the fault gate is defeated by one line.** Step 1 puts the fixture and the four bodies in the same file and the same process, and nothing stops a body from reading `CARTRIDGE_COMPOSED_FAULT` itself. Block 3 *requires* the string to appear in `composed.rs` but never bounds where. Measured: a `composed.rs` whose four bodies are `assert!(!faulted())`, with the block-3 decoy strings in a doc comment, produced `Starting 4 tests` / `4 tests run: 4 passed` plain and `4 tests run: 0 passed, 4 failed` under the fault — **blocks 1, 2, 3 and 4 all exit 0**, in 18 ms of test time. It starts no host, composes nothing, and proves none of the four claims. Fault injection gates *sensitivity to the injected fault*, which is strictly weaker than *asserting the four claims*, and is a cheat defence only when the signal is unreachable by the code under test. Recommendation, both parts: (i) split the fixture into its own file, bodies in the other, and make block 3 assert `test "$(grep -c 'CARTRIDGE_COMPOSED_FAULT' <fixture>)" = 1` **and** `test "$(grep -c 'CARTRIDGE_COMPOSED_FAULT' <bodies>)" = 0`, plus a zero-count guard on the fixture accessor's name in the bodies file (separate positive guards, never `a\|b`); (ii) add an out-of-band receipt that a vacuous body cannot forge — each test appends its observed daemon pid, composition count and node count to `$CARGO_TARGET_DIR/composed-log/report.txt` (outside the footprint), block 1 asserts four receipt lines carrying `compositions=1 nodes=3` and a non-zero pid, and block 2 asserts the fault receipt carries `compositions=3`. That gates measured world state, not an exit code.
- **B2 (blocking) — the scratch `XDG_RUNTIME_DIR` is discarded at 38 characters.** See the dimension-5 evidence. Recommendation: place the per-test runtime dir with `TempDir::new_in("/tmp")` under a short prefix (`/tmp/cx<pid>` keeps the joined path near 20 chars), and add a positive Verify guard that the fixture does not use the default `tempfile::tempdir()` for the runtime dir; better still, have the fixture assert at runtime that the run directory it is about to count actually lives under the dir it exported, which fails loudly instead of silently sharing `/tmp/cartridge-<uid>`.
- **B3 (blocking) — teardown is not panic-safe, and block 2 panics by design.** Recommendation: make the fixture a `Drop` guard that issues `cartridge stop` for every root it started (and reaps the spawned `sleep 120` children), so the fault run cleans up; state it in Step 1 and keep block 3's `pkill`/`killall` ban.
- **F4 (non-blocking) — Verify block 4 is inert for this PRD**, exit 0 on the clean tree. Keep it, but it earns no acceptance credit; the four real gates are blocks 1–3.
- **F5 (non-blocking) — the analyst's cheat table is simulated, and one row is internally inconsistent.** Ruling: the gap is **acceptable in a plan, not blocking**. It is disclosed plainly in analyst-1.md ("I did *not* build four full Rust trees... that is the implementation of the PRD"), it names its scripts, and the **spec itself carries no simulated table presented as measurement** — which is precisely what the sibling spec was marked down for. Demanding a reference implementation from an analyst is the wrong bar. But the simulation is the proximate cause of B1: simulating the blocks' arithmetic can only confirm the blocks compute what their author already imagined; it can never discover a tree the author did not imagine. The cheapest possible real measurement — 28 lines, one worktree, under a minute — falsified the table's central claim. One real tree beats five imagined ones.

Disposition: revise. The footprint, the counting rule, the Rust-not-bun call, the exact-equality discipline and the block string shapes are all correct and should be preserved verbatim; round 2 needs the fixture/body split, the receipt, the short runtime dir and the `Drop` teardown.

Validation (all commands run by the reviewer; cwd and exit status as shown):

- `cd cartridge.ctg && git rev-parse HEAD` → `d1692932449c89106bb1928b717146ee8b0083a8`; `git status --porcelain` empty before and after.
- Verify blocks run verbatim as `sh -eu -c` against the **clean tree**, cwd `cartridge.ctg`, `CARGO_TARGET_DIR` preset to a scratch path outside every repository (the blocks' own `${CARGO_TARGET_DIR:-...}` honours it):
  - block 1 → **exit 1** (`Starting 0 tests across 2 binaries (180 tests skipped)`, `error: no tests to run`).
  - block 2 → **exit 1** (same census).
  - block 3 → **exit 1** (`test -f .../composed.rs` fails first).
  - block 4 → **exit 0** — passes with the deliverable absent.
- Verify blocks run verbatim against a **scratch worktree of d169293** carrying the 28-line vacuous `composed.rs` described in B1 (worktree removed, `worktree prune` run, `status --porcelain` empty afterwards):
  - block 1 → **exit 0**, `Summary [ 0.010s] 4 tests run: 4 passed, 180 skipped`.
  - block 2 → **exit 0**, `Summary [ 0.008s] 4 tests run: 0 passed, 4 failed, 180 skipped`.
  - block 3 → **exit 0**. block 4 → **exit 0**.
- Budget: `CARGO_TARGET_DIR=<empty scratch> cargo nextest run --workspace --no-run` → exit 0, `Finished 'test' profile in 7.96s`, `real 9.64`s; `rustc-wrapper = "kache"` in `cartridge.ctg/.cargo/config.toml`.
- Isolation: `python3` probe of `tempfile.mkdtemp()` → 60-char path, 70 with `/cartridge`, `< 48` is `False`; `ls /tmp/cartridge-501` → 229 run directories.
- Inert-guard sweep of spec01.md: no statement-level `! grep`, no `\|` alternation, no `test -n "$X" && test "$X" -ge N`. Clean.

Reviewer identity: independent reviewer subagent, round 1, session 546d3989.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (68/100, three unresolved blocking findings).
Unresolved blocking findings: B1 in-band fault switch defeats the fault gate (measured); B2 scratch `XDG_RUNTIME_DIR` discarded above 37 chars; B3 teardown not panic-safe while block 2 panics by design.
Rounds used / remaining: 1 / 4.
Next action: bounded revision of spec01.md addressing B1–B3; no implementation until round 2 passes.

## Round 2 — 2026-09-17

Presented revision: `cartridge.ctg` d1692932449c89106bb1928b717146ee8b0083a8, clean tree
(`git -C cartridge.ctg status --porcelain` empty at start and end; `git worktree list`
shows no worktree added by this review). Reviewed revision is the analyst's second
`specs/spec01.md`, published in place, plus the preserved reference implementation.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../prd.md` — `b5f47656e02fe2f659eee49dafdf64dca350f75a80ab9dbcd55b44047883f5a3` (unchanged since round 1) |
| Specs | `specs/spec01.md` — `ea4c7f799a9ff26cbceec281fa963e2937e602d319522f02970db7f75cd6b4e1` |
| Reference implementation | `.state/loop/.../reference/fixture.rs` — `6e73b6b130b69e6c1cf450b4aa002708a24efe0ef98f6cb2096018454c65a68f`; `reference/mod.rs` — `a6db12bd4b90d5124e41d2402382b18b6d95cc4c61ef7d8a9472567b4642f72d` |
| Material contracts/dependencies | `cartridge.ctg` d169293: `src/host/socket.rs:12-33` (`owner_only_dir` **creates** the directory), `:47-62` (`base()`, the silent `< 48` filter), `:71-79` (`run_dir`), `:80-86` (`host_dir`), `:89-90`+`:268-278` (`sweep` → `lock_names` → `host.lock`), `Cargo.toml:8`, `.cartridge/tests/unit/src/tests/mod.rs:1-4,26-…` (`built()`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Unchanged from round 1 and still right: the PRD is the parent's Acceptance made runnable, one fixture plus four bodies. −3: the toy three-cartridge profile is not the real composed profile; disclosed honestly and unavoidable from a `cartridge.ctg` lane. |
| Ownership and reuse | 17 | Every new structural claim re-verified and all hold: `socket::base()` really does `.join("cartridge")` then `.filter(len < 48)` (`socket.rs:49-53`); `run_dir = base()/tag()`; `host.lock` is written only by `lock_names` from `sweep`, reached from `host_dir`, i.e. by a starting host; `--yolo status` and `--yolo call` are refused with exactly the quoted message; `call`/`status` start no host. Reuses `built()`, `trust`, the documented `stop`. −2: Step 1 tells the implementer to copy `attempt-1/composed/` "beside this file" — **that path does not exist**; the reference lives in `.state/loop/.../reference/`, which the spec never names, and the spec's own title line says `spec02` inside `specs/spec01.md`. |
| Dependencies and implementable slices | 14 | Footprint (three paths, all inside `.cartridge/tests/`) is correct and needs no widening; `mod composed;` needs no `src/` edit; compile budget confirmed (whole gate, cold-ish target dir, 7.7 s wall for block 1). −4 for **B7**: Step 3 says "Nothing else", but the preserved reference **fails Verify block 3** (`cargo fmt --all --check`, measured exit 1, diffs in both `fixture.rs` and `mod.rs`). Copy-as-instructed produces a red gate, and the spec's measured table has no block-3 column to show it. −2 for the missing/renamed reference path above. |
| Observable acceptance and baseline evidence | 6 | **The gate is defeated again, more cheaply than in round 1.** A 78-line `mod.rs` (`cheat D`) that uses the reference's *unmodified* `fixture.rs`, starts **no daemon, no composition and no node**, passed **all three Verify blocks, exit 0 each**, in 1.8 s of test time (`4 tests run: 4 passed`). It forges the four receipts by calling `lab.receipt("daemon=4242 compositions=1 nodes=3 …")` with literal text, and it mints the load-bearing **fifth `host.lock`** with one line: `std::fs::File::create(lab.run_dir(&lab.project()).join("host.lock"))`. −10 for **B6**. −2: the spec's measured table again reports only what its author looked for — block 3 is absent from it, and the reference's own run is marked `4 passed (1 leaky)` by nextest, which the gate's substring grep cannot see. Credit: the census strings, the exact-equality discipline and the guard shapes are all correct — the inert-guard sweep is clean (no statement-level `! grep`, no `a\|b`, no `test … && test …`). |
| Failure, recovery and compatibility | 15 | **B2 is closed as an effect** (−0): measured, `/tmp/cartridge-501` held 229 run directories before the reference run and 229 after, every counted path was under the block's own `/tmp/cxv<pid>` (13 chars; `+ "/<name>/cartridge"` ≈ 33, comfortably under 48), and the fixture's `assert!(dir.join("cartridge").as_os_str().len() < 48)` and `assert!(dir.starts_with(&self.base))` are real asserts on the measured path, not greps. **B3 is closed for daemons** (−0): daemon census 1 before, 1 after (only the live project daemon 3353), no lab root left under `/tmp`, `Drop` demonstrably ran. −5 for **F8**: `Drop` reaps the `launch` *instances* it spawned but not what the host launched for them — two orphan `/bin/sleep 120` (ppid 1) survived the reference run and lived out their 120 s. Bounded and self-terminating, but the spec claims "kills and reaps every spawned child", and pass 2 runs in the live checkout. |
| Reviewer total | 69 / 100 | Two blocking findings. The gate still does not gate: the new receipt is in-band, and so is the fifth host lock. |

Findings and concrete revisions:

- **B6 (blocking) — the receipt and the fifth `host.lock` are both in-band; a no-host implementation passes the whole gate in 1.8 s.** Two independent holes, both measured:
  1. `Lab::receipt(fields)` (`fixture.rs:240-250`) writes **whatever string the body hands it**. Block 2 bans the *env var name* in the bodies but not the *call*, so `lab.receipt("daemon=4242 compositions=1 nodes=3 same_node=1")` satisfies every receipt guard in block 1 without measuring anything. The receipt is out-of-*footprint*, not out-of-*band*.
  2. `Lab::run_dir` → `crate::host::socket::run_dir` → `owner_only_dir` (`socket.rs:12-33`) **creates** `base()/tag(descriptor)` for any descriptor, host or no host — independently confirmed outside the test suite: a plain `cartridge status` against a cold project left `/tmp/cxq1/cartridge/936bc0ed1266/` behind and started nothing. So a body can mint host locks under the gate's own `XDG_RUNTIME_DIR` at will, and `std::fs::File::create` is not in block 2's ban list (`create_dir` does not match it). The analyst's own `cheat C` was caught only by `4 = 5`; cheat D reaches `5 = 5` with **zero** daemons.
  Recommended fix, and it is small: **the fixture must measure and the body must not supply numbers.** Change `receipt` to take only a label (`lab.receipt("cold")`) and have it write `compositions=`, `nodes=` and `daemon=` from its *own* `self.compositions/nodes/daemon` calls at the moment it is invoked. Then a body that started no host writes `compositions=0 nodes=0 daemon=0` and block 1's existing guards reject it — the forging surface disappears rather than being grepped for. Do the same for the claim markers (`same_node`, `launches`, `control`) or drop them: a marker a body can type is not evidence. Additionally: the host-lock count is a weak second witness even so (any process can `touch` one); prefer counting what only a running host leaves *and* that the fixture reports — e.g. require the receipts' distinct non-zero `daemon=` pids to number 5 across the four files, computed by the fixture. Keep the body-side bans and add `File::create`/`fs::File` to them.
- **B7 (blocking) — the artifact Step 1 tells the implementer to copy does not exist at the named path, and fails Verify block 3.** `attempt-1/composed/` is not beside `spec01.md` (nothing is; the reference is in `.state/loop/.../reference/`), and `cargo fmt --all --check` against the preserved reference exits **1** with diffs in both files. Step 3's "Nothing else. No change under `src/`" therefore yields a red gate. Fix: run `cargo fmt` over the reference, re-preserve it, name its real path in Step 1, add a block-3 column to the measured table, and correct the `spec02` title line in `spec01.md`.
- **F8 (non-blocking) — launched grandchildren outlive `Drop`.** Measured: two `/bin/sleep 120` with ppid 1 after the reference run. `Drop` kills the `cartridge launch` children, not the programs the host launched on their behalf. Bounded (120 s) and daemon-free, so not blocking, but state it honestly instead of "kills and reaps every spawned child", or have test 2 stop the daemon before it drops the instances.
- **F9 (non-blocking) — nextest reports the reference as `4 tests run: 4 passed (1 leaky)`** (test 4, the cold one). Block 1's substring grep passes on it. Worth a line in the spec: the leak is real and the gate is blind to it.

Verdict on round 1's findings: **B1 NOT closed** — fault injection was correctly removed, but its replacement is defeated by a cheaper cheat (B6); the receipt is in-band because the body supplies its contents and can create the lock files the gate counts. **B2 closed** — measured as an effect, not an instruction. **B3 closed for daemons and directories**, partially open for launched grandchildren (F8). **F4 superseded by B7** — the fmt block is no longer inert, it is red against the spec's own reference. **F5 closed** — round 2's table is genuinely measured; its remaining defect is coverage (no block 3), not simulation.

Disposition: revise. Keep the footprint, the counting rule, the short-runtime asserts, the `Drop` guard, the exact-equality discipline and the block string shapes verbatim; round 3 needs only the receipt inversion (fixture measures, body labels), the extra body-side bans, a formatted reference at a path that exists, and block 3 in the table.

Validation (all commands run by the reviewer; `sh -eu <block>` verbatim from `spec01.md`, cwd = a scratch worktree of d169293, `CARGO_TARGET_DIR=/tmp/cxt2`, outside every repository):

| tree | block 1 | block 2 | block 3 | where it stopped |
| --- | ---: | ---: | ---: | --- |
| clean (no `composed/`) | **1** | **1** | — | `grep 'Starting 4 tests'` — `0 tests run`, `error: no tests to run` |
| reference implementation | **0** | **0** | **1** | block 1 green (`4 tests run: 4 passed (1 leaky)`, 4.1 s test / 7.7 s wall, 4 receipts, 4 test dirs, 5 host locks); block 3 red — `cargo fmt --all --check` diffs in `fixture.rs` and `mod.rs` |
| cheat A (four matching titles, empty bodies, real fixture) | **1** | **1** | — | compile error: `struct Lab is never constructed` (`warnings = "deny"`) — census absent |
| **cheat D (mine: no host at all; receipts forged as literals, fifth `host.lock` forged with `File::create`)** | **0** | **0** | **0** | **nothing stopped it** — `4 tests run: 4 passed`, 1.8 s, `test 4 = 4` test dirs, `test 5 = 5` host locks |

- Engine facts verified for the spec's design notes: `--yolo status` and `--yolo call` → `invalid argument: --yolo requires run, launch or daemon; it cannot change an existing daemon`; `status`/`call` against a cold project fail on the missing `host.sock` and start no host (daemon census unchanged) while still creating the run directory; `warnings = "deny"` turned three unused `mut`s and every unused fixture item into hard compile errors (this is what killed cheat A, and it is trivially silenced by an `#[allow(dead_code)]` never-called `touch()` — which is exactly what cheat D does, so do not rely on it as a defence). The one-file-per-receipt interleaving claim was not independently reproduced; the chosen design makes it moot.
- Inert-guard sweep of all three blocks: no statement-level `! grep`, no `a\|b` alternation, no `test -n "$X" && test "$X" -ge N`. Clean.
- Host hygiene: `cartridge daemon` census **1 before, 1 after** (only the live project daemon, pid 3353, `--dir /Users/feb/dev/cartridge`); `/tmp/cartridge-501` **229 run directories before and after**; no `/tmp` directory and no worktree left behind (`git worktree prune` run; `git -C cartridge.ctg status --porcelain` empty). Transient leak: two `/bin/sleep 120` orphans from the reference run, expired on their own (F8). **Leaked daemons: 0.**

Reviewer identity: independent reviewer subagent, round 2, session 546d3989.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (69/100, two unresolved blocking findings).
Unresolved blocking findings: B6 the receipt and the fifth host lock are in-band — a no-host cheat passes all three blocks in 1.8 s (measured); B7 the reference the spec says to copy is at a path that does not exist and fails `cargo fmt --all --check`.
Rounds used / remaining: 2 / 3.
Next action: bounded revision of `spec01.md` and the preserved reference addressing B6 and B7; no implementation until round 3 passes.

## Round 3 — 2026-09-17

Presented revision: `cartridge.ctg` d1692932449c89106bb1928b717146ee8b0083a8, clean tree
(`git -C cartridge.ctg status --porcelain` empty at start and end; `git worktree list`
shows no worktree added by this review). Reviewed revision is the analyst's third
`specs/spec01.md`, published in place, plus the preserved reference implementation,
which is byte-identical to the `attempt-2/composed/` copy the spec names.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../prd.md` — `b5f47656e02fe2f659eee49dafdf64dca350f75a80ab9dbcd55b44047883f5a3` (unchanged since round 1) |
| Specs | `specs/spec01.md` — `39caa4a942fcf888828a8ffda41ac388a4a4dc00c056e33e8fc1acca78f0c228` |
| Reference implementation | `.state/loop/.../reference/fixture.rs` — `a6bad1b2feeb6384d72b83d455985785070ab2666ec2f6dd8345c3d70a2ae623` (md5 `35304fff909420c9aa7c522a66be5dcf`); `reference/mod.rs` — `3699fd18cd8be74ee971ad3e9b1b86728860bbf42de0d6a6bdb702f21d0d5d2d` (md5 `f9c7a61bd4291b4dbea88f2932382110`). **Both md5s equal `<scratch>/analyst-composed-test/attempt-2/composed/`** — the two copies the spec distinguishes are the same bytes. |
| Material contracts/dependencies | `cartridge.ctg` d169293: `Cargo.toml:74-75` (`[lints.rust] warnings = "deny"` — *not* `Cargo.toml:8`, which is `autotests = false`), `src/host/socket.rs:12-33,49-53,71-79`, `.cartridge/tests/unit/src/tests/mod.rs:1-4` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Unchanged and still right: the parent's Acceptance made runnable, one fixture plus four bodies, correctly specced-not-split. −3: the toy three-cartridge profile is not the real composed profile; honestly disclosed and unavoidable from a `cartridge.ctg` lane. |
| Ownership and reuse | 18 | Re-verified independently at d169293: `[lints.rust] warnings = "deny"` is real and bites the *fixture* too (measured: removing every `lab.call` from the bodies made `method 'call' is never used` a hard compile error — an enforcement surface the spec does not claim and did not anticipate); `mod composed;` needs no `src/` edit; the counting rule and the short-runtime asserts are correct. −2 for **F15**: the spec states the `.state/loop/.../reference/` copy "is the round-2 version … and **fails `cargo fmt --all --check`**". It does not: it is byte-identical to `attempt-2` and Verify block 3 exits **0** against it (measured). An implementer is sent looking for a difference that does not exist, and the one artefact guaranteed to survive the scratchpad is the one the spec disparages. |
| Dependencies and implementable slices | 18 | Copy-as-instructed now produces a green gate; both named source paths exist and are `rustfmt`-clean; budget re-measured (3.3 s test time, whole block 1 well inside 120 s). Footprint unchanged and correct. −2 for **F13/F14**: block 1's default `CARGO_TARGET_DIR` is `$PWD/target/composed-verify`, i.e. inside `repo` — it is `.gitignore`d and distinct from `target/debug|release`, so it cannot hot-restart a live cartridge, but collect pass 2 runs in the live submodule and the block should pin a dir outside it; and `Drop` removes the project roots but not the `/tmp/cx<pid>` runtime directories (4 left behind after one run, measured). |
| Observable acceptance and baseline evidence | 5 | **The gate does not gate — third design, third pass-through.** My **cheat F** — four bodies containing only `Lab::new`, `lab.start`, `lab.settled`, one `lab.call`, the two `assert_eq!` strings block 2 greps for, and `lab.receipt(label)`, every assertion live, reached and *true*, no `#[allow`, no `#[expect`, no parked decoy, no comment, `rustfmt`-clean — passes **all three blocks, exit 0 each**, in 1.85 s, and its four receipts are indistinguishable from the reference's. It never runs `cartridge run`, never launches, never starts an `mcp`, never starts cold or concurrently: claims 1, 2 and 4 are wholly unproven and only the fixture's own probe touches claim 3. −10 for **B10**. −3: the stated ceiling is materially understated — it says cheat E is caught by block 2's `#[allow` rule, but cheat E needs no silencer at all, so nothing catches it. −2: the table's cheat E row is the weakest cheat in that class and its rejection column is an artefact of how it was built, not of the gate. |
| Failure, recovery and compatibility | 14 | Isolation **independently confirmed sound**: six suite runs (~20 daemons, plus one plain `cargo nextest run` with `XDG_RUNTIME_DIR` unset, which is the `just test` path and is green) left `/tmp/cartridge-501` at **231 before and 231 after**, daemon census 1 before and 1 after (only live pid 3353), 0 `sleep` orphans at the end. `is_socket` genuinely works (measured, below). −4 for **B11**: the `#[allow` rule, which the spec itself names as the last line of defence, is bypassable four ways, two of them measured. −2: `/bin/sleep 20` orphans (2 observed, self-terminating) and the runtime-directory residue above, both bounded. |
| Reviewer total | **72 / 100** | Two blocking findings. The inverted receipt is a genuine advance and beats cheat D; the body-side half of the gate collapsed instead. |

### Reproduced table (my own trees, my own reference, my own port of cheat D)

Scratch worktree of `d169293` at `/tmp/cxr3w`, `CARGO_TARGET_DIR=/tmp/cxr3t` (outside
every repository), blocks extracted verbatim from `spec01.md` and run as `sh -eu`.
Worktree removed and pruned afterwards.

| tree | b1 | b2 | b3 | rejected at |
| --- | ---: | ---: | ---: | --- |
| clean (no `composed/`) | **1** | **1** | 0 | census absent; `test -f "$bodies"` |
| reference implementation | **0** | **0** | **0** | — `Starting 4 tests` / `4 tests run: 4 passed`, 3.3 s, no `leaky`, 4 receipts exactly as the spec prints them |
| cheat D, ported (no host; `host.lock`, `host.sock` and three `.sock` files minted with `File::create`) | **1** | **0** | 0 | b1: `0 passed, 4 failed` — the bodies' own `assert_eq!(lab.compositions(&root), 1)` fails against the forgery, so no receipt is even written. **b2 exits 0**, not 1 as the spec's table claims (see B11.4) |
| **cheat F (mine): every required assertion live, reached and true; nothing else** | **0** | **0** | **0** | **nothing stopped it** — `4 tests run: 4 passed`, 1.85 s, receipts `roots=1 live=1 compositions=1 nodes=3 daemon=<pid> probe=hit probe_node=same` ×3 and `roots=2 live=2 …` for `instances` |
| cheat G (mine): cheat F plus `#![allow(dead_code)]` and a parked decoy holding the real claim assertions | **0** | **0** | **0** | **nothing stopped it** — `grep -c '#\[allow'` = **0**, `grep -c '#\[expect'` = **0** |

Cheat F's receipts, for comparison with the reference's in the spec:

```
test=cold      label=cold      roots=1 live=1 compositions=1 nodes=3 daemon=56070 probe=hit probe_node=same
test=instances label=instances roots=2 live=2 compositions=1 nodes=3 daemon=56069 probe=hit probe_node=same
test=run       label=run       roots=1 live=1 compositions=1 nodes=3 daemon=56071 probe=hit probe_node=same
test=shared    label=shared    roots=1 live=1 compositions=1 nodes=3 daemon=56064 probe=hit probe_node=same
```

### Findings

- **B10 (blocking) — the inverted receipt holds, and the gate falls anyway: a body that does only what block 2 greps for passes everything.** The receipt inversion is sound; I could not forge a number through it (see B12). But the fixture measures the *world*, and the world block 1 requires is produced by `lab.start` alone. Meanwhile block 2 requires exactly two things of a body: `grep -c 'assert_eq!(lab.compositions'` ≥ 4 and `grep -c 'assert_eq!(lab.nodes(&root), 3)'` ≥ 4 — **both of which are restatements of numbers the receipt already measured.** Nothing in either block requires `run`, `launch`, `mcp`, a cold concurrent start, a cross-process read, or any of the per-claim assertions that carry the parent's four boxes (`reply["node"] == before`, `launches == 2`, `read["hit"] == true`, `a["node"] == b["node"]`, `assert_eq!(lab.compositions(&root), 0)` first in the cold body). Measured: cheat F, 50 lines, 0/0/0, receipts byte-shaped exactly like the reference's, 1.85 s. The correct reading of rounds 1–3 is that the analyst has been hardening the *receipt* while the *body* requirement stayed a two-string grep. Recommended fix, in the same spirit as the round-2 fix that worked: **make the fixture observe the body's behaviour, not the body's text.** The fixture already mediates every interesting action — `cli`, `spawn`, `call`. Have `Lab` record which verbs passed through it (`run`, `launch`, `mcp`, `daemon`, `call`), which distinct client pids it saw, and how many roots were composed cold, and have `receipt` print those counts as fields alongside the existing ones (e.g. `verbs=run,launch,mcp,call clients=<n> cold=<0|1>`). Then block 1 requires `label=instances … launch=2 mcp=1`, `label=run … run=1`, `label=cold … cold=1`, and the four claims cannot be skipped by a body that starts a daemon and asserts the two grepped strings. That is still fixture-measured and still out-of-band, and it needs no new ban list.
- **B11 (blocking) — the `#[allow` rule, which the spec names as the enforcer of "assertions must be reached", is bypassable four ways.** rustc denying dead code is real; the gate's share of it is `grep -c '#\[allow'`, and that string is trivially avoided:
  1. **Measured.** `#![allow(dead_code)]` — the *inner* attribute — silences the whole module and contains no `#[allow` substring. `grep -c '#\[allow'` returns **0** and cheat G passes blocks 1, 2 and 3 with a parked function holding the real claim assertions.
  2. **Measured, same file.** `#[cfg(any())]` code is discarded before analysis, so it never warns at all; the assertions inside it still satisfy block 2's `grep -c` requirement.
  3. **Measured.** A commented-out assertion satisfies the count: `grep -c 'assert_eq!(lab.compositions'` on a file whose only such line is `// assert_eq!(lab.compositions(&root), 1);` returns **1**. rustc has nothing to deny.
  4. **Measured.** Block 2 greps only `$bodies` for `#[allow`; `fixture.rs` is in the same footprint and is never checked. My cheat D port silenced six unused `Lab` methods with `#[allow(dead_code)]` **in the fixture** and **block 2 exited 0** — so the spec's own table row for cheat D (b2 = 1) is an artefact of where its author chose to put the silencer.
  `#[cfg_attr(all(), allow(dead_code))]` and a bare `let _ = decoy;` are two more of the same shape, untested because the first two already settle it. A grep cannot express "this code runs"; only the fixture can, which is the same conclusion as B10.
- **B12 (verdict on the inverted receipt — it survived).** I could not make the fixture measure a number the world did not hold. `is_socket` genuinely rejects a plain file: cheat D's `File::create("store.sock")` × 3 plus `host.lock` and `host.sock` in the real `run_dir` produced `compositions()` = 0 and killed all four bodies on their own assertion. `run_dir` still creates `base()/tag()` for any descriptor (round 2's mechanism — my `forge` obtained the directory from a cold project with no host), but a directory with no socket in it counts 0, and each body gets its own `XDG_RUNTIME_DIR/<name>`, so leftovers from an earlier test in the same run cannot be seen, let alone counted. The only way I found to make the receipt read `compositions=1 nodes=3 probe=hit probe_node=same` was to start a real host — which is exactly what the inversion was for. **B6 is closed.**
- **F15 (non-blocking) — the spec misdescribes the preserved reference.** `.state/loop/.../reference/` is byte-identical to `attempt-2/composed/` (md5 `35304fff…`, `f9c7a61b…`) and passes block 3, contrary to the spec's claim that it is the round-2 copy and fails `cargo fmt --all --check`. Delete that paragraph and name `.state/loop/.../reference/` as the source: the scratchpad path does not outlive the session. Also: the spec's title line still reads `spec03` inside `specs/spec01.md` (round 2 raised the same mismatch as `spec02`), and the digest table's `Cargo.toml:8` for `warnings = "deny"` is wrong — it is `Cargo.toml:74-75`.
- **F13/F14 (non-blocking) — build and runtime residue.** Block 1 defaults `CARGO_TARGET_DIR` to `$PWD/target/composed-verify`, inside `repo`; harmless here (gitignored, distinct from `target/debug|release`, so no live dylib is replaced) but collect pass 2 runs in the live submodule and the block should pin a directory outside it. `Drop` does not remove the `/tmp/cx<pid>` runtime directories it creates; four were left after a single run.
- **On the stated ceiling — naming it is not enough, because the ceiling is named in the wrong place.** Candour is the right instinct and the disclosure is more honest than rounds 1 and 2. But the statement is *inaccurate in the direction that flatters the gate*: it says cheat E is caught by block 2, and the cheat-E class is not caught at all (B10) — and even the parked-decoy variant it does describe is not caught (B11). "A grep with rustc behind it" overstates the arrangement: rustc is behind it only for the one spelling the grep happens to match. A disclosed ceiling is acceptable when the thing above the ceiling is small and the disclosure is true; here the thing above the ceiling is three of the parent's four acceptance boxes, and the disclosure is not true. Blocking.

### Verdict on every earlier finding

- **B1 (round 1, in-band fault switch)** — superseded. Fault injection is gone for good; the successor defect is B10, one layer over.
- **B2 (round 1, `XDG_RUNTIME_DIR` discarded above 37 chars)** — **closed**, re-confirmed as an effect: `assert!(dir.join("cartridge").as_os_str().len() < 48)` and `assert!(dir.starts_with(&self.base))` are real asserts; `/tmp/cartridge-501` was 231 before and 231 after six suite runs.
- **B3 (round 1, panic-safe teardown)** — **closed** for daemons and roots; `Drop` ran on every path, daemon census unchanged, no lab root left. Open only for the disclosed `sleep` orphans and the runtime-dir residue (F14).
- **B6 (round 2, in-band receipt and forged fifth `host.lock`)** — **closed**, and closed well. See B12: the inversion plus `is_socket` defeats the ported cheat D outright.
- **B7 (round 2, reference at a non-existent path, fails block 3)** — **closed** on substance: both named copies exist and block 3 exits 0. Downgraded to F15 for the inaccurate description of which is which.
- **F8 (round 2, launched grandchildren outlive `Drop`)** — **closed as disclosed and bounded**: `sleep 120` → `sleep 20`, two observed, both gone within the run; the spec now says so instead of claiming it reaps everything.
- **F9 (round 2, `4 passed (1 leaky)` invisible to the gate)** — **closed**: block 1 now carries `if grep -qn 'leaky' "$log"; then exit 1; fi`, and my reference run produced no `leaky` line.
- **F4/F5 (round 1)** — remain closed; round 3's table is genuinely measured, and block 3 now has a column in it. Its defect is which cheats it chose, not whether it ran them.

### Validation

- Blocks extracted verbatim from `spec01.md` and run as `sh -eu` from a scratch worktree of `d169293` at `/tmp/cxr3w`, `CARGO_TARGET_DIR=/tmp/cxr3t`. Five trees, three blocks each, every exit code in the table above.
- Extra engine facts measured: `[lints.rust] warnings = "deny"` denies an unused **fixture** method, not only an unused body function (`method 'call' is never used … -D dead-code implied by -D warnings`) — a defence the spec does not claim; `#![allow(dead_code)]` and `#[cfg(any())]` both evade `grep -c '#\[allow'` and `grep -c '#\[expect'`; the reference is green under a plain `cargo nextest run --workspace -E 'test(tests::composed::)'` with `XDG_RUNTIME_DIR` unset (the `just test` path) in 3.3 s.
- Inert-guard sweep of all three blocks: no statement-level `! grep`, no `a\|b` alternation, no `test -n "$X" && test "$X" -ge N`. Every static guard is `if grep -qn …; then exit 1; fi` or a single `test`. **Clean.**
- Host hygiene: `cartridge daemon` census **1 before, 1 after** (only the live project daemon, pid 3353). `/tmp/cartridge-501` **231 before, 231 after** — my six suite runs added **zero**. `sleep` orphans: 0 at the end. `/tmp/cx*` removed. `git -C cartridge.ctg status --porcelain` empty; `git worktree list` shows no worktree of mine. **Leaked daemons: 0.**
- On the analyst's unattributed 229 → 231: the two entries are `/tmp/cartridge-501/d4ff636cacb6` and `/tmp/cartridge-501/aa1b45234521`, both stamped 14:19, both containing **only an empty `host.lock`** and no `host.sock` and no node directory — i.e. two client invocations that reached the fallback base, failed, and started nothing. Two distinct tags means two distinct project descriptors. The fixture cannot produce them: `short_runtime` falls back to `/tmp/cx<pid>` when `XDG_RUNTIME_DIR` is unset and *asserts* rather than falls back when it is set and long, and my six runs (two of them without the gate's env wrapper) added none. So the isolation **is** sound, and the +2 almost certainly came from `cartridge` commands run by hand outside the fixture during that round. The analyst's suspicion was right and its inability to prove it was a gap in its own bookkeeping, not in the fixture.

Reviewer identity: independent reviewer subagent, round 3, session 546d3989.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (72/100, two unresolved blocking findings).
Unresolved blocking findings: B10 — a body that satisfies block 2's two grepped assertion strings and nothing else passes all three blocks (measured, cheat F, 0/0/0), leaving three of the parent's four claims unproven; B11 — the `#[allow` reached-ness rule is bypassed by `#![allow(dead_code)]`, by `#[cfg(any())]`, by a comment, and by putting the silencer in `fixture.rs`, which block 2 never greps (four ways, two measured end to end).
Rounds used / remaining: 3 / 2.
Next action: bounded revision of `spec01.md` and the reference: have `Lab` record the verbs, client processes and cold starts it mediates and print them in the receipt, so block 1 requires the four claims' actions rather than block 2 greping for two assertion strings. Keep the receipt inversion, `is_socket`, the short-runtime asserts and the `Drop` guard verbatim — they are the parts that work.

---

## Round 4 — 2026-09-17

Presented revision: `cartridge.ctg` d1692932449c89106bb1928b717146ee8b0083a8, clean tree
(`git -C cartridge.ctg status --porcelain` empty at start and end; no worktree of this
review remains). Reviewed revision is the analyst's fifth `specs/spec01.md`, published in
place, plus the preserved `reference/` and `cheats/` beside `analyst-1.md`. Independent
reviewer; did not write the plan and did not review rounds 1–3.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../prd.md` — `b5f47656e02fe2f659eee49dafdf64dca350f75a80ab9dbcd55b44047883f5a3` (unchanged since round 1) |
| Specs | `specs/spec01.md` — `9a32104c2db19883898a45828ede4e9269a6a4bc12880c604b22a8eb12425099` |
| Reference implementation | `.state/loop/.../reference/{fixture.rs,mod.rs}`, copied verbatim into a detached worktree of d169293; all four blocks extracted verbatim from the spec and run with `sh -eu` |
| Material contracts/dependencies | `cartridge.ctg` d169293: `src/host/socket.rs:12,51,72-82` (`run_dir` → `owner_only_dir`), `Cargo.toml:74-75`, `.cartridge/tests/unit/src/tests/mod.rs`; `~/.cargo/config.toml` (`rustc-wrapper = "kache"`) — **not** `cartridge.ctg/.cargo/config.toml`, which does not exist |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Unchanged and still right: the parent's Acceptance made runnable, one fixture plus four bodies, footprint `.cartridge/tests/` only, no `src/` edit. −3: the toy three-cartridge profile is not the real composed profile, honestly disclosed. |
| Ownership and reuse | 17 | Re-verified at d169293: `mod composed;` needs no `src/` edit, the reference is `rustfmt`-clean, blocks 1–3 green on it, block 4 green in **11 s**. Every guard in blocks 1, 2 and 4 is a single positive statement — **no statement-level `! grep`, no `a\|b` alternation, no `test -n && test -ge` AND-OR**; round 3's shape lesson is fully absorbed. −3: the spec attributes `rustc-wrapper = "kache"` to `cartridge.ctg/.cargo/config.toml`; that file does not exist, the wrapper lives in the developer's user-global `~/.cargo/config.toml`, and block 4's whole 11 s budget rests on it. |
| Dependencies and implementable slices | 15 | Steps are two file copies plus one line; both named artefacts exist and are formatted. −3: **block 4 pins the deliverable to the analyst's exact Lua source text.** Its mutations are `str.replace` on `local node = tostring({})\nlocal seen = {}` and `count = #launches }`; any conforming alternative fixture makes the Python `assert body != before` fire and block 4 exits non-zero with `AssertionError`, i.e. the mutant gate is not implementation-independent — it is a copy check with a mutation attached. −2: **mutation 1's second replacement has no anchor assert of its own.** `assert body != before` is already satisfied by the first replacement, and `assert 'node()' in body` is true after the first replacement alone, so a half-applied mutation 1 passes both guards (memory: *verify that a patch anchor matched*). |
| Observable acceptance and baseline evidence | 12 | The verb tally is a genuine advance and genuinely kills cheat F. **But the mutant, which the spec names as the only thing that can kill cheat G, is defeated in-band — the same defect class as round 1's fault switch.** Measured, my own tree (**cheat H**, below): all four blocks exit **0**, receipts byte-shaped like the reference's, and **not one assertion about any of the four claims**. −6 for **B16**. −2: the measured table's `reference + stronger assertions` row claims **0/0/0/0**; measured, it is **0/0/1/0** — the preserved artefact fails `cargo fmt --all --check`, which is round 2's B7 pattern recurring on the artefact that advertises "no false red". −0 (credit) for the analyst's own correction about cheat G's rejection being incidental, which is right about block 1 — but wrong about block 4. |
| Failure, recovery and compatibility | 13 | Isolation is sound where it is claimed: **a controlled window over a full block 1 + block 2 + block 3 + block 4 cycle left `/tmp/cartridge-501` at 366 before, 366 after, 366 after** — the suite creates none. Daemon census 2 before, 2 after (both pre-existing). No `/tmp/cx*` residue after the blocks' traps. −5 for **B17**: the spec's Remaining risk ("running these beside other heavy work — expect a spurious red and rerun the target alone") is a **direct contradiction of the PRD's third Acceptance box**, which requires the test to pass "with a dirty developer environment (live daemon running, other sessions active) — contention-safe like host-tests-hold-under-suite-contention". −2: block 1 still defaults `CARGO_TARGET_DIR` to `$PWD/target/composed-verify`, inside `repo` (round 3's F13, not closed), and block 4's cost is a from-empty build into a fresh `$work/target` every run under a 120 s ceiling, held up only by the user-global `kache` wrapper above. |
| Reviewer total | **74 / 100** | Two blocking findings. The verb tally works; the mutant — the load-bearing gate — does not. |

### Reproduced table (my own worktree of d169293, my own tree, one at a time)

Detached worktree of `d169293` under my scratch, `CARGO_TARGET_DIR=/tmp/cxr4t` (outside
every repository), blocks extracted verbatim from the spec and run with `sh -eu` from the
worktree root. Exit codes, all four blocks, every row:

| tree | b1 | b2 | b3 | b4 | note |
|---|---:|---:|---:|---:|---|
| **reference** (preserved, verbatim) | **0** | **0** | **0** | **0** | 4 passed, no leaky; block 4 = **11 s wall** |
| **reference + stronger assertions** (preserved) | **0** | **0** | **1** | **0** | analyst's table says 0/0/**0**/0. b3 fails: `rustfmt` wants three of its five extra assertions wrapped. The *semantic* gate does not false-red it — **round 3's sibling finding does not recur** — but the preserved artefact is unformatted and the table cell is wrong. |
| **cheat H — mine, the round-4 defeat** | **0** | **0** | **0** | **0** | **passes everything; asserts nothing** |

I did not re-measure cheats A, D, F, or plain G: cheat H strictly supersedes them, since it
is cheat G with the verb tally tuned and one extra line. Their rejections in blocks 1 and 4
are not in dispute and are not what the round turns on.

### B16 (blocking) — the mutant is detectable from inside the code under test, so a tree with no assertions passes all four blocks

Block 4 discriminates the mutant run from the honest run **by the environment it hands the
code under test**: the tree is copied to `/tmp/cxm$$/tree`, built with
`--manifest-path "$mutant/Cargo.toml"`, and run with `XDG_RUNTIME_DIR="$work/rt"` where
`$work` is `/tmp/cxm$$`. Block 1's run uses `/tmp/cxv$$`. A body can read that difference.

**Cheat H** is the preserved cheat G — every verb performed for real against a real
one-daemon composition, the negative control real, **no assertion about any of the four
claims** — with exactly two changes:

1. three `let _ = lab.compositions/nodes/daemon(&root);` lines, so `warnings = "deny"` has
   no unused fixture method to complain about;
2. one helper, called first in each body, that looks like hygiene:

```rust
/// "The suite must run under the gate's own scratch root, never a developer's
/// live runtime directory." Reads as hygiene; is a mutant detector.
fn under_the_gates_root() {
	let rt = std::env::var("XDG_RUNTIME_DIR").unwrap_or_default();
	assert!(rt.contains("cxv"), "not the gate's scratch root: {rt}");
}
```

Measured exit codes: **block 1 = 0, block 2 = 0, block 3 = 0, block 4 = 0.**

Its four receipts are indistinguishable from the reference's, verb tally included:

```
test=run       label=run       roots=1 live=1 compositions=1 nodes=3 daemon=33797 probe=hit probe_node=same run=2 launch=0 mcp=0 call=5 cold=0 peak=1 run_node=same launched=0
test=instances label=instances roots=2 live=2 compositions=1 nodes=3 daemon=33795 probe=hit probe_node=same run=1 launch=2 mcp=1 call=5 cold=0 peak=5 run_node=same launched=2
test=shared    label=shared    roots=1 live=1 compositions=1 nodes=3 daemon=33798 probe=hit probe_node=same run=1 launch=0 mcp=0 call=7 cold=0 peak=1 run_node=same launched=0
test=cold      label=cold      roots=1 live=1 compositions=1 nodes=3 daemon=33867 probe=hit probe_node=same run=3 launch=0 mcp=0 call=5 cold=2 peak=2 run_node=same launched=0
```

And this is the mutant run block 4 accepted as proof that the suite objects to a broken
world:

```
Starting 4 tests across 2 binaries (180 tests skipped)
    FAIL [   0.010s] (1/4) cartridge tests::composed::one_instance_writes_what_another_reads_off_one_node
    ... panicked at .cartridge/tests/unit/src/tests/composed/mod.rs:13:5
 Summary [   0.011s] 4 tests run: 0 passed, 4 failed, 180 skipped
```

**Eleven milliseconds, no host started, no composition, four reds at the same line** — and
block 4 exits 0. Both of its structural guards behave exactly as designed and neither
helps: `Starting 4 tests` correctly distinguishes *built and ran* from *failed to build*,
and `4 tests run: 0 passed, 4 failed` correctly rejects a tree that asserts only one claim.
What neither constrains is **why** the four went red. This is the round-1 lesson restated:
a fault gate is a cheat defence only when the injected signal is unreachable by the code
under test. The mutant's signal — its own path — is the first thing the code under test can
read. The analyst moved the discriminator out of the footprint and out of the repository,
but not out of the process.

Answering the round's four sub-questions directly: **yes**, a body can detect the mutant
(`XDG_RUNTIME_DIR`, `env!("CARGO_MANIFEST_DIR")`, `file!()`, the absence of `.git`, the
mutant's separate `CARGO_TARGET_DIR` — measured with the first, the rest are the same
lever); **yes**, block 4 does distinguish a build failure from a test failure, correctly;
**yes**, a tree can satisfy `0 passed, 4 failed` for a reason unrelated to the claims — a
panic before any setup is the cheapest such reason and is what cheat H does; and the
mutations' anchors do match what the spec says they match, with the caveat in the
dimension-3 row.

Recommended fix, in the spirit of the round-2 fix that worked (make the fixture measure the
world, not the text) and the round-4 fix that worked (make the fixture tally the verbs, not
the greps): **make the mutant run indistinguishable from the honest run, and make the
fixture the judge of why a test went red.**

- Run the mutant *in the same place and the same environment* as block 1 — copy to the same
  `/tmp/cxv$$`-shaped root, export the same `XDG_RUNTIME_DIR` shape, and build with the same
  `CARGO_TARGET_DIR` layout — so no path, env var or compile-time constant differs between
  the two runs. This alone costs nothing and removes every lever cheat H used.
- Better, and independent of path hygiene: **require the receipts to prove the mutant run
  got as far as a live composition before objecting.** The fixture writes a receipt
  unconditionally at `lab.receipt(label)`; under mutation 1 the world really is composed
  (`compositions=1 nodes=3`), and the claim linkages really do go wrong
  (`probe_node=differs`, `run_node=differs`). So block 4 can require, from the *mutant's*
  `$work/receipts`, that the tests reached a real composition and that the fixture's own
  measurements record the broken world — e.g. four receipt files, `compositions=1 nodes=3`
  on each, and `probe_node=differs` / `run_node=differs`. Cheat H writes **no** receipt at
  all under the mutant, because it panics at line 13. A body that panics before composing
  anything then fails block 4 no matter what it detected, and the judge is again the
  fixture's measurement rather than an exit code.
- Both together are cheap and do not lengthen the block.

### B17 (blocking) — the spec's Remaining risk disclaims the PRD's third Acceptance box

The PRD's Acceptance reads: *"The test passes with a dirty developer environment (live
daemon running, other sessions active) — contention-safe like
host-tests-hold-under-suite-contention."* The spec's Remaining risk reads: *"Running all
six trees back to back … reddened every one of them, reference included … If collect runs
this beside other heavy work, expect a spurious red and rerun the target alone."* Those are
the same sentence with opposite signs, and the second is the measured one.

I rule this **blocking**, and I rule against the "rerun the target alone" mitigation, for
three reasons specific to this spec rather than to flaky tests in general.

1. **It is the PRD's own acceptance criterion**, not an incidental quality. This PRD's
   entire product is a gate; a gate whose red is not trustworthy has not delivered it.
   The board's standing note that a busy host fails gates spuriously is a note about
   *other* PRDs' gates being collateral damage — it is not a licence for a PRD whose
   deliverable is the gate.
2. **Collect runs each block twice** (lane, then `repo`), and block 4 runs a second full
   four-daemon suite inside block 1's own budget window. The suite is already its own
   heaviest neighbour: nextest runs the four bodies in parallel, so five hosts and fifteen
   node processes are racing a `settled` poll, inside a 120 s block limit.
3. **"Rerun alone" is not available to collect.** Nothing in the Verify contract lets a
   block ask for a quiet machine, and a human is not in the loop.

The fix is cheap and does not weaken anything: make the suite not contend with itself —
`cargo nextest run … --test-threads=1` in both block 1 and block 4, which serialises the
four bodies and costs roughly the sum of their runtimes (~4 s measured) — and, if that is
not enough under external load, raise `settled`'s budget and say what it is. Then either
re-measure the six-trees-back-to-back case honestly or amend the PRD's third box. What is
not acceptable is a spec that ships the box unmet and names the breach as remaining risk.

### Verdict on every earlier finding

| finding | round | verdict now |
| --- | --- | --- |
| **B1** in-band fault switch | 1 | **Regressed in a new form.** Fault injection is gone; the mutant that replaced it carries the same defect — the discriminator is readable by the code under test. See B16. |
| **B2** scratch `XDG_RUNTIME_DIR` discarded | 1 | **Closed.** `short_runtime` asserts `< 48`, `run_dir` asserts `starts_with(&self.base)`, both greppable in block 2; measured, the suite touches no shared base. |
| **B3** teardown not panic-safe | 1 | **Closed.** `impl Drop for Lab` issues `cartridge stop` per root and reaps children; no `pkill`/`killall` anywhere, guarded positively in block 2 for both files. |
| **F4** block 4 inert | 1 | **Superseded.** Block 4 is now the mutant and is anything but inert — it is simply beatable. |
| **F5** simulated cheat table | 1 | **Closed and stayed closed.** Round 4's table is built and measured; two cells are nonetheless wrong (see the reproduced table), which is a coverage/hygiene defect, not simulation. |
| **B6** receipt and fifth `host.lock` in-band | 2 | **Closed.** The inverted receipt holds. I did not attempt a forgery; round 3 already established none is available, and the verb fields are written from a private `Verbs` a body cannot reach. |
| **B7** named artefact missing / fails block 3 | 2 | **Closed for the reference** (measured `cargo fmt --all --check` = 0), **recurs for `cheats/reference-with-stronger-assertions.rs`**, which the spec cites as measured evidence of no false red and which exits **1** on block 3. Non-blocking; fix by formatting the preserved artefact and correcting the cell. |
| **F8** launched grandchildren outlive `Drop` | 2 | **Closed as disclosed.** `/bin/sleep 20`, `Stdio::null()`, stated honestly in Remaining risk. |
| **F9** leaky pass | 2 | **Closed.** Block 1 has `if grep -qn 'leaky' "$log"; then exit 1; fi`; measured green on the reference. |
| **B10** body requirement is a two-string grep | 3 | **Closed, and the fix is the best thing in this revision.** The verbs are tallied in `Lab::command()`, the one private constructor of every client process, before the command runs; a body cannot name a verb it did not perform, and cheat F dies at the claim-1 line. |
| **B11** `#[allow` rule bypassable four ways | 3 | **Closed by deletion, and the deletion leaves no gap** — the rule is gone from block 2 and nothing in the blocks now depends on it. One residue: the spec still claims under *Measured engine facts* that `warnings = "deny"` makes "a body that stops exercising part of the instrument fail to compile rather than pass quietly". Cheat H silences that in one character per method (`let _ = lab.nodes(&root);`), so the sentence overclaims a defence the spec no longer greps. Drop it or qualify it. Non-blocking. |
| **F13** `CARGO_TARGET_DIR` inside `repo` | 3 | **Not closed.** Block 1 and block 3 still default to `$PWD/target/composed-verify`. Harmless today (gitignored, not `target/debug|release`), still wrong for collect pass 2. |
| **F14** runtime-directory residue | 3 | **Closed.** Each block now traps `rm -rf "$work"`; measured, no `/tmp/cx*` survives any block. |
| **F15** spec misdescribes the preserved reference | 3 | **Closed.** The spec now names `.state/loop/…/reference/` as the source and its claim that it is `rustfmt`-clean and passes all four blocks is measured true. |

### Rulings the round specifically asked for

- **The verb tally cannot be faked without the command being built and run.** `Lab::command`
  is private, `Verbs` is a private field, and every path to it (`cli`, `spawn`, and through
  them `call`, `start`, `settled`, `try_call`, `try_run`) actually executes the command. The
  deleted `#[allow` rule leaves no gap the verbs do not cover. One honest qualification for
  the spec: the tally counts *attempted* invocations, not successful ones — `cli` increments
  before `.output()` and never checks the status — so `run=2` means two `cartridge run`
  processes were started, not that two succeeded. Cheat H did not need this, and the receipt's
  other fields (`probe`, `run_node`, `launched`) cover the gap in practice; state it rather
  than leave it implied.
- **The analyst's precision about cheat G is half right, and the wrong half is the one it
  staked the round on.** It is right that block 1's rejection of cheat G is incidental: I
  tuned G's verb counts to the reference's in about ten lines, and block 1 exits 0. It is
  **wrong** that block 4's rejection is the real one — block 4 exits 0 on the same tree. So
  the revision's answer to "would the test object?" is, as of this round, not gated at all.
- **No inert guard anywhere.** I checked every statement in all four blocks for the three
  known shapes: there is no statement-level `! grep` (all negatives are
  `if grep -qn …; then exit 1; fi`), no `grep 'a\|b'` alternation, and no
  `test -n "$X" && test "$X" -ge N` (the two `-ge` guards are single `test` statements on a
  `sed -n …p` substitution). Round 3's shape lesson is fully absorbed.

### `/tmp/cartridge-501`: 321 → 366 (+45), and **not** the suite's

The analyst reported +45 it could not attribute and asked for the mechanism. The mechanism
it names is right — `socket::run_dir` (`src/host/socket.rs:72-82`) calls `owner_only_dir` on
`base()/tag(descriptor)` and creates the directory, and the resulting skeleton is exactly one
empty `host.lock` with no socket and no node directory, which is what every one of the new
entries holds (newest inspected: `e19cacb306eb`, `-rw------- 0 host.lock`, nothing else).

But it is not this suite. **Controlled measurement: 366 entries before block 1, 366 after
block 1, 366 after blocks 2, 3 and 4** — a complete cycle including a four-daemon suite and a
four-daemon mutant suite created **zero**. My session's own +45 is real and matches the
analyst's +45 almost exactly, which given that we ran comparable numbers of suites in the
same repository is better explained by what we have in common *outside* the blocks — the live
project daemon and the other sessions working this board, every one of whose `cartridge`
invocations that lacks a usable `XDG_RUNTIME_DIR` mints one of these — than by the suite,
which I have now measured as creating none. The analyst was right to leave them in place and
right that its own short-base asserts did not fire. **Recommendation: this is a host-side
finding (`run_dir` creates and never reaps a run directory for a client that starts nothing),
not a defect of this spec; raise it against `runtime`, and delete nothing here.**

### Hygiene

`git -C cartridge.ctg status --porcelain` empty at start and end; `git worktree list` shows
no worktree of mine (the pre-existing `.runtime-composer-lane` is untouched). No `prd`
command, no commit, no edit to the spec, the PRD, the preserved reference or cheats, or any
file in `cartridge.ctg`. `CARGO_TARGET_DIR=/tmp/cxr4t`, removed; every block's own scratch
removed by its trap; no `/tmp/cx*` remains. **Daemons: 2 before, 2 after** (both pre-existing;
none killed, none by name). **`/tmp/cartridge-501`: 321 before, 366 after**, none attributable
to the blocks under controlled measurement — see above.

Result: **FAIL** (74/100, two unresolved blocking findings).
Unresolved blocking findings: **B16** — block 4's mutant is discriminated by a path and an
env var the code under test can read, so a tree with every verb real and no assertion at all
(cheat H) passes all four blocks, 0/0/0/0, with the mutant reporting `0 passed, 4 failed` in
11 ms from a panic at the detector line, having started no host; **B17** — the spec's
Remaining risk ("expect a spurious red, rerun the target alone") disclaims the PRD's third
Acceptance box (contention-safety), in a gate collect runs twice and which contends with
itself at four bodies in parallel.


## Round 5 — 2026-09-17 — FINAL ROUND

Presented revision: spec06 (`specs/spec01.md`, sixth revision) against
cartridge.ctg `d169293` (verified `git -C cartridge.ctg rev-parse HEAD` =
`d1692932449c89106bb1928b717146ee8b0083a8`, worktree clean before and after).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — b5f47656e02fe2f659eee49dafdf64dca350f75a80ab9dbcd55b44047883f5a3 |
| Specs | `specs/spec01.md` — 0de103fc13afadd8bf93699b7c3676e8fe8adf0f086a14ed2147cec77db88aa3 |
| Reference | `reference/fixture.rs` f26036e6…, `reference/mod.rs` 379aa0c4… |
| Cheats (preserved) | `g.rs` c2435634…, `h.rs` 48076e6b…, `strong.rs` 45b61bfe… |
| Reviewer's own tree | `cheats/i.rs` (new this round, written beside them) |
| Material dependency | cartridge.ctg `d169293`; `~/.cargo/config.toml` `rustc-wrapper = "kache"` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome; the four bodies map 1:1 onto the parent's four acceptance boxes. −2: the toy three-cartridge profile is not the real composition (disclaimed, and unavoidable from a lane whose `.lanes/` siblings do not include `memory.ctg`). |
| Ownership and reuse | 19 | All three footprint paths inside the PRD's `.cartridge/tests/`; attachment through `tests/mod.rs` with no `src/` edit — reproduced: adding `mod composed;` was sufficient, the suite compiled and ran. −1: `CARGO_TARGET_DIR=/tmp/cxbuild-composed` departs from the template (justified, but the gate now writes outside its own tree). |
| Dependencies and implementable slices | 19 | Three files, three steps; I installed the preserved reference into a clean checkout and it was green first time. −1: block 4's budget silently depends on `kache` being in `~/.cargo/config.toml` — stated, but it is an unstated prerequisite of the gate wherever collect runs. |
| Observable acceptance and baseline evidence | 14 | The receipt is genuinely the fixture's: `Drop` measures probe, `run_node`, `launched`, `live`, and the verb tally is taken in `command()`. Cheats A, D, F, G, H all still die. −6: **acceptance box 4 asserts a property measurement refutes.** A body with zero assertions about any of the four claims passes all four blocks (cheat I, 0/0/0/0) and produces exactly the four mutant receipts the box demands. |
| Failure, recovery and compatibility | 18 | `Drop` writes the receipt, then `cartridge stop` per root, reaps children, removes roots and its own runtime dir — on the panic path; verified across ~10 runs including four all-red mutant runs: daemon count 1 before / 1 after, no `/tmp/cxv*` left. No `pkill`/`killall` anywhere. −2: `/bin/sleep` orphans bounded not eliminated; `peak ≥ 4` is the one bound left. |
| Reviewer total | **88 / 100** | One blocking finding (B19). B18 is recorded as a ceiling, not as a blocker. |

### Reproduced table — real checkout, not a `/tmp` worktree

Trees measured at `/Users/feb/dev/cxr5-cartridge`, a detached worktree of
`d169293` under the developer's own `dev` tree (removed at the end; `git worktree
list` back to two entries). Every tree got the preserved `reference/fixture.rs`;
only `mod.rs` varied. `CARGO_TARGET_DIR` outside every repository.

| tree | b1 | b2 | b3 | b4 | where it was rejected |
|---|---:|---:|---:|---:|---|
| **reference** | **0** | **0** | **0** | **0** | — 4 passed, block 1 **11 s**, block 4 **15 s** |
| **reference + stronger assertions** (`strong.rs`) | **0** | **0** | **0** | **0** | — **self-correction confirmed: 0/0/0/0, `cargo fmt --all --check` clean** |
| cheat H (preserved, strengthened) | **0** | 0 | 0 | **1** | **b4 `test -d "$report"`** — **self-correction confirmed**: in a real checkout H passes b1; block 4 is its only rejection; its mutant run was 0.054 s and started no host |
| **cheat I (new — the defeat)** | **0** | **0** | **0** | **0** | **nowhere** |

### B18 — the `Drop` receipt does not close the class; it widened it (cheat I)

Cheat I is the preserved cheat G — every verb performed for real against a real
one-daemon composition, **not one assertion about any of the four claims** — plus
one line per body, placed *after* the `Lab` exists and after every verb:

```rust
fn from_a_checkout() {
	assert!(
		!env!("CARGO_MANIFEST_DIR").contains("/tmp/"),
		"running from a copy, not a checkout"
	);
}
```

Block 4 still copies the tree to `"$work/tree"` and builds it with
`--manifest-path`. Equalising `XDG_RUNTIME_DIR` removed one discriminator and
left a stronger one: the mutant's **path** — available to the body as a
compile-time constant, needing no runtime environment at all.

What the analyst's argument missed is that moving the receipt into `Drop` made
this *easier*, not harder. Because `Drop` writes a receipt unconditionally, a
body may now panic for **any** reason once the `Lab` is built and still leave the
receipts block 4 demands — and `probe_node` / `run_node` say `differs` because
the *mutation* made them differ, not because the body noticed. The two facts the
block reads are therefore independent of each other:

- *the world was whole and the mutation bit* — produced by the fixture, true of
  cheat G as well, which asserts nothing;
- *the four bodies went red* — produced by the body, for a reason the receipt
  does not record.

Measured, block 4 keeping its scratch (cheat I, mutant run):

```
Starting 4 tests across 2 binaries (180 tests skipped)
Summary [7.672s] 4 tests run: 0 passed, 4 failed, 180 skipped

test=cold      … compositions=1 nodes=3 daemon=7349 probe=hit probe_node=differs run=3 … cold=2 peak=2 run_node=differs launched=2
test=instances … compositions=1 nodes=3 daemon=7802 probe=hit probe_node=differs run=1 launch=2 mcp=1 … run_node=differs launched=4
test=run       … compositions=1 nodes=3 daemon=6827 probe=hit probe_node=differs run=2 … cold=0 peak=1 run_node=differs launched=2
test=shared    … compositions=1 nodes=3 daemon=6899 probe=hit probe_node=differs run=1 … call=7 … run_node=differs launched=2
```

and all four panics:

```
thread 'tests::composed::a_run_against_a_live_daemon_starts_no_node' panicked at
  …/composed/mod.rs:12:5: running from a copy, not a checkout
```

Four identical panics at the detector line — line 12, the hygiene helper — not
one at a claim. Block 4 exited **0**. The spec's sentences "the body now chooses
nothing" and "closes the class rather than disguising it" are refuted: the body
still chooses *whether to go red*, and that is the only thing block 4 asks of it.

**This is the same defect as rounds 1–4, one layer out**, judged by the review
method's own distinguishing test: the receipt's *contents* are fixture-produced
and could not be forged (a genuine advance, and it is what kills A, D, F), but
the *reddening* block 4 pairs them with is body-produced and keyed on an
out-of-band discriminator the body can read. Equalising one discriminator
(`XDG_RUNTIME_DIR`) cannot close it while the mutant is built from a different
path: `CARGO_MANIFEST_DIR`, `CARGO_TARGET_DIR` and the source path in
`file!()`/`std::env::current_exe()` all differ between block 1 and block 4.

Per the review method's ceiling clause (`review-plan.md:58-69`), a round has
been spent on this gate and it has been defeated again; **B18 is recorded as the
ceiling of this gate and is not by itself a blocking finding.** The backstop is
the diff reading: the preserved `reference/mod.rs` was read this round and does
contain four exact `assert_eq!`s per claim, with no bound and no detector.

Directions, should the user authorise another attempt: build the mutant **at the
same path** (mutate the checkout in place under a restore, or copy the clean tree
to `"$work/tree"` for block 1 as well, so both runs are the same shape), and/or
require the mutant's failure *messages* to name the claims' assertions rather
than only counting four reds.

### Verdict on every earlier finding

| # | round | finding | verdict |
|---|---|---|---|
| B1 | 1 | in-band fault switch defeats the fault gate | **resolved** — fault injection is gone entirely; replaced by the mutant |
| B2 | 1 | scratch `XDG_RUNTIME_DIR` silently discarded above 48 chars | **resolved** — fixture asserts `as_os_str().len() < 48`, block 2 greps it; hosts really came up under `/tmp/cxv…/rt` in all my runs |
| B3 | 1 | teardown not panic-safe | **resolved** — `Drop` stops, reaps, removes; verified across four all-red mutant runs with no daemon growth and no leftovers |
| B6 | 2 | receipt and the fifth host lock are in-band | **resolved** — the receipt's contents are fixture-measured; I could not author a field from a body |
| B7 | 2 | reference path missing / not rustfmt-clean | **resolved** — reference exists at the loop path and block 3 passes on it and on `strong.rs` |
| B10 | 3 | a two-string grep let cheat F pass without running the verbs | **resolved** — the verb tally is in the receipt, taken in `command()`; cheat I had to perform every verb for real to survive block 1 |
| B11 | 3 | `#[allow]` reached-ness rule bypassable four ways | **resolved (moot)** — the rule is gone |
| B16 | 4 | block 4's mutant discriminated in-band (cheat H) | **partly resolved, not closed** — the env discriminator is gone and cheat H now dies at block 4; the path discriminator remains and cheat I passes. Succeeded by B18 |
| B17 | 4 | contention disclaimed, contradicting the PRD's third box | **resolved** — the sentence is gone, `--test-threads=1` is in blocks 1 and 4, measured here at **11 s** and **15 s**, both far inside 120 s; the PRD box is not amended |

### B19 — the acceptance text asserts a gate property that measurement refutes (blocking)

Spec acceptance box 4 ("**A mutant … fails all four tests AND leaves four
receipts …** — the suite objected to the broken composition, not to the fact that
it was a mutant") and the What-changed prose ("the body now chooses nothing",
"closes the class") state as fact a discrimination the gate does not have. An
implementer or collector reading this spec would believe the suite is protected
against an assertion-free body; it is not (cheat I, 0/0/0/0, measured above).
This is a text defect, not new gate design: replacing those two claims with the
recorded ceiling — *"block 4 gates the node-identity claims; it is defeated by a
body that panics on the mutant tree's path, so the diff reading of `mod.rs`'s
four `assert_eq!`s is the backstop"* — would make the spec true as written, and
on my scoring would carry dimension 4 to 16–17 and the total to 90–91. No round
remains to make that edit, which is why it is recorded rather than fixed.

### Shell-hygiene audit of the four Verify blocks

No statement-level `! grep` (every negative guard is `if grep -qn …; then exit 1;
fi`), no `grep 'a\|b'` alternation, no `test -n "$X" && test "$X" -ge N` AND-OR
pair. `--no-fail-fast` is present in block 4 and is load-bearing: re-running the
same mutant without it gives `1/4 tests run: 0 passed, 1 failed` and **one**
receipt, which would fail both the census grep and the four-receipt count.
Block 1 correctly does not need it (it requires `4 tests run: 4 passed`).

Findings and concrete revisions: **B18** (recorded ceiling — `Drop`-receipt gate
defeated by cheat I, 0/0/0/0, evidence above and `cheats/i.rs` preserved);
**B19** (blocking — acceptance box 4 and the What-changed prose state a property
that is false; the correction is two paragraphs).
Disposition: **keep** the plan and the reference implementation — both are sound
and were reproduced green in a clean checkout — and correct the acceptance text
to the ceiling.
Validation: cwd `/Users/feb/dev/cxr5-cartridge` (detached worktree of `d169293`,
removed after; `git -C cartridge.ctg status --porcelain` empty, `git worktree
list` back to 2). Blocks run verbatim from the spec with
`CARGO_TARGET_DIR=/tmp/cxbuild-composed` (outside every repository). Exit codes
in the table above; block 1 11 s, block 4 15 s, both under the 120 s limit.
Host hygiene: 1 daemon before, 1 daemon after; no kill by process name; every
host started under a short `XDG_RUNTIME_DIR` inside the blocks' own `/tmp/cxv…`
roots; all scratch roots removed (`/tmp/cxv*` count 0, `/tmp/cxbuild-composed`
removed). `/tmp/cartridge-501` 1491 → 1626, already attributed to the host and
other sessions and not re-raised.
Reviewer identity: independent reviewer subagent, round 5 (did not write the
plan and did not review rounds 1–4).
User rating: not supplied; delegated.
User feedback/provenance: none this round.
Result: **FAIL (88/100)** — round 5 exhausts the allowance. **This was the final
round.**
Unresolved blocking findings: **B19** — the spec's fourth acceptance box and its
"the body now chooses nothing / closes the class" prose assert a discrimination
the gate does not have (cheat I passes all four blocks with no assertion about
any claim).
Recorded ceiling (not blocking, per `review-plan.md:58-69`): **B18** — the
mutant block can be defeated by any body that panics on the mutant tree's path
once the `Lab` exists; defeated attempts A, D, F, G, H, I are preserved beside
this record; the diff reading of `reference/mod.rs` is the backstop.
Rounds used / remaining: **5 / 0**.
Next action: **stop automatic revisions.** The PRD goes to `question`. What the
user is being asked to decide is narrow: accept the spec with B18 recorded as a
ceiling and B19's two paragraphs corrected (the implementation itself is green
and was reproduced by an independent reviewer), or grant a new allowance for a
same-path mutant.

## Round 6 — 2026-09-19 — user-granted round, scoped to B19 by the Decision

Presented revision: spec06 with the analyst's B19 text edits
(`analyst-composed-6.md`), against cartridge.ctg `d169293`
(`git -C cartridge.ctg rev-parse HEAD` = `d1692932449c89106bb1928b717146ee8b0083a8`;
live worktree untouched before and after, its only dirt the unrelated
untracked `src/asp/` of a peer session). Scope per `prd.md` `## Decision
(2026-09-19, coordinator cartridge-ctg-cd)`: B19 only; no gate design.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — 3bbc615b9c62c20da8d13f8fe8791d0557051126d7543d39c72b7d8307c08b72 (Decision section added since round 5; body otherwise unchanged) |
| Specs | `specs/spec01.md` — 6a6953e13d6673c4efbcf3be0b2aafce7586009e1043fb9065e45e38209fc78c |
| Reference | `reference/fixture.rs` f26036e62ef9cfb1…, `reference/mod.rs` 379aa0c4f84b1aeb… (unchanged since round 5) |
| Material dependency | cartridge.ctg `d169293`; `~/.cargo/config.toml` `rustc-wrapper = "kache"`; `review-plan.md` step 4 ceiling rule |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Unchanged from round 5: one outcome, four bodies 1:1 onto the parent's four boxes. −2 toy profile (disclaimed, unavoidable from the lane). |
| Ownership and reuse | 19 | Unchanged; attachment via `tests/mod.rs`, no `src/` edit — reproduced again in the `ref` clone. −1 `CARGO_TARGET_DIR` outside the tree (justified). |
| Dependencies and implementable slices | 19 | Unchanged; reference installed per Steps, green first time. −1 kache as a silent prerequisite of block 4 (stated). |
| Observable acceptance and baseline evidence | 15 | **Improved from 14, not to 16–17.** Acceptance box 4 is now true: it keeps the mechanical requirement, calls the receipt "the fixture's own measurements … unforgeable by the body", says the reddening is not attributed to the claims, names cheat I / B18 and the diff reading of `reference/mod.rs` as backstop. The new "Ceiling (B18, cheat I)" paragraph is accurate and cites the defeated attempts. −5: **the same refuted property is still asserted in five other places of the same spec** (B20 below), one of them the sentence directly above the corrected paragraph, so the spec now contradicts itself; the analyst's "grepped clean" statement is false. |
| Failure, recovery and compatibility | 18 | Unchanged. Re-measured: 1 `cartridge daemon` before, 1 after; `/tmp/cxv*` count 0 after; no kill by name. −2 `/bin/sleep` orphans bounded; `peak ≥ 4`. |
| Reviewer total | **89 / 100** | One blocking finding (B20, the unfinished part of B19). B18 remains a recorded ceiling, not a blocker. |

### B19 — verdict: partly resolved

Resolved where the Decision pointed: acceptance box 4 and the What-changed
paragraph beginning "The receipt's fields are the fixture's alone" now claim
only what is true, and the ceiling paragraph states B18 accurately (one round
spent on a same-path/same-environment gate, B16 closed, path discriminator
open, cheat I passes, `Drop` writes unconditionally, backstop = diff reading of
`reference/mod.rs`). I re-read `reference/mod.rs`: each body's claim-specific
linkage is an exact `assert_eq!` (`reply["node"] == before`; `launches == 2`;
`read["node"] == wrote["node"]`; `a["node"] == b["node"]`), with no `<=`/`>=`
and no detector — the backstop holds as described. ("one `assert_eq!` per
claim" should read "one linkage `assert_eq!` per claim"; each body has several.
Non-blocking.)

### B20 — the refuted discrimination is still asserted elsewhere in the spec (blocking)

The analyst reports "No other overclaiming language found … grepped clean
after edit". Measured with `grep -n` on the presented `specs/spec01.md`:

| line | text | why it is false |
|---|---|---|
| 50 | "A body that short-circuits on anything else writes no such receipt." | Cheat I short-circuits on its own path check and writes exactly this receipt (round 5, measured). It sits directly above the corrected paragraph that says the opposite. |
| 305 (block 2 comment) | "so no body chooses a field, a label, or whether a receipt exists at all." | The body chooses the label (`Lab::new("run")`, receipt uses `self.name`) and chooses whether a receipt exists (cheat H panics before any `Lab`; that is how block 4 rejects it). Line 55 of the same spec says "it supplies only its own label". |
| 335–337 (block 4 comment) | "the four tests must go red *because the composition they measured was wrong* … A body that short-circuits on anything else writes no such receipt." | This is the attribution the Decision said not to make. |
| 390 (block 4 comment) | "WHY they objected: the composition was whole, and what broke was the one thing the mutation broke." | The receipt records what the fixture measured, not why the body objected. |
| 452–454 (Remaining risk) | "The mutant gates the four claims … A body asserting only one claim survives mutation 1 but not the `0 passed, 4 failed` requirement" | A body asserting **no** claim passes it (cheat I, 0/0/0/0). |

The shipped reference also carries the claim in code: `reference/fixture.rs`
`receipt()` doc comment, "The body chooses NOTHING — not a number, not a label,
not whether it is written" — false on label and existence for the same reasons
(non-blocking, but it is deliverable text and should change in the same edit;
comment-only, `rustfmt` unaffected).

This is B19's defect — the spec states a discrimination the gate does not have
— left in five of its seven places. Verify-block comments are what a collector
reads when block 4 goes green, so they are not incidental prose. Fix: delete
line 50's sentence; make line 305 "no body authors a field; it supplies the
label and decides whether a `Lab` (and so a receipt) exists"; make 335–337 and
390 "the fixture measured a whole composition whose node identity the mutation
broke; why the body went red is not recorded (B18)"; rewrite the Remaining-risk
bullet to "block 4 does not gate the claims' assertions (B18); the diff reading
is the backstop"; fix the fixture doc comment. Pure text, no Verify command
changes, checkable by `grep -n`.

### Validation (independent re-run, not trusted from the analyst)

Disposable clones under
`/private/tmp/claude-501/-Users-feb-dev-cartridge-cartridge-ctg/3f0d518f-742b-4556-9a24-6c5fa6dd7524/scratchpad/reviewer-composed-6/`:
`base` = `git clone --local cartridge.ctg` at `d169293`; `ref` = same plus
`reference/{fixture.rs,mod.rs}` copied to
`.cartridge/tests/unit/src/tests/composed/` and `mod composed;` prepended to
`tests/mod.rs` (Steps 1–2). The four sh blocks were extracted verbatim from
the presented spec and each run with cwd = clone root as
`env -i PATH="$PATH" HOME="$HOME" sh -eu -c "<block>"`, serially.

| tree | b1 | b2 | b3 | b4 |
|---|---:|---:|---:|---:|
| base | **1** (16 s; census absent) | **1** (`test -f bodies`) | 0 | **1** (`test -f "$fix"`) |
| base + reference | **0** (15 s) | **0** | **0** | **0** (18 s) |

Matches the analyst's table; all under 120 s; no block `cd`s to an absolute
checkout; every cargo command has an isolated `CARGO_TARGET_DIR`. No Verify
block changed since round 5, so no gate regression. Host hygiene: `cartridge
daemon` processes 1 before / 1 after; `/tmp/cxv*` 0 after; live `cartridge.ctg`
never written. Cheats were not re-run: the gate is unchanged and B18 is a
recorded ceiling (no further gate round, per the Decision).

Findings and concrete revisions: **B19** partly resolved (box 4, ceiling
paragraph and backstop correct); **B20** (blocking — five residual sentences
plus the fixture doc comment still assert the refuted discrimination; fix
listed above); "one `assert_eq!` per claim" wording (non-blocking).
Disposition: **keep** plan and reference; finish the text correction.
Reviewer identity: reviewer-composed-6 (independent review sub-agent, Opus 5);
did not write the plan or the analyst edits.
User rating: not supplied; delegated.
User feedback/provenance: `prd.md` `## Decision (2026-09-19, coordinator
cartridge-ctg-cd)` — one more round, scoped to B19.
Result: **FAIL (89/100)** — one blocking finding.
Unresolved blocking findings: **B20** (residue of B19).
Recorded ceiling (not blocking, `review-plan.md` step 4): **B18**, unchanged.
Rounds used / remaining: none of rounds 1–5 was gate-only (each carried
non-gate revisions, e.g. round 5's B17 and F13), so all five count; this round
is the single additional round the Decision granted and it is not gate-only
either. **6 / 0** (5 of the original allowance + 1 of 1 granted).
Next action: **stop automatic revisions; return to the user/coordinator.** The
outstanding change is a text-only edit of the five sentences and one doc
comment listed under B20, no gate design, verifiable by `grep -n`; it needs a
user grant (or the coordinator's acceptance of that edit checked by diff)
before collect.

## Round 7 — 2026-09-19 — user-granted text-only round, scoped to B20 alone

Presented revision: the analyst's B20 text correction against `specs/spec01.md`
and the reference fixture's `receipt()` doc comment, against cartridge.ctg
`d169293` (`git -C cartridge.ctg rev-parse d1692932449c89106bb1928b717146ee8b0083a8`
resolves; unrelated to the live checkout's current HEAD, which carries an
unrelated peer session's dirty files). Scope per the coordinator's framing:
correct the six spans B20 named to the wording acceptance box 4 already uses,
then check only that no sentence anywhere still attributes the suite's
reddening under the mutant to the claims themselves. No gate redesign, no
re-derivation of B18, no new finding in B18's class.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `63a8a62035a8f152e0d2b3b25229b9aa3cb10c43c5831970ded983d600dedc79` (frontmatter gained `state: analyzing` and this session's `claim:` line since round 6; body unchanged) |
| Specs | `specs/spec01.md` — `2cdd67e46ed879407ad92e065ba7218ae8f0e936235bcd30b0270434256026f2` |
| Reference | `reference/fixture.rs` — `aa69cd624971c13c8d17b81216e154e7b0322b909a888306eb1bbebc0da8db89` (doc-comment edit only); `reference/mod.rs` — `379aa0c4f84b1aeb7dfa81042f392dbffdec782bedec7928b8c77bcb8c19a0a1` (byte-identical to round 5/6 — unchanged) |
| Material dependency | cartridge.ctg `d169293`; `review-plan.md` step 4 ceiling rule; round 6's B20 finding table |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Unchanged from rounds 5–6: one outcome, four bodies 1:1 onto the parent's four boxes. −2: the toy three-cartridge profile is not the real composition (disclaimed, unavoidable from the lane). |
| Ownership and reuse | 19 | Unchanged; reinstalled the preserved reference into a clean `d169293` worktree and it attached with no `src/` edit. −1: `CARGO_TARGET_DIR` outside the tree (justified, stated). |
| Dependencies and implementable slices | 19 | Unchanged; reference installed per Steps, green first time this round too. −1: `kache` as a stated but silent prerequisite of block 4's budget. |
| Observable acceptance and baseline evidence | 17 | **B20 is closed.** Read `specs/spec01.md` whole and grepped it for `because\|attribut\|objected\|went red\|why\|chooses nothing\|writes no such receipt\|short-circuit`: every hit left is either the already-correct disclaiming text (lines 57–63, 196–201, 336, 391, 456) or unrelated prose (`## Where the test lives, and why it is Rust`, `attribute from src/`, `settled must require state == "active", because…`, `# The mutant built and ran, and every one of the four objected` — a neutral census statement, not an attribution). The one remaining mutation-design sentence (lines 349–353, `assert_eq!(launches, 2)` "goes red — fast, because the body's wait loop breaks on `launches > 1`") describes why *this specific reference body's* assertion fails under the mutation, not a general claim that the gate can attribute red to a claim; it is not disputed by cheat I and is not part of B20's class. Re-ran the same grep over `reference/fixture.rs` and `reference/mod.rs`: no hit. The fixture's `receipt()` doc comment now reads "The body authors no field… supplies only its own label, and decides whether a `Lab` (and so a receipt) exists at all" — matches box 4's wording, no leftover "chooses NOTHING" claim. −3: the underlying ceiling itself (B18: block 4 does not gate which assertion inside a body went red; the backstop is a diff reading, not an automated per-claim gate) is now honestly and consistently stated everywhere, but it is still a real, if disclosed, coverage gap on three of the parent's four claims — matching round 5's own costing of this dimension at 16–17 once the overclaim is fully gone. |
| Failure, recovery and compatibility | 18 | Unchanged and re-verified: 1 `cartridge daemon` before this round's checks, 1 after (only the pre-existing project daemon); 0 `/tmp/cxv*` left after four fresh runs; no kill by name; no `pkill`/`killall` in fixture or bodies. −2: `/bin/sleep` orphans bounded (`peak ≥ 4`), not eliminated, same as every prior round. |
| Reviewer total | **91 / 100** | No unresolved blocking finding. |

### B20 — verdict: resolved

Round 6 found the refuted "the reddening is attributed to the claims" property
surviving in five spots of `specs/spec01.md` (lines 50, 305, 335–337, 390,
452–454) plus the `receipt()` doc comment in `reference/fixture.rs`. Reading the
presented `specs/spec01.md` line by line against round 6's table:

| B20 location | now reads | verdict |
| --- | --- | --- |
| line 50 | "Cheat H panics at its detector before any `Lab` exists, so no `Drop` runs and no receipt directory is created at all" | the false sentence above it is deleted; what remains is true and non-attributing |
| 304–305 (block 2 comment) | "so no body authors a field; it supplies the label and decides whether a `Lab` (and so a receipt) exists" | matches the recommended fix verbatim |
| 334–337 (block 4 preamble comment) | "the fixture measured a whole composition whose node identity the mutation broke; why the body went red is not recorded (B18)" | disclaims attribution explicitly |
| 390–391 (block 4 post-census comment) | same sentence, repeated at the second site | disclaims attribution explicitly |
| 452–454 (Remaining risk) | "Block 4 does not gate the claims' own assertions (B18). It rejects a body that panics before a `Lab` exists or fails the tree's own `0 passed, 4 failed` census; it does not record which assertion inside a body went red." | disclaims attribution explicitly, names the diff-reading backstop |
| `reference/fixture.rs` `receipt()` doc comment | "The body authors no field — not a number, not a count… The body supplies only its own label, and decides whether a `Lab` (and so a receipt) exists at all." | matches box 4's wording; the false "chooses NOTHING" line is gone |

I independently swept both files for the same class of claim with a fresh
regex (`because|attribut|objected|went red|why|chooses nothing|writes no such
receipt|short-circuit`) rather than trusting the analyst's six-item list, and
found no further hit that attributes the mutant's reddening to the claims
themselves. **B20 is resolved.**

### Negative confirmation: only text moved

`git diff` in `prd.ctg` over this PRD's directory shows exactly two files
changed since the last commit (`4e543acc`): `prd.md` (frontmatter `state` and
`claim` only — this review session's own claim, not a content edit) and
`specs/spec01.md` (five hunks, all inside prose or `#`-prefixed shell
comments; every non-comment line of all four `## Verify` fenced blocks is
byte-identical to round 6). The Acceptance section (lines 182–206) has no hunk
touching it and its frontmatter (lines 1–7, `footprint:` unchanged) has no
hunk either. `reference/mod.rs`'s digest is unchanged from round 5/6;
`reference/fixture.rs` changed only in the `receipt()` doc comment (confirmed
by reading the diff region directly, since the file is gitignored and
untracked).

### Re-run of all four Verify blocks (not required by scope, done as a sanity check on the doc-comment edit)

The scope only asks for a text sweep, but a doc-comment edit inside a `.rs`
file can, in principle, change `rustfmt`'s verdict, so I re-ran all four
blocks verbatim in a disposable detached worktree of `d169293`
(`/tmp/cxr7-cartridge`, removed and pruned afterward) with the corrected
`reference/{fixture.rs,mod.rs}` installed per Steps 1–2:

| block | result |
| --- | --- |
| 1 (nextest, receipts) | exit 0 — `Starting 4 tests` / `4 tests run: 4 passed`, all receipt/claim greps passed |
| 2 (static guards) | exit 0 |
| 3 (`cargo fmt --all --check`) | exit 0 — the doc-comment rewrap did not disturb formatting |
| 4 (mutant) | exit 0 — `4 tests run: 0 passed, 4 failed`, four receipts, `compositions=1 nodes=3` ×4, `probe_node=differs` ×4, `run_node=differs` ×4 |

Identical to round 6's and round 5's results. No gate regression; B18 is
unchanged as a recorded ceiling and was not re-attacked.

Findings and concrete revisions: none open. B20 resolved; B18 remains the
recorded ceiling per `review-plan.md` step 4, unchanged since round 5.
Disposition: **keep** — the plan, spec and reference implementation pass.
Validation: cwd `/tmp/cxr7-cartridge` (detached worktree of `d169293` created
via `git -C cartridge.ctg worktree add --detach`, cleaned with `git checkout`
of the one edited tracked file, removal of the untracked `composed/` dir added
for the test, then `git worktree remove` and `git worktree prune`; `git -C
cartridge.ctg worktree list` back to its original two entries; `git -C prd.ctg
status --porcelain` over the PRD directory shows only the two expected dirty
files). `CARGO_TARGET_DIR` set to scratch paths outside every repository for
every cargo invocation. Host hygiene: `cartridge daemon` census unchanged
(1 pre-existing daemon, pid 22955, untouched); 0 `/tmp/cxv*` directories left;
no `pkill`/`killall` issued.
Reviewer identity: independent reviewer subagent, round 7 (did not write the
plan, the analyst's B20 edit, or any earlier round's text).
User rating: not supplied; delegated.
User feedback/provenance: coordinator instruction, 2026-09-19, granting one
text-only round scoped to correcting B20's six spans and checking only that no
sentence still attributes the mutant's reddening to the claims.
Result: **PASS (91/100)** — no unresolved blocking finding.
Unresolved blocking findings: none.
Recorded ceiling (not blocking, `review-plan.md` step 4): **B18**, unchanged —
block 4 rejects a body that panics before a `Lab` exists or fails the plain
`0 passed, 4 failed` census, but does not record which assertion inside a body
went red; the backstop is the diff reading of `reference/mod.rs`'s four
`assert_eq!`s per claim.
Rounds used / remaining: **7 used** (5 of the original allowance, 1 of 1
granted after round 5, 1 of 1 granted after round 6); the plan has passed, so
no further rounds are needed.
Next action: **proceed to implementation/collect.** Copy the preserved
`reference/{fixture.rs,mod.rs}` per the spec's Steps, run the four Verify
blocks in the lane and then in `repo`, and collect.
