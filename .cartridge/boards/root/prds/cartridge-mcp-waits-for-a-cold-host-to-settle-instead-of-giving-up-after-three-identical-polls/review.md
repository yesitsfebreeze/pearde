# @root/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls review history

Plan: `@root/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls`,
`prd.ctg/.cartridge/boards/root/prds/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls/prd.md`.
Scope: one observable outcome — a cold `cartridge mcp` waits for its listener instead of
giving up on three identical status polls. Executable leaf, owner `runtime`, prio 75.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: root `b4c3dfd` (the spec cites `4684791`; the two later commits are
planning records only), `cartridge.ctg` `63ff234` clean. No dirty files in the footprint.

| Input | Content digest |
| --- | --- |
| Plan | `prds/<slug>/prd.md` — sha256 `312164cd3452e27c530f80a9af015b4dc84345dea83184a0b5585b12d60a8d93` |
| Specs | `prds/<slug>/specs/spec01.md` — sha256 `4b726543cd538c40c84c66cb5c2c2f5e6625f5df2e4b6dfe9a3afbbcd5fa5549` |
| Analyst report | `prds/<slug>/analyst-1.md` — sha256 `f9fedb3e1dfcf6c77d930f7df6af475dc31bca5b7861b90aba7f836e5ee9397b` |
| Prototype | `.state/loop/<slug>/attempt-1.patch` — sha256 `1a1e56f95817cf6f6b8b88577641251ddcc304681fd9e538ce103c325ce0f273` |
| Material source | `cartridge.ctg/src/cli/host.rs` @ `63ff234` — sha256 `566c72536dff367b934331b5d52115bd3e722a3178a53a030b74d2e2592857c7` |
| Material contracts | `cartridge.ctg/.cartridge/settings.json` (`startup_timeout_secs` 60, `verify_timeout_secs` 300), `src/host/mod.rs:37-49` (`Status.listen`), `prd.ctg/.cartridge/templates/spec.md` (engine facts) |

### Verification performed (independent, isolated)

Scratch worktreeless copies of `cartridge.ctg` at `63ff234` (`git archive`, no write to the
live checkout or its `.git`), one unpatched (`src-head`) and one with `attempt-1.patch`
applied (`src-patched`, applies clean, +41/-19, one file). Builds used
`CARGO_TARGET_DIR` under `$HOME/.cache/` only; the live `cartridge.ctg/target` was never
written. Every cold probe ran with a scratch `CARTRIDGE_HOME` under `mktemp -d` and a
binary outside the live tree. All block scripts and probe files live in a private
scratchpad subdirectory (`…/scratchpad/review-cartridge-mcp-settle/`).

**Code claims — all confirmed at `63ff234`.** `attach` `src/cli/host.rs:59`; the settle call
`:74` is `settle_remote(&found.0, settings.verify_timeout())` and returns at `:75` from
inside the `Ok(Some(found))` arm, *before* the `attach` deadline check at `:92`, so
`startup_timeout()` computed at `:63` never bounds the settle — the only bound is
`verify_timeout_secs` (default 300, documented as `verify`'s budget). `settle_remote` `:147`,
`if stable >= 3 && !empty` `:180`. Callers `:226` (`run`, `key`), `:241` (`launch`, `"proxy"`),
`:287` (`mcp`), `:313` (`Backend` re-attach); there are no others. `Status.listen` exists
(`src/host/mod.rs:47`), so no new RPC. The three other `verify_timeout()` callers
(`src/host/run.rs:37`, `:166`, `src/cli/setup.rs:649`) all go through `Host::settled`
(`src/host/run.rs:12`), a lifecycle-event wait with **no** three-identical-poll shortcut, used
by `verify`/contracts/`setup` — they genuinely want the verify budget and are untouched by
this change. **The deadline argument is correct.**

**The defect reproduces for me — but not 5 of 5.** Using the spec's own fixture with a
HEAD-built binary, on genuinely cold runs (fresh temp project root per run):
**5 failures of 8**, each with exactly ``service `mcp` unavailable: no active listener``.
Patched binary, same probe: **0 failures of 8**. Running the spec's `## Verify` block 4
unchanged with the HEAD binary three times gave `1 of 5 wrong`, `5/5 ok`, `5/5 ok`; under
10 CPU hogs, HEAD gave `1 of 5 wrong` and patched `5/5 ok`. Every observed failure was
**run 1**, the only genuinely cold run — runs 2-5 reuse the same temp root, so the snapshot
dylibs are page-warm and `mcp` reaches `active` before the picture holds still for 300 ms.

**Prototype results reproduce.** Block 4 at repo root, patched binary: exit 0, `5/5 ok`,
1.9-2.5 s per run, 16.8 s for the block. Block 5 (untrusted): exit 0, fails in 2.0 s and
1.6 s naming `mcp`, no 60 s stall. `cargo clippy --all-targets --all-features -- -D warnings`
on the patched tree: exit 0, zero warnings; `cargo fmt --all --check`: exit 0.

**Guard block discriminates.** Exit 1 on the unpatched live checkout ("settle_remote still
ends the wait on three identical polls"), exit 1 on the unpatched scratch copy, exit 1 where
`cartridge.ctg/src/cli/host.rs` is absent (`test -f`), exit 0 on the patched tree. All eight
patterns were matched individually against both trees: neg1/neg2/neg3 present only
unpatched, pos1-pos5 present only patched. No guard is `!`-prefixed; the file is `test -f`
guarded, and blocks 2, 4 and 5 `test -x`/`test -f`/`test -d` every artefact they consume.

**One risk tested and cleared.** Keying the wait on a single listener can hand `mcp` back
before the composition settles, which could yield a short `tools/list`. Measured: the cold
run and a second run against the already-settled daemon both returned **20 tools**, three
attempts out of three. No partial list in this composition.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Real, user-visible first-MCP-client failure; one outcome; footprint is exactly the file changed; the smoke-fixture workaround correctly split into its own PRD rather than widened into this footprint. −2: the Outcome ("3 of 3") and the Planning note ("every cold run fails in ~2.0 s") state as settled fact a baseline I measure at 5 of 8 cold runs. |
| Ownership and reuse | 19 | Owner `runtime`; one guard in the shared function instead of four call-site patches, so `run` and `launch` are fixed with `mcp`; reuses the existing `listen` field and mirrors `explain` rather than inventing a shared helper; no new RPC, no new setting; `verify_timeout()` left to its three real callers. −1: the in-process sibling `Host::settled` is never named, although it is the reason the fix does not need to touch `run`/`verify` (I verified it has no poll shortcut). |
| Dependencies and implementable slices | 19 | One file, +41/−19, prototype attached and applies clean; `needs` the done attach leaf and the premise was re-established after that rewrite; the overlap with `@root/an-attach-gives-up-…` is disclosed with a defensible order and an in-footprint `tokio::time::timeout(left, …)` wrapper that is correct (`left` recomputed per iteration, `Ok(Ok(status))`-else-return preserves the old semantics, the one-shot reload `continue` cannot busy-loop); no-lane landing shape matches the engine facts and the blocks are written to run once in `repo`. −1: blocks 2 and 3 set `CARGO_TARGET_DIR` unconditionally instead of the template's `${CARGO_TARGET_DIR:-…}` form, and block 2 runs cargo inside the footprint (a `Cargo.lock` refresh would abort pass 2 with "source footprint changed"); neither bit me, neither is named. |
| Observable acceptance and baseline evidence | 11 | The source guard block is deterministic and every pattern discriminates; box 2's untrusted probe is real and passes; boxes for `just check/test cartridge` and `just test lifecycle` run and pass (18.1 s / 42.2 s). −9 (blocking): box 1 does not discriminate the change it gates. Only run 1 of the five is genuinely cold, so an **unpatched** binary passed the block in 2 of 3 attempts here; the spec's supporting argument ("the baseline is deterministic… an order of magnitude, not a race") is contradicted by re-measurement (≈62 % per cold run, not 100 %), and its "five runs share one root" bullet treats the warm runs as added signal when they are padding. Also `ok` is `out.includes('"tools"')`, which an empty or partial tool list would satisfy. |
| Failure, recovery and compatibility | 17 | Both new exits are bounded (`serves` or `!starting && !empty`) and the deadline now actually binds each poll; untrusted composition measured failing in 1.6-2.0 s naming `mcp`; no test in `cartridge.ctg/.cartridge/tests` references `settle_remote` or `attach`, so deleting the shortcut breaks nothing; clippy/fmt/174 unit tests/11 lifecycle tests clean. −2: one behaviour change is unnamed — when the key is never served *and* a cartridge stays `starting`/`waiting`, the old code returned after ~300 ms while the new code polls to `startup_timeout` (60 s); bounded and arguably correct, and it did not materialise in either degraded composition I ran (1.6-2.1 s), but it belongs in the spec as the accepted cost. −1: the 120 s block budget rests on this machine's `rustc-wrapper = "kache"` cache (cold-target build measured 8.9 s); on a host without it blocks 2-3 can exceed the limit, and block 8 already uses 42 s of 120 s. |
| Reviewer total | **84** / 100 | FAIL: below 90, one blocking finding. |

### Findings and concrete revisions

1. **BLOCKING — box 1 can green-light an unpatched tree.** Evidence: the spec's block 4,
   unchanged, with a HEAD binary: `1 of 5 wrong`, then `5/5 ok`, then `5/5 ok` (and `1 of 5
   wrong` under 10 CPU hogs). Cause: the fixture builds one temp project root and reaps only
   the daemon between runs, so runs 2-5 are warm and cannot fail; the whole box rests on run
   1, which fails ≈62 % of the time at HEAD (5 of 8 fresh-root runs). Recommendation: make
   every run genuinely cold — build a fresh project root (or at minimum re-copy the snapshot
   dylibs) inside the loop instead of once before it. With five independent cold runs at the
   measured rate, an unpatched tree passes with probability ≈0.4⁵ < 1 %, and the box becomes
   the regression gate it is presented as. Resolution: pending round 2.
2. **Restate the baseline honestly** in the Planning note and in "Why box 1 is not a coin
   flip": the defect is a real but *probabilistic* cold-start race (≈5 in 8 here), not a
   deterministic 5-of-5, and the margin argument (300-400 ms plateau vs a 1.6 s listener) is
   not what decides a run — what decides it is whether any 300 ms window passes with no state
   change before `mcp` goes active. The independent-round evidence belongs beside the
   analyst's. Resolution: pending round 2.
3. **Strengthen the run assertion**: `out.includes('"tools"')` passes on an empty list.
   Count the tools (or compare with the settled second run, which I measured at 20 both ways)
   so "answers `tools/list`" is actually checked. Resolution: pending round 2.
4. **Name the accepted cost of deleting the shortcut**: an unserved key plus a cartridge
   stuck in `starting`/`waiting` now waits to `startup_timeout` (60 s) where it used to return
   in ~300 ms. One sentence in "Option chosen". Resolution: pending round 2.
5. **Name the build-cache assumption** behind the 120 s limit for blocks 2-3 (measured 8.9 s
   and 11.5 s here with a `kache` rustc wrapper from an empty target dir), and the
   `Cargo.lock`-inside-the-footprint caveat for block 2. Non-blocking. Resolution: pending.
6. Endorsed as written, no change needed: the `startup_timeout()` move and the claim that
   `verify_timeout()`'s three callers want the verify budget; the `key: &str` threading through
   all four call sites; the deletion of `stable`/`last`; the local `tokio::time::timeout`
   wrapper and "ship both, this one first" over merging with
   `@root/an-attach-gives-up-on-a-daemon-that-answers-its-socket-but-never-its-status`
   (merging would make this PRD wait on a fix it does not need, and the wrapper is redundant
   but harmless once `rpc.rs` lands); the no-lane landing shape; and splitting the smoke
   fixture's daemon pre-start into `@root/the-smoke-fixture-drops-its-daemon-pre-start-workaround`.

Disposition: **keep and revise** — the diagnosis, the fix and the source guards are right;
the behavioural acceptance test needs to become discriminating.

### Validation

All commands run by the reviewer, with observed exit codes. Each `## Verify` block was
extracted verbatim from `spec01.md` and run as a `sh -eu` script.

| cwd | command | exit / result |
| --- | --- | --- |
| repo | `git rev-parse HEAD` (`b4c3dfd`), `git -C cartridge.ctg rev-parse HEAD` (`63ff234`), `git -C cartridge.ctg status --porcelain` (empty) | 0 |
| scratch | `git -C cartridge.ctg archive 63ff234 \| tar -x` ×2, `patch -p1 < attempt-1.patch` | 0, "1 file changed, 41 insertions(+), 19 deletions(-)" |
| repo (unpatched) | Verify block 1 (source guards) | **1** — "settle_remote still ends the wait on three identical polls" |
| scratch repo-patched | Verify block 1 | **0** — "source guards ok" |
| scratch (no `cartridge.ctg`) | Verify block 1 | **1** — `test -f` |
| scratch | each of the 8 guard patterns, `grep` against `src-head` and `src-patched` separately | all 8 discriminate (3 unpatched-only, 5 patched-only) |
| scratch repo-head | `cargo build --bin cartridge` (`CARGO_TARGET_DIR` = smoke cache) → HEAD binary | 0, 1.4 s |
| scratch repo-patched | Verify block 2 (host build, empty target dir) | 0, 8.9 s |
| scratch repo-patched | Verify block 3 (mcp/memo dylibs) | 0, 11.5 s |
| repo | Verify block 4, patched binary | **0** — `run 1 ok in 2.5s … 5/5 ok`, block 16.8 s |
| repo | Verify block 4's fixture, HEAD binary, ×3 | 0 — `1 of 5 runs wrong`, `5/5 ok`, `5/5 ok` |
| repo | same, HEAD then patched under 10 CPU hogs | HEAD `1 of 5 runs wrong`; patched `5/5 ok` |
| repo | fixture reduced to run 1 only (fresh root each time), ×8 per binary | HEAD **5 failures of 8** (`no active listener`); patched **0 of 8** |
| repo | fixture with run 2 against the settled daemon, ×3 | `run 1 tools=20`, `run 2 tools=20` each time |
| repo | Verify block 5 (untrusted) | **0** — fails in 2.0 s and 1.6 s naming `mcp` |
| scratch src-patched | `cargo fmt --all --check` | 0 |
| scratch src-patched | `cargo clippy --all-targets --all-features -- -D warnings` | **0**, zero warnings |
| repo | Verify block 6 (`just check cartridge`) | 0, 11.5 s |
| repo | Verify block 7 (`just test cartridge`) | 0, 18.1 s, 174 tests passed |
| repo | Verify block 8 (`just test lifecycle`) | 0, 42.2 s, 11 tests passed |
| repo | `grep -rn "settle_remote\|stable >= 3\|attach(" cartridge.ctg/.cartridge/tests/` | no match — no test depends on the deleted shortcut |

Limits and isolation: no `prd` state operation, no `git add`, no commit, no push, no write to
the live `cartridge.ctg` checkout (it is still clean); the live project daemon was never
started, stopped, replaced or reloaded by this review, and every probe used a scratch
`CARTRIDGE_HOME`, a temp project root and a binary outside the live tree. Observation for the
coordinator, not attributed to this review: the project's daemon pid changed from 79923's
cohort to `8772` (started 15:19:32) while `.cartridge/daemon.log` filled with `live.ctg`
trust/manifest errors from another session; Verify blocks 5-8, including `just test
lifecycle`, left that pid unchanged.

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL (84/100)**.
Unresolved blocking findings: finding 1 — the 5-of-5 cold-start acceptance check does not
discriminate the fix; an unpatched binary passed it in 2 of 3 independent attempts.
Rounds used / remaining: 1 / 4.
Next action: bounded revision — make every run of the box-1 fixture genuinely cold, restate
the baseline as probabilistic with the independent measurement, tighten the `tools/list`
assertion, and name the two accepted costs (findings 2-5); then re-review in round 2.

## Round 3 — 2026-09-17

Record note: this file holds Round 1 only. A round-2 revision was presented and
reviewed (the PRD's Planning note and spec01 both cite round-2 findings and an
analyst-2 re-measurement of 31 failures in 108 cold runs), but no Round 2 section
was ever appended here. The count is not reset: this is **round 3 of 5**, and the
round-2 result is recorded as missing rather than invented.

Presented revision: root `bfb1cf9`, `cartridge.ctg` `63ff234` with 18 dirty files
from other sessions (among them `src/cli/host.rs`, +44/−1, the `stop_when_idle` /
`--idle-timeout` work). The superproject index holds another session's staged
rename `.cartridge/tools/pi-voice -> .cartridge/tools/live`.

| Input | Content digest |
| --- | --- |
| Plan | `prds/<slug>/prd.md` — sha256 `b109b09fa3428391f3ea0d2c50b7e08019c4ed225e30fb8f05d249784db068b3` |
| Specs | `prds/<slug>/specs/spec01.md` — sha256 `e842e9070cbdb048e36553786b602f8ec011c2a1c16c9b36afb796d7a77294b1` |
| Prototype | `.state/loop/<slug>/attempt-1.patch` — sha256 `1a1e56f95817cf6f6b8b88577641251ddcc304681fd9e538ce103c325ce0f273` (unchanged from round 1) |
| Material source | `cartridge.ctg/src/cli/host.rs` (working tree, dirty) — sha256 `bde3cb1d4a85c76611d60448ccf136a9a1c5db6cdc694e84a86f28c57b0eb14e` |
| Material source | `cartridge.ctg/.cartridge/tests/unit/stdio.rs` — sha256 `d131b2bbd4a8c77127a513b5a2ce31336ddd7e02724aaa60c32e9b0552da5927` |
| Material contracts | `prd.ctg/src/lifecycle.ts` (block limit `120_000` ms, `cap: 65536`, `cleanIndex`, `assertFootprint`), `prd.ctg/src/planner.ts:5-9` (`feet` = PRD footprint ∪ spec footprints), `.cartridge/justfile` `_fan`/`_one`, `.cartridge/tests/integration/takeover.test.ts` |

### Verification performed (independent)

**The behaviour is genuinely absent from the working tree.** At the dirty tree the
spec's own line numbers are exact: `pub(crate) async fn attach(project: &Project)`
at `cartridge.ctg/src/cli/host.rs:59`, `settle_remote(&found.0,
settings.verify_timeout())` at `:74`, `async fn settle_remote(...)` at `:182`,
`if stable >= 3 && !empty { return; }` at `:215`. Reading the loop confirms the
spec's structural claim: the only path that returns *while a cartridge is still
`starting`/`waiting`* is the `stable >= 3` shortcut, because the other early exit
is guarded by `!starting && !empty`.

**The unit-test home exists and is already wired.**
`cartridge.ctg/.cartridge/tests/unit/stdio.rs` exists (1767 bytes), is included by
`#[path = "../../.cartridge/tests/unit/stdio.rs"] mod stdio_tests;` at
`src/cli/host.rs:493-494`, and already holds the pure `untrusted` test
(`only_trust_refusals_prompt_an_attach_reload`) over a synthetic status of exactly
the shape `settled` will read. No new file and no new module wiring is needed, as
the spec says. `cargo test --bin cartridge -- --list` prints the module path as
`cli::host::stdio_tests::<name>`, so block 2's fixed-string
`grep -qF "stdio_tests::$case ... ok"` matches as a substring; and the bin carries
16 unit tests today, so the filter `settled_` selecting exactly four and
`test result: ok. 4 passed` is consistent.

**Verify blocks, run by me from `/Users/feb/dev/cartridge`, exit codes observed:**

| Block | Command | Exit | Elapsed |
| --- | --- | ---: | ---: |
| 1 | source guards | **1** — "settle_remote still ends the wait on three identical polls" | <1 s |
| 2 | `cargo test --locked … --bin cartridge -- settled_` | **1** — "unit case settled_when_the_key_is_active did not run" (`0 passed; 16 filtered out`) | <1 s (warm target) |
| 3 | `just check cartridge` | **0** | 3 s |
| 4 | `just test cartridge` | **0** — 176 tests run, 176 passed | 12 s |
| 5 | `just test lifecycle` | **0** — 13 pass, 0 fail, 852 expect() | 47 s |

Blocks 1 and 2 both discriminate an unimplemented tree, which is what the round-1
blocking finding asked for. Block 4's stdout is 20 813 bytes, inside the engine's
65 536-byte cap.

**No block rebuilds or restarts the live daemon.** Every cargo invocation exports
`CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/cartridge-mcp-waits-verify}"`
(the template's own form; round 1's unconditional-assignment deduction is
resolved), and `--locked` now prevents the `Cargo.lock` refresh round 1 warned
about. `target/` is git-ignored at the repo root (`.gitignore:2:/target/`; checked
with `git check-ignore -v`). Observed across blocks 3, 4 and 5: the project daemon
pid stayed `71453` throughout, no `*.ctg/target/debug` directory and no `*.dylib`
anywhere in the composition was written in the window, and `git -C cartridge.ctg
status --porcelain` still reports the same 18 files. `just check cartridge` and
`just test cartridge` resolve through `.cartridge/memos/routine/cartridge-development.md`'s
`runtime|cartridge)` arm to `cartridge.ctg/justfile`, so `cargo fmt --all --check`,
`cargo clippy --workspace --all-targets` and `cargo nextest run --workspace` all
land in the isolated directory.

**One inter-block dependency the spec does not state, verified working.** Block 5
is `bun test .cartridge/tests/integration/takeover.test.ts`, which resolves its
binary as `${CARGO_TARGET_DIR}/debug/cartridge` and throws "Build the runtime
first" if it is absent; it never builds. I moved that binary aside and re-ran
block 4: `cargo nextest run --workspace` uplifted it back, so the bin target is in
nextest's build graph and block 4 satisfies block 5's precondition. The ordering
holds, but nothing in the spec says block 5 depends on block 4 having run.

**The gate is not host-free, and the spec undersells itself.** spec01 states the
blocks "deliberately do not launch a host". Block 5 launches many: `takeover.test.ts`
runs 13 real daemon lifecycles under scratch roots with two tiny cartridges, and
among them `two runs with no daemon share one` (`:303`) is a genuine **cold**
`cartridge run` pair through the changed `attach` → `settle_remote`, asserting
exit 0. `a run against a socket that errors reports it and starts nothing` (`:259`)
and `a run during --replace starts no host of its own` (`:316`) exercise the same
path. This is smaller-composition cold-start coverage than the round-2 fixture,
but it is not nothing, and it is already inside the gate at 47 s.

**Timing margin.** The engine limit is `timeout: 120_000` ms per block
(`prd.ctg/src/lifecycle.ts:45`), and with no lane each block runs **once**, not
twice, so the two-pass concern does not apply here. My 47 s for block 5 reproduces
the analyst's 47 s exactly: 2.55× margin on the longest block, and block 5 compiles
nothing, so that figure does not depend on this machine's `rustc-wrapper = "kache"`.
Blocks 3 and 4 do depend on it when the target directory is cold — and the
pre-warm command the spec prints warms the wrong thing (see finding 3).

**Footprint.** `feet(prd)` (`prd.ctg/src/planner.ts:5-9`) is the union of prd.md's
footprint and every spec's, so it is `{cartridge.ctg, cartridge.ctg/src/cli/host.rs,
cartridge.ctg/.cartridge/tests/unit/stdio.rs}` — the spec's narrowing to two files
does **not** narrow the effective footprint, because prd.md still carries the whole
submodule. From the superproject, `git status --porcelain=v1 --untracked-files=all --`
over all three paths reports exactly one entry, ` M cartridge.ctg` (the gitlink):
collect cannot see inside the submodule at all, so whatever the submodule HEAD
holds is what the receipt certifies.

**Collect is blocked for an unrelated reason, not scored here.** `cleanIndex`
(`prd.ctg/src/lifecycle.ts:103-105`) throws on any staged path repository-wide, and
the superproject index holds another session's `R100 .cartridge/tools/pi-voice ->
.cartridge/tools/live`. That is environmental and is not counted against this spec.

### The central judgement: is the unit gate sufficient proof?

**Yes for the Outcome, and demoting the 15-run fixture is the better engineering —
but it is not sufficient for PRD acceptance box 2, which round 3 left with no
proof path at all.** Argued from the dimensions, not from taste:

1. *Test validity (dimension 4).* The defect is "the wait ends while cartridges are
   still starting". In the code at `:182-219` the **only** path that can do that is
   `stable >= 3`; every other exit is guarded by `!starting`. Block 1 proves that
   path is gone and block 2 proves the replacement decision answers `false` for a
   status whose key is `starting`. That is a property over all executions. The
   round-2 fixture was a *sample*: round 1 measured the per-cold-run failure rate at
   5 of 8, analyst-2 at 31 of 108, so 15 runs detect an unpatched tree with roughly
   99 % confidence — strictly weaker than a structural proof, and weaker in the
   other direction too, since a patched tree that trips on load or on a missing
   sibling dylib fails the collect for reasons that are not this change.
2. *Baseline evidence is preserved, not lost.* review-plan.md step 2 asks that a
   suspected defect be reproduced in a disposable fixture — it was, twice, and the
   measurements survive in prd.md and in spec01's defect section. The fixture's job
   was to establish that the behaviour is absent; that job is done and does not need
   redoing on every later collect of this repository.
3. *The residual blind spot does not reach the Outcome.* Unit cases feed `settled`
   synthetic `Value`s, so they cannot prove the real daemon emits `state`/`listen`
   in the shape `settled` reads. But if that read were wrong, `settled` would simply
   never match the key and the loop would fall through to "nothing left starting and
   non-empty" — which is strictly **stronger** than the deleted `stable >= 3`
   shortcut and is exactly the wait the measured race skipped. The Outcome survives
   the worst unit-test blind spot. That is why unit cases suffice *here*, and it is
   the reason to state: for a change whose correctness depended on the field read,
   they would not.
4. *Where it is genuinely insufficient.* PRD acceptance box 2 — "fails within the
   documented startup deadline with a message naming the missing listener" — is now
   gated by nothing. spec01 restates it as acceptance box 3 and gates that with a
   single `grep` for `tokio::time::timeout(left, …)`, which proves a line exists, not
   that the failure path is bounded or that the message names `mcp`. Round 2 carried
   a deterministic untrusted-composition probe for exactly this, which round 1
   measured passing in 1.6 s and 2.0 s — about 3.6 s of gate. Round 3 discarded it
   together with the expensive probabilistic fixture. Dropping a cheap deterministic
   check because an expensive flaky one had to go is an over-correction, and it
   leaves one of three PRD acceptance boxes with neither a Verify block nor a named
   receipt obligation (the receipt obligation covers only the cold-start count).

So: not a blocking loss of evidence for the cold-start Outcome. A blocking gap for
the failure-path acceptance box.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Real first-MCP-client failure on a fresh project; one outcome, one owner; round 1's finding 2 is resolved — the baseline is now stated as probabilistic (31 of 108) in both prd.md and spec01, with the independent measurement beside the analyst's; the smoke-fixture workaround is correctly left to a follow-up PRD rather than widened into this footprint. −2: "The Verify blocks … deliberately do not launch a host" is false — block 5 launches 13 daemon lifecycles including a genuinely cold `run` pair (`takeover.test.ts:303`), which I observed passing in 47 s. The spec misstates its own scope, against itself. |
| Ownership and reuse | 19 | Owner `runtime`; one guard in the shared function repairs `run`, `launch` and `mcp` together rather than four call-site patches; reuses the already-`#[path]`-wired `.cartridge/tests/unit/stdio.rs` (verified: wired at `host.rs:493-494`, already home to a pure test over the same status shape) instead of a new file or module; reuses the existing `listen` field, no new RPC and no new setting; `verify_timeout()` left to its three in-process callers; explicitly declines a shared helper for two three-line readers. −1: round 1's deduction stands unaddressed — `Host::settled` (`src/host/run.rs:12`), the in-process sibling that is the reason this fix need not touch `run`/`verify`, is still never named. |
| Dependencies and implementable slices | 15 | One source file plus one test file; prototype attached and applies clean; overlap with `@root/an-attach-gives-up-…` disclosed with a defensible order and an in-footprint wrapper; the no-lane landing shape matches the engine (I confirmed `feet`, `cleanIndex` and `assertFootprint`); round 1's `CARGO_TARGET_DIR`-form and `Cargo.lock` deductions are resolved by the `${…:-…}` form and `--locked`. −4 (blocking, finding 1): the landing step cannot execute in the tree the spec itself describes — the other session's 44 uncommitted lines are in `src/cli/host.rs`, the same file. −1 (finding 3): the printed pre-warm command warms only the bin's test target while blocks 3 and 4 need `clippy --workspace --all-targets` and `nextest run --workspace`. |
| Observable acceptance and baseline evidence | 15 | Block 1 exits 1 on the live tree and every guard discriminates; block 2 exits 1 on the live tree (`0 passed; 16 filtered out`, caught by the explicit per-case check — the "a filter that matches nothing also exits 0" comment is right and the guard is right); the `stdio_tests::` substring form matches real cargo output; blocks 3, 4 and 5 exit 0 at 3 s, 12 s and 47 s. The structural argument in "What is gated and what is not" is sound and, for the measured defect, stronger than a 15-run sample. −4 (blocking, finding 2): PRD acceptance box 2 has no Verify block and no receipt obligation; the cheap deterministic untrusted-composition probe from round 2 was discarded along with the expensive fixture. −1: the source guards forbid `stable >= 3` by name only; an implementer could satisfy all nine patterns and still add a different early return inside the loop, which block 2's four cases over the pure predicate would not see. |
| Failure, recovery and compatibility | 16 | Round 1's finding 4 is resolved: the accepted cost (an unserved key plus something stuck `starting`/`waiting` now waits to `startup_timeout_secs` where it used to return in ~300 ms) is named, with the correct argument that trust-refused compositions go `failed` and settle at once. Isolation verified rather than trusted: daemon pid `71453` unchanged across blocks 3-5, no `*.ctg/target/debug` or `*.dylib` written, submodule dirty set unchanged, `target/` git-ignored at `.gitignore:2`. Margin 47 s of 120 s on the longest block, which compiles nothing and so does not rest on the `kache` wrapper; the build-cache assumption is named for the blocks that do. −2: "Footprint narrowed to `src/cli/host.rs` and `.cartridge/tests/unit/stdio.rs`" describes the spec's footprint, not `feet(prd)` — prd.md still carries `cartridge.ctg`, so the guard covers the whole submodule and, from the superproject, resolves to the single gitlink entry ` M cartridge.ctg`; collect can neither exclude foreign submodule content from the receipt nor keep a later submodule commit by any session from turning this PRD's receipt into "verified source footprint changed after collection". −2: block 5's dependence on block 4 having uplifted `${CARGO_TARGET_DIR}/debug/cartridge` is unstated (I verified it holds), and the failure mode if it ever did not is a hard "Build the runtime first" at collect time. |
| Reviewer total | **83** / 100 | FAIL: below 90, two blocking findings. |

### Findings and concrete revisions

1. **BLOCKING — the landing step cannot execute in the tree the spec describes.**
   Evidence: `git -C cartridge.ctg diff --stat -- src/cli/host.rs` is `44 insertions(+),
   1 deletion(-)` of another session's `stop_when_idle` / `--idle-timeout` work, in
   the same file this change edits, plus 17 other dirty files in the submodule. The
   spec names those 44 lines twice (to justify its line numbers) and never names them
   as a landing hazard. Neither route it offers works: the prescribed clean worktree
   of `cartridge.ctg` produces a clean commit that `git merge --ff-only` will refuse
   to fast-forward into the live submodule while `src/cli/host.rs` is locally
   modified there; and committing from the live checkout carries the foreign 44 lines
   into the same submodule commit, which `feet(prd)` cannot exclude because from the
   superproject the whole footprint collapses to one gitlink entry. Recommendation:
   one paragraph in "Landing shape" that states the precondition — the submodule's
   `src/cli/host.rs` must be clean before the fast-forward, so this PRD lands after
   the idle-timeout work commits (or its owner commits it first) — and says
   explicitly that a hunk-level commit is not an acceptable substitute. This is not
   the staged-rename blocker, which is environmental; this one is inside the spec's
   own "Landing shape" section. Resolution: pending round 4.
2. **BLOCKING — PRD acceptance box 2 has no proof path.** Evidence: the five Verify
   blocks gate the source structure, the four unit cases and the three repository
   gates; none exercises the failure path, and the "Cold-start evidence remains the
   implementer's obligation" paragraph names only the 0-of-15 cold-start count.
   spec01's acceptance box 3 covers box 2 with a grep for a single line, which proves
   the line exists, not that a composition that never serves the key fails inside
   `host.startup_timeout_secs` naming the missing listener. Round 2 had a
   deterministic block for this and round 1 measured it passing in 1.6 s and 2.0 s.
   Recommendation: restore that one block (a trust-refused or key-less composition,
   asserting a non-zero exit inside the deadline whose stderr names `mcp`) — it is
   ~4 s of gate and it is not probabilistic — or, if it must stay out of the blocks,
   add it to the receipt obligation beside the 0-of-15 count. Resolution: pending
   round 4.
3. **The printed pre-warm command warms the wrong target set.** Evidence: the spec
   prints `cargo test --locked … --bin cartridge --no-run`, which builds only the
   bin's test target; block 3 runs `cargo clippy --workspace --all-targets` and block
   4 runs `cargo nextest run --workspace`, both far larger. On a host without this
   machine's `rustc-wrapper = "kache"` the pre-warm would leave exactly the blocks it
   is meant to protect facing a cold dependency build inside 120 s. Recommendation:
   `CARGO_TARGET_DIR=… cargo nextest run --locked --manifest-path
   cartridge.ctg/Cargo.toml --workspace --no-run`. Non-blocking. Resolution: pending.
4. **State block 5's precondition.** `takeover.test.ts` resolves
   `${CARGO_TARGET_DIR}/debug/cartridge` and throws rather than building. I verified
   block 4 uplifts it (moved the binary aside, re-ran block 4, it came back), so the
   order works — but one sentence in the engine-facts comment saying block 5 consumes
   what block 4 built would keep a future reordering from failing at collect time.
   Non-blocking. Resolution: pending.
5. **Correct "deliberately do not launch a host", and claim the credit.** Block 5
   launches 13 real daemon lifecycles under scratch roots, including a genuinely cold
   `cartridge run` pair with no daemon (`takeover.test.ts:303`), through the changed
   `attach`. That is live cold-start coverage of a two-cartridge composition already
   inside the gate; saying otherwise understates the evidence and misdescribes what
   the blocks do. Non-blocking. Resolution: pending.
6. **Consider narrowing prd.md's footprint.** `feet(prd)` unions prd.md's footprint
   with the specs', so the spec's two-file narrowing is inert while prd.md lists
   `cartridge.ctg`. Recorded as an observation, not a required revision: from the
   superproject the whole footprint collapses to the `cartridge.ctg` gitlink either
   way, so narrowing prd.md changes nothing the engine checks, and every superproject
   PRD over a submodule shares the property. Worth one sentence so the spec does not
   claim protection it does not have. Non-blocking.
7. **Endorsed as written, no change needed** (carried forward from round 1 and
   re-checked here): the `startup_timeout()` move and the reading of
   `verify_timeout()`'s three callers; `key: &str` threaded through all four call
   sites; the deletion of `stable`/`last` and the argument that a pure `settled` makes
   the regression unrepresentable rather than merely absent; the local
   `tokio::time::timeout(left, …)` wrapper and "ship both, this one first"; the
   no-lane landing shape; `--locked` and the `${CARGO_TARGET_DIR:-…}` form; the
   explicit `if grep -qF …; then exit 1; fi` negative guards (no inert `! grep`); and
   the decision to demote the 15-cold-start fixture to an implementer's probe, which
   this round endorses on the merits above.

Disposition: **keep and revise.** The round-1 blocking finding is decisively
resolved and the central judgement goes the author's way — the structural gate is
better proof of the Outcome than the fixture it replaced. Two narrow, cheaply fixed
gaps block: a landing step that cannot run in the tree it names, and one PRD
acceptance box with no proof path.

### Validation

All commands run by this reviewer from `/Users/feb/dev/cartridge`, with the exit
codes observed.

| cwd | command | exit / result |
| --- | --- | --- |
| repo | `git rev-parse HEAD` / `git -C cartridge.ctg rev-parse HEAD` | 0 — `bfb1cf9`, `63ff234` |
| repo | `git -C cartridge.ctg status --porcelain` | 0 — 18 modified files, `src/cli/host.rs` among them |
| repo | `git -C cartridge.ctg diff --stat -- src/cli/host.rs` | 0 — `44 insertions(+), 1 deletion(-)` |
| repo | `grep -n` for the four defect anchors in `src/cli/host.rs` | `:59`, `:74`, `:182`, `:215` — all as the spec states |
| repo | Verify block 1 (source guards), verbatim, `sh -eu` | **1** — "settle_remote still ends the wait on three identical polls" |
| repo | Verify block 2 (unit cases), verbatim, `sh -eu` | **1** — `0 passed; 16 filtered out`, then "unit case settled_when_the_key_is_active did not run" |
| repo | `cargo test --locked --manifest-path cartridge.ctg/Cargo.toml --bin cartridge -- --list` | 0 — names print as `cli::host::stdio_tests::<name>` |
| repo | Verify block 3 (`just check cartridge`) | **0**, 3 s |
| repo | Verify block 4 (`just test cartridge`) | **0**, 12 s, 176 tests run / 176 passed, 20 813 bytes of stdout |
| repo | Verify block 5 (`just test lifecycle`) | **0**, 47 s, 13 pass / 0 fail / 852 expect() |
| repo | binary moved aside, Verify block 4 re-run | **0** — `${CARGO_TARGET_DIR}/debug/cartridge` uplifted back; block 5's precondition is satisfied by block 4 |
| repo | `pgrep` for the project daemon before and after blocks 3, 4, 5 | pid `71453` unchanged throughout |
| repo | `find` for `*.ctg/target/debug` and `*.dylib` written in the window | no match — no live dylib touched, no hot restart |
| repo | `git check-ignore -v target/cartridge-mcp-waits-verify` | 0 — `.gitignore:2:/target/` |
| repo | `git status --porcelain=v1 -uall -- cartridge.ctg cartridge.ctg/src/cli/host.rs cartridge.ctg/.cartridge/tests/unit/stdio.rs` | 0 — one entry, ` M cartridge.ctg` (the gitlink) |
| repo | `git diff --cached --name-status` | 0 — `R100 .cartridge/tools/pi-voice -> .cartridge/tools/live`, which `cleanIndex` refuses; environmental, not scored |
| repo | read `prd.ctg/src/lifecycle.ts:45`, `:103-105`, `:128-175`; `prd.ctg/src/planner.ts:5-9` | block limit 120 000 ms, `cap: 65536`, repository-wide staged-path refusal, `feet` = PRD ∪ spec footprints |
| repo | read `.cartridge/tests/integration/takeover.test.ts:1-140`, `:303-316` | binary resolved from `CARGO_TARGET_DIR`, never built; scratch roots and `XDG_RUNTIME_DIR`; a cold two-`run` case with no daemon |

Limits and isolation: no `prd` transition operation, no `git add`, no commit, no
push, no stash, no edit to any spec or to `prd.md`; no other session's uncommitted
work was touched. The only mutation was moving
`target/cartridge-mcp-waits-verify/debug/cartridge` aside and letting block 4
restore it, inside a git-ignored scratch target directory created for this PRD's
verification. Every block script was extracted verbatim from `spec01.md` into a
private scratchpad subdirectory.

Reviewer identity: independent reviewer agent (round-3 reviewer, Claude Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL (83/100)**.
Unresolved blocking findings: finding 1 — the landing step cannot execute while the
other session's 44 uncommitted lines sit in `cartridge.ctg/src/cli/host.rs`;
finding 2 — PRD acceptance box 2 (bounded failure naming the missing listener) has
neither a Verify block nor a named receipt obligation.
Rounds used / remaining: 3 / 2.
Next action: bounded revision — state the landing precondition for the dirty
`src/cli/host.rs`, restore a deterministic failure-path block (or add it to the
receipt obligation), fix the pre-warm command, state block 5's precondition, and
correct "deliberately do not launch a host"; then re-review in round 4.

## Round 4 — 2026-09-17

Presented revision: root `bfb1cf9`, `cartridge.ctg` `63ff234` with the same 18
dirty files from other sessions. `prd.md` is byte-identical to the revision
round 3 scored; only `specs/spec01.md` changed.

| Input | Content digest |
| --- | --- |
| Plan | `prds/<slug>/prd.md` — sha256 `b109b09fa3428391f3ea0d2c50b7e08019c4ed225e30fb8f05d249784db068b3` (unchanged from round 3) |
| Specs | `prds/<slug>/specs/spec01.md` — sha256 `89a12fadf82a6f43abff05d4192231eaccd113edd44e6863ec6510126f661b1a` |
| Prototype | `.state/loop/<slug>/attempt-1.patch` — sha256 `1a1e56f95817cf6f6b8b88577641251ddcc304681fd9e538ce103c325ce0f273` (unchanged) |
| Material source | `cartridge.ctg/src/cli/host.rs` (working tree, dirty) — sha256 `bde3cb1d4a85c76611d60448ccf136a9a1c5db6cdc694e84a86f28c57b0eb14e` |
| Material contracts | `cartridge.ctg/src/host/socket.rs:47-66` (socket base and per-descriptor tag), `cartridge.ctg/src/host/mod.rs:805-849` (`NotProvided` vs `Unavailable`), `cartridge.ctg/src/host/run.rs:11` (`Host::settled`), `prd.ctg/src/planner.ts:5-9`, `prd.ctg/src/lifecycle.ts:45` |

### The six blocks, run by me from `/Users/feb/dev/cartridge`

| Block | What it is | Exit | Elapsed |
| --- | --- | ---: | ---: |
| 1 | source guards, now with the `awk` return count | **1** — "settle_remote still ends the wait on three identical polls" | <1 s |
| 2 | `cargo test … --bin cartridge -- settled_` | **1** — `0 passed; 16 filtered out`, then "unit case … did not run" | <1 s |
| 3 | `just check cartridge` | **0** | 1 s |
| 4 | `just test cartridge` | **0** — 176 tests run, 176 passed | 13 s |
| 5 | failure path, new | **0** — JSON-RPC error −32603, message "`mcp` is not provided", then "the missing mcp listener was named in 2s, inside the 60 s startup deadline" | 2 s |
| 6 | `just test lifecycle` | **0** — 13 pass, 0 fail, 819 expect() | 48 s |

Every author-reported exit code reproduced. Longest block 48 s against the
engine's `timeout: 120_000` (`prd.ctg/src/lifecycle.ts:45`), and with no lane each
block runs once.

**Block 1 is satisfiable as well as discriminating — verified, not assumed.**
Because this is the last round I built an independent patched reference rather
than trusting the author's: `git -C cartridge.ctg archive 63ff234` of the two
footprint files into a scratch tree, `attempt-1.patch` applied, then step 3's fold
done by hand (`serves` renamed to `settled` with the `starting`/`empty` computation
moved inside it and out of the loop) and the four unit cases appended to
`stdio.rs`. Block 1 against that tree: **exit 0, "source guards ok"**. So the nine
greps and the new `awk` guard are all satisfiable by a natural implementation of
the spec's own steps. The `awk` count is 3 on the live tree and 2 on the reference,
exactly as the author reports; round 3's −1 on this point is closed. The grep'd
`tokio::time::timeout(left, peer.call("status", Value::Null))` sits on a single
93-character line in the reference, inside rustfmt's 100-column limit, so block 3's
`cargo fmt --all --check` cannot reflow it out from under block 1.

**Daemon safety, verified three ways rather than accepted.** Across all six
blocks: the project daemon pid stayed `71453`; its socket directory
`/tmp/cartridge-501/69a3b8e0c7a1/71453/` still holds the same 24 entries; no
`*.ctg/target/debug` directory and no `*.dylib` in the composition was written;
`git -C cartridge.ctg status --porcelain` still reports 18 files. After block 5 no
scratch daemon survives — its trap's `stop` works. The live daemon is genuinely
never reached.

**But not by the mechanism the spec claims** (finding 3 below). Block 5's comment
says it takes "A runtime directory of its own, as takeover.test.ts does".
`cartridge.ctg/src/host/socket.rs:47-55` honours `XDG_RUNTIME_DIR` only when
`<dir>/cartridge` is **shorter than 48 characters**; here `mktemp -d` returns
`/var/folders/_p/…/T/tmp.GVpAWpwZGA`, 63 characters, 73 with the suffix, so the
filter drops it and `base()` falls back to `/tmp/cartridge-501` — the same base the
live daemon uses. I watched the directory count there go 887 → 888 across block 5.
`takeover.test.ts:15` is *not* the same: it uses `fs.mkdtempSync("/tmp/ctgrt-")`,
17 characters, 27 with the suffix, which is honoured. What actually keeps block 5
off the live daemon is `tag(descriptor)` (`socket.rs:64-66`), 12 hex characters of
the project path hash, which is per-project and cannot collide. Safe, but not what
it says, and on a Linux collect host (short `TMPDIR`) the block would isolate by a
different mechanism than it does here.

**The failure-path block does what the finding asked.** Block 5's fixture declares
`listen: ["mcp"]` and fails at load, and I observed each asserted clause hold:
`"listen":["mcp"]` and `"state":"failed"` in `status`, an `"error"` object rather
than a tool list, the name `mcp` in it, and 2 s against the 60 s bound. It is
deterministic, compiles nothing, and consumes the binary block 4 uplifts. It does
**not** discriminate a patched tree from an unpatched one — I ran it against the
live unpatched binary and it passed — and the spec says exactly that in the block's
own comment. That is the right division of labour: blocks 1 and 2 discriminate the
fix, block 5 guards the accepted cost of deleting the shortcut.

**On the message string — the PRD needs no correction.** I traced both paths.
`Host::sender` (`src/host/mod.rs:805-807`) returns `Error::NotProvided` when the
event is not in the *active* directory at all, whose Display is
``  `mcp` is not provided `` (`src/error/mod.rs:31`), and that is block 5's
composition, where the only cartridge failed. `Host::bail`
(`src/host/mod.rs:840-849`) returns `Error::Unavailable { why: "no active listener" }`
when the event *is* in the directory with an empty listener set, and that is the
cold-start composition the PRD's Outcome quotes. Two different compositions, two
different correct messages. PRD Acceptance box 2 says "a message naming the missing
listener" and quotes nothing, so it is accurate as written and block 5 asserts
precisely that clause. **Do not change the PRD body.** What is missing is one
sentence in spec01 (finding 4), because a reader comparing the receipt's
`` `mcp` is not provided `` against the Outcome's quoted string would otherwise
think the fixture reproduces the defect.

**Round-3 items checked off.** The pre-warm command now names the target set
blocks 3 and 4 really build (`nextest run --workspace --no-run`, spec01:279-283).
The block ordering is stated accurately (`:284-290`), including that neither block 5
nor block 6 compiles and that both fail loudly with the binary's path — block 5's
`test -x "$bin"` and `takeover.test.ts`'s throw both do. The false "deliberately do
not launch a host" is replaced by an accurate account (`:157-171`) naming
`takeover.test.ts:303`, `:259` and `:316`; I confirmed all three exist and that
`:303` is a genuinely cold `cartridge run` pair. The standing round-1 deduction is
also closed: "Why only the CLI path changes" (`:71-77`) now names `Host::settled`
and explains why it needs no change — I confirmed at `src/host/run.rs:11` that it
is a lifecycle-event wait with no poll shortcut (the spec cites `:12`, off by one).

### Blocker 1: does a precondition the implementer cannot satisfy answer the finding?

**Yes — accepted, and the finding is resolved.** Not because the obstacle is gone;
because this is everything a plan is permitted to do about it.

1. review-plan.md's own Fails-when row for a plan that is not executable as written
   prescribes "Resolve **or present the disposition** before continuing." Presenting
   the disposition is an authorised outcome of the method, not an evasion of it.
2. Every route that would let the implementer satisfy the precondition himself is
   one this repository forbids: no stash, no revert, no partial commit of another
   session's lines. The 44 lines are user-owned, and the coordinator confirmed
   independently that no live peer session owns them. A plan cannot be marked down
   for declining the only actions available to it when those actions are prohibited
   — the alternative would be a plan that instructs the implementer to do something
   the rules forbid, which is strictly worse.
3. What a plan *can* do, this one now does. Step 0 (`:102-105`) makes
   `git -C cartridge.ctg status --porcelain -- src/cli/host.rs` an executable first
   step with a defined stop-and-report; the "Landing hazard" section (`:191-226`)
   names both failing routes exactly as I found them — the ff-only refusal and the
   gitlink collapse, cited to `prd.ctg/src/planner.ts:5-9` — rules out `git add -p`
   with a reason (it produces a submodule tree nobody built or gated, and the
   receipt would certify it), and names the remedy's owner. That converts a latent
   trap into a gate. It is a behavioural change, not prose.
4. Consistency. The staged superproject rename blocks collect today and is not
   scored against this spec because it is environmental. The dirty `host.rs` is the
   same kind of fact, and the spec now handles it more carefully than the rename is
   handled anywhere on this board.

The distinction the coordinator should carry forward: **the plan is ready; the
landing waits on an external event.** Those are different states, and the review
gate scores the first.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Real, user-visible first-MCP-client failure; one outcome, one owner; the baseline stays honestly probabilistic (31 of 108). Round 3's −2 is resolved: "What is gated and what is not" (`:157-171`) now states what the blocks really do, names the cold-start coverage already inside the gate at `takeover.test.ts:303`/`:259`/`:316`, and restates the true property as "no block touches the live project daemon" — which I verified. −1: spec01 still does not say that its own block-5 fixture answers `` `mcp` is not provided `` rather than the string the PRD's Outcome quotes, so the collect receipt will not match the PRD at a glance. |
| Ownership and reuse | 20 | Owner `runtime`; one guard in the shared function repairs `run`, `launch` and `mcp` together; reuses the already-wired `stdio.rs` unit module, the existing `listen` field and the existing `explain` reader; no new file, module, RPC or setting; `verify_timeout()` left to its three in-process callers; a shared helper declined with a reason. The standing round-1 deduction is now closed by `:71-77`, which names `Host::settled` (`src/host/run.rs:11`, verified: a lifecycle-event wait with no poll shortcut) and explains why `settle_remote` exists separately at all. Nothing left to deduct. |
| Dependencies and implementable slices | 19 | Round 3's blocking finding 1 is resolved by Step 0 plus "Landing hazard" (see above). The pre-warm command is corrected to the target set blocks 3 and 4 actually build. The block ordering is written down and matches what I established experimentally last round. One source file plus one test file, prototype attached, overlap disclosed with a defensible order, no-lane shape matching the engine. −1: block 5's isolation mechanism is platform-dependent and inert here (`socket.rs:53`'s 48-character filter against a 73-character path), so a collect on a short-`TMPDIR` host and a collect on this one isolate by different mechanisms — the same portability trap the spec is careful about elsewhere for `rustc-wrapper = "kache"`. |
| Observable acceptance and baseline evidence | 19 | Round 3's blocking finding 2 is resolved: every acceptance box now has a gate, and I ran all six. Block 1 exits 1 on the live tree **and exits 0 on a patched reference I folded myself from the prototype**, so the gate is satisfiable as well as discriminating; the new `awk` guard reads 3 live and 2 patched, closing round 3's −1 about a differently spelled early return. Block 2 exits 1 on the live tree. Block 5 exits 0 in 2 s with every asserted clause observed. Blocks 3, 4 and 6 exit 0. −1: block 5 gates the `failed` half of the accepted cost — the half the spec itself says returns at once — and not the `starting`-forever half that actually spends the 60 s; gating that would cost a 60 s block to prove intended behaviour, so the omission is proportionate but it is an omission. `grep -qF 'mcp'` is also a weak naming assertion for a three-letter string, adequate only because it is paired with the `"error"` assertion. |
| Failure, recovery and compatibility | 18 | The accepted cost is named and now gated. Isolation verified rather than trusted: pid `71453` unchanged across all six blocks, the live socket directory unchanged at 24 entries, no `*.ctg/target/debug` or `*.dylib` write, the submodule's dirty set unchanged at 18, `target/` git-ignored, no scratch daemon left alive. Margin 48 s of 120 s on the longest block, which compiles nothing. The footprint's real reach is now stated honestly (`:221-226`: the two-file list "is an honest statement of what the implementer touches, not a protection the engine enforces"), closing round 3's finding 6. −1: the stated isolation mechanism is wrong (finding 3) — safe in effect, but the third time across rounds that a claim the spec makes about its own blocks does not survive measurement. −1: block 5 leaves a socket directory under the shared `/tmp/cartridge-501` base on every collect (887 → 888 here), and `returns=$(awk … \| grep -c 'return;')` under `sh -eu` exits the block silently when the count is 0, losing its own diagnostic — it fails closed, so it is hygiene rather than risk. |
| Reviewer total | **95** / 100 | PASS: at or above 90, no blocking findings. |

### Findings

Both round-3 blockers are resolved. Nothing below blocks.

1. **Resolved — the landing step.** Step 0 (`:102-105`) and "Landing hazard"
   (`:191-226`). Accepted as an authorised disposition for the reasons argued above.
   The precondition is unmet today: `git -C cartridge.ctg status --porcelain --
   src/cli/host.rs` prints ` M src/cli/host.rs`. The implementer must stop at Step 0
   until the owner of the `stop_when_idle` / `--idle-timeout` work commits it.
2. **Resolved — PRD box 2 has a proof path.** Block 5 (`:367-406`), observed exit 0
   in 2 s with every clause asserted and holding.
3. **Non-blocking — the block-5 isolation comment is false on this platform.**
   `spec01:382-383` and `:291-295` claim an `XDG_RUNTIME_DIR` "of its own, as
   takeover.test.ts does". `cartridge.ctg/src/host/socket.rs:47-55` drops
   `XDG_RUNTIME_DIR` unless `<dir>/cartridge` is under 48 characters; `mktemp -d`
   here yields 73, so the host falls back to the shared `/tmp/cartridge-501` base
   (directory count 887 → 888 across the block). `takeover.test.ts:15` avoids this
   by using a short `/tmp/ctgrt-` prefix. Isolation still holds through
   `tag(descriptor)` (`socket.rs:64-66`), and I verified the live daemon is
   untouched, so this is an accuracy fix, not a safety one. Smallest change:
   `rt=$(mktemp -d /tmp/ctgmcp-XXXXXX)` in block 5, and reword the two comments to
   say the separation is per-descriptor, with the short runtime directory as
   belt-and-braces.
4. **Non-blocking — name the message block 5 actually produces.** One sentence
   beside block 5: this composition answers `` `mcp` is not provided ``
   (JSON-RPC −32603, `src/error/mod.rs:31`) rather than the Outcome's
   ``service `mcp` unavailable: no active listener``, because the failed cartridge
   leaves the event out of the active directory entirely
   (`src/host/mod.rs:805-807`) while a *starting* one leaves it present with no
   listener (`:840-849`). The PRD body is correct and needs no edit.
5. **Non-blocking — two hygiene nits.** `returns=$(awk … | grep -c 'return;')`
   exits the block with no diagnostic when the count is 0 (`|| true` after `grep -c`
   restores the message; it already fails closed, so this is cosmetic). And
   `Host::settled` is at `src/host/run.rs:11`, not `:12`.
6. **Endorsed as written**, re-checked this round: the `startup_timeout()` move; the
   `key: &str` threading; the deletion of `stable`/`last` and the unrepresentability
   argument; the `tokio::time::timeout(left, …)` wrapper and "ship both, this one
   first"; the no-lane landing shape; `--locked` and the `${CARGO_TARGET_DIR:-…}`
   form; the explicit `if grep -qF …; then exit 1; fi` negative guards; the demotion
   of the 15-cold-start fixture to an implementer's probe with the receipt
   obligation retained; and the division of labour between the discriminating blocks
   (1 and 2) and the accepted-cost gate (5).

Disposition: **keep — ready to implement.** Two preconditions stand outside the
plan and outside this score, and the coordinator should hold both in view:
`cartridge.ctg/src/cli/host.rs` must be clean before Step 1, and the superproject
index must be free of the staged `.cartridge/tools/pi-voice -> .cartridge/tools/live`
rename before `prd collect` will run at all (`prd.ctg/src/lifecycle.ts:103-105`).

### Validation

| cwd | command | exit / result |
| --- | --- | --- |
| repo | Verify block 1 (with the new `awk` guard), verbatim | **1** — "settle_remote still ends the wait on three identical polls" |
| scratch reference | Verify block 1, verbatim, against `63ff234` + `attempt-1.patch` + step 3's fold + the four unit cases, all applied by me | **0** — "source guards ok" |
| repo | `awk '/^async fn settle_remote\(/{b=1} b&&/^\}/{b=0} b' … \| grep -c 'return;'` | 0 — **3** live, **2** on the reference |
| repo | Verify block 2, verbatim | **1** — `0 passed; 16 filtered out` |
| repo | Verify block 3 (`just check cartridge`) | **0**, 1 s |
| repo | Verify block 4 (`just test cartridge`) | **0**, 13 s, 176/176 |
| repo | Verify block 5 (failure path), verbatim | **0**, 2 s — `{"error":{"code":-32603,"message":"…is not provided"},"id":2,"jsonrpc":"2.0"}` |
| repo | Verify block 6 (`just test lifecycle`) | **0**, 48 s, 13 pass / 819 expect() |
| repo | `pgrep` for the project daemon before and after every block | pid `71453` throughout |
| repo | `ls /tmp/cartridge-501/69a3b8e0c7a1/71453/ \| wc -l` before and after | 24 → 24 |
| repo | `ls -d /tmp/cartridge-501/*/ \| wc -l` around block 5 | 887 → **888** — block 5's host used the shared base, not `$XDG_RUNTIME_DIR` |
| repo | `mktemp -d` length check against `socket.rs:53`'s 48-character filter | 63 chars, 73 with `/cartridge` — the filter drops it |
| repo | `find` for `*.ctg/target/debug` and `*.dylib` written in the window | no match |
| repo | `git -C cartridge.ctg status --porcelain \| wc -l` after the full run | 18, unchanged |
| repo | `pgrep -fl cartridge` after block 5 | no scratch daemon survives; only pid `71453` and unrelated sessions' clients |
| repo | read `src/host/mod.rs:795-855`, `src/error/mod.rs:31`, `src/host/run.rs:8-20`, `src/host/socket.rs:40-75` | `NotProvided` vs `Unavailable` paths, `Host::settled`, socket base and per-descriptor tag |

Limits and isolation: no `prd` transition operation, no `git add`, no commit, no
push, no stash, no edit to `prd.md` or to any spec, and no other session's
uncommitted work touched. Writes were confined to a private scratchpad
subdirectory and to the git-ignored `target/cartridge-mcp-waits-verify`; the
patched reference tree was built from `git archive` and never written back.

Reviewer identity: independent reviewer agent (round-4 reviewer, Claude Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS (95/100)**.
Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: proceed to implementation. Hold at Step 0 until
`git -C cartridge.ctg status --porcelain -- src/cli/host.rs` prints nothing, and
clear the staged superproject rename before attempting `prd collect`. Findings 3-5
are one-line corrections that can ride along with the implementation rather than
consuming the last round.
