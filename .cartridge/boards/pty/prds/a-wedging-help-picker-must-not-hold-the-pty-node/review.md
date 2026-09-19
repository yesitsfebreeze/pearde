# @pty/a-wedging-help-picker-must-not-hold-the-pty-node review history

Plan: `@pty/a-wedging-help-picker-must-not-hold-the-pty-node`, `prd.ctg/.cartridge/boards/pty/prds/a-wedging-help-picker-must-not-hold-the-pty-node/prd.md`.
Scope: one observable outcome. `cartridge help` run in the wrapped shell must not wedge the pty. Leaf PRD with one spec (`specs/spec01.md`); repo `cartridge.ctg`, footprint `src/cli/manual.rs`.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-19

Presented revision: PRD with `## Decision (2026-09-19, coordinator)` (option (a), host-only), spec01 as written by analyst-2. cartridge.ctg HEAD `beb8213d7236a228be2dca531e726cdad5d624ab` (only `src/asp/` untracked, outside the footprint). pty.ctg HEAD `9c64ee3`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `7c79117b2f37956ae8bf0e00a2216a88dce12ab5d7f12dbbebfe94eb0edcc93d` |
| Specs | `specs/spec01.md` sha256 `b3cb85e75670f8db50d6d5a56d8216dfb63875f5ef11c3f590cc7063c4aee71f` |
| Material contracts/dependencies | `cartridge.ctg/src/cli/manual.rs` at beb8213 sha256 `f5de0acf…77ad085`; `pty.ctg/src/tool.rs` at 9c64ee3 sha256 `1995a0e33516e61e0c9a9e01662893d2e06d1c97b55833bab3271157677ad085`; analyst-1.md `7bd26e3c…`, analyst-2.md `2c225eea…` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The outcome is real, small, and scoped to one file. Under option (a), however, the picker still opens for an agent, and the shell stays held until the agent sends `q`/Esc. Box 1 counts as met only under the coordinator's reading of "never blocks the next command". For `cartridge help <words>` (a search: `help()` passes `what` as the initial query), `q` stays filter text, so `q` does not exit on that path (−4). |
| Ownership and reuse | 18 | Correct repo and file. The test goes into the existing `mod tests`, with no new file or dependency. The line references are stale: the footer is at `manual.rs:878`, not 891; the view footer is at 925, not 938; the loop is at 743–773 (−2). |
| Dependencies and implementable slices | 17 | A single slice, which is right. Box 2 rests on pty.ctg behaviour with no named check and no `needs` link (−3). |
| Observable acceptance and baseline evidence | 11 | See blockers B1 and B2. The spec rewrites box 3 from "drives the picker path against a fake pty" to "drives `exits()` directly". Mutant `mut2` consumes `q` in `browse()` but passes both Verify blocks. Box 2 is claimed from a code reading only, and that reading conflicts with the PRD's own observed evidence (−9). |
| Failure, recovery and compatibility | 14 | `Key::Back` covers both `Esc` and `Left`, so after the fix `Left` quits the whole picker instead of stepping up a level. Esc mid-filter no longer clears the filter. The new list footer (`esc/ctrl-c quit`) leaves out `q`, the key this PRD is about (−6). |
| Reviewer total | 76 / 100 | |

Findings and concrete revisions:

- **B1 (blocking): the box 3 test does not drive the picker path and does not fail when the picker consumes the exit key.** `q_and_escape_exit_the_list_instead_of_being_consumed` tests only the pure `exits()` function. I built mutant `mut2`: the reference fix with `exits()` called as a match arm (`ref k if exits(k, &level.query) => return Ok(())`) placed after the `Key::Char(c) => level.query.push(c)` arm. In that mutant the picker consumes `q` as filter text, which is exactly the bug. Block 1 still exits 0 and block 2 still exits 0 (the greps match and the build passes, because `exits` is used). A second mutant that defines `exits()` but never calls it is caught, but only incidentally: `warnings = "deny"` turns the unused function into a build error in block 2's `cargo build`.
  Revision: move `browse()`'s key handling into a function that `browse()` itself calls. Either:
  - `fn step(manual: &Manual, stack: &mut Vec<Level>, k: Key, rows: usize) -> bool /*exit*/`, called by `browse()` after `key()?`, or
  - make the loop take a key source `impl FnMut() -> io::Result<Key>` with drawing split out.

  The test then feeds key sequences through that same code:
  - `[Char('q')]` exits at the root and at a pushed module level;
  - `[Char('s'), Char('q')]` does not exit, and the query becomes `"sq"`;
  - `[Char('s'), Back]` exits in one press from a pushed level.

  Record in the spec that a scripted key source replaces the "fake pty". This is the reviewer's accepted reading of box 3, given that `Screen::open`/`terminal::size` need a real tty. The spec's probe must show that `mut2`'s reordering turns the test red.
- **B2 (blocking): box 2 is claimed from existing behaviour with no named check, and the claim conflicts with the PRD evidence.** An Acceptance box can be satisfied by behaviour that already exists, but only if a named, executed check proves it. The spec has none: it says box 2 is "not re-verified here". pty.ctg's only tool unit test (`.cartridge/tests/unit/tool/tests.rs`) covers `whole_read`. The PRD's Evidence reports that the next shell-tool call returned "mcp did not answer in time" while the picker held the node. `pty.ctg/src/tool.rs` itself says "the node answers one event at a time", which suggests a read may wait behind an in-flight `run` for up to that call's `timeout_ms` (≤600000). The analysts did not reconcile this.
  Revision: do one of the following.
  - Name a pty.ctg test that already holds box 2 (none was found).
  - File a pty-owned leaf, linked through `needs`, with a test showing that a plain `tool.shell` read answers within its timeout while a raw-mode foreground program (the picker, or a stand-in) holds the pty. It should also explain or fix the observed "did not answer in time".
  - Have the coordinator re-scope box 2 explicitly in the PRD, with that rationale recorded.
- N1 (non-blocking): `Left` now quits the whole picker. Keep `Left` stepping up a level: split `Esc` from `Left` in `key()`, adding a `Key` variant in the same file, so `view()` still treats both as back. Otherwise, state the change in the Acceptance.
- N2 (non-blocking): the list footer and the no-terminal help line should name `q`, for example `q/esc quit`, since `q` is the key box 1 depends on.
- N3 (non-blocking): state in spec Acceptance that on the search path (`help <words>`, which starts with a non-empty query) `q` stays literal and `Esc` exits.
- N4 (non-blocking): fix the stale line numbers (878/925, loop at 743–773).
- UX rule "q quits only when the filter is empty": sound. It is the usual convention for filter-as-you-type lists, it keeps every query typeable, and it matches `view()`, where `q` already quits. It needs the N2 footer change to be discoverable.
- Docs: README.md:92 names no picker keys, so it needs no change. The only key descriptions are `manual.rs:341` (no-terminal overview), `:878` (list footer) and `:925` (`view()`, already accurate). The spec's two string edits cover the first two.

Disposition: revise (B1 in spec01; B2 through a pty-owned check or an explicit coordinator re-scope).

Validation: each run was a disposable `git clone --local` of cartridge.ctg under `…/scratchpad/reviewer-picker-1/{base,ref,mut,mut2}`, using `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`, with the per-clone `CARGO_TARGET_DIR=$PWD/target/help-picker-verify`. I rebuilt the reference fix from the spec's text, with the two string edits applied.

| Clone | Block 1 | Block 2 |
| --- | --- | --- |
| `base` (beb8213) | exit 1: "the exit-key test did not run" | exit 1: `fn exits` grep |
| `ref` | exit 0 (test ok, ~13 s cold) | exit 0 |
| `mut2` (q consumed before `exits`) | exit 0 | exit 0 (defeats both gates) |
| `mut` (`exits` never called) | not run | build exit 1, `function exits is never used` under `warnings = "deny"` |

I never ran `cartridge help`, nothing ran in the live checkout, and I did not use the live shell tool.

Reviewer identity: reviewer-picker-1 (independent review sub-agent, Opus 5).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (76/100).
Unresolved blocking findings: B1, B2.
Rounds used / remaining: 1 / 4.
Next action: make a bounded revision of spec01 for B1 and N1–N4, resolve B2 through the pty-owned check or a coordinator re-scope, then run round 2.

## Round 2 — 2026-09-19

Presented revision: the PRD with `## Decision` and `## Box 2 moved out`, and spec01 revision 2 (analyst-3). cartridge.ctg HEAD `beb8213d7236a228be2dca531e726cdad5d624ab`; `src/asp/` is untracked and outside the footprint. The reference is analyst-3's `analyst-picker/reference` tree diff, which this reviewer extracted as `reviewer-picker-2/reference.patch` and read line by line against the spec text.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `bc99f3701b89313f6a477e881e58d84443fa7a83289aad13816fea99106d511b` |
| Specs | `specs/spec01.md` sha256 `41072cb077e22433ff106b8a4b5ce94318f2e8e450ab29fcdcdfecb1d3a969b3` |
| Material contracts/dependencies | `cartridge.ctg/src/cli/manual.rs` at beb8213 sha256 `f5de0acfa5fa3e475000497c25bfabb0e4b8f7089b0f375f7034c22c2d5251b0`; reference.patch sha256 `6dc0a4d77be4a83d7b3157edf597f83aa1170b9c593fffe625ebaa0fc6fc9bde`; analyst-3.md sha256 `b8f851a006e3fdd1b970d9797f958493574b2436e1518cafebfcdafedb9b0ba6`; `@pty/a-shell-read-answers-while-a-foreground-program-holds-the-pty` (state open, repo pty.ctg) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | A single Esc now ends the list from any depth and any filter state, and a single `q` ends it when the filter is empty. That is enough for an agent to release the node. The search path, where `q` stays literal, is now stated. Under option (a) the picker still opens in the wrapped shell, and the agent must still send a key (−2; accepted by the coordinator, and (b) is noted as future work). |
| Ownership and reuse | 19 | One file, the existing `mod tests`, no new dependency, and the `run()` seam is the loop `browse()` really calls. The line references are now correct (723, 743–773, 878, 925). The spec's test code is not rustfmt-clean: `cargo fmt --all --check` reports a diff at the reference's `manual.rs:1050`, so the implementer must run `just fmt` (−1). |
| Dependencies and implementable slices | 19 | B2 is resolved: box 2 now lives in the filed `@pty/a-shell-read-answers-while-a-foreground-program-holds-the-pty` (pty.ctg, open). This PRD no longer depends on it, and the spec now points to it instead of claiming it. Nothing is left in this PRD that needs pty.ctg. The PRD's Acceptance still reads "fake pty", and only the spec records the scripted-key reading (−1). |
| Observable acceptance and baseline evidence | 16 | B1 is fixed. `scripted_keys_drive_the_real_list_loop` calls `run()` itself. Round 1's `mut2` now fails block 1 (`left: "q"`, `right: ""`). A natural "Esc needs >1 press" mutant (`mutescA`: Esc routed into the old `Back` arms) fails too (`esc must exit before appending anything of its own`, `left: ""`, `right: "s"`). A depth-dependent mutant survives, though. `mutescB` makes Esc act as `Back` whenever `level.address` is non-empty, so from `memo` Esc steps up and a second Esc exits, which is the PRD's own "Escape returned to the list" shape. That mutant passes block 1 and block 2 (exit 0/0). The cause is `run_keys`' fallback `unwrap_or(Key::Quit)`, which exits any loop that asks for more keys, so only the query text can tell the fixed loop from the broken one. No Esc case runs below the root (−3). Case 2's message says "a pushed module level", but `start = "memo"` is `stack[0]`, not a pushed level (−1). |
| Failure, recovery and compatibility | 19 | `Left` still decodes to `Key::Back`, and the `Back` arms are untouched. This reviewer confirmed that by reading the diff; no test covers it. `view()` maps `Exit` to back, which is unchanged behaviour. Both key descriptions (`:341` and the list footer) now name `q`. All 22 `--bin cartridge` tests pass on the reference, including `addresses_resolve_and_search_lands_in_the_section`. `cargo clippy --bin cartridge --tests` is clean. The cost is the fmt drift already counted above (−1). |
| Reviewer total | 91 / 100 | |

Findings and concrete revisions:

- B1 (round 1): resolved. The test drives the real loop through a scripted key source, and `mut2` goes red.
- B2 (round 1): resolved by the move, which the coordinator recorded in the PRD. The new pty-owned PRD exists and states the "did not answer in time" evidence.
- N-A (non-blocking, gate ceiling): the one-press Esc claim is only partly gated. `mutescB`, where Esc takes one press at the root but steps up below it, defeats both blocks. Under review-plan step 4, round 1 was the round spent designing this gate. The defeat is therefore recorded here as the ceiling, and the backstop is the diff reading: `exits()` runs before the match on every iteration, whatever `stack`/`address` is, and it returns true for `Key::Exit` unconditionally. Recommended cheap hardening, which the implementer should do: make the scripted source return `Err` when it runs out of keys instead of `Key::Quit`, and assert `result.is_ok()` so the loop must exit on the scripted keys themselves. Then add `run_keys(&manual, "memo", &[Key::Exit])` plus a genuinely pushed level (`[Key::Open, Key::Exit]` from the root, which pushes `memo`). The third case already ends in an explicit `Key::Quit`, so it keeps working.
- N-B (non-blocking): rename case 2's message, or push the level for real as above.
- N-C (non-blocking): run `just fmt`. The spec's code blocks are not rustfmt-shaped, and `just check` runs `cargo fmt --all --check`.
- N-D (non-blocking): optionally, one scripted case showing that `Key::Back` at a pushed level pops instead of exiting, so Left's navigation has a test and not only a reading.

Disposition: keep, and proceed to implementation with N-A–N-C folded into the change.

Validation: each run was a disposable `git clone --local` of cartridge.ctg under `…/scratchpad/reviewer-picker-2/{base,ref,mut2,mutescA,mutescB}`, run through `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "<spec block verbatim>"` with cwd set to the clone root and `CARGO_TARGET_DIR=$PWD/target/help-picker-verify`. The whole matrix took about 75 s; no block came near 120 s.

| Clone | Block 1 | Block 2 |
| --- | --- | --- |
| `base` (beb8213) | exit 1 (test did not run / does not compile) | exit 1 (grep) |
| `ref` (analyst-3 reference) | exit 0 (both tests ok) | exit 0 |
| `mut2` (`exits` demoted to an arm after `Key::Char`) | exit 1: `scripted_keys…` left `"q"` right `""` | exit 0 |
| `mutescA` (Esc routed into the old `Back` arms) | exit 1 (truth-table test); running `scripted_keys…` alone also FAILED, left `""` right `"s"` | exit 1 (grep) |
| `mutescB` (Esc acts as `Back` below root) | exit 0 (survives) | exit 0 (survives) |

Extra checks on `ref`: `cargo test --bin cartridge` passed 22/22. `cargo clippy --bin cartridge --tests` gave no warnings. `cargo fmt --all --check` reported a diff, in the test code only.

This reviewer never ran `cartridge help`, wrote nothing in the live checkout, and ran no `prd` transition.

Reviewer identity: reviewer-picker-2 (independent review sub-agent, Opus 5).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: PASS (91/100).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation. The implementer folds in N-A (the scripted source errors when it runs out of keys, plus Esc cases below the root) and N-C (fmt). The verifier should rerun `mutescB` against the implemented tree and expect red.
