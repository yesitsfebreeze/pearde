# @router/a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect review history

Plan: `@router/a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect`,
`prd.ctg/.cartridge/boards/router/prds/a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect/prd.md`.
Scope: executable leaf — a route that refuses a tool's JSON Schema for its dialect
receives the same tool in the dialect it accepts, and answers.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: `prd.md` + `specs/spec01.md` as published at review time, against
`router.ctg`. The spec names base `a4ea6e985361a29a3649b6013e5f30aa5b37bb9d`; the
repository was at `a4ea6e9` when the round opened and moved to `121913e` while it ran
(`fae0290 Add the availability test module src/health.rs already declares`, then
`121913e Land the requirements helper the collected proxy code already calls`).
Dirty in `router.ctg` throughout: `.cartridge/docs/recovery.md`, `.cartridge/help.md`,
`.cartridge/docs/cost-latency.md`, `cartridge.json`, `src/catalog.rs`, `src/known.json`,
`src/service.rs`, `src/sync.rs`, four `.cartridge/tests/unit/**` files; untracked
`.cartridge/memos/system/`, `.cartridge/memos/type/system.md`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `dc09bbcbd4203fb69b68112711f743367dc56723372b8a5e928cc00934ea2f6b` |
| Specs | `specs/spec01.md` — `c883836d2eeddf11889a853276b081aac73610dd5e727ad781f6e5db8574d927` |
| Material contracts/dependencies | `router.ctg/src/health.rs` `91ba4044…`; `router.ctg/src/proxy.rs` `c9155830…`; `router.ctg/.cartridge/tests/unit/proxy/capabilities.rs` `3438ea06…` (all three unchanged by `fae0290`/`121913e`); `prd.ctg/src/lifecycle.ts` `177200f0…` at `prd.ctg` `b27a7cb` — the collect/verify engine this spec's integration depends on |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | The outcome is measured, not asserted: 11 of 211 routes carry an open `compatibility` incident from a tool schema, and they are every Anthropic-family route the subscription offers. One coherent slice, one owner. The spec is honest that most of the outcome landed in `a4ea6e9` and still restates every Acceptance line, so no claim is unfalsifiable — the right call. −3: outstanding item 5 (commit the untracked availability test module) is an unnumbered obligation with no Acceptance line and no stated content, smuggled into a spec whose stated scope is proof completion. |
| Ownership and reuse | 17 | Correct owner. Reuses `Rules`/`propose`/`PRESERVING` rather than adding a mechanism; explicitly models the new loopback test on `a_renamed_parameter_moves_its_value_instead_of_losing_it` (`.cartridge/tests/unit/proxy/capabilities.rs:1654-1688`), which already proves the two-call retry shape against the same fixture. Refuses the `enum`/non-object wrapping with a reason tied to the Outcome shape, and pins the refusal of a provider branch with block 2's `route.provider` guard (0 matches in `health.rs` today — verified). Correctly reasons that `src/protocol.rs` needs no change because `rules.apply` runs on `outgoing` after the wire conversion. −3: `src/proxy.rs` is named by Acceptance line 4 and grepped twice by block 2 but appears in neither the PRD footprint nor the spec footprint, so any `proxy.rs` edit aborts collection at `prd.ctg/src/lifecycle.ts:134,154`; defensible today but unstated. |
| Dependencies and implementable slices | 9 | One lane, one line of production code, three tests, two doc edits — correctly sized and correctly ordered internally. But the lane→repo integration path is broken, and the spec reasons about the two causes and reaches the wrong conclusion on both. See blocking findings 1 and 2. This is exactly the "integration order and compatibility path" the method asks for at step 2. |
| Observable acceptance and baseline evidence | 16 | Every Acceptance line has a check, and the checks are engine-correct. Block 1 names exact test ids and guards a filter that matches nothing with `grep -q "^test .*$t \.\.\. ok$"` — that guard actually fired in my run, which is the proof it is not decorative. The module path `proxy::capability_tests` matches `src/proxy.rs:1244-1245`, and `--exact` disambiguates it from `catalog::capability_tests` (`src/catalog.rs:662`). Block 2 uses `if grep -qn …; then exit 1; fi`, not the inert `! grep` under `set -e`. Every baseline claim I checked is true. −4 across three weaknesses: (a) block 3 proves the three union keywords textually — `grep -q "\"oneOf\":"` passes on any occurrence anywhere in the file — where Acceptance line 3 asks for a property; the assertion belongs in the test block 1 runs. (b) Block 3's `grep -qi 'oneOf'` and `grep -qi 'widen'` on `.cartridge/docs/recovery.md` already pass in the live checkout from another PRD's unstaged hunk (`recovery.md:54,70`), so verify pass 2 proves half of Acceptance line 6 with work this PRD did not do; the `help.md` grep still forces real work and the lane pass is honest, so this is a weakness rather than a hole. (c) Block 2's `self.drop.contains(key)` pins an implementation literal; block 1's behavioral test is the real proof of that line. |
| Failure, recovery and compatibility | 12 | "Denied worlds" is genuinely falsifiable — four counterfactuals, each naming the check that catches it, and I confirmed the first by reading `preserves`. The widening argument is sound and matches the committed code: branch properties are merged, branch `required` is not promoted, so every input the original schema admitted the rewritten one admits. The 120 s budget is stated with a measurement and I reproduced it: 10 s for a cold build into a fresh `CARGO_TARGET_DIR`, then four filtered runs. `CARGO_TARGET_DIR` is pinned per the known hot-restart hazard, and it lands outside both footprints. −8: denied world 4 states the wrong recovery for the untracked module (finding 2); nothing states what happens when collection aborts after the lane commit has landed; nothing states that a no-lane collection would sweep the foreign `help.md`/`recovery.md` hunks into `Implement @router/…`. |
| Reviewer total | 71 / 100 | Two blocking findings, both of which make `prd collect` abort after the implementer's work is already committed on the lane branch. |

Findings and concrete revisions:

1. **BLOCKING — the fast-forward cannot land, because two spec-footprint files are
   dirty in the live checkout.** `specs/spec01.md` frontmatter footprint names
   `.cartridge/help.md` and `.cartridge/docs/recovery.md`; both carry unstaged
   modifications in `/Users/feb/dev/cartridge/router.ctg` right now
   (`.cartridge/help.md` +3/−3 on `availability` and `routing.quality_margin`;
   `.cartridge/docs/recovery.md` +69/−2 adding "What a route can be taught",
   "Adaptation and waiver", "A model the provider has withdrawn" and "When every
   route is on cooldown"). A lane worktree is cut from HEAD when the PRD is claimed
   at `specced` (`prd.ctg/src/lifecycle.ts:225`), and Acceptance line 6 requires the
   implementer to change both files inside that lane. `collect` refuses only *staged*
   changes (`prd.ctg/src/lifecycle.ts:104`) — unstaged dirt survives to the
   fast-forward at `prd.ctg/src/lifecycle.ts:166`. Reproduced in a scratch repository:
   `git merge --ff-only` aborts with "Your local changes to the following files would
   be overwritten by merge" and exit 1 even when the lane's hunk and the local hunk do
   not overlap. At that point `prd.ctg/src/lifecycle.ts:157-158` has already committed
   the work on the lane branch, and the PRD is stuck claimed.
   Recommendation: state as an explicit precondition in the spec that `router.ctg`'s
   pending `.cartridge/help.md` and `.cartridge/docs/recovery.md` hunks are committed
   or stashed *before* the PRD is claimed. The implementer cannot do this from inside
   the lane, so it cannot be left to them. Alternatively drop `recovery.md` from this
   spec's footprint and let the sibling PRD that authored those rows carry it —
   but `help.md` still has to move, and `help.md` is dirty too.

2. **BLOCKING — the spec is stale against its own base, and its handling of the
   untracked test module was wrong even before it went stale.** The spec pins
   `Base: a4ea6e9`. `router.ctg` is now at `121913e`; `fae0290 Add the availability
   test module src/health.rs already declares` landed during this round, so
   `.cartridge/tests/unit/health/availability.rs` is tracked
   (`git ls-files --error-unmatch` exits 0). Outstanding item 5 and denied world 4
   now describe a repository that no longer exists, and the footprint entry for that
   file is obsolete. Independently, the remedy item 5 offered was already wrong:
   "It is inside the PRD footprint, so collection sweeps it" holds only when there is
   no lane, because the status sweep runs against `tree`, which is the lane whenever
   one exists (`prd.ctg/src/lifecycle.ts:125,145`). With a lane, the implementer
   commits the file in the lane and the fast-forward then aborts on the untracked
   duplicate in the live checkout — reproduced in a scratch repository: `git merge
   --ff-only` refuses with "The following untracked working tree files would be
   overwritten by merge" even when the content is byte-identical.
   Recommendation: rebase `Base:` onto `121913e`, delete outstanding item 5 and denied
   world 4, drop `.cartridge/tests/unit/health/availability.rs` from the spec
   footprint, and re-verify. The same round should confirm the `#[path]` at
   `src/health.rs:1021-1022` still resolves (it does).

3. Non-blocking — `src/proxy.rs` carries Acceptance line 4's guard and is grepped
   twice by block 2, but is in neither footprint. Any needed edit there aborts with
   "committed path is outside the PRD footprint" (`prd.ctg/src/lifecycle.ts:134`).
   Add it to the spec footprint, or say in one line that it is deliberately frozen
   because the guard already landed.

4. Non-blocking — Acceptance line 3 asks for the widening property over all three
   union keywords; block 3 only greps for the literals `"allOf":`, `"oneOf":`,
   `"anyOf":` in the test file. Move the claim into
   `a_union_tool_schema_is_widened_into_the_object_every_provider_takes` by looping the
   existing assertions over the three keywords, so block 1 proves it and block 3's
   grep is a backstop rather than the evidence.

5. Non-blocking — block 3's `recovery.md` greps already pass at HEAD from another
   PRD's unstaged rows (`recovery.md:54,70`), so verify pass 2 will report Acceptance
   line 6 satisfied for `recovery.md` without this PRD having written it. Naming a
   string only this change introduces would restore the attribution.

Claims checked independently and confirmed sound, with no deduction:

- Acceptance lines 1 and 2 are implemented at HEAD. `pub widen_tools: bool`
  (`src/health.rs:142-145`), `next.widen_tools = true` under `tool_schema_refused`
  in `propose` (`src/health.rs:249-251`), `pub fn widen_tools` / `pub fn widen_schema`
  (`src/health.rs:424-489`), `fn tool_schema_refused`, and the retry-same-route path
  generic over `propose` in `src/proxy.rs:580-587` — which pushes the route back to
  the front of the queue before the failure counts against its health.
- The hole in `Rules::preserves` is real. `src/health.rs:219-223` returns
  `PRESERVING.contains(&key) || …` with no regard for *how* the key changed, and
  `PRESERVING` is `["messages", "input", "tools"]` (`src/health.rs:155`). A rule with
  `drop: {"messages"}` therefore passes the waiver guard at `src/proxy.rs:846-856` and
  the route is called with the conversation gone. `propose` cannot learn that rule
  today, because `refused_field` is gated on `DROPPABLE` — the spec says exactly this,
  and asking for a pinning test anyway is the right call. The proposed one-line fix
  (`preserves` denies a key in `self.drop`) is correct and does not disturb the
  reasoning-key or router-added-field paths, neither of which is in `PRESERVING`.
- The 120 s budget holds. Cold build into a fresh `CARGO_TARGET_DIR` outside the
  repository: 10 s, exit 0.

Disposition: revise. The spec's analysis and proof design are strong; both blockers
are preconditions and staleness, not design errors, and one round should clear them.

Validation: cwd `/Users/feb/dev/cartridge/router.ctg` unless stated. Each Verify block
extracted verbatim and run as `sh -eu <file>`, the same interpreter and flags as
`prd.ctg/src/lifecycle.ts:44` (`['sh','-eu','-c',block]`), well inside the 120 s cap.

- Block 1 — exit **1**. Fails on
  `a_refused_tool_schema_is_rewritten_and_the_same_route_answers did not run`: the
  `--exact` filter matched 0 of 78 tests and the `grep -q "^test … ok$"` guard caught
  it. The preceding test
  `a_union_tool_schema_is_widened_into_the_object_every_provider_takes` ran and passed,
  so the module path and filter are mechanically correct. Same exit before and after
  HEAD moved.
- Block 2 — exit **1**. Fails on `grep -q 'self.drop.contains(key)' src/health.rs`.
  Every other grep in the block passes; `grep -cn 'route.provider' src/health.rs`
  returns 0, so the provider-branch guard passes rather than short-circuiting.
- Block 3 — exit **1**, printing `oneOf is never built into a schema`. The two
  refusal-text greps pass (`capabilities.rs:1612-1613`) and `allOf` passes
  (`capabilities.rs:1624`), so the block reaches the real gap.
- `git -C /Users/feb/dev/cartridge/router.ctg ls-files --error-unmatch
  .cartridge/tests/unit/health/availability.rs` — exit 1 at round open
  ("did not match any file(s) known to git"), exit 0 after `fae0290`.
- Scratch-repository reproductions of both `git merge --ff-only` refusals
  (untracked duplicate; non-overlapping local modification), each exit 1.
- Cold build measurement: `CARGO_TARGET_DIR` set outside the repository, one filtered
  `cargo test --lib`, 10 s, exit 0.

No file in `router.ctg`, `prd.ctg/src`, `prd.md` or `specs/spec01.md` was modified by
this review; the only write is this record.

Reviewer identity: Claude Opus 5 (1M context), independent reviewer subagent; not the
author of `prd.md` or `specs/spec01.md`.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: (1) the lane fast-forward cannot land while
`.cartridge/help.md` and `.cartridge/docs/recovery.md` are dirty in the live checkout
and in this spec's footprint; (2) the spec is stale against base `a4ea6e9` — the
repository is at `121913e` — and outstanding item 5 / denied world 4 state a recovery
that collection does not perform when a lane exists.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision addressing findings 1 and 2, folding in 3–5, then
re-review against the new base.

## Round 2 — 2026-09-17

Presented revision: `specs/spec01.md` revised against round 1, with `prd.md`'s
planning note rebased to `121913e` and carrying the no-lane decision. `router.ctg`
at `121913eddef9a2c5537e21ee5405cffe1d86291c`, unmoved for the whole round.
Dirty in `router.ctg` throughout, unchanged from round 1: `.cartridge/docs/recovery.md`,
`.cartridge/help.md`, `.cartridge/docs/cost-latency.md`, `cartridge.json`,
`src/catalog.rs`, `src/known.json`, `src/service.rs`, `src/sync.rs`, and
`.cartridge/tests/unit/{auth/tests.rs,catalog/capabilities.rs,settings/tests.rs,sync/tests.rs}`;
untracked `.cartridge/memos/system/`, `.cartridge/memos/type/system.md`.
The PRD directory is itself untracked in `prd.ctg` (new record, not yet committed).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `40ef24ecc261699e8afae1cb5ac8c468a9c16e739b0176884c04a5be8f831bdc` (was `dc09bbcb…` in round 1) |
| Specs | `specs/spec01.md` — `204c3841fc6898aac762af63018ae7d1c2a0b907dc3bbc65a96b6d261d67d0c5` (was `c883836d…`) |
| Material contracts/dependencies | `router.ctg/src/health.rs` `91ba4044…`, `src/proxy.rs` `c9155830…`, `.cartridge/tests/unit/proxy/capabilities.rs` `3438ea06…` — all three byte-identical to round 1; `prd.ctg/src/lifecycle.ts` `177200f0…` and `prd.ctg/src/planner.ts` `fd60f4c7…`, the collect/verify engine and the footprint union this revision's landing decision rests on |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Value unchanged and still measured. Scope is cleaner than round 1: outstanding item 5 is gone, the base is current, and Acceptance line 6 now demands specific words — the `tool-schema` cause label and "top level" only — which turns a vague docs obligation into a checkable one and simultaneously fixes the attribution weakness. −2: the "Landing" section puts coordination policy inside a spec. Justified here, since the decision is a precondition on how the work is landed rather than what is built, but it is the spec carrying weight the board would normally carry. |
| Ownership and reuse | 19 | `src/proxy.rs` is now explicitly frozen, with the exact abort it would produce (`prd.ctg/src/lifecycle.ts:134`) and an instruction to stop and ask rather than work around it — better than silently widening the footprint. The obsolete `availability.rs` footprint entry is gone. Reuse reasoning (the rename test as the model, `rules.apply` on `outgoing` making `protocol.rs` unnecessary, the `enum`/non-object exclusion tied to the Outcome shape) is unchanged and I confirmed it again. −1: `src/protocol.rs` stays in the PRD footprint although the spec argues it needs no change; a reservation that only widens the sweep. |
| Dependencies and implementable slices | 15 | Round-1 blocker 1 is genuinely resolved, and resolved on the merits rather than by assertion. I verified each leg: `prd.ctg/src/lifecycle.ts:113` reads `collect requires claimed or specced work`, so collecting from `specced` is an engine-sanctioned path, not a workaround; `prd.ctg/src/lifecycle.ts:125` selects `tree = code` when no lane directory exists, so there is no worktree, no fast-forward at `:166` and therefore no abort-after-commit; `verify` runs at `:137` and again only under `tree !== code` at `:168`, so the blocks run exactly once, in `repo`. The spec's Verify comment states this correctly. −5 for understating its own consequence: see finding 2. |
| Observable acceptance and baseline evidence | 13 | The attribution fix is real and I checked it rather than took it: at `121913e` with the live dirt in place, `grep -q 'tool-schema' .cartridge/docs/recovery.md` exits 1, `grep -qi 'top level' .cartridge/docs/recovery.md` exits 1 (the sibling's row says "top-level", hyphenated, which does not match), and `grep -qi 'tool schema' .cartridge/help.md` exits 1. So all three doc checks now fail on work only this change can do. Block 2's demotion to a tripwire that passes at base is labelled honestly and is correct practice — a structural regression guard is not evidence of outstanding work, and saying so is better than pretending. Block 1 is unchanged and still mechanically sound. −7: Acceptance line 3 now has no executable check at all. See blocking finding 1. |
| Failure, recovery and compatibility | 13 | The denied-worlds section gained a lane counterfactual with a stated recovery (reset the lane branch, re-collect with no lane), which is the right shape. On the coordinator's question about a stranded compile dependency: this spec does not leave a comparable hole. `feet` is the union of the PRD and spec footprints (`prd.ctg/src/planner.ts:5-9`), and the PRD footprint's `.cartridge/tests` entry covers the entire test tree, so a new or moved test module cannot be stranded the way `fae0290` was. The only stranded-dependency risk left is `src/proxy.rs`/`src/requirements.rs`, and the spec names both the abort and the escalation. I also confirmed the untracked `.cartridge/memos/**` sit outside the footprint, so the post-receipt `ls-files --others` check at `prd.ctg/src/lifecycle.ts:174` will not abort. Cold-build budget restated as 10–15 s; I measured 10 s in round 1. −7: denied world 4 is false — see blocking finding 1 — and a false gate claim in the section that carries this dimension's evidence is the specific defect this method exists to catch. |
| Reviewer total | 78 / 100 | Both round-1 blockers cleared convincingly; one new blocking finding, and the plan misstates its own collection cost. |

Findings and concrete revisions:

1. **BLOCKING — Acceptance line 3 has no executable check, and denied world 4
   claims one that does not exist.** Round 1 asked for the meaning-preservation
   property to move from a grep into the test. The spec moved the *prose* — line 3
   now names `a_union_tool_schema_is_widened_into_the_object_every_provider_takes`
   and spells out what it must assert for each of `allOf`, `oneOf`, `anyOf` — but
   added no check that the test actually does it. Block 1 runs that test and asserts
   only `^test .*$t \.\.\. ok$`; a test still covering `allOf` alone passes it. Block 3
   still only greps the file for the literals `"allOf":`, `"oneOf":`, `"anyOf":`,
   which any schema literal anywhere in `capabilities.rs` satisfies — including ones
   in the new loopback test. So an implementer who writes all four tests, leaves the
   widening test on `allOf`, and happens to use `oneOf`/`anyOf` literals elsewhere
   gets block 1 exit 0 and block 3 exit 0 with line 3 unmet. Denied world 4 asserts
   the opposite — "block 3 passes and block 1 still fails, because Acceptance line 3
   now names the test rather than the file" — and that is not how block 1 works; it
   does not read the test's body, only its result. By the spec's own standard in its
   third paragraph, "a claim nobody can fail is not a claim", line 3 is now such a
   claim.
   Recommendation, either one: split the widening proof into three tests —
   `a_union_tool_schema_is_widened_into_the_object_every_provider_takes_for_all_of`,
   `…_for_one_of`, `…_for_any_of` — and name all three in block 1's loop, so the
   engine fails when a keyword is unproven; or keep one test and add to block 3 a
   structural check that it iterates the three keywords rather than merely mentioning
   them. The first is cheaper to read and impossible to satisfy accidentally.
   Correct denied world 4 to match whichever is chosen.

2. Non-blocking, but must be fixed in the same revision — **the stated collection
   consequence is understated by four files.** The spec says "`collect` sweeps the
   whole dirty in-footprint file, so the sibling PRD's pending `help.md` and
   `recovery.md` hunks land inside this PRD's commit", and calls that "stated so
   nobody is surprised by it". The sweep is not two files. `feet` unions the PRD
   footprint with every spec footprint (`prd.ctg/src/planner.ts:5-9`), and `prd.md`
   frontmatter still reserves `.cartridge/tests` wholesale. Running the engine's own
   sweep query over that union — `git status --porcelain=v1 --untracked-files=all --`
   the footprint, as `prd.ctg/src/lifecycle.ts:145` does — returns six modified files,
   not two: `.cartridge/docs/recovery.md`, `.cartridge/help.md`, and also
   `.cartridge/tests/unit/auth/tests.rs`, `.cartridge/tests/unit/catalog/capabilities.rs`,
   `.cartridge/tests/unit/settings/tests.rs`, `.cartridge/tests/unit/sync/tests.rs`.
   All four are other sessions' uncommitted work, one of them in a different
   cartridge's test area, and all four will be committed as `Implement @router/a-tool-schema…`.
   Collection still succeeds — every path is inside the footprint, so `assertFootprint`
   passes — which is why this is not blocking. But a plan that names the cost and then
   names a third of it is worse than one that stays silent.
   Recommendation: name all six, or narrow the PRD footprint from `.cartridge/tests`
   to `.cartridge/tests/unit/proxy/capabilities.rs` so the sweep matches the work.
   Narrowing is the better fix and costs nothing here — but note that narrowing a
   footprint is exactly what stranded the compile dependencies that `fae0290` and
   `121913e` had to repair, so if it is narrowed, block 1 must stay as the proof that
   the crate's tests still build.

3. Non-blocking — with no lane, the verification evidence in the receipt is produced
   against a tree carrying roughly a dozen other sessions' uncommitted files, so the
   recorded exit 0 describes a state that never existed in git and cannot be
   reconstructed from the receipt's commit. That is an inherent cost of the no-lane
   decision, not an error in it, and the alternative is a collection that provably
   aborts. Worth one sentence in the Landing section so the receipt is read correctly
   later.

4. Non-blocking — `prd.md`'s Acceptance lines 3 and 6 still carry the round-1 wording
   while `spec01.md`'s carry the sharpened wording. `collect` ticks boxes in both
   (`prd.ctg/src/lifecycle.ts:112`), so nothing breaks, but the PRD and its spec now
   state different acceptance for the same two lines. Bring `prd.md` into line.

Verified fixed since round 1:

- Round-1 blocker 1 (lane fast-forward) — resolved. Verified on the merits above; the
  engine permits collect from `specced` (`prd.ctg/src/lifecycle.ts:113`), the no-lane
  path skips the fast-forward entirely (`:125`, `:166`), and the spec's Verify comment
  describes blocks running once in `repo` correctly.
- Round-1 blocker 2 (staleness) — resolved. Base is `121913e`; outstanding item 5,
  denied world 4's untracked-file case and the `availability.rs` footprint entry are
  all gone. `git ls-files --error-unmatch .cartridge/tests/unit/health/availability.rs`
  exits 0, and the `#[path = "../.cartridge/tests/unit/health/availability.rs"]` at
  `src/health.rs:1020-1022` resolves — block 1 compiles the crate's tests, which is
  the standing proof of it.
- Round-1 finding 3 (`src/proxy.rs` footprint) — resolved by an explicit freeze.
- Round-1 finding 5 (`recovery.md` attribution) — resolved; all three doc greps are
  0 matches in the live file today.
- Round-1 finding 4 (meaning preservation) — **not** resolved; it is blocking
  finding 1 above.

Disposition: revise. One bounded change to block 1 and denied world 4, plus the
footprint or wording fix in finding 2. The plan's substance is sound.

Validation: cwd `/Users/feb/dev/cartridge/router.ctg` unless stated. Each Verify block
extracted verbatim from the revised spec and run as `sh -eu <file>`, matching the
engine's `['sh','-eu','-c',block]` at `prd.ctg/src/lifecycle.ts:44`.

- Block 1 — exit **1**. Fails on
  `a_refused_tool_schema_is_rewritten_and_the_same_route_answers did not run`; the
  `--exact` filter matched 0 of 78 tests and the `^test … ok$` guard caught it. The
  preceding widening test ran and passed, so the module path and filter are sound.
- Block 2 — exit **0**, as the spec says it should be at base and labels it. Every
  grep passes and `route.provider` has 0 matches in `src/health.rs`, so the
  provider-branch tripwire passes rather than short-circuiting.
- Block 3 — exit **1**, silently, on
  `grep -q 'a_refused_tool_schema_is_rewritten_and_the_same_route_answers'` — the
  reordering means it now fails on the missing test name before reaching the union
  loop or the doc greps. I therefore ran the three doc greps separately: `tool-schema`
  in `recovery.md` exit 1, `top level` in `recovery.md` exit 1, `tool schema` in
  `help.md` exit 1. All three fail for the stated reason.
- `git status --porcelain=v1 --untracked-files=all --` over `feet(prd)` — six modified
  paths, no untracked paths (finding 2).
- `git ls-files --error-unmatch .cartridge/tests/unit/health/availability.rs` — exit 0.

Author-reported exit codes were 1, 0, 1; observed 1, 0, 1. No file in `router.ctg`,
`prd.ctg/src`, `prd.md` or `specs/spec01.md` was modified by this round, no `prd`
operation was run, nothing was committed, and no dirty hunk was stashed or reverted;
the only write is this record.

Reviewer identity: Claude Opus 5 (1M context), independent reviewer subagent; same
reviewer as round 1, not the author of `prd.md` or `specs/spec01.md`.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: (1) Acceptance line 3 has no executable check — block 1
asserts only that `a_union_tool_schema_is_widened_into_the_object_every_provider_takes`
passed, block 3 greps the file for the three keyword literals, and denied world 4
falsely claims block 1 catches a test left on `allOf`.
Rounds used / remaining: 2 / 3.
Next action: one bounded revision — make block 1 prove the three keywords, correct
denied world 4, and fix the understated sweep in finding 2 — then re-review.

## Round 3 — 2026-09-17

Presented revision: `specs/spec01.md` revised against round 2, with the PRD footprint
narrowed by the coordinator from the bare `.cartridge/tests` to
`.cartridge/tests/unit/proxy/capabilities.rs`. `router.ctg` at
`121913eddef9a2c5537e21ee5405cffe1d86291c`, unmoved for the whole round.
Dirty in `router.ctg`, unchanged from rounds 1 and 2 and untouched by this review:
`.cartridge/docs/recovery.md`, `.cartridge/help.md`, `.cartridge/docs/cost-latency.md`,
`cartridge.json`, `src/catalog.rs`, `src/known.json`, `src/service.rs`, `src/sync.rs`,
`.cartridge/tests/unit/{auth/tests.rs,catalog/capabilities.rs,settings/tests.rs,sync/tests.rs}`;
untracked `.cartridge/memos/system/`, `.cartridge/memos/type/system.md`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `e49fa223dac0bad5fdfe7d790ecef2e9a9c71b849aa0880e6e1a7c21cb900596` (was `40ef24ec…`; footprint narrowed) |
| Specs | `specs/spec01.md` — `f661e5aefc9f2f8c3c34d2d4ddbb3e45bd62bf8baaa8bf96767261fd0c1277b4` (was `204c3841…`) |
| Material contracts/dependencies | `router.ctg/src/health.rs` `91ba4044…`, `src/proxy.rs` `c9155830…`, `.cartridge/tests/unit/proxy/capabilities.rs` `3438ea06…` — all three still byte-identical to round 1; `prd.ctg/src/lifecycle.ts` `177200f0…`, `prd.ctg/src/planner.ts` `fd60f4c7…` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Value unchanged and still measured — 11 of 211 routes, every Anthropic-family route the subscription offers. Scope is tight and the spec remains unusually honest about what already landed. Outstanding item 3 grew, and earns it: it now explains *why* the widening proof is three tests rather than one loop, which is the reasoning a reader needs to not "simplify" it back. −2: the Landing section still carries landing policy inside a spec. It is load-bearing and now precisely correct, so the deduction is small, but it is board policy living in a plan. |
| Ownership and reuse | 19 | Unchanged and sound. The three widening tests share one helper rather than triplicating assertions — reuse, not copy-paste, which is the right answer to "split it into three". `src/proxy.rs` stays frozen with the exact abort and an escalation path; the rename test is reused as the model for the loopback proof; the `enum`/non-object exclusion stays tied to the Outcome shape; `src/protocol.rs` is still argued unnecessary. −1: `src/protocol.rs` nonetheless remains reserved in the PRD footprint. Harmless now that it is clean, but vestigial. |
| Dependencies and implementable slices | 19 | Round-2 finding 2 is resolved, and I verified the fix rather than the claim. Running the engine's own sweep — `git status --porcelain=v1 --untracked-files=all --` over `feet(prd)`, the union of the PRD's three entries and the spec's four (`prd.ctg/src/planner.ts:5-9`) — now returns exactly two paths, `.cartridge/docs/recovery.md` and `.cartridge/help.md`, which is precisely what the Landing section says. The four dirty files under `.cartridge/tests/unit/{auth,catalog,settings,sync}` have dropped out of scope. Every engine citation in that section checks out: `lifecycle.ts:104` staged-only, `:125` tree selection, `:134` footprint abort, `:143-155` the sweep, `:157-158` the lane commit, `:166` the fast-forward. The no-lane path remains correct and engine-sanctioned (`lifecycle.ts:113`). −1 for the exposure the narrowing created, carried into the next dimension. |
| Observable acceptance and baseline evidence | 18 | Round-2's blocker is closed, and closed with the right fix. Block 1 now names all six tests, three of them one per union keyword, so Acceptance line 3 is gated by the engine rather than by prose. I checked both directions instead of one: block 1 fails on the first missing name (`an_all_of_… did not run`), and the identical block body over the two tests that exist today exits 0 with exactly two `… ok` lines — so the failure is the intended gate, not a broken filter or a wrong module path. Deleting or renaming any one of the three makes `--exact` match nothing and the guard fire. The doc greps are still 0 matches in the live file (`tool schema` in `help.md`, `tool-schema` and `top level` in `recovery.md` — the sibling's row writes "top-level", hyphenated, and never writes the cause label), so Acceptance line 6 cannot be credited to another session's work. Block 2's tripwire role and block 3's backstop role are both labelled honestly. −2 for the residual the coordinator named: block 1 reads a test's result, never its body, so a test that keeps its name while weakening its assertions passes. That is inherent to every test-gated spec — closing it would mean grepping test internals, which is both brittle and the anti-pattern this codebase names — and Acceptance line 3 spells the assertions out for the reviewer who reads the diff. Three names is the maximal gate available; I do not deduct further for it. |
| Failure, recovery and compatibility | 16 | Denied world 4 is now true, and it is the one I had falsified in round 2. I confirmed its exact mechanism three times across three rounds: the `--exact` filter matches 0 of 78 tests, `cargo test` still exits 0 reporting "0 passed; 78 filtered out", and `grep -q "^test .*$t \.\.\. ok$"` fires with `<name> did not run` and exit 1. Denied world 3 is correctly restated over all three widening tests, and the lane world keeps a stated recovery. The cold-build budget (10–15 s against a 120 s cap) matches the 10 s I measured in round 1. −4: the new stranded-file rule is prose where a one-line gate exists. See finding 1. |
| Reviewer total | 90 / 100 | Both round-1 blockers and the round-2 blocker are closed, each verified independently. One non-blocking finding remains, with a fix recommended for the next spec rather than this one. |

Findings and concrete revisions:

1. Non-blocking — **the stranded-file rule is stated well but gated only by prose,
   and narrowing the footprint is what made it necessary.** The spec says, in bold,
   that every new test goes into `.cartridge/tests/unit/proxy/capabilities.rs`,
   gives the reason, and names the `availability.rs` failure `fae0290` repaired.
   That is as clearly as prose can put it. But nothing fails if it is ignored, and
   I can show the exposure without writing anything: the sweep over the narrowed
   footprint no longer reports the four modified files under
   `.cartridge/tests/unit/{auth,catalog,settings,sync}`, so it is equally blind to a
   *new* file there. A new test file outside `unit/proxy/` would therefore be invisible
   to the sweep at `prd.ctg/src/lifecycle.ts:143-155`, invisible to the post-receipt
   `ls-files --others` check at `:174`, left untracked, and collection would go green
   with `HEAD` carrying a `#[path]` to a file no clean checkout has — exactly the
   state `fae0290` had to repair. It also needs two deliberate acts against an explicit
   written instruction (create the file, then add a `#[cfg(test)] #[path]` module
   declaration in `src/health.rs`), which is why this is a finding and not a blocker:
   ordinary drift does not reach it.
   Recommended gate, one line in block 2 or 3:
   `test -z "$(git ls-files --others --exclude-standard -- .cartridge/tests)"`.
   At verify time nothing is committed yet, so an edited `capabilities.rs` is modified
   rather than untracked and passes, while any new file under `.cartridge/tests`
   fails the block.
   **I am not requiring this change in this round.** Editing a Verify block is a
   substantive change to the reviewed revision, which under review method step 8 would
   make this rating stale and cost a fourth round for a hazard that needs deliberate
   disobedience to reach. Carry it into the next spec on this board instead, where it
   costs nothing.

2. Withdrawn — round-2 finding 4 said `prd.md` and `spec01.md` state different
   acceptance for lines 3 and 6. They still do, and on reflection that is correct
   layering rather than a defect: the PRD states the outcome in general terms and the
   spec sharpens it into a gated proof. The PRD's lines are weaker versions of the
   spec's, not contradictions of them, and `collect` ticks boxes in both
   (`prd.ctg/src/lifecycle.ts:112`). No change wanted.

Verified fixed since round 2:

- Round-2 blocker (Acceptance line 3 ungated) — **resolved**. Three named tests, all
  six names in block 1's loop, verified in both directions as described above.
  Denied world 4 rewritten to the real mechanism and confirmed against observed
  behavior.
- Round-2 finding 2 (understated sweep) — **resolved**, and resolved better than
  asked: rather than restating the six files, the coordinator narrowed the PRD
  footprint so the sweep genuinely is the two files the spec names. Verified.
- Round-2 finding 3 (evidence produced against a dirty tree) — partially addressed;
  the tree is still shared, but the footprint that reaches the commit is now exactly
  two foreign-dirty files instead of six, which is the material part.
- Round-1 blockers 1 and 2, and round-1 findings 3 and 5 — all remain resolved;
  rechecked this round, nothing regressed.

Disposition: keep. Proceed to implementation.

Validation: cwd `/Users/feb/dev/cartridge/router.ctg` unless stated. Each Verify block
extracted verbatim from the revised spec and run as `sh -eu <file>`, matching the
engine's `['sh','-eu','-c',block]` at `prd.ctg/src/lifecycle.ts:44`, well inside the
120 s cap.

- Block 1 — exit **1**, stopping at
  `an_all_of_tool_schema_is_widened_into_the_object_every_provider_takes did not run`
  after `cargo test` reported "0 passed; 78 filtered out" and exited 0. The intended
  gate on the first unwritten test.
- Block 2 — exit **0**, as designed and labelled. `route.provider` has 0 matches in
  `src/health.rs`, so the provider-branch tripwire passes rather than short-circuits.
- Block 3 — exit **1**, silently, on
  `grep -q 'a_refused_tool_schema_is_rewritten_and_the_same_route_answers'`. I ran the
  three doc greps separately since the block stops before them: `tool schema` in
  `.cartridge/help.md` exit 1, `tool-schema` in `.cartridge/docs/recovery.md` exit 1,
  `top level` in `.cartridge/docs/recovery.md` exit 1.
- Control run — block 1's body unchanged except for substituting the two tests that
  exist at `121913e` (`a_union_tool_schema_is_widened_into_the_object_every_provider_takes`,
  `an_adaptation_applies_where_a_waiver_is_refused`): exit **0**, exactly two
  `… ok` lines. This is the evidence that block 1's module path, `--exact` filter and
  `… ok` guard all work, and that its exit 1 above is the gate firing rather than a
  mechanical defect.
- Engine sweep over `feet(prd)` — `git status --porcelain=v1 --untracked-files=all --`
  the five union paths: exactly `.cartridge/docs/recovery.md` and `.cartridge/help.md`,
  no untracked entries.

Author-reported exit codes were 1, 0, 1 with a passing control; observed 1, 0, 1 with a
passing control. No file in `router.ctg`, `prd.ctg/src`, `prd.md` or `specs/spec01.md`
was modified by this round, no `prd` operation was run, nothing was committed, and no
dirty hunk was stashed or reverted; the only write is this record.

Reviewer identity: Claude Opus 5 (1M context), independent reviewer subagent; same
reviewer as rounds 1 and 2, not the author of `prd.md` or `specs/spec01.md`.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS** — 90/100, threshold met, no unresolved blocking finding. This passes
the delegated review gate for the revision digested above. It is a reviewer score, not
a measurement of the shipped behavior; the Verify blocks still have to go green on the
implemented change.
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: proceed to implementation. `prd specced`, then dispatch an implementer who
works directly in `/Users/feb/dev/cartridge/router.ctg` with no lane, puts every new
test in `.cartridge/tests/unit/proxy/capabilities.rs`, and stops to ask rather than
editing `src/proxy.rs`. A substantive later edit to `prd.md` or `specs/spec01.md` makes
this rating stale and costs one of the two remaining rounds.
