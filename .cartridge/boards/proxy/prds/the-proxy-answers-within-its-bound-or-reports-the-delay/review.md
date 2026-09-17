# @proxy/the-proxy-answers-within-its-bound-or-reports-the-delay review history

Plan: `@proxy/the-proxy-answers-within-its-bound-or-reports-the-delay`,
`prd.ctg/.cartridge/boards/proxy/prds/the-proxy-answers-within-its-bound-or-reports-the-delay/prd.md`.
Scope: executable leaf — one observable outcome (a proxy stall names its stage,
its elapsed time and its bound instead of returning a silent timeout).
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: spec01 as on disk at review time (SHA-256
`1faf7ab38808ab16ea8333f77d6ba068322d3bfca079232666f9854270150270`), against
`proxy.ctg` HEAD `0692c18626950dcf0d4847dff7acae4bf37e7a06`. That checkout is
dirty and none of the diff belongs to this PRD: `M .cartridge/tests/unit/tests.rs`,
`M .cartridge/tests/unit/wire/tests.rs`, `M Cargo.lock`, `M Cargo.toml`,
`M src/context.rs`, `M src/lib.rs`, `M src/notice.rs`, `M src/service.rs`,
`M src/wire.rs`, `?? src/evidence.rs`.

| Input | Content digest |
| --- | --- |
| Plan | `prds/…/prd.md` — `1d8743b93daf8d66733772776db0fbd4444102d6ba681abf29741381b6eb2882` |
| Specs | `prds/…/specs/spec01.md` — `1faf7ab38808ab16ea8333f77d6ba068322d3bfca079232666f9854270150270` |
| Material contracts/dependencies | `proxy.ctg@0692c18` (`Cargo.toml`, `cartridge.json`, `src/service.rs`, `src/usage.rs`, `src/notice.rs`, `.cartridge/tests/unit/tests.rs`); `cartridge.ctg` `src/transport/cartridge.rs:95`, `src/host/plan.rs:322-324`, `src/host/socket.rs`, `src/loader/document.rs:179-183`, `.cartridge/settings.json:26-31`; `lsp.ctg/cartridge.json:96`; `prd.ctg/src/lifecycle.ts:21-25,39-50,120-175`, `src/planner.ts:5-9` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The outcome is real and the three edits are minimal and correctly aimed: at `0692c18` `src/service.rs:317` returns a bare `"proxy request deadline exceeded"`, `run()` propagates every downstream wait with a bare `?` (`:661-665`, `:741`, `:743-747`, `:785-787`), and `cartridge.json` declares `events.proxy` with no `timeout_ms` — all three verified at HEAD. Deducted for scope honesty: the spec never states plainly that the PRD's `mcp did not answer in time` evidence is out of scope, and it silently re-reads PRD acceptance 1's "the bound it exceeded" as "elapsed ms plus a knob name" for downstream stalls. |
| Ownership and reuse | 18 | Correct owner — for the `proxy` event the proxy is the provider, so `events.proxy.timeout_ms` is the only place a bound can be declared; the shape is established (`lsp.ctg/cartridge.json:96` = 600000, verified) and validation rejects only `0` (`loader/document.rs:179-183`, verified). No new files, one nine-line helper, and the skipped host-settings read is justified — `cartridge.ctg/src/host/socket.rs` serves exactly `auth`, `bail`, `cartridges`, `gather`, `reload`, `snapshot`, `status`, `stop`, `subscribe`, confirmed by grep. Deducted only for the unstated placement of `staged` (free fn vs associated fn changes the call sites to `Self::staged`). |
| Dependencies and implementable slices | 6 | Blocking: at `0692c18` `Cargo.toml:17` carries `evidence = { path = "../memo.ctg/evidence" }`, which cannot resolve from a lane at `boards/proxy/.lanes/<slug>` (only `cartridge.ctg` sits beside it). Reproduced on a `git archive 0692c18` extraction: both cargo blocks die in 0 s with "failed to load manifest for dependency `evidence`". The analyst's "no path dependencies … the lone-worktree hazard does not apply" describes only the working tree, where that dependency is uncommittedly removed. The spec therefore also has an unstated hard prerequisite: it measured a tree that only exists uncommitted. |
| Observable acceptance and baseline evidence | 8 | I ran all four blocks at HEAD myself. Blocks 1 and 3 exit 1 with the messages the spec predicts; block 2 exits 1 on the pinned test name once a sibling `memo.ctg` is present (55 passed at HEAD, not the dirty tree's 57), cold run 5.9 s, well inside the engine's 120 s. But block 4 exits **1** at HEAD — `cargo fmt --all --check` reports drift at `.cartridge/tests/unit/tests.rs:699` and `.cartridge/tests/unit/wire/tests.rs:32`, the second outside the footprint. And the spec's own named main hazard has no executable proof: the new test asserts `classify("model request (429 rate limited)")` on a literal, which already passes at HEAD and keeps passing under a blanket wrap, and no existing test drives an upstream error through `run()` (every `429` assertion in `tests.rs:2490-2520` calls `classify` directly). |
| Failure, recovery and compatibility | 13 | Compatibility is reasoned and verified: `usage.rs:248` and `notice.rs:49` are prefix matches so appending to the deadline message is safe; the `ends_with` guard keeps the notice hint firing and leaves `UPSTREAM_PREFIX` errors at the front untouched; `notice.rs` is correctly in the footprint with an add-if-absent instruction, because that branch genuinely does not exist at `0692c18` (confirmed by `git show`). Deducted: the residual failure is mitigated only by a doc sentence that no acceptance box and no Verify block pins, and it cannot be closed at all — `timeout_secs` max is 86400 s while `event_timeout_ms` max is 86400000 ms, so a raised `timeout_secs` always restores the undiagnosed host timeout. The trust/reload consequence of editing `cartridge.json` is also absent from the spec. |
| Reviewer total | 61 / 100 | Design is sound and minimal; the lane world and the proof of its own main hazard are not. |

Findings and concrete revisions:

**Blocking**

1. **The lane cannot build at HEAD.** `git -C proxy.ctg show 0692c18:Cargo.toml`
   contains `evidence = { path = "../memo.ctg/evidence" }`; the working tree
   removes it (that is what untracked `src/evidence.rs` and the `crate::evidence::`
   hunks in `src/service.rs` are). A lane is `git worktree add … HEAD` at
   `boards/proxy/.lanes/<slug>` (`prd.ctg/src/lifecycle.ts:21-25,225`), so
   `../memo.ctg/evidence` resolves to `boards/proxy/.lanes/memo.ctg/evidence`,
   which does not exist. Verify blocks 2 and 4 both exit 1 in 0 s there, before
   any code is compiled. Recommendation: either name the pending evidence-vendoring
   work as a hard prerequisite that must land before this lane is cut, or make the
   cargo blocks provide the sibling, or drop the lane and collect in `repo`.
   Resolution: open.
2. **Verify block 4 fails at HEAD for a reason the implementer cannot fix inside
   the footprint.** `cargo fmt --all --check` at `0692c18` reports
   `.cartridge/tests/unit/tests.rs:699` and `.cartridge/tests/unit/wire/tests.rs:32`;
   the uncommitted diff is exactly those two fmt fixes, which is why the analyst
   saw exit 0. `wire/tests.rs` is not in the footprint, so formatting it would be
   an out-of-footprint write that collect rejects. Recommendation: add
   `.cartridge/tests/unit/wire/tests.rs` to the footprint, or narrow block 4 to the
   crate's own sources, or make the prerequisite in finding 1 cover it.
   Resolution: open.
3. **The `usage::classify` trap is named but not pinned.** The spec calls the
   `ends_with` guard "load-bearing" and the acceptance box says a router rejection
   must be untouched, but the named test
   `a_stalled_stage_names_the_stage_and_how_long_it_ran` proves it with
   `classify("model request (429 rate limited)")` — a literal that never passes
   through `staged`, true at HEAD and true under a blanket wrap. Block 3's
   `grep 'ends_with("did not answer in time")' src/service.rs` only proves the
   string is present. Recommendation: assert through the service — drive the
   `"router"` call to `Err("model request (429 Too Many Requests): {}".into())`
   and assert the resulting failure still starts with `model request (429` and
   classifies 429. The fixtures already allow it (`service.call = Arc::new(…)`).
   Resolution: open.

**Non-blocking**

4. `tests.rs:832-836`, `:2113-2115` and `:2531` are working-tree line numbers; the
   uncommitted hunk `@@ -702 +702,5 @@` shifts everything after line 702 by +4, so at
   HEAD `timeout_secs = 1` is at `:2110` and the classify assertion at `:2527`
   (`:2531` is a comment). The claims themselves hold at HEAD; only the numbers move.
5. `usage.rs:214-222` is cited for `classify`; at HEAD the function is `219-260`
   and `214` is blank. `cartridge.json:12-52` is cited for `events.proxy`; `"events"`
   opens at `:14` and `"proxy"` at `:15`.
6. Scope honesty: the analyst states plainly that the PRD's `mcp` stalls are the
   sibling `@mcp/a-cartridge-call-is-cancellable-and-bounded`'s territory; the spec
   does not. As written, PRD acceptance 1 cannot honestly be ticked for
   `mcp did not answer in time` by this spec, and for downstream stalls it reports
   elapsed ms and a knob name rather than "the bound it exceeded". Fix the wording,
   not the footprint.
7. The coupling doc line is the entire mitigation for the residual case and nothing
   pins it: acceptance box 1 and Verify block 1 check only `timeout_ms > 1800000`.
   And the residual case cannot be closed — `timeout_secs` max 86400 s equals
   `event_timeout_ms` max 86400000 ms, so no manifest value strictly exceeds a
   maximally raised `timeout_secs`. Say so and pin the doc string.
8. The spec says collect "sweeps every changed in-footprint path"; the sharper
   consequence is that `git merge --ff-only` of the lane into `repo`
   (`lifecycle.ts:167`) aborts outright while `src/service.rs` and `src/notice.rs`
   are locally modified. Same remedy, harder deadline.
9. `staged`'s placement is unstated; inside `impl Service` the four call sites must
   read `Self::staged(...)`. Block 3's grep matches either spelling, so this only
   costs the implementer a compile.
10. The footprint uses absolute paths. The engine resolves them
    (`planner.ts:8` `path.resolve(root, p)`), so this is not a defect, but every
    other spec on these boards uses repo-relative paths.
11. The analyst's report names revision
    `6e66d22bda90384a2f5bae06f7e559b3dd43d3869be2799915f9289e30aa53d7`, which is not
    the digest of the spec on disk. The spec reviewed here is the on-disk one.
12. The unreproduced stall is **not** a finding. The 60000 ms / 1800 s mismatch is a
    static three-link chain and I re-verified every link independently:
    `cartridge.json` declares `events.proxy` with no `timeout_ms`;
    `host/plan.rs:322-324` applies `settings::host().event_timeout_ms`;
    `cartridge.ctg/.cartridge/settings.json:26-31` defaults it to 60000. No timing
    run is owed, and Verify block 1 pins the manifest side deterministically.

Disposition: revise. The design survives review; the lane world and the proof do not.
Validation: `sh -eu -c` on a `git archive 0692c18` extraction of `proxy.ctg`
(`$SCRATCH/head-tree`, cwd = tree root, `CARGO_TARGET_DIR` under the scratchpad) —
block 1 exit 1 (`events.proxy.timeout_ms is None; it must be an integer > 1800000`),
block 3 exit 1 (`the deadline message does not quote proxy.timeout_secs`),
block 2 exit 1 in 0 s with no sibling (`failed to load manifest for dependency evidence`)
and exit 1 in 9 s with a symlinked `../memo.ctg` (`missing or failed:
tests::deadline_message_names_the_bound`; suite itself 55 passed, 0 failed; cold
`cargo test --lib` 5.9 s against the 120 s engine limit at `lifecycle.ts:45`),
block 4 exit 1 in 0 s with no sibling and exit 1 in 0.2 s with one (`cargo fmt
--all --check` drift). Nothing in `proxy.ctg` was modified; `git status --porcelain`
was identical before and after.
Reviewer identity: reviewer-1 (round 1).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: 1 (lane cannot build at HEAD — `../memo.ctg/evidence`
path dependency), 2 (Verify block 4 fails at HEAD on out-of-footprint fmt drift),
3 (the `usage::classify` trap has no executable proof).
Rounds used / remaining: 1 / 4.
Next action: bounded revision addressing findings 1–3, then round 2.

## Round 2 — 2026-09-17

Presented revision: spec01 as on disk at review time (SHA-256
`edcb260e017b3b43682b7da23c0e7563d71beca8c4db1ae62b0bcb02d5361c3a`, the revision
carrying the Scope section, the "builds at HEAD, but not hermetically" base, the
scoped-gate Verify block 5 and the third test
`an_upstream_rejection_survives_the_stage_wrapper`), against `proxy.ctg` HEAD
`0692c18626950dcf0d4847dff7acae4bf37e7a06`, still dirty with the same ten
unrelated paths. `prd.md` is unchanged from round 1.

| Input | Content digest |
| --- | --- |
| Plan | `prds/…/prd.md` — `1d8743b93daf8d66733772776db0fbd4444102d6ba681abf29741381b6eb2882` (unchanged) |
| Specs | `prds/…/specs/spec01.md` — `edcb260e017b3b43682b7da23c0e7563d71beca8c4db1ae62b0bcb02d5361c3a` |
| Material contracts/dependencies | `proxy.ctg@0692c18` (`cartridge.json`, `src/service.rs`, `src/usage.rs`, `src/notice.rs`, `src/lib.rs`, `.cartridge/tests/unit/tests.rs`); `cartridge.ctg@63ff234` (`src/host/plan.rs:299-301`, `.cartridge/settings.json:19-25`, `src/host/socket.rs:434-465`, `src/loader/document.rs:163-167`); `prd.ctg@3ef3426b` (`src/lifecycle.ts:45,166`, `src/planner.ts:5-9`); `lsp.ctg/cartridge.json:96`; `mcp` board child `the-mcp-event-declares-its-own-bound` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The Scope section now states plainly that only the proxy side closes here and names the child `@mcp/a-cartridge-call-is-cancellable-and-bounded/the-mcp-event-declares-its-own-bound`, which exists on disk with `repo: mcp.ctg` and a `cartridge.json` footprint; deducted because PRD acceptance 1's "the bound it exceeded" still ships as elapsed ms plus a knob name for downstream stalls, so a verifier ticking that box has to accept the spec's (disclosed, and platform-forced — `host/socket.rs` serves no settings RPC) reading. |
| Ownership and reuse | 19 | Correct owner and an established shape: `lsp.ctg/cartridge.json:96` is `"timeout_ms": 600000` verbatim, `loader/document.rs:163-167` at `63ff234` rejects only `0` so `1860000` loads, the `staged` placement is now stated (`Self::staged`), and no new file appears — I implemented the whole spec touching exactly the four footprint paths. |
| Dependencies and implementable slices | 18 | The lane world is now right: at `boards/proxy/.lanes/<slug>` the `cartridge.ctg` and `memo.ctg` symlinks exist, a HEAD tree placed there builds and tests clean (55 passed, 7.4 s), and the non-hermetic consequence is stated with the sibling's 39 uncommitted files re-counted; the `git merge --ff-only` landing hazard is correctly re-cited to `lifecycle.ts:166`. Deducted for finding 12: a faithful implementation of the Design snippets fails Verify block 3 on formatting alone. |
| Observable acceptance and baseline evidence | 19 | I re-derived everything: all five blocks exit 1 at HEAD, each for an in-footprint reason; after implementing the spec all five exit 0 (58 passed, the three names pinned); block 5's scoped `rustfmt` names only `tests.rs:699` and passes after formatting that one in-footprint file while `cargo clippy --workspace --all-targets` exits 101 out of footprint at `wire/tests.rs:29` and `cargo clippy --lib` exits 0; and the stated falsification holds — deleting the `ends_with` guard reddens exactly `an_upstream_rejection_survives_the_stage_wrapper` (57 passed, 1 failed) with the other two green. Deducted for finding 13. |
| Failure, recovery and compatibility | 17 | Prefix contracts re-verified safe (`usage.rs:248-250`, `notice.rs:49`), the guard's load-bearing role is now proven rather than asserted, and the residual is stated honestly with its ceiling equality confirmed (`timeout_secs` max 86400 s, `event_timeout_ms` max 86400000 ms). Deducted for finding 11: `timeout_ms` is declared per event, so the new 1 860 000 ms bound covers all five `proxy` ops while only `request` has an inner deadline, and the spec never says so. |
| Reviewer total | 91 / 100 | The three round-1 blockers are resolved on re-derived evidence; what remains is friction and one unexamined side effect, none of it blocking. |

Findings and concrete revisions:

**Blocking**: none.

Round 1's three blockers, re-tested:

1. **Lane build — resolved, and the replacement hazard is stated correctly.** Round 1's
   reproduction was in a scratch extraction, which is the wrong world. At the real lane
   path the siblings exist; a `0692c18` tree at
   `boards/proxy/.lanes/reviewer2-probe` ran `cargo test --lib` to exit 0, 55 passed,
   0 failed in 7.4 s. The spec now records the correct hazard — the lane compiles
   against the live `memo.ctg` working tree (`git -C memo.ctg status --porcelain | wc -l`
   → 39, matching the spec) in both passes with nothing pinning it.
2. **Out-of-footprint gates — resolved.** At HEAD `cargo fmt --all --check` exits 1 on
   `tests.rs:699` **and** `wire/tests.rs:32`, and `cargo clippy --workspace --all-targets`
   exits 101 with `cloned_ref_to_slice_refs` at `wire/tests.rs:29:31` — the author's
   second blocker is real and round 1 did miss it (the `sh -eu` abort on the fmt line
   masks it). The replacement is correct: scoped `rustfmt --check` exits 1 naming only
   `tests.rs:699` (one `Diff in` line; `wire/tests.rs` is reached through `src/wire.rs:422`,
   which is not in the scoped list), and `cargo clippy --lib` exits 0 in 4.5 s. After
   `rustfmt` on that one in-footprint file — a single hunk, one file — block 5 exits 0.
3. **The `usage::classify` trap — resolved, and the proof falsifies.** I implemented the
   spec (all three edits, the `notice.rs` branch, the three tests) in a throwaway copy at
   the lane path: 58 passed, block 2 exits 0 with all three names present. Deleting the
   `ends_with` guard so the wrap is unconditional turns exactly
   `an_upstream_rejection_survives_the_stage_wrapper` red (`57 passed; 1 failed`) while
   `deadline_message_names_the_bound` and
   `a_stalled_stage_names_the_stage_and_how_long_it_ran` stay green — and nothing else in
   the suite catches the blanket wrap, which is precisely why the test earns its place.

**Non-blocking**

11. **The new bound covers four ops that have no inner deadline.** `timeout_ms` is declared
    per event, and `on_proxy` (`src/lib.rs:376-404`) serves `request`, `context`, `trace`,
    `usage` and `launch`; only `request` passes through the `timeout_secs` wrap at
    `service.rs:302-317`. Raising the event bound to 1 860 000 ms therefore means a wedged
    handler on the other four is reported after 31 minutes instead of 60 seconds, with no
    diagnosis. The practical exposure is narrow — their downstream calls are themselves
    bounded, since `router.ctg` and `memo.ctg` declare no `timeout_ms` and inherit the
    60 000 ms default — but the spec asserts "it stays a real backstop" without ever
    saying which callers it is a backstop for. Add the sentence.
12. **Verify block 3's stage greps are coupled to line breaking.** `grep -q "staged(\"$stage\""`
    requires the stage literal on the same line as the call. Wrapping the awaits as the
    Design writes them and then running `rustfmt` puts `"harness",` and `"cartridge call",`
    on their own lines, and block 3 exits 1 with `no stage wrapper for harness` on
    correct code; only `"provider route"` fits. I made it pass by hoisting each future
    into a local first (`let inject = (self.call)(…); Self::staged("harness", inject)`).
    Fixable inside the footprint and self-diagnosing, but it costs an implementer a cycle
    — say it in the Design, or match on `staged(` and the stage separately.
13. **Block 4's first needle is vacuous.** `"timeout_ms" in doc` is implied by
    `"event_timeout_ms" in doc`, so the gate really only requires the doc to name the
    host knob; a doc string that never mentions `events.proxy.timeout_ms` passes. It is
    not theatre — pinning the doc sentence is the only gateable part of a residual that
    the spec correctly shows cannot be closed — but check for `events.proxy.timeout_ms`
    if the gate is meant to hold the coupling.
14. **The Design's helper snippet is not `rustfmt`-clean as printed.** Copied verbatim it
    reflows to `call.await\n\t.map_err(…)`, so block 5 fails until the implementer runs
    `rustfmt`. Harmless, worth a word given block 5 is now a formatting gate.
15. **Cross-repo citations all check out.** `plan.rs:299-301` and `settings.json:19-25` at
    `cartridge.ctg@63ff234`, `lifecycle.ts:166` at `prd.ctg@3ef3426b`, and the worktree
    numbers the spec contrasts them with (`plan.rs:322-324`, `settings.json:26-31`, 18
    dirty paths) are all exact. So are the re-derived `proxy.ctg` numbers: `service.rs:302-317`,
    `:317`, `:661-665`, `:741`, `:743-747`, `:785-787`; `usage.rs:210`, `:219-260`, `:221-222`,
    `:248-250`; `notice.rs:27-28`, `:49`; `tests.rs:829`, `:832`, `:2110`, `:2497`, `:2527`;
    `cartridge.json:14`, `:15`, `:198`; baseline 55 passed. Round 1's findings 4 and 5 are
    closed. One nit: `cartridge.json:198` is the `timeout_secs` key, its `default` is `:200`.
16. **Footprint paths are still absolute** (round 1, finding 10). The engine resolves them
    (`planner.ts:8`) and every gate passes, so this is convention only — the sibling
    `mcp` child uses `"cartridge.json"`.
17. **The streaming route is wrapped but untested.** `staged("provider route", live.round(…))`
    also carries `UPSTREAM_STREAM_PREFIX` errors; the guard protects them by the same
    branch the third test exercises, so this is coverage symmetry, not a hole.

Disposition: keep — implement as written, folding in findings 11 and 12.
Validation: all commands run with cwd = a `git archive 0692c18` tree of `proxy.ctg`
placed at `prd.ctg/.cartridge/boards/proxy/.lanes/reviewer2-probe` (the real lane path,
so the `cartridge.ctg`/`memo.ctg` siblings resolve), `CARGO_TARGET_DIR` under the
reviewer's scratchpad. At HEAD: block 1 exit 1 (`events.proxy.timeout_ms is None`),
block 2 exit 1 in 7.4 s (`missing or failed: tests::deadline_message_names_the_bound`;
suite itself `55 passed; 0 failed`), block 3 exit 1 (`does not quote proxy.timeout_secs`),
block 4 exit 1 (`doc does not mention timeout_ms: 'How long one request may run.'`),
block 5 exit 1 (`tests.rs:699`). `cargo fmt --all --check` exit 1 (two files),
`cargo clippy --workspace --all-targets` exit 101 (`wire/tests.rs:29`),
`cargo clippy --lib` exit 0. After implementing the spec in that copy: blocks 1–5 all
exit 0, `58 passed; 0 failed`. Falsification: guard deleted → `57 passed; 1 failed`,
the failure being `tests::an_upstream_rejection_survives_the_stage_wrapper` at
`tests.rs:2796`. No `prd` command was run; the probe tree was deleted afterwards and
`git -C proxy.ctg status --porcelain` plus `rev-parse HEAD` are identical before and
after (same ten dirty paths, `0692c18`).
Reviewer identity: reviewer-2 (round 2).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: PASS.
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation on this revision; fold findings 11 and 12 into
the spec as a formatting-only clarification, or hand them to the implementer directly.
