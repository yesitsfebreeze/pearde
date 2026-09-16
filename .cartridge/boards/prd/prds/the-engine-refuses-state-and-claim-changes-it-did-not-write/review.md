# @prd/the-engine-refuses-state-and-claim-changes-it-did-not-write review history

Plan: @prd/the-engine-refuses-state-and-claim-changes-it-did-not-write, `prd.ctg/.cartridge/boards/prd/prds/the-engine-refuses-state-and-claim-changes-it-did-not-write/prd.md`.
Scope: leaf. One observable outcome: the engine detects and refuses `state`/`claim`/`commit` changes written outside engine ops.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
When copying this template, resolve that link relative to the actual owner board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: prd.ctg HEAD 6f030296 (footprint `src/`, `.cartridge/tests/` and `.cartridge/.gitignore` identical to the probe base 75a8f8f7 and to the patch base 6807f025). `prd.md` is untracked and has never been committed. `specs/spec01.md` is committed in 75a8f8f7.

| Input | Content digest |
| --- | --- |
| Plan | `prds/the-engine-refuses-state-and-claim-changes-it-did-not-write/prd.md` SHA-256 `7e59fad88527cc1b576a5b2de62e4791a304a3a23475ad5636ca9c69cf67ea50` (untracked) |
| Specs | `specs/spec01.md` SHA-256 `9ccba7823f2aaa5e5bc10db609cf5e73f4e5d7781228db256ac988436ea47aca` |
| Material contracts/dependencies | `.state/loop/…/analyst-1.md` `aa67d35f…f541e`; `.state/loop/…/attempt-1.patch` `71d3fb0b…4190e`; `src/records.ts` `b6f88b29…13724`; `src/lifecycle.ts` `a5e34ee2…d4072`; `src/engine.ts` `ed3ce2e3…c97`; `src/service.ts` `c423d868…90f1`; related PRD @prd/the-records-test-knows-deferred-and-the-current-root-board |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | A real incident from 2026-09-16 with one bounded outcome. The Planning note correctly scopes out the engine-routed foreign release. −3: the Outcome still opens with that second incident as motivation, and the "restores the recorded values" reconcile path in the Outcome has no op (spec: hand restore only). |
| Ownership and reuse | 17 | One owner (prd.ctg). Reuses `edit()` as the single controlled-field writer (verified: claim/release/specced/refine/defer/retry/unblock via `transition()` line 244, collect line 179), `atomic()`, the gitignored `/boards/**/.state/` and the mutation lock. −3: `add` (lifecycle.ts:197 writes `state: open` via `atomic()`, not `edit()`) is left outside the store on purpose, which causes B1. The spec's "restart the daemon" claim misreads `service.ts:89`: the daemon spawns `src/cli.ts` for each op, so it picks up new code at once. The real old-code window is in-flight `prd run`/`collect` processes. |
| Dependencies and implementable slices | 18 | One spec, complexity 2, with a working prototype. Stale `records.test.ts` is split out to the related PRD, and box 4 is amended to match. −2: the PRD footprint lists `records.test.ts`, which the spec never touches. `cli.ts` help (the op list) is outside the footprint, so `adopt` stays undiscoverable except through the error text. |
| Observable acceptance and baseline evidence | 16 | Baseline and patched runs reproduced (below). The tamper test fails without the src hunks, and the Verify block is temp-board only. −4: spec acceptance box 3 says `add` raises no problem, but probe P1 shows it can. There is no test for `commit` tampering or for `add` over a leftover digest. The second new test also passes without the src change, so it guards only against false positives. |
| Failure, recovery and compatibility | 11 | Rollout on a copy of the live boards is clean (574 records, 0 field problems, 574 digests, check 2.3 s vs 1.9 s). The link bootstrap and 50 ms re-read are sound for unlocked readers. −9: B1 (a fresh `add` is refused over a stale digest). B2: `adopt` is an unaudited, identity-less override, and the refusal text tells whoever tampered to run it. Also unhandled: a crash between the record rename and the digest rename leaves a permanent report, `git checkout/reset/stash/pull` of records reports as tampering with no documented recovery, and old-code processes can create false reports during rollout. |
| Reviewer total | 79 / 100 | |

Findings and concrete revisions:

- **B1 (BLOCKING): a new PRD at a reused path inherits a stale digest and is refused.** Probe P1: `claim one` → delete the dir (retire/rehome) → `prd add one` exits 0. Then `check` exits 2 with `one: state changed outside the engine (recorded "analyzing", found "open"); claim changed … (recorded "w …", found null)`, and `claim one w2` exits 2 with the same text. This contradicts spec box 3 ("`add` … raise no problem"). Digests are keyed by path and never cleared. Fix: `add` calls `recordFields(file)` after its `atomic()` write (skipped with `--dry`), plus a test "add over a leftover digest raises no problem". Optionally have `check` skip or clean orphan digests.
- **B2 (BLOCKING): `adopt` launders silently.** Probe P3: `claim one alice`, then hand-write `claim: "mallory now"`, then `adopt one` exits 0 (`Adopted one analyzing`), then `release one open` exits 0. `.state/` held only `fields/one.json`, so nothing records who adopted or what was overwritten. The refusal text ends with "run prd adopt to accept it", which points an agent that made the edit straight at the override. Fix: `adopt <ref> <identity>` (same identity pattern as `claim`). Append one JSON line `{ref, by, at, recorded, found}` to `<board>/.state/fields/adoptions.jsonl` inside the mutation lock, and print the recorded→found diff in the output. Also make `adopt` refuse when the recorded claim is non-null and the found claim names a different holder, unless the identity equals the recorded claimant. Add tests for both.
- N1: Replace the "restart the daemon" note. The service runs the CLI for each op (`service.ts:89`), so the new code applies immediately. The real window: an old-code `prd run`, or this PRD's own `collect` (it loads old code, ff-merges, then `edit()`s `done` without a digest). A concurrent new-code `check` in that window bootstraps `claimed`, and this PRD then reports itself. Rollout step: no in-flight `prd run` during collect. Afterwards run `prd check --board root` and adopt (with identity) only the refs the engine itself wrote.
- N2: The crash window between `atomic(file)` and `recordFields` in `edit()` leaves a permanent false report. Document `adopt` as the recovery.
- N3: Probe P2: `git checkout -- prd.md` after `claim` is reported as tampering. That is correct, but name it under recovery (restore the recorded values or adopt), because coordinators commit and move records with git.
- N4: Make the refusal name the full command, `prd adopt <ref> <identity> --board <board>`. Add `adopt` to the `cli.ts` help op list, or state why it is hidden.
- N5: Tests: cover `commit` tampering and a `refine`/`specced` refusal, not only claim/release/collect.
- N6: Drop `records.test.ts` from the PRD footprint, or add it to the spec. Commit `prd.md`, which is currently untracked.

Disposition: revise (keep scope and design; fix B1 and B2 in spec01 and the prototype, then fold in N1–N4).

Validation (scratch detached worktree of prd.ctg at 75a8f8f7 under the session scratchpad, `node_modules` symlinked, temp boards and a board copy only; worktree removed without `--force`):
- `git apply --check attempt-1.patch` → applies cleanly.
- Baseline `bun test` engine/service/parity/event-stream/host → 16/11/14/6/0 pass, 0 fail.
- Test hunk only → exit 1, `(fail) hand edits to state or claim are reported and refused until adopted`, 17 pass / 1 fail.
- Full patch → engine 18 pass. Service 11, parity 14, event-stream 6: no regressions. records 0 pass / 2 fail (pre-existing, same as baseline per analyst-1).
- Probes P1–P4 (temp boards, `bun test` probe file): P1 false refusal after `add` (B1). P2 git restore reported. P3 adopt launders with no audit (B2). P4 `check` bootstraps a digest, `status` is unaffected, `adopt --dry` writes nothing.
- Rollout: live `.cartridge/boards` rsynced (without `.state`/`.lanes`) into the worktree. `bun src/cli.ts check --board root --json`, run twice → exit 0 both times, 574 records, 0 problems, 574 digest files. 2.33 s / 2.06 s vs 1.92 s unpatched.
- No command ran against the live boards. Nothing was committed.

Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: B1 (`add` over a stale digest is refused), B2 (`adopt` unaudited, no identity, launders foreign claims).
Rounds used / remaining: 1 / 4.
Next action: bounded revision of spec01 and attempt-1.patch for B1 and B2 (plus N1–N4), then round 2.
