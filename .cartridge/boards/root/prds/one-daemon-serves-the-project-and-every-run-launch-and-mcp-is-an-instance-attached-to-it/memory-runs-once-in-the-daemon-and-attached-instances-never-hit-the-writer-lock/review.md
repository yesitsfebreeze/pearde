# memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock review history

Plan: `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock`,
`prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock/prd.md`.
Scope: executable leaf. One observable outcome — memory.ctg's provable share of "memory is composed
exactly once and the attached shape never takes the writer lock". Accountable cartridge: memory.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: prd.ctg `4a13f56c` (working tree dirty; this PRD's `prd.md`, `specs/spec01.md`
and `analyst-1.md` are untracked/modified planning records). Spec base memory.ctg `5097a83`
("Keep every Vamana node reachable: prune over one occlusion factor"), working tree **clean** —
confirmed, so the spec's declared base is the live base.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../memory-runs-once.../prd.md` — `e4d05d3b266fb94fde5f899b444e03af39a74b5ff318c63c7e47f2aa29baa044` |
| Specs | `specs/spec01.md` — `f6ef69248d6f33c10fbbc236fe2dd4313391239c452b601ddb4cc5d1973c79e4` |
| Analyst record | `analyst-1.md` — `7a7fad46af69a7f931ef731e4f028836d6c37dee4643618d70f2c8bbff755298` |
| Prototype | `.state/loop/.../attempt-1.patch` — `fdedfa658954e40322f59e145561e2b53aac088c1b0c430855804568ef534fdf` |
| Material contracts/dependencies | memory.ctg `5097a83`: `src/commands/src/memory.rs` `8718858917…`, `src/cartridge/src/lib.rs` `5a60d987e8…`, `src/store/core/src/lock.rs` `669a725c6f…`. Sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently` state `done`; `the-composed-acceptance-test-…` state `open`; precedent sibling `agent-runs-key-per-attached-instance-not-per-process` `f7c38fe`. |

### Independent re-verification of the premise

Both halves were re-checked against the live checkout, not taken from the analyst.

- **Held.** `LockError::Held` prints exactly `another memory writer holds this data dir`
  (`src/store/core/src/lock.rs`, `Display` impl; with a holder it appends ` (<holder>)`), and only
  `TryLockError::WouldBlock` maps to it — `Error(e)` stays `LockError::Io`. `acquire` is at `:99`,
  takes one flock on `<data_dir>/writer.lock`, and `try_lock_patiently` retries a bounded
  `PATIENCE = 100ms`. `Engine::open` acquires it as `"cartridge memory"` at
  `src/commands/src/memory.rs:14-15` and parks it in `Engine._writer` (`:5-9`), documented as held
  through process teardown.
- **Already false, as the Planning note says.** `ServiceConfig::Attached`
  (`src/cartridge/src/lib.rs:23-29`) is selected only when `owner` is a non-null table
  (`:31-40`), and the attached branch returns at `:300-312` through
  `memory_transport::owner::read_observed` — textually before the `ServiceConfig::Local(cfg) = cfg
  else { unreachable!() }` line and before any `status.engine.get_or_try_init`. The status probe
  takes the same early branch (`src/cartridge/src/status.rs:208-224`); only the `Local` arm reaches
  `store::lock::observe` (`:245`), and only when the engine is not yet open. Nothing on the attached
  path touches `store::lock`. The PRD's escape hatch was genuinely empty.

Conclusion "no production change, one regression test" rests on two verified halves. Accepted.

### Condensing-loop ownership

Confirmed structurally, not on assertion: `grep -rn spawn_ledger src --include=*.rs` returns exactly
two hits in one file — the definition `src/commands/src/memory.rs:59` and the single call
`src/commands/src/memory.rs:44`, the last statement of `Engine::open` after the lock. `ledger_pass`
has exactly two callers: the 60s/900s loop inside `spawn_ledger` (`:69`) and the explicit
`Some("rollover")` op (`src/rpc/src/ledger.rs:734`), which is operator-triggered, not a scheduler.
So `spawn_ledger` is the repo's only rollover scheduler and has one call site; a service refused the
lock gets `Err` from `Engine::open`, no `Engine`, and therefore no pass. Claim accepted.

### Non-vacuity — reproduced, and one analyst row corrected

Lane: `git clone --shared` of memory.ctg at `5097a83` into the scratchpad (chosen over
`git worktree add` so the live checkout's `.git` is never written), isolated `CARGO_TARGET_DIR`,
scratch `CARTRIDGE_HOME`, every store a `tempfile::tempdir()`. The live project daemon was never
started, stopped, replaced, reloaded or called; no memory call ran against a live store.

- **R2 (`Engine::open` locks a per-pid subdir) — reproduced exactly.** FAILED at
  `engine_test.rs:179`, `assertion left == right failed: and holds the writer for its lifetime,
  left: Missing, right: Held`. Reverted; `git diff --stat` back to the one test file.
- **R1 (`service_configuration` always `Local`) — reproduced, but it does not fail where the
  analyst reported.** Flipping the branch condition so the `owner` table reaches `configuration`
  fails at `engine_test.rs:214`: `an attached configuration: "unknown memory config field: owner"`.
  Line `:214` is `.expect("an attached configuration")`; the assertion the analyst quotes,
  `"attached memory must not reach for the writer lock"`, is at `:220`. Analyst row 5 pairs the
  line number of one panic with the message of another, so the load-bearing attached assertion was
  never actually shown to fire.
- **R1b (faithful variant, built by this reviewer) — the load-bearing assertion does fire.**
  `service_configuration` strips `owner` and returns a real `Local` config over the same dir, i.e.
  attached memory silently falls back to a local engine. FAILED at `engine_test.rs:220`:
  `attached memory must not reach for the writer lock: another memory writer holds this data dir
  (cartridge memory pid 19913)`. Reverted.

Non-vacuity is therefore **established, and more strongly than the analyst established it** — R1b is
the exact regression the outcome exists to prevent. The defect is in the analyst's evidence table,
not in the test.

Coverage is also new, not duplicated: `another memory writer` appears **nowhere** under
`.cartridge/tests`, so no existing test pins the refusal at the service level. `lock_test.rs` and
`commands_writer_boundary_test.rs` both exist as the spec describes and pin the primitive and the
two-process boundary, not this property.

### Baseline — confirmed independently, and it has two modes, not one

`cargo test -p memory_cartridge --lib` at `5097a83` **unpatched**, 4 runs: exit 101 every time,
`19 passed; 1 failed` every time. But the failing test is not stable:

- 3 of 4 runs: `engine_tests::health_overtakes_blocked_ingestion_and_dispose_drains_it` fails
  **itself**, `panicked at engine_test.rs:137: health is independent of ingestion: Elapsed(())`.
- 1 of 4 runs: a sibling fails —
  `engine_tests::ingest_query_tool_and_context_reach_one_engine`, `called Result::unwrap() on an Err
  value: "shutting down: the daemon refused this request, retry against a fresh one"`.

The spec and analyst describe only the second mode. The count is stable, so the 19/1 → 20/1
comparison the spec rests on is sound and I confirmed it: **patched, 5 runs, exit 101 and
`20 passed; 1 failed` every time**, the new test never the victim. The characterization of the
*mechanism* is incomplete, and it matters because the deferral PRD
`@memory/the-memory-engine-tests-do-not-depend-on-which-test-ran-before-them` is framed purely as
test ordering, while the more frequent mode is that test timing out on its own.

**The `drop(owner)` workaround is honest.** It avoids *causing* the known process-wide
`util::lifecycle::SHUTTING_DOWN` bug rather than concealing it, says so in a code comment and in
Remaining risk, and names the separate PRD. It is also load-bearing in the right direction: dropping
the last `Arc<Tracker>` drops the `OnceCell<Engine>` and so the `_writer`, which is exactly what the
preceding `observe(&dir) == Held` assertions are asserting is still true. The drain/dispose path it
skips is already covered by `health_overtakes_blocked_ingestion_and_dispose_drains_it`. Naming the
single test in Verify is the correct response to a red package baseline, not a dodge.

### Footprint

Correct. `git apply` of `attempt-1.patch` leaves `git status --porcelain` showing exactly
` M .cartridge/tests/unit/src/cartridge/engine_test.rs` — one file, and it is in the footprint. The
`#[path]` include is real (`src/cartridge/src/lib.rs:581`), so the coordinator's addition was
required and the trap was correctly recognised from the agent sibling. Dropping the non-existent
`src/store/lock.rs` was right; the real file is `src/store/core/src/lock.rs`, already under `src/`.
Keeping the broad `src/` entry matches the done sibling `agent-runs-key-per-attached-instance-…`
(`src/` + one test path) and is needed if a later spec on this PRD touches production code; the
spec's step 2 ("Nothing else. No change under `src/`") is the guard against a stray in-footprint
edit being swept into the receipt. Nothing the spec touches is outside the footprint, and nothing
in the footprint is touched that shouldn't be. Writes made by the Verify blocks land outside the
repo (`../memo.ctg`) or in gitignored `/target`, so neither pollutes a collect.

`CARGO_TARGET_DIR` is pinned to `$PWD/target/memory-one-writer-verify`, distinct from the
`target/debug` artifacts a live daemon loads — so collect pass 2 in the real submodule cannot
hot-restart a live cartridge. This is the one thing the verify-block rule most cares about and the
spec gets it right in both cargo blocks.

### Operational warning observed mid-review — read before collecting

The live `memory.ctg` checkout was **clean at `5097a83`** when this review started and went dirty at
13:11, during it, from a concurrent session:

```
 M src/cartridge/Cargo.toml        (removes `evidence = { path = "../../../memo.ctg/evidence" }`)
 M src/cartridge/src/source.rs
?? src/cartridge/src/evidence.rs   (untracked; the dependency being vendored in)
```

Two consequences, neither a defect in this plan:

1. **Do not collect this PRD while those paths are dirty.** `src/` is in this PRD's footprint and a
   collect commits every changed in-footprint path, so a receipt taken now would sweep another
   session's in-progress vendoring into this child's commit. Check `git -C memory.ctg status` before
   the collect and coordinate with whoever owns that change. This is the concrete form of the risk
   behind keeping a broad `src/` entry on a child whose spec changes nothing under it.
2. **That change, if it lands, obsoletes Verify block 1's symlink line entirely.** Its whole
   justification is `src/cartridge/Cargo.toml:13` reaching `../../../memo.ctg/evidence`; the
   concurrent diff deletes exactly that line. Finding 5 below should then be applied as a plain
   deletion rather than a rewrite — and the spec's base (`5097a83`) will need re-confirming if the
   vendoring commits first, since it touches the crate this test compiles into.

HEAD is still `5097a83`, so the revision binding of this review stands as recorded.

### The three reworded acceptance boxes

- **Box 1 — right call, not hollowed out.** The original needed a live daemon, `cartridge run` and a
  process count, none of them observable from memory.ctg. The rewording keeps three falsifiable
  clauses (lock taken once in `Engine::open` and held for the node's lifetime; a second local
  service refused with that exact message and opening no engine; the attached shape never asking),
  and the test proves all three. The delegation is to a sibling I confirmed is actually `state:
  "done"`, not to a promise, plus the `open` composed test for the daemon-wide re-proof. This is
  memory.ctg's real share.
- **Box 2 — acceptable, with one clause the test does not exercise.** Under the attach contract the
  original round trip really is cartridge.ctg event routing, so delegating it is correct. But the
  reworded box says the writer serves "ingest, query and ledger from a single `Engine`", and the
  test calls only `ingest` and `ledger status` on the owner — the sole `query` goes to the attached
  service and is expected to error. The claim is true and covered by the sibling test
  `ingest_query_tool_and_context_reach_one_engine`, but this spec's own test does not carry it. A
  four-line `call(&owner, json!({"op":"query","q":"Cedar"}))` asserting Cedar comes back would close
  the gap and would additionally prove the ingested content is readable from the one engine.
- **Box 3 — the right call, said plainly.** The literal wording is confirmed unsatisfiable:
  `ledger::status` (`src/rpc/src/ledger.rs:289-297`) builds a map of `{rows, bytes}` per tier over
  `["raw","part","day","week","month","year"]` and nothing else — no pid, no node, no owner. Making
  it answerable is a production change this child's body explicitly scopes out, and I agree with
  dropping it rather than smuggling a feature into a verification child. The rewording is also the
  *stronger* property: structural ownership ("only `Engine::open` can start a pass") cannot be
  violated without the test failing, whereas a status field would only report after the fact. If an
  operator-visible "who is condensing" is wanted, its own PRD is the right home, and `pid` is the
  wrong field for it anyway once attach is in force — the useful identity is the owner endpoint.
  Recorded so a later reader does not mistake the rewording for a narrowing to nothing.

### Scores

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Outcome is real and correctly narrowed to what this repo can prove; the "no production change" conclusion is re-verified from source, not accepted. −1: the PRD body's bullet "verify a short-lived attached `run`/`call` does not start or interfere with [the condensing loop]" is answered structurally (an attached service opens no engine) but never dispositioned in the Planning note the way the three acceptance boxes were, so a reader cannot tell whether the lifecycle half was delegated or judged moot. |
| Ownership and reuse | 20 | Correct owner (memory), correct base, `needs` resolves to a `done` sibling. The test reuses the file's existing `settings`/`service_for`/`call` helpers and `test_support::spawn_http` rather than inventing fixtures; the spec forbids touching `src/`. No duplication — `another memory writer` appears nowhere under `.cartridge/tests`, so this is genuinely uncovered ground, and the shape matches the done precedent `f7c38fe`. |
| Dependencies and implementable slices | 19 | One file, ~90 lines, `git apply --check` exit 0, one coherent slice with no ordering hazard; the two delegations name a done sibling and an open composed test explicitly. −1: Verify block 1 bakes the absolute developer path `/Users/feb/dev/cartridge/memo.ctg` into the durable record as `MEMO_CTG`'s default and `ln -sfn` will happily create a **dangling** symlink anywhere that path is absent, surfacing as a confusing cargo manifest error rather than "this lane has no siblings". Lane sibling seeding belongs to the lane, not to a Verify block; the spec's own Remaining risk concedes this. |
| Observable acceptance and baseline evidence | 16 | All three blocks pass verbatim on the patched lane and the two regressions fail it. −2: analyst row 5's non-vacuity evidence is mislabeled (line `:214` = `.expect("an attached configuration")`, message quoted from `:220`); I reproduced the analyst's R1 and got the `:214` config-validation panic, so the attached assertion was accepted on evidence that did not demonstrate it — resolved only by my R1b. −1: **Verify block 1 is vacuous on its own** — run verbatim on the *unpatched* lane it exits 0 with `running 0 tests … 20 filtered out`, so a filter typo or an `#[ignore]` leaves it green with the test never running; block 2's name grep catches deletion but not either of those. −1: block 2's `test "$(grep -rl spawn_ledger src --include=*.rs \| wc -l)" = 1` counts **files**, not call sites, while box 3 asserts "called from exactly one place" — a second `spawn_ledger(…)` added inside `memory.rs` passes it. −1: box 2's "query" clause is not exercised by this test (see above). |
| Failure, recovery and compatibility | 18 | The red baseline is disclosed, quantified and worked around correctly, and the `drop(owner)` choice is honest — it declines to add a second `SHUTTING_DOWN` setter, documents why in the code and the record, and defers the real fix to a named PRD. Attached-leg limitation (dead endpoint pins which error, not a working owner read) is disclosed. `CARGO_TARGET_DIR` pinning keeps collect pass 2 off live artifacts. −2: the baseline mechanism is described as one mode when it is two — in 3 of 4 unpatched runs `health_overtakes_blocked_ingestion_and_dispose_drains_it` fails itself with `Elapsed(())` at `:137` rather than stranding a successor, which the deferral PRD's ordering framing does not cover. |
| Reviewer total | **92** / 100 | ≥ 90 and no blocking finding. |

Findings and concrete revisions (all non-blocking; recommended for the implementing worker):

1. *Analyst evidence row 5 is mislabeled* (`analyst-1.md`). Evidence: my reproduction of the
   analyst's R1 panics at `:214` with `"unknown memory config field: owner"`, not at `:220`.
   Recommendation: record R1b (strip `owner`, return a real `Local`) as the non-vacuity proof for
   the attached leg — it fails at `:220` with `another memory writer holds this data dir (cartridge
   memory pid …)`. Resolution: established by this review; the spec needs no change.
2. *Verify block 1 passes with zero tests run.* Evidence: verbatim on the unpatched lane, exit 0,
   `running 0 tests`. Recommendation: one line — append `-- --exact` and assert the summary, e.g.
   pipe to `grep -q '1 passed'`, so a renamed/ignored test cannot be silently green.
3. *Block 2's `spawn_ledger` check counts files, not call sites.* Recommendation: count the call
   instead, e.g. `test "$(grep -rc 'spawn_ledger(&server)' src --include=*.rs | grep -v ':0$' | wc -l
   | tr -d ' ')" = 1`, or assert the call sits inside `Engine::open`.
4. *Box 2 claims a `query` the test does not make.* Recommendation: add
   `call(&owner, json!({"op":"query","q":"Cedar"}))` and assert Cedar is returned (~4 lines), or
   drop "query" from the box's wording.
5. *`MEMO_CTG`'s absolute default.* Recommendation: prefer a lane that already seeds `*.ctg`
   siblings and drop the line; failing that, fail loudly when `../memo.ctg` is absent instead of
   creating a possibly-dangling link.
6. *Residual, no action:* the new test can itself become the `SHUTTING_DOWN` victim in a
   package-wide run. It was not in 5 of 5 patched runs, and Verify names the single test, so the
   gate is unaffected. Folded into the existing deferral PRD.
7. *Operational, not a plan defect — action required before collect.* The live `memory.ctg` went
   dirty under `src/cartridge/` at 13:11 from a concurrent session (see the warning section above).
   Because `src/` is in the footprint, check `git -C memory.ctg status` before collecting, or that
   foreign work lands in this child's receipt.

Disposition: **keep**. Implement spec01 as written, ideally with findings 2–4 folded in.

Validation (all in an isolated lane; the live project daemon was never started, stopped, replaced,
reloaded or called, and no memory call ran against a live store):

| # | command | cwd | exit |
| --- | --- | --- | --- |
| 1 | `git clone --shared --no-checkout /Users/feb/dev/cartridge/memory.ctg <scratch>/lane/memory.ctg` + `git checkout --detach 5097a83` | scratchpad | 0 (clean tree at `5097a83`) |
| 2 | Verify block 1 verbatim, `sh -eu -c`, **unpatched**, cold `CARGO_TARGET_DIR` | lane | **0**, `running 0 tests … 20 filtered out`, 23 s cold (limit 120 s) |
| 3 | `cargo test -p memory_cartridge --lib` **baseline**, ×4 | lane | **101** each, `19 passed; 1 failed` each; 3× victim `health_overtakes…` (`Elapsed(())` at `:137`), 1× victim `ingest_query_tool_and_context_reach_one_engine` (`shutting down: …`) |
| 4 | `git apply --check attempt-1.patch` then `git apply` | lane | 0 / 0; ` M .cartridge/tests/unit/src/cartridge/engine_test.rs` only |
| 5 | Verify block 1 verbatim, `sh -eu -c` | lane | **0**, `1 passed`, 2 s warm |
| 6 | Verify block 2 verbatim, `sh -eu -c` | lane | **0**, <1 s |
| 7 | Verify block 3 verbatim (`cargo fmt --check`), `sh -eu -c` | lane | **0**, <1 s |
| 8 | `cargo test -p memory_cartridge --lib` **patched**, ×5 | lane | **101** each, `20 passed; 1 failed` each; new test never the victim |
| 9 | regression **R2** (`Engine::open` locks `<data_dir>/pid-<pid>`), then revert | lane | test **FAILED** at `engine_test.rs:179` `"and holds the writer for its lifetime" left: Missing right: Held`; reverted |
| 10 | regression **R1** (analyst's, `service_configuration` always `Local`), then revert | lane | test **FAILED** at `engine_test.rs:214` `an attached configuration: "unknown memory config field: owner"` — *not* the assertion the analyst reported; reverted |
| 11 | regression **R1b** (strip `owner`, return a real `Local`), then revert | lane | test **FAILED** at `engine_test.rs:220` `attached memory must not reach for the writer lock: another memory writer holds this data dir (cartridge memory pid 19913)`; reverted |
| 12 | `grep -rn spawn_ledger \| ledger_pass src --include=*.rs` | live memory.ctg (read-only) | 0 — `spawn_ledger` defined `memory.rs:59`, called once `memory.rs:44`; `ledger_pass` called from the loop `:69` and the explicit `rollover` op `ledger.rs:734` |
| 13 | `grep -rn "another memory writer" .cartridge/tests` | live memory.ctg (read-only) | 1 — no matches; coverage is new |

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS (92/100)**.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed to implementation of `specs/spec01.md`, folding in findings 2–4 (three one-to-four-line
edits) if the worker can do so without touching `src/`; before collecting, confirm the live
`memory.ctg` has no foreign dirty paths under `src/` (finding 7).
