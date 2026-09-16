# @root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/agent-runs-key-per-attached-instance-not-per-process review history

Plan: `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/agent-runs-key-per-attached-instance-not-per-process`, source `prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/agent-runs-key-per-attached-instance-not-per-process/prd.md`. Owner repo `agent.ctg`, capability-owner `agent`, priority 80.
Scope: executable leaf. One observable outcome — agent runs are keyed per attached instance (per session), so two attached instances never serialize onto one guard or overwrite one transcript.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none. This slug has no prior canonical ID; it was created by `prd refine` from the parent rollup on 2026-09-15 and carries no used rounds.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: `prd.ctg` at `0f32da2e37ef371849c0f785907e867de91b671e` with the plan dirty in the working tree (`M .../agent-runs-key-per-attached-instance-not-per-process/prd.md`, `?? .../specs/`); target repo `agent.ctg` at `4e544f2e0960978ab8e6bacb936917db9b318775` ("Give the loop tests their own CARTRIDGE_HOME"), working tree clean.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../agent-runs-key-per-attached-instance-not-per-process/prd.md` — SHA-256 `f25b80da5044e0d34b93cfc62d27e85a0e0ff10714c09e3b7a0ed96854a912c2` |
| Specs | `specs/spec01.md` — SHA-256 `0560f901dd8482d73d1b618cc8a38a2d730f01bee1dfc734620dd5e6c04cd4b7` |
| Prototype | `.state/loop/.../attempt-1.patch` — SHA-256 `9319836bbac4f31c27dc3072328f21e7985275988c66d337b38541a3583aaa89` |
| Analyst report | `.state/loop/.../analyst-1.md` — SHA-256 `ea16e24ececd08aca37a62f9f53f7d2960af61007faf9c3978f6c80d457e4e26` |
| Material contracts/dependencies | `agent.ctg/src/lib.rs` @4e544f2 — SHA-256 `aec999dabf369bfb7b64e87163ff4447af2c86ab54400383098529b2fc367c40`; `agent.ctg/.cartridge/tests/unit/run_state.rs` @4e544f2 — SHA-256 `89106ff239c1848c5778774e19e177a1b8ed3d30fa099d64af5f1127ffb3fecc`; parent rollup `prd.md` — SHA-256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445`; `needs` sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently` — `state: "done"`, `commit: f364f46f77c2f84345fe4cc5850c6182c0754568`; `prd.ctg/.cartridge/templates/spec.md` (Verify engine facts) |

### The load-bearing claim, re-derived independently

The plan's central claim is that the parent audit's premise was wrong — agent's single-flight guard was never node-wide. I re-derived every cited line against `agent.ctg` @4e544f2 rather than accepting the analyst's trace. **The claim is correct.**

| Claim | Verified at | Observed |
| --- | --- | --- |
| The guard map is keyed by session id | `src/lib.rs:169` | `runs: Mutex<HashMap<String, Arc<Control>>>`; inserted as `runs.insert(id.clone(), control.clone())` where `id` is the session (`src/lib.rs:289`) |
| `start` refuses only for the same session | `src/lib.rs:283-288` | `if runs.get(&id).is_some_and(\|c\| !c.live.lock().unwrap().finished) { return Err("run_active") }` — a lookup by that one key, never a scan |
| Every other op resolves by session, no ambient run | `src/lib.rs:348-357` | `Agent::control` takes `string(args, "session")`, looks it up, then requires `args["run"]` to equal that control's own `snapshot["run"]`, else `run mismatch`. `status`/`answer`/`cancel` all route here |
| The transcript is sessions-owned under CAS, not node state | `src/lib.rs:526-546` | `Run::save` → `sessions {"op":"checkpoint","id": self.session, "expected_revision": self.revision, …}` |
| The run id derives from the session's own revision | `src/lib.rs:293-300` | `format!("{id}:{}", revision + 1)` |
| `Run::new` takes cwd from the session record, not the process | `src/lib.rs:489` | `cwd: string(saved, "cwd")?.into()` |
| **No node-wide lock or ambient "current run" exists anywhere in `agent.ctg/src`** | exhaustive grep for `static`/`lazy_static`/`OnceCell`/`OnceLock`/`thread_local` over `src/` | Five hits only: `stream.rs:14` HTTP `CLIENT`, `sse.rs:20` `LIMIT`, `base.rs:18` `RUNTIME`, `base.rs:32` `ENTERED`, and `module.rs:23-27` (`AGENT`, relay `PIPE`, `PENDING` asks keyed by `NEXT: AtomicU64`). **None holds a run, a session or a lock over runs.** Confirmed. |
| `Agent::recover` is the real many-node symptom, called once per node start | `src/lib.rs:219-237`, called from `src/module.rs:85` (`base::runtime().block_on(agent.recover())`, immediately before `AGENT.set`) | It lists sessions, and for every session whose `agent.phase` is unfinished builds a `Run` and `finish("interrupted", "unfinished run recovered; tool outcome unknown")`. With N nodes each node clobbers the others' live sessions; with one daemon it runs once and is a truthful restart marker. Confirmed, and the `needs` sibling that delivers one daemon is `state: "done"` at `f364f46`. |
| The existing test exercises only ONE session | `.cartridge/tests/unit/run_state.rs:293-329` | `concurrent_starts_produce_one_run_one_error_one_checkpoint_pair` binds `first`/`second` both to `json!({"session":"s1", …})`, `tokio::join!`s them and asserts one winner and one `run_active` **refusal**. It asserts the guard *fires*; nothing in the suite asserts two sessions may both run. Confirmed. |
| agent.ctg starts no host, node or child process | `grep -rn 'Command::new\|std::process\|cartridge daemon' src/` → exit 1, no hits | Independently corroborated: `Cargo.toml` enables tokio features `rt-multi-thread, macros, sync, time` — **not** `process`, so `tokio::process` is not even compiled in; no dependency is a process spawner (mlua, tokio, serde, serde_json, futures, reqwest, sha2); `build.rs` uses no process API; `init.lua` only loads the module, opens a pipe and listens. Confirmed. |

### The decisive check: is the new test vacuous?

A test that passes against unmodified `src/` proves nothing unless it also fails when the behavior regresses. I injected the exact regression the PRD names and measured.

**Regression A — node-wide single-flight lock.** In a scratch worktree I changed `src/lib.rs:283-288` from the per-session lookup to a node-wide scan:

```rust
if runs.values().any(|c| !c.live.lock().unwrap().finished) { return Err("run_active".into()); }
```

Result: `test result: FAILED. 13 passed; 1 failed`. The **only** failing test was `two_sessions_hold_concurrent_runs_with_separate_transcripts`, panicking at `run_state.rs:831` (the `b.expect("s2 start")` unwrap). Every pre-existing test, including `concurrent_starts_produce_one_run_one_error_one_checkpoint_pair`, still passed.

This is the strongest evidence in the review and it lands on both halves of the plan's argument at once: the new test is **not** vacuous (it is the one thing standing between the repo and a node-wide lock), and the claimed baseline gap is **real** (the suite as it stands would ship that regression green).

**Regression B — ambient "current run".** Changing `Agent::control` (`src/lib.rs:348-357`) to ignore the session key and return the first unfinished control failed 10 of 14 tests, including the new one. That regression class is already densely covered; the new test adds to it without being the sole guard. Both injections were reverted and the worktree verified clean before removal.

### The two coordinator amendments

**Footprint gained `.cartridge/tests/unit/run_state.rs` — sound and necessary.** Verified at `src/lib.rs:894-896`: `#[cfg(test)] #[path = "../.cartridge/tests/unit/run_state.rs"] mod run_state;`. This repo keeps its unit tests outside `src/` by convention and `#[path]`-includes them, so the spec's only changed file genuinely sat outside the declared `src/` footprint. Without the amendment collect would have refused the write. The amendment is minimal — the one file, not the whole `.cartridge/tests/` tree.

**Acceptance box 3 narrowed to agent.ctg's provable share — sound.** The original box ("exactly one agent node with the daemon running") is not observable from this repo without a live daemon, which is forbidden here. The narrowing is honest in both directions: it keeps the daemon-wide count attributed to the `done` sibling and to the composed test, and it states agent.ctg's actual contribution ("starts no host, node or child process"), which Verify block 3 does prove and which I corroborated independently above. It narrows the claim, not the truth.

### Acceptance provability

| Box | Where proven | Provable by a Verify block? |
| --- | --- | --- |
| PRD 1 / spec 1 — two instances each hold an active run, neither refused | new test: both `start`s `expect` Ok, runs `s1:1`/`s2:1`, both `wait_phase` to `running` | Yes — block 1 `cargo test --lib run_state`; block 3 additionally greps that the test exists and drives `"session":"s2"`, so it cannot be silently deleted |
| PRD 2 / spec 2 — resuming never reads or writes the other's transcript or session | cross-session `status` both directions assert `run mismatch`; cancel s1 leaves s2 `running`; each transcript contains only its own prompt and exactly one `run_started`/`run_finished` | Yes — block 1 |
| PRD 3 / spec 3 — agent.ctg's share of the one-node count | `! grep -rn 'Command::new\|std::process\|cartridge daemon' src/` | Yes — block 3, and I corroborated it beyond the grep (tokio `process` feature absent, no spawner dependency, `build.rs` and `init.lua` clean) |

Every box in both records is reachable from a Verify block. No box is asserted without a check.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One observable outcome, one accountable cartridge, three acceptance boxes, body ~330 words — inside the 150–300/400 guidance. The real value is that the plan refuted its own parent's premise and recorded the refutation in `What changes` instead of quietly shipping a no-op diff to look productive; that is the behaviour the method wants. The remaining value — the regression pin — is not ceremonial: I proved by injection that it is the sole guard against the exact regression the PRD names. **−1**: the title and `Outcome` still read as end-state assertions of per-instance keying, so a reader who stops before `What changes` expects production work. The first sentence of `What changes` corrects it, which is why this is one point and not more. |
| Ownership and reuse | 19 | `repo: agent.ctg` matches the code; the footprint now covers the only changed path. The plan climbs the right rung: it explicitly rejects introducing an instance id above the session as "a second name for the same thing", which is correct — the session already is that key, per the trace above. The test reuses the file's existing `Fakes` (`run_state.rs:14`), `call_fn` (`:60`), `fast` (`:239`), `wait_phase` (`:248`) and `count_kind` (`:264`) and adds no fixture module. Out-of-footprint work (`agent.event` node-wide fan-out, `src/lib.rs:549-556`) is handed up to cartridge.ctg event routing rather than absorbed. **−1**, two small nits: the new driver duplicates the existing `concurrent_starts_…` driver shape with an `AtomicBool` instead of the file's `Notify` (justified — a cancelled run parked on `Notify` never wakes — but left as two near-identical closures with no shared helper); and Verify block 3's `grep -q 'runs: Mutex<HashMap<String, Arc<Control>>>' src/lib.rs` is a brittle textual pin on a declaration that `rustfmt` or a type alias would break with a confusing failure, and that the behavioural test already covers. |
| Dependencies and implementable slices | 19 | `needs` names exactly one edge and it is the right one: I confirmed `Agent::recover` (`src/lib.rs:219-237` ← `src/module.rs:85`) is the real many-node clobber, and that the sibling which removes it is `state: "done"` at `f364f46`. One slice, one spec, `complexity: small`, 72 added lines in one file, no hidden ordering, nothing blocked behind an open sibling. **−1**, advisory: acceptance box 1 holds only if two instances receive distinct session ids. The spec defers that to the **open** sibling `sessions-runs-once-in-the-daemon-with-one-buffer-id-space` under `Remaining risk`, but neither record argues why no `needs` edge is required. I checked and the deferral is correct — `sessions.ctg/src/lib.rs:654-665` mints ids from `UNIX_EPOCH.elapsed()` nanos plus a process-wide `UNIQUE.fetch_add`, with a disk-existence check, so uniqueness already holds inside one daemon — but the plan asserts the deferral rather than closing it. |
| Observable acceptance and baseline evidence | 19 | The dimension this review turned on, and it holds. Every premise re-derived line by line (table above) and none was wrong. The baseline gap is real and I confirmed it at the source: `run_state.rs:293-329` drives `"session":"s1"` twice and asserts the refusal. The new test is provably load-bearing: under a node-wide-lock regression it was the *only* failure out of 14. All three Verify blocks were extracted from `spec01.md` verbatim and run as `sh -eu -c` with empty stdin — exit 0 / 0 / 0 in 1.2 s, 2.5 s, 0.0 s warm, and 6 s (cold dedicated target dir) / 12 s (cold, compile cache bypassed) for block 1. Far inside the 120 s limit. Paths relative to the repo root, no `cd` to an absolute checkout, `CARGO_TARGET_DIR` pinned per the template's own `${CARGO_TARGET_DIR:-$PWD/target/<slug>-verify}` form in both cargo blocks, and `target/` is gitignored (`agent.ctg/.gitignore:2`). After all three blocks `git status --porcelain` showed only the footprint file the patch changes — no block wrote inside the footprint, so neither the lane commit nor pass 2's "source footprint changed" abort is at risk. **−1**: spec Acceptance box 3 still leads with "Exactly one agent node exists with the daemon running", which the spec cannot prove, and puts the narrowing in prose afterwards. The PRD box was narrowed; the spec box should be reworded to agent.ctg's provable share so the two records do not read differently on the same box. |
| Failure, recovery and compatibility | 19 | Recovery is addressed where it matters: the PRD names `Agent::recover` as the real symptom and shows one daemon removes it, and the existing `restart_marks_unfinished_run_interrupted_without_replay_and_allows_a_new_start` already pins that path, so no new coverage is owed. Compatibility is total — no `src/` change, so no caller, wire shape or on-disk format moves; on the applied patch `cargo test --lib` gave 21 passed / 0 failed and `cargo clippy --all-targets` + `cargo fmt --check` were clean under `warnings = "deny"`. `Remaining risk` is honest and complete on the three real limits: same-session single-flight is the intended contract, session-id uniqueness is owned elsewhere, and `agent.event` fans out node-wide but carries `{session, run}` so no transcript leaks. **−1**: the unbounded `Agent.runs` map is the one place the plan accepts a real ceiling without leaving a check — under one long-lived daemon it retains one entry per session ever started, and "add pruning only if ever measured as a problem" is the right call but nothing makes it measurable. A one-line comment at `src/lib.rs:169` naming the ceiling and the reason (`status` serves `checkpoint_error` from the finished entry and it exists nowhere else) would close it. |
| Reviewer total | **95** / 100 | Five deductions, each one point, each specific and each non-blocking. No finding invalidates the plan's central claim, which I verified independently and which the regression injection corroborated empirically. |

Findings and concrete revisions:

1. *(minor, non-blocking)* **Spec acceptance box 3 is phrased wider than the spec can prove.** Evidence: `specs/spec01.md` Acceptance box 3 opens "Exactly one agent node exists with the daemon running", with the delegation to the `done` sibling and the composed test following in prose; the PRD's box 3 was already narrowed by the coordinator to agent.ctg's provable share. Recommendation: reword the spec box to lead with agent.ctg's share ("agent.ctg starts no host, node or child process of its own, so a second agent node can only come from the host"), keeping the delegation as the trailing note. Resolution: open — a wording change to `spec01.md`, no re-run needed.
2. *(minor, non-blocking)* **The session-id-uniqueness deferral is asserted, not argued.** Evidence: `specs/spec01.md` `Remaining risk` hands concurrent-`start` session-id uniqueness to `sessions-runs-once-in-the-daemon-with-one-buffer-id-space`, which is `state: open`, while the PRD's `needs` lists only the attach sibling. Recommendation: add one sentence stating that no `needs` edge is required because ids already come from nanos plus a process-wide atomic with a disk-existence check (`sessions.ctg/src/lib.rs:654-665`), which is unique inside one daemon. Resolution: open — one sentence; I verified the underlying fact, so no edge is actually needed.
3. *(minor, non-blocking)* **Verify block 3 pins a declaration textually.** Evidence: `grep -q 'runs: Mutex<HashMap<String, Arc<Control>>>' src/lib.rs` would fail on a `rustfmt` reflow or a type alias with a failure message that names nothing useful, and the behaviour it guards is already pinned by the new test under injection. Recommendation: drop it, or relax to `grep -q 'runs: Mutex<HashMap<String,' src/lib.rs`. Resolution: open — optional; harmless as written.
4. *(minor, non-blocking)* **`Agent.runs` grows without bound and without a marker.** Evidence: `src/lib.rs:169`; nothing removes a finished control, and `spec01.md` `Remaining risk` records the ceiling only in the plan. Recommendation: a one-line comment at the declaration naming the ceiling and the upgrade path, so the next reader finds it in the code rather than in a spec. Resolution: open — inside the existing `src/` footprint, but it is a comment, and the spec's "no change under `src/`" rule is there to prevent churn; the coordinator may reasonably defer it.
5. *(informational)* **PRD title and `Outcome` read as pending production work.** Evidence: the title "Agent runs key per attached instance, not per process" and the `Outcome` paragraph state the end state; `What changes` then reports it already holds. No revision required — both are true as end-state statements, and PRD outcomes are end states rather than diffs. Noted so a later reader is not surprised by an empty `src/` diff. Resolution: no action.

Disposition: **keep**. The plan owns one observable outcome, the accountable cartridge is right, and the deliverable is the correct minimum. Retiring the PRD as already-satisfied was the tempting alternative and would have been wrong: the outcome holds today only by a keying decision that nothing in the suite defended, and I demonstrated that a one-line change to `src/lib.rs` silently removes it with the suite still green. The regression pin is the smallest thing that makes the outcome durable, and it is the whole change.

Validation: all commands run in a scratch worktree of `agent.ctg` at `4e544f2` under the session scratchpad (`…/scratchpad/wt-review`), with `CARGO_TARGET_DIR` isolated to `…/scratchpad/target-review`, `…/scratchpad/target-nocache` or the block's own in-worktree `target/agent-runs-key-verify`. The live checkout's default target dir was never built in; the live daemon was never touched. `agent.ctg` is a standalone cargo workspace with no path dependencies (`Cargo.toml` has no `path =` entry outside its own `src/lib.rs` and integration test), so no sibling `*.ctg` symlinks were required.

| # | Command | cwd | Exit | Observed |
| --- | --- | ---: | ---: | --- |
| 1 | `git worktree add …/scratchpad/wt-review 4e544f2 --detach` | `agent.ctg` | 0 | detached at 4e544f2 |
| 2 | `git apply --check attempt-1.patch` then `git apply attempt-1.patch` | `wt-review` | 0 | 1 file changed, 72 insertions(+); `M .cartridge/tests/unit/run_state.rs` only |
| 3 | Verify block 1 as `sh -eu -c` (`cargo test --lib run_state`) | `wt-review` | 0 | 14 passed, 0 failed, 7 filtered out, 1.04 s test time; 12 s wall, fresh target dir |
| 4 | Verify block 2 as `sh -eu -c` (`cargo clippy --all-targets`; `cargo fmt --check`) | `wt-review` | 0 | clean under `warnings = "deny"`; 2 s wall |
| 5 | Verify block 3 as `sh -eu -c` (4 greps incl. the `!`-negated spawn check) | `wt-review` | 0 | 0 s wall |
| 6 | `cargo test --lib` (full lib suite) | `wt-review` | 0 | 21 passed, 0 failed, 1.03 s |
| 7 | Regression A: `start` guard → `runs.values().any(…)`, then `cargo test --lib run_state` | `wt-review` | 101 (test failure) | **FAILED. 13 passed; 1 failed** — only `two_sessions_hold_concurrent_runs_with_separate_transcripts`, panic at `run_state.rs:831`. `concurrent_starts_…` still passed. Reverted. |
| 8 | Regression B: `Agent::control` → ambient first-unfinished run, then `cargo test --lib run_state` | `wt-review` | 101 (test failure) | FAILED. 4 passed; 10 failed. Reverted; `git diff --stat src/lib.rs` empty. |
| 9 | Cold block 1 with `CARGO_TARGET_DIR` unset (block default `$PWD/target/agent-runs-key-verify` applied) | `wt-review` | 0 | 6 s wall, 433 MB target dir, 14 passed; `git check-ignore -v target/agent-runs-key-verify` → `.gitignore:2:/target/` |
| 10 | Cold block 1 with the compile cache bypassed (`RUSTC_WRAPPER=""`, fresh target dir) | `wt-review` | 0 | 12 s wall, 14 passed — the 120 s limit holds without the machine's `kache` wrapper (`~/.cargo/config.toml` `build.rustc-wrapper`) |
| 11 | All three blocks re-extracted verbatim from `spec01.md` and run as `sh -eu -c`, empty stdin, `CARGO_TARGET_DIR` removed from the environment | `wt-review` | 0, 0, 0 | 1.2 s, 2.5 s, 0.0 s |
| 12 | `git status --porcelain` after the literal blocks | `wt-review` | 0 | `M .cartridge/tests/unit/run_state.rs` only — no block wrote inside the footprint |
| 13 | `grep -rn 'static \|lazy_static\|OnceCell\|OnceLock\|thread_local' src/` | `agent.ctg` | 0 | 5 hits, none holding a run/session/lock (see trace table) |
| 14 | `grep -rn 'Command::new\|std::process\|cartridge daemon' src/` | `agent.ctg` | 1 (no match) | corroborated by absent tokio `process` feature and no spawner dependency |
| 15 | `git apply -R attempt-1.patch`; remove previewed untracked `target/`; `git worktree remove …/wt-review` (**no `--force`**) | `wt-review`, `agent.ctg` | 0 | worktree gone; live `agent.ctg` `git status --porcelain` empty at 4e544f2 |

No `prd` state operation was run, nothing was staged, committed or pushed, and `prd.md` was not edited by this review.

Note for the coordinator: the analyst's own scratch worktree is still registered at `…/scratchpad/wt` (detached 4e544f2), and `/Users/feb/dev/cartridge-worktrees/ws/agent.ctg` shows as `prunable`. Neither is mine to remove; both are housekeeping, not findings.

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS** (95/100, no unresolved blocking finding).
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed to implementation. The worker lands `attempt-1.patch` as is — it applies cleanly to `4e544f2` and its only changed path is inside the amended footprint. Findings 1–4 are optional polish and none requires another review round; if the coordinator applies finding 1 or 2 (wording in `spec01.md` only, no semantic change to any acceptance box or Verify block), record the diff under the formatting-only rule so this rating is preserved rather than spending round 2.
