# @router/a-deprecated-model-leaves-the-catalog-instead-of-being-retried review history

Plan: `@router/a-deprecated-model-leaves-the-catalog-instead-of-being-retried`,
`prd.ctg/.cartridge/boards/router/prds/a-deprecated-model-leaves-the-catalog-instead-of-being-retried/prd.md`.
Scope: executable leaf — a model the provider withdrew stops being re-asked by the routing loop.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: `specs/spec01.md` as of 2026-09-17 09:12, reviewed against
`router.ctg` at `7b2917a` with an empty `git status --porcelain` at both the
start and the end of the review. No dirty files.

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-deprecated-model-leaves-the-catalog-instead-of-being-retried/prd.md` — SHA-256 `fc03fb6f8a125f5d85bcb80451a15bc00b4d3a3dc702c7a968f0a117044117ca` |
| Specs | `specs/spec01.md` — SHA-256 `1a19896657aa97ad88d9f562db3f85abe5a3ff8053de6be2782a3d0e31e66448` |
| Material contracts/dependencies | `router.ctg` @ `7b2917a`; `src/health.rs` SHA-256 `626269d9…ed34cbc`; `src/proxy.rs` SHA-256 `13c5db5f…5aeda565`; `.cartridge/tests/unit/proxy/capabilities.rs` SHA-256 `081f0b3c…a5174b45`; `prd.ctg/.cartridge/templates/spec.md`; sibling PRD `@router/the-last-resort-pass-does-not-ask-a-model-the-provider-withdrew` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The gap is real and I measured it myself: 24 `auto` turns ask the withdrawn route 3 times at base, 1 with the guard. Scope is one guard in one function; the residue is split into its own PRD rather than smuggled in. −2: the PRD's Outcome sentence ("stops being ranked, stops being probed") still over-promises against the 5-calls-over-3-turns residue, and the PRD body carries no pointer to the follow-up that owns it. |
| Ownership and reuse | 19 | `retry_due` has exactly one caller (`src/proxy.rs:464`), so the guard sits at the root, not in a caller; no new file, both tests appended to the only test file in the footprint; `src/sync.rs` deliberately untouched with the rejection reasoned. −1: the spec's frontmatter footprint uses absolute paths where every other collected spec on this board uses repo-relative ones. |
| Dependencies and implementable slices | 20 | Base pinned to clean HEAD with both mid-analysis commits (`42bddc0`, `7b2917a`) and their concrete effect on this outcome stated; no dependency on unlanded work; one commit's worth of change; the out-of-footprint residue is a filed sibling PRD, not a widened footprint. |
| Observable acceptance and baseline evidence | 17 | Reproduced end to end in a scratch archive of `7b2917a`: 90 committed tests green, both new tests red at base with the exact stated failures (`left: 3 / right: 1`; `no override reaches a withdrawal`), 92/92 green with the guard. Both Verify blocks fail in the world they deny and pass with the change. Every cited line resolves. −3: two of block 2's pins already match at base, and the spec's "92/92" is stated as deterministic while a pre-existing test flakes. |
| Failure, recovery and compatibility | 19 | Lock ordering is argued and holds (the `data` read guard is released before `self.skips`); the skipped `skips` increment has no other consumer; the withdrawal survives `Health::load` including its `retry_at` clamp; no catalog or schema change, so nothing to roll back; the `--exact`-exits-0 trap is closed by the `... ok` grep, which I confirmed returns `test result: ok.` for a nonexistent name. −1: block 2's stray-file guard is repo-wide over `.cartridge/tests` in pass 2. |
| Reviewer total | 93 / 100 | Above threshold with no blocking finding. |

Findings and concrete revisions:

- **Non-blocking A — the PRD's Outcome over-promises against the shipped
  narrowing.** The spec scopes Acceptance line 5 to "while the turn has any
  other candidate", and that narrowing is honest: the residue is measured (5
  calls over 3 turns), its cause is cited (`src/proxy.rs:449-450,497`), it is
  out of footprint, and `@router/the-last-resort-pass-does-not-ask-a-model-the-provider-withdrew`
  exists and owns it. PRD Acceptance line 5 as literally worded ("a test asserts
  that a withdrawn route is not ranked as a candidate for `auto`") *can* be
  ticked by this spec alone — the last-resort pass reaches the route by draining
  the deferred queue, not by ranking it. The PRD's Outcome paragraph cannot:
  "stops being ranked, stops being probed" is flatly false for the last-resort
  turn. Recommendation: add the qualifier to PRD line 5 and one sentence to the
  Evidence naming the follow-up PRD, so a future reader of six ticked boxes does
  not conclude the route is never asked. Not blocking — the spec says all of
  this in its own words and the residue is owned.
- **Non-blocking B — two of block 2's pins are inert with respect to this
  change.** `grep -q 'has been deprecated' src/health.rs` and
  `grep -q 'Kind::Withdrawn && incident.state != "recovered"' src/health.rs`
  both match at `7b2917a` unmodified (the second on line 810, inside
  `availability()`). They are legitimate regression pins, but the second reads
  as pinning the new guard while the new guard's text is
  `|i| i.kind == Kind::Withdrawn && i.state != "recovered"` — a different
  string. Recommendation: keep them, and say in the prose that they pin the
  pre-existing early return rather than the change; the `sed`-range guard is the
  only one that discriminates, and it does (verified: base exits 1 with
  "retry_due does not exempt a withdrawn route", patched exits 0).
- **Non-blocking C — the whole-suite gate can fail on a pre-existing flake.**
  Block 1 ends with `cargo test --lib` gated on `test result: ok.`, and that
  block runs twice. `proxy::capability_tests::a_turn_waits_for_the_first_reopening_rather_than_failing_on_a_full_shelf`
  is load-sensitive: 1 red in 19 patched suite runs and 1 red in 6 base runs,
  20/20 green when run alone in either tree. It is not a regression from this
  change, but the spec states 92/92 as a fact. Recommendation: note it as a
  known flake so a spurious collect failure is re-run rather than diagnosed.
- **Non-blocking D — spec footprint paths are absolute.** `planner.feet()` does
  `path.resolve(root, p)`, which returns an absolute `p` unchanged, and every
  consumer converts back with `path.relative(code, …)`, so these resolve to the
  same paths and nothing breaks. It is a convention deviation from the four
  collected sibling specs on this board, which are repo-relative.
- **Non-blocking E — the stray-file guard is repo-wide.** `git ls-files --others
  --exclude-standard -- .cartridge/tests` in pass 2 fails on any untracked file
  under `.cartridge/tests`, including one left by another session working this
  checkout, and the message would blame this spec. The guard does fire
  (verified) — the analyst's stated uncertainty about it is resolved.

Disposition: keep. Proceed to implementation as specified.

Validation (all commands in
`/tmp/claude-501/-Users-feb-dev-cartridge/f7fcfe90-665f-4f0d-8e5d-1bfe54929eb3/scratchpad/router-review`,
`CARGO_TARGET_DIR` under it or at `$PWD/target/withdrawn-verify` inside the
scratch copies; `router.ctg` was never written):

| # | Command | cwd | Result |
| - | - | - | - |
| 1 | `git archive 7b2917a \| tar -x -C scratch/base`, copied to `scratch/patched` | `router.ctg` | 0; `src/health.rs` digest identical to the live tree |
| 2 | spec's `rust` block appended to both copies; spec's before/after snippet applied to `patched/src/health.rs` | scratch | anchor matched exactly once |
| 3 | `cargo test --lib` | `scratch/base` | 101 — 90 passed, 2 failed: `left: 3 right: 1`, `no override reaches a withdrawal` |
| 4 | `cargo test --lib` ×19 | `scratch/patched` | 18× `ok. 92 passed`; 1× 91/1 on the pre-existing flake |
| 5 | `cargo test --lib` ×6 | `scratch/base` | 5× 90/2; 1× 89/3, same flake — pre-existing |
| 6 | flaky test alone ×5 in each tree | both | 10/10 pass |
| 7 | Verify block 1 under `sh -eu`, cold target dir | `scratch/base` | 1 (fails in the denied world) |
| 8 | Verify block 1 under `sh -eu`, cold target dir | `scratch/patched` | 0 — 10.49 s real, well inside the 120 s limit; 503 MB into `target/withdrawn-verify`, which `router.ctg/.gitignore` ignores as `/target/` |
| 9 | Verify block 2 under `sh -eu` | `scratch/base` (git-init'd) | 1 — "retry_due does not exempt a withdrawn route" |
| 10 | Verify block 2 under `sh -eu` | `scratch/patched` (git-init'd) | 0 |
| 11 | `cargo test --lib -- --exact …a_name_that_does_not_exist` | `scratch/patched` | 0, `test result: ok. 0 passed … 92 filtered out` — confirms the `... ok` grep is the real gate |
| 12 | stray file under `.cartridge/tests`, `git ls-files --others` | `scratch/base` | guard fires |
| 13 | every load-bearing citation read with `sed -n Np` | `router.ctg` @ `7b2917a` | all correct — see below |

Citations re-derived at `7b2917a`, all confirmed: `src/health.rs:54` `classify`,
`:110` `fn withdrawn`, `:335` `fn deprecated_parameter`, `:389` `pub fn
availability` (range `389-415` ends exactly on the `json!({"adaptable"…})`),
`:652` `pub async fn retry_due`, `:725` `Recovery::degraded(t,
"model_withdrawn_by_provider")`, `:758` `retry_at: if withdrawn`, `:810` the
`Kind::Withdrawn` early return, `:976` `fn summarize`; `src/proxy.rs:437`
`deferred: Vec<(u64, Route)>`, `:449-450` `last_resort` / `sort_by_key`, `:464`
the `retry_due` override, `:497` `"health_overridden"`, `:1507`
`Kind::Withdrawn => Some("model_withdrawn_by_provider")`, `:1569` the `#[path]`
module; `cartridge.json:288-290` `limits.retry_every` default 10.

Reviewer identity: `reviewer-1 (round 1)`, independent agent; did not author the
spec, and edited no spec, PRD frontmatter or source file.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this round.
Result: **PASS**.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed to implementation of `spec01.md` as written. Findings A–E
are optional improvements, none of them gating; A is the only one that changes a
record rather than a comment.
