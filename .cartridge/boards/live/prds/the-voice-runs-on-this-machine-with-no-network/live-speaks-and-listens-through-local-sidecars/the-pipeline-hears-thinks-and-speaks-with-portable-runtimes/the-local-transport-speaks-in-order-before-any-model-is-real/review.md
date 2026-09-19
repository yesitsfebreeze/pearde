# live/the-local-transport-speaks-in-order-before-any-model-is-real review history

Plan: `live` board, `@live/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars/the-pipeline-hears-thinks-and-speaks-with-portable-runtimes/the-local-transport-speaks-in-order-before-any-model-is-real`, source `prds/.../the-local-transport-speaks-in-order-before-any-model-is-real/prd.md` and `specs/spec01.md`.
Scope: one leaf — `provider: "local"` runs a whole session through STT/TTS/turn-end seams with stubs and an HTTP brain; it carries all 7 Acceptance boxes of its roll-up parent `the-pipeline-hears-thinks-and-speaks-with-portable-runtimes`.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none. The parent was split by its analyst before any review round.

Use the shared [review method](../../../../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-19

Presented revision: `live.ctg` HEAD `6922a8f` (clean). The reference implementation is the analyst's scratch tree `scratchpad/analyst-pipeline/live-probe`, applied onto a fresh `git clone --local` at `scratchpad/reviewer-localtransport-1/ref`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `b4f56feced50d60c939966c8fc5aa49208cab6c7f2a74783dd3613db0a10dc56` |
| Specs | `specs/spec01.md` sha256 `7c870ee6c0d6cd3d3bbd78609c307d038c54e2f5177eb1fe0afc7806318b1e35` |
| Material contracts/dependencies | parent `prd.md` sha256 `7a6ea0aefc00050385279caf3d0412e0eb0e4cd667f23b1182cb1a5ee312d043`; `live.ctg@6922a8f` `src/service.rs` (`start_voice` 266-316, `event` 544-616, `status` 169); sibling PRDs whisper, kokoro, `the-turn-ends-when-the-speaker-is-done-not-when-silence-runs-out` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 15 | The slice is tight, cheap and offline, and cleanly separated from whisper, kokoro and turn-taking. −5: `Transport::open` opens `local::Settings::default()` and never reads the four settings the manifest declares. `provider: "local"` therefore can never reach a stand-in endpoint, even though README tells the user to "point `stt`/`tts` at an HTTP endpoint in the meantime" (B2). |
| Ownership and reuse | 17 | Reuses `Transport`, the service's name-based event dispatch and `socket::pcm`. Each seam is a plain function with a `Source::Model` branch that whisper and kokoro replace in place, with no speculative traits. −3: the turn-taking sibling shares `src/local.rs` and `src/turn.rs` but does not `needs` this child (the analyst raised it; still open). The `send` no-op silently drops the greeting and the spoken-back delegation result, and nothing names which child owns that. |
| Dependencies and implementable slices | 17 | `needs` is satisfied. The footprint is justified, and widening `src/service.rs` by one line keeps the test's intent (`"carrier-pigeon"` stays unknown in both the service and transport tests). −3: fixing B1 and B2 requires `src/service.rs` beyond that one line (`Config` fields, event ordering), and the spec rules that out. |
| Observable acceptance and baseline evidence | 13 | Verify reads 9 named tests from cargo's own output, needs `socket::`/`audio::` to be present, and fails on `FAILED`. Base goes red and the reference goes green (below). The event order is an exact `assert_eq!`, and the PCM is compared byte for byte against the stub's own output. −7: parent box 4 says an error "`status` then reports", but the spec drops that clause and tests only through `local::connect`, so the defect in B1 goes unseen. The delegation "no audio" assertion snapshots straight after the delegation event: it caught an injected post-delegation audio delta 5/5, but only because the stub answers within the 10 ms poll (N3). |
| Failure, recovery and compatibility | 13 | Missing-file and refused-endpoint paths emit `error` then `session.closed`, and no panics were seen. `gpt` stays the default, and `cfg`/`Command` are absent. −7: B1, the failure is invisible to `status`. N2, `reqwest::Client::new()` has no timeout, so an endpoint that accepts but "will not answer" (the parent's wording) hangs the turn forever with no error. |
| Reviewer total | 75 / 100 | |

Findings and concrete revisions:

- **B1 (blocking): a local failure never reaches `status`.** `local::connect` emits `session.started`, then on a missing model it emits `error` and `session.closed`, all synchronously inside `Transport::open`. `start_voice` sets the id holder and inserts the `Live` entry only after `open` returns (`src/service.rs:276-307`), so `event()` drops all three.
  - Reviewer probe: a service test with `provider: "local"`, default settings and `audio::fake::open`, then `status()` after 300 ms. Result: `{"voice":[{"error":null,"live":"local-…","ready":true}]}`, meaning a dead session reported as ready.
  - The docs repeat the false claim ("a live id `status` can report against").
  - Revision: make an event that arrives before the id is known wait instead of vanishing. For example, the `start_voice` callback queues events until the holder is set and then replays them. That takes a few lines in `src/service.rs`, so the spec must allow it.
  - Add a named `service::tests::` test to Verify's list: a `local` session with a missing model shows its reason in `status()["voice"][0]["error"]`.
  - Restore the parent's "which `status` then reports" in the spec's Acceptance.
- **B2 (blocking): the four declared settings are inert.** `Transport::open` → `local::connect(Settings::default(), …)`, and `Config` has no `stt`/`tts`/`brain`/`models`. The manifest and all three docs describe values that change nothing.
  - Revision: add the four fields to `Config` with the manifest's defaults, and read them where `lib.rs` builds `Config`.
  - Build `local::Settings` from `Config` in `Transport::open`.
  - Add a named test proving a non-default value is honoured. The B1 service test, with `models` set to a scratch dir, can name that dir in the error.
- N1: `turn.rs`'s "30 ms silence" is really 30 ms with no frame arriving (`timeout(SILENCE, rx.recv())`). Real capture delivers 200 ms batches on a 50 ms poll (`src/audio.rs:17,181`), so once speech has been heard the gap after every batch commits a turn. Either judge silence by frame energy over a window longer than a batch, or say plainly in the spec and docs that the placeholder is not usable live.
- N2: give the `reqwest` client a bounded timeout. Add a named test with a stub that accepts and never replies, and assert `error` then `session.closed`.
- N3: in `a_delegate_tool_call_is_a_delegation_with_no_audio`, wait a bounded settle (for example 200 ms) after the delegation, or until the stub's `/speak` route would have answered, before asserting the kinds.
- N4: say in the docs that `send` is a no-op for `local` (no greeting; the agent's delegated answer is not spoken), and name the owning child.
- N5 (coordinator): add `needs: [this child]` to `the-turn-ends-when-the-speaker-is-done-not-when-silence-runs-out`.
- The ceiling paragraph is honest and in line with `review-plan.md` step 4: it names the diff reading as the backstop and designs no new gate. This round spent no time on gate design.

Disposition: revise (keep scope). B1 and B2 both need the spec to allow a small, named change in `src/service.rs` beyond the one test literal.

Validation (every run under `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`; blocks extracted verbatim from `spec01.md`; cwd is each clone; live `live.ctg` was never written and is still clean at `6922a8f`):

- base block 1 → exit 1 (`test -f src/local.rs`), 0 s.
- base block 2 → exit 1, `21 passed`, "missing or failing test: local::tests::a_session_starts", 6 s cold.
- ref block 1 → exit 0, 0 s.
- ref block 2 → exit 0, all 9 names `... ok`, clippy clean, 8 s with a fresh `CARGO_TARGET_DIR`.
- ref `cargo test --lib` ×8 → `29 passed; 0 failed` every time, 0.78 s.
- Probe clone `reviewer-localtransport-1/probe`: B1 status probe → FAILED as described. The injected post-delegation audio → the delegation test FAILED 5/5.

Reviewer identity: reviewer-localtransport-1 (independent review sub-agent, Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (75/100, two blocking findings).
Unresolved blocking findings: B1, B2.
Rounds used / remaining: 1 / 4.
Next action: make one revision of `spec01.md` (and the child's Acceptance box 4 wording) that allows a small `src/service.rs` change covering event buffering and `Config` fields, and adds the named service-level test. Fold in N1–N4 where cheap, update the reference to match, then request round 2.

## Round 2 — 2026-09-19

Presented revision: `live.ctg` HEAD `6922a8f` (live checkout clean before and after). The reference is the analyst's `scratchpad/analyst-pipeline/live-probe` diff plus its untracked `src/local.rs` and `src/turn.rs`, applied onto a fresh `git clone --local` at `scratchpad/reviewer-localtransport-2/ref`. The base clone is `.../reviewer-localtransport-2/base`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `b4f56feced50d60c939966c8fc5aa49208cab6c7f2a74783dd3613db0a10dc56` (unchanged since round 1) |
| Specs | `specs/spec01.md` sha256 `8b3c894977ee446d43dd12590779fd0723face5830dc007ba141854f190ff304` |
| Material contracts/dependencies | parent `prd.md` sha256 `7a6ea0aefc00050385279caf3d0412e0eb0e4cd667f23b1182cb1a5ee312d043`; `live.ctg@6922a8f` `src/service.rs` (`start_voice`, `event`, `status`), `src/audio.rs` (`RATE` 24000, `BATCH` = RATE/5, 50 ms poll, lines 17 and 179-196); analyst report `analyst-child1-3.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 15 | B2 is fixed: `Config` has the four fields with `#[serde(default)]`, `lib.rs` already deserialises `cartridge.config` into `Config` by field name, and `Transport::open` builds `local::Settings` from them. −5: the N1 revision swapped one broken turn end for another (B3). At real capture cadence the placeholder never commits a turn, so README's "Point `stt`/`tts` at an HTTP endpoint in the meantime to exercise the pipeline end to end" cannot happen with a real microphone. |
| Ownership and reuse | 18 | The seams, the `Transport` enum and name-based dispatch are reused. `Config::default()` takes the local defaults from `local::Settings::default()`, so the two cannot drift. `send` being a no-op is now documented and its owner (kokoro) is named (N4 resolved). −2: the `session.closed` → mic teardown gap (N7) is left unowned. |
| Dependencies and implementable slices | 18 | `needs` is satisfied, and N5 was resolved by the coordinator. The `src/service.rs` change is named in the spec (Step 7), covers exactly what it names, and nothing else in the file moved. −2: the spec says the widening is "the coordinator's round-2 decision recorded in `prd.md`'s 'Footprint widened' section", but that section (digest unchanged) still says "for one line" (N6). |
| Observable acceptance and baseline evidence | 17 | The 11 named tests are read out of cargo's own output. Base is red and the reference is green. The new service test really exercises `status` after a local failure: three mutations each turn it red (below). The N3 settle and the N2 never-answers test are present. −3: no test drives the turn end at the cadence `audio.rs` actually delivers, which is how B3 got in unseen. The turn tests only check `Turn::hear`/`ready`, not the commit timing. |
| Failure, recovery and compatibility | 17 | B1 is fixed (events buffered, `Live` inserted before the flush), and the client timeout is 3 s. All 21 base test names still report `... ok` in the reference. Five consecutive runs gave `31 passed; 0 failed`. The `gpt` path is unchanged apart from the insert-then-update reordering. −3: N7 (a mic opens on an already-dead local session) and N8 (a narrow ordering window in the flush). |
| Reviewer total | 85 / 100 | |

Findings and concrete revisions:

- **B1: resolved.** `Buffered::{Pending, Known}` replaces the `Option<String>`. The `Live` entry is inserted before the replay, and a replayed `error` is not overwritten by a later mic error. `service::tests::a_local_sessions_missing_model_reaches_status` polls `status()` and asserts three things: the reason names the scratch `models` dir and `whisper-base.en.bin`, and `ready == false`. Mutation probes, each on a copy of the reference:
  - (a) Pending events dropped → the test FAILED (`src/service.rs:1503`).
  - (b) Flush replaced by a discard, which models "insert after flush" → FAILED (`:1501`).
  - (c) `Transport::open` ignores `config.models` → FAILED (`:1504`).
- **B2: resolved.** The chain `cartridge.config` → `Config` (serde by name, `#[serde(default)]`) → `local::Settings` is intact. Mutation (c) shows the test depends on it.
- N2, N3, N4: resolved as described. N5: resolved by the coordinator (the turn-ends sibling needs the whole parent).
- **B3 (blocking, the N1 revision): the placeholder turn end now never commits under real capture.**
  - Silence is still judged by frame arrival: `timeout(SILENCE, rx.recv())` in `local::connect`. Real capture (`audio.rs:179-196`) forwards a `BATCH` of 4800 samples (200 ms at 24 kHz) about every 200 ms for as long as the mic is open, whether or not anyone is speaking.
  - With `SILENCE` at 350 ms the timeout therefore never elapses. Round 1's 30 ms committed at every batch boundary; this commits never.
  - Probe: a scratch test in a copy of the reference sent one loud 3200-sample frame, then ten silent 3200-sample frames 200 ms apart, using the file's own `stub`/`collector`/`kinds`. It FAILED: "2 s of silent 200 ms batches after speech never committed a turn: ["session.started"]".
  - The docs (`.cartridge/docs/README.md` "sized above real capture's own batching … does not commit mid-sentence", and README's "exercise the pipeline end to end") claim a live path that cannot work.
  - Revision: judge silence by energy, not arrival. For example, `Turn` counts quiet samples since the last loud frame, and the loop commits once that count is at least `SILENCE` × `RATE`, keeping the arrival timeout for a stalled stream. Add a named test at `audio.rs`'s cadence (loud frame, then silent frames 200 ms apart must commit within about 1 s) and put it in Verify block 2's list. Or, at minimum, say plainly in the spec and all three docs that the placeholder does not commit turns from a live microphone.
- N6: `prd.md`'s "Footprint widened" section still describes a one-line change, and the spec attributes a round-2 decision to that section. Record the decision there (body only, in place) or drop the attribution from the spec.
- N7: after a missing-model failure, `start_voice` still calls `Voice::start`, so the microphone opens on a session that is already closed and stays open until `stop`. Skip `Voice::start` when the entry is already `closed` after the flush (one check), or note it.
- N8: `mem::replace(… Known(id))` runs before the queued events replay. A callback that lands in between dispatches ahead of older queued events. That window is not reachable for the missing-model path, but a GPT socket can hit it. Replay the queue while still holding the holder lock (`event` does not take it), then set `Known`.
- No gate design was attempted. The spec's ceiling paragraph matches `review-plan.md` step 4.

Disposition: revise (keep scope). B3 is a small fix in `src/turn.rs`/`src/local.rs` plus one named test; N6 to N8 are cheap.

Validation (every block extracted verbatim from `spec01.md` and run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "$(cat blockN.sh)"`, cwd = each clone; the default isolated `CARGO_TARGET_DIR` is inside the clone):

- base block 1 → exit 1, 0 s.
- base block 2 → exit 1 (`21 passed`, first named local test missing), 8 s.
- ref block 1 → exit 0, 0 s.
- ref block 2 → exit 0, 11 s (all 11 names `... ok`, `socket::`/`audio::` present, clippy clean).
- ref `cargo test --lib` ×5 → `31 passed; 0 failed` each time, 3.4 s. Each of the 21 base test names reports `... ok` in the reference, including `service::tests::an_unknown_provider_fails_the_voice_call_before_any_dial` with `"carrier-pigeon"`.
- Probes in `reviewer-localtransport-2/probe`: mutations (a), (b) and (c) → FAILED as listed. The cadence probe → FAILED (B3).
- Live `live.ctg` was never written: `git status --short` is empty.

Reviewer identity: reviewer-localtransport-2 (independent review sub-agent, Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (85/100, one blocking finding).
Unresolved blocking findings: B3.
Rounds used / remaining: 2 / 3.
Next action: revise `spec01.md` and the reference to fix B3: judge silence by energy, add a named cadence test and put it in Verify block 2. Correct the two docs claims. Fold in N6 to N8. Then request round 3.

## Round 3 — 2026-09-19

Presented revision: `live.ctg` HEAD `6922a8f` (live checkout clean before and after). The reference is the analyst's `scratchpad/analyst-pipeline/live-probe` diff plus its untracked `src/local.rs` and `src/turn.rs`, applied onto a fresh `git clone --local` at `scratchpad/reviewer-localtransport-3/ref`. The base clone is `.../reviewer-localtransport-3/base`, and mutation probes ran in `.../probe`. Analyst report: `analyst-child1-4.md`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `515ef8e00fc922f94d388420a6352e06a7d7d8eadfead8c12fcd898ec150bdc2` (body only: N6 paragraph appended) |
| Specs | `specs/spec01.md` sha256 `1972275d03fa81765e01146bd6d94a3efc1a7d3316a37f6338435bbfbbbc4919` |
| Material contracts/dependencies | parent `prd.md` sha256 `7a6ea0aefc00050385279caf3d0412e0eb0e4cd667f23b1182cb1a5ee312d043` (unchanged); `live.ctg@6922a8f` `src/service.rs` (`start_voice`, `event`, `delegated`), `src/socket.rs` (`on_event` is called only on the reader task, lines 183 and 190), `src/audio.rs` (`BATCH` 4800 at 24 kHz, about every 200 ms) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | B3 is fixed in the code. `Turn` counts quiet samples after speech, `local::connect` checks `committed(RATE)` after every frame, and `STALL` (1.5 s, about 7 capture batches) is only an arrival fallback. My continuous-cadence probe commits within 800 ms of speech. −2: "loud" is a single-sample peak above 400 (`any(|s| s.unsigned_abs() > 400)`), not energy. On a real microphone, one noise spike per 200 ms batch resets the count, and because frames keep arriving `STALL` never fires either (N9). |
| Ownership and reuse | 18 | Unchanged from round 2. `Config` defaults come from `local::Settings`, and dispatch is reused. The N7 skip is one check. −2: `send` no-op / kokoro ownership stays as documented, and the peak detector's replacement is owned by the turn-ends sibling but not named as a limit. |
| Dependencies and implementable slices | 19 | N6 is resolved: `prd.md` records the whole-file widening, body only, frontmatter untouched. The spec's steps line up with the diff one for one. −1: the spec's Step 3 says "five tests" and it is five, but box 11 (N7) has no step naming its proof. |
| Observable acceptance and baseline evidence | 14 | Blocks 1 and 2 are red on base and green on the reference, and all 15 names report `... ok`. −6: **B4**, the named B3 test does not test B3 (below). The N7 Acceptance box ("never opens the microphone") has no test at all: removing the `already_closed` return keeps all 36 tests green. |
| Failure, recovery and compatibility | 18 | N7 and N8 are correct on reading. Deadlock check for the N8 lock-across-flush: the order is `holder` → `live` in both the flush and the callback. `event()` never takes `holder`. `delegated` only `tokio::spawn`s. Neither transport's `Session` holds `on_event` (local: `{id, tx, closed}`; socket: reader task only), so no session method can re-enter the callback while `live` is held. No cycle, no await under the std lock. The GPT path is intact: all 21 base test names are `ok` in the reference. −2: N8 has no test (hard to reach deterministically, acceptable). The callback now holds `holder` across every `event()`, audio included, which serialises callbacks: harmless, but worth knowing. |
| Reviewer total | 87 / 100 | |

Findings and concrete revisions:

- **B3: fixed in code, not proven.** The diff reading and my probe (below) show the energy commit works at real cadence.
- **B4 (blocking): `speech_then_silence_at_real_capture_cadence_commits_a_turn` passes with the energy commit disabled.**
  - The test sends one loud batch, then four silent batches 200 ms apart, then *stops feeding*. `wait_for` waits up to 6 s.
  - Once the frames stop, the `STALL` arrival fallback commits after 1.5 s. So the test passes whichever path commits, including round 2's broken 350 ms arrival-only design.
  - Mutation probe: `if false && turn.committed(...)` → this test `... ok` (2.33 s).
  - The spec's claim that "a regression back to an arrival-judged timeout fails it the same way it fails a live microphone" is false.
  - Revision: keep feeding silent batches at 200 ms for longer than `STALL` (for example 8 or more batches), and assert the transcript is present *before* the feed stops, without the long `wait_for`. Or assert the commit lands within about 1 s of the loud frame while frames are still arriving.
  - My probe `probe_cadence_continuous` (1 loud frame + 7 silent × 200 ms, assert straight away) FAILED under the mutation and passed on the fixed code, so this shape discriminates.
- N7: implemented, but its Acceptance box has no proof. Add an assertion to `a_local_sessions_missing_model_reaches_status` that no voice was opened, for example via `audio::fake`'s open count or a `voice` field in `status`. Or drop the box to a diff-reading note.
- N8: implemented, and no deadlock (analysis above). No test; the diff reading is the backstop.
- N9: judge "loud" by RMS over the frame, not by any single sample above 400. Or say in the docs that a noisy room may never commit, until the turn-ends sibling replaces it.
- Docs no longer overclaim: all three describe content-judged silence and `STALL` as a stall-only fallback. README's "exercise the pipeline end to end" is now true in a quiet room (see N9).
- No gate design was attempted. B4 is a test that proves the wrong thing, not a beatable gate, so the step-4 ceiling does not apply.

Disposition: revise (keep scope). B4 is a change of a few lines to one test, plus the matching sentence in the spec.

Validation (blocks extracted verbatim from `spec01.md`, each run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "$(cat blockN.sh)"`, cwd = each clone):

- base block 1 → exit 1, 0 s.
- base block 2 → exit 1, 5 s (`21 passed`, first named local test missing).
- ref block 1 → exit 0, 0 s.
- ref block 2 → exit 0, 15 s with a cold isolated target (all 15 names `ok`, `socket::`/`audio::` present, clippy clean).
- ref `cargo test --lib` ×3 → exit 0, `35 passed; 0 failed` each time, 4.51 s. No flakiness.
- Base `cargo test --lib` → 21 names `ok`, and all 21 appear in the reference run.
- Probes in `probe`:
  - energy commit disabled → the named B3 test `ok` (B4) and `probe_cadence_continuous` FAILED.
  - fixed code → both `ok`.
  - `already_closed` return removed → 36/36 green (N7 untested).
  - lock dropped before replay → 36/36 green (N8 untested).
- Live `live.ctg` was never written: `git status --short` is empty at `6922a8f`.

Reviewer identity: reviewer-localtransport-3 (independent review sub-agent, Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (87/100, one blocking finding).
Unresolved blocking findings: B4.
Rounds used / remaining: 3 / 5 (2 remaining).
Next action: rework the cadence test so it keeps feeding silent 200 ms batches past `STALL` and asserts the commit while they are still arriving. Confirm it goes red with `committed` disabled. Correct the spec's claim about it. Prove or drop the N7 box, and address N9 in code or docs. Then request round 4.

## Round 4 — 2026-09-19

Presented revision: `live.ctg` HEAD `6922a8f` (live checkout clean before and after). The reference is the analyst's `scratchpad/analyst-pipeline/live-probe` diff (sha256 `1af8bdfb…2dca02`) plus its untracked `src/local.rs` (`98736a3a…5f3633`) and `src/turn.rs` (`b43a71e4…d729a`). It was applied onto fresh `git clone --local` copies at `scratchpad/reviewer-localtransport-4/{ref,mutant}`, and the base is `.../base`. Analyst report: `analyst-child1-5.md`, re-run here, not trusted.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `515ef8e00fc922f94d388420a6352e06a7d7d8eadfead8c12fcd898ec150bdc2` (unchanged since round 3) |
| Specs | `specs/spec01.md` sha256 `5b83cf700d3aa2dbe1a6187c564e92a7331c08b291b84c62c113bc57be5cd387` |
| Material contracts/dependencies | parent `prd.md` sha256 `7a6ea0aefc00050385279caf3d0412e0eb0e4cd667f23b1182cb1a5ee312d043` (unchanged); `live.ctg@6922a8f` `src/service.rs`, `src/transport.rs`, `src/audio.rs` (`BATCH` 4800 at 24 kHz); `prd.ctg/src/lifecycle.ts` (`verify`, `testBlock`, `passedTests`); `templates/spec.md` (working tree, which carries the uncommitted `test`-block guidance) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The placeholder now commits at real capture cadence, and a test proves it (below). −2: N9 is documented in `.cartridge/docs/README.md` only. README.md still says "exercise the pipeline end to end" without saying that a noisy room may never commit. |
| Ownership and reuse | 18 | Unchanged. `Config` defaults come from `local::Settings`, the `Transport` enum dispatches, and the seams are plain functions. `listening` is a one-field addition to `status` that avoids touching `src/audio.rs`, which is out of the footprint. −2: `send` stays a no-op until kokoro, and the single-sample detector's replacement is owned by the turn-ends sibling. Both are documented, neither is fixed. |
| Dependencies and implementable slices | 19 | Steps 3, 4 and 7 match the diff one for one. Step 7 now names N7's proof (`listening == false`), which closes round 3's −1. `needs` is satisfied. −1: the `STALL`/`SILENCE` constants and the 1 s test deadline are coupled with no comment tying them together in `turn.rs`. The test's own comment covers it. |
| Observable acceptance and baseline evidence | 18 | **B4 is fixed.** On the mutant (`if false && turn.committed(…)`), block 2 exits 1, and the only failure is `speech_then_continuous_silence_at_real_capture_cadence_commits_before_a_stall_would` (panic at `local.rs:606`, 34 passed, 1 failed). On the reference the test passes in 0.62 s. The N7 mutant (the `already_closed` return removed) fails only `a_local_sessions_missing_model_reaches_status` at the `listening` assertion (`service.rs:1539`). All 15 names report `ok`. −2: Acceptance box 9 says all three docs describe the timeout and the turn-timing placeholder, including single-sample sensitivity, but README.md and `.cartridge/help.md` describe neither (N10). |
| Failure, recovery and compatibility | 18 | GPT path: every one of the 21 base test names reports `... ok` in the reference. Reading the diff, `Live` is inserted before the flush, the lock order is holder → live everywhere, and the one GPT-visible change is `voice` set after insert (plus the new `listening` field). −2: N8 is still untested, with the diff reading as backstop. The cadence test's margin is about 400 ms (commit at about 600 ms against a 1 s deadline). It held 18 of 18 runs, 5 of them with all 10 cores pinned by `yes`, but it is timing-based (N12). |
| Reviewer total | 91 / 100 | |

Findings and concrete revisions:

- **B4: resolved and verified.** A background feeder keeps sending silent 4800-sample batches every 200 ms for 2.4 s. The foreground bounds the commit to 1 s, which is less than `STALL` (1.5 s), so only the energy path can pass. The mutant goes red and the reference goes green (block 2 exit codes below). The spec's claims (Acceptance box 7 and Step 4, "fails this test (and no other)") match what I observed.
- **N7: resolved.** It is proven by the `listening` assertion, and the mutation turns it red.
- N8: accepted as diff-read only. I re-read the lock order: callback holder → `event` → live; flush holder → `event` → live; the `already_closed` check takes live only. No cycle.
- N9: accepted as documented, not fixed. That is reasonable for a placeholder the turn-ends sibling replaces.
- N10 (non-blocking): either narrow Acceptance box 9 to `.cartridge/docs/README.md` for the timing and timeout details, or add one line each to README.md (next to "end to end") and `.cartridge/help.md` naming the content-judged placeholder, its noisy-room limit and the 3 s per-call timeout.
- N11 (non-blocking): the working-tree `templates/spec.md` now asks for a `test` block (`run:` plus `pass:` lines) rather than a hand-rolled census. `lifecycle.ts` supports both, and the `sh` census works as written. Consider converting block 2's name list into a `test` block, keeping the `socket::`/`audio::` presence checks and clippy in `sh`.
- N12 (non-blocking): the cadence test's deadline has about 400 ms of slack. If it ever flakes under CI load, raise the deadline toward 1.2 s. That is still below `STALL`, so the test still discriminates.

Disposition: keep. Proceed to implementation.

Validation (blocks extracted verbatim from `spec01.md`, each run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "$(cat blockN.sh)"`, cwd = each clone, with the block's own isolated `CARGO_TARGET_DIR` inside the clone):

- base block 1 → exit 1; ref → exit 0; mutant → exit 0 (shape only).
- base block 2 → exit 1, 12 s (`21 passed`, "missing or failing test: local::tests::a_session_starts").
- ref block 2 → exit 0, 23 s cold (all 15 names `ok`, `socket::`/`audio::` present, clippy clean).
- mutant (energy commit disabled) block 2 → exit 1, 22 s. The cadence test is the only FAILED test (34 passed, 1 failed).
- ref `cargo test --lib`: ×3 → `35 passed; 0 failed` each run, 4.5 s. A further ×5 with 10 `yes` burners pinning every core → 35/35 each run. The cadence test alone ×10 → 10/10 ok, 0.62 s each.
- The 21 base test names (`base.names`) are all a subset of the reference's `ok` names (`comm -23` is empty). `carrier-pigeon` is in both the service and transport tests.
- N7 mutant (`already_closed` return removed, energy commit restored) → 34 passed, 1 failed: `a_local_sessions_missing_model_reaches_status` at the `listening` assertion.
- Live `live.ctg` was never written: `git status --short` is empty at `6922a8f`.

Reviewer identity: reviewer-localtransport-4 (independent review sub-agent, Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: PASS (91/100, no blocking finding).
Unresolved blocking findings: none.
Rounds used / remaining: 4 / 5 (1 remaining).
Next action: proceed to implementation from `spec01.md` as reviewed. Fold N10 and N11 in cheaply at implementation time if the coordinator chooses; neither changes behaviour.
