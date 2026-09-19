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

## Round 2 — 2026-09-19

Plan: @root/the-smoke-fixture-drops-its-daemon-pre-start-workaround
(`prd.ctg/.cartridge/boards/root/prds/the-smoke-fixture-drops-its-daemon-pre-start-workaround/`).
Reviewer: fresh reviewer agent, coordinator-5c-13. This reviewer did not write the plan and has
not reviewed it before this round.
Presented revision: superproject dirty checkout (HEAD c84b3a4), prd.ctg dirty (spec01/prd.md
revised in place per revision-1.md), cartridge.ctg 324f36e, debug host built 2026-09-19 15:02
(after the cold-host fix d169293, confirmed an ancestor of 324f36e by `git merge-base
--is-ancestor d169293 HEAD`).

| Input | Content digest |
| --- | --- |
| prd.md | 813ce51566df7c2d29322a1a7a659b5556281d86778e0b0ff0b2b1677fe42ad9 (sha256) |
| specs/spec01.md | 636eae74f192315abd8f8e5e5240a7f123cd7f01c4714223fd5886d1e8439415 (sha256) |
| .cartridge/tests/integration/smoke.test.ts (footprint, unchanged since round 1) | fe3170082b98a2c3ea090321aa9e0cf15b28994e276221fa1e8de0e2d90d9200 |
| loop/revision-1.md | author's change log for this round, checked claim-by-claim below |

### What I checked myself

- **B1 (block split + re-timing) — resolved, independently re-verified.** I built the spec's cold
  variant myself from the live `smoke.test.ts` (Python splice of the exact `Change` text: delete
  the `Pre-settled` comment and the daemon-spawn/settle/`stop` machinery, replace with the single
  `ok([...command, "mcp"], ...)` line). It was placed under scratch
  `smoke-r2/cold.test.ts`, with `runtime` pinned to `/Users/feb/dev/cartridge` (out-of-tree
  scratch measurement only; not part of the spec's change, same technique the round-1 reviewer
  used). Ran each spec block verbatim, `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`, cwd = repo
  root, foreground:
  - **Block 1** (combined `CARTRIDGE_SMOKE=all` run): exit 0, **12.27 s**, load average
    31.8→34.1 at start. Matches the spec's recorded "12 s at load average 30" closely.
  - **Block 2** (10 cold `mcp` runs): exit 0, **46.3 s**, load average 36.0→25.8 across the run
    (today's load, ~30 average, matches the task's stated load). Spec recorded "52 s at load
    29–30 (43% of cap)"; mine came in a bit faster but in the same band, ~39% of the 120 s cap.
  Both blocks now carry real headroom under today's load (~30): block 1 at ~10% of its 120 s cap,
  block 2 at ~40%. This is a substantive fix, not just a re-worded number — the split plus
  independent per-block budget resolves B1's actual risk (a single 120 s cap shared by 14 s
  combined + 10 cold runs, previously measured at 67 s but headroom-thin against load spikes).
  The recovery line ("pass 2 runs after the fast-forward... rerun `prd collect` once the host is
  quiet") is accurate: I read `collect()` in `prd.ctg/src/lifecycle.ts` (~lines 174–245). Pass 1's
  `evidence` is reassigned by a second, unguarded `evidence = await verify(prd, code, signal)`
  call that runs only *after* `git(code, ['merge', '--ff-only', candidate])` has already moved
  `code`'s HEAD. If that second `verify()` throws (timeout, or a live module rebuilt by another
  session), the throw propagates out of `collect()` before the receipt (`collection.md`) is
  written or `prd.md` is transitioned to `done` — so the change is on HEAD with no receipt, exactly
  as the recovery text says.
- **Block 3 fails at base, passes on the cold variant — confirmed.** Ran the exact block-3 text
  against the live (unmodified) `.cartridge/tests/integration/smoke.test.ts`: exit 1, "the smoke
  fixture still names the cold-host PRD" (correct — the workaround and its comment are still
  present at HEAD). Ran the same block against the cold variant: exit 0. This is the one block
  that actually distinguishes "changed" from "unchanged."
- **Blocks 1 and 2 at base — they pass too, and that is by design, not a gap.** I ran block 1's
  exact text against the *live, unmodified* `smoke.test.ts` (still has the pre-start workaround):
  exit 0, 7.5 s, all three cases pass. So block 1 (and by extension block 2, which exercises the
  same `mcp` case ten more times) do **not** by themselves prove the workaround is gone — they only
  prove the suite still functions, with or without the change. That is fine because they run
  alongside block 3 in the same collect pass: block 3 is the structural gate on "no daemon
  pre-start" and "comment gone" (spec's box 2 cites it correctly), while blocks 1–2 are the
  behavioural gate that the changed `mcp` case (once block 3 confirms the shape) actually executes
  cold and passes 11 times. Together they are airtight; neither block subsumes the other. One
  wording nit: spec01's acceptance box 1 ("The `mcp` case no longer starts a daemon before
  `cartridge mcp`. All three cases ... (Verify block 1) ... (Verify block 2)") could be misread as
  attributing the no-daemon claim to blocks 1–2 rather than block 3. Box 2 correctly cites block 3
  for that claim, so this is not misleading once both boxes are read together — noted below as
  non-blocking (N7).
- **Lane-skip does not leak into the repo pass.** Confirmed `/Users/feb/dev/cartridge/.git` is a
  real directory (`test -d .git` → true), matching the engine fact that the repo pass runs with
  `.git` as a directory and the lane runs in a worktree where `.git` is a file. The guard
  (`if [ ! -x cartridge.ctg/target/debug/cartridge ]; then if [ -d .git ]; then ... exit 1; fi;
  ... exit 0; fi`) therefore only takes the "lane pass: skip" branch when `.git` is not a
  directory — never in the repo pass. Since the live debug host is in fact built (`-x` true), this
  branch isn't even reached in either pass today; the check is dormant but correctly scoped.
- **No inert guards under `set -e`.** All three blocks use the safe `if grep -qX ...; then :;
  else ... exit 1; fi` / `if grep -qX ...; then ... exit 1; fi` idiom (never a bare `! grep` or an
  `A && B` guard chain). Block 3's `n="$(grep -c ... || true)"` is the correct idiom for capturing
  a zero-match count without the command substitution's nonzero exit aborting the script under
  `set -e` — not a masked failure, since the subsequent `if [ "$n" != 1 ]` still gates on the
  captured value.
- **N1–N5, each checked against the actual revised text, not just revision-1.md's claim:**
  - N1 (stale outside-failure pointer): spec01 "Out of scope" and prd.md's scope note both now
    name `@mcp/the-mcp-refresh-test-expects-the-host-s-synthetic-asp-tool`. Confirmed that PRD
    exists, `state: open`, `repo: mcp.ctg`, footprint `refresh.test.ts` — matches the failure
    described. Resolved.
  - N2 (box 3 wording): both prd.md and spec01's acceptance boxes now say "Not gated... fails
    about 1 time in 5 (recorded: 2 of 12)... catch such a revert about 91% of the time," with "so
    the cold path is covered here" removed. Resolved.
  - N3 (receipt provenance): Verify section states pass 2's output replaces pass 1's in the
    receipt. Confirmed against the actual `collect()` code (see B1 above) — accurate. Resolved.
  - N4 (live host version requirement): Verify section states blocks 1–2 need the live host built
    at or after d169293, with "run `just build runtime` first" as the recovery. Resolved.
  - N5 (run-dir litter): noted under "Out of scope," informational as before. Resolved.

### New, non-blocking observations (not in round 1)

- **N6 — Blocks 1 and 2 hand-roll a JUnit census instead of using the spec template's `test`
  block form.** `prd.ctg/.cartridge/templates/spec.md` explicitly says: "Gate behaviour with a
  `test` block, not a hand-rolled census... a JUnit report written to `$PRD_TEST_REPORT`." Blocks 1
  and 2 instead write their own `$out/all.xml` / `$out/mcp-$i.xml` and grep them directly for case
  names and `<failure|<skipped|<error>`. Functionally this is at least as strict as the canonical
  mechanism (it fails on *any* failure/skip/error in the whole report, not just the named cases),
  and it isn't a text gate an implementation can trivially defeat — but it diverges from the
  template's stated preference and the shared `$PRD_TEST_REPORT`/`pass:` path the engine already
  implements (`runTestBlock` in `lifecycle.ts`). Not a correctness defect; a consistency
  suggestion for a future revision, not this one.
- **N7 — box 1's citation is slightly loose (see above).** A one-clause pointer to block 3 in box
  1 ("...no longer starts a daemon (established structurally by Verify block 3, below)") would
  remove the ambiguity, though box 2 already carries the correct attribution.

### Scores

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | Single observable outcome; box 1's honest rescoping stands from round 1; the stale-pointer deduction (N1) is resolved and independently confirmed against the actual referenced PRD. |
| Ownership and reuse | 20 | One file, reuses `ok`/`reap`/`stop`, no new helper. The round-1 stale-pointer deduction (shared with N1) is resolved. |
| Dependencies and implementable slices | 20 | `needs` is done; d169293 confirmed an ancestor of the built host's commit by me directly. The round-1 deduction (unstated live-host version dependency, N4) is resolved and stated in Verify. |
| Observable acceptance and baseline evidence | 19 | B1 resolved and independently re-verified (12 s / 46 s against my own cold-variant run, both well inside their own 120 s caps). N2 and N3 wording changes confirmed accurate against the actual `collect()`/`verify()` engine code, not just prose. −1: N6, hand-rolled JUnit grep census instead of the template's `test:` block form — a consistency gap, not a correctness one. |
| Failure, recovery and compatibility | 20 | Block split gives real headroom (10% and ~40% of the 120 s cap under today's load ~30, both independently timed). The recovery line is accurate against the real fast-forward-then-verify sequence in `collect()`, including the flake note about a live module rebuilt mid-run (round-1's −1 for this being unmentioned is resolved — it's now the second clause of the same sentence). `reap`/socket/YOLO chain unchanged since round 1 (identical footprint digest) and already independently verified there. |
| **Reviewer total** | **99 / 100** | |

### Findings

**Blocking:** none.

**Non-blocking**

- **N6 — Blocks 1–2 use a hand-rolled JUnit grep census instead of the spec template's `test`
  block form (`run:`/`pass:`, `$PRD_TEST_REPORT`).** Not a defeatable gate as written (it checks
  for *any* failure/skip/error, which is at least as strict as a per-name check), but it diverges
  from the template's explicit guidance and the shared mechanism. Suggest converting in a future
  revision if this spec is touched again; not required to pass this round.
- **N7 — spec01's acceptance box 1 sentence could be misread as attributing the "no longer starts
  a daemon" claim to blocks 1–2** rather than block 3, which is where it is actually proven (box 2
  correctly cites block 3). A one-clause pointer would remove the ambiguity. Purely cosmetic; box 2
  already carries the correct attribution.

### Answers to the coordinator's checklist

1. B1 is resolved: block 1 and block 2 are split with independent 120 s budgets, and I re-timed
   both myself against a freshly built cold variant under today's load (~30): 12.27 s and 46.3 s,
   both comfortably inside cap.
2. N1–N5 are each resolved, checked against the live revised text (not revision-1.md's claim
   alone), and for N3/N4 I independently confirmed the underlying engine behaviour they describe.
3. Block 3 fails at base with the correct message and passes on the cold variant; blocks 1–2 pass
   at both base and the cold variant, which is expected — they gate suite health, not "coldness";
   block 3 is the structural gate, and together the three blocks in one collect pass are sound.
4. The lane-skip guard is correctly scoped to `.git` being a non-directory (the lane worktree);
   the superproject's real `.git` is a directory, so the repo pass can never take the skip branch.
5. No inert guards under `set -e` in any of the three blocks; the one `|| true` (block 3's
   `grep -c`) is a correct idiom for capturing a possibly-zero count, not a masked failure.

### Validation

- `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "<block 1, path pointed at scratch cold copy>"`,
  cwd `/Users/feb/dev/cartridge`: exit 0, 12.27 s (`smoke-r2/block1-cold.log`).
- Same for block 2: exit 0, 46.3 s (`smoke-r2/block2-cold.log`).
- Block 3 against the live (unmodified) file: exit 1, "the smoke fixture still names the
  cold-host PRD" (`smoke-r2/block3-head.sh` run inline).
- Block 3 against the scratch cold copy: exit 0 (`smoke-r2/block3-cold.sh` run inline).
- Block 1 against the live (unmodified) file, to characterize blocks 1–2 at base: exit 0, 7.5 s
  (`smoke-r2/block1-base.log`).
- `git -C cartridge.ctg merge-base --is-ancestor d169293 HEAD` → exit 0 (ancestor confirmed).
- `test -d /Users/feb/dev/cartridge/.git` → true.
- Scratch: `/private/tmp/claude-501/-Users-feb-dev-cartridge/a3492fbd-f726-4514-b5ee-796fd5ea14c1/scratchpad/smoke-r2/`.
- No edits to the live checkout, no daemon replace/reload/trust action, no commits, no PRD
  transitions.

Reviewer identity: fresh reviewer agent, coordinator-5c-13.
User rating: not required under delegation.
Result: PASS (99 ≥ 90; no blocking findings).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation under this passed plan; N6/N7 are optional cleanups for
whoever next touches spec01, not gates on proceeding.

VERDICT: PASS
