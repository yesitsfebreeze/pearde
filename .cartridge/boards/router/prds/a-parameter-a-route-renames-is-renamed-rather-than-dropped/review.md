# @router/a-parameter-a-route-renames-is-renamed-rather-than-dropped review history

Plan: `@router/a-parameter-a-route-renames-is-renamed-rather-than-dropped`,
`prd.ctg/.cartridge/boards/router/prds/a-parameter-a-route-renames-is-renamed-rather-than-dropped/prd.md`.
Scope: executable leaf — a route that refuses a parameter under one name but accepts
it under another receives it under the name it accepts, and the output limit in
particular survives the translation.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none. This is a distinct leaf (second of seven causes filed from
`@router/system/vision.md`), not a rename or split of
`@router/a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect`, whose three
rounds are its own. That sibling's findings are nevertheless held against this spec,
since it is the same board, the same file and the same landing route.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: `prd.md` + `specs/spec01.md` as published, with the PRD footprint
already narrowed by the coordinator from the bare `.cartridge/tests` to `src/health.rs`
and `.cartridge/tests/unit/proxy/capabilities.rs`. `router.ctg` at
`08d9463fea82e1484242ae446d0d17c3ad8cfc59`, unmoved for the whole round;
`prd.ctg` at `148302f6`.
Dirty in `router.ctg` throughout, untouched by this review: `.cartridge/docs/cost-latency.md`,
`.cartridge/tests/unit/{auth/tests.rs,catalog/capabilities.rs,settings/tests.rs,sync/tests.rs}`,
`cartridge.json`, `src/catalog.rs`, `src/known.json`, `src/service.rs`, `src/sync.rs`;
untracked `.cartridge/memos/system/vision.md`, `.cartridge/memos/type/system.md`.
Both footprint files are clean.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `a88a9f447912ea7ccad1cf2121a74b27204afbeb5f984fc6e6630fbce551349f` |
| Specs | `specs/spec01.md` — `4da14841fb7716c475f7cd43839c56994e44b0c522a0e71453448181e06eac20` |
| Material contracts/dependencies | `router.ctg/src/health.rs` `1515d16c…`; `router.ctg/src/proxy.rs` `c9155830…`; `router.ctg/.cartridge/tests/unit/proxy/capabilities.rs` `66d9fc59…`; `prd.ctg/src/lifecycle.ts` `177200f0…`; `prd.ctg/src/planner.ts` `fd60f4c7…` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The outcome is measured, not asserted: five routes shelved, each having spent four attempts learning the same OpenAI sentence, and the field at stake is the caller's output budget. One coherent slice, one owner. The spec's central claim — already implemented, zero production change, two pure `#[test]`s — is true, and I checked it line by line rather than taking it: `pub rename: BTreeMap<String, String>` `src/health.rs:141`, `next.rename.insert(from, to)` `:246`, `renamed_field` `:311-330`, `DROPPABLE: [&str; 12]` `:267-278` with no `max_tokens`, the `else if` at `:245-251`, `preserves` `:221-226`, the retry-same-route path `src/proxy.rs:580-587`, the waiver guard `src/proxy.rs:848-856`. The spec restates all six Acceptance lines rather than deleting the ones already met, which is the right call and its own stated standard. −2: the Landing section puts board-level collection policy inside a spec — load-bearing and correct here, as on the sibling, but still a plan carrying what the board carries. |
| Ownership and reuse | 19 | Correct owner, correct file, correct rung. Both tests go into the existing `.cartridge/tests/unit/proxy/capabilities.rs` beside the model they imitate; they call `Rules::propose` and `crate::health::cause` directly — no fixture, no network, no helper, no new module. The `DROPPABLE` privacy argument is sound and I verified it rather than accepted it: `const DROPPABLE` (`src/health.rs:267`) carries no `pub`, and the test module is `proxy::capability_tests` (`src/proxy.rs:1243-1245`), not a descendant of `health`, so `crate::health::DROPPABLE` is genuinely unreachable and pinning by behaviour is the only available proof. `src/health.rs` and `src/proxy.rs` are explicitly frozen with the exact abort (`prd.ctg/src/lifecycle.ts:134`) and an escalation instruction — the sibling's round-1 finding 3 is not repeated. −1: `src/health.rs` remains reserved in the PRD footprint although the spec freezes it; harmless while clean, but the same vestigial reservation the sibling carried for `src/protocol.rs`. |
| Dependencies and implementable slices | 20 | No dependencies, no lane, two tests, sub-millisecond, 12 s cold against a 120 s cap. I re-verified every engine citation rather than inheriting the sibling's verdict: `prd.ctg/src/lifecycle.ts:113` accepts `claimed` **or** `specced`; `:125` selects `tree = code` when no lane directory exists, so `:166`'s `git merge --ff-only` never runs and there is no abort-after-commit; `verify` runs at `:137` and again only under `tree !== code`, so the blocks run once, in `repo`, exactly as the Verify comment says. The coordinator's narrowing did what the analyst asked for: running the engine's own sweep — `git status --porcelain=v1 --untracked-files=all --` over `feet(prd)` (`prd.ctg/src/planner.ts:5-9`, the union of the PRD's two entries and the spec's one) — returns **nothing at all**, and `git ls-files --others --exclude-standard` over the same union is likewise empty. `feet(prd)` sweeps nothing foreign; the receipt will commit exactly the two new tests. Nothing to deduct. |
| Observable acceptance and baseline evidence | 14 | The author's three exit codes reproduce exactly (1 / 0 / 0, below). Block 1's `--exact` + `grep -q "^test .*$t \.\.\. ok$"` guard is real and fired on the base tree with `an_output_budget_is_renamed_rather_than_dropped did not run`, so it is not decorative; the module path `proxy::capability_tests` is right and `--exact` disambiguates it. Block 2 uses `if grep -qn …; then exit 1; fi`, not the inert `! grep` under `set -e`, and is honestly labelled a tripwire that passes at base rather than offered as evidence of the work. I did not stop at reading: I mutated `src/health.rs` five ways and re-ran block 1 each time (probes A–E below). Three of the four acceptance claims genuinely fail on a real regression — adding `max_tokens` to `DROPPABLE` fails test 1's third assertion, stripping the rename clauses from `preserves` fails the loopback test, and letting `renamed_field` accept `messages` fails test 2's last assertion. −6: the fourth does not. Acceptance line 6's `use ` conjunct — the literal "names both sides" guard at `src/health.rs:314-316` — is ungated; deleting it leaves block 1 at exit 0. Blocking finding 1. |
| Failure, recovery and compatibility | 13 | "Denied worlds" is the right shape and four of its six behavioural entries are true by measurement: skipping a test (observed, exit 1), `max_tokens` joining `DROPPABLE` (probe A, exit 1), `preserves` losing the rename (probe C, exit 1), `renamed_field` accepting `messages` (probe D, exit 1). The two-tree/no-lane and stranded-file worlds are stated with the right mechanism and the right commits (`fae0290`, `121913e`). `CARGO_TARGET_DIR` is pinned per the known hot-restart hazard and lands in gitignored `target/`, outside both footprints; scratch goes to `mktemp`. The scoped-out case (unquoted wording, replacement named first) is correctly scoped out — no observed refusal has that shape, no Acceptance line claims it, and the fallback is cause `unknown`, which is the router's own way of naming the next shape to learn. −7: two denied worlds are false by measurement (findings 1 and 2), one names the wrong failing assertion (finding 3), and the stranded-file rule is prose where the sibling review left a one-line gate for this very spec (finding 4). A false counterfactual in the section that carries this dimension's evidence is the defect this method exists to catch, and it is the second round on this board to carry one. |
| Reviewer total | 84 / 100 | The central claim is true and the landing route is now clean; one Acceptance line is gated only in the spec's own narrowed restatement, and the section that says otherwise is wrong twice. |

Findings and concrete revisions:

1. **BLOCKING — the PRD's Acceptance line 6 is not gated, and denied world 4 claims
   it is.** `renamed_field` refuses a one-sided message with two conjuncts
   (`src/health.rs:314-316`): the text must contain `not supported` **and** `use `.
   The spec's new test exercises neither conjunct directly — its three one-sided
   probes (`Unsupported parameter: 'temperature'`, `Unsupported parameter: 'max_tokens'`)
   carry a single quoted token, so they return `None` at the quoted-pair step
   (`src/health.rs:317-319`) whether or not the `use ` guard exists. I deleted the
   `use ` conjunct — `if !lower.contains("not supported") {` — and ran block 1 with
   both new tests present: **exit 0, all four `ran`** (probe E). The router in that
   state learns a bogus rename from any refusal that says "not supported" and happens
   to quote two name-shaped tokens, which is exactly what `prd.md`'s line 6 forbids:
   "A rename is only learned when the message names both sides." Denied world 4
   asserts the opposite — "Loosen `renamed_field` to fire on `not supported` alone …
   fails on its first and last assertions" — and its first clause is false; so is the
   sub-clause "the second because a one-sided refusal would no longer degrade to
   `unknown`" (`cause` still returns `unknown`, since `renamed_field` still fails at
   the quoted-pair step). Note also that `spec01.md`'s Acceptance line 6 silently
   narrows `prd.md`'s: it demands three named assertions rather than the property.
   `collect` ticks the boxes in both (`prd.ctg/src/lifecycle.ts:112`), so the PRD's
   general claim is credited on evidence that does not reach it.
   Recommendation, one assertion appended to
   `a_rename_is_learned_only_when_the_message_names_both_sides`:
   ```rust
   assert!(
       Rules::default()
           .propose(&body, "'max_tokens' is not supported with this model, see 'documentation'")
           .is_none(),
       "a refusal that never says what to use instead names only one side"
   );
   ```
   I confirmed both directions: it passes at `08d9463` and fails under probe E.
   Correct denied world 4 to name it, and either restore the spec's line 6 to the
   PRD's property or say in one line that it is deliberately narrowed and why.

2. Non-blocking — **denied world 3 is false.** "Move the rename branch after the drop
   branch in `propose`: the first assertion still passes … but `learned.drop.is_empty()`
   fails, because the same message would teach both rules at once." I swapped the two
   branches at `src/health.rs:245-251` (drop first, rename in the `else if`) and ran
   block 1 with both new tests: **exit 0, all four `ran`** (probe B). The reorder is
   invisible because `refused_field` cannot parse the two-sided message at all — it
   strips `Unsupported parameter: ` and `trim_matches(['\'', '"'])` leaves
   `max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.`,
   which is in no `DROPPABLE` entry (`src/health.rs:285-286,304`). The ordering at
   `:245-251` is therefore defensive rather than load-bearing for any observed refusal,
   which is fine — but the spec cites it as evidence for Acceptance line 2 and then
   claims a test catches its loss. Recommendation: delete denied world 3, or restate
   it honestly ("the ordering is defensive; no observed message reaches both branches,
   so no test can distinguish them").

3. Non-blocking — **denied world 5 names the wrong failing assertion.** It says
   dropping the rename from `preserves` makes
   `a_renamed_parameter_moves_its_value_instead_of_losing_it` fail on
   `response.status() == OK`. Observed (probe C): the test fails one assertion later,
   on `assert_eq!(first.len(), 2, "the refused route is retried once, adapted")` with
   `left: 1` — the status is still `OK`, because the turn falls through to the sibling
   route `last` and answers from there. The gate holds, and the admit half of
   Acceptance line 4 is genuinely gated even though it is gated indirectly; but the
   stated mechanism is wrong, and it matters here because the spec's own argument for
   accepting an indirect gate is that the failure is deterministic and predictable.
   Recommendation: one-line correction.

4. Non-blocking — **the stranded-file rule is the sibling's round-3 finding, repeated.**
   `../a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect/review.md` round 3,
   finding 1 recommended exactly one line — `test -z "$(git ls-files --others
   --exclude-standard -- .cartridge/tests)"` — and explicitly deferred it: "Carry it
   into the next spec on this board instead, where it costs nothing." This is that
   spec. It states the rule in bold, gives the reason, and names both repair commits,
   which is as clearly as prose can put it — but nothing fails if it is ignored, and
   the narrowed footprint is precisely what makes a new file there invisible to the
   sweep at `prd.ctg/src/lifecycle.ts:143-155` and to the post-receipt `ls-files
   --others` at `:174`. I confirmed the proposed gate passes at base (`git ls-files
   --others --exclude-standard -- .cartridge/tests` returns nothing). It stays
   non-blocking for the same reason the sibling gave — reaching it needs two deliberate
   acts against an explicit written instruction — but the deferral was to here, and
   declining it a second time should be a stated choice rather than a silence.
   Recommendation: add the line to block 2. It costs nothing and is already written.

Claims checked independently and confirmed sound, with no deduction:

- **Every per-line citation in the evidence table is accurate at `08d9463`.** Line 1:
  `src/health.rs:141`, `:246`, `:311-330`. Line 2: `DROPPABLE` has exactly 12 entries,
  `max_tokens` is absent, and the rename branch precedes the drop branch via `else if`
  at `:245-251`. Line 3: `src/proxy.rs:580-587` pushes the route back to the front of
  the queue in the same turn, and `a_renamed_parameter_moves_its_value_instead_of_losing_it`
  asserts `first.len() == 2`. Line 4: `src/proxy.rs:848-856` and `preserves`
  `src/health.rs:221-226`. Line 5: the committed loopback test uses the PRD's evidence
  string verbatim and asserts `max_completion_tokens == 100` with no `max_tokens`.
  Line 6: `src/health.rs:314-329`.
- **`DROPPABLE` really is unreachable from a test, and the behavioural pin really does
  close line 2.** Verified by privacy (no `pub`, test module is not a descendant of
  `health`) and by probe A: adding `max_tokens` to `DROPPABLE` fails test 1's third
  assertion with the message the spec predicts, exit 1.
- **The indirect gate on line 4's admit half is proof, not a gesture.** `Rules::apply`
  inserts both `from` and `to` into the changed set (`src/health.rs:186-190`), and
  `crate::requirements::present` (`src/requirements.rs:22-24`) is `Some` for
  `max_tokens` in `request()`, so the guard at `src/proxy.rs:848-856` is genuinely
  exercised. Probe C confirms it: with the rename clauses stripped from `preserves`,
  the loopback test fails. An indirect gate whose failure I can produce on demand is a
  gate.
- **The base-drift note is true.** `git diff 121913e 08d9463 -- src/health.rs` shows
  `preserves` gained exactly `!self.drop.contains(key)` and nothing else on this path.
- **The scoped-out case is correctly scoped out.** `renamed_field` takes the first two
  quoted tokens in order; a provider that omits quotes or names the replacement first
  is not adapted and degrades with cause `unknown`. No observed refusal has that shape,
  no Acceptance line claims it, and speculatively generalising the parser would be the
  wrong rung. It belongs in a later PRD, filed when a route actually sends one.
  (Tension worth naming: the spec scopes out "names the replacement first" while
  leaving "never says use at all" both unscoped and ungated — finding 1.)

Would the Verify blocks fail on a real regression? **Mostly yes, and I proved it rather
than argued it.** Five independent mutations of `src/health.rs`, each followed by block
1 in full: `max_tokens` into `DROPPABLE` → exit 1; `preserves` stripped of its rename
clauses → exit 1; `renamed_field` allowed to rename `messages` → exit 1. Those are
Acceptance lines 2, 4 and 6's conversation guard, and the blocks catch all three. The
two that pass are the branch reorder (probe B — not a regression for any observed
message, but the spec says it is caught) and the loss of the `use ` conjunct (probe E —
a real weakening of the PRD's line 6, and not caught). This is not a rubber stamp: the
spec builds genuine falsifiable gates for a change whose production code already
landed, and the one hole is a hole in one conjunct of one guard, closable by one
assertion.

Disposition: revise. The analysis is strong and the landing route is now verified clean;
one bounded revision — one assertion, two corrected denied worlds, optionally the free
`ls-files` line — should clear this comfortably.

Validation: cwd `/Users/feb/dev/cartridge/router.ctg` unless stated. Each Verify block
extracted verbatim from `specs/spec01.md` (lines 237-251 and 262-274) and run as
`sh -eu <file>`, matching the engine's `['sh','-eu','-c',block]` at
`prd.ctg/src/lifecycle.ts:44`. `CARGO_TARGET_DIR` exported to
`…/scratchpad/rename-review-target`, outside the checkout, so no `target/debug` or
`target/release` dylib moved and the live daemon was never restarted. The two proposed
tests were appended verbatim from the spec's `rust` fence (lines 61-114) for the probe
runs.

| Run | Tree | Exit | Observed |
| - | - | ---: | - |
| Block 1 | `08d9463`, base | **1** | `an_output_budget_is_renamed_rather_than_dropped did not run` |
| Block 2 | `08d9463`, base | **0** | every grep passes; `route.provider` has 0 matches in `src/health.rs` |
| Block 1 | base + the two new tests | **0** | all four `ran` |
| Probe A | + `max_tokens` prepended to `DROPPABLE` (13 entries) | **1** | test 1: `max_tokens stays out of DROPPABLE, so a one-sided refusal learns no drop` |
| Probe B | + drop branch before rename branch (`else if` swapped) | **0** | all four `ran` — denied world 3 falsified |
| Probe C | + `preserves` reduced to `!self.drop.contains(key) && PRESERVING.contains(&key)` | **1** | loopback test: `assertion left == right failed: the refused route is retried once, adapted`, `left: 1` |
| Probe D | + `renamed_field` name guard reduced to `!["model"]` | **1** | test 2: `rewriting the conversation is not a spelling difference` |
| Probe E | + `use ` conjunct deleted from `renamed_field` | **0** | all four `ran` — denied world 4 falsified, blocking finding 1 |
| Fix check | base + the two tests + finding 1's assertion | **0** | all four `ran` — the recommended assertion passes at `08d9463` |
| Fix check | probe E + the two tests + finding 1's assertion | **1** | test 2: `a refusal that never says what to use instead names only one side` |

- `git status --porcelain=v1 --untracked-files=all --` over `feet(prd)`
  (`src/health.rs`, `.cartridge/tests/unit/proxy/capabilities.rs`) — **no output**.
  `git ls-files --others --exclude-standard` over the same union — no output.
- `git ls-files --others --exclude-standard -- .cartridge/tests` — no output; the
  gate recommended in finding 4 passes at base.
- Author-reported exit codes were 1, 0, 0; observed 1, 0, 0.

Tree as found. `src/health.rs` was mutated and restored from a byte copy after each of
the six mutated runs (`md5 43ef55079d62d207380da942756b2efd` before and after every one);
`.cartridge/tests/unit/proxy/capabilities.rs` was appended to and restored
(`md5 4fa525ed65e4e54d24406123cf1c9475`, unchanged). `git status` in `router.ctg` is
identical to the round's opening list. No `prd` operation was run, nothing was
committed, no other session's dirty hunk was stashed or reverted, and `prd.md`
frontmatter was not touched. The only write is this record.

Reviewer identity: Claude Opus 5 (1M context), independent reviewer subagent; not the
author of `prd.md` or `specs/spec01.md`.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: (1) the PRD's Acceptance line 6 — "a rename is only
learned when the message names both sides" — is ungated for the `use ` conjunct at
`src/health.rs:314-316`; deleting that conjunct leaves block 1 at exit 0, and denied
world 4 claims the opposite.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision — add the one-sided-with-two-quoted-tokens assertion
to `a_rename_is_learned_only_when_the_message_names_both_sides`, correct denied worlds
3, 4 and 5, and decide the `ls-files` gate explicitly — then re-review against the same
base.

## Round 2 — 2026-09-17

Presented revision: `specs/spec01.md` revised against round 1's blocker and all three
non-blocking findings. `prd.md` unchanged (digest identical to round 1). `router.ctg`
at `08d9463fea82e1484242ae446d0d17c3ad8cfc59`, unmoved for the whole round;
`prd.ctg` at `148302f6`. Dirty in `router.ctg` throughout, untouched by this review and
identical to round 1's list: `.cartridge/docs/cost-latency.md`,
`.cartridge/tests/unit/{auth/tests.rs,catalog/capabilities.rs,settings/tests.rs,sync/tests.rs}`,
`cartridge.json`, `src/catalog.rs`, `src/known.json`, `src/service.rs`, `src/sync.rs`;
untracked `.cartridge/memos/system/vision.md`, `.cartridge/memos/type/system.md`.
Both footprint files clean.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `a88a9f447912ea7ccad1cf2121a74b27204afbeb5f984fc6e6630fbce551349f` (unchanged from round 1) |
| Specs | `specs/spec01.md` — `ee87dcf10edf9dc2c7528ccee89ef7cc74e2545bedfb08feeba20c2d030d505d` (was `4da14841…`) |
| Material contracts/dependencies | `router.ctg/src/health.rs` `1515d16c…`, `src/proxy.rs` `c9155830…`, `.cartridge/tests/unit/proxy/capabilities.rs` `66d9fc59…` — all three byte-identical to round 1; `prd.ctg/src/lifecycle.ts` `177200f0…`, `prd.ctg/src/planner.ts` `fd60f4c7…` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Value unchanged and still measured. Scope is better stated than in round 1: the `use `-only narrowing is now named as a knowing decision rather than a silent one, with the failing verbs enumerated ("try", "pass", "send", "switch to"), the cost bounded and visible (`router availability` shows the route as cause `unknown`), and that shelf entry named as the trigger for the follow-up PRD. That is the honest disposition, and the right one: all five shelved routes send OpenAI's one sentence, `prd.md`'s own Acceptance line 1 scopes to the `Use 'X' instead` clause by name, and widening the parser now would be guessing at a message nobody has sent. The spec also pins the narrowing as deliberate with the third probe, so "generalising" by deleting the guard fails rather than passes. −2: unchanged from round 1 — the Landing section still puts board-level collection policy inside a spec. Load-bearing and correct, but a plan carrying what the board carries. |
| Ownership and reuse | 19 | Unchanged and sound; the revision adds no mechanism, no file and no production change. The fourth probe reuses the same `Rules::propose` call shape as the other three rather than reaching for a fixture, and the new block-2 guard is one `git ls-files` invocation rather than a script. `src/health.rs` and `src/proxy.rs` remain explicitly frozen with the exact abort and escalation path. −1: unchanged from round 1 — `src/health.rs` is still reserved in the PRD footprint although the spec freezes it. Harmless (verified clean, sweeps nothing) and not the analyst's to change. |
| Dependencies and implementable slices | 20 | Unchanged and re-verified this round: the engine sweep — `git status --porcelain=v1 --untracked-files=all --` over `feet(prd)` — still returns nothing, so the receipt commits exactly the new tests. The no-lane route (`prd.ctg/src/lifecycle.ts:113`, `:125`, `:166`) is unchanged. The revision adds one assertion and one `git ls-files` guard; the slice is still two tests in one file, sub-millisecond, 12 s cold against a 120 s cap. Nothing to deduct. |
| Observable acceptance and baseline evidence | 19 | **Round-1's blocker is closed, and closed on the merits.** I re-ran the mutation rather than accepting the report: with the revised tests appended and `&& lower.contains("use ")` deleted from `src/health.rs:314`, block 1 exits **1**, panicking at `.cartridge/tests/unit/proxy/capabilities.rs:2193` with `two names the provider never joined with \`use\` are not a rename` — the exact message, the exact line, the exact exit the author reported. The author's diagnosis of why the first draft missed it is correct and is now written into the spec at lines 59-66: every single-token probe returns `None` at the quoted-pair step (`src/health.rs:317-319`) whether or not the guard exists, so only a message that *would* pair can distinguish them. All five reported exit codes reproduce exactly (table below). Spec Acceptance line 6 is restated as `prd.md`'s property rather than three narrower assertions, and I checked it does not overclaim in the other direction: the added conjunct ("says which one to use") is exactly what the third probe proves, and the remaining implementation conjuncts are consistent with the stated property rather than counterexamples to it — I confirmed the one that looked like a gap, deleting `lower.contains("not supported")` while keeping `use ` (block 1 exit 0), and a message reaching that path still names both sides and says which to use, so the property holds. −1: the inherent ceiling the sibling's round 3 also took — block 1 reads a test's result, never its body, so a probe that keeps its name while weakening its assertion passes. Four named behavioural probes per conjunct is the maximal gate available short of grepping test internals; I do not deduct further. |
| Failure, recovery and compatibility | 17 | Three of round 1's four findings are fixed and I verified each rather than read it. Denied world 4 (`use ` conjunct) is now true — observed exit 1 above. Denied world 5 is corrected to `assert_eq!(first.len(), 2)` with the reason stated, matching precisely what I measured in round 1 (`left: 1`, status still `200` through the fixture's sibling route), and the correction is **fully propagated**: the evidence table's line-4 row (spec:29) now names the two-call assertion and explicitly says the status assertion alone would not catch it, and spec Acceptance line 4 (spec:242-247) is rewritten to rest on the same assertion. Nothing in the record still leans on the status code for line 4. The untracked-file gate deferred to this spec by the sibling's round-3 finding 1 is in block 2 and works in both directions: exit 0 at base, exit 1 naming `.cartridge/tests/unit/proxy/stray_probe.rs` against a planted file, and the four *tracked* dirty files under `.cartridge/tests/unit/**` correctly do not trip it. Denied world 3's primary claim is now correct, and I had verified its mechanism in round 1. −3: its re-justification is wrong — see finding 1. |
| Reviewer total | 93 / 100 | The blocking finding is closed and verified by re-mutation; all three non-blocking findings are addressed, two of them exactly. One trailing justification remains unverified and wrong, against an assertion that does earn its place. |

Findings and concrete revisions:

1. Non-blocking — **denied world 3's re-justification names two mutations, and neither
   one fails the assertion it is offered to justify.** The entry's primary claim is now
   correct and I had already confirmed its mechanism: reordering the branches at
   `src/health.rs:245-251` changes no observed outcome, because `refused_field` cannot
   parse the two-sided message at all. The spec then keeps `learned.drop.is_empty()`
   and says it "earns its place against a different mutation — one that makes the two
   branches additive instead of exclusive, or that adds `max_tokens` to `DROPPABLE`
   *and* reorders". I ran both:
   - **Additive** (replace `} else if let Some(field) = refused_field(message) {` with
     `}` + `if let Some(field) = refused_field(message) {`, so both branches run):
     block 1 **exit 0**, all four `ran`. `refused_field` still returns `None` on the
     two-sided message, so the drop set is still empty and the assertion still passes.
   - **`DROPPABLE` + reorder**: block 1 **exit 1**, but at
     `.cartridge/tests/unit/proxy/capabilities.rs:2164` on
     `max_tokens stays out of DROPPABLE, so a one-sided refusal learns no drop` — the
     *third* assertion, which round 1 already showed fires on the `DROPPABLE` change
     alone without any reorder. `drop.is_empty()` passed. The reorder contributes
     nothing.
   The assertion does earn its place, just not against either named mutation. The
   mutation that fires it is one that makes a rename *also* record a drop of the old
   name — `next.drop.insert(from.clone());` beside `next.rename.insert(from, to);`,
   which is the realistic "a route that renames it clearly cannot take it" slip.
   Verified: block 1 **exit 1** at `capabilities.rs:2160` with
   `a renamed parameter is never also dropped`.
   Recommendation, one sentence: replace the two named mutations with that one. This
   is non-blocking because no Acceptance line is ungated by it — line 2's
   "renamed, never dropped" half is genuinely gated, as the probe above proves — and
   because the entry's load-bearing claim is now correct. But this is the second round
   in which this entry has carried a counterfactual that was written rather than run,
   and the same habit produced round 1's blocker. Worth running the next one before
   writing it.

Verified fixed since round 1:

- Round-1 blocker (Acceptance line 6's `use ` conjunct ungated) — **resolved**, by
  re-mutation, with the panic message, line number and exit code all matching the
  author's report.
- Round-1 finding 2 (denied world 3 false) — **resolved** in its primary claim; its
  trailing re-justification is finding 1 above.
- Round-1 finding 3 (denied world 5 named the wrong assertion) — **resolved**, and
  propagated completely into the evidence table and spec Acceptance line 4.
- Round-1 finding 4 (untracked-file gate deferred from the sibling's round 3) —
  **resolved**, gate added to block 2 and verified in both directions.
- The `use `-only narrowing disposition — honest, and correctly not a blocker. It
  names the recognised wording, the verbs that fail, the observable cost, and the
  trigger for the follow-up PRD, and it defends the guard with a probe so the
  narrowing cannot be undone by accident.

Disposition: keep. Proceed to implementation. Finding 1 is a one-sentence correction
that does not change a Verify block, an assertion or an Acceptance line; under review
method step 8 it can be made without staling this rating, or left to the next spec.

Validation: cwd `/Users/feb/dev/cartridge/router.ctg` unless stated. Both Verify blocks
extracted verbatim from `specs/spec01.md` (lines 288-300 and 326-342) and run as
`sh -eu <file>`, matching the engine's `['sh','-eu','-c',block]` at
`prd.ctg/src/lifecycle.ts:44`. Block 1 is byte-identical to round 1's (`diff` clean);
block 2 differs only by the six-line untracked-file guard. `CARGO_TARGET_DIR` exported
to `…/scratchpad/rename-review-target`, outside the checkout, so no `target/debug` or
`target/release` dylib moved and the live daemon was never restarted. The revised tests
were appended verbatim from the spec's `rust` fence (lines 77-144) for every probe run.

| Run | Tree | Exit | Observed |
| - | - | ---: | - |
| Block 1 | `08d9463`, base, without the new tests | **1** | `an_output_budget_is_renamed_rather_than_dropped did not run` |
| Block 1 | base + the two revised tests | **0** | all four `ran` |
| Block 1 | + `use ` conjunct deleted from `renamed_field` (`src/health.rs:314`) | **1** | `capabilities.rs:2193` — `two names the provider never joined with \`use\` are not a rename` |
| Block 2 | base | **0** | every grep passes; `route.provider` 0 matches; no untracked path under `.cartridge/tests` |
| Block 2 | base + untracked `.cartridge/tests/unit/proxy/stray_probe.rs` | **1** | `untracked test file outside the footprint, unbuildable from a clean checkout:` then the path |
| Block 1 | + branches made additive instead of exclusive | **0** | all four `ran` — finding 1 |
| Block 1 | + `max_tokens` in `DROPPABLE` *and* branches reordered | **1** | `capabilities.rs:2164`, the `DROPPABLE` pin — not `drop.is_empty()` — finding 1 |
| Block 1 | + a rename also records a drop of the old name | **1** | `capabilities.rs:2160` — `a renamed parameter is never also dropped` (the correction finding 1 recommends) |
| Block 1 | + `not supported` conjunct deleted, `use ` kept | **0** | checked and cleared: a message reaching that path still names both sides and says which to use, so spec Acceptance line 6's property is not violated |

- `git status --porcelain=v1 --untracked-files=all --` over `feet(prd)`
  (`src/health.rs`, `.cartridge/tests/unit/proxy/capabilities.rs`) — no output, unchanged
  from round 1.
- Author-reported exit codes were 1, 0, 1, 0, 1; observed 1, 0, 1, 0, 1 — all five
  reproduced, including the panic message and source line of the third.

Tree as found. `src/health.rs` was mutated and restored from a byte copy after each of
the six mutated runs (`md5 43ef55079d62d207380da942756b2efd` before and after every
one, `git diff` empty); `.cartridge/tests/unit/proxy/capabilities.rs` was appended to
and restored (`md5 4fa525ed65e4e54d24406123cf1c9475`); the planted
`.cartridge/tests/unit/proxy/stray_probe.rs` was deleted in the same command that
created it and `git status` over `.cartridge/tests` confirms no `unit/proxy` entry
remains. `git status` in `router.ctg` is identical to this round's opening list. No
`prd` operation was run, nothing was committed, no other session's dirty hunk was
stashed or reverted, and `prd.md` frontmatter was not touched. The only write is this
record.

Reviewer identity: Claude Opus 5 (1M context), independent reviewer subagent; same
reviewer as round 1, not the author of `prd.md` or `specs/spec01.md`.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS**.
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation. `prd specced` and dispatch an implementer; the
work is appending the spec's two verified tests to
`.cartridge/tests/unit/proxy/capabilities.rs` and nothing else. Finding 1's
one-sentence correction to denied world 3 is optional and does not stale this rating.
