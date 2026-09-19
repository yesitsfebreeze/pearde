# @sessions/file-drift-awareness review history

Plan: `@sessions/file-drift-awareness`, `prd.ctg/.cartridge/boards/sessions/prds/file-drift-awareness/prd.md`.
Scope: a file changed outside the session is named before it is trusted; executable leaf on the `sessions` board.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-19

Presented revision: `sessions.ctg` HEAD `b42aff29360d7699d34f924bf9ec23a2741e9094`, clean working tree. Planning records dirty in the shared `cartridge` checkout; no source file dirty in `sessions.ctg`.

| Input | Content digest |
| --- | --- |
| Plan | `prds/file-drift-awareness/prd.md` — `c22c51722892adf88ec46dcf187670fb27ec47c0f7c16103331f0116e9b2ac71` |
| Specs | `prds/file-drift-awareness/specs/spec01.md` — `9a032d9ec66894de639ea62ea4e9740670dc941f3c2330fbdfaae002e18400e3` |
| Material contracts/dependencies | `sessions.ctg` @ `b42aff2` (`src/lib.rs`, `src/changes.rs`, `cartridge.json`, `Cargo.toml`, `.gitignore`); `fs.ctg/src/lib.rs:84-96`, `fs.ctg/src/service.rs:346-352,561`; `harness.ctg/src/lib.rs:349-400`; `prd.ctg/src/lifecycle.ts:67-102,111` (verify engine) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 13 | The outcome is real and correctly confined to one cartridge. Deduction: the slice is inert in the live composition. `sessions {op:"touch"}` (`src/lib.rs:716-721`) has no caller — confirmed across the composition; `fs.ctg`'s only `sessions` call is `record_changes` (`fs.ctg/src/lib.rs:84-96`), fired only when `outcome.evidence` is `Some` (`fs.ctg/src/service.rs:346-352`), i.e. on writes. The only live populator of `Session.files` is `changes::append` (`src/changes.rs:134`). After this spec lands, `stamps` holds only files the session **wrote**, freshly re-stamped, so `drift` can only report an external edit to a file this session itself wrote. The PRD's headline — a file *read* again from a stale belief — is delivered by nothing in the repository. |
| Ownership and reuse | 18 | Right cartridge, no sibling file in the footprint, the `fs`/`harness` work correctly excluded. Reuses `change_record::Version`'s tagging shape, the existing `Dir`/`setup()` pattern (`change_records_tests.rs:3-27`), and the existing `files` record rather than a second one. Correctly adds no `limits.*` key. `README.md`, `.cartridge/help.md` and `cartridge.json` all in the footprint, per `cartridge-readme-stays-current`. Small deduction: no existing snapshot-compat fixture is identified or reused (see dimension 5). |
| Dependencies and implementable slices | 14 | Steps 1–9 are concrete, ordered and file:line anchored; the two cross-cartridge consumers are identified accurately, including the `build_system` append-after-render tail (`harness.ctg/src/lib.rs:385-400`) that keeps the cached prompt prefix fixed. Deduction: those consumers exist only as prose in the spec's Boundary section. The PRD has no `needs`, no children, and `grep -rl file-drift prd.ctg/.cartridge/boards/` finds no follow-on PRD on the `fs` or `harness` boards. The slice has no recorded successor, and neither PRD nor spec states which acceptance boxes this slice cannot demonstrate end to end. |
| Observable acceptance and baseline evidence | 10 | Five pinned test names is the right instrument (`lifecycle.ts:97-99` matches a name exactly or as the last `::` segment, so a rename, deletion or `#[ignore]` fails collection), and the determinism choice — mutate length as well as content, so `(mtime_ns, len)` differs whatever the clock did — correctly avoids a sleep in an mtime feature. Three of the five tests are real. Deductions: the self-write test is vacuous (B1); the stamp test has no specified assertion (F4); block 3 asserts a compatibility claim it does not test (B2). |
| Failure, recovery and compatibility | 11 | Forward compatibility is handled (`#[serde(default)]`). Deductions: backward compatibility is broken and unstated (B2); the sweep is unbounded (F5); a transient stat failure produces a false "gone" then a false "changed" (F7); the block-timing fallback lives only in the analyst report, not in the spec (F6). The Denied worlds section is a genuine strength, but one of its five entries is false — see B1. |
| Reviewer total | 66 / 100 | Below the 90 threshold; two blocking findings. |

Findings and concrete revisions:

- **B1 (blocking) — the self-write test is vacuous.** `specs/spec01.md:150-153` and `:165-166`. The test drives `record_changes` for a path and asserts `drift` answers a null report, but never stamps that path first. `sweep` iterates `stamps` keys only (`spec01.md:80-86`), so a path that was never stamped can never be reported. The test therefore passes on a tree where Step 6 (`spec01.md:118-123`) was never written. The Denied-worlds entry at `spec01.md:242-243` ("`record_changes` left the pre-write stamp in place") describes a pre-write stamp the specified test never creates. The PRD's third acceptance box — one of the three the brief names as easy to fake — is ungated. Recommendation: the test must `touch` the path so it is stamped, then change the file's bytes **and** length, then `record_changes` for that path, then assert the null report; and a sibling assertion must show the same sequence *without* `record_changes` reports the path in `changed`, so the null is attributable to Step 6 and not to an empty map. Resolution: unresolved.
- **B2 (blocking) — the compatibility claim is one-way and its Verify block does not test it.** `specs/spec01.md:100-103` and `:229-235`. `Session` is `#[serde(deny_unknown_fields)]` (`src/lib.rs:60`), so a snapshot carrying `stamps` is rejected by any binary without the field; `decode_snapshot` (`src/lib.rs:314-315`) turns that into a `diagnostics` entry (`src/lib.rs:302-303`), and `get` then refuses the session outright (`src/lib.rs:570-577`). `skip_serializing_if` protects only sessions that never stamped, and Step 6 stamps on every `record_changes`, so every actively-written session stamps. A rollback of the sessions dylib makes every active session unloadable — silently, as a diagnostic rather than an error at the call site. Verify block 3 proves neither direction: it runs the whole existing 92-test suite, every session in which is created by the new binary. Recommendation: pin a named test that decodes a literal pre-change snapshot (no `stamps` key) and a named test for the rollback direction, and let block 3 pin those names instead of running 92 unrelated tests; or state the one-way migration in the PRD's Proof-and-recovery boundary as an accepted cost with the `repair` path named. Resolution: unresolved.
- **F3 (major, non-blocking) — the feature is inert on arrival.** Evidence under dimension 1. The spec is honest about this at `spec01.md:52-68`, but honesty in a spec section is not a plan. Recommendation: create the two follow-on PRDs (`fs` board: `tool.read`'s success path calls `sessions {op:"touch"}`; `harness` board: a `drift` field on `Frame` appended in the `build_system` tail) with `needs: [@sessions/file-drift-awareness]` before this collects, and add one sentence to the PRD's Proof-and-recovery section saying box 1 delivers a door, not a behaviour.
- **F4 (major, non-blocking) — the stamp test has no specified assertion.** `spec01.md:157-159` asks for "persisted in the snapshot, and `drift` sees it", but a touch-then-drift sequence answers null whether or not a stamp exists, so the test can be written green against an unstamped tree. Recommendation: pin the assertion — read `<id>.json` from the store directory and assert the `stamps` object names the path. The same weakness, smaller, applies to `nothing_changing_answers_no_report_at_all` (`spec01.md:169-171`): require at least one stamped, unmodified file, or the test is trivially green on an empty map.
- **F5 (moderate) — the sweep is unbounded.** `spec01.md:33-36` concludes no cap is needed because stamps are keyed by paths already in `files`, but `files` is itself uncapped, and `drift` re-stats every key on every call, synchronously, while holding the per-session gate (`src/lib.rs:1052-1053`). The `ponytail:` ceiling comment covers resolution, not cost. Recommendation: bound the sweep or state the cost as an accepted ceiling.
- **F6 (moderate) — block 3 costs more than it proves.** Measured in `sessions.ctg` at `b42aff2`: `cargo test --manifest-path Cargo.toml -p sessions --lib` in an isolated `CARGO_TARGET_DIR` exits **0** with **92 passed, 0 failed**, 54.38 s of test time and 57 s wall. Block 2 (`cargo fmt` + `cargo clippy --all-targets -- -D warnings`) took 2 s; a cold-target build took 4 s. Those small build numbers are an artefact of `rustc-wrapper = "kache"` in `~/.cargo/config.toml`; the analyst's "roughly two minutes" is the empty-cache figure, and on a cache-cold collector block 1 alone would approach the 120 s ceiling (`lifecycle.ts:93,111`). Block 3 duplicates block 1's build and spends 54 s on a claim it does not test. Recommendation: replace block 3 with the named compatibility tests from B2; if the full suite is kept, record the fallback (drop block 3, never weaken block 1) in the spec rather than only in the analyst report.
- **F7 (minor) — a transient stat failure produces two false reports.** `spec01.md:77-79` maps every `metadata` error to `Absent`. A write-temp-and-rename observed mid-flight, or a transient permission error, reports the path as **gone**, rewrites the stamp to `Absent`, and then reports it as **changed** on the next sweep. The prior art's `-1` sentinel had the same shape but never separated gone from changed, so it never produced the second report. Recommendation: distinguish `NotFound` from other `io::Error` kinds, or state the noise as accepted.

Credited as correct, verified in source, not deductions:

- Verify guards use `if grep -qn ...; then :; else ...; exit 1; fi` — correct under `set -e`, not the inert `!` or `a && b` forms; and no failure message names the token the implementer must add.
- No `cd` to an absolute checkout; all paths are repo-root relative. `sessions.ctg/Cargo.toml` declares its own `[workspace]` and has **no** sibling path dependency, so the lane pass builds standalone and the sibling-symlink hazard does not apply here.
- `target/` is gitignored (`sessions.ctg/.gitignore`) and outside the footprint, so it is a legal scratch root, and every cargo command sets an isolated `CARGO_TARGET_DIR`.
- The manifest's `op` property is an unconstrained `{"type":"string"}` (`cartridge.json:11-19`), so the event description really is the whole declared surface; `grep -c -i drift cartridge.json README.md .cartridge/help.md` returns 0 for all three today, so the three doc gates are not pre-satisfied.
- Isolation holds: the footprint contains no sibling cartridge's file, and the `fs`/`harness` work is correctly excluded.
- The `harness.ctg` boundary claim is accurate: `build_system` renders the template and then appends `frame.roster`, `frame.record`, `frame.notice` (`harness.ctg/src/lib.rs:380-400`), so a drift block in that tail leaves the cached prefix byte-identical.

Disposition: revise. Keep the design; fix the two gates and record the successors.

Validation, all in `/Users/feb/dev/cartridge/sessions.ctg` unless noted:

| command | exit | note |
| --- | ---: | --- |
| `CARGO_TARGET_DIR=/tmp/rev78-cold-target cargo test --manifest-path Cargo.toml -p sessions --lib` | 0 | 92 passed, 0 failed, 0 ignored; 54.38 s test time, 57 s wall |
| `CARGO_TARGET_DIR=/tmp/rev78-cold2 cargo test --manifest-path Cargo.toml -p sessions --lib --no-run` | 0 | 4 s from an empty target dir (`kache` wrapper warm) |
| `CARGO_TARGET_DIR=/tmp/rev78-cold2 cargo fmt --manifest-path Cargo.toml -p sessions -- --check` | 0 | block 2, part 1 |
| `CARGO_TARGET_DIR=/tmp/rev78-cold2 cargo clippy --manifest-path Cargo.toml -p sessions --all-targets -- -D warnings` | 0 | block 2 total 2 s |
| `grep -c -i drift cartridge.json README.md .cartridge/help.md` | 0 | 0 matches in each; the doc gates are meaningful |
| `rg -n '\.files' src/ .cartridge/` (cwd `sessions.ctg`) | 0 | writes only at `src/changes.rs:134` and `src/lib.rs:719` |

No `prd` state operation was run, no source file was modified, `prd.md` was not touched, nothing was staged or committed.

Reviewer identity: reviewer agent, coordinator-78 session.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: B1 (`specs/spec01.md:150-153,165-166,242-243`); B2 (`specs/spec01.md:100-103,229-235`).
Rounds used / remaining: 1 / 4.
Next action: bounded revision of `spec01.md` addressing B1 and B2, plus F3's two follow-on records, then round 2.

## Round 2 — 2026-09-19

Presented revision: `sessions.ctg` HEAD `b42aff29360d7699d34f924bf9ec23a2741e9094`, working tree clean (`git status --porcelain` empty). `spec01.md` revised in place; `prd.md` unchanged from round 1.

| Input | Content digest |
| --- | --- |
| Plan | `prds/file-drift-awareness/prd.md` — `c22c51722892adf88ec46dcf187670fb27ec47c0f7c16103331f0116e9b2ac71` (unchanged) |
| Specs | `prds/file-drift-awareness/specs/spec01.md` — `58aeb48031dd8c63a120790d3f74328057c6d7cf501a2011bcc7b376078b242c` |
| Material contracts/dependencies | `sessions.ctg` @ `b42aff2` (`src/lib.rs:59-85,261-348,413-461,478-495,607,642-740,985-1131`, `src/changes.rs:120-140`, `src/mapping.rs:352-361`, `.cartridge/tests/unit/main/change_records_tests.rs:1-35`); `fs.ctg/src/lib.rs:85-96`, `fs.ctg/src/service.rs:561`, `fs.ctg/src/provenance.rs`; `harness.ctg/src/lib.rs:349,387-406,1206`; `@fs/a-read-stamps-the-file-it-returned` and `@harness/the-turn-names-the-files-that-changed-underneath-it` (both exist, both declare `needs: ["@sessions/file-drift-awareness"]`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 15 | Outcome real, scope correctly confined to one cartridge, and the slice is now the recorded unblocker for two scheduled dependents rather than an orphan. Deduction: the spec's own capability table marks PRD box 3 "**Yes, fully and live** … exercised by the running system the moment it ships" (`spec01.md:25`). That is false — `drift` has no caller either, so nothing exercises the rule on landing. The whole live effect of collecting this is one extra `std::fs::metadata` per recorded write, observable to nobody. See B3. |
| Ownership and reuse | 17 | Right cartridge, no sibling file in the footprint, reuses `change_record::Version`'s tagging shape, the `Dir`/`setup()` disposable-directory pattern, and the existing `files` record; adds no `limits.*` key; all three doc surfaces in the footprint. Deduction: Step 7 (`spec01.md:190-192`) reasons about `"delete"` dropping stamps but never about `Store::install` (`src/lib.rs:340-348`), which replaces the whole `Session` from a decoded snapshot and is called from three live paths. See B5. |
| Dependencies and implementable slices | 15 | Steps 1–10 are concrete, ordered and anchored, and **every** file:line the spec cites was checked and is correct: `src/lib.rs:59-60` (`Default` + `deny_unknown_fields`), `:295` (non-`json` entries skipped), `:413`, `:528`, `:716-721`, `:1128`; `src/changes.rs:127,135`; `fs.ctg/src/service.rs:561`; `fs.ctg/src/lib.rs:86-92`; `harness.ctg/src/lib.rs:385-395` (the append-after-render tail is `:387-406`, so the cited range is accurate in substance) and `:1206`. Round 1's F3 record half is resolved: both follow-on PRDs exist on their owner boards with `needs` pointing back here, and the `@harness` one is already claimed and analyzing. Deduction: the key contract between the two stamp producers is unstated (F8) — `record_changes` stamps the absolute, `Evidence::validate`-normalized `evidence.target.path`, while `"touch"` inserts an arbitrary unvalidated string (`src/lib.rs:719`) and `observe` would stat it as given, against the host process cwd. Two keys for one file makes box 3 fail the moment `@fs` lands. |
| Observable acceptance and baseline evidence | 13 | B1 is genuinely fixed: `a_file_the_session_wrote_is_not_named_as_drift` now stamps `w` and `o` by `touch` before rewriting both, so a missing Step 6 fails assertion one and a clear-all-stamps implementation fails assertion two. `nothing_changing_answers_no_report_at_all` now establishes its precondition (two stamped files) — round 1's F4 half fixed. `a_changed_file_is_named_apart_from_a_deleted_one` and `a_reported_change_is_not_reported_twice` both establish their preconditions. Deductions: the author's claim to have swept every test for the vacuous shape missed one — `a_file_never_read_is_not_named_when_it_changes` establishes nothing at all and passes on a stub (B4). `stamps_are_not_written_into_the_session_snapshot` leaves its decisive assertion in prose rather than pinning the key list (F9). Nothing separates "refresh the stamp" from "drop the stamp" on write or on report (F10). |
| Failure, recovery and compatibility | 11 | B2's *mechanism* is genuinely fixed and I verified it rather than took it: nothing new is emitted, so `deny_unknown_fields` (`src/lib.rs:60`) is now irrelevant rather than merely avoided; `Session` derives `Default` (`:59`), which is what `skip` needs on decode; and stamps ride the existing clone-mutate-publish path untouched — `sessions()` clones at `:528`, `publish_checked` installs with `*self = candidate` at `:461`, and `SharedStore::execute` builds its narrow candidate by cloning whole `Session` values (`:1065-1070`) and merges them back with `state.sessions.extend(candidate.sessions)` (`:1128`). No change to that machinery is required. `observe`'s three-way `Option<Stamp>` is a proper fix for F7. Deductions: the stated ceiling is false (B5); the prior-art defence is false — `file-touch-tracker.ts` is in-memory in a process whose *session* also dies with it, whereas here `files` persists across restarts and `stamps` do not, so the record keeps claiming knowledge the store has silently discarded; and round 1's F5 (the sweep re-stats every key synchronously under the per-session gate, `src/lib.rs:1052-1053`) is neither bounded nor recorded as an accepted ceiling. |
| Reviewer total | 71 / 100 | Below the 90 threshold; three blocking findings. |

Findings and concrete revisions:

- **B3 (blocking) — "fully and live" is false for box 3.** `spec01.md:25`, restated at `:276` and in the analyst report. `record_changes` is indeed called on every write (`fs.ctg/src/lib.rs:85-96`), so stamps will be written; but the rule "a file the session wrote is not reported as drifted" is only observable through `drift`, and `drift` has no caller in the composition either — the `@harness` row that would call it is a separate, unlanded PRD. Nothing in the running system exercises box 3 on landing. Recommendation: replace "Yes, fully and live" with "the mechanism, exercised only once `@harness` calls `drift`", and state plainly in the table's preamble that **no** box is observable on this footprint alone — boxes 3, 5 and 6 are proven by tests, not by the running system. Resolution: unresolved.
- **B4 (blocking) — a second vacuous test, in the pair introduced to cure B1.** `spec01.md:233-235`, Denied world at `:376-378`. `a_file_never_read_is_not_named_when_it_changes` creates a file, rewrites it, never `touch`es it, and asserts a null report — but the session it runs against has an **empty** `files` set and an **empty** `stamps` map, so no precondition is established. `fn drift(..) -> Ok((json!({"id":id,"report":Value::Null}), None))` passes it, as does an implementation that sweeps `files`, as does one that sweeps `stamps`; the three are indistinguishable here. Its Denied-worlds justification — "because a file the session only wrote would be reported as read-then-drifted" — is textually false: the test performs no write. This is the round-1 B1 defect class recurring, in a test the author added to fix B1 and after asserting the other tests had been swept for exactly this shape. Recommendation: either give the test the precondition its Denied world describes — `record_changes` a *different* path so `files` is non-empty while the path under test is unstamped — or delete the test and the false Denied-worlds entry and stop claiming the sweep-`files` world is gated. Note that under the specified design every path entering `files` is also stamped, so that denied world is close to unreachable and the honest move may be deletion. Resolution: unresolved.
- **B5 (blocking) — "the stamps live for the life of the host process" is false.** `spec01.md:120-124`. `Store::install` (`src/lib.rs:340-348`) does `self.sessions.insert(file.session.id.clone(), file.session)` with a `Session` decoded from disk, whose `#[serde(skip)]` map is `Default` — empty. It is called from three places that run while the host is up: `publish_checked`'s post-rename recovery (`src/lib.rs:443`), `repair_empty` (`src/lib.rs:488`), and `mapping::…` on the live `mapping`/`connect` ops (`src/mapping.rs:360`, routed at `src/lib.rs:1013`). Each silently zeroes that session's stamps with no diagnostic. The sentence is the load-bearing claim of the section rewritten to fix B2, and it is wrong about the design's own behaviour. Recommendation: either re-stamp every path in `files` inside `install` (and on `Store::load`, which also closes the restart hole cheaply and is the difference between "silent until the next read" and "silent forever", given `touch` has no caller), or enumerate the three call sites in the ceiling paragraph and drop the false prior-art analogy — there the session dies with the process; here the session record outlives it, so the store keeps a `files` list it can no longer reason about. Resolution: unresolved.
- **F8 (major, non-blocking) — the stamp key contract is unstated.** The two producers disagree in kind: `changes::append` supplies `evidence.target.path`, which `Evidence::validate` has already forced absolute and normalized (`src/change_record.rs:105-116`), while `"touch"` inserts whatever string the caller passed with no validation at all (`src/lib.rs:716-721`), and `drift::observe` would `metadata()` it as given — against the *host process* cwd, not the session's. A relative key silently stamps `Absent {}` or, worse, a different real file. Recommendation: state in Step 4 that `touch` rejects a non-absolute or non-normalized `file`, or that `observe` resolves against the session `cwd`; and add the requirement to the `@fs` need so the two producers key the same file identically.
- **F9 (moderate) — the compatibility gate's decisive assertion is prose.** `spec01.md:255-260`. The reload half (`Store::load`, empty `diagnostics`) cannot fail under either candidate design, because the same binary knows its own field; the whole gate therefore rests on "assert the session object carries no key beyond the ones an older binary knows". Written as a whitelist that is strong; written as `!obj.contains_key("stamps")` it is defeated by a rename. Recommendation: pin the whitelist explicitly — the exact key set `Session` serializes today.
- **F10 (moderate) — refresh and drop are indistinguishable.** In `a_file_the_session_wrote_is_not_named_as_drift`, an implementation that *removes* `w`'s stamp rather than refreshing it (Step 6) passes both assertions; in `a_reported_change_is_not_reported_twice`, an implementation that removes a path from `stamps` after reporting it rather than writing the new stamp back also passes. Both lazy implementations silently end drift awareness for that path forever. Recommendation: in each test, after the first assertion, change the file again and `drift` a second time, asserting it is named — that separates refresh from drop in one extra line per test.
- **F5 (moderate, carried from round 1, unaddressed) — the sweep is unbounded.** `drift` re-stats every stamped key synchronously while holding the per-session gate (`src/lib.rs:1052-1053`), and `files` is uncapped. The spec observes that stamps add no *new* unbounded collection (`spec01.md:91-93`), which is true and is not the finding. Recommendation: bound the sweep or record the per-call cost as an accepted ceiling in the spec.

Credited as correct, verified rather than accepted:

- The `#[serde(skip)]` design does what it claims about the snapshot, for the reasons given, and needs no change to the mutation machinery — traced through `:528`, `:413/:461`, `:1065-1070`, `:1128`.
- The removal of `cargo fmt` and `cargo clippy` from Verify is **right**. Measured here, `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=/tmp/rev2-target cargo test --manifest-path Cargo.toml -p sessions --lib` from a wiped target directory: exit **0**, **92 passed, 0 failed**, 49.04 s test time, **54.33 s wall** — the *whole* suite, comfortably inside the 120 s ceiling, and the gate as written filters to `drift_tests` so its run phase is near zero. The author's corrected reading of the round-1 "~2 minute" figure as a first-ever crates.io download is consistent with what I see; `just check sessions` is the coordinator's gate for fmt and clippy and is named in the PRD.
- The deleted persistence grep block was correctly deleted for the stated reason: `src/lib.rs` really does carry three legitimate `#[serde(default)]` fields at `:75`, `:77` and `:79`.
- Verify-block hygiene holds: no `cd` to an absolute checkout, repo-root-relative paths, an isolated `CARGO_TARGET_DIR` inside gitignored `target/` and outside the footprint, the `if grep -qn …; then :; else …; exit 1; fi` form (not the inert `!` or `a && b`), no `${VAR:?}` and no reliance on injected environment, and no failure message naming the token an implementer must add. The filtered command runs 0 tests and exits 0 on today's tree, so the gate fails on the `pass:` names rather than passing vacuously — confirmed by running it.
- The `@fs` and `@harness` needs are real, not prose: both PRDs exist, both declare `needs: ["@sessions/file-drift-awareness"]`, and the `@harness` one is claimed and analyzing.

Disposition: revise. The design is right and the two round-1 blockers are substantively addressed; three new blocking findings are prose and test corrections, none requiring a redesign.

Validation, `env -u CARTRIDGE_YOLO` in every form, cwd `/Users/feb/dev/cartridge/sessions.ctg` unless noted:

| command | exit | note |
| --- | ---: | --- |
| `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=/tmp/rev2-target cargo test --manifest-path Cargo.toml -p sessions --lib` | 0 | wiped target dir; 92 passed, 0 failed, 0 ignored; 49.04 s test time, **54.33 s wall** |
| `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=/tmp/rev2-target cargo test --manifest-path Cargo.toml -p sessions --lib drift_tests` | 0 | 0 passed, 92 filtered out — the gate fails today on its `pass:` names, not vacuously |
| `sed -n` / `grep -n` over `src/lib.rs`, `src/changes.rs`, `src/mapping.rs`, `.cartridge/tests/unit/main/change_records_tests.rs` | 0 | every cited line confirmed; `install` call sites at `:443`, `:488`, `mapping.rs:360` found |
| `grep -n` over `fs.ctg/src/{lib,service}.rs`, `harness.ctg/src/lib.rs` (cwd `/Users/feb/dev/cartridge`) | 0 | `service.rs:561`, `lib.rs:91`, `harness lib.rs:387`, `:1206` all exact |
| `grep -rln file-drift prd.ctg/.cartridge/boards/` (cwd `/Users/feb/dev/cartridge`) | 0 | both follow-on PRDs present with `needs` back to this row |

No `prd` state operation was run, no source file was modified, `prd.md` was not touched, nothing was staged or committed.

Reviewer identity: reviewer agent, coordinator-78 session.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: B3 (`specs/spec01.md:25,276`); B4 (`specs/spec01.md:233-235,376-378`); B5 (`specs/spec01.md:120-124`, against `sessions.ctg/src/lib.rs:340-348,443,488` and `src/mapping.rs:360`).
Rounds used / remaining: 2 / 3.
Next action: bounded revision of `spec01.md` for B3 (one table row and its preamble), B4 (one test's precondition or its deletion with the false Denied world) and B5 (re-stamp in `install`/`load`, or enumerate the three reset sites and drop the prior-art analogy), then round 3.

## Round 3 — 2026-09-19

Presented revision: `sessions.ctg` HEAD `b42aff29360d7699d34f924bf9ec23a2741e9094`, working tree clean. `spec01.md` revised in place; `prd.md` unchanged from round 1. This round changed only the spec and the analyst report, so the suite is still the round-1 baseline.

| Input | Content digest |
| --- | --- |
| Plan | `prds/file-drift-awareness/prd.md` — `c22c51722892adf88ec46dcf187670fb27ec47c0f7c16103331f0116e9b2ac71` (unchanged) |
| Specs | `prds/file-drift-awareness/specs/spec01.md` — `908347167c8c8e04445839bb0558797592c3e9f62e7e7e344ce3f1b36cb15fc5` |
| Material contracts/dependencies | `sessions.ctg` @ `b42aff2` (`src/lib.rs:59-85,290-348,425-500,1005-1013`, `src/changes.rs:118-142`, `src/mapping.rs:114,176,344-361`, `src/change_record.rs:100-116`, `src/limits.rs:19-76`, `cartridge.json`, `.cartridge/tests/unit/main/change_records_tests.rs:1-45`); every other `sessions`-board PRD (`state: done` or `deferred`, so no footprint collision); `@fs/a-read-stamps-the-file-it-returned`, `@harness/the-turn-names-the-files-that-changed-underneath-it` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | B3 is fully resolved and I verified the table against its own preamble: `spec01.md:19` now leads with "No box in this PRD is observable in the running composition on this footprint alone", and the box-3 row reads "observable only through `drift`, which has no caller. Proven by test, not by the running system." No row overclaims. Deduction: the slice is still inert on landing (correctly recorded, two scheduled consumers), and B7 below narrows the delivered value further than the spec states — the feature exists to name drift *during a live turn*, and a live `mapping`/`connect` op silently re-baselines it away. |
| Ownership and reuse | 17 | Right cartridge, no sibling file. The footprint growth to `src/change_record.rs` and `src/limits.rs` is justified by the fixes and collides with nothing: `file-drift-awareness` is the only `sessions`-board PRD not `done` or `deferred`, `src/limits.rs` is in no other footprint, and the seven other specs naming `src/change_record.rs` are all `done`. The footprint list matches what the steps touch, file for file. Step 1 promotes `normalized` rather than restating it — correct, and I confirmed `normalized` (`src/change_record.rs:105-116`) is the rule `Evidence::validate` already applies. `limits.stamps` follows the crate's own pattern; I counted **21** existing `limits.*` keys in `cartridge.json` and `Limits::declared` (`src/limits.rs:57-62`) reads them back out of the document, so the two-file edit is self-consistent and a mismatch panics in every unit test. Deductions: no step declares `mod drift;` in `src/lib.rs`, and `restamp` (Step 2) walks `files` without filtering through the `normalized` rule Step 1 exists to promote (F16). |
| Dependencies and implementable slices | 16 | B5's mechanism is real and I checked it rather than took it. `install` has **exactly four** callers: `src/lib.rs:299` (`Store::load`), `:443` (`publish_checked`'s post-rename recovery), `:488` (`repair_empty`), `src/mapping.rs:360` (`refresh_mapping_target`). The only other `install(` hit in the crate is `src/lib.rs:1174`, which is `crate::limits::install` — a different function. No fifth caller. The gating test does fail without a re-stamp: `Store::load` produces `stamps: Default` and `sweep` would answer null. Deductions: the borrow justification at `spec01.md:197` is **false** (F11, proven by compiling), and the one-line design alternative that removes B7 entirely is never considered. |
| Observable acceptance and baseline evidence | 12 | F9 is resolved and correct — I diffed the whitelist against `Session` (`src/lib.rs:59-85`): mandatory `id`, `name`, `cwd`, `buffers`, `files`, `agent`, `created`, `updated`, `revision`, `parent`, `transcript`; optional `change_log`, `mailbox_lineage`, `mailbox_cursor`. Exact match, and `parent`/`transcript` are correctly in the mandatory half. F10 is resolved: both tests carry the second-change line. B4's test and its false Denied world are gone. Deductions: **both** tests I attacked fell to a lazy implementation (B6, B8), and both are gates written to close a previous round's finding; the new `limits.stamps` cap has no executed test although its documented behaviour is a user-visible silence; `stamps_are_not_written_into_the_session_snapshot` passes unchanged on today's tree. |
| Failure, recovery and compatibility | 13 | The `#[serde(skip)]` compatibility argument is right and still holds. `observe`'s three-way `Option<Stamp>` and the skip-on-`None` sweep are correct and remain the right fix for round 1's F7. F5 is genuinely bounded now rather than merely recorded. The frozen report contract (`report: null`, `changed`/`gone` as two lists, nothing rendered in the null case) is the right shape and I raise **no objection** to it. Deductions: B7 — the stated ceiling is, for the third round running, incomplete about the code's own behaviour; F16; and the cap's silent partial is documented but unproven. |
| Reviewer total | 74 / 100 | Below the 90 threshold; three blocking findings. |

Findings and concrete revisions:

- **B6 (blocking) — the B5 gate does not gate B5's scope.** `spec01.md:134-141` (Step 5), restated at `:302-306`, `:341` and `:446-449`. All three passages claim the test covers all four `install` callers. It covers one. I wrote the lazy implementation: put the re-stamp in `Store::load`'s snapshot loop (`src/lib.rs:299`) — `Ok(file) => { let id = file.session.id.clone(); store.install(file); if let Some(s) = store.sessions.get_mut(&id) { drift::restamp(s); } }` — instead of inside `install`, and implement every other step verbatim. `a_reloaded_session_is_restamped_from_its_touched_files` **passes**, and all six siblings pass, while `publish_checked`'s recovery (`src/lib.rs:443`), `repair_empty` (`:488`) and `refresh_mapping_target` (`src/mapping.rs:360`) still zero the stamp map. The acceptance box at `:341` says "neither a reload nor a repair nor a mapping op" and only the reload is executed. Recommendation: pin an eighth test that drives the `repair` or `connect` op after a `touch` and asserts the stamp survives. `.cartridge/tests/unit/main/repair_tests.rs` and `mapping_tests.rs` already exist, so the fixture is available; the alternative — deleting "repair" and "mapping" from the acceptance box and naming the diff reviewer for them — is weaker and would leave the Denied world at `:446-449` false. Resolution: unresolved.
- **B7 (blocking) — the load-time re-stamp absorbs drift in the live window, and the stated cost omits that window.** `spec01.md:137-144`. The spec names two absorbed windows: "while the host was down" and "between the rename and the recovery decode". It omits the one that matters. `refresh_mapping_target` (`src/mapping.rs:344-361`) takes the per-session gate, reads `<id>.json` and calls `state.install(file)` on a session that is **already resident in memory**; it runs from `src/mapping.rs:114` and `:176`, on the live `mapping`/`connect` ops routed at `src/lib.rs:1011-1013`. With Step 5 as written, a `connect` mid-session re-baselines every stamp to current disk, so a file read at turn *n*, edited by a person at turn *n+1*, and `connect`ed at *n+2* is never named. `repair_empty` and the post-rename recovery have the same shape. This is not an unavoidable cost: `install` knows whether the session is already present. Carrying the resident session's stamps forward and re-stamping only when the id is genuinely new is the same one line of work, removes the live-window false negative completely, and leaves the cold-`Store::load` re-baseline — which *is* unavoidable — as the only absorbed window, exactly matching the sentence the spec already wrote. Recommendation: take that branch in Step 5 and keep the honesty paragraph for cold load only; or, if the spec keeps the unconditional re-stamp, the paragraph must name `mapping`/`connect` as a live absorbing op and say why the resident-session branch was rejected. Stating the cost is not enough while the statement is incomplete and the cheaper design is unconsidered. Resolution: unresolved.
- **B8 (blocking) — F8's contract is asserted in prose and gated only against the easy half.** `spec01.md:278-281` and the Denied world at `:463-466`. Step 4 requires `touch` to refuse a path that is not absolute **and** normalized by `change_record::normalized`; the test asserts only that a **relative** path is an error. I wrote the lazy implementation: guard with `Path::new(&file).is_absolute()` alone. The assertion passes, and `touch` then accepts `/work/../work/a` and `/work/./a` — absolute, not normalized, and rejected by `Evidence::validate` (`src/change_record.rs:105-116`). The two producers key the same file differently, which is precisely the failure the spec calls out as "box 3 fails the moment this lands", and every test here still passes. Recommendation: one more line in the same test — an absolute-but-unnormalized path is also refused. Resolution: unresolved.
- **F11 (major, non-blocking) — the borrow justification is false, and I proved it by compiling.** `spec01.md:194-199` says `restamp` cannot take `(&files, &mut stamps)` "because those two borrows of one `&mut Session` do not coexist and the workaround is a clone or a `mem::take`". The borrow checker splits disjoint field borrows. I built a crate with `pub fn restamp(files: &BTreeSet<String>, stamps: &mut BTreeMap<String,u64>)` and called it both as `restamp(&s.files, &mut s.stamps)` on a `&mut Session` and through `map.get_mut(id)`; `cargo build` finished clean in 0.85 s. The `&mut Session` signature is a fine choice — the *reason given for it* is wrong. This is the same defect class as round 2's B5 and round 1's B1: a load-bearing sentence about code the author had read, written from memory instead of from the compiler or the call site.
- **F12 (moderate) — the measured cost table understates, though its conclusion survives.** `spec01.md` reports 63.28 s test / 74 s wall for the machine-default build. I ran the identical command against a wiped target directory: **79.92 s test time, 92.97 s wall** — 26 % above the spec's figure on the same machine, and 71 % above round 2's 54.33 s. That spread does **not** threaten the 120 s ceiling, because the gate as written filters to `drift_tests`: measured cold, `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=/tmp/rev3-filtered cargo test --manifest-path Cargo.toml -p sessions --lib drift_tests` cost **9.97 s wall**, 0 passed / 92 filtered out, exit 0. The build is ~10 s and the run phase is the seven new tests. Recommendation: the table should either be re-measured or labelled as one observation, since a reader is being asked to accept a margin argument from it.
- **F13 (moderate) — B4's deletion is right, its justification is false.** The spec argues the deleted test guarded an unreachable world because "every path entering `files` is also stamped". Under the spec's own design that is untrue twice: Step 4 inserts into `files` and adds **no** stamp when `observe` returns `None`, and Steps 2/4/7 all stop inserting once the map reaches `limits.stamps` while `files` keeps growing. Deletion remains the correct call — no test distinguishes sweeping `files` from sweeping `stamps`, and under the new `install` the two are behaviourally equivalent in every pinned scenario — but the reason recorded for it is wrong.
- **F14 (moderate) — the new cap is undocumented by any execution.** `limits.stamps` (`spec01.md:161-172`) is a new declared setting whose stated behaviour past the cap is a **silent** partial: drift awareness for the first 4096 paths in `BTreeSet` order and none for the rest. The spec rightly requires the README to say so in those words, and then gates nothing. A cap whose failure mode is silence is the kind the spec elsewhere argues must not go unproven. Recommendation: one test that installs a tiny `Limits`, touches past it, and asserts the over-cap path is neither stamped nor named.
- **F15 (minor) — no step declares the new module.** Step 2 creates `src/drift.rs`; nothing adds `mod drift;` to `src/lib.rs`. `src/lib.rs` is in the footprint so it is implementable, but the step list is meant to be complete.
- **F16 (minor) — `restamp` stats whatever is in `files`.** Step 2's `restamp` walks `session.files` and `observe`s each entry without the `normalized` check Step 1 exists to promote. A legacy or unvalidated entry is stat'd against the *host process* cwd — the exact hazard F8 named, on the read side. The risk today is small, because `touch` has no caller and `changes::append` only ever inserts a validated path, but the guard costs one line and the spec has already paid for the function.

Credited as correct, verified rather than accepted:

- B3 is fully resolved; I read the preamble and every table row against the claim.
- B4's test and its false Denied-worlds entry are gone; `grep -n a_file_never_read specs/spec01.md` returns nothing.
- `install` has exactly four callers and no fifth; the spec's list is exact, including the distinction from `crate::limits::install` at `src/lib.rs:1174`.
- F9's whitelist is exactly what `Session` serializes today, checked field by field including the two that carry no `skip_serializing_if`.
- F10's extra assertion is present in both named tests.
- F5's footprint growth is justified and collision-free; 21 existing `limits.*` keys confirmed, `Limits::declared` reads them back, and `src/limits.rs` is in no other spec's footprint.
- Verify-block hygiene holds again: repo-root-relative paths, no `cd` to an absolute checkout, `CARGO_TARGET_DIR` set unconditionally inside gitignored `target/` and outside the footprint, no `${VAR:?}`, no `$TMPDIR`, no injected environment, the `if grep -qn …; then :; else …; exit 1; fi` form rather than the inert `!` or `a && b`, and no failure message naming the token an implementer must add.
- The frozen report contract is right and I raise **no objection**: `report: null` when nothing moved, `changed` and `gone` as two distinct lists, nothing rendered in the null case. `@harness/…` may keep building against it.

Disposition: revise. The design has been correct and stable since round 1 and is not what is failing; three rounds have now failed on the same two defects — a load-bearing prose claim that contradicts the code, and a gate whose acceptance text is wider than the world it executes.

Validation, `env -u CARTRIDGE_YOLO` in every form, cwd `/Users/feb/dev/cartridge/sessions.ctg` unless noted:

| command | exit | note |
| --- | ---: | --- |
| `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=/tmp/rev3-target cargo test --manifest-path Cargo.toml -p sessions --lib` | 0 | wiped target dir; **92 passed, 0 failed, 0 ignored**; **79.92 s test time, 92.97 s wall** |
| `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=/tmp/rev3-filtered cargo test --manifest-path Cargo.toml -p sessions --lib drift_tests` | 0 | wiped target dir; 0 passed, 92 filtered out; **9.97 s wall** — the gate's real cost, 8 % of the 120 s ceiling |
| `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=/tmp/borrowtest-target cargo build` (cwd `/tmp/borrowtest`) | 0 | disjoint-field borrow crate compiles in 0.85 s; disproves `spec01.md:197` |
| `grep -rn 'install(' src/` | 0 | four `Store::install` callers: `lib.rs:299,443,488`, `mapping.rs:360`; `lib.rs:1174` is `limits::install` |
| `grep -c '"limits\.' cartridge.json` | 0 | 21 |
| `sed -n '55,90p' src/lib.rs` | 0 | `Session` serialized key set matches the spec's whitelist exactly |
| `grep -m1 '^state:' …/boards/sessions/prds/*/prd.md` (cwd `/Users/feb/dev/cartridge`) | 0 | every other `sessions` PRD `done` or `deferred`; no footprint collision |

No `prd` state operation was run, no source file was modified, `prd.md` was not touched, nothing was staged or committed.

Reviewer identity: reviewer agent, coordinator-78 session.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: B6 (`specs/spec01.md:134-141,302-306,341,446-449`, against `sessions.ctg/src/lib.rs:299,443,488` and `src/mapping.rs:360`); B7 (`specs/spec01.md:137-144`, against `sessions.ctg/src/mapping.rs:114,176,344-361`); B8 (`specs/spec01.md:278-281,463-466`, against `sessions.ctg/src/change_record.rs:105-116`).
Rounds used / remaining: 3 / 2.
Next action: one bounded revision closing B6 (an eighth test through `repair` or `connect`), B7 (the resident-session branch in `install`, or a complete statement of the live absorbing window) and B8 (one assertion line), then round 4. Before pinning any gate, write its lazy implementation and check it fails; before writing any sentence about the code, open the call site.


## Coordinator record: round 4

Independent reviewer /root/drift_reviewer scored this revision FAIL 88/100. B6, B7 and B8 are resolved; B9 is a reproduced caller and fixture compatibility gap. Four rounds are used and one remains. All canonical input and report hashes were checked before appending the full attributed report.

# Sessions file drift: independent round 4

Reviewer: `/root/drift_reviewer`. Verdict: **FAIL, 88/100**, with one blocking compatibility/footprint finding, B9. This is substantive round 4: four rounds used, one remains. Earlier scores 66, 71 and 74 remain unchanged. No user rating is requested or asserted.

## Authority and reviewed revision

I ran `./task prompt` first, read the brief, canonical specification, complete previous review history, analyst-codex-4 report, review-plan workflow, both successor briefs, relevant Rust guidance and the test-behavior-not-implementation principle. The repository review workflow and delegated bounded assignment govern this report; no interactive skill approval or nested delegation was introduced.

Sessions source HEAD is `499191501e7e3cbb1ac1537ea75a5f1906f97f21`. The live diff contains only foreign changes to cartridge.json, README.md and .cartridge/help.md. I read that diff; it is the task-command migration, not drift implementation. Those changes were not copied into the disposable probe. The nine canonical footprint paths agree with the specification, but the footprint omits necessary migrations identified below. There is no implementation diff to approve yet.

## Score

| Dimension | Score | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19/20 | The useful Sessions mechanism and the two live consumer outcomes are honestly distinguished. Both FS and Harness successor records exist with needs on this leaf. Original live acceptance remains unticked. |
| Ownership and reuse | 18/20 | Reuses lexical normalization, Session, candidate publication, existing mapping and repair seams, and declared Limits. Dedicated drift module is now explicit. Deduction for omitted owned test/document migration paths. |
| Dependencies and implementable slices | 16/20 | Install branching is implementable in the stated source and does not require a new store. The exact footprint cannot implement strict touch and still pass existing owner tests. Root's opt-in JEV fixture also needs coordinated migration. |
| Observable acceptance and baseline evidence | 18/20 | Eleven concrete tests now distinguish cold load, live mapping/connect, post-rename recovery, replay, own writes, cap, null notification and snapshot schema. Existing compatibility tests contradict strict touch; targeted execution proves the missing migration. No new test is claimed to have passed before implementation. |
| Failure, recovery and compatibility | 17/20 | Resident stamps, including an empty map, survive install; absent-only repair is accurately bounded. Metadata and cold-load ceilings are honest. Strict-touch migration is incomplete and a linked manual still promises display-only touch and no file access. |
| Total | **88/100** | **FAIL: B9 remains blocking.** |

## Previous blockers resolved

**B6:** The test plan now drives all four actual install entry paths with appropriate semantics. Cold load is tested separately. Existing mapping lookup and connect are requested independently in both durable and connection-local contexts, each with an observed file changed before refresh. DirectorySync failure after an unrelated buffer mutation exercises publish_checked recovery without acknowledging the observed file itself. Real empty legacy repair is tested as empty repair followed by ordinary touch/drift; a resident valid session cannot be repaired. The earlier demand for a files-bearing legacy repair would contradict recovery::legacy and is not retained.

**B7:** Store::install must branch on resident identity, transfer resident stamps without reobservation, prune only missing incoming file keys, and never treat an empty resident map as cold. The current source makes this possible: publish_checked invokes install on its candidate, and mapping refresh invokes install on the resident Store under the session gate. Successful candidate publication and SharedStore merging clone/retain the new skipped field automatically. Cold-load absorption is separately documented. This resolves the actual live-window reset, not just its prose.

**B8:** Literal absolute strings containing `/../`, `/./` and repeated separators join relative inputs in the refusal test. The existing normalized implementation compares reconstructed path bytes, so it rejects the internally normalized-away dot/separator cases too. The test must build literal malformed strings, as stated.

F11–F16 are addressed coherently: no false disjoint-borrow assertion, old timings labeled historical, no files/stamps equivalence claim, a tiny-cap subprocess, explicit module registration, and normalization before cold observation. The cap clarification is accepted: first successful live admissions without eviction; cold traversal examines only its first capped sorted candidates, including invalid/indeterminate candidates in that budget. This bounds additional traversal and stat count while documenting partial coverage. Existing tracked keys refresh at capacity. This is not a claim to bound filesystem syscall latency.

The flat reply remains a rendered string with changed/gone siblings, or exactly id/report:null without changed/gone. The no-change changed-id is None. Harness's earlier object-shape mistake does not change that contract.

## B9: migrate existing callers and their fixtures within an executable footprint

The plan requires strict absolute normalized touch and forbids editing old fixture files. Four current Rust tests require relative touch success. A minimal faithful guard in a disposable committed-HEAD archive makes all four fail; restoring the two source files to the same HEAD makes all four pass. The required full-owner Cargo gate therefore cannot pass under the declared nine-path boundary.

| Owned file and line | Existing assumption | Required migration |
| --- | --- | --- |
| `.cartridge/tests/unit/main/tests.rs:51` | `changed.rs` must reach injected persistence failure. | Use a normalized absolute disposable path, retaining the assertion that failure comes from Write/FileSync/Rename and state stays intact. Do not weaken it to any error. |
| Same file, lines 178 and 215/230 | `x` and `a.rs` must touch successfully; round-trip asserts `a.rs`. | Use fixture-root absolute paths and preserve scratch-buffer and round-trip assertions. |
| `.cartridge/tests/unit/main/change_records_tests.rs:46,75` | `legacy arbitrary path` is supplied through live touch, then retained in files. | Preserve actual legacy compatibility by loading a literal legacy snapshot containing this string; use normalized absolute inputs for new touch calls. Do not delete legacy retention coverage. |
| `.cartridge/tests/integration/change-records.test.ts:18,45` | Two real native calls touch `legacy noncanonical path` and `legacy` successfully. | Seed legacy snapshots while the native service is stopped, restart, and retain exact legacy metadata/byte preservation assertions. Use valid normalized new-call inputs where testing current touch. |

These are all Sessions touch call sites found by the source sweep. `.cartridge/tests/integration/context.test.ts:22` uses `/PRIVATE-FILE`, which already satisfies the new format and needs no path change. The four Rust failures are executed evidence; the two native failures are source-derived predictions, not claimed executions.

The same class appears outside this owner: root `.cartridge/tests/integration/jev-reliability.test.ts:28` sends `jev.ctg/src/assess.ts`. It is an opt-in live test (`CARTRIDGE_LIVE_JEV_RELIABILITY=1`) and was not run. Its owner should change the fixture to the normalized absolute path resolved from cwd before integrated reliability verification. Keep that change in root ownership; do not widen a Sessions leaf into a cross-cartridge patch or invoke the live assessments just to prove a lexical rejection.

Recommended coherent final revision: add the two Sessions unit files and the one native integration file to the footprint; remove the contradictory do-not-edit instruction for those exact files; specify the migrations above and preserve their original assertions. Add executed migrated tests to verification alongside the existing eleven drift cases. Bind native verification to an explicit compatible host and candidate Sessions module with isolated runtime state and unset CARTRIDGE_YOLO; if that external host is unavailable, record a real prerequisite rather than treating Cargo as proof of native tests. Coordinate the one root-owned fixture migration before its affected integrated gate.

## Additional documentation finding F17

`.cartridge/docs/change-records.md:7` says touch and get.files remain display-only. Lines 18–19 say Sessions validates coordinates without reading files. With this change, touch and accepted record_changes observe filesystem metadata. Add this one owned manual to the footprint and qualify those statements: get.files is metadata projection; evidence validation remains lexical and conveys no authorization, while accepted paths additionally refresh bounded in-memory filesystem observations. Preserve the distinctions between metadata observation, content verification and ownership. This is the same compatibility sweep, not a new feature.

The resulting necessary Sessions footprint is thirteen paths: the current nine plus two existing unit files, one native integration file and one manual. No source outside this scope was found to require modification for strict touch in this review.

## Probe and command accounting

Disposable archive: `/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/drift-round4-review-fu4fuhxe`.

The probe exported committed Sessions HEAD and changed only two archived source files: exposed change_record::normalized as pub(crate), and added a guard before touch inserts into files. It did not implement drift or alter tests. Each command used `env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=target/review-probe cargo test --offline --locked --lib <name>` (equivalent environment removal in the Python subprocess runner). No downloads or shared runtime access occurred.

| Test filter | Minimal guard | Restored HEAD |
| --- | --- | --- |
| publication_identity_deduplicates_only_same_publication_and_keeps_legacy_projection | exit 101; unwrap rejected relative path | exit 0, one passed |
| every_pre_rename_failure_preserves_all_mutations_and_notifications | exit 101; rejection did not contain injected | exit 0, one passed |
| unattached_buffers_remain_memory_only_and_survive_other_session_commits | exit 101; unwrap rejected relative path | exit 0, one passed |
| a_session_round_trips_through_its_file | exit 101; unwrap rejected relative path | exit 0, one passed |

The archive now contains restored baseline source, `strict-touch-probe.log` for the last three guarded failures, and `baseline-targeted.log` for all four restored passes. The first guarded failure is also preserved in this tool transcript. Initial guarded build took 21.43 seconds; restored build took 13.43 seconds. These are targeted observations, not whole-suite performance claims. The full library currently has 100 tests, as shown by one executed plus 99 filtered tests; historical 92-test results are not relabeled current.

Read-only commands included source/fixture reads, git status/rev-parse/diff/show, rg across all source touch callers and normalization assumptions, and SHA-256 computation. One initial Python archive extraction attempt failed because this Python lacks tarfile's filter keyword; the retry used a git-owned trusted archive and succeeded. One rg request named a nonexistent unit/settings.rs and exited 2; the relevant settings source was present and the failed path was not evidence. No full baseline, native integration or new drift test was run.

All tool sessions are terminal, including 83625 and 37386. No source, canonical record, acceptance checkbox, PRD lifecycle state or commit was changed. Only this reviewer report was written in the shared tree.

## Review ceiling and next action

The previous defeated vacuous write gate, load-only gate, and absolute-only gate remain in review history. This review neither erases them nor spends another round trying to make tests prove their own honesty. Independent implementation diff reading remains the backstop for actual install wiring, empty resident maps, cap checks, error classification, replay and assertion validity. B9 is separately proven incompatibility between a required behavior and existing tests outside the allowed footprint; it is not a gate-design-ceiling exception.

One final substantive revision remains. Resolve the complete known migration class above, retain the now-correct observation/recovery design and frozen reply, then obtain the fifth independent review. Do not reset rounds or claim implementation completion.

## Input digests

| Input | SHA-256 |
| --- | --- |
| `prd.ctg/.cartridge/boards/sessions/prds/file-drift-awareness/prd.md` | `76a9da0b43ba58b82102915333da5f81c2f3ce125ca5f562643f90907c453ebe` |
| `prd.ctg/.cartridge/boards/sessions/prds/file-drift-awareness/specs/spec01.md` | `3c089fa802a8d282d299e477f345600a27121988c17bd159b31004d2a8b6e9ba` |
| `prd.ctg/.cartridge/boards/sessions/prds/file-drift-awareness/review.md` | `6bb7107ef326c9dc220b5621f552bb99fdf09c55292068067716a9d566eebd83` |
| `prd.ctg/.cartridge/boards/fs/prds/a-read-stamps-the-file-it-returned/prd.md` | `57333a3d5dde500819ae8f861012ca52dec9186953f119c4af579866721938cc` |
| `prd.ctg/.cartridge/boards/harness/prds/the-turn-names-the-files-that-changed-underneath-it/prd.md` | `9a36424810f339de5e0da1a6085eca008745972aa0cfcba201f8b113e93f9d2b` |
| `prd.ctg/.cartridge/workflows/review-plan.md` | `1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9` |
| `sessions.ctg HEAD:src/lib.rs` | `a8b4eea48c966f6c3848c86aaa35d37813dc4c770a8428d1ec071d93cd697260` |
| `sessions.ctg HEAD:src/changes.rs` | `55e924df9d5e9356f2317d745e60de17a8cdb734253954eaad6dd17a31c471d8` |
| `sessions.ctg HEAD:src/change_record.rs` | `f7911c17e83f1442edd3e73b3944803460626dc0d7cbdb0720d9c567763df5f8` |
| `sessions.ctg HEAD:src/limits.rs` | `168464fb2548d10ebba52d63fc373d65d89c3d374cbf86e5dd96d037b7bb1cc8` |
| `sessions.ctg HEAD:src/mapping.rs` | `de3daad979305f5cf4e30f9a831f66f25947d81cc154bbc2660c5e2da96d4e05` |
| `sessions.ctg HEAD:src/recovery.rs` | `9c8064a3269f434150a3a3425cf3e6c18de277530ff350c1f2663329b5cb4c35` |
| `sessions.ctg HEAD:cartridge.json` | `6d0131f44e2b7c4fcef6b35f0095d54494dc7bdf7656fefa5279d55b0ccd02b3` |
| `sessions.ctg HEAD:.cartridge/tests/unit/main/tests.rs` | `ff42268c5161eaaa4fd13479021cabc6f70d18a719c7bb8c7237bb6c0b590af6` |
| `sessions.ctg HEAD:.cartridge/tests/unit/main/change_records_tests.rs` | `fb5e8c1f4e318b64bdb91c8182ab57c619296a192f0ad737f84ef13e0ee6b979` |
| `sessions.ctg HEAD:.cartridge/tests/unit/main/mapping_tests.rs` | `14dd748d25c2c01579d3380ef9c58eb3ddb6c81022895fa62d817873482cbf68` |
| `sessions.ctg HEAD:.cartridge/tests/unit/main/repair_tests.rs` | `d228a1519c41d16cac9697a63912f02ef034cb761d2def6635869f7840829f57` |
| `sessions.ctg HEAD:.cartridge/tests/integration/change-records.test.ts` | `c04ca45a995a627291845fb87f461dbd550cfba58f8cd62b64c362b554bdd1d3` |
| `sessions.ctg HEAD:.cartridge/docs/change-records.md` | `d97571b03407d62b9c3fb1d5a59c3e028f5e90f3551868fb50b2b84dcf688555` |


# Sessions file drift: independent round 5

Reviewer: `/root/drift_final_reviewer`. Verdict: **FAIL, 89/100**, with one blocking dependency and completion-boundary finding, B10. This is the fifth substantive round; all five rounds are now used. Earlier FAIL scores 66, 71, 74 and 88 remain history. No sixth automatic revision is authorized, including after renaming or splitting this scope.

## Reviewed authority and evidence

I ran `./task prompt` first and read PROMPT.md, the review-plan workflow, the canonical PRD/specification/review history, revision-5 analyst report, round-4 reviewer report, both dependent PRDs and the root fixture handoff. I applied the Rust routing and error-handling skills while inspecting source publication, observation-error and recovery boundaries. Source HEAD remains Sessions `499191501e7e3cbb1ac1537ea75a5f1906f97f21`; the only live tracked changes are foreign manifest/README/help edits. No implementation candidate exists to certify.

The canonical spec matches the assigned SHA-256 `9080d4d41d2a689a68815b68c5a4e427e2a946f2564df3af19206a99f75c2c31`. Its thirteen-path footprint matches the PRD. I read actual Store publication/install/repair, SharedStore dispatch, mapping refresh, changes append, lexical normalization, Limits, existing legacy unit fixtures, and the complete native helper and native change-records tests. I also read the engine's ordinary and committed collection checks and executed its read-only graph/refusal functions against current records.

## Scores

| Dimension | Score | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19/20 | Original read-to-next-turn outcome remains visible, and the Sessions-only mechanism is described honestly. Live delivery remains future work. |
| Ownership and reuse | 19/20 | Thirteen owned paths cover the implementation and known caller/manual migration. Existing normalization, Store transactions, mapping locks, snapshot decoder and Limits are reused. Root fixture stays with its owner. |
| Dependencies and implementable slices | 14/20 | The code slice is implementable, but its collection still requires evidence from consumers that the planner refuses to dispatch before this slice is done. No authoritative transfer or aggregate completion record resolves that cycle. |
| Observable acceptance and baseline evidence | 18/20 | Eleven mechanism tests, four migrated Rust tests and five native tests are concrete and preserve their assertions. These gates cannot establish the original live read/next-turn criteria that remain in canonical acceptance. No candidate tests have run yet. |
| Failure, recovery and compatibility | 19/20 | Resident versus cold install, replay, bounded admission, null publication, legacy load and native host identity are coherent. Metadata, cold-restart and latency ceilings remain explicit. |
| Total | **89/100** | **FAIL: B10 blocks execution through collection.** |

## B6, B7, B8 and B9 are resolved in this revision

B6 remains resolved: the plan exercises actual cold load, independent mapping/connect requests in durable and connection-local contexts, DirectorySync recovery after an unrelated buffer mutation, and actual empty-only legacy repair. It does not invent a files-bearing repair fixture. B7 remains resolved: install branches on resident identity, preserves even an empty resident stamp map, prunes removed keys, and never reobserves resident files. Reading publish_checked confirms recovery calls install on the already-mutated candidate, so carrying that candidate's resident stamps retains accepted observations as well as unrelated outstanding drift. Ordinary publication replaces self with the candidate and does not overwrite its stamp map.

B8 remains resolved: refusals cover literal relative, dot, parent and duplicate-separator strings; the existing normalized rule reconstructs and compares path bytes. Determinate absence, indeterminate metadata failures and pre-epoch conversion remain distinct. The cap bounds observation count and map size without claiming bounded filesystem latency. Existing tracked keys refresh at capacity; cold candidates consume a bounded traversal budget, including invalid entries.

B9 is now resolved within the allowed paths. The three ordinary relative unit callers become disposable absolute paths while retaining their original fault-origin, round-trip and scratch-buffer assertions. The persistence-fault fixture explicitly avoids creating an extra store-directory file. The legacy unit caller and both native legacy callers instead load literal legacy snapshot data. The plan preserves exact legacy strings and byte/metadata/replay checks rather than erasing compatibility coverage by normalizing old data. Native services are stopped before editing snapshots and replacement instances are used after restart.

The new native test exercises candidate strict touch and drift through the real host. The build explicitly selects the candidate dylib. The host path is prepared in ignored scratch and checked against a pinned digest, with a real blocker if preparation fails. I independently hashed the current compatible artifact and obtained the declared `b081f7d1b9aab6c1130bb61ee4ec356931b65483dcac7e88c998ca283ff6dc75`. This is artifact identity, not a native test pass. Whole-owner tests, fmt, strict clippy, audit and isolation remain required.

F17 is resolved: the owned manual now has an explicit migration separating bounded filesystem metadata observation from lexical evidence validation, content verification and authorization. The actual root JEV fixture has the absolute path.resolve argument and matches the declared hash. That file remains foreign/untracked; neither this review nor the handoff claims committed delivery or a live JEV execution. Its owner reconciliation before integration is explicit and does not introduce a reverse product prerequisite.

## B10: original completion still depends on blocked successors

The canonical PRD remains a leaf with these original unchecked requirements: reading a file records a stamp, and a changed file is named at the next turn start. The spec explicitly states that there is no live read or turn caller in its footprint and instructs the coordinator not to tick the original live criteria merely because the Sessions mechanism passes. It requires successor integrated evidence before claiming that composed outcome. Those are correct fidelity constraints.

However, both successor records have `needs: [@sessions/file-drift-awareness]`. FS explicitly says to collect the Sessions row first. The Harness record likewise says the provider must land before end-to-end verification. The engine's planner refuses each while Sessions is not done. Ordinary collection at lifecycle.ts:184–185 requires dependencies done and all original PRD/spec acceptance boxes closed; committed collection at collection-proof.ts:88 also rejects open boxes. The plan therefore has no authorized path from its successful mechanism tests to collection, and neither live successor can start through the specified board workflow before collection.

Executed read-only graph evidence (exit 0):

```text
@sessions/file-drift-awareness: analyzing; openBoxes=true; held by coordinator-codex-14
@fs/a-read-stamps-the-file-it-returned: open; openBoxes=true; needs: not done — @sessions/file-drift-awareness
@harness/the-turn-names-the-files-that-changed-underneath-it: open; openBoxes=true; needs: not done — @sessions/file-drift-awareness
```

A source sweep of fs.ctg/src and harness.ctg/src found no current touch/drift caller supplying the missing integration. The only relevant root fixture touch call is the unrelated JEV fixture. The coordinator confirmed no existing authoritative acceptance transfer beyond this successor mapping is known. Mapping future ownership in a table does not change what the collection engine requires of the original leaf.

This is not a demand to widen Sessions into other cartridges, implement future consumers prematurely, or remove the original outcome. It is a requirement for a faithful, executable decomposition. A possible disposition is to retain the original composed outcome as an aggregate, give the provider mechanism its own collectable acceptance, and make FS/Harness depend on that provider rather than on the aggregate. The original read/turn criteria must remain attached to completion evidence, not be silently deleted or ticked by mechanism tests. Such a restructuring changes the reviewed plan and inherits its exhausted allowance; it needs explicit authorization for further review before automatic implementation resumes. Do not evade the limit by changing addresses or converting unchecked boxes into historical prose.

This problem existed across earlier rounds, but their acceptance of the successor mapping does not waive canonical acceptance or engine ordering. B10 is an orchestration contradiction found in the actual records, not another attempt to design self-policing tests. The prior gate-design ceiling remains intact.

## Disposition and command accounting

Record the fifth failure and review exhaustion. Retain the resolved technical design and migration evidence. The coordinator should use the question transition with the concrete completion-boundary finding and proposed faithful decomposition; no automatic sixth revision or implementation handoff is supported by this review.

This review ran read-only source/record inspections, git status/rev-parse, hashes and the actual graph/refusal functions. No new implementation test, full baseline, native runtime or live JEV test was run or claimed. A few exploratory reads named nonexistent src/shared.rs, src/concurrent.rs and src/collect.ts files; rg reported those missing paths, and the relevant existing files were then inspected. The initial spec path omitted the central prd.ctg owner and was corrected. These lookup failures are not behavioral evidence.

No canonical record, source, lifecycle state, acceptance checkbox, index or commit was changed. Only this report was written. Every tool command is terminal; no background process or open exec handle remains.

## Input digests

| Input | SHA-256 |
| --- | --- |
| `prd.ctg/.cartridge/boards/sessions/prds/file-drift-awareness/prd.md` | `73feb3b1054c79c974ebe305c4b31f11dd65c553bad911119decb0f49fcdb478` |
| `prd.ctg/.cartridge/boards/sessions/prds/file-drift-awareness/specs/spec01.md` | `9080d4d41d2a689a68815b68c5a4e427e2a946f2564df3af19206a99f75c2c31` |
| `prd.ctg/.cartridge/boards/sessions/prds/file-drift-awareness/review.md` | `40b9a34911bf3a1fae1a2d7b822b818632d8213571fc428e5ec0832a897a4578` |
| `prd.ctg/.cartridge/boards/sessions/.state/loop/file-drift-awareness/analyst-codex-5.md` | `6705de19d63d6c4232213f97c6288d7b0add42047cfe99b0a6fa5111cb7b516d` |
| `prd.ctg/.cartridge/boards/fs/prds/a-read-stamps-the-file-it-returned/prd.md` | `57333a3d5dde500819ae8f861012ca52dec9186953f119c4af579866721938cc` |
| `prd.ctg/.cartridge/boards/harness/prds/the-turn-names-the-files-that-changed-underneath-it/prd.md` | `9a36424810f339de5e0da1a6085eca008745972aa0cfcba201f8b113e93f9d2b` |
| `prd.ctg/src/lifecycle.ts` | `504a35ddf8c48cc6902bca8c29d650af1e334728e549eec897dc5a06dd28a7c7` |
| `prd.ctg/src/collection-proof.ts` | `cb6b4ed34186545401754f6815ccd5904f7cc6986faab1da64f30ebac72d684f` |
| `prd.ctg/src/planner.ts` | `fd60f4c7603e212279d47bf1bc37a30e7f2b28d2865b9cc3cbb175317807fcfe` |
| `prd.ctg/.cartridge/workflows/review-plan.md` | `1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9` |
| `.cartridge/tests/integration/jev-reliability.test.ts` | `e101e2aab73a74ebe26edec2e54b669105515868dd3813b8d9c18764321e30ec` |
