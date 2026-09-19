# @runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node review history

Plan: `@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node`,
`prd.ctg/.cartridge/boards/runtime/prds/a-native-cartridge-s-outbound-call-does-not-block-its-own-node/prd.md`.
Scope: executable leaf. One observable outcome — a node keeps answering unrelated
events while a handler is parked in an outbound call, locked by a host regression
test and stated in the host's documentation. Under the user's Option A the host
does not change.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-19

Presented revision: `prd.ctg` at `813bfb54` with `prd.md` modified in the working
tree and `specs/` untracked.

Code base, and this is itself a finding: the spec declares "Base: cartridge.ctg
`beb8213`", and `cartridge.ctg` moved eight commits during this single review —
`beb8213` → `ab2383a` → `3be9745` → `7af748a` → `804a08b` → `a2c5962` →
`5980c7c` → `2ea1aae` → `324f36e`. **Every measurement in this round was taken
twice: first at `ab2383a`, then re-taken in a fresh clone at `2ea1aae` after the
coordinator flagged the move, with the pass-2 formatting snapshot at `324f36e`.**
Both series are reported below, because one of them flipped. Two of the spec's
five footprint paths moved in that window: `.cartridge/help.md` (+2) and
`.cartridge/tests/unit/src/tests/host.rs` (+2/-2), both at `804a08b`.

Reviewing environment: `CARTRIDGE_YOLO=1` present, inherited from
`just launch claude --yolo`; no `CARTRIDGE_HOME`, no `CARTRIDGE_BIN`. Every
measurement that could depend on it was taken both as-is and under
`env -u CARTRIDGE_YOLO`, because Verify blocks run in the collector's
environment and inherit whatever it carries.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../prd.md` — SHA-256 `25ea50e46e7716a5b7abc21119e0fd897059e06ac7f1aaebd4adbd7a4c21c207` |
| Specs | `specs/spec01.md` — SHA-256 `7757675c10477c82c2990f0c703354804f409c7f0aa5e7f947936464faa1de92` |
| Material contracts/dependencies | `.state/loop/outbound-call-does-not-block/analyst-1.md` — SHA-256 `4b33620a4239409e50c99db761c35c89c5766636c1a1ab6e91cbcb30e630d73b`; `cartridge.ctg` at `ab2383a` and `2ea1aae` (`src/node/mod.rs:48-52` `EITHER`, `src/transport/cartridge.rs:976-980`, `.cartridge/tests/unit/src/tests/host.rs`); `prd.ctg/src/lifecycle.ts:64-101` (Verify engine); `prd.ctg/src/planner.ts:39` (`complexity`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The spec honours Option A exactly: step 1 is a test, steps 2 and 3 are comments, step 4 is two documentation sentences. No host behaviour changes — confirmed by reading every step, and negatively by the mutant work, where the only code edit that moved the gate was one I made, not one the spec proposes. Its value claim is that the yieldable branch of `EITHER` has no test of its own, and that is measured, not argued: under the mutant, at both bases and in both environments, exactly one of the 17 selected tests failed — the new one — while the sibling the spec names as insufficient, `tests::host::a_node_serves_other_events_while_a_handler_waits`, stayed green every time. Deduction 2: the spec also claims `host.rs:296 a_call_that_comes_back_into_its_sender_is_answered` stays green under the mutant. It still exists at that line at `2ea1aae`, but it is not in the gate's selection and I did not run it under the mutant, so that half of the coverage argument remains the spec's assertion rather than a measurement. |
| Ownership and reuse | 18 | `footprint:` in the spec is byte-identical to the PRD's five paths (`diff` of both lists: no output). The justification for moving the test out of the two originally declared files is checked and correct: `src/lib.rs:15-17` mounts the suite by `#[path = "../.cartridge/tests/unit/src/tests/mod.rs"]` and the `host.rs:11-58` helpers are private to `crate::tests`, so the spec reuses the existing harness instead of duplicating about fifty lines of it. `complexity: 1` is a valid positive number for `planner.ts:39`, where the analyst's draft `complexity: S` would have been discarded as NaN. Deduction 2: step 4 invokes "the cartridge README rule" to justify pairing `src/node/README.md` with `.cartridge/help.md`, but that rule names the cartridge's own `README.md`. Leaving `cartridge.ctg/README.md` alone is the right call — nothing about behaviour or surface changes — but the rule cited is not the rule applied. |
| Dependencies and implementable slices | 15 | One spec, one complexity unit, no `cartridge.json` surface, setting, need or event touched. The absence of `--locked` is correct and justified: no manifest is touched. Downstream work (the mcp trampoline, the vendored `base.rs` in `agent.ctg` and `router.ctg`) is named as out of scope and left to its own PRDs, and the post-integration gates are a note rather than a box, which is the right shape. Deduction 5: the spec pins itself to "Base: cartridge.ctg `beb8213`" and treats its Verify measurements as settled against that commit. The lane is cut from HEAD, not from the declared base, and HEAD moved eight commits while this round was running. Two of the five footprint paths moved with it: `.cartridge/help.md` gained the `tool.asp` line at `804a08b`, and `.cartridge/tests/unit/src/tests/host.rs` had two assertions rewritten for the same reason. Neither collides with this spec — I checked, and the two rewritten assertions are in `a_glob_in_needs_names_what_the_others_listen_to` (`host.rs:631`) and `two_cartridges_that_need_each_other_…` (`host.rs:657`), neither named by the gate, and the spec's new test asserts on no `tool.*` needs list at all, so it needs no `tool.asp` update. But a spec whose Verify evidence is bound to a commit eight behind HEAD, in a file two other PRDs are actively editing, is asserting more stability than it has. |
| Observable acceptance and baseline evidence | 14 | Acceptance is byte-identical to the PRD's three boxes with box 2 in its new mutant wording (`diff` of both `- [ ]` lists: no output). **The gate was executed by me, engine-faithfully** (`sh -eu -c` under the engine's `PRD_TEST_REPORT`/redirect wrapper from `lifecycle.ts:89`, cwd the clone root, `CARGO_TARGET_DIR` unset in the caller so the `:-` default applied, empty target dir), at both bases and in both environments, and it passed all four times: at `ab2383a`, exit **0**, `17 passed; 0 failed; 147 filtered out`; at `2ea1aae`, exit **0**, `17 passed; 0 failed; 158 filtered out` with `CARTRIDGE_YOLO=1` and the same counts under `env -u CARTRIDGE_YOLO`. It runs real tests, not zero, and the named `tests::host::` paths still resolve at the new base after `804a08b` touched that module — `a_node_serves_other_events_while_a_handler_waits` is present at `host.rs:670`. The analyst's `libtest` claim is **true**: three positional filters after `--` selected 2 `tests::host::` tests plus all 15 `transport::cartridge::tests`, so they are ORed. All five `pass:` names appear as `test <path>::<name> ... ok` and each matches the engine's `p.endsWith('::' + name)` rule. No inert guard anywhere: the blocks contain no `! grep`, no `test -n "$X" && ...`, no custom conditional at all — they propagate cargo's exit status. Nothing self-curing: the only bespoke failure message, `the second event did not run while the first was parked: {waited:?}`, names the property and a measured duration and enumerates no token that would satisfy it. Nothing self-referential: `assert_eq!(answer, Some(json!("quick")))` compares against a literal the Lua listener returns, not a value the test computed, and the two `!relay.is_finished()` guards do stop the degenerate-fast-provider tautology — proved by the mutant, not asserted. Deduction 3: box 3 says "the transport suite stays green", but the gate's filter is `transport::cartridge::tests`, 15 of the 56 tests under `transport::`; `transport::rpc::tests` and five `transport::typed::*` modules are uncovered. Measured at `2ea1aae`: `cargo test --lib -- --test-threads=1 transport::` is exit 0, `56 passed; 0 failed`, 2.2 s, so the widening costs two seconds. Deduction 3: the spec's `## Denied worlds` states as measured fact that "Twelve tests already fail at `beb8213` in a pristine clone", names them, and makes that the justification for scoping every cargo invocation by filter. **That is false.** The twelve are an artefact of an inherited `CARTRIDGE_YOLO=1`, which the analyst's session and mine both carried. At `ab2383a`: as-is exit 101, `152 passed; 12 failed`; under `env -u CARTRIDGE_YOLO` exit **0**, `164 passed; 0 failed`. At `2ea1aae`: as-is exit 101, `163 passed; 12 failed`; clean exit **0**, `175 passed; 0 failed`. The base is all green and `cargo test --lib` bare was never a denied gate for the reason given. |
| Failure, recovery and compatibility | 16 | The gate is environment-independent where it counts, which is the question that mattered most: the mutant turns the new test red in **eight of eight runs across both bases and both environments**, always exit 101, always with the new test as the only failure. It is not measuring `CARTRIDGE_YOLO`. Both build commands carry `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/outbound-node-verify}"` — a `:-` default, never `${VAR:?}`, so neither pass aborts on an unset variable, and pass 2 stays clear of the live daemon's `target/debug`. No block writes inside the footprint: after every run above, `git status --porcelain` in each clone showed only ` M .cartridge/tests/unit/src/tests/host.rs`. No `cd`; all paths relative to the repo root. `## Denied worlds` correctly refuses to put the mutant in a block and hands it to the diff reviewer. Deduction 2: the timing table is stale and the trend is adverse. The `test` block cold was 20.9 s at `ab2383a` against the spec's stated 30 s, but **48.8 s at `2ea1aae`** — the `src/asp/` work added roughly 1500 lines and the suite grew from 164 to 175 tests in a day. Still inside the 120 s per-block limit, but the margin fell from 4× to 2.5× in eight commits, and nothing in the spec says the table must be re-measured. Cold `cargo clippy --all-targets`, which the spec never measured and which is the first cargo block a fresh lane runs, is 9.0 s on an empty target dir and 4.0 s warm — comfortable. Deduction 1: `## Denied worlds` pins one exact panic line for the diff reviewer to reproduce, and it reproduces about half the time; see finding 4. Deduction 1: the `cargo fmt` block is the only cargo command without the isolated `CARGO_TARGET_DIR`; harmless because rustfmt compiles nothing, but it departs from the rule the spec template states for every cargo command. |
| Reviewer total | **81** / 100 | Below the 90 threshold. No blocking finding remains. |

Findings and concrete revisions:

1. **The spec's "twelve tests already fail at base" is an artefact of
   `CARTRIDGE_YOLO=1`, not a property of the tree.** Raised by the coordinator
   mid-round and probed at both bases. This session carries `CARTRIDGE_YOLO=1`
   (exported by `just launch claude --yolo`), so the analyst's measurements and
   my own first pass both inherited it; the host merges `yolo: true` into every
   cartridge declaring that setting, which is exactly what the twelve tests
   assert against. Measured, same clone, same warm target dir: at `2ea1aae`
   as-is, exit 101, `163 passed; 12 failed`; under `env -u CARTRIDGE_YOLO`, exit
   **0**, `175 passed; 0 failed`. Same at `ab2383a` (12 failed / 164 passed
   clean). The twelve names under the variable are exactly the analyst's list —
   `lua::tests::each_file_is_evaluated_in_a_state_of_its_own`,
   `tests::host::a_restart_keeps_its_dependents_working`,
   `tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced`,
   `tests::settings::an_untrusted_project_config_is_refused_at_its_read` and
   eight `trust::tests::*`. Recommendation: rewrite the second half of
   `## Denied worlds`. The filtered gate should stay — it is the right choice on
   speed and precision, 8 s against 55 s — but its stated reason must become
   "these three filters are what boxes 2 and 3 need", not "the bare suite is red
   at base", which is untrue in a clean environment and will mislead the next
   reader of this board into scoping around a failure that is not there.
   Resolution: unresolved.

2. **Box 3's "transport suite" is under-covered by its gate.** Evidence:
   `cargo test --lib -- --list` reports `transport::rpc::tests` and five
   `transport::typed::*` modules beside `transport::cartridge::tests`; the gate
   selects only the last, 15 of 56. Recommendation: replace the third positional
   filter with `transport::`. Measured at `2ea1aae`: exit 0, `56 passed; 0
   failed`, 2.2 s, and none of the twelve yolo-sensitive tests lives under
   `transport::`, so the widening is free in both environments. While there, add
   `pass: a_listener_that_blocks_does_not_park_the_only_worker` — it is the test
   that actually locks box 3's first half ("the listener never runs on a tokio
   worker") and it is currently pinned only by the block's exit status.
   Resolution: unresolved.

3. **The declared base is eight commits stale and the timing table with it.**
   Evidence: spec says "Base: cartridge.ctg `beb8213`"; HEAD went through
   `ab2383a`, `3be9745`, `7af748a`, `804a08b`, `a2c5962`, `5980c7c`, `2ea1aae`
   to `324f36e` during this round, and the lane is cut from HEAD. Two footprint
   paths moved with it — `.cartridge/help.md` (+2) and
   `.cartridge/tests/unit/src/tests/host.rs` (+2/-2), both at `804a08b` for
   `tool.asp`. Neither collides: the two rewritten host assertions are in tests
   the gate does not name, and the spec's new test asserts on no `tool.*` needs
   list, so it needs no `tool.asp` update. But the cold `test` block went from
   20.9 s to 48.8 s across that window. Recommendation: restate the base as the
   current HEAD, re-measure the timing table there, and say in the spec that the
   table is a headroom claim against a growing suite rather than a constant.
   Resolution: unresolved.

4. **The mutant's pinned panic line does not reproduce reliably; the mutant
   itself does.** The `## Denied worlds` block quotes one exact line and exit
   101 as what the diff reviewer should see. Across eight mutant runs — two
   bases × two environments, plus repeats — every run was exit 101 with the new
   test as the only failure, but the message alternated between
   `the second event did not run while the first was parked: 900.952917ms /
   906.111125ms / 949.876791ms / 1.069105875s / 1.366903625s` and the earlier
   guard `the relay answered before the second event did`, independently of the
   environment (I saw each message both with and without `CARTRIDGE_YOLO`).
   Both are correct detections of the same serialization; the earlier guard
   fires when the relay's 1.2 s loop expires before the blocked `caller.quick`
   returns. Recommendation: state the property the reviewer must reproduce —
   "the new test fails, exit 101, no other selected test fails" — and keep the
   observed line as one example rather than the criterion. Resolution:
   unresolved, not blocking.

5. **Minor — the cartridge README rule is cited for the wrong file.** Step 4
   justifies `src/node/README.md` by "the cartridge README rule", which names the
   cartridge's own `README.md`. Leaving `cartridge.ctg/README.md` alone is right
   because no behaviour or surface changes; the sentence should say that rather
   than invoke a rule it is not applying. Resolution: unresolved, not blocking.

6. **Minor — the `cargo fmt` block omits the isolated `CARGO_TARGET_DIR`.**
   Harmless in fact (rustfmt builds nothing), but the spec template states the
   rule for every cargo command. Resolution: unresolved, not blocking.

Withdrawn during this round, recorded so it is not re-raised: I first scored
`cargo fmt --all --check` as a **blocking** finding, having measured it exit 1
in both passes at `ab2383a` because of an unformatted `src/cli/manual.rs`
outside this footprint (exit 0 at `beb8213`, exit 1 at `ab2383a` pristine and
with the live tree's dirty files overlaid). Commit `3be9745`, "Format the help
picker's tests so the check gate passes again", cured it. Re-measured: exit
**0** pristine at `2ea1aae`, exit **0** at `2ea1aae` with the spec's test
applied, and exit **0** in a pass-2 snapshot at `324f36e` with the live tree's
four dirty `.rs` files overlaid. The finding is withdrawn, not downgraded. It is
worth keeping in the record only as the sharpest evidence for finding 3: an
unpinned base made a Verify block red and then green again inside one review.

Not findings, recorded so a later round does not re-litigate them: the gate runs
17 real tests at both bases and matches nothing-and-exits-0 in no case;
`libtest` does OR multiple positional filters; the mutant turns the new test red
and nothing else red, at both bases and in both environments; no block writes
inside the footprint; no inert guard, no `${VAR:?}`, no `cd`, no
self-referential and no self-curing check; footprint and Acceptance match the
PRD's Decision exactly; nothing in the spec changes host behaviour, so Option A
is honoured.

Disposition: revise. The gate itself is the strongest part of this spec and it
survived every attack I made on it, including a base change mid-review. What
fails is the accuracy of the record around it — a false baseline census used as
a justification, a stale base, an under-covering filter for box 3 and an
unreproducible pinned message. All four are text changes plus one filter edit;
round 2 should pass comfortably.

Validation: all probing in throwaway clones under `$TMPDIR/review-outbound-r1`
(`base` at `ab2383a`, `b2` at `2ea1aae`, `p2` at `324f36e`), each a
`git clone --local` of `/Users/feb/dev/cartridge/cartridge.ctg`. The live
checkouts were not written to, no `prd` op was run and nothing was committed.

| command | base | env | exit | wall |
| --- | --- | --- | ---: | --- |
| `cargo fmt --all --check`, pristine | `beb8213` | — | 0 | <1 s |
| `cargo fmt --all --check`, pristine | `ab2383a` | — | **1** | <1 s (`src/cli/manual.rs` only) |
| `cargo fmt --all --check`, live dirty files overlaid | `ab2383a` | — | **1** | <1 s |
| `cargo fmt --all --check`, pristine | `2ea1aae` | — | **0** | <1 s |
| `cargo fmt --all --check`, spec test applied | `2ea1aae` | — | **0** | <1 s |
| `cargo fmt --all --check`, live dirty `.rs` overlaid (pass-2 snapshot) | `324f36e` | — | **0** | <1 s |
| `rustfmt --edition 2021 --check .cartridge/tests/unit/src/tests/host.rs` | `ab2383a` | — | 0 | <1 s |
| the spec's `test` block `run:` line, engine wrapper, **empty** target dir | `ab2383a` | yolo | **0** | **20.9 s** — `17 passed; 147 filtered out` |
| the same, warm | `ab2383a` | clean | **0** | 7.6 s — `17 passed` |
| the same, **empty** target dir | `2ea1aae` | yolo | **0** | **48.8 s** — `17 passed; 158 filtered out` |
| the same, warm | `2ea1aae` | clean | **0** | 8.6 s — `17 passed` |
| gate with the `EITHER` yieldable branch deleted (`src/node/mod.rs:50`) | `ab2383a` | yolo | **101** | 20.3 s — `16 passed; 1 failed` |
| the same mutant | `ab2383a` | clean | **101** | 11.3 s — `16 passed; 1 failed` |
| the same mutant | `2ea1aae` | yolo | **101** | 15.5 s — `16 passed; 1 failed` |
| the same mutant | `2ea1aae` | clean | **101** | 7.1 s — `16 passed; 1 failed` |
| mutant, single-name filter, two repeats each way | `ab2383a` | both | **101** ×4 | — |
| `cargo test --lib -- --test-threads=1` (bare) | `ab2383a` | yolo | 101 | 41 s — `152 passed; 12 failed` |
| `cargo test --lib -- --test-threads=1` (bare) | `ab2383a` | clean | **0** | 34 s — `164 passed; 0 failed` |
| `cargo test --lib -- --test-threads=1` (bare) | `2ea1aae` | yolo | 101 | 55 s — `163 passed; 12 failed` |
| `cargo test --lib -- --test-threads=1` (bare) | `2ea1aae` | clean | **0** | 56 s — `175 passed; 0 failed` |
| `cargo test --lib -- --test-threads=1 transport::` (proposed widening) | `2ea1aae` | yolo | 0 | 2.2 s — `56 passed; 0 failed` |
| `cargo clippy --all-targets`, **empty** target dir | `ab2383a` | — | 0 | **9.0 s** |
| `cargo clippy --all-targets`, warm | `2ea1aae` | — | 0 | 4.0 s |
| `cargo test --lib -- --list`, `transport::` modules enumerated | `ab2383a` | — | 0 | — |
| `git status --porcelain` after every run above | both | — | 0 | ` M .cartridge/tests/unit/src/tests/host.rs` only |

The mutant, executed rather than quoted. `src/node/mod.rs:50`,
`\tif yieldable() then return yielding(...) end`, deleted from the `EITHER`
chunk, nothing else changed. At `2ea1aae` under `env -u CARTRIDGE_YOLO`:

```
thread 'tests::host::a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge' panicked at src/../.cartridge/tests/unit/src/tests/host.rs:1464:5:
the second event did not run while the first was parked: 907.779667ms
test result: FAILED. 16 passed; 1 failed; 0 ignored; 0 measured; 158 filtered out; finished in 7.12s
```

Process exit **101**, and the same at `2ea1aae` with the variable
(`1.366903625s`) and at `ab2383a` both ways. `src/node/mod.rs` was restored from
a copy after each run and `git diff --stat` showed only the 50 added test lines.
The gate is behavioural, it bites, and it bites for the reason the spec claims.

Reviewer identity: fresh independent reviewer subagent (Claude Opus 5, 1M
context), session `18d6ba8cb545f358-2`, spawned for this round; not the spec's
author, and neither the spec nor `prd.md` was edited.
User rating: not required under delegation; none supplied.
User feedback/provenance: the PRD's `## Answer` (2026-09-19, Option A, "the host
does not change") and the `## Decision` block are settled inputs to this review,
not subjects of it.
Result: **FAIL** — 81/100, below the 90 threshold, with no blocking finding.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: bounded revision addressing findings 1–4 (correct the `## Denied
worlds` census and its justification, widen the transport filter and pin
`a_listener_that_blocks_does_not_park_the_only_worker`, restate the base at
current HEAD with a re-measured timing table, and replace the pinned mutant
message with the property), then round 2.

## Round 2 — 2026-09-19

Presented revision: `prd.ctg` at `ce911ede` with `prd.md` modified in the working
tree and `specs/` still untracked. `specs/spec01.md` is at revision 2 (SHA-256
`ac18b86e…`, was `7757675c…` in round 1). `prd.md` is byte-unchanged from round 1
(SHA-256 `25ea50e4…` both rounds), so the `## Answer` and `## Decision` this round
judges against are the same settled text, and the spec's author did not edit them.

Code base: `cartridge.ctg` HEAD is `324f36e35f1c15aad5e2e4e7e3fa8e9d869d7e33`,
checked by `git rev-parse HEAD` in the live checkout at the start of this round.
**That is exactly the base the spec declares**, so round 1's finding 3 is cured at
the moment of review rather than merely restated. The live checkout carries four
pre-existing dirty files that are not this PRD's — `README.md`, `src/cli/args.rs`,
`src/cli/host.rs`, `src/cli/mod.rs` — and no untracked paths.

Reviewing environment: `CARTRIDGE_YOLO=1` present, inherited from
`just launch claude --yolo`; no `CARTRIDGE_HOME`, no `CARTRIDGE_BIN`, no
`CARGO_TARGET_DIR`. Every measurement that could depend on the variable was taken
both as-is and under `env -u CARTRIDGE_YOLO`.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../prd.md` — SHA-256 `25ea50e46e7716a5b7abc21119e0fd897059e06ac7f1aaebd4adbd7a4c21c207` (unchanged from round 1) |
| Specs | `specs/spec01.md` — SHA-256 `ac18b86e1bf98ee897c281a6da382c8997c9627241582f39b22a66c75b9ef039` |
| Material contracts/dependencies | `.state/loop/outbound-call-does-not-block/analyst-1.md` — SHA-256 `b726595e5e0d3d60d3247c565a55517a863582b86dfad8080135e3dc55609291`; `cartridge.ctg` at `324f36e` (`src/node/mod.rs:48-52`, `src/transport/cartridge.rs:976-980`, `.cartridge/tests/unit/src/tests/host.rs`, `src/transport/tests/cartridge.rs:568`); `prd.ctg/src/lifecycle.ts` (Verify engine) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Option A is honoured: step 1 is a test, steps 2 and 3 are comments, step 4 is documentation sentences, and no step changes host behaviour. Confirmed negatively as well — across every run in this round the only edit that ever moved the gate was the mutant I applied myself, never anything the spec proposes. Round 1's deduction on this dimension was that the spec's claim about `a_call_that_comes_back_into_its_sender_is_answered` was asserted rather than measured. It is now measured, and the measurement refuted the claim; the spec was corrected to the truth rather than defended. See the self-correction paragraph below. Deduction 1: Acceptance box 1 says "a **native** cartridge's node", but the test the spec delivers exercises a *yielding Lua* caller (`cartridge.bail` from a listener), which is precisely the case that already works. The spec explains why — under Option A the non-yieldable native caller is fixed in `mcp.ctg`, not here — and the PRD's `## Decision` settled that box 1 stands as written, so this is not a scope error and is not relitigated. But nothing in the spec tells whoever eventually ticks box 1 how to read the word "native" against the evidence that will be offered for it. |
| Ownership and reuse | 20 | `footprint:` in the spec `diff`ed against the PRD's five paths: **no output**, identical. Round 1's finding 5 is fixed and the fix is accurate: step 4 now says `src/node/README.md` is paired with the help page because it is the node's own document, and states that the cartridge README rule names a cartridge's own top-level `README.md`, which is left alone because neither behaviour nor surface changes. Checked against the rule itself (`system/cartridge-readme-stays-current.md`): that reading is correct, and the spec's own update of `.cartridge/help.md` is owed to the user's Answer, not to that rule. The harness-reuse justification was re-verified line by line at `324f36e`: `src/lib.rs:16-18` is `#[cfg(test)]` / `#[path = "../.cartridge/tests/unit/src/tests/mod.rs"]` / `mod tests;` — the spec corrected this from round 1's `15-17` and the corrected span is the right one — and the helper `cartridge` is at `host.rs:11`. `complexity: 1` is a valid positive number. No deduction found. |
| Dependencies and implementable slices | 19 | One spec, one complexity unit, no `cartridge.json` surface, setting, need or event touched, and no `--locked` (correct, since no manifest is touched). Round 1's finding 3 is fixed: the base is restated as `324f36e`, which I independently confirmed is current HEAD, and the spec now names the eight-commit drift, the `804a08b` `tool.asp` change to the in-footprint `host.rs`, the two assertions it rewrote (`a_glob_in_needs_names_what_the_others_listen_to` and `two_cartridges_that_need_each_other_both_start_when_one_asks_with_a_question_mark`), why neither collides with this gate, and instructs an implementer to re-check HEAD before cutting the lane. Every cited line number was re-verified at this base and all of them hold: `EITHER` at `src/node/mod.rs:48-52` with the yieldable branch at line 50, the listener comment beginning at `src/transport/cartridge.rs:976`, `host.rs:296`, `host.rs:670`, `host.rs:11-58`, `src/transport/tests/cartridge.rs:568`. Deduction 1: the drift the spec now documents is mitigated by prose only. `host.rs` is in this footprint and is actively edited by other PRDs, so the same eight-commit problem can recur between this review and the lane; nothing in the spec gates on it, and nothing can. |
| Observable acceptance and baseline evidence | 19 | Acceptance `diff`ed against the PRD's three `- [ ]` lines: **no output**, identical, box 2 in its mutant wording. **The gate was executed by me, engine-faithfully** — `sh -eu -c`, cwd the clone root, `CARGO_TARGET_DIR` unset in the caller so the `:-` default applied, on a `target/` directory that did not exist. Cold, under `env -u CARTRIDGE_YOLO`: exit **0**, **35 s** wall, `58 passed; 0 failed; 0 ignored; 0 measured; 117 filtered out; finished in 11.56s`. The spec's cold claim is 47 s, so its headroom table is conservative against my machine rather than optimistic, and `58 + 117 = 175` accounts for the whole `--lib` suite. Round 1's finding 2 is fixed and the widening is real, not nominal: the module spread of the executed run is `tests::host` 2, `transport::cartridge::tests` 15, `transport::rpc::tests` 8, `transport::typed::bind_tests_unix` 9, `transport::typed::owner_tests_unix` 10, and four further `transport::typed::typed_tests*` modules totalling 11 — 56 under `transport::`, exactly as the spec enumerates, against 15 of 56 in round 1. **All six `pass:` names appear as `test <path>::<name> ... ok` in that run**, each matching the engine's last-`::`-segment rule, including the newly added `a_listener_that_blocks_does_not_park_the_only_worker` at `transport::cartridge::tests`. The filter selects 58 real tests and matches-nothing-and-exits-0 in no case. No inert guard: the Verify section contains no `! grep`, no `test -n "$X" && …`, no `&&` at all, and no custom conditional — the blocks propagate cargo's exit status. No `${VAR:?}` (`:?` appears zero times), no `cd`, all paths relative to the repo root. Nothing self-curing: the only bespoke failure messages are inside the test source, they name the property and a measured duration, and neither enumerates a token that would satisfy it. Nothing self-referential: `assert_eq!(answer, Some(json!("quick")))` compares against a literal the Lua listener returns rather than a value the test computed, and the two `!relay.is_finished()` guards stop the degenerate-fast-provider tautology — proved by the mutant below, not asserted. Deduction 1: the same box 1 wording gap noted above, carried here because box 1 is the box whose tick will rest on this evidence. |
| Failure, recovery and compatibility | 19 | Round 1's finding 4 is fixed, and this round produced the evidence that vindicates the fix. `## Denied worlds` no longer pins a panic line; it states the property — exit 101 with the new test the only failure among the selected set — and lists the observed lines as examples. **I executed the mutant five times and the property held five times out of five**, every run exit **101** with `test result: FAILED. 57 passed; 1 failed; 0 ignored; 0 measured; 117 filtered out` and `tests::host::a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge` as the sole name under `failures:`. Three runs were under `env -u CARTRIDGE_YOLO` and two with `CARTRIDGE_YOLO=1`; the mutant is not measuring that variable. The message did alternate, exactly as the spec now warns: four runs gave `the second event did not run while the first was parked:` with 1.231383833s, 1.133635917s, 1.58839275s and 1.184746583s, one gave 993.679167ms, and a sixth run over the three host names gave the earlier guard `the relay answered before the second event did`. Pinning any one line would have been wrong. Round 1's finding 6 is fixed: the `cargo fmt --all --check` block now carries the same `${CARGO_TARGET_DIR:-$PWD/target/outbound-node-verify}` default as the other two, verified in the text and by executing the block verbatim (exit **0**). Pass-2 shape checked directly, which is what flipped red and back in round 1: with the live checkout's four dirty `.rs` files overlaid on the clone, `cargo fmt --all --check` exit **0**, `cargo clippy --all-targets` exit **0** with zero warnings and zero errors, and the gate exit **0**, `58 passed; 0 failed`. No block writes inside the footprint: after every run `git status --porcelain` in the clone showed only the paths I placed there myself, and both builds write solely under `target/outbound-node-verify`, which pass 2 keeps clear of the live daemon's `target/debug`. Deduction 1: the cold gate's cost depends on a warm `kache` rustc cache. The spec discloses the dependency by name but does not bound what a cold `kache` would cost, and my own bare-suite measurement came in at 75 s against the spec's 58 s, so the absolute numbers in the table move with machine load in both directions. The spec's instruction to re-run the cold row when far from this base is the right mitigation and is present. |
| Reviewer total | **96** / 100 | At or above the 90 threshold, with no blocking finding. **PASS.** |

Round 1's six findings, each checked by execution rather than by reading the revision:

1. **The false twelve-failure census — genuinely fixed.** `## Denied worlds` now
   says "That claim was false and is withdrawn", attributes the twelve to the
   inherited `CARTRIDGE_YOLO=1`, tables both measurements and rejustifies the
   filter on two grounds that are true. I re-measured both numbers myself in a
   clone at `324f36e`, warm target dir. Under `env -u CARTRIDGE_YOLO`:
   `cargo test --lib -- --test-threads=1` exit **0**, `175 passed; 0 failed`,
   75 s. With `CARTRIDGE_YOLO=1`: exit **101**, `163 passed; 12 failed`, 84 s.
   The twelve names are exactly the set the spec and round 1 name —
   `lua::tests::each_file_is_evaluated_in_a_state_of_its_own`,
   `tests::host::a_restart_keeps_its_dependents_working`,
   `tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced`,
   `tests::settings::an_untrusted_project_config_is_refused_at_its_read` and
   eight `trust::tests::*`. The spec's claim that none of them lies under
   `transport::` or is one of the two selected `tests::host::` names was checked
   name by name against my own run log and is **true**, which is why the gate is
   green in both environments. Resolution: **resolved**.

2. **The stale base — genuinely fixed.** `git rev-parse HEAD` in
   `/Users/feb/dev/cartridge/cartridge.ctg` returns `324f36e`, the commit the
   spec declares, and HEAD did not move during this round. Every line number the
   spec cites was re-verified at that commit and all of them hold, including the
   `src/lib.rs:16-18` correction. Resolution: **resolved**.

3. **Box 3's under-covering filter — genuinely fixed.** The third positional
   filter is now `transport::`. Executed: 58 selected, 117 filtered out, 56 of
   the 58 under `transport::` spanning `transport::cartridge::tests`,
   `transport::rpc::tests` and five `transport::typed::*` modules. The sixth
   `pass:` name, `a_listener_that_blocks_does_not_park_the_only_worker`, is
   present in the block and appeared as `... ok` in the executed run.
   Resolution: **resolved**.

4. **The unreproducible pinned mutant message — genuinely fixed.** The property
   replaced the line, and the property reproduced five times out of five while
   the message itself alternated across my runs between both of the test's
   assertions. Resolution: **resolved**.

5. **The miscited README rule — genuinely fixed**, and the corrected sentence is
   an accurate reading of the rule. Resolution: **resolved**.

6. **The `cargo fmt` block's missing isolated `CARGO_TARGET_DIR` — genuinely
   fixed**, verified in the block text and by executing the block. Resolution:
   **resolved**.

**The self-correction, verified in both halves.** Round 1 flagged as unmeasured
the spec's claim that `tests::host::a_call_that_comes_back_into_its_sender_is_answered`
stays green under the mutant. The analyst measured it, found the claim false,
and rewrote the coverage argument rather than defending it. I ran the three host
names under the mutant and both halves hold:

```
test tests::host::a_call_that_comes_back_into_its_sender_is_answered ... FAILED
test tests::host::a_node_serves_other_events_while_a_handler_waits ... ok
test tests::host::a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge ... FAILED
test result: FAILED. 1 passed; 2 failed; 0 ignored; 0 measured; 172 filtered out; finished in 11.55s
```

`a_call_that_comes_back_into_its_sender_is_answered` fails at `host.rs:317:10`
with `left serves pong while its go handler waits: Elapsed(())`, which is the
self-deadlock to its own timeout the spec now describes, and it is a different
property from the one box 1 states.
`a_node_serves_other_events_while_a_handler_waits` stays **ok** under the mutant
in this run and in all five full-gate mutant runs, so the coverage argument now
rests on a sibling that genuinely does stay green. The spec's revised text says
exactly this. A revision that corrects its own claim against its own interest is
the strongest evidence in this round that the record can be trusted.

New findings this round, none blocking:

7. **Box 1 says "native" and the evidence will say "yielding Lua".** Box 1 reads
   "While one event on a **native** cartridge's node is parked in an outbound
   call…", and the test delivers two Lua cartridges where the caller yields
   through `cartridge.bail`. That is the case that already works; the native
   non-yieldable caller is what still serializes and is deferred to the `mcp.ctg`
   child PRD. The spec is internally consistent about this and the PRD's
   `## Decision` settled that box 1 stands as written, so this is not relitigated
   and is not blocking. Recommendation, for the implementer rather than for a
   further review round: add one sentence saying which half of box 1 this spec
   locks and which half the mcp child delivers, so the tick is not later read as
   a claim that the native path was fixed here. Resolution: open, not blocking.

8. **The timing assertion can fail spuriously under load, which is the safe
   direction.** `waited < Duration::from_millis(250)` is measured against a
   1.2 s busy loop on a machine that also runs the rest of the suite. A heavily
   loaded collector could push `caller.quick` past 250 ms and turn the gate red
   without any regression. `--test-threads=1` is the mitigation and the spec
   says so explicitly. Recorded because the failure direction is a false **red**,
   never a false **pass**, so it costs a rerun rather than a wrong tick.
   Resolution: open, not blocking.

Not findings, recorded so a later round does not re-litigate them: the gate
selects 58 real tests and all six `pass:` names resolve; `libtest` ORs multiple
positional filters; the mutant turns the new test red and nothing else red, in
both environments; the gate and the mutant are both environment-independent with
respect to `CARTRIDGE_YOLO`; no block writes inside the footprint; no inert
guard, no `${VAR:?}`, no `cd`, no `--locked`, nothing self-referential and
nothing self-curing; footprint and Acceptance match the PRD exactly; nothing in
the spec changes host behaviour, so Option A is honoured; and box 2 has no
Verify block by design, which the review method expressly permits with the diff
reviewer as the backstop.

Disposition: **keep**. Proceed to implementation. Both open findings are one
sentence of spec text and neither gates the lane; an implementer may fold
finding 7 in while writing the code without a further review round.

Validation: all probing in a throwaway `git clone --local` of
`/Users/feb/dev/cartridge/cartridge.ctg` at `$TMPDIR/review-outbound-r2/base`,
HEAD `324f36e`. The live checkouts were not written to, no `prd` op was run,
neither `prd.md` nor `specs/spec01.md` was edited, and nothing was committed.

| command | target dir | env | exit | wall |
| --- | --- | --- | ---: | --- |
| `git rev-parse HEAD` in the live `cartridge.ctg` | — | — | 0 | `324f36e35f1c15aad5e2e4e7e3fa8e9d869d7e33` |
| `diff` of the spec's `footprint:` against `prd.md`'s | — | — | 0 | no output |
| `diff` of the spec's `- [ ]` lines against `prd.md`'s | — | — | 0 | no output |
| `cargo fmt --all --check`, block verbatim, test applied | n/a | yolo | **0** | under 1 s |
| the `test` block's `run:` line, **no `target/` at all** | **empty** | clean | **0** | **35 s** — `58 passed; 0 failed; 117 filtered out` |
| the `test` block's `run:` line | warm | clean | **0** | 18 s — `58 passed; 0 failed` |
| the `test` block's `run:` line | warm | `CARTRIDGE_YOLO=1` | **0** | 10 s — `58 passed; 0 failed` |
| mutant, gate command, runs 1–3 | warm | clean | **101** ×3 | `57 passed; 1 failed` every time |
| mutant, gate command, runs 4–5 | warm | `CARTRIDGE_YOLO=1` | **101** ×2 | `57 passed; 1 failed` both times |
| mutant, the three `tests::host::` names | warm | clean | **101** | `1 passed; 2 failed` — see the self-correction above |
| `cargo clippy --all-targets`, block verbatim | warm | yolo | **0** | 7 s, zero warnings |
| `cargo test --lib -- --test-threads=1` bare | warm | clean | **0** | 75 s — `175 passed; 0 failed` |
| `cargo test --lib -- --test-threads=1` bare | warm | `CARTRIDGE_YOLO=1` | **101** | 84 s — `163 passed; 12 failed`, the same twelve names |
| `cargo fmt --all --check`, live dirty `.rs` overlaid (pass-2 shape) | n/a | yolo | **0** | under 1 s |
| `cargo clippy --all-targets`, pass-2 shape | warm | yolo | **0** | 5 s |
| the `test` block's `run:` line, pass-2 shape | warm | clean | **0** | 14 s — `58 passed; 0 failed` |
| `git status --porcelain` in the clone after every run | — | — | 0 | only paths placed there by this review |

The mutant, executed rather than quoted. Line 50 of `src/node/mod.rs`,
`\tif yieldable() then return yielding(...) end`, deleted from the `EITHER`
chunk, leaving exactly the four-line chunk the spec quotes in `## Denied
worlds`; `git diff --stat` showed `src/node/mod.rs | 1 -` and nothing else
beyond the 50 added test lines. Under `env -u CARTRIDGE_YOLO`:

```
thread 'tests::host::a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge' panicked at src/../.cartridge/tests/unit/src/tests/host.rs:1469:5:
the second event did not run while the first was parked: 1.231383833s
test result: FAILED. 57 passed; 1 failed; 0 ignored; 0 measured; 117 filtered out; finished in 16.97s
```

Process exit **101**, and the same shape in four further runs across both
environments. `src/node/mod.rs` was then restored from a copy and the gate
returned to exit **0**, `58 passed; 0 failed`. The gate is behavioural, it
bites, it bites for the reason the spec claims, and it bites on the new test
alone.

Reviewer identity: fresh independent reviewer subagent (Claude Opus 5, 1M
context), session `18d6ba8cb545f358-2`, spawned for round 2; not the spec's
author, not round 1's reviewer, and neither the spec nor `prd.md` was edited.
User rating: not required under delegation; none supplied.
User feedback/provenance: the PRD's `## Answer` (2026-09-19, Option A, "the host
does not change") and its `## Decision` (footprint widened to five paths, box 2
reworded to the executed mutant) are settled inputs to this review, not subjects
of it. Both were judged for compliance only, and the spec complies with both.
Result: **PASS** — 96/100, at or above the 90 threshold, with no blocking
finding and no unresolved finding from round 1.
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation. The spec is implementable as written;
findings 7 and 8 are recorded for the implementer and the diff reviewer and
require no further review round.
