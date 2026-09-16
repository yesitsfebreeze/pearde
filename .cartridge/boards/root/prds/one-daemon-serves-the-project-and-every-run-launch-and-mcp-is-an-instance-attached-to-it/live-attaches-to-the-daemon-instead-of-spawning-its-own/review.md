# `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/live-attaches-to-the-daemon-instead-of-spawning-its-own` review history

Plan: `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/live-attaches-to-the-daemon-instead-of-spawning-its-own`,
`prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/live-attaches-to-the-daemon-instead-of-spawning-its-own/prd.md`.
Scope: executable leaf — `cartridge launch` becomes an instance attached to the project daemon and starts no daemon of its own; attaching marks no in-flight work `interrupted`.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: superproject `47b01e6` (the spec's stated base `0e3916c` advanced during
review; the `live.ctg` gitlink is unchanged at `4cbb053`, and both spec-touched files are clean
at it, so the reviewed content is not stale). `live.ctg` working tree is dirty for other
sessions' work: `M .cartridge/docs/README.md`, `M .cartridge/help.md`, `M cartridge.json`,
`M mcp/cartridge.json`, `M src/auth.ts`, `M src/control.ts`, **`M src/coordinator.ts`**,
`M src/server.ts`, `?? .cartridge/tests/integration/delegate.test.ts`,
`?? .cartridge/tests/integration/voice.test.ts`, `?? src/voice.ts`.

| Input | Content digest |
| --- | --- |
| Plan | `prds/…/live-attaches-to-the-daemon-instead-of-spawning-its-own/prd.md` — `70c5dbbadd4226021cf89c81a02b8f79754818c8ec7cfe7912a5e2c9f4e5acc7` |
| Specs | `specs/spec01.md` — `ddcd56705db835b3d1c796ee1fd47d6e230c74cc2f3f368612dd24aae6b50098` |
| Prototype | `.state/loop/…/attempt-1.patch` — `1d678d9e29c77e9304da698b2eb14bdfff18cb3b3f0bbf86e066710ad41ff2d5` |
| Analyst report | `.state/loop/…/analyst-1.md` — `dfaf82b15274aaa68b9c624dfe175c15c9ebf639fec1e8748d78476c2dea84f6` |
| Material contracts/dependencies | `live.ctg/src/launch.ts` `285437c66fd3d2ac4275c225cf0f14a9c18ed33613f7a8192af569a043725f12`; `live.ctg/src/coordinator.ts` (dirty) `64dd1eeba35df5dece029d789758072bb47b64d4e9035fca66e552daf949a6b5`; `live.ctg/.cartridge/tests/integration/launch.test.ts` `0b0dbb1efb2ad28551de0ff64394e42bf602aa0f07eae72d5e226d548a97dfc7`; `cartridge.ctg/src/cli/host.rs` `5158eef8c9cbe771b195d8a7d09d52740401a1c8647f91aa693fb96af6408def`; `cartridge.ctg/.cartridge/settings.json` `58dce7c1c98f9169fc5dfdf8897fa9274dc17f09c9c39a33e69924fab71ab000`; done sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently` at `f364f46` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | One observable outcome, one owner, three acceptance boxes, well under 400 words; it removes the last daemon-spawner outside `cartridge.ctg` (`live.ctg/src/launch.ts:46-55`), which the parent's Findings name as the main cause of many compositions. **−4 (F3):** the change silently drops `--yolo` from the project daemon. Today `launch.ts:52` spawns `["--yolo","daemon"]`; `--yolo` sets `YOLO_ENV` (`cartridge.ctg/src/cli/mod.rs:87-89`), which `settings::apply` merges as `{"yolo": true}` into every cartridge declaring that setting (`src/settings/mod.rs:15-17`) — `agent.ctg/cartridge.json:100` ("bypass tool policy and skip resolver provenance recording"), `proxy.ctg/cartridge.json:75` ("grant every tool call without asking the policy … for a launched agent"), `memo.ctg/cartridge.json:129`. `spawn_daemon` passes only `--dir <project> daemon` (`host.rs:117-125`), and `cartridge.ctg/src/cli/args.rs:170` states plainly that `--yolo` "cannot change an existing daemon". So `just live` stops composing its agent/proxy/memo in automatic-execution mode. The direction is the safe one and it is a consequence of the parent's one-daemon shape, but neither the spec's "Option chosen" nor its "Remaining risk" records it, and it changes how a launched agent's tool calls are governed. |
| Ownership and reuse | 13 | Textbook reuse: the spec deletes ~20 lines and delegates the race, the detached spawn and the settle to `host::attach`, refusing to re-derive them in Bun; it also refuses an "is this an attach?" flag on `Coordinator` as a second name for "did this node just start". Ownership is correct — live board child, `needs` the done sibling. **−7 (F1, blocking):** the amendment that kept `src/coordinator.ts` in the PRD footprint is not free. `feet(prd)` is the **union** of the prd.md and spec footprints (`prd.ctg/src/planner.ts:5-9`), and `collect` runs `git status --porcelain … -- <footprint>` and then `git add` + `git commit --only` on **every changed path in it** (`prd.ctg/src/lifecycle.ts:143-158`). `src/coordinator.ts` currently carries 60 uncommitted lines of another session's delegation/watcher work (`git diff --stat src/coordinator.ts` → `60 insertions(+), 9 deletions(-)`), so collecting this PRD would commit that work under "Implement @root/…/live-attaches-to-the-daemon-instead-of-spawning-its-own". The path also needlessly reserves the file against other PRDs through `clash()` (`planner.ts:10-13`). The stated reason — "so a later slice can touch it without a re-review" — does not hold: a later slice touching `coordinator.ts` would carry its own spec and its own review anyway. |
| Dependencies and implementable slices | 18 | `needs` names the done sibling, and the delegation of Acceptance box 3 is **legitimate**, verified independently: `run` is `attach` then `client::bail` (`host.rs:222-230`) and `launch` is the same `attach` (`:236-238`), so both share one path; `attach` sets `spawned` once and never spawns twice (`:83-91`); a losing daemon exits at the bind rather than running nodeless (`:396-401`); and the concurrency itself is pinned upstream by `.cartridge/tests/integration/takeover.test.ts:303` — *"two runs with no daemon share one"*, which asserts one surviving composition and a working `status`. Box 3 is therefore proven by somebody. **−2:** the spec cites that file as `.cartridge/tests/integration/takeover.test.ts` without qualification; `live.ctg` has its own `.cartridge/tests/integration/`, and the test lives in the **superproject**. Qualify the path. |
| Observable acceptance and baseline evidence | 15 | Both `## Verify` blocks run as literal `sh -eu -c` commands, are repo-root-relative, contain no `cd`, and use no cargo (so the `CARGO_TARGET_DIR` rule is not engaged). Timed: block 1 ≈ 1 s, block 2 < 1 s — far inside 120 s. Reproduced the analyst's table exactly (see Validation): patched suite exit 0 (2 pass / 16 assertions), the rewritten test against unpatched `launch.ts` exit 1 (0 pass / 2 fail), and Verify block 2 exit 1 at base, matching `src/launch.ts:52`. Also checked the lane pass specifically: block 1 still exits 0 with `node_modules` removed, so a bare worktree without siblings is fine. **−5:** (a) the rewritten test's red against unpatched code comes from the *fake binary refusing the `daemon` argv* (`The local coworker stopped (2)`, exit 2 propagated to `expect(code).toBe(0)`), so the run never reaches `expect(calls.filter(args=>args.includes("daemon"))).toHaveLength(0)` — the direction is right and the assertion is a real backstop for other regressions, but the assertion that names the outcome is not what fails today; (b) only box 1's live-side half is locally observable — boxes 1 (process count) and 3 (concurrency) are honestly declared as upstream, which leaves one of three boxes proven inside this repo. |
| Failure, recovery and compatibility | 10 | Claim 2 is **sound and independently confirmed**: the marking is in `Coordinator`'s constructor (`coordinator.ts:31-42`); its only caller is `startServer`, whose only caller is `wire.on("apply")` (`live.ctg/src/main.ts:17-21`, and `grep startServer live.ctg/src` shows no other construction path); the host sends `apply` exactly once, right after the node's socket connects (`cartridge.ctg/src/host/process.rs:207-210`); and `Host::replace` stops the slot before re-planning (`src/host/mod.rs:531`), so a reload is a new process, never a second `apply` on a live one. Acceptance box 2 holds. Recovery is also decent: a killed `cartridge run` leaves the detached daemon composing, and a rerun succeeds; the error now points at `<root>/.cartridge/daemon.log`, which is where `spawn_daemon` actually writes. **−8 (F2, blocking):** the 90 s ceiling is derived from the wrong setting. `attach`'s own `deadline` is `startup_timeout` (60 s), but when a socket answers it calls `settle_remote(&found.0, settings.verify_timeout())` (`host.rs:76`) and returns from inside that branch — `settle_remote`'s own deadline is `verify_timeout_secs`, **default 300** (`cartridge.ctg/.cartridge/settings.json:33-39`), and it blocks while any cartridge is `starting`/`waiting` or the status list is empty (`host.rs:145-177`). A cold attach is therefore bounded at ~300 s, not 60 s, so the launcher's 90 s per-command kill and 90 s loop deadline can fire *while the attach is legitimately settling*. The spec's "Remaining risk" compounds it — "If `startup_timeout_secs` is ever raised above 90 the attach would be killed early; the number tracks that setting" — when the setting that governs is already at 300 today. **−2:** the spec's absolute "An attaching instance … constructs nothing" has one counterexample it does not name: `settle_remote` issues one `reload {"cartridge": null}` on a trust refusal (`host.rs:152-165`) → `Host::reconcile`, which keeps healthy running slots (`mod.rs:307-311`) but starts `Waiting`/failed ones — so an attach *can* start a live node, and that node start does fire the recovery marking. The natural reading of box 2 still holds (nothing was in flight in a node that was not running), but the claim should be stated with that boundary. |
| Reviewer total | **72** / 100 | Two blocking findings; below the 90 threshold. |

### Findings and concrete revisions

**F1 — blocking. `src/coordinator.ts` must leave the PRD footprint.**
Evidence: `prd.ctg/src/planner.ts:5-9` unions the prd.md and spec footprints; `prd.ctg/src/lifecycle.ts:143-158` stages and commits every changed path in that union; `git -C live.ctg diff --stat src/coordinator.ts` → 60 insertions / 9 deletions of another session's uncommitted delegation work. Collecting this PRD as planned would commit that work under this PRD's receipt. The spec itself declares only `src/launch.ts` and the test, and step 3 says "Nothing under `src/coordinator.ts`", so the file is dead weight that is actively dangerous in this shared dirty checkout.
Recommendation: drop `src/coordinator.ts` from the prd.md `footprint` list (frontmatter edit by the coordinator, which owns it) and delete the "The path stays in the footprint so a later slice can touch it without a re-review" sentence from the PRD body. This does **not** break the Verify block: `lifecycle.ts` restricts *writes and commits* to the footprint, never reads, so `grep -q "phase='interrupted'" src/coordinator.ts` keeps working. If the intent is to pin that the marking is untouched, the grep alone already does it.
Resolution: open.

**F2 — blocking. The 90 s ceiling is derived from the wrong timeout, and the analyst never measured one.**
Evidence: `cartridge.ctg/src/cli/host.rs:74-77` — on `Ok(Some(found))`, `attach` calls `settle_remote(&found.0, settings.verify_timeout())` and returns without consulting its own `startup_timeout` deadline; `settle_remote` (`:140-177`) loops while any cartridge is `starting`/`waiting` or the list is empty, bounded by `verify_timeout_secs`, **default 300** (`cartridge.ctg/.cartridge/settings.json:33-39`). So the cold-attach bound the spec reasons about (`startup_timeout_secs` = 60) is not the bound that applies, and a settling attach may exceed 90 s without anything being wrong. The analyst states plainly that no cold attach was measured. A derived ceiling would be adequate *if it were derived from the right ceiling*; it is not, and the mitigation sentence names the wrong setting too.
Recommendation (any one, cheapest first): (a) drop the launcher's per-command kill timer entirely and let `cartridge run` be the authority on its own timeouts, keeping only an outer loop deadline that tracks `verify_timeout_secs`; or (b) keep a timer but size it from `verify_timeout_secs` and say so in Remaining risk; or (c) measure one cold attach in a scratch `CARTRIDGE_HOME` and scratch composition root and record the number. Whichever is chosen, the "Remaining risk" bullet must name `verify_timeout_secs`, not `startup_timeout_secs`.
Resolution: open.

**F3 — non-blocking, must be recorded. `--yolo` disappears from the project daemon.**
Evidence: `live.ctg/src/launch.ts:52` spawns `["--yolo","daemon"]` today; `cartridge.ctg/src/cli/mod.rs:87-89` turns `--yolo` into `YOLO_ENV`; `src/settings/mod.rs:15-17` merges `{"yolo": true}` into each cartridge declaring the setting — `agent.ctg/cartridge.json:100`, `proxy.ctg/cartridge.json:75`, `memo.ctg/cartridge.json:129`; `spawn_daemon` (`host.rs:112-130`) passes no such flag, and `src/cli/args.rs:164-170` says an instance "cannot change an existing daemon". The `trust --ask` gate with `CARTRIDGE_YOLO=1` survives (it is a separate, pre-attach `spawnSync`), so trust behaviour is unchanged; what changes is that a `just live` composition no longer runs agent/proxy/memo in automatic-execution mode.
Recommendation: one bullet in the spec's "Remaining risk" naming the delta and its direction (a policy bypass is lost, not gained), so nobody rediscovers it as a bug when a launched agent starts asking the policy.
Resolution: open.

**F4 — minor. Qualify the upstream test path.**
`.cartridge/tests/integration/takeover.test.ts` is in the **superproject**, not in `live.ctg` (which has its own `.cartridge/tests/integration/`). Write it as `<superproject>/.cartridge/tests/integration/takeover.test.ts` in both Acceptance box 3 and the "Option chosen" paragraph. Resolution: open.

**F5 — minor. Bound the "constructs nothing" claim.**
Add one clause to the `coordinator.ts` paragraph: an attach constructs nothing *except* through `settle_remote`'s single trust-refusal `reload` (`host.rs:152-165` → `Host::reconcile`, `mod.rs:294-327`), which starts `Waiting`/failed slots — and a node start is exactly when the recovery marking is meant to fire. Resolution: open.

### Judgements the coordinator asked for

- **Claim 1 (drop the spawn, rely on `cartridge run`) — upheld.** `run` is `attach` + `bail`; `attach` spawns at most one detached daemon per invocation and settles the composition before answering; `launch` uses the same `attach`. The "at most one" part is true per process, and true across concurrent processes because the loser exits at `listen()` rather than running nodeless. Box 3's concurrency is genuinely proven upstream by the done sibling's `takeover.test.ts:303` — the delegation is legitimate, not an orphaned box.
- **Claim 2 (`coordinator.ts` needs no change) — upheld**, with F5's boundary added. The "audit premise dissolves under one daemon" move is correct here for the same reason it was in `agent-runs-key-per-attached-instance-not-per-process`; I traced the constructor's single reachable caller chain and the host's single `apply` send myself rather than taking it on the sibling's precedent.
- **Claim 3 (10 s/30 s → 90 s) — not upheld.** See F2. A derived ceiling would be adequate; this one is derived from a setting that does not bound the operation.
- **Footprint amendment, `.cartridge/tests/integration/launch.test.ts` — correct and necessary.** Without it the spec has no executable Verify block from inside `live.ctg`, and both Verify blocks are now real gates (both reproduce red at base).
- **Footprint amendment, keeping `src/coordinator.ts` — incorrect.** See F1.
- **The analyst's "the rewritten test fails against unpatched `launch.ts`" — confirmed**, exit 1, 0 pass / 2 fail, with the caveat in F-column (b) of the acceptance dimension: the failure mode is the fake binary refusing the daemon argv, not the daemon-count assertion.
- **Folding the `launch.test.ts` fix into this PRD — right, keep it here.** The spec has to rewrite the same file regardless (its old fake `status` exits 0, so it never reached the spawn it claimed to forbid, and its `tui`/`pty` expectations assert code that `the-profile-is-the-orchestration-service` deleted). A separate live-board PRD would touch the identical path, so `clash()` would serialise the two anyway, and the "fix" is deletion of expectations for removed code — there is nothing to design and nothing to review separately. The only cost is a receipt that carries two reasons, and the Planning note already records that. No split.

Disposition: **revise** (keep the plan; it is the right shape). Fix F1 in `prd.md` frontmatter/body and F2–F5 in `spec01.md`, then present round 2.

### Validation

All work on `rsync` copies under the scratchpad
(`/private/tmp/claude-501/-Users-feb-dev-cartridge/0b0c3ecc-8350-4d76-ae7b-7feeb94a710f/scratchpad`),
with `auth.ctg` and `cartridge.ctg` symlinked as siblings. Nothing was written to the live
checkout; no daemon was started, stopped, replaced or reloaded, and no cargo was run.

| # | cwd | command | exit |
|---|-----|---------|------|
| 1 | `live-new` | `git apply --check attempt-1.patch`, then `git apply` | 0, 0 |
| 2 | `live-new` (patched) | `bun test ./.cartridge/tests/integration/launch.test.ts` | **0** — 2 pass, 0 fail, 16 assertions, 937 ms |
| 3 | `live-orig` (HEAD) | `bun test ./.cartridge/tests/integration/launch.test.ts` | **1** — 1 pass, 1 fail, `expect(ui).toBeDefined()` at `launch.test.ts:30` |
| 4 | `live-mixed` (unpatched `launch.ts` + rewritten test) | `bun test ./.cartridge/tests/integration/launch.test.ts` | **1** — 0 pass, 2 fail, both `The local coworker stopped (2)` → `expect(code).toBe(0)` received 2 |
| 5 | `live-orig` | Verify block 1 verbatim, `sh -eu -c` | **1** (red at base) |
| 6 | `live-orig` | Verify block 2 verbatim, `sh -eu -c` | **1** — first grep matched `src/launch.ts:52`, 1 s |
| 7 | `live-new` | Verify block 1 verbatim, `sh -eu -c` | **0**, < 1 s |
| 8 | `live-new` | Verify block 2 verbatim, `sh -eu -c` | **0**, < 1 s |
| 9 | `live-bare` (patched, `node_modules` removed) | Verify block 1 verbatim, `sh -eu -c` | **0** — 2 pass, 718 ms; the lane pass needs no siblings and no install |

Verify-block engine conformance: two `sh` blocks, both repo-root-relative, no `cd`, no absolute
checkout path, no cargo command (so no `CARGO_TARGET_DIR` export is required), both well inside
the 120 s limit, and neither writes inside the footprint (the test writes only under `mkdtempSync`).

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL — 72/100**, two unresolved blocking findings.
Unresolved blocking findings: F1 (`src/coordinator.ts` in the PRD footprint would sweep another session's uncommitted work into this PRD's collection receipt); F2 (the 90 s ceiling is derived from `startup_timeout_secs` when `verify_timeout_secs` = 300 is the bound that governs a settling attach, and no cold attach was measured).
Rounds used / remaining: 1 / 4.
Next action: bounded revision — remove `src/coordinator.ts` from the prd.md footprint, re-derive or remove the launcher's timeout ceiling and correct the Remaining-risk bullet, record the `--yolo` delta, qualify the `takeover.test.ts` path and bound the "constructs nothing" claim; then present round 2.

## Round 2 — 2026-09-16

Presented revision: superproject `fb44521` (round 1 reviewed at `47b01e6`; the superproject HEAD
has moved for unrelated collections). `live.ctg` gitlink unchanged at `4cbb053`, and both footprint
files are clean at it (`git -C live.ctg status --porcelain -- src/launch.ts
.cartridge/tests/integration/launch.test.ts` → empty). `live.ctg` remains dirty with other
sessions' work (`M src/coordinator.ts`, `M src/server.ts`, `M src/auth.ts`, `M src/control.ts`,
`M cartridge.json`, `M mcp/cartridge.json`, `M .cartridge/docs/README.md`, `M .cartridge/help.md`,
`?? src/voice.ts`, `?? .cartridge/tests/integration/{delegate,voice}.test.ts`) — none of it inside
this PRD's footprint any more.

| Input | Content digest |
| --- | --- |
| Plan | `prds/…/prd.md` — `848368a724c90f6319ecee52035c727e4d64b20d3b6148a74642e53b48098f01` (was `70c5dbba…`) |
| Specs | `specs/spec01.md` — `bbed9966bafc039f58d2ceec3407025407bfb6dc8b7615f39cd53a1bb0ccb8de` (was `ddcd5670…`) |
| Prototype | `.state/loop/…/attempt-2.patch` — `1cb6984cc27d78b10d6de7e8eaddef9f8512e285e6756b94207f7136d3b7380a`; round 1's `attempt-1.patch` — `1d678d9e29c77e9304da698b2eb14bdfff18cb3b3f0bbf86e066710ad41ff2d5` (kept, unchanged) |
| Analyst report | `.state/loop/…/analyst-2.md` — `6b132393de8fe6c7f326ff7751b5d5fae9c412ff58477172a6373bcd3bdb8b48` |
| Material contracts/dependencies | **unchanged since round 1**, re-hashed: `live.ctg/src/launch.ts` `285437c6…`; `live.ctg/.cartridge/tests/integration/launch.test.ts` `0b0dbb1e…`; `live.ctg/src/coordinator.ts` (dirty) `64dd1eeb…`; `cartridge.ctg/src/cli/host.rs` `5158eef8…`; `cartridge.ctg/.cartridge/settings.json` `58dce7c1…`; `~/.cartridge/config.lua` **absent**; `/Users/feb/dev/cartridge/.cartridge/config.lua` — no `host` section |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Unchanged shape, one outcome, one owner, still well under 400 words. **F3 closed:** the `--yolo` delta is now a Remaining-risk bullet with the full chain, and it states the direction (a policy bypass **lost**, not gained) plus the workaround. I re-verified every leg: `launch.ts:52` spawns `["--yolo","daemon"]` today; `src/cli/mod.rs:87-89` sets `YOLO_ENV`; `YOLO_ENV == "CARTRIDGE_YOLO"` (`src/transport/settings.rs:188-191`); `settings::apply` merges `{"yolo": true}` into each cartridge declaring it (`src/settings/mod.rs:14-19`) — `agent.ctg/cartridge.json:100`, `proxy.ctg/cartridge.json:75`, `memo.ctg/cartridge.json:129`; `spawn_daemon` passes only `--dir <project> daemon` (`host.rs:110-140`) and `args.rs:163-171` refuses `--yolo` against an existing daemon. **−1 (F6):** the bullet's *cost* claim is wrong. `spawn_daemon` builds a plain `std::process::Command` and so **inherits the environment** of the `cartridge run` that spawns it, and `yolo()` is a bare env read — so `env:{...process.env,CARTRIDGE_YOLO:"1"}` on `command()`'s `Bun.spawn` would restore the old composition mode in one line *inside* the footprint. The refusal is still right, but it rests on the principle the same bullet already states ("one daemon serves every instance, so no instance may set its mode"), not on "it is not a one-line change inside the footprint". Correct the clause so a later reader does not rediscover the env path as a cheap fix. |
| Ownership and reuse | 19 | **F1 closed and independently confirmed.** `prd.md` frontmatter `footprint` is now exactly `src/launch.ts` and `.cartridge/tests/integration/launch.test.ts`; `spec01.md` declares the same two, so `feet()` (`prd.ctg/src/planner.ts:5-9`) unions to those two paths and `collect` can no longer stage `src/coordinator.ts`'s 60 uncommitted lines (`prd.ctg/src/lifecycle.ts:143-158` — it stages and commits every changed path in `feet(prd)` and throws on any changed path outside it). The union still covers everything the spec touches: `attempt-2.patch` modifies exactly those two files and nothing else. The PRD body's replacement sentence records the reason correctly. The Verify block's `grep -q "phase='interrupted'" src/coordinator.ts` keeps working — it is a *read*, the lane is a full `git worktree add … HEAD` (`lifecycle.ts:224`), and I confirmed the string is present both at `HEAD:src/coordinator.ts:30` and in the dirty worktree at `:35`, so both collection passes are green today. Reuse is now better than round 1: the F2 fix is a **deletion** that hands the bound back to the process that reads the settings. **−1:** that third grep is a gate on a file outside the footprint that another session is actively editing; it passes today, but pass 2 runs in the real submodule and a peer's rename of that literal would turn this PRD red for reasons it does not own. A comment saying so, or pinning a less fragile literal, would remove the coupling. |
| Dependencies and implementable slices | 20 | **F4 closed:** both references now read `<superproject>/.cartridge/tests/integration/takeover.test.ts` (`spec01.md:40` in "Option chosen", `:209` in Acceptance box 3, the latter now citing `:303`), each saying explicitly it is not live.ctg's own `.cartridge/tests/integration/`. `needs` still names the done sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently` (`f364f46`). Step 1 now names `attempt-2.patch`, which I confirmed applies clean to a pristine copy of the gitlink (`git apply --check` → 0, then `git apply` → 0). One slice, no split needed. |
| Observable acceptance and baseline evidence | 18 | **Round 1 note (b) closed — reproduced, not taken on trust.** The fake now answers a `daemon` argv with exit 0, so against unpatched `launch.ts` the old `host.on("exit")` handler exits 0, `expect(code).toBe(0)` passes, and the run reaches the assertion that names the outcome: both mixed cases fail at `.cartridge/tests/integration/launch.test.ts:48` on `expect(calls.filter(args=>args.includes("daemon"))).toHaveLength(0)` — `Expected length: 0, Received length: 1` (exit 1, 0 pass / 2 fail). The analyst's whole table reproduces: patched **0** (2 pass, 16 assertions, ~1.0 s), base **1** (`expect(ui).toBeDefined()`), Verify block 2 red at base on `src/launch.ts:52`, and both blocks green in a bare lane with `node_modules` removed. The rewritten assertions are stronger than round 1's: zero `daemon` argv, zero bare `status`, the first attach is literally `["run","live",{"op":"status"}]`, `trust` ran first, exactly one `{"op":"open"}`, and `cold=true` forces a second attach. `bun run check` (tsc) also passes on the patched copy with the siblings symlinked (exit 0). **−2:** unchanged from round 1 and inherent to the scope — only box 1's live-side half is observable inside this repo; boxes 1 (process count) and 3 (concurrency) are honestly delegated, each naming whose proof covers the rest. |
| Failure, recovery and compatibility | 16 | **F2 closed on substance; I re-derived all three legs from the source rather than from the report.** (1) `attach`'s own deadline is `startup_timeout` (`host.rs:59-101`, deadline at `:62`, checked at `:92-99`), `startup_timeout_secs` default **60** (`settings.json:12-18`). (2) `host.rs:72-76` is `Ok(Some(found)) => { settle_remote(&found.0, settings.verify_timeout()).await; return Ok(found); }` — it **returns from inside the branch** and never re-checks `deadline`; `settle_remote` (`host.rs:144-183`) loops while any cartridge is `starting`/`waiting` or the list is empty, bounded by `verify_timeout_secs` default **300** (`settings.json:33-39`). (3) `run` (`host.rs:222-228`) → `client::bail` (`cli/client.rs:91-99`, no client-side timeout) → `Host::bail` (`host/mod.rs:798-814`) → `ctx.bail` (`transport/cartridge.rs:416-425`) → `send` (`:354-395`), which wraps the call in `tokio::time::timeout(prepared.timeout, …)`; that timeout is the event's declared `timeout_ms` or `event_timeout_ms` (`host/plan.rs:294-302`), and `live.ctg/cartridge.json` declares the `live` event with **no** `timeout_ms`, so **60 000 ms** applies. **60 + 300 + 60 ≈ 420 s confirmed.** Neither config layer moves it: `~/.cartridge/config.lua` does not exist and `/Users/feb/dev/cartridge/.cartridge/config.lua` declares no `host` key (`settings/files.rs:31-35` merges global then project; `settings/host.rs:69-93`). **F5 closed** in both spec and PRD body, and the qualification is accurate: `Host::reconcile` (`host/mod.rs:267-330`) keeps a running slot whose plan still resolves (`(Some(mut slot), Some(Ok(plan))) if slot.running.is_some()`) and puts every other planned entry into `State::Waiting` to be started — so an attach can indirectly start a live node, which is exactly when the marking is meant to fire. **Dropping the launcher's kill is the right call**: no fixed number in a Bun script can track three host settings, and killing a settling attach is the one failure this PRD cannot afford. **−2 (F7):** the stated ceiling is wrong in the safe-sounding direction. The readiness loop checks `Date.now()<deadline` only at the *top*, and sets `deadline` after the first attach returns — so a cold, never-ready `just live` runs the `run` child **twice**: ≤420 s, then `deadline=now+60 s`, then a second (warm, socket already answering) attach of ≤360 s before the loop can exit. Worst case ≈ **780 s ≈ 13 min**, not the "~7 minutes" the Remaining-risk bullet records. The related claim that "an attach that keeps failing is now retried at most once" holds only for slow failures; a fast-failing attach (socket answers but does not serve — `client::unanswered`) still retries every ~1.75 s for the full 60 s. **−1 (F8):** "Every invocation already ends by itself, non-zero, with the host's own message naming `<root>/.cartridge/daemon.log`" (spec prose and the new comment at `launch.ts:27-34`) is over-broad. Only `attach`'s startup-timeout error names the log (`host.rs:92-99`); `settle_remote` exhausting `verify_timeout_secs` returns **silently** and the command proceeds to `bail`; an event timeout surfaces as `Error::Remote` naming the key; `client::unanswered` names the socket path and `cartridge stop`. The launcher's own not-ready error does point at `daemon.log`, which is correct. **−1 (F9):** one genuinely unbounded case is not named. `peer.call` (`transport/rpc.rs:239-257`) awaits a oneshot with no timeout, and `settle_remote` checks its deadline only between calls — so a daemon that accepts the connection but never answers `status` (or `reload`) hangs the attach, and now the launcher, **forever**. The old 10 s kill bounded that at ~30 s with a wrong diagnosis; nothing does now. This is upstream's hole (every `run`/`launch`/`mcp` has it) and re-adding a launcher timer would undo F2, so the right resolution is one sentence in Remaining risk qualifying the bound as "as long as the daemon answers its own RPCs" — not a code change here. |
| Reviewer total | **92** / 100 | No blocking findings; above the 90 threshold. |

### Findings and concrete revisions

**F1 — closed.** `src/coordinator.ts` is out of the PRD footprint; `feet()` now unions to exactly
the two spec-declared paths, `collect` can no longer sweep the peer session's 60 uncommitted lines,
and the PRD body records the reason. The Verify block's read of that file still works in both
collection passes (checked at HEAD and in the dirty worktree). Resolution: **closed**.

**F2 — closed.** The launcher keeps no deadline over an attach. The 60 / 300 / 60 000 chain is
re-derived above from `cli/host.rs`, `cli/client.rs`, `host/mod.rs`, `transport/cartridge.rs`,
`host/plan.rs`, `live.ctg/cartridge.json` and `.cartridge/settings.json`, and both config layers are
confirmed silent on `host`. The residual accuracy defects are recorded as F7–F9, none blocking.
Resolution: **closed**.

**F3 — closed with one correction owed (F6).** The delta and its direction are recorded.
Resolution: **closed**; see F6.

**F4 — closed.** Both references qualified as `<superproject>/…`, box 3 now cites `:303`.
Resolution: **closed**.

**F5 — closed.** Qualified in `spec01.md` and in the PRD body's "What changes" bullet, and the
`reconcile` behaviour it names is what the code does. Resolution: **closed**.

**F6 — non-blocking. The `--yolo` bullet's cost claim is false; rest it on the principle.**
Evidence: `spawn_daemon` (`cartridge.ctg/src/cli/host.rs:110-140`) uses a plain
`std::process::Command`, which inherits the parent environment; `yolo()` is
`std::env::var("CARTRIDGE_YOLO") == "1"` (`src/transport/settings.rs:188-191`). Adding
`env:{...process.env,CARTRIDGE_YOLO:"1"}` to `command()`'s `Bun.spawn` in `src/launch.ts` would
therefore restore the old composition mode on the cold path in one line inside the footprint.
Recommendation: delete "it is not a one-line change inside the footprint" and keep only "one daemon
serves every instance, so no instance may set its mode", adding that the env-inheritance path exists
and is deliberately not taken (whoever starts the daemon first would otherwise decide the policy mode
for every later instance).

**F7 — non-blocking. The recorded ceiling understates the launcher by about 2×.**
Evidence: the patched loop is `while(Date.now()<deadline)` with `deadline=Infinity` until after the
first reply, so a cold never-ready run performs two `cartridge run` children: ≤420 s + ≤360 s ≈ 780 s.
Recommendation: change "~7 minutes worst case" in Remaining risk to "~13 minutes (the readiness loop
checks its deadline only between attempts, so one further attach always runs after the deadline is
set)", and soften "retried at most once" to "at most once when each attach is itself slow".

**F8 — non-blocking. Qualify the "ends with a message naming `daemon.log`" claim.**
Evidence: only `host.rs:92-99` names the log; a `verify_timeout_secs` exhaustion in `settle_remote`
returns silently and the command continues. Recommendation: one clause in the spec and in the
`launch.ts:27-34` comment — the host ends the invocation by itself, and *where it times out on the
socket* it names `<root>/.cartridge/daemon.log`; the launcher's own not-ready error names it in the
other cases.

**F9 — non-blocking. Name the one case the bound does not cover.**
Evidence: `transport/rpc.rs:239-257` (`call` awaits an untimed oneshot) and `host.rs:144-183`
(deadline checked only at loop top). Recommendation: one sentence in Remaining risk — the bound holds
as long as the daemon answers its own RPCs; a daemon wedged with an open socket hangs the attach, and
that bound belongs upstream in `cartridge run`, not in a re-added launcher timer.

Disposition: **keep** — proceed to implementation. F6–F9 are four sentences of record in
`spec01.md`'s Remaining risk (plus one code comment), touching no behaviour and no footprint; they
can be folded into the implementation slice's own edit of the spec rather than consuming a round.

### Validation

All work on `rsync` copies under
`/private/tmp/claude-501/-Users-feb-dev-cartridge/0b0c3ecc-8350-4d76-ae7b-7feeb94a710f/scratchpad/r2`,
with `auth.ctg` and `cartridge.ctg` symlinked as siblings. Nothing was written to any real checkout;
**no daemon was started, stopped, replaced or reloaded**, no composition was run, no cargo was run,
and no `prd` transition was performed. `live-new` = gitlink `4cbb053` + `attempt-2.patch`;
`live-mixed` = unpatched `src/launch.ts` + this round's test only; `live-bare` = `live-new` with
`node_modules` removed. Both `## Verify` fenced blocks were extracted verbatim from `spec01.md` and
run as `sh -eu -c "<block>"` from each copy's repo root.

| # | cwd | command | exit |
|---|-----|---------|------|
| 1 | `live-new` | `git apply --check attempt-2.patch` then `git apply` | **0**, **0** |
| 2 | `live-mixed` | `git apply --include='.cartridge/tests/integration/launch.test.ts' attempt-2.patch` | **0** |
| 3 | `live-new` | Verify block 1 — `bun test ./.cartridge/tests/integration/launch.test.ts` | **0** — 2 pass / 0 fail, 16 expect() calls, 1019 ms (1 s wall) |
| 4 | `live-new` | Verify block 2 verbatim | **0** — < 1 s |
| 5 | `live-orig` (HEAD) | Verify block 1 | **1** — 1 pass / 1 fail, `expect(ui).toBeDefined()` at `launch.test.ts:30` |
| 6 | `live-orig` (HEAD) | Verify block 2 | **1** — first grep matched `src/launch.ts:52` |
| 7 | `live-mixed` | Verify block 1 | **1** — 0 pass / 2 fail, **both at `launch.test.ts:48`**, `expect(calls.filter(args=>args.includes("daemon"))).toHaveLength(0)`, `Expected length: 0, Received length: 1` |
| 8 | `live-bare` (no `node_modules`) | Verify block 1 | **0** — 2 pass, 652 ms |
| 9 | `live-bare` (no `node_modules`) | Verify block 2 | **0** — < 1 s |
| 10 | `live-new` | `bun run check` (`tsc --noEmit`), siblings symlinked | **0** |
| 11 | `cartridge` (superproject, read-only) | `git ls-tree HEAD live.ctg`; `git -C live.ctg status --porcelain -- <footprint>` | **0** — gitlink `4cbb053`, footprint clean |

Verify-block engine conformance: two `sh` blocks, both repo-root-relative, no `cd`, no absolute
checkout path, no cargo command (so no `CARGO_TARGET_DIR` export is required), each ≈1 s — far inside
the 120 s limit — both green in a bare lane without `node_modules` and without siblings (rows 8-9),
and neither writes inside the footprint (the test writes only under `mkdtempSync`).

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS — 92/100**, no unresolved blocking finding.
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation. Fold F6–F9 (four recorded sentences in `spec01.md`'s
Remaining risk and one corrected comment in `src/launch.ts`) into the implementation slice; they are
record-only and change no behaviour, so they do not require another review round.
