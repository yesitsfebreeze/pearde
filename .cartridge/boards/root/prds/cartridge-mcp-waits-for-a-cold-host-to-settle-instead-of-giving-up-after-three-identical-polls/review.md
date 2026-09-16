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
