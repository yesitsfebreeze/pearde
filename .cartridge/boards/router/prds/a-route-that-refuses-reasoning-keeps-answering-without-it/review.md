# @router/a-route-that-refuses-reasoning-keeps-answering-without-it review history

Plan: `@router/a-route-that-refuses-reasoning-keeps-answering-without-it`,
`prd.ctg/.cartridge/boards/router/prds/a-route-that-refuses-reasoning-keeps-answering-without-it/prd.md`.
Scope: a route that refuses a reasoning control answers the turn without it; executable leaf on the `router` board.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-19

Presented revision: superproject `801aa8e`; `router.ctg` base
`192300fd5003f94ef1492876cfb0fc6f22430185`, working tree dirty — 19 modified
files, of which `src/health.rs` (+211/−…) and `src/proxy.rs` together carry 279
uncommitted lines from other sessions. Every source reading below was taken with
`git show 192300f:<path>`, never from the working tree.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `4daeecacddaf40b05107ece64acd7a8583daa818d4c9a4fe83ce5b493c91e5d0` |
| Specs | `specs/spec01.md` — `4914e84a8726e54366bd53653ab56f8b9621e730a9077d358129f599ca3bb5b2` |
| Material contracts/dependencies | `router.ctg` @ `192300f` (`src/health.rs`, `src/proxy.rs`, `src/catalog.rs`, `src/frontier.rs`, `src/requirements.rs`, `.cartridge/tests/unit/proxy/capabilities.rs`); ancestor `a4ea6e9`; `prd.ctg/src/lifecycle.ts:63-111`; `router.ctg/.cartridge/memos/system/vision.md`; sibling review `prds/a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect/review.md:122` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | The remaining value is real and correctly re-scoped: three of the PRD's five boxes are already code-complete from `a4ea6e9` (verified: `git merge-base --is-ancestor a4ea6e9 192300f` exit 0; `const REASONING` at `health.rs:263`; `DROPPABLE` at 267 carrying all three spellings; the `Unrecognized request argument supplied: ` prefix at 287; the `REASONING` cascade at 173-183), so the spec is right to be test-weighted. The durability finding is a genuine user-visible defect discovered by reading, not asserted. −3: the value now rests almost entirely on tests over landed code, and the spec leaves its central reading of the Outcome as an open hedge rather than a decision (see finding 6). |
| Ownership and reuse | 16 | Right owner; extends the one adaptation mechanism rather than branching on a provider (vision law 1 and 5); copies `a_refused_tool_schema_is_rewritten_and_the_same_route_answers` (`capabilities.rs:1823`) instead of inventing a harness; extends the existing fixture. −4: the proposed `record_rules` call contradicts the rationale comment sitting on the very line it edits — `src/proxy.rs:444-447`, "Held here rather than in the health store because no probe has verified it yet" — and the vision's "verified by a structural probe before it is trusted". The spec neither cites nor retires that comment, and nothing anywhere invalidates a durably recorded rule (`data.rules` has exactly one writer, `health.rs:971`, and no remover). |
| Dependencies and implementable slices | 12 | Base-sha discipline is exemplary: every anchor re-derived from `git show`, symbols named ahead of numbers, ancestry proven. −8: the test recipe — the spec's whole remaining deliverable — is wrong in three places that each stop the prescribed tests from passing (finding 1). "The fixture needs one extension" understates it by two. |
| Observable acceptance and baseline evidence | 13 | The gate is an executed `test` block naming five tests; no `grep`/count gate stands in for a behavioural assertion; nothing is inert under `sh -eu -c` (no `!`-negated guard, no `&&`-chained test, no `${VAR:?}`); `${CARGO_TARGET_DIR:-…}` is `set -u`-safe; paths are relative to the repo root; no `cd`; the target dir is isolated, gitignored (`/target/`) and outside the footprint, so the live dylib is untouched. The anti-vacuity rule — assert `calls[0].1` carried `reasoning_effort` before asserting `calls[1].1` does not — is exactly the assertion that keeps these four tests from being self-satisfying. −7: the stated ceiling is unmeasured and is contradicted by a measurement already recorded on this board (finding 2), and the mutant run — the only gate technique that has survived here — is relegated to an Acceptance box on that unmeasured claim. |
| Failure, recovery and compatibility | 14 | The waiver/adaptation distinction is preserved and pinned by a test rather than quietly inverted; the same-turn retry cannot loop (`propose` returns `None` once there is nothing new to learn, `proxy.rs:619`); `record_rules`' equality guard makes the write idempotent, so a long run persists once. −6: a rule recorded on this path is durable and unprobed with no invalidation (finding 3); the recording point is described as "the first statement after the response is known good", which is untrue on the streaming path — `stream_response` is spawned at `proxy.rs:559` and the stream can still fail into `health.fail` at `proxy.rs:1352` (finding 4); and the spec carries no denied-worlds/counterfactual section, which sibling specs on this board carry and prior rounds scored on. |
| Reviewer total | 72 / 100 | Two blocking findings. |

### Findings and concrete revisions

**1. BLOCKING — the fixture prescription cannot produce the prescribed tests.**
The spec says "The fixture needs one extension" and names only the `reasoning`
cap plus an `auto` selector. Three things are wrong or missing, each of which
stops three of the four proxy tests dead:

- *The effort is never injected, because the fixture's policy is empty.*
  `fixture()` builds the catalog with `Catalog::new(models, providers)`
  (`capabilities.rs:145`), and `Catalog::new` sets `policy:
  crate::frontier::Policy::default()` (`catalog.rs:438`). `Policy` is a bare
  `frontiers: BTreeMap<String, Vec<Entry>>` (`frontier.rs:22-24`), so
  `board(task)` returns `None` and `policy.entry(task, route)` returns `None`
  for every task — and `proxy.rs:1006-1017` injects nothing when the effort is
  `None`. The implementer must seed
  `fixture.proxy.catalog.write().await.policy.frontiers` with an `Entry` whose
  `model` matches the route (`rank` reads `route.alias`, `route.id`,
  `route.model` — `frontier.rs:109`) and whose `effort` is `Some(_)`. The spec
  does not say this; the analyst's own note does, and it did not reach the
  document the implementer reads.
- *The task key is `vision`, not `text` or `reasoning`.* `request()`
  (`capabilities.rs:163`) sends an `image_url` content part, and
  `frontier::task` returns `"vision"` on the image modality before it reaches
  the tools or reasoning branches (`frontier.rs:215-224`). A frontier seeded
  under any other key is never consulted.
- *The selector and the `["last","last"]` assertion conflict.* The injection
  gate requires `body["model"]` to be `auto` or `auto:…` (`proxy.rs:998-1004`),
  while the reference test the spec says to copy gets `["last","last"]` by
  pinning `body["model"]="fixture@last"` **and** `cartridge_strict=true`
  (`capabilities.rs:1841-1842`). Those cannot be combined: with base `auto` the
  canonical is `"auto"`, no route has `alias == "auto"`, and `preferred`
  (`catalog.rs:650-652`) is therefore false for every route, so a strict
  `auto@last` turn returns zero candidates and never calls upstream. The form
  that works is `auto@last` **without** `cartridge_strict` — the pin sort at
  `catalog.rs:512-514` puts the `last` routes first, so the first attempt is
  `last` and the same-turn retry gives `["last","last"]`. The spec must say so;
  as written it points the implementer at a 404 with an empty `calls`.

None of the three fails silently, which is why this is a correctness finding
about the spec rather than about the tests it would produce. It is blocking
because the tests are this PRD's entire remaining deliverable and the spec's
instructions for building them are wrong in three places.

**2. BLOCKING — the stated ceiling is unmeasured and contradicted by this
board's own measurement.** The spec's Verify section asserts that a `$TMPDIR`
copy "compiles `mlua`, `axum` and `reqwest` from a cold fingerprint set and will
not finish inside 120 s", and moves the mutant proof out of the gate on that
basis. No cargo command was run to establish it — the analyst's note says so
explicitly. The sibling review at
`prds/a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect/review.md:122-123`
records the opposite, measured: "Cold build into a fresh `CARGO_TARGET_DIR`
outside the repository: 10 s, exit 0", repeated at line 150. The claim is also
self-defeating: `prd.ctg/src/lifecycle.ts:93,111` gives each block 120 s and
runs it first with cwd = the lane, a fresh worktree whose
`$PWD/target/reasoning-verify` is exactly as cold as a `$TMPDIR` copy. If the
ceiling holds, this spec's own pass 1 times out; if pass 1 passes, the mutant
fits. One measurement settles it. This matters because the mutant run is the
technique that finally held on this board after every text and count gate was
beaten, and it is being given up on an assumption.
Resolution: measure a cold `cargo test -p router --lib` into a fresh target dir
and either carry the mutant as a second `sh` block or keep the Acceptance box
with the measurement quoted beside it.

**3. Durable rule with no probe and no invalidation.** `data.rules` is written
in exactly one place today, `Health::finish_recovery` (`health.rs:971`), which
runs only behind a `Permit` over an open incident, and nothing anywhere removes
an entry. The spec adds a second, unprobed writer and does not say what retires
the rule when the provider later accepts the field. The route having actually
answered is stronger evidence than a structural probe, so this is a paragraph
the spec owes, not a design error — but it must be written, and the now-false
comment at `proxy.rs:444-447` must go with it.

**4. "Known good" is inaccurate on the streaming path.** `decision.selected` at
`proxy.rs:586` is reached with `id` bound at 555 (`route.id.clone()` — the
lookup key in the proposed snippet is correct) but, when `streaming`, the
response at that point is a spawned `stream_response` (`proxy.rs:559`) that can
still fail into `health.fail` at `proxy.rs:1352`. Recording the shape rule there
is defensible — the rule concerns whether the request shape was accepted, which
the upstream 200 already settles — but the spec's justification is wrong and
should say that instead.

**5. Two blocks disagree about an inherited target dir.** Block 1 honours an
inherited `CARGO_TARGET_DIR` via `:-`; the `test` block hardcodes
`env CARGO_TARGET_DIR=target/reasoning-verify`. If the collector's environment
already sets one, the two blocks build in different trees and the claimed
incrementality is lost. Make the `test` block use the same default form.
Related, minor: `cargo test -p router --lib` runs the whole lib suite (52
`#[tokio::test]`/`#[test]` in `capabilities.rs` alone, plus eight other test
files) inside one 120 s block; every other cargo gate on this board filters.
Keep the unfiltered run only if the measurement in finding 2 shows it fits.

**6. The boundary should be encoded as a decision, not a hedge.** Ruling below;
the spec's reading is right, and the paragraph should state it as settled with
its warrant rather than offering to invert the fourth test.

### Rulings the coordinator asked for

**(a) The widening to `src/proxy.rs` is JUSTIFIED.** Every load-bearing claim
checks out at `192300f`: `let mut learned: BTreeMap<String, Rules>` is a turn
local declared inside `execute`'s candidate loop (`proxy.rs:447`, read back at
531, written at 625); the successful same-turn retry `continue`s before
`proxy.health.fail(...)` (`proxy.rs:619-627`), so no incident opens; and
`data.rules` has exactly one writer, `Health::finish_recovery`
(`health.rs:971`), which returns early unless `data.incidents.get_mut(route)`
yields an incident with a matching `Permit`. A route that recovers in the same
turn therefore starts every later turn from `Rules::default()` and pays one
refused upstream call per turn forever — the literal wording of Acceptance box
3. There is no seam inside `health.rs`: `Health::success` is
`(&self, route: &str)` (`health.rs:797`) and carries no rules, `Rules::propose`
is `&self` on `Rules` with no handle on `Health`, and the only other place the
rules are in scope on a success is `attempt`/`collect_response` — both in
`proxy.rs`. Even widening `success`'s signature would require editing
`proxy.rs`'s three call sites (1283, 1352, 1464). The widening is necessary, and
four lines is the minimum shape of it.

**(b) The "most of this already landed" claim is TRUE, not overstated.**
`a4ea6e9` is an ancestor of the base (`git merge-base --is-ancestor`, exit 0).
At `192300f`: `refused_field` strips `Unrecognized request argument supplied: `
and trims `'"` and `.` (`health.rs:287-288`); `const REASONING: [&str; 3]` is at
263; `DROPPABLE` at 267 carries `thinking`, `reasoning` and `reasoning_effort`;
the cascade in `Rules::apply` at 173-183 removes all three plus
`output_config.effort` and reports `output_config` in `changed`; `propose`'s
`|| REASONING.contains(&field)` disjunct is at 248; `effort_refused` at 503. The
spec is right to be test-weighted, and right that the PRD's evidence predates
the commit that fixed most of it.

**(c) The Verify blocks are mechanically sound; the ceiling is not
established.** Checked against `prd.ctg/src/lifecycle.ts:63-111`: `sh -eu -c`,
120 s per block, two passes. No grep or count gate stands in for a behavioural
assertion — the gate is a `test` block naming five tests the runner must report
passed. Nothing is inert: there is no `! grep`, no `test -n "$X" && test …`, no
`${VAR:?}`; `${CARGO_TARGET_DIR:-$PWD/…}` is exempt from `set -u`. Paths are
relative to the repo root and no block `cd`s to an absolute checkout. Both cargo
commands are pinned to an isolated target dir that is gitignored (`/target/`),
outside the footprint (`src/health.rs`, `src/proxy.rs`, `.cartridge/tests`), and
away from the `target/debug` and `target/release` dylibs the live host watches.
Findings 2 and 5 are the exceptions. On the ceiling specifically: not
established, contradicted by a measurement on this board, and self-defeating if
true. An Acceptance box is an adequate substitute only once the measurement
shows the block cannot carry it.

**(d) The boundary: the spec's reading is CORRECT and should be encoded, not
left open.** A reasoning control the caller supplied stays a waiver. Three
independent reasons. The vision's first law is explicit that an adaptation which
cannot preserve meaning "is a refusal, not a silent downgrade", and the vision
is "the authority on intent". The waiver/adaptation distinction is the whole
subject of `a4ea6e9`, the sibling PRD that landed days after this PRD's evidence
was measured; inverting it here would undo a collected outcome from inside a
test file. And the mechanism already encodes the line exactly where the PRD's
evidence puts it: `requirements::present(body, &key)` (`requirements.rs:22`)
reads the *caller's* body, so a router-injected field withdraws cleanly at
`proxy.rs:1052-1060` while a caller-supplied one is refused. The PRD's own
evidence says "The value is also not the caller's". The spec should state this
as decided, cite the vision's first law, and drop the offer to invert
`a_reasoning_control_the_caller_asked_for_is_still_a_waiver`. The PRD's Outcome
sentence deserves a one-clause scope note in the same revision so the next
reader does not re-open it.

Disposition: revise. The analysis is strong and the two structural questions the
analyst raised were raised correctly and resolve in his favour; the failure is in
the test recipe and in one unmeasured claim, and one round should clear both.
Validation: cwd `/Users/feb/dev/cartridge` and
`/Users/feb/dev/cartridge/router.ctg`. All reads at the base via
`git show 192300f:<path>` (`src/health.rs`, `src/proxy.rs`, `src/catalog.rs`,
`src/frontier.rs`, `.cartridge/tests/unit/proxy/capabilities.rs`, `.gitignore`,
`Cargo.toml`); `git merge-base --is-ancestor a4ea6e9 192300f` exit 0;
`git rev-parse HEAD` = `192300fd5003…`; `git status --porcelain | wc -l` = 19;
`shasum -a 256` on `prd.md` and `specs/spec01.md`; `grep -n` on
`prd.ctg/src/lifecycle.ts` for the engine facts. No cargo command was run: the
checkout is shared and a build hot-restarts the live cartridge. No file in
`router.ctg`, `prd.md` or `specs/spec01.md` was modified; the only writes are
this record and `.state/loop/a-route-that-refuses-reasoning/reviewer-1.md`.
Reviewer identity: Claude Opus 5 (1M context), independent reviewer subagent;
not the author of `prd.md` or `specs/spec01.md`.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: (1) the fixture prescription cannot produce the
prescribed tests — the policy is never seeded so no effort is injected, the task
key is `vision`, and `auto@…` cannot carry `cartridge_strict`; (2) the 120 s
ceiling on the mutant run is unmeasured and is contradicted by the tool-schema
review's measured cold build of 10 s, and would break this spec's own lane pass
if true.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision of `specs/spec01.md` addressing findings 1-6,
then round 2.

## Round 2 — 2026-09-19

Presented revision: superproject `c84b3a4126224af211de08f2e45fe06e705a5e99`;
`router.ctg` still at base `192300fd5003f94ef1492876cfb0fc6f22430185`, working
tree still dirty — 19 modified files, unchanged from round 1. Every source
reading below was re-taken with `git show 192300f:<path>`, and the base-sha
build/mutant claims were independently reproduced in a throwaway tree outside
the repository, never in `router.ctg`'s working copy.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `241015ade80eeec2a005e2c41f53318da7829b6ac65e3e2cd21c37c6f63e12c1` |
| Specs | `specs/spec01.md` — `b0e5ffc3df9ab59efd6fe9c17cfe33f9979fc4f795cfc4a712cb5e09aabb3698` |
| Material contracts/dependencies | `router.ctg` @ `192300f` (`src/health.rs`, `src/proxy.rs`, `src/catalog.rs`, `src/frontier.rs`, `src/requirements.rs`, `.cartridge/tests/unit/proxy/capabilities.rs`); a throwaway `git archive 192300f` tree at `/tmp/reasoning-review-*` with its own `CARGO_TARGET_DIR`; a separate mutant copy at `${TMPDIR}/reasoning-mutant-review-*` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The Outcome hedge round 1 asked to close is closed: `git diff HEAD -- prd.md` shows exactly the one-clause scope note ruled for — "where the control is one the router itself added from policy; a control the caller supplied is a waiver and still refuses the route" — with no other content change beyond a pre-round-1 claim/state pair. The spec's own discovery that `a_refused_thinking_request_loses_every_spelling_of_reasoning` (`capabilities.rs:1490`, verified present, verified to already assert the ollama `changed == {"reasoning_effort"}` case and the OpenAI wording) already gates the PRD's first and second Acceptance boxes is real and honestly stated, not claimed as new work. −1: the PRD's own Acceptance list is not annotated to say two of its five boxes are already gated elsewhere; only the spec records it. |
| Ownership and reuse | 19 | The now-false comment at `src/proxy.rs:444-447` is quoted verbatim and corrected in the same edit (verified the base text matches the spec's quote exactly); the fixture recipe is lifted from an already-passing test, `a_policy_reload_during_fallback_does_not_change_the_attributed_snapshot` (`capabilities.rs:510-545`, verified present, verified it computes `task` dynamically and seeds the identical `Entry` shape), instead of inventing one; a near-duplicate test is withdrawn rather than added beside line 1490. −1: `record_rules`'s comment claims a same-turn retry is "stronger evidence" than `finish_recovery`'s structural probe — a reasoned paragraph, not a measured one, though the workflow permits stating such a ceiling rather than engineering around it. |
| Dependencies and implementable slices | 19 | I re-derived the routing trace independently at the base sha and it holds: `Catalog::candidates` (`src/catalog.rs:457-514`) with `body["model"]="auto"`, no pin, gives filtered order `[first, last]` (incompatible dropped by `requirements::rejection`); `rank_by_policy` (`catalog.rs:588-607`) cannot reorder same-alias routes because `Board::entry` scores them identically; the retry loop (`src/proxy.rs:447, 528-625`) pops `first` (503, `propose` returns `None`, no adaptation), then `last` (effort injected per `proxy.rs:998-1017`, refused, `propose` returns a drop rule, same route pushed to the front and retried at once per `proxy.rs:619-625`). That reproduces the claimed `["first","last","last"]` sequence and is consistent with the existing anchor test `actual_failover_skips_incompatible_routes_and_preserves_required_fields` (`capabilities.rs:169`, confirmed `["first","last"]` for the non-`auto` case built from the same ordering code). All three of round 1's concrete objections — unseeded policy, wrong task key, `auto@last`+`cartridge_strict` incompatibility — are closed by a different, verified approach rather than patched over. −1: the 3b test bodies are still names and descriptions, not code; normal at spec stage, but real execution risk remains for the implementer. |
| Observable acceptance and baseline evidence | 10 | The measured-ceiling claim holds in substance: rebuilt the base sha in a throwaway `git archive` tree with an isolated `CARGO_TARGET_DIR`, cold, both ways — 25.4 s wall with `CARTRIDGE_YOLO=1` ambient, 26.3 s wall under `env -u CARTRIDGE_YOLO`, both exit 0, both "93 passed; 0 failed" — comfortably inside the 120 s ceiling either way, so the mutant correctly lives in a Verify block now rather than an Acceptance box; this closes round 1's finding 2 on substance, though the specific seconds quoted (17 s/18 s) were not reproduced (mine ran ~50% longer on the same measurement design — a discrepancy worth noting, not blocking, since even the slower number clears the ceiling with room to spare). I also built the mutant (`sed` on `const REASONING`) against the base sha and confirmed `cmp` correctly detects a real change and that `a_refused_thinking_request_loses_every_spelling_of_reasoning` and `a_route_that_will_not_reason_and_use_tools_together_drops_the_effort` both fail under it on their own, exactly as claimed. **Blocking:** the "tightened" mutant guard does not verify what it claims to. Its final check, `if grep -q '<turn-driving test name>' "$mutant/out.log"; then :; else exit 1; fi`, only tests whether that test's name appears anywhere in the captured log — not whether that test is reported `FAILED`. I reproduced this with a real two-test `cargo test` run: one test named identically to the PRD's turn-driving test made to **pass**, one unrelated test made to fail. The command exited 101 (satisfying the outer "did the suite fail" check) and `grep -q` on the passing target test's own name still matched, because cargo's default text output prints every test's name followed by `... ok` or `... FAILED` and the guard does not require `FAILED` adjacency. So a future implementation whose turn-driving test does **not** die under this mutant would still pass this block, as long as anything else among the other ~90 tests failed for any reason. This is exactly the "grep/count standing in for a behavioural assertion" pattern this board's settled facts record as beaten every previous time, reappearing inside an otherwise well-built mutant harness. A one-line fix (anchor on the `FAILED` line or the `failures:` summary list, not the whole log) would close it; as written it does not hold. |
| Failure, recovery and compatibility | 18 | The streaming justification is now accurate: verified `src/proxy.rs:573-583` is the non-streaming failure check immediately before `decision.selected(selected)` at 586, that `stream_response` is spawned at 559, and that it can still call `proxy.health.fail` at `src/proxy.rs:1352-1358` on a later failure — matching the corrected claim that 586 records "the request shape was accepted" rather than "the response is known good." The staleness/no-invalidation gap is now a named ceiling with a warrant (a like ceiling already exists on `finish_recovery`'s own writes) instead of being silently absent. The caller-waiver boundary is recorded as decided, citing the vision's first law, `a4ea6e9`'s provenance, and `requirements::present` (`src/requirements.rs:21-23`, verified) exactly as round 1 ruled, and the offer to invert the fourth proxy test is gone. −2: round 1's non-blocking note that sibling specs on this board carry a denied-worlds/counterfactual section is still not answered; "Decided, not open" substitutes for part of it but does not enumerate what this spec forecloses. |
| Reviewer total | 85 / 100 | One blocking finding. |

### Findings and concrete revisions

**1. BLOCKING — the tightened mutant guard passes on an unrelated failure,
not on this PRD's test dying.** `specs/spec01.md`, the mutant `sh` block's
final `if`:

```sh
if grep -q 'a_route_that_refuses_the_injected_effort_answers_without_it' "$mutant/out.log"; then
  :
else
  echo "the suite failed under the mutant, but the turn-driving test did not:"
  exit 1
fi
```

tests only whether that string is present anywhere in the log, and `cargo
test`'s plain-text output prints every test's name regardless of outcome
(`test <path> ... ok` or `... FAILED`). Reproduced directly: a two-test crate
where the target-named test explicitly **passes** and an unrelated test
fails gives exit 101 from `cargo test` (satisfying the block's outer check)
and `grep -q` on the passing test's own name still matches. The claim "the
guard is now said to require the failure list to name this PRD's own
turn-driving test" is not what is implemented — it requires the *log*, not
the *failure list*, to name it. Fix: anchor on the line reporting failure,
e.g. `grep -qE '^test .*a_route_that_refuses_the_injected_effort_answers_without_it \.\.\. FAILED$'`
against the log, or grep only the text following the `failures:` summary
header, which cargo prints as a clean one-name-per-line list of exactly the
tests that failed.

None of round 1's two blocking findings survive this revision unresolved —
see rulings below — but this is a new one, found by executing the block
rather than by reading it, in the same dimension and for the same reason
round 1's finding 2 existed: an unexecuted gate design is not evidence the
gate holds.

### Round 1 findings, re-checked

**Round 1 finding 1 (fixture prescription impossible): CLOSED.** Verified
independently, not merely accepted. `body["model"]="auto"` with no pin avoids
the `auto@last` dead end (`src/proxy.rs:998-1004`'s raw-string test excludes
`"auto@last"`, confirmed by reading the literal condition at the base); the
task key is now computed with `crate::frontier::task(...)` rather than
hardcoded, which is correct regardless of which modality it resolves to,
because the same computation runs again inside `attempt`'s injection check
(`proxy.rs:998-1017`) against the same body; and the fixture-seeding shape is
copied from a test that already exists and already passes
(`capabilities.rs:510-545`). I traced the candidate ordering by hand through
`Catalog::candidates`/`rank_by_policy`/`rank_by_canonical`
(`src/catalog.rs:457-514, 588-607, 679-687`) and confirm the claimed call
sequence `["first","last","last"]`.

**Round 1 finding 2 (ceiling unmeasured/contradicted): CLOSED in substance.**
Independently rebuilt the base sha cold, isolated target dir, both
`CARTRIDGE_YOLO` settings: 25.4 s and 26.3 s wall, both "93 passed; 0 failed."
The specific numbers the spec quotes (17 s/18 s) are about 50% lower than what
I measured on what should be the same machine and design; I cannot explain
the gap and record it rather than guess, but it does not change the
conclusion — both readings clear the 120 s ceiling with room to spare, so the
mutant belongs in a Verify block, which is where this revision puts it. Not
blocking.

### Rulings carried forward, not re-litigated

Per the brief, round 1's rulings (a) footprint widening to `src/proxy.rs`
justified, (b) "most of this already landed" true, (c) Verify blocks
mechanically sound apart from the (now closed) ceiling claim, (d) a
caller-supplied reasoning control stays a waiver, all stand; this revision's
changes to the sections those rulings covered are consistent with them, not
contrary to them, on inspection.

Disposition: revise. One narrowly-scoped fix — make the mutant guard's final
check require `FAILED` adjacency (or read only cargo's `failures:` summary
list) instead of a whole-log substring match — should be a small, mechanical
change to one `sh` block and should not cost a full round of rediscovery.
Validation: cwd `/Users/feb/dev/cartridge` and `/Users/feb/dev/cartridge/router.ctg`
for reads; a throwaway tree at `/tmp/reasoning-review-*` (from
`git archive 192300fd5003f94ef1492876cfb0fc6f22430185`) and a mutant copy at
`${TMPDIR}/reasoning-mutant-review-*` for builds, both outside the repository
with their own `CARGO_TARGET_DIR`, never in `router.ctg`'s shared checkout.
Commands: `cargo test -p router --lib` cold with and without `CARTRIDGE_YOLO=1`
(93 passed / 0 failed both times, 25.4 s and 26.3 s wall); the same after
applying the spec's `sed` mutation (91 passed / 2 failed, the two tests the
spec names, 40.4 s wall); a standalone `minitest` crate built to reproduce the
guard's `grep -q` behavior on a passing-vs-failing pair of test names (exit
101, false match confirmed). `shasum -a 256` on `prd.md` and `specs/spec01.md`;
`git diff HEAD -- prd.md` to confirm the only content change is the one-clause
Outcome scope note. No file in `router.ctg`, `prd.md`, or `specs/spec01.md`
was modified; the only writes are this record and
`.state/loop/a-route-that-refuses-reasoning/reviewer-2.md`.
Reviewer identity: Claude (independent reviewer subagent for this round; not
the author of `prd.md` or `specs/spec01.md`, not the round 1 reviewer).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: (1) the mutant block's final check passes when
the turn-driving test merely *ran* (pass or fail) rather than when it *died*,
because `grep -q` on the whole log matches a passing test's own `... ok` line
just as readily as a `FAILED` line; demonstrated by direct reproduction, not
inferred.
Rounds used / remaining: 2 / 3.
Next action: one bounded revision of the mutant block's final check in
`specs/spec01.md`, then round 3.

## Round 3 — 2026-09-19

Presented revision: superproject `b34e8ae714d1188da9e4ea4a0c5b95513404c3f8`;
`router.ctg` now at `ca11f6b90da09b661828d8e5002e1740c79b6a51` (working tree
clean, 0 modified files — the 19-file drift seen in rounds 1-2 has since landed
via an unrelated commit, "Read unavailable and entitlement refusals as
operator-side and drop the Copilot token exchange"); `prd.ctg` at
`e56330ed16b02675c7d91b2f73b4e41543127d47`. Reads were taken from the working
tree (clean) and cross-checked against `192300fd5003f94ef1492876cfb0fc6f22430185`,
the base the spec's line numbers still cite.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `241015ade80eeec2a005e2c41f53318da7829b6ac65e3e2cd21c37c6f63e12c1` (identical to round 2 — confirmed unchanged) |
| Specs | `specs/spec01.md` — `8abea317a5ceedd08f4a7408447ea9931ac2c3da013d10ac82164dcb43ecb14f` |
| Material contracts/dependencies | `router.ctg` @ `ca11f6b` (`src/health.rs`, `src/proxy.rs`, `src/catalog.rs`, `src/frontier.rs`, `src/requirements.rs`, `.cartridge/tests/unit/proxy/capabilities.rs`); diffed against `192300f` to confirm the drift did not touch any symbol this spec depends on; a standalone `guardproof`/`guardproof2` two-test crate at `$TMPDIR` for the mutant-guard attack |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Unchanged from round 2 and correctly so — the author's report and my own reading agree only the mutant guard's final check and one ceiling sentence were touched this round. `prd.md`'s digest is byte-identical to round 2's, confirmed by `shasum -a 256`; `git diff HEAD -- prd.md` in `prd.ctg` is empty (the round-2 Outcome scope note is now the committed text, nothing further changed). |
| Ownership and reuse | 19 | Unchanged from round 2. No new reuse claim was added or needed to fix the guard. |
| Dependencies and implementable slices | 19 | Unchanged from round 2. Additionally verified: `router.ctg`'s shared checkout has moved from `192300f` to `ca11f6b` (one unrelated commit, system-prompt hoisting and operator-side refusal classification) since round 2. Diffed every file this spec anchors against across both revisions: `const REASONING` (health.rs:324, was 263), `DROPPABLE`, `refused_field`, `effort_refused`, `thinking_refused` all present and unchanged in substance; `data.rules.insert` still has exactly one call site (health.rs:1174, was 971 — the shift is earlier unrelated insertions, not a semantic change); `let mut learned` (proxy.rs:447) and `decision.selected(selected)` (proxy.rs:586) sit at the *same* line numbers as the base sha, coincidentally undisturbed; the injection gate (`proxy.rs:1004-1023`) is textually the same condition; `Catalog::new`'s `Policy::default()` (catalog.rs:450, was 438), `frontier::task` (frontier.rs:199, was ~200-224) and `requirements::present` (requirements.rs:22, unchanged) all hold; the fixture test `a_policy_reload_during_fallback_does_not_change_the_attributed_snapshot` and the anchor test at line 169 are present and untouched (the only test-file diff in the drift is 5 lines in an unrelated `reserve_recovery` call at line ~763). The base-sha drift is real but does not stale any fact this spec relies on — noted for the record, not deducted, since the spec already anchors by symbol and the drift is not the round-3 edit's doing. |
| Observable acceptance and baseline evidence | 14 | Round 2's literal finding is CLOSED: reproduced the target-passes/unrelated-fails case in a fresh two-test crate (`cargo test --lib`, exit 101) and confirmed the new guard, `grep -Eq '^test [a-z_:]*a_route_that_refuses_the_injected_effort_answers_without_it \.\.\. FAILED$'`, correctly rejects it (NOMATCH) where the old bare-name guard accepted. The guard as it appears in `specs/spec01.md`'s mutant block is verbatim what the round-3 report claims. Credit for real adversarial work: the author's own three-case proof table (pass/fail, concurrent-runner fail, absent) is genuine and I have no reason to doubt it. The ceiling wording fix (item 2 of this round's brief) is also done as claimed — see below. **Blocking, new:** the anchor is not tight enough at its left edge. `[a-z_:]*` permits *any* prefix built from lowercase letters, underscores and colons immediately before the target name, with no requirement that the boundary be a `::` module separator or the start of the identifier. So a *different* test whose full name merely *ends with* the target's exact name — e.g. `some_other_prefix_a_route_that_refuses_the_injected_effort_answers_without_it` — produces the libtest line `test tests::some_other_prefix_a_route_that_refuses_the_injected_effort_answers_without_it ... FAILED`, which satisfies the pattern. Reproduced directly: a crate with the target test absent entirely and only that suffix-named test present and failing gives the new guard a MATCH — i.e., a false accept, on exactly the case round 3 was asked to defend against ("a test whose name is a prefix or suffix of the target's"). This is the same class of defect as round 2's — a grep standing in for a behavioural assertion — surviving in narrower form after the anchor tightening. A one-line fix closes it: require the character preceding the target name to be either absent (bare `test ` immediately followed by the name) or a `::` module separator, e.g. `^test ([a-zA-Z0-9_]+::)*a_route_that_refuses_the_injected_effort_answers_without_it \.\.\. FAILED$`. |
| Failure, recovery and compatibility | 18 | Unchanged from round 2; not touched this round and nothing in the drift disturbs it. |
| Reviewer total | 89 / 100 | One blocking finding. |

### Findings and concrete revisions

**1. BLOCKING — the tightened mutant guard still accepts on a route the
brief asked this round to test: a failing test whose name has the target's
name as a trailing suffix.** `specs/spec01.md`, mutant `sh` block, final
check:

```sh
if grep -Eq '^test [a-z_:]*a_route_that_refuses_the_injected_effort_answers_without_it \.\.\. FAILED$' "$mutant/out.log"; then
```

`[a-z_:]*` is unbounded on its left and requires no separator before the
target name. Reproduced in a standalone two-test crate (`cargo test --lib`):
target test **absent entirely**, one test named
`some_other_prefix_a_route_that_refuses_the_injected_effort_answers_without_it`
present and made to fail. Suite exit 101; log line
`test tests::some_other_prefix_a_route_that_refuses_the_injected_effort_answers_without_it ... FAILED`;
the guard's regex **matches** this line (verified with the exact pattern
copied from the spec) even though the named target test does not exist in the
crate at all. A future implementation that never wires the turn-driving test
into the suite — or renames/breaks it — would still pass this block, riding on
any co-located test whose name happens to end with the target's name. Fix:
anchor the left edge on a module boundary or the start of the identifier
instead of a bare character class, e.g.
`^test ([a-zA-Z0-9_]+::)*a_route_that_refuses_the_injected_effort_answers_without_it \.\.\. FAILED$`.

This is not the "judge sees the judged" ceiling the workflow allows one round
for and then stops chasing — that ceiling is about a Verify block being unable
to prove a test died *of the behaviour* rather than of something the test
itself supplied. This is an ordinary anchoring bug with a one-line fix, in the
same dimension and for the same underlying reason round 1's finding 2 and
round 2's finding 1 both existed: an unexecuted (or under-executed) gate
design is not evidence the gate holds.

### Round 2 finding, re-checked

**Round 2 finding 1 (bare substring match anywhere in the log): CLOSED.**
Reproduced the exact adversarial case round 2 used — target test passing,
unrelated test failing, suite exit 101 — against a fresh build of the new
guard: NOMATCH (correct rejection), where the old guard matched. The fix as
merged is the one the round-2 finding asked for; a different, narrower gap in
the same mechanism is what blocks this round.

### Item 2 of this round's brief — ceiling wording, verified

`specs/spec01.md`'s Verify section states: "The claim is that a cold run
finishes well inside the 120 s block, and it is measured," then "Plan against
the slower of the two independent measurements, not the faster," quotes 25.4 s
and 26.3 s as the numbers to plan against with the author's own 17 s/18 s given
only as "the second data point," names the ~50 percent gap as "unexplained and
... not worth a round to chase," and closes with the forward rule: "If a cold
run ever approaches the block limit, that is the signal to filter — not the
faster number." This is what the round-2 finding asked for: the property is
stated as the property, the slower independent measurement is the one planned
against, and the gap is named rather than hidden. Not blocking.

### Item 3 of this round's brief — regression check, verified

`git diff HEAD -- prd.md` in `prd.ctg`: empty (byte-identical to the committed
revision; `shasum -a 256` matches round 2's recorded digest exactly). No file
in `router.ctg` was modified by this round or by any prior round: `git status
--porcelain` in `router.ctg` is now empty (0 files) — the working tree drift
present in rounds 1-2 has since landed as a normal commit from another
session, unrelated to this PRD, and diffed clean against every symbol this
spec depends on (see the dependencies row above). The parts of the spec earlier
rounds passed — the fixture recipe, the footprint widening rationale, the
`proxy.rs:444-447` comment correction, the streaming justification, the
caller-waiver "Decided, not open" section — read the same this round as
quoted in the round 2 review entry; the only textual changes are the mutant
guard's final `if` line and the ceiling paragraph.

### Rulings carried forward, not re-litigated

Per the brief: round 1's rulings (a) footprint widening to `src/proxy.rs`
justified, (b) "most of this already landed" true, (c) Verify blocks
mechanically sound apart from the (closed) ceiling claim, (d) a
caller-supplied reasoning control stays a waiver, all stand, unchanged by this
round's edit or by the unrelated upstream drift.

Disposition: revise. One narrowly-scoped fix — tighten the mutant guard's
left-edge anchor to a module boundary or start-of-identifier instead of an
open character class — should be a small, mechanical change to one regex and
should not cost a full round of rediscovery.
Validation: cwd `/Users/feb/dev/cartridge`, `/Users/feb/dev/cartridge/router.ctg`
and `/Users/feb/dev/cartridge/prd.ctg` for reads. `git rev-parse HEAD` in each:
superproject `b34e8ae714d1188da9e4ea4a0c5b95513404c3f8`, `router.ctg`
`ca11f6b90da09b661828d8e5002e1740c79b6a51`, `prd.ctg`
`e56330ed16b02675c7d91b2f73b4e41543127d47`. `git status --porcelain` in
`router.ctg`: 0. `git diff 192300f ca11f6b --stat -- src/health.rs src/proxy.rs
src/catalog.rs src/frontier.rs src/requirements.rs
.cartridge/tests/unit/proxy/capabilities.rs` and targeted `grep -n` on every
symbol the spec cites, at `ca11f6b`, to confirm none shifted in substance.
`shasum -a 256` on `prd.md` and `specs/spec01.md`; `git diff HEAD -- prd.md` in
`prd.ctg`. Two standalone throwaway crates at `$TMPDIR` (`cargo init --lib`,
deleted after use): one reproducing round 2's adversarial case against the new
guard (NOMATCH, correct), one reproducing the suffix-name attack (MATCH, the
new blocking finding) — both run with an isolated `CARGO_TARGET_DIR` under
`$TMPDIR`, never in `router.ctg`'s checkout. No cargo command was run inside
`router.ctg` or `prd.ctg`. No file in `router.ctg`, `prd.md`, or
`specs/spec01.md` was modified; the only writes are this record and
`.state/loop/a-route-that-refuses-reasoning/reviewer-3.md`.
Reviewer identity: Claude Sonnet 5, independent reviewer subagent for this
round; not the author of `prd.md` or `specs/spec01.md`, not the round 1 or
round 2 reviewer.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: (1) the mutant guard's anchor,
`^test [a-z_:]*<name> \.\.\. FAILED$`, accepts a log line produced by a
*different* failing test whose name ends with the target test's exact name,
because the character class before the name enforces no word or module
boundary; demonstrated by direct reproduction (target test absent, suffix-named
test failing, guard matches) rather than inferred.
Rounds used / remaining: 3 / 2.
Next action: one bounded revision of the mutant block's regex anchor in
`specs/spec01.md` (require a `::` boundary or start-of-identifier before the
target name), then round 4.
