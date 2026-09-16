# @root/smoke-passes-mcp-and-proxy review history

Plan: @root/smoke-passes-mcp-and-proxy, `prd.ctg/.cartridge/boards/root/prds/smoke-passes-mcp-and-proxy/prd.md`.
Scope: leaf. `just smoke policy|mcp|proxy` pass against the composed runtime after the stale smoke fixture is fixed.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: superproject 373ef5c (prd.md and spec01.md uncommitted in prd.ctg); mcp.ctg 54e309c (clean), proxy.ctg 1851ccf plus foreign uncommitted edits, router.ctg 2ba93ad plus foreign uncommitted edits, cartridge.ctg cdd3124 (clean), memo.ctg 1634651.

| Input | Content digest |
| --- | --- |
| Plan | `prds/smoke-passes-mcp-and-proxy/prd.md` sha256 `3b6a24c48e54a222e7e258ea8d5fc644a791a97e31f99a2420e3934050c5de0b` |
| Specs | `prds/smoke-passes-mcp-and-proxy/specs/spec01.md` sha256 `3d7cb8ae7e0cebcf6e7bdadc7199aee5d8283033cc53b92b196129f08685cf65` |
| Material contracts/dependencies | `.cartridge/tests/integration/smoke.test.ts` (root 373ef5c); `.cartridge/memos/routine/cartridge-smoke.md`; `.cartridge/justfile` `_fan smoke`; prd.ctg `src/lifecycle.ts` (verificationBlocks, collect footprint status/commit); cartridge.ctg `src/cli/host.rs:68-138`, `src/host/watch.rs`, `src/loader/document.rs:305`, `src/node/mod.rs:363-385`; analyst-1.md and scratchpad `probe/` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | One outcome, and it is grounded: the analyst table shows all three targets failing at HEAD, and a patched copy of the fixture passes all three. Dropping "harness context injected" is justified (the smoke memo makes no model request) and the clause has an owner. -3: the PRD `## Result` still says the sandbox fix belongs in cartridge.ctg and suggests "add cartridge.ctg". The Planning note contradicts both, and neither is marked superseded. The PRD box and the spec's three boxes also say different things ("clean, freshly built" appears only in the spec). |
| Ownership and reuse | 13 | The root owner is right, and the fixture is now in the footprint. The build uses `cargo build --lib`, not `just build`, so it does not relink `~/.local/bin`. -7: the PRD footprint still lists `mcp.ctg`, `proxy.ctg` and `memo.ctg`, but spec01 changes none of them (spec footprint = fixture only). `git status --porcelain -- mcp.ctg proxy.ctg memo.ctg` gives ` M proxy.ctg`: the content is dirty (`1851ccf…-dirty`) while the pointer is unchanged. Collect (`lifecycle.ts`) adds every footprint path in that status to `changed` and runs `git commit --only`. So if the proxy session commits (or the mcp lane `lane/mcp-deferred-tool-band` advances) before collection, that foreign pointer move lands in this receipt. |
| Dependencies and implementable slices | 17 | Both needs are `state: done`. One small spec with numbered steps and line references. The daemon-attach leaf no longer touches smoke.test.ts. -3: the gate depends on another session committing proxy.ctg (see Observable), and the plan does not say so. It does not check that the host binary `cartridge.ctg/target/debug/cartridge` is at least cdd3124 (today it is: 10:28 vs 10:27, clean tree). |
| Observable acceptance and baseline evidence | 13 | Baseline evidence is strong. `just smoke <t>` blocks fail on any real fixture regression, and the mcp block asserts `memo`. -7: Verify block 1 fails **today and after integration** because proxy.ctg carries foreign uncommitted edits (`.cartridge/docs/README.md`, `tests/unit/tests.rs`, `cartridge.json`, `src/lib.rs`, `src/service.rs`). The gate cannot pass for a reason unrelated to this work, and the spec's acceptance text ("clean, freshly built proxy.ctg") cannot be met while another session holds that tree. The analyst showed that both the dirty dylib (10:30) and a HEAD build pass the proxy smoke. In the last block, `! grep -n '"builtin", module' "$f"` is exempt from `sh -e` and is not the last command, so it can never fail. `grep -q CARTRIDGE_HOME` / `grep -q '"memo"'` are weak shape checks. |
| Failure, recovery and compatibility | 15 | Live-daemon isolation holds. The scratch socket tag comes from the scratch `.cartridge` hash. `CARTRIDGE_HOME` and pre-trust keep the real `~/.cartridge` out. An in-place `cargo build --lib` does not hot-reload the live project daemon: the watched sources are `cartridge.json` plus the entry (`document.rs:305`), not the dylib. Block 1 also stops a build of foreign dirt. The 30 s leak poll catches a fixture that stops calling `stop`. -5: step 6 runs `stop` and then `rmSync` while the mcp daemon is still alive for ~16 s, so it can write into or fail on a deleted root. Nothing covers `cargo` lock contention with other sessions' builds or a cold build within 120 s, and the spec gives no recovery line for it. The `pgrep` pattern also matches another session's concurrent smoke run (false leak). |
| Reviewer total | 75 / 100 | FAIL (below 90; two blocking findings). |

Findings and concrete revisions:

1. **BLOCKING: the gate is unpassable while proxy.ctg has foreign dirt.** Evidence: `git -C proxy.ctg status --porcelain --untracked-files=no` lists 5 modified files from another session, so Verify block 1 exits 1. Revision: this plan changes no submodule, so do not require clean trees for them. Build only a clean tree, and never build foreign dirt:
   ```sh
   for m in mcp proxy; do
     if [ -z "$(git -C $m.ctg status --porcelain --untracked-files=no)" ]; then cargo build --lib --manifest-path $m.ctg/Cargo.toml
     else echo "$m.ctg has foreign edits: smoking its existing dylib" >&2; fi
   done
   ```
   Split this into one block per module if 120 s is tight. Restate spec acceptance 1 as "against the current mcp.ctg/proxy.ctg dylibs, rebuilt at HEAD when the tree is clean". Add a recovery line: if a build hits a cargo lock or a cold-build timeout, run `cargo build --lib` outside the gate and re-verify.
2. **BLOCKING: the footprint sweeps unrelated gitlinks.** Evidence: ` M proxy.ctg` is in footprint status today, and collect commits every footprint path in that status with `git commit --only`. Revision: narrow the PRD footprint to `.cartridge/tests/integration/smoke.test.ts`. Keep `.cartridge/memos/routine/cartridge-smoke.md` only if the memo text changes (spec01 does not change it). Drop `mcp.ctg`, `proxy.ctg` and `memo.ctg`.
3. Non-blocking: replace `! grep -n '"builtin", module' "$f"` with `if grep -n '"builtin"' "$f"; then echo "builtin root is back" >&2; exit 1; fi`.
4. Non-blocking: in step 6, after `stop`, poll up to 30 s until the scratch daemon is gone (for example, `stop`/status fails or no `--dir <root>` process remains). Only then `rmSync`.
5. Non-blocking: mark the PRD `## Result` diagnosis items 2–3 and "add cartridge.ctg" as superseded by the Planning note, and align the PRD box with the spec acceptance.
6. Non-blocking: add a host-freshness precondition (`cartridge.ctg/target/debug/cartridge` newer than the `cartridge.ctg` HEAD commit time, or fail with "run just build runtime"). Scope the leak `pgrep` to process groups started by this run, or accept and document the false positive from concurrent smoke runs.

Disposition: revise (keep the scope; narrow the footprint; rework Verify blocks 1–3 and the fixture-shape block).
Validation (cwd /Users/feb/dev/cartridge, read-only; no smoke, build or daemon command run):
- `git status --porcelain -- mcp.ctg proxy.ctg memo.ctg router.ctg` gives ` M proxy.ctg`, ` M router.ctg`.
- `git diff --submodule=short` gives proxy `1851ccf…-dirty` with the pointer unchanged.
- `git -C {mcp,memo,cartridge}.ctg status` is clean. The mcp gitlink = lane head 54e309c.
- Dylib mtimes: mcp 10:42, proxy 10:30, router 10:36, host 10:28.
- `pgrep -fl 'cartridge.*daemon'`: no `cartridge-*-smoke-*` daemon running.
- Both needs are `state: done`.
- sha256 via `shasum -a 256`.

Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: 1 (Verify block 1/acceptance cannot pass while proxy.ctg has foreign dirt); 2 (footprint includes mcp.ctg/proxy.ctg/memo.ctg gitlinks that the spec does not change).
Rounds used / remaining: 1 / 4.
Next action: one bounded revision of prd.md footprint/Result and spec01 Verify blocks and acceptance, then round 2 review.

## Round 2 — 2026-09-16

Presented revision: superproject 373ef5c (prd.md and spec01.md uncommitted in prd.ctg). mcp.ctg 54e309c is clean. proxy.ctg 1851ccf has foreign edits to 5 files, including `cartridge.json` (`"listener": "listen"`), `src/lib.rs` and `src/service.rs`. router.ctg 2ba93ad has foreign edits to 3 files. cartridge.ctg cdd3124 now **also has foreign edits** (`src/loader/document.rs`, `src/loader/mod.rs`, `src/node/mod.rs`, trust tests, mtimes 10:44:27–10:45:30).

| Input | Content digest |
| --- | --- |
| Plan | `prds/smoke-passes-mcp-and-proxy/prd.md` sha256 `dd0d0e530804725850dd10e9dfe223120d2abc235cc6b046515b448a0bd4b14e` |
| Specs | `prds/smoke-passes-mcp-and-proxy/specs/spec01.md` sha256 `5a35a1e52d1647f71d552643ac07df5db52f3211752005e8e77b221a5fb577bd` |
| Material contracts/dependencies | `.cartridge/tests/integration/smoke.test.ts` (root 373ef5c); `.cartridge/memos/routine/cartridge-smoke.md`; `.cartridge/justfile` `_fan smoke`; `.cartridge/init.lua` (router, mcp, proxy and 14 more modules are composed); analyst-1.md and scratchpad `probe/smoke.test.ts` (HEAD worktrees, `trust runtime`); artifact mtimes: host 10:45:33, mcp 10:42:26, proxy 10:30:38, router 10:36:35 |

Round-1 findings:
- B1 (gate cannot pass while proxy.ctg is dirty): resolved as stated. Blocks 1 and 2 build only a clean tree, and today both exit 0. A recovery line was added.
- B2 (footprint swept gitlinks): resolved. The footprint is the fixture only, and `git status --porcelain -- .cartridge/tests/integration/smoke.test.ts` is empty.
- Findings 3–6: resolved. The builtin grep is now an `if`, so it fails. Step 6 polls before `rmSync`. `## Result` is marked superseded. The PRD box matches the spec. Block 3 adds a host-freshness check. The leak `pgrep` is scoped to a temp dir the block owns.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome. The dropped clause has an owner. -2: the spec baseline says cartridge.ctg is clean and that no product code blocks the smoke. The first is no longer true: the host binary (10:45:33) was built after foreign cartridge.ctg edits (10:45:30). |
| Ownership and reuse | 19 | Footprint = the fixture. No submodule change. `cargo build --lib`, not `just build`. -1: the HEAD-worktree technique the analyst already used for proof (`probe/`, `PROBE_OVERRIDE`) is not reused where the gate needs HEAD evidence (see finding 1). |
| Dependencies and implementable slices | 16 | Both needs are done. Steps are concrete. Analyst probe 3 confirms `trust runtime` works. -4: the gate result now depends on three foreign WIP trees that the smoke loads: proxy (its manifest and dylib), router (dylib) and cartridge (the host). The plan names only mcp/proxy dirt and does not declare this dependency. |
| Observable acceptance and baseline evidence | 12 | Before integration, blocks 4–7 fail for the fixture's reasons (ENOENT `builtin/…`, builtin grep). That is a good baseline. -8, BLOCKING: block 3 compares each artifact's mtime only to its HEAD **commit time**. Today it exits 0 while the proxy dylib contains foreign `src/lib.rs`/`service.rs` edits (sources 10:27:20 < dylib 10:30:38) and the host contains foreign loader/node edits. So "not older than HEAD" certifies HEAD+dirt as current. It also cannot detect a dylib that is stale against the dirty tree it is paired with. "Smoking its existing dylib" is also not what happens: the fixture links the whole `proxy.ctg` folder, so the dirty `cartridge.json` (`listener`, which the host binds per the dirty cartridge.ctg loader) is loaded whatever the dylib is. A pass therefore proves the fixture against another session's unfinished listener feature. It does not prove the gitlinks the receipt commits (proxy 1851ccf, cartridge cdd3124). A failure could come from that WIP. Nothing in the gate log records which revision or dirt was smoked. |
| Failure, recovery and compatibility | 17 | Live-daemon isolation holds (scratch `CARTRIDGE_HOME`, scratch-keyed daemon, the leak poll, stop before rmSync). Recovery for cargo locks and cold builds is present. -3: in blocks 5 and 6, a failing `just smoke` exits under `sh -e` before the leak poll and before `rm -rf "$t"`. The poll is skipped exactly when a daemon is most likely to leak, and the temp dir stays behind (observed: 2 empty `tmp.*` dirs, removed by this reviewer). If a dirty tree's artifact is older than HEAD, block 3 says "rebuild it", which would build foreign dirt, and that is what blocks 1 and 2 forbid. |
| Reviewer total | 82 / 100 | FAIL (below 90; one blocking finding). |

Findings and concrete revisions:

1. **BLOCKING: a dirty-tree pass is not labelled or bound, and block 3 certifies foreign-dirt artifacts as fresh.** Minimal honest revision, keeping the smoke on the working composition, because the change under test is the fixture:
   - (a) Apply the dirty/clean rule and the freshness check to every tree whose code the smoke executes as built: `cartridge.ctg` (host), `router.ctg`, `mcp.ctg`, `proxy.ctg`.
   - (b) In block 3, compare each artifact against the newer of the HEAD commit time and the newest mtime among that tree's dirty tracked files, so a stale artifact fails. On a dirty tree, the failure message must say "wait for the owning session" or "build outside the gate with the owner's consent", never a plain "rebuild".
   - (c) Before the smoke blocks, one block prints `<sub> $(git -C <sub> rev-parse --short HEAD) dirty=$(git -C <sub> diff HEAD | shasum -a 256 | cut -c1-12)` for the four trees.
   - (d) Acceptance and `## Result` must state the revisions the pass ran against. A pass with dirt in proxy.ctg, router.ctg or cartridge.ctg counts as proof of the fixture against HEAD+named foreign edits, not as proof of the committed gitlinks.

   If the PRD must prove the committed composition instead, the stronger alternative (reusing analyst probe 3) is this. Let the fixture accept a per-module link override (for example `CARTRIDGE_SMOKE_LINK=proxy.ctg=<dir>`). Then, for each dirty tree, the gate builds a detached HEAD `git worktree` in a scratch dir the gate owns and smokes that. This costs a worktree in the foreign submodule's git dir and a possibly cold build. Pick one of the two and say which.
2. Non-blocking: blocks 5 and 6 should always run the leak poll and the cleanup: `rc=0; TMPDIR=$t just smoke mcp || rc=$?; <poll>; rm -rf "$t"; exit $rc`.
3. Non-blocking: update the spec baseline line (cartridge.ctg no longer clean; host rebuilt 10:45:33 from dirt). Update analyst-1's "Blocks 1-3 fail loudly on a dirty or stale tree", which is no longer true of the revised blocks.

Disposition: revise (keep scope and footprint; rework Verify block 3, add a revision-record block, and restate acceptance for dirty trees).
Validation (cwd /Users/feb/dev/cartridge; each block extracted from spec01 and run with `sh -eu -c`, before integration; no daemon was started because the fixture fails at symlink time):
- `sh -n` on all 7 blocks: ok.
- block 1: rc=0, 0 s. mcp clean; cargo reported `Finished` in 0.09 s.
- block 2: rc=0, 0 s ("proxy.ctg has foreign edits").
- block 3: rc=0, 0 s (passes over the dirty proxy dylib and the dirty host).
- block 4 (`just smoke policy`): rc=1, 1 s (ENOENT `builtin/policy`).
- block 5: rc=1, 0 s (ENOENT `builtin/auth.ctg`; leak poll and cleanup skipped).
- block 6: rc=1, 0 s (same).
- block 7: rc=1, 0 s (line 38 still links builtin).
- `git -C {proxy,router,cartridge}.ctg status --porcelain --untracked-files=no`: dirty (5, 3 and 4 files). mcp.ctg is clean.
- `git -C proxy.ctg diff cartridge.json`: adds `"listener": "listen"`.
- Dirty-source mtimes (`stat`) were compared with artifact mtimes (above).
- `pgrep -fl smoke-`: none.
- sha256 via `shasum -a 256`.

Reviewer identity: independent reviewer agent r2 (coordinator cartridge-c4).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: 1 (freshness and dirty-tree proof are not bound to the revisions actually smoked; cartridge.ctg and router.ctg dirt are unaccounted for).
Rounds used / remaining: 2 / 3.
Next action: one bounded revision of spec01 Verify blocks 3, 5 and 6 plus a revision-record block and the dirty-tree acceptance wording, choosing the labelled-dirty or the HEAD-worktree option; then round 3.

## Round 3 — 2026-09-16

Presented revision: superproject 6b5f208 at review time (the round started at 373ef5c; other sessions advanced it). No uncommitted changes in the PRD directory. Submodule HEADs at review, all trees clean: mcp.ctg 54e309c, proxy.ctg 96ef23c, router.ctg fa83bb4, cartridge.ctg 771e046, memo.ctg 1634651. proxy.ctg, router.ctg and cartridge.ctg were committed at 10:51:32, during this review. The router.ctg gitlink in the superproject still lags its HEAD.

| Input | Content digest |
| --- | --- |
| Plan | `prds/smoke-passes-mcp-and-proxy/prd.md` sha256 `7118673bf0b0c2bba1288131ee01776e63465cfc92fe31a6ecc56e92e5779f5f` (matches the hand-off) |
| Specs | `prds/smoke-passes-mcp-and-proxy/specs/spec01.md` sha256 `87fd980e279c1409833c6701028f8c69c9925743c869dfe441cb67bf2d26f8a8` (matches the hand-off) |
| Material contracts/dependencies | `.cartridge/tests/integration/smoke.test.ts` sha256 `1cba673199ece153…` (unchanged, stale fixture); `.cartridge/memos/routine/cartridge-smoke.md`; `.cartridge/justfile` `_fan smoke`; `.cartridge/init.lua` (17 entries); prd.ctg `src/lifecycle.ts:45` (`sh -eu -c`, `timeout: 120_000`); cartridge.ctg 771e046 "Restart a cartridge in the running host when its native module is rebuilt" (`src/loader/document.rs` watches `native_candidates`, including `target/debug/lib<name>.dylib`); proxy.ctg `Cargo.toml:17` `evidence = { path = "../memo.ctg/evidence" }`; artifacts: host 10:45:33, mcp 10:42:26, proxy 10:30:38, router 10:36:35; project daemon pid 8989 started 10:42:47 |

Round-2 findings:
- B1 (a dirty-tree pass is not labelled or bound): resolved by taking the stronger option. There is no dirty fallback. Block 1 requires clean trees. Blocks 2–5 rebuild all four trees, including the router and the host binary. Block 6 re-checks cleanliness and logs the full HEAD shas. The mtime freshness check is gone; cargo fingerprints handle freshness. Two gaps remain: new findings 2 and 3.
- N2 (trap/cleanup): resolved. Checked with a synthetic copy of the trap under `/bin/sh -eu -c` (bash 3.2): a failing command gives rc=1 and the dir is removed; a pass gives rc=0 and the dir is removed; a lingering process naming `$t` with a passing command gives the "leaked" message, rc=1 and the dir removed; a leak with a failing command gives rc=1. The trap keeps the original exit status unless it calls `exit 1`. `pgrep -f "$t"` is scoped to the block's own realpath temp dir, and the other sessions' `.tmp*` scratch daemons that are running do not match it.
- N3 (stale baseline): resolved at hand-off, but stale again. The trees became clean at 10:51 with new HEADs, so "other sessions hold uncommitted edits" and the proxy/router/cartridge shas in the baseline no longer hold.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome. The dropped clause has an owner, and the box and spec agree. -2: the baseline is stale again (see N3). |
| Ownership and reuse | 18 | The footprint is only the fixture, and no submodule changes. Builds use plain `cargo build`. -2: the build blocks write shared artifacts in the real repo that live hosts load (see finding 1), and the plan does not reuse an isolated target or worktree. |
| Dependencies and implementable slices | 17 | Both needs are done. The steps are concrete, and the wait mechanics are simple: block 1 fails loudly and names the tree. -3: proxy.ctg compiles `../memo.ctg/evidence`, and memo.ctg also provides the `memo` tool the acceptance asserts. memo.ctg is neither in the clean set nor logged. |
| Observable acceptance and baseline evidence | 17 | Before integration, the smoke and shape blocks fail for the fixture's own reasons, which is a correct baseline. Block 6 binds the HEAD shas. -3: block 6 logs HEAD after the builds. A commit between block 1 and block 6 leaves the tree clean with a new HEAD, so the log names a revision the artifacts were not built from. Dirt in memo.ctg would enter the proxy dylib without being labelled. |
| Failure, recovery and compatibility | 13 | Recovery for cargo locks and cold builds is present, cleanup is verified, and scratch `CARTRIDGE_HOME` is used. -7, BLOCKING: the spec says "No block touches the project daemon", but committed cartridge.ctg HEAD 771e046, which is the very tree the gate requires, watches each cartridge's `target/debug/lib<name>.dylib` and restarts that cartridge when the file is rebuilt. Once the project daemon runs a HEAD binary (after any `daemon --replace`, which is routine), blocks 2–4 restart mcp, proxy and router inside the live daemon serving other sessions whenever cargo relinks. A proxy restart drops in-flight model requests. The running pid 8989 (started 10:42:47) predates the feature, so this is latent today. Also noted, without a separate deduction: the worst case in blocks 8/9 is the 90 s test timeout plus the 30 s trap poll plus the `just tools` preamble, which is at least 120 s. The engine timeout would then cut the trap short. |
| Reviewer total | 83 / 100 | FAIL (below 90; two blocking findings). |

Findings and concrete revisions:

1. **BLOCKING: the gate's rebuilds restart cartridges in the live project daemon under committed cartridge HEAD.** Evidence: 771e046 `src/loader/document.rs` adds `native_candidates(root, name)` to the watched sources, and its commit message states the intent. The project daemon composes the same `mcp.ctg`, `proxy.ctg` and `router.ctg` directories whose `target/debug` blocks 2–4 write. Pick one option:
   - (a) Build into a gate-owned `--target-dir` (for example `$HOME/.cache/cartridge-smoke-target` or a scratch dir), point the host at that dir with `CARGO_TARGET_DIR`, and have the fixture link each native module's dylib from that target dir into a scratch copy of the module instead of symlinking the real module folder.
   - (b) If restarting the live cartridges on a HEAD rebuild is acceptable (it is what `just build` does), correct the spec's isolation sentence to say so, make the coordinator record that decision, and run the build blocks only while no session has an in-flight proxied request.
   Either way, remove the false "No block touches the project daemon" claim.
2. **BLOCKING: memo.ctg dirt is unaccounted for.** Evidence: proxy.ctg `Cargo.toml:17` path-depends on `../memo.ctg/evidence`, so block 3 compiles memo.ctg's working tree into the proxy dylib. The mcp acceptance asserts memo's tool. Revision: add `memo.ctg` to the loops in blocks 1 and 6, add it to the acceptance and box wording, and state whether memo's own dylib is rebuilt (`cargo build --lib --manifest-path memo.ctg/Cargo.toml`) or smoked as built.
3. Non-blocking: make the logged shas bind to the build. Record `git rev-parse HEAD` per tree in block 1 into the log, then in block 6 compare against the same list (for example by re-deriving it and failing on a mismatch with "HEAD moved during the gate: re-verify"). Also print the superproject gitlink (`git ls-tree HEAD <sub>`) next to each HEAD. The receipt commits only the fixture, so a gitlink that lags HEAD (router.ctg now) means the committed superproject does not name the proven revision.
4. Non-blocking: keep blocks 8/9 inside 120 s. Lower the trap poll to about 10 s (the fixture already polls 30 s after `stop` and kills the daemon itself), or lower the fixture test timeout to 75 s.
5. Non-blocking: refresh the spec baseline to the 10:51 commits (proxy 96ef23c, router fa83bb4, cartridge 771e046), with the artifacts still older than them.
6. Non-blocking: `pkill -f "$t"` kills only processes whose argv names `$t`. Children of a leaked daemon that don't name it survive, and `rm -rf` runs without waiting. This is acceptable as a last resort; mention it or follow the kill with a short re-poll.

Disposition: revise (keep the scope, footprint and clean-tree decision; fix the build isolation claim or the build target, and add memo.ctg to the bound trees).
Validation (cwd /Users/feb/dev/cartridge; blocks were extracted from spec01 by awk and run with `sh -eu -c` before integration; build blocks 2–5 were not run, to avoid relinking shared artifacts under live hosts; no daemon was started because the fixture fails at symlink time):
- `sh -n` on all 10 blocks: ok.
- Block 1: rc=0. The trees became clean at 10:51. Earlier in this review, `git status --porcelain` showed 5, 3 and 4 dirty files in proxy, router and cartridge.
- Block 6: rc=0. It printed mcp 54e309c…, proxy 96ef23c…, router fa83bb4…, cartridge 771e046….
- Block 7: rc=1, 0 s (ENOENT `builtin/policy`).
- Blocks 8 and 9: rc=1, ≤1 s (ENOENT `builtin/auth.ctg`). The `tmp.*` count in `$TMPDIR` was 68 before and 68 after, so the trap removed its dirs.
- Block 10: rc=1 (line 38 still links builtin).
- Trap semantics were checked with a scratch copy (`trap.sh`, modes fail/pass/leak/leakfail), with the results above.
- Reviewed with `git -C cartridge.ctg show HEAD`, `ps -axo pid,lstart,command` for the daemons, and `grep` of proxy.ctg `Cargo.toml` for the path dependency.
- sha256 via `shasum -a 256`.

Reviewer identity: independent reviewer agent r3 (coordinator cartridge-c4).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: 1 (the gate's in-place rebuilds restart cartridges in the live project daemon under cartridge HEAD 771e046; the isolation claim is false); 2 (memo.ctg is compiled into proxy and asserted by the mcp smoke, but is not bound as clean or logged).
Rounds used / remaining: 3 / 2.
Next action: one bounded revision of spec01 (the build target or an explicit restart decision; memo.ctg added to blocks 1 and 6 and to the acceptance; sha binding; the 120 s bound), then round 4.

## Round 4 — 2026-09-16

Presented revision: superproject 1e37c78 at review time. Submodule HEADs (superproject gitlink = HEAD for all five): mcp.ctg 54e309c (clean), proxy.ctg 96ef23c (clean), router.ctg 943eef3 (**7 dirty files from another session**: `cartridge.json`, `src/catalog.rs`, `src/health.rs`, two unit tests, two docs), memo.ctg 1634651 (clean), cartridge.ctg 771e046 (clean).

| Input | Content digest |
| --- | --- |
| Plan | `prds/smoke-passes-mcp-and-proxy/prd.md` sha256 `abdb7c78d2416699191b74c152efae9a6b9c976ba0063aa823beacc8675b3de1` (matches the hand-off) |
| Specs | `prds/smoke-passes-mcp-and-proxy/specs/spec01.md` sha256 `d85ebb2591eb554f623e86041c96bedf9f6216a4a4cc4c1e70587730a6372a62` (matches the hand-off) |
| Material contracts/dependencies | `.cartridge/tests/integration/smoke.test.ts` (unchanged, stale); `.cartridge/justfile` `_fan`/`_one smoke` (no build step; runs the smoke memo); `.cartridge/memos/routine/cartridge-smoke.md`; `.cartridge/init.lua`; prd.ctg `src/lifecycle.ts:37,45`, `src/process.ts:67-73` (timeout kills the process group); cartridge.ctg 771e046 `src/loader/document.rs:304-311`, `src/loader/mod.rs:65-85`, `src/node/mod.rs:363-368`, `src/cli/host.rs:68-96,157-179,234,328`, `src/cli/client.rs:9` (`status` never spawns), `src/trust/mod.rs:19,81-98`; `mcp/proxy/router/memo.ctg/cartridge.json` (`entry: "init.lua"` at module root) and `Cargo.toml` `[lib] name`; `~/.cache/cartridge-smoke-target/*/debug/lib{mcp,proxy,router,memo}.dylib` and `cartridge.ctg/debug/cartridge` present; filed `@root/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls` |

Round-3 findings, checked against the code:
- B1 (rebuilds hot-restart live cartridges): **resolved.** `native_candidates` is `<root>/lib<sym>.dylib`, `<root>/target/{release,debug}/…`. The watched root and the load root are both `entry.parent()`, and every rebuilt module's entry is `init.lua` at the module root. So a build with `--target-dir ~/.cache/cartridge-smoke-target/<tree>` changes no path the live daemon watches. No module has a root-level dylib (`find … -name '*.dylib' -not -path '*/target/*'` is empty), so a copy can't load a stale live dylib through a copied symlink. The dylib basenames match the watched names (`libmcp`, `libproxy`, `librouter`, `libmemo`). `_one smoke` runs no build, so no block writes a live `target/`. The only watcher of the copies is the scratch host.
- B2 (memo.ctg unchecked): **resolved.** memo.ctg is in blocks 1 and 7, is built in block 2 and is copied by step 1. The acceptance and the PRD box name it.
- N3 (HEADs bound): resolved for the builds. Block 1 records `head=` and `gitlink=`, and block 7 fails on a dirty tree or a moved HEAD. See new finding 1 for the gap after the builds.
- N4 (120 s): resolved. Worst case per smoke block is 60 s test timeout + 10 s trap poll + 2 s + preamble. The engine timeout kills the process group (`process.ts:73`). The build blocks were measured at 3–13 s on a warm wrapper cache, and a cold-build recovery line is present.
- N5 (baseline): refreshed, but already stale for router (943eef3 is now dirty).
- N6 (pkill limits): documented.
- Trap cleanup: unchanged from round 3, which verified it. Copied modules pass trust: `trust::own` skips verification for paths under `CARTRIDGE_HOME`, and the copies sit under the realpath'd scratch root.
- Cold-host workaround: it hides no failure this outcome needs. The pre-settle loop stops only when no cartridge is `starting` or `waiting`. It does not require `running`, so a failed memo or mcp still surfaces through the `"memo"` assertion or the `tools/list` reply. `status` goes through `client::ask`, which never spawns a daemon, so the poll can't start a detached competitor. What the workaround does exclude is the worker's cold-start `cartridge mcp` path (`attach` → `spawn_daemon` → `settle_remote`). That path is broken and is owned by the filed PRD, whose acceptance tests it (5 of 5 cold starts). This PRD, though, neither names that PRD nor records the exclusion (finding 3).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome, and the dropped clauses have owners. -2: the PRD box says "a pass proves committed HEAD", but modules other than the five (sessions, harness, agent, fs, pty, …, which shape `tools/list`) load as built from live dirs. The spec says so and the box does not. The cold-start mcp door a worker uses is excluded without a note in the box. |
| Ownership and reuse | 19 | Footprint = fixture only. Reuses `CARGO_TARGET_DIR` (`smoke.test.ts:9`) and the trust home rule. No submodule changes. -1: the filed cold-host PRD is not referenced by ID in prd.md (the Planning note says only "Host race for the coordinator"). |
| Dependencies and implementable slices | 17 | Both needs are done, and every cited line checks out against 771e046. -3: step 6 doesn't say the `status` poll must tolerate a non-zero exit before the socket exists (`client::ask` errors on connect). The inner worst case (30 s status poll + 30 s `run` kill + 10 s SIGKILL = 70 s) exceeds the 60 s test timeout, so a bun timeout skips the fixture's `finally` and leaves cleanup to the trap's `pkill`. `$C/heads` is shared by concurrent gate runs in other sessions, and a second run's block 1 truncates it. |
| Observable acceptance and baseline evidence | 16 | The baseline fails correctly (blocks 1 and 11 below). The mcp block asserts `memo`. -4: (a) the smoke blocks `cpSync` the working trees of mcp/proxy/router/memo **after** block 7's clean/HEAD check. Router is being edited right now, so dirt or a commit that lands during blocks 8–10 is smoked without being recorded, and "a pass proves committed HEAD" can be false. (b) Acceptance box 2 ("No gate block writes a live `<module>/target`") is not observed by any block. |
| Failure, recovery and compatibility | 18 | Isolation holds by code: separate target dirs, copied modules, scratch `CARTRIDGE_HOME`, a tracked daemon child, a process-group kill on engine timeout, and trap cleanup. A recovery line covers cold builds. -2: a bun test timeout skips the fixture's cleanup (see above). The `pkill -f "$t"` fallback misses node children whose argv doesn't name `$t`. This is documented but not re-polled. |
| Reviewer total | 88 / 100 | FAIL (below 90; no blocking finding). |

Findings and concrete revisions:

1. Non-blocking (−4 of the Observable deduction): move the clean/HEAD re-check after the smoke blocks, or repeat block 7 as the last block. The copies are taken from working trees during blocks 8–10.
2. Non-blocking: make acceptance box 2 observable. In block 1, record `stat -f '%m %N' {mcp,proxy,router,memo}.ctg/target/debug/lib*.dylib cartridge.ctg/target/debug/cartridge 2>/dev/null` into `$C/live-mtimes.<run>`. In the last block, diff against a fresh `stat` and fail on a change. Note the caveat that another session's `just build` also changes it, so name that in the message.
3. Non-blocking: in the PRD box or Result, reference `@root/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls`. State that the smoke pre-settles the daemon and does not cover the cold-start `cartridge mcp` path, and that after that fix the pre-settle can be dropped. Qualify "proves committed HEAD" as covering the five trees, with other modules as built.
4. Non-blocking: in step 6, treat a non-zero `status` as "not ready yet". Cap the status poll plus the `run` kill so that the inner total, including the 10 s SIGKILL, stays under the test timeout (for example, a 20 s poll, a 25 s `run` kill and a 60 s test timeout).
5. Non-blocking: key `heads` per run (for example `$C/heads.$$`, passed by name, or written under a gate-owned temp path) so concurrent gates in other sessions don't clobber it.

Disposition: revise (keep the scope, footprint, isolation design and clean-tree decision; move the HEAD re-check after the smokes; observe box 2; link the cold-host PRD).
Validation (cwd /Users/feb/dev/cartridge; blocks extracted from spec01 by awk into this reviewer's scratchpad):
- `sh -n` on all 11 blocks: ok.
- Block 1 (`sh -eu -c`): rc=1, 0 s. "router.ctg has uncommitted changes: wait for the owning session to commit, then re-verify". It rewrote `~/.cache/cartridge-smoke-target/heads` with identical mcp/proxy lines. This is the expected failure on a dirty tree under the accepted coordinator decision.
- Block 11 (fixture shape): rc=1 ("fixture links <runtime>/builtin again", line 38). This is the correct pre-integration baseline.
- Blocks 2–10 (builds, the HEAD re-check and smokes) were **not run**, because router.ctg was dirty at review time.
- Checked read-only: `git status --porcelain` per tree, `git ls-tree HEAD`, `git -C <tree> ls-files --others --ignored` (only empty `.cartridge/bin/` and one debug log are copied), module `cartridge.json` entries and `Cargo.toml` lib names, isolated target contents, and the cited cartridge.ctg and prd.ctg source.
- sha256 via `shasum -a 256`; both match the hand-off.

Reviewer identity: independent reviewer agent r4 (coordinator cartridge-c4).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: none (both round-3 blockers resolved; total below threshold).
Rounds used / remaining: 4 / 1.
Next action: one bounded revision (findings 1–4, optionally 5), then the final round-5 review. Gate execution also waits for router.ctg's owner to commit.

## Round 5 — 2026-09-16

Presented revision: superproject 18fe75d at review time; prd.ctg 522cbf9e with prd.md, spec01.md and review.md uncommitted. Submodule HEADs (gitlink = HEAD, all clean at review time): mcp.ctg 54e309c, proxy.ctg 96ef23c, router.ctg b567168, memo.ctg 1634651, cartridge.ctg 771e046.

| Input | Content digest |
| --- | --- |
| Plan | `prds/smoke-passes-mcp-and-proxy/prd.md` sha256 `85946b8e17ff361462aa157dbac6004548cad16347e085e8ce8a2b157d857c4c` (matches the hand-off) |
| Specs | `prds/smoke-passes-mcp-and-proxy/specs/spec01.md` sha256 `75bc54a7c588d0a90daa8030b7af57d14918c47ac553e39dfa89c6b17e5fdb9a` (matches the hand-off) |
| Material contracts/dependencies | `.cartridge/tests/integration/smoke.test.ts` (unchanged, stale); `.cartridge/justfile` `_fan`/`_one smoke`; `.cartridge/tools/memo-run` (`MEMO_JUSTFILE` under `$TMPDIR`); `.cartridge/memos/routine/cartridge-smoke.md`; prd.ctg `src/lifecycle.ts:21-25,37,39-47,106-175,210-218`, `src/process.ts` (detached spawn, group kill, 1.2 s grace), `src/coordinator.ts:49,70`, `init.lua` (service `timeout_seconds` 600 + 30); cartridge.ctg 771e046 `src/cli/host.rs:68-96,104-136,138-163,165-183` |

Round-4 findings, checked:
- F1 (re-check after the smokes): **resolved.** Block 11 repeats the clean/HEAD check after blocks 8–10.
- F2 (box 2 observable): **resolved.** Block 1 records live `stat -f '%m %N'`; block 12 diffs it and names the other-session `just build` caveat. Globs that match nothing produce identical output both times (`2>/dev/null || true`), so an absent artifact can't cause a false failure; a live build in the window fails with the documented message. Second-resolution mtimes are sufficient because a relink lands seconds after block 1.
- F3 (cold-host PRD, "as built" scope): **resolved** in the PRD box and Planning note.
- F4 (status tolerance, inner bound): **resolved.** Step 6 treats non-zero/unparsable `status` as not ready; mcp inner worst case 2 + 22 + 25 + 10 = 59 s < 75 s; policy 51 s < 60 s; proxy 36 s < 60 s. `run policy` never spawns a detached daemon (`host::run` runs a private host when none is served); `cartridge mcp` against the tracked daemon attaches, and if that daemon died, `spawn_daemon` starts one with argv `--dir <builtin under $t>`, which the trap's `pgrep -f "$t"` sees even though `process_group(0)` escapes the engine's group kill.
- F5 (per-run state): **resolved** with `run.$PPID`. Checked:
  - `verify()` spawns `sh -eu -c` directly (`spawn('sh', …, { detached: true })`, no shell). Reproduced with bun 1.3.14: `$PPID` in the block and in a subshell both equal the bun parent PID, identical for consecutive blocks. It is therefore stable across one run and distinct between concurrent CLI runs.
  - Two passes: with no lane, `collect` calls `verify` **once** (line 137); the post-integration `verify` (line 167) runs only when `tree !== code`. The hand-off's "then again after" does not apply to this path. With a lane the second pass has the same `$PPID`; pass 1's block 12 already removed `$R`, and pass 2's block 1 `rm -rf` + fresh `heads`/`live-mtimes` make each pass self-contained, so the mtime diff never compares across passes.
  - Stale dirs: a failed run leaves `run.<pid>`; only a later run with the same PID clears it. Others accumulate (a few KB each). Harmless, as documented.
  - When `collect` goes through the live daemon's prd service (`init.lua` spawns one long-lived `bun src/service.ts`), `$PPID` is that service's PID for every run; concurrent collects of this one PRD in that service would share `$R`, which claim/state make unlikely.
- Timeout per smoke block: ≤ 75 s test + trap (10 × (pgrep + 1 s) ≈ 10.5 s, `pkill`, 2 s) + `just tools`/bun preamble ≈ 89 s < 120 s. Trap exit status: a failing `just smoke` keeps its status (the trap only overrides with `exit 1` on a leak); observed below.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome (both worker doors pass the composed smoke) with an exact proof boundary: five committed HEADs, other modules as built, cold-start mcp excluded and owned by a named PRD, "harness context injected" rehomed. -1: the single acceptance bullet in prd.md is dense (~150 words), and the Result section keeps superseded "add cartridge.ctg / prd refine" guidance behind a supersede note. |
| Ownership and reuse | 19 | Footprint = fixture only; no submodule change; reuses `CARGO_TARGET_DIR` (`smoke.test.ts:9`), the `CARTRIDGE_HOME` trust rule, `just smoke`. -1: the stale Result text above still names cartridge.ctg as a fix owner. |
| Dependencies and implementable slices | 18 | Both needs done; nine concrete steps with line references that match the fixture; builds, re-checks and smokes are separate blocks. -2: the spec asserts "cwd /Users/feb/dev/cartridge" but does not state how collection avoids a lane. `prd claim` on a `specced` PRD (and `prd run`, `coordinator.ts:49`) creates `.lanes/smoke-passes-mcp-and-proxy`, a superproject worktree with uninitialised submodules, where block 1 sees the lane's own dirty fixture or block 2 finds no `memo.ctg/Cargo.toml`. The failure is safe, but the default dispatch path can never pass. Also unstated: running `collect` through the daemon's prd tool caps the call at 630 s while 13 × 120 s is possible, and runs under that node's confinement. |
| Observable acceptance and baseline evidence | 19 | Every box has a block: HEAD/gitlink log (1, 7, 11), live mtimes (12), temp dir and process leak (trap in 8–10), `memo` tool and fixture shape (13). Baseline reproduced below. -1: the spec baseline still names router 943eef3 (now b567168); blocks 7/11 print "HEAD moved" when `$R/heads` is missing (blocks run by hand as separate shells get different `$PPID`s), a misleading message where block 12 has a guard. |
| Failure, recovery and compatibility | 18 | Isolated target and per-run snapshots, copied modules, scratch home, tracked daemon with SIGTERM/SIGKILL/await, trap poll plus last-resort `pkill`, cold-build recovery, dirty-tree and live-build messages that say what to do. -2: no recovery line for the lane case (collect from `specced` without claiming, or remove the lane); if the engine's 120 s timeout ever fires, its 1.2 s SIGKILL grace cuts the ~13 s trap, so `$t` can survive (precluded by the arithmetic, not handled). |
| Reviewer total | 93 / 100 | PASS (≥ 90, no blocking finding). |

Findings and concrete revisions (all non-blocking; they can be folded in by the implementer without changing the contract, or noted by the coordinator):

1. Non-blocking: state the lane precondition. Collect this PRD from `specced` without `prd claim` (no `.lanes/smoke-passes-mcp-and-proxy`), editing the fixture in the superproject; or, if a lane exists, remove it before collecting. Evidence: `lifecycle.ts:125` (`tree = lane if it exists`), `:216-217` (claim from specced adds the worktree), `coordinator.ts:49`.
2. Non-blocking: run `collect` from the CLI (`just prd collect …`), not through the daemon's prd tool (`init.lua` call timeout 630 s, node confinement).
3. Non-blocking: in blocks 7 and 11 add `test -f "$R/heads" || { echo "block 1 recorded no heads for run $PPID" >&2; exit 1; }`, matching block 12.
4. Non-blocking: refresh the spec baseline to router b567168.
5. Non-blocking (informational): the hand-off's two-pass premise does not hold with no lane; the design is correct either way.

Disposition: keep (proceed to implementation under findings 1–2).
Validation (cwd /Users/feb/dev/cartridge; 13 blocks extracted with the engine's own regex from `lifecycle.ts:37` into this reviewer's scratchpad):
- `sh -n` on all 13 blocks: ok.
- `$PPID` probe: bun 1.3.14 `spawn('sh', ['-eu','-c', …], { detached: true })` ×2 printed `ppid=` and subshell `sub=` equal to the bun PID.
- All five trees were clean immediately before the run, so the non-building blocks 1, 7, 8, 9, 10, 11, 12, 13 were run in order from one bun parent (PID 95728), each via `sh -eu -c`, detached, as the engine does (not stopping on failure, to observe each). Build blocks 2–6 were not run.
  - Block 1: rc=0, 0.2 s. Logged five `head=` = `gitlink=` lines; created `run.95728` with five live mtimes.
  - Block 7: rc=0, 0.1 s.
  - Blocks 8, 9, 10: rc=1, 0.9/0.5/0.5 s, ENOENT `/Users/feb/dev/cartridge/builtin/policy` and `builtin/auth.ctg` at `smoke.test.ts:38` (expected pre-integration failure; no daemon started). `tmp.*` in `$TMPDIR`: 68 before, 68 after.
  - Block 11: rc=0. Block 12: rc=0 (no live artifact changed), and `run.95728` was removed (no `run.*` left).
  - Block 13: rc=1, "fixture links <runtime>/builtin again" (line 38), the correct baseline.
- Read-only: `prd.ctg/src/{lifecycle,process,coordinator}.ts`, `prd.ctg/prd`, `prd.ctg/init.lua`, `.cartridge/justfile`, `.cartridge/tools/memo-run`, cartridge.ctg `src/cli/host.rs`, `git worktree list` (no lane for this PRD), per-tree `git status --porcelain` and `git ls-tree HEAD`.
- sha256 via `shasum -a 256`; both match the hand-off.

Reviewer identity: independent reviewer agent r5 (coordinator cartridge-c4).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: PASS (93/100).
Unresolved blocking findings: none.
Rounds used / remaining: 5 / 0.
Next action: proceed to implementation of spec01 in the superproject without a lane (finding 1), collect from the CLI (finding 2); findings 3–4 may be folded in, but any substantive spec change makes this rating stale with no rounds left, so prefer recording them in the implementation notes rather than editing spec01.
