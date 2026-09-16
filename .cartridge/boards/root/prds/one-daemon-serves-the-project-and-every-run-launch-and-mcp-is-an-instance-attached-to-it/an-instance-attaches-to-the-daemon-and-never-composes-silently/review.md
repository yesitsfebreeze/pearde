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
