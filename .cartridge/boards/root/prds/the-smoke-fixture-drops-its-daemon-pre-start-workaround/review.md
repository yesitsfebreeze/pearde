# @root/the-smoke-fixture-drops-its-daemon-pre-start-workaround review history

Plan: @root/the-smoke-fixture-drops-its-daemon-pre-start-workaround (prd.md, specs/spec01.md).
Scope: leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: none.

## Round 1 — 2026-09-19

Plan: @root/the-smoke-fixture-drops-its-daemon-pre-start-workaround
(`prd.ctg/.cartridge/boards/root/prds/the-smoke-fixture-drops-its-daemon-pre-start-workaround/`).
Reviewer: fresh reviewer agent, coordinator-5c-13. This reviewer did not write the plan.
Presented revision: superproject 28314c3 (dirty shared checkout), prd.ctg bdf0370c, cartridge.ctg 324f36e.

| Input | SHA-256 |
| --- | --- |
| prd.md (with the 2026-09-19 scope note) | 4d17d87320007c9ead04e014c716cd9a5c0a9fbc3da1cc15babd7366394a0404 |
| specs/spec01.md | 9f933e926c3fe4cb283cc39ed6a88e8fa5ed977215cd641f75fd01e816331e18 |
| .cartridge/tests/integration/smoke.test.ts (footprint, unchanged) | fe3170082b98a2c3ea090321aa9e0cf15b28994e276221fa1e8de0e2d90d9200 |
| loop/analyst-1.md | e5ac4e71eeb1b5c2e3214b5afd0b9957471ed48fb3c4313d04add8b6a5a720f2 |

### What I checked myself

- **The change.** I built the spec's cold variant from the live file myself (Python splice, with `runtime` pinned to the repo). It is byte-identical to the analyst's `smoke-an/cold.test.ts`, so the recorded mutant and fixed-host runs measured exactly the change the spec prescribes. The unpinned variant passes block 2's logic: one `"daemon"]` left, and no cold-host PRD name.
- **Block 1 on the cold variant** (`sh -eu -c`, cwd = repo root, the block's text with the test path pointing at the scratch copy). It exited 0 in **67 s** at load average 19–20. The combined run took 14.4 s. The 10 cold `mcp` runs took 3.5–7.3 s each. The spec's "Measured at HEAD: exit 0 in 16 s" is a measurement of the *pre-start* fixture, whose `mcp` case runs in about 1 s (`smoke-an/b1.log`). It does not measure the block the implementer will collect.
- **Reap (point 5).** I sampled one cold run every 0.3 s. `cartridge mcp` spawns `cartridge --dir <root>/mcp/builtin daemon --idle-timeout 3600` (`src/cli/host.rs` `spawn_daemon`). Its argv contains `root`, so `pgrep -f root` matches it. Its nodes are `cartridge node` processes of the same binary, each in its own process group, with cwd `<root>/mcp`. `pids(binary).filter(inside)` matches them. After the run, no daemon child was alive. A `ps` diff before and after the full 11-run block showed no smoke process left. Without `reap`, this daemon would idle for an hour. With it, none survive.
- **Socket isolation (point 3), confirmed.** `socket::base()` falls back to `/tmp/cartridge-<uid>` when `XDG_RUNTIME_DIR` is unset or too long. `run_dir = base/<first 12 hex of FNV(path_tag(descriptor))>`, and the descriptor is the scratch project. So every fixture host gets its own `host.sock`, and it cannot attach to the shared daemon (barring a 48-bit tag collision). Side effect: each run leaves a run dir in the shared base (1784 entries there now). This is not new, and it is not this footprint's to fix.
- **YOLO (point 3).** `runProcess` spawns with `{ ...process.env }`. "No environment injected" therefore means the collector's own environment is *inherited*, `CARTRIDGE_YOLO` included if the collector has it. The block's `env -u CARTRIDGE_YOLO` strips it from `bun test`. The fixture's `env` is `{...process.env, CARTRIDGE_HOME}`. `spawn_daemon` adds `--yolo` only when `yolo()` is true. So the whole chain (fixture → `cartridge mcp` → auto-spawned daemon → nodes) runs without YOLO, and trust is exercised for real. Correct as written.
- **Lane and repo passes (point 2).** `lifecycle.ts` `collect`: pass 1 runs in the lane (a superproject worktree, where `.git` is a file). `seedSubmodules` checks `cartridge.ctg` and the modules out at the pinned sha with no `target/`. The fixture's `runtime` is `import.meta.dir/../../..`, meaning the lane, so the modules are linked to lane checkouts that have no dylibs. Pointing only the host at the live binary (`CARGO_TARGET_DIR`) would not help. `CARTRIDGE_SMOKE_BUILT` expects a `<dir>/<module>/debug` layout that the live `*/target/debug` does not have. Building 18 cartridges inside 120 s is not realistic. So the lane skip is justified, not lazy. Pass 1 is vacuous by design. But `evidence = await verify(prd, code)` replaces pass 1's evidence with pass 2's, so the collection receipt records the real repo run, not the skip message. With no lane, the single pass runs in the repo, where `.git` is a directory, and cannot skip. Pass 2 is enough on its own for the gate. Its cost: it runs after `git merge --ff-only`, so a pass-2 failure leaves the change landed with no receipt (see B1).
- **Box 3 evidence.** `smoke-an/mut/src/cli/host.rs:74` shows `settle_remote(&found.0, settings.verify_timeout())`, which is the reverted fix. `mut-target/debug/cartridge` exists. `cold-mut-2.log` and `cold-mut-5.log` fail with `service \`mcp\` unavailable: no active listener`. The fixed host passed 0-fail in 12 + 6 runs (analyst) and 12 runs (mine).
- **Outside failure.** An mcp-board PRD now exists: `@mcp/the-mcp-refresh-test-expects-the-host-s-synthetic-asp-tool` (open, repo `mcp.ctg`, footprint `refresh.test.ts`). The spec still says "No open PRD owns this failure … the coordinator must file" it, and the PRD scope note names a session (`cartridge-cc`) instead of that PRD.

### Scores

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One observable outcome: the suite exercises a genuinely cold start. The rescoping of box 1 is honest: `just smoke` is red for a reason outside this footprint, and the box now names exactly what this file can prove. −2: the scope note and spec cite a session and "no PRD" instead of the filed `@mcp/the-mcp-refresh-test-...` PRD. |
| Ownership and reuse | 19 | One file. Reuses `ok` and `reap`, keeps `stop` for `proxy`, and needs no new helper. −1: the same stale ownership pointer. |
| Dependencies and implementable slices | 19 | `needs` is the done cold-host PRD, and fix d169293 is an ancestor of 324f36e. It is a single slice, and the spec's Change is precise enough to be mechanical. −1: the block depends on the live debug host staying ≥ d169293, which is not stated. |
| Observable acceptance and baseline evidence | 16 | Block 1 is well built: JUnit case names are required per case and per run, the guards use the `if`-form, no cargo runs, and the environment is stripped deliberately. Block 2 is a sound structural check. Box 3 invokes the gate ceiling without spending a round, but its infeasibility argument is concrete and measured, which is acceptable under review-plan step 4. −2: the recorded block timing (16 s) measured the pre-change fixture, not the block as it will run. −1: box 3's "so the cold path is covered here" overstates the coverage. The 11 cold runs per collect catch a revert about 1 − 0.8^11 ≈ 91% of the time, and the box should say that instead of "covered". −1: pass 1 is vacuous. The reason is justified, but the prose should say explicitly that the receipt records pass 2. |
| Failure, recovery and compatibility | 16 | `reap` verified: no stray daemon or node. Sockets are isolated. YOLO is stripped end to end. −3: the only substantive pass runs after the fast-forward, at 56% of the 120 s cap at load 20. A timeout there lands the change without a receipt, and the spec gives no recovery line for it. −1: flake exposure to live module dylibs rebuilt by other sessions during pass 2 is unmentioned. |
| **Reviewer total** | **88 / 100** | |

### Findings

**Blocking**

- **B1 — Block 1's cost is misrecorded, and its headroom is thin in the only pass that counts.** The spec's "exit 0 in 16 s" measured the pre-start fixture. The cold block measures 67 s at load 19–20: 14 s combined plus 10 runs at 3.5–7.3 s. A single slow cold start (the `ok` kill is 25 s) or a heavier load pushes it toward 120 s. That happens in pass 2, after `merge --ff-only`, where a failure leaves code landed and uncollected.
  *Fix:* split block 1 into two blocks, each with its own 120 s: (a) the host check and lane skip, then the combined `CARTRIDGE_SMOKE=all` run with its three case-name checks; (b) the same host check and lane skip, then the 10 cold `mcp` runs. Re-record both timings against the cold variant, with the load average. Add one recovery line: "a pass-2 red after fast-forward: rerun `prd collect` once the host is quiet; the change is already on HEAD."

**Non-blocking**

- **N1 — Stale outside-failure pointer.** Replace "No open PRD owns this failure … the coordinator must file" in spec01, and "reported to its owner (cartridge-cc)" in the prd.md scope note, with `@mcp/the-mcp-refresh-test-expects-the-host-s-synthetic-asp-tool`.
- **N2 — Box 3 wording.** Keep the box and do not add a gate; the ceiling argument holds. Reword it to what is true, for example: "With the cold-host fix reverted, a cold `mcp` run fails about 1 in 5 (recorded: 2 of 12 against the spec's exact variant). Block 1's 11 cold runs catch such a revert about 91% of the time. Not gated. Ticked from the recorded run, and the diff reviewer confirms that the committed branch is that variant." Drop "so the cold path is covered here".
- **N3 — Say where the receipt evidence comes from.** Add one sentence to Verify: with a lane, `collect` keeps pass 2's output as evidence, so the lane skip message never stands as proof.
- **N4 — The block depends on the live host.** State that block 1 uses the live `cartridge.ctg/target/debug/cartridge` and needs it built at or after d169293. A stale debug binary would turn the cold runs red for a reason that has nothing to do with this diff.
- **N5 — Run-dir litter (informational).** Every run adds a dir under the shared `/tmp/cartridge-501`, now 1784 entries. This PRD's 11 runs per pass add to it. It is not in this footprint. File it separately if the owner cares.

### Answers to the coordinator's five questions

1. The box 1 rescoping is honest. Box 3 resting on the recorded run plus the diff reviewer is acceptable. The recorded run measured byte-for-byte the spec's variant, which I verified. Keep box 3, but reword it (N2).
2. Pass 1 is vacuous by necessity: the lane has no module dylibs, and using the live host alone cannot fix that. Pass 2 is sufficient as the gate, and its output is what the receipt keeps. The residual risk is timing after the fast-forward (B1).
3. The socket claim is confirmed (`socket.rs` `run_dir` is keyed by the project descriptor's path tag). YOLO is inherited from the collector, because the engine injects nothing but also clears nothing, and the block's `env -u` removes it for the whole process chain.
4. The block fits within 120 s today (67 s at load 20), but only at 56% of the cap. Split it (B1).
5. `reap(root)` does kill the auto-spawned daemon (argv match) and its `cartridge node` children (binary plus cwd match). I observed no strays.

Validation: `sh -eu -c "<block 1 against the scratch cold copy>"`, cwd /Users/feb/dev/cartridge, exit 0 in 67 s (logs in scratchpad `rev1-smoke/b1.log`, `rev1-smoke/xml/`). A process-sampled single cold run gave exit 0 in 4.8 s with no children alive afterwards (`rev1-smoke/sample.txt`). No edits to the live checkout. No daemon replace, reload or trust change.
User rating: not required under delegation.
Result: FAIL (88 < 90; one blocking finding).
Unresolved blocking findings: B1.
Rounds used / remaining: 1 / 4.
Next action: a bounded revision of spec01 (split block 1, re-record timing, recovery line) and body-only edits to prd.md (box 3 wording, the outside-failure PRD ref). Then round 2.

VERDICT: FAIL
