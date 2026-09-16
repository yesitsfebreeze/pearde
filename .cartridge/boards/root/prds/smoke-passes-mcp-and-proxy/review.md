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
