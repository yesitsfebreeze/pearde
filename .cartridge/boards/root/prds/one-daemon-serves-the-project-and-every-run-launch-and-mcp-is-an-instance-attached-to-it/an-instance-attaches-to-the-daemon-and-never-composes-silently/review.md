# @root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently review history

Plan: @root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently, `prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently/prd.md` with `specs/spec01.md`.
Scope: a leaf with one observable outcome. `run`/`call`/`launch`/`mcp` attach to the one project daemon or start it. They never compose on their own, a second daemon refuses, and there is one stop command.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none. The parent has no review record.

Use the shared [review method](../../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: prd.ctg `7a8efbca`, with `prd.md` modified and `specs/` untracked (dirty). Code base: cartridge.ctg `cdd3124`, clean tree. Analyst evidence: `.state/loop/an-instance-attaches-to-the-daemon-and-never-composes-silently/analyst-1.md`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `34c20105bc274c1052c9fbce6efb29bbafd8190c9e18712f62b6390195620c65` |
| Specs | `specs/spec01.md` sha256 `37ed60f995fa3845101a442215d2b39ef31a2368eb5955ff877f2ea2cda3553d` |
| Material contracts/dependencies | parent `prd.md` sha256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445`. cartridge.ctg `cdd3124`: `src/cli/{client,host}.rs`, `src/host/{mod,socket}.rs`, `src/transport/typed.rs:902-925`. Superproject `.cartridge/tests/integration/{takeover,smoke}.test.ts` and `.cartridge/justfile`. Sibling `@root/smoke-passes-mcp-and-proxy` (claimed by coordinator-c4-9). Dependents: the live, mcp, memory and composed-test children. Callers of `cartridge run` in temp projects: `tools.ctg/.cartridge/tests/integration/lane.test.ts:48`, `prd.ctg/.cartridge/tests/{host,source-records}.test.ts` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | This is the root cause of the many compositions seen on 2026-09-15, and the spec narrows the work to the real gap at `cdd3124`: `run` still falls back to composing its own host (`host.rs:165-183`), `client::served` still uses `.ok()` (`client.rs:38-47`), and a racing daemon stays alive with no nodes (`host.rs:344-348`). The analyst answered both open questions (solo `verify`/`doctor`; `launch` keeps its agent). −2: PRD box 1 names `run`/`call` and says to count node children, but the spec proves only `run` and proves it differently (see N1). |
| Ownership and reuse | 17 | The plan reuses what `d840064` built: `attach`, `Host::unpublish` with its dev/ino identity (`mod.rs:595-605`), `cartridge stop`, and the `profile`/`cli`/`daemon`/`active` test helpers. Dropping `serve_beside` is forced anyway by `warnings = "deny"`. −3: the spec edits `.cartridge/tests/integration/smoke.test.ts`, which the claimed `smoke-passes-mcp-and-proxy` item is repairing. Callers of `run` in other owners' tests are outside the footprint and not considered (B3). |
| Dependencies and implementable slices | 13 | The steps are small and ordered, and the footprint covers every cartridge.ctg file the steps touch (through the `cartridge.ctg` gitlink) plus both superproject tests. −4: `needs: []`, but the `just smoke policy` block cannot pass until `smoke-passes-mcp-and-proxy` lands (B1). −3: the live child needs a way for an outside process to attach or start without spawning its own daemon (PRD Findings, bullet 4). After this spec that way is `cartridge run <event>`, but neither the spec nor the live child says so (N3). |
| Observable acceptance and baseline evidence | 13 | The new lifecycle tests fail at HEAD for the unmet boxes: `run` against an erroring socket exits 0 today, racing daemons both stay alive, two `run`s leave no daemon and `status` fails, and `grep 'cartridge stop'` exits 1 (checked). Box 3 is already met, and the racing test's inode check covers it. Each gate has its own block, and every lifecycle host uses its own `XDG_RUNTIME_DIR` and scratch root. −3: block `just smoke policy` exits 1 at HEAD with ENOENT `…/builtin/policy`, so collect cannot pass (B1). −2: the "no `<pid>/plain.sock` appears" check is empty, because a private host removes its pid dir when it drops (N1). −2: `just test cartridge` took 63 s and failed 2 of 168 tests at HEAD under load (N5). |
| Failure, recovery and compatibility | 11 | Refusing a losing daemon and binding before composing are correct, and the residual stale-file race is disclosed. −5: `attach` turns every error on a socket that answers the probe into a hard failure. That includes the short window during `daemon --replace` or `just proxy`, when the old host still accepts and then drops the connection. `mcp`'s `Backend::message` reattaches exactly in that window, and HEAD retries there (B2). −4: auto-start from `run` multiplies orphaned detached daemons. 32 `target/debug/cartridge --dir <deleted tmp> daemon` processes were alive during this review. Nothing makes a daemon exit when its project goes away (B3). |
| Reviewer total | 72 / 100 | |

Findings and concrete revisions:

- **B1 — BLOCKING. The smoke block is red at HEAD and has an unrecorded dependency.** `just smoke policy` (cwd superproject) exits 1 in 1 s: `smoke.test.ts:38` symlinks `<root>/builtin/policy`, which does not exist. `@root/smoke-passes-mcp-and-proxy` owns this failure and is claimed. Revision, pick one: (a) add `needs: smoke-passes-mcp-and-proxy` and coordinate the `smoke.test.ts` overlap with that item; or (b) drop the `just smoke policy` block and the smoke step 7 from this spec, and hand "stop the daemon the policy case now starts" to the smoke item as a note.
- **B2 — BLOCKING. Loud failure breaks the host swap.** Step 2/3 make `attach` return the `socket::client` error whenever `socket::served` connected. In the swap window (old host stopping, staged socket not yet renamed, or probe and client landing on different hosts), connect or auth fails for a moment. `mcp` reattach, `launch` and prompt-recall `run` would then error where HEAD retried. Revision: in `attach`, retry an erroring socket like a silent one until the 1.5 s grace ends, and never spawn a daemon while the socket answers. Return the last error only after the grace. Add a lifecycle test: `run plain null` in a loop, run concurrently with `daemon --replace`, exits 0 every time.
- **B3 — BLOCKING. Auto-start leaks detached daemons.** At review time 32 detached daemons were alive, with `--dir` pointing at deleted temp dirs (`.tmp*`, `mcp-approval-*`, `mcp-refresh-*`), left by suites that already attach. With spec01, every `cartridge run` in a temp project also spawns one: `tools.ctg lane.test.ts:48`, `prd.ctg host.test.ts:27`, `source-records.test.ts:80`, and the smoke policy case. It also adds the 1.5 s grace to each. The `takeover.test.ts` `afterAll` SIGKILLs only direct children, and detached daemons are not its children. Root-cause revision inside the footprint: a daemon stops itself when its descriptor (`.cartridge/init.lua`) or project dir disappears. The existing `host.watch()` can trigger it. Add a lifecycle test that removes the root and expects the daemon to exit within 10 s. Also make `afterAll` run `stop` for every root before removing it.
- **N1 — non-blocking.** The box-1 test's "no pid dir with `plain.sock`" check passes even when a private host composed, because its drop deletes the dir. Revision: also assert that stderr lacks "starting the host", that no `daemon.log` was created, and (as the PRD says) that the `sample()` count of pid dirs holding sockets stayed 0 while `run` ran.
- **N2 — non-blocking.** In smoke step 7, put `stop` in `finally`, not only on the success path. The `mcp` smoke case at HEAD already leaves a detached daemon; stop it too if B1(a) is chosen.
- **N3 — non-blocking.** Give the dependent live child its contract in one sentence of the spec's Outcome: out-of-process tools attach or start with `cartridge run <event>` or `cartridge call` after an attach, never `daemon`. Add the same line to the live child's What changes.
- **N4 — non-blocking.** No recovery is specified for a wedged daemon, one that accepts connections but never authenticates. `stop` cannot reach it, `--replace` now exits on the `?`, and killing by name is banned. Revision: the error names the socket and says how to find the pid (e.g. `lsof <host.sock>`), or `stop` falls back to the pid recorded at publish.
- **N5 — non-blocking.** `just test cartridge` at HEAD ran 168 tests in 63 s: 166 passed, and 2 hit `NotProvided` after 60 s (`tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare`, `…a_node_serves_other_events_while_a_handler_waits`). Both pass in 4 s when run alone, so this is contention and not caused by this spec. The block is under 120 s but can go red at collect. Note it in Remaining risk or in the contention item.
- **N6 — non-blocking.** The name-kill guard ignores `*.md` routine memos, which `memo-run` executes, and `pgrep … | xargs kill`. Widen it with `-g '*.md' -g '!**/prds/**' -g '!**/.state/**'`. That scope is clean today.

Disposition: keep. Revise B1–B3 in one spec revision. N1–N6 are recommended.

Validation (cwd `/Users/feb/dev/cartridge`, host load average about 3, other sessions active, the live project daemon untouched):
- `just test lifecycle`: exit 0, 4 tests, 9 s.
- `just test cartridge`: exit 1, 63 s, 166/168 passed. Rerunning the 2 failures alone in `cartridge.ctg` passed in 4 s.
- `just check cartridge`: exit 0, 0.7 s (warm).
- `just smoke policy`: exit 1, 1 s, ENOENT `/Users/feb/dev/cartridge/builtin/policy`.
- `sh -eu -c "! rg -n 'pkill\s+-f|killall\s' …"`: exit 0, under 1 s. The widened `*.md/*.lua/*.toml` search found nothing.
- `grep -q 'cartridge stop' cartridge.ctg/docs/development.txt`: exit 1, as the spec expects at HEAD.
- `ps -Ao pid,ppid,etime,command` (read only): 32 detached `target/debug/cartridge --dir <deleted tmp> daemon` processes, aged 46 s to 47 min, all with parent pid 1. None were touched.

Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL (72/100).
Unresolved blocking findings: B1, B2, B3.
Rounds used / remaining: 1 / 4.
Next action: one bounded spec revision for B1–B3, with N1–N6 as needed, then round 2.

## Round 2 — 2026-09-16

Presented revision: spec01 revision 2 (the round 1 B1 smoke block dropped, B2 swap-tolerant attach, B3 project-gone exit, N1–N6 folded in). Code base: cartridge.ctg `cdd3124`, clean tree. Analyst evidence: `.state/loop/an-instance-attaches-to-the-daemon-and-never-composes-silently/analyst-1.md`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `4c322dbd0fff1cd2aa739c047ca1d0671bbd3221802c5e97d69d8416d02fa2f9` |
| Specs | `specs/spec01.md` sha256 `2061810430add9ed45bc8f75a680eb278da13141f23e9d37550d8ae4b9f31451` |
| Material contracts/dependencies | parent `prd.md` sha256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445` (unchanged since round 1). cartridge.ctg `cdd3124`: `src/cli/{client,host}.rs`, `src/host/{mod,socket,watch}.rs`, `src/transport/typed.rs:902-925,1210-1219`. Superproject `.cartridge/tests/integration/takeover.test.ts`. Sibling `live-attaches-to-the-daemon-instead-of-spawning-its-own` (needs this plan; contract line present at `prd.md:30`). `@root/smoke-passes-mcp-and-proxy` Planning note (records "a daemon that is never stopped") |

Round 1 resolutions, checked:
- B1: resolved. The smoke block, the smoke step and `smoke.test.ts` are gone from the spec and the footprint. `needs: []` is now true, and the smoke item's Planning note owns the unstopped daemon.
- B2: resolved in design. Step 3 retries `Err` through the grace and never spawns while the socket answers. The author's addition holds against HEAD. `Host::takeover` binds `sockets/host.sock.<pid>` before it calls `stop` on the old host (`mod.rs:641-647`). The old accept loop breaks on cancel, and dropping its `LocalListener` unlinks `host.sock` only while the identity still matches (`typed.rs:1210-1219`). So from then until the `rename` (`mod.rs:660`), the name is refused or missing while the staged socket connects. `takeover_pending` (the pid is `alive` and the socket is `served`) is true for exactly that window. `sweep` leaves a staged socket that answers, and a stale staged file from a dead replacer, or from a reused pid that does not answer, does not count. Keeping the poll until the startup deadline is bounded.
- B3: resolved in part. Step 7 and the `afterAll` `stop` are added, and the lifecycle test removes the root. See R2-B1 for the exit condition.
- N1 (stderr, `daemon.log` and `sample().seen === 0`), N3 (contract section plus the live child line), N4 (the error names the socket, `cartridge stop`, then `kill` of the numeric pid directory), N5 (Remaining risk) and N6 (widened globs): all folded in. N6 has no effect in practice (R2-N1).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The same root cause as round 1, now with the swap and orphan cases that made it harmful. Both open questions are answered in step 9. −1: PRD box 1 names `run`/`call`, but only `run` is tested. `call` is already attach-only (`cli/mod.rs:106-134`), so this is a small gap. |
| Ownership and reuse | 19 | The spec no longer overlaps the smoke item. It reuses `attach`, `Host::unpublish` identity, `socket::listen`/`publish_listener` (step 6 lifts `mod.rs:256-261`), `cartridge stop` and the test helpers. Callers of `run` in other owners' temp projects are named and covered by step 7. −1: step 1 makes `served` `pub` next to the identically named `client::served`, which invites confusion. A distinct name such as `answers` would avoid it. |
| Dependencies and implementable slices | 19 | `needs: []` is correct now. The live child `needs` this plan and states the `cartridge run <event>`/`call` contract. The steps are ordered, each fits one file, and step 7 has a stop-and-report cap. The line references match HEAD (`host.rs:345`, `mod.rs:595,623`, `watch.rs:12-59`). −1: the two-`run` race depends on both instances spawning a daemon and the loser exiting through step 5. That is correct, but it prints `starting the host` twice and leaves a loser line in `daemon.log`. The test should not assert against either. |
| Observable acceptance and baseline evidence | 14 | New tests fail at HEAD for the unmet boxes, as round 1 checked. Every host is isolated (`XDG_RUNTIME_DIR` of its own, a scratch root). −4 (R2-B2): the `--replace` test requires that every looped `run` exits 0. A `run` that attaches to the old host just before the replacer's `stop` sends its `bail` to a host that is cancelling its slots (`host.rs:352-366`, `Host::bail`/`sender` `mod.rs:741-803`). It gets an error, and neither HEAD nor the spec retries a non-idempotent event. This comes from reading the source; a probe was blocked by the session's shell guard. −2 (R2-N1): the name-kill guard `rg` skips hidden paths, so `.cartridge/` (tests, justfile, routine memos) is never searched. The block exits 0 in 0.02 s and also misses `takeover.test.ts`. |
| Failure, recovery and compatibility | 15 | Swap-tolerant attach, loser exit and owned unlink are all correct against HEAD. Wedged-host recovery is documented. −4 (R2-B1): step 7 stops the host when `descriptor.join("init.lua")` is missing, and checks `Path::exists()` on the watcher event itself. An editor's backup-rename save or a checkout briefly removes `init.lua` while the project directory exists. `exists()` also returns false on EACCES. Either case stops the live project daemon that other sessions use. −1: a manual `daemon` started while a takeover is staged sees the name refused, and `bind_unix` removes that file and rebinds (`typed.rs:916-918`). The replacer's `rename` then orphans that daemon's listener. Step 5 should also refuse while `takeover_pending`. |
| Reviewer total | 86 / 100 | |

Findings and concrete revisions:

- **R2-B1 — BLOCKING. The project-gone exit can stop a live daemon whose project still exists.** Step 7 uses `init.lua` presence and `exists()` checked right at the event. Revision: stop only when `host.dir.try_exists()` or `host.descriptor.try_exists()` returns `Ok(false)` (directories only, never `init.lua`; an `Err` counts as present), and only on the 2 s tick after two consecutive misses. That still exits within 10 s. Symlinks and moves are already handled: `Host::new` canonicalizes both paths (`mod.rs:132,137`). Removing a symlink alias leaves the daemon running, and moving or removing the real directory stops it, which is correct because the socket tag is keyed to the old path. Add one unit or lifecycle assertion: renaming `init.lua` away and back within 1 s leaves the daemon serving.
- **R2-B2 — BLOCKING. The `--replace` test demands something no specified code guarantees.** A `run` already attached to the old host fails when that host stops mid-`bail`, so "every run exits 0" will flake at collect. Revision, pick one: (a) word box 5 and the test as "no run starts a host (no `starting the host`, no `daemon.log`, `both === 0`); every run *started after* `host.sock.<pid>` appears, or after the first daemon exits, exits 0"; or (b) have the old host finish in-flight `bail`s before it acts on `stop`, and prove it. Option (a) is the smaller change.
- **R2-N1 — non-blocking.** Add `--hidden -g '!**/.git/**'` to the guard. With that flag it currently matches prose in `prd.ctg/.cartridge/boards/root/PROGRESS.md:80` and in `{.cartridge,memory.ctg/.cartridge}/memos/routine/proc-kill.md` (which warn about `pkill -f`). Restrict it to code globs (`*.ts,*.rs,*.sh,justfile,*.lua`) or exclude those two memo paths by name.
- **R2-N2 — non-blocking.** Step 5 also checks `socket::takeover_pending` and refuses with the same message while a replacement is staged.
- **R2-N3 — non-blocking.** Rename the public `socket::served` (for example `answers`) so it does not shadow `client::served`. In the two-run test, do not assert anything on stderr or `daemon.log`.

Disposition: keep. Make one bounded spec revision for R2-B1 and R2-B2, with R2-N1–N3 as needed.

Validation (cwd `/Users/feb/dev/cartridge`; the live project daemon was untouched and no process was started):
- `git -C cartridge.ctg log -1`: `cdd3124`, porcelain empty.
- The spec's name-kill guard block under `sh -eu -c`: exit 0 in 0.02 s. The same search with `--hidden`: 3 prose hits, listed in R2-N1.
- Source read at HEAD: `src/host/socket.rs` (served/alive/sweep/listen), `src/cli/host.rs` (attach/run/daemon/Backend), `src/host/mod.rs:125-200,256-261,575-665,741-803,924-939`, `src/host/watch.rs`, `src/transport/typed.rs:902-925,1210-1219`.
- The isolated `--replace` + `call` loop probe (own `XDG_RUNTIME_DIR` and scratch root) was blocked by the session's shell safety guard and not run. R2-B2 rests on the source reading.
- `just test lifecycle`, `just test cartridge`: not rerun (code unchanged since round 1's results).

Reviewer identity: independent reviewer agent r2 (coordinator cartridge-c4).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL (86/100).
Unresolved blocking findings: R2-B1, R2-B2.
Rounds used / remaining: 2 / 3.
Next action: one bounded spec revision for R2-B1 and R2-B2, then round 3.

## Round 3 — 2026-09-16

Presented revision: spec01 revision 3 (round 2: R2-B1 directory-only two-miss tick, R2-B2 only runs started after staging must exit 0, R2-N1–N3). prd.ctg `a0454963`, with `prd.md`, `specs/spec01.md` and `review.md` modified (dirty). Code base: cartridge.ctg `cdd3124`. Its tree is now dirty with another session's uncommitted edits, which this plan does not own: `src/loader/{document,mod}.rs`, `src/node/mod.rs` and `.cartridge/tests/unit/src/trust/tests.rs`. Analyst evidence: `.state/loop/an-instance-attaches-to-the-daemon-and-never-composes-silently/analyst-1.md`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `157fbbbf28519c9e039b1f1bae6c9e673e37f1d3dc566945784facc3ceb98005`, which matches the hand-off |
| Specs | `specs/spec01.md` sha256 `79304397479a1afd784f3a801ea4ba5ca2683450dcb8bbed3681bd4dae16d8b6`, which matches the hand-off |
| Material contracts/dependencies | parent `prd.md` sha256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445` (unchanged since round 1). cartridge.ctg `cdd3124`: `src/cli/{client,host}.rs` (attach/run/daemon), `src/host/{mod,socket,watch}.rs`, `src/transport/typed.rs:902-925`, `src/settings/host.rs` with the `.cartridge/settings.json` defaults (startup 60 s, shutdown 15 s, debounce 500 ms). Superproject `.cartridge/tests/integration/takeover.test.ts` and `.cartridge/justfile:108`. Sibling `live-attaches-to-the-daemon-instead-of-spawning-its-own` (`needs` this plan) |

Round 2 resolutions, checked against the code:
- R2-B1: resolved. Step 7 checks only `host.dir`/`host.descriptor` with `try_exists()`, counts an `Err` as present, acts only on the 2 s tick, needs two consecutive misses and resets on a hit. Both fields exist and are canonicalized in `Host::new` (`mod.rs:129-137`). `daemon` exits after `stopped()`, aborts the watcher and calls `host.stop()` (`host.rs:352-366`). A new lifecycle test renames `init.lua` away for 2.5 s. Only `daemon` calls `watch`.
- R2-B2: resolved with option (a). Box 5 and the test now require exit 0 only from runs started after `host.sock.<replacer pid>` exists or after the first daemon exits. Every run must still start no host (`starting the host` absent, no `daemon.log`, `both === 0`), and the non-idempotent `bail` is not retried. In `Host::takeover` (`mod.rs:636-660`) the staged socket lives in `self.sockets` (the run dir, the same dir as `host.sock`) and `old.call("stop")` follows it at once. A run spawned after staging would have to be accepted by the old host before that one RPC lands, which process start-up latency (tens of ms against well under 1 ms) makes negligible. After cancel, the name is refused or missing, so `answers` is false and `takeover_pending` is true, because the staged listener is bound and a plain `UnixStream::connect` (`socket.rs:198-200`) succeeds against its backlog. The run polls until the 60 s startup deadline, which exceeds the 2 × 15 s takeover wait.
- R2-N1: resolved. The guard uses `--hidden` with code globs. Under `sh -eu -c` in the superproject it exits 0 in 0.05 s.
- R2-N2: resolved (step 5 refuses while `takeover_pending`).
- R2-N3: resolved. `socket::served` becomes `pub fn answers`, and the two-run test asserts nothing on stderr or `daemon.log`. The loser daemon's pid dir is removed by `Drop` → `unpublish` (`mod.rs:120-125,595-605`), so "exactly one numeric pid dir with `.sock` files" holds.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The same root cause, now covering the swap, race, orphan and editor-save cases. Both open questions are answered in step 9, and the planning note accepts auto-start from `run`. −1: PRD box 1 names `run`/`call`, but only `run` is tested. `call` is attach-only at HEAD (`cli/mod.rs:106-134`), so this is a small gap. PRD box 2 says "answers from the new host" and the spec says "exits 0"; that difference is cosmetic. |
| Ownership and reuse | 19 | The plan reuses `attach`, `Host::unpublish` identity, `socket::listen`/`publish_listener` (step 6), `cartridge stop` and the test helpers `profile`/`cli`/`daemon`/`active`/`sample`. It has no overlap with the smoke item. −1: the shared cartridge.ctg checkout now holds foreign uncommitted edits (loader, node, trust tests). The implementer must not fold them into this plan's commits. The first Verify block catches this at collect, but the plan does not say to coordinate. |
| Dependencies and implementable slices | 19 | `needs: []` is correct. The live child `needs` this plan and names the attach path. Each step fits one file, in order, and step 7 has a ~20-line cap. −1: step 3 points to "the recovery hint (step 7)", but the recovery text is in step 8. |
| Observable acceptance and baseline evidence | 17 | Every new test is isolated (its own `XDG_RUNTIME_DIR` under `/tmp/ctgrt-*`, a scratch root, `stop` in `afterAll` and `finally`) and fails at HEAD for the unmet boxes, as round 1 checked. The flaky oracle is gone. −2: "exits within 6.5 s" rests on the arithmetic (two misses ≤ 4 s, then `host.stop()`) and was not measured. The file-event body (500 ms debounce, `reconcile`, `replace_changed` → `stop_slot`) runs inline in the same `select!` loop and can delay a tick. A probe of the removal on the HEAD binary confirmed only the baseline: the daemon is still alive 8 s after `rm -rf` of the root. −1: `just test lifecycle` grows from 4 tests (9 s) to about 11. Several wait multiple seconds (4 s sample, 10 s race, `--replace` loop until exit plus 3 s, 6.5 s, 7.5 s). The estimated 50–70 s under load is unmeasured against the 120 s limit per block. |
| Failure, recovery and compatibility | 18 | The swap-tolerant attach, the loser exiting before it composes (`listen` before `reconcile`), owned unlink, the refusal while a takeover is staged, the directory-only project-gone exit and the documented recovery for a wedged host (`stop`, then `kill` of the numeric pid dir) are all correct against HEAD. −1: `tokio::time::interval` defaults to `MissedTickBehavior::Burst`. After a long inline `reconcile` on a real composition (the startup timeout is 60 s), the delayed ticks fire back to back, so "two misses 2 s apart" can collapse to microseconds. −1: the stale-file bind race is disclosed (`typed.rs:916-918`) but not closed. |
| Reviewer total | 92 / 100 | |

Findings and concrete revisions:

- **R3-N1 — non-blocking.** Step 7: run the project check in its own spawned task (an `interval` with `set_missed_tick_behavior(MissedTickBehavior::Delay)`, cancelling `stop_signal()`) or keep the `select!` but set `Delay`. Event handling then cannot starve the tick, and a catch-up burst cannot count two misses at once. The line cap still holds.
- **R3-N2 — non-blocking.** Record the measured `just test lifecycle` duration after implementation, in the Verify comment. If it exceeds about 90 s, split the lifecycle tests into two `bun test` files or blocks.
- **R3-N3 — non-blocking.** Before implementation, confirm that the cartridge.ctg edits in `src/loader`, `src/node` and `.cartridge/tests/unit/src/trust` belong to another session, and keep them out of this plan's commits. Block 1 stays red until their owner commits them.
- **R3-N4 — non-blocking.** Step 3: change "(step 7)" to "(step 8)". Optionally add `call` to the erroring-socket test, since it is a single `cli` call.

Disposition: keep. Proceed to implementation; fold R3-N1 into step 7 while implementing.

Validation (cwd `/Users/feb/dev/cartridge`; the live project daemon was untouched):
- `shasum -a 256` of `prd.md` and `specs/spec01.md`: both match the hand-off digests.
- `git -C cartridge.ctg log -1`: `cdd3124`. Porcelain shows 4 modified files outside this plan (R3-N3).
- The spec's name-kill guard block under `sh -eu -c`: exit 0 in 0.05 s.
- An isolated probe (scratchpad `probe.ts`, `XDG_RUNTIME_DIR=/tmp/ctgrt-*`, a scratch root, HEAD binary `target/debug/cartridge` built 10:45): after `call plain null` succeeded, `rm -rf` of the root left the daemon alive 8 s later (exitCode null). This is the baseline step 7 fixes. The daemon was SIGKILLed by its pid as the probe's own child, and the runtime dir was removed. `ps` shows no probe process left.
- Source read at HEAD: `src/cli/host.rs:55-200,330-366`, `src/cli/client.rs:30-50`, `src/host/watch.rs`, `src/host/socket.rs:1-150,198-220,476`, `src/host/mod.rs:120-137,250-265,504-605,623-665`, `src/transport/typed.rs:902-925`, `.cartridge/tests/integration/takeover.test.ts:1-140`.
- `just test lifecycle`, `just test cartridge`: not rerun. The code is unchanged, and the cartridge.ctg tree carries foreign edits.

Reviewer identity: independent reviewer agent r3 (coordinator cartridge-c4).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: PASS (92/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: proceed to implementation (R3-N1 folded into step 7; R3-N3 coordinated before commits).
