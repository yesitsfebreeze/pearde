---
complexity: medium
footprint:
  - src/lib.rs
  - src/service.rs
  - src/local.rs
  - src/turn.rs
  - src/transport.rs
  - cartridge.json
  - Cargo.toml
  - Cargo.lock
  - README.md
  - .cartridge/help.md
  - .cartridge/docs/README.md
---

# spec01 — Three seams, stub implementations, no model runtime yet

Base: `live.ctg` at `6922a8f` (`provider` already exists on `Config` and
accepts only `"gpt"`; `src/local.rs`/`src/turn.rs` do not exist).
`src/service.rs` is in this footprint as a whole file, per the coordinator's
round-2 decision recorded in `prd.md`'s "Footprint widened" section: round 1
review found that a local failure never reaches `status` (B1) and that the
four settings do nothing (B2), and both fixes need more than the one test
literal round 1 already covered. `start_voice` still calls `Transport::open`
generically (`src/service.rs:276`) and `event` still dispatches by name
unmodified (`src/service.rs:544-616`) — B1 changes *how* `start_voice` wires
its own callback to `event`, not that dispatch itself.

`src/transport.rs` gains `Provider::Local` and `Transport::Local`, selected
the same way GPT already is: `Provider::parse(&config.provider)?`. The local
branch now reads `config.models`/`config.stt`/`config.tts`/`config.brain`
(new `Config` fields, round 2) and builds `local::Settings` from them — round
1's `local::Settings::default()` call, which made the manifest's settings
inert (B2), is gone.

`stt` and `tts` are each either a model filename resolved under `models`
(checked for existence before any dial; missing closes the session through
`error` naming the file, then `session.closed`) or a literal `http(s)://`
endpoint standing in for the model — the seam sibling PRDs replace with real
whisper.cpp/Kokoro inference without moving. `brain` is always an
OpenAI-shaped `chat/completions` endpoint, dialled with a bounded client
timeout (round 2, N2) so an endpoint that accepts and never answers closes
the session instead of hanging the turn forever.

**B3, the round-2 blocking finding, in full:** round 2's own N1 fix judged
silence by *arrival* — `timeout(SILENCE, rx.recv())` — which never elapses
against real capture: `src/audio.rs` delivers a `BATCH` (a fifth of a second)
roughly every 200 ms for as long as the microphone is open, silent or not, so
the gap between two arrivals never grows past ~200 ms and the timeout in
round 2's 350 ms never fires. Round 1's 30 ms committed on every batch;
round 2's 350 ms committed on none — a live session simply never ends a
turn. Round 3's fix judges silence by what a frame *carries*: `Turn` counts
low-energy samples since the last loud one and `committed(sample_rate)` is
true once that count reaches a fixed window, `turn::SILENCE` (600 ms of
samples). The loop in `local::connect` now checks `committed` after every
frame instead of waiting on a timeout for the commit itself; a separate,
longer arrival timeout, `turn::STALL` (1.5 s), still exists, but only to end
a turn if the capture stream stops delivering frames at all — well above the
~200 ms cadence a live microphone actually delivers at, so it is a stall
detector, not the commit path.

Both documentation claims the round-2 review named are corrected: the
`.cartridge/docs/README.md` paragraph now describes silence judged by
content, not arrival, and no longer implies a raised timer alone fixes a
live microphone.

**B1, the round-1 blocking finding, in full:** `local::connect`'s own
callback can fire (`session.started`, then `error`/`session.closed` on a
missing model) before `start_voice` has recorded the session's id, because
that id only becomes known once `Transport::open` returns. The old callback
silently dropped any event that arrived before the id was known, and
`event()` itself silently drops anything for an id it has no `Live` entry
for yet — two places an early event could vanish, not one. Round 2's fix in
`start_voice`: a `Buffered` enum (`Pending(Vec<Value>)` before the id is
known, `Known(String)` after) replaces the plain `Option<String>` holder;
the callback queues into `Pending` instead of discarding, and once
`Transport::open` returns, `start_voice` inserts the `Live` entry *first*,
then flushes the queued events through the normal `event()` path in arrival
order, then proceeds to open the microphone as before. This also closes the
same theoretical race for `gpt`, though round 1 only observed it on `local`.

No model, no daemon and no network beyond loopback are needed to run the
tests: two hand-rolled `127.0.0.1:0` listeners stand in for the speech stage
(one route each for transcribe/speak) and the brain; the refused-endpoint
test binds a listener only to reserve a port, then drops it; the
never-answers test (N2) accepts a connection and leaks the socket so nothing
ever completes it; the cadence test (B3, see below) keeps feeding frames in
the background for longer than `turn::STALL` while asserting a commit lands
well before that — under two seconds of real wall-clock time, well inside
the 120 s budget.

**B4, the round-3 blocking finding, in full:** round 3's own cadence test,
`speech_then_silence_at_real_capture_cadence_commits_a_turn`, sent one loud
batch, four silent batches 200 ms apart, then *stopped feeding* and waited
up to 6 s. That let `turn::STALL`'s arrival fallback commit the turn 1.5 s
after the feed stopped, so the test passed whether the energy commit worked
or not — proven by mutating `turn.committed(...)` to `false && …` and
watching the same test still report `... ok`. The spec's own claim that this
test "fails it the same way it fails a live microphone" was false. Round 4's
fix, renamed to
`speech_then_continuous_silence_at_real_capture_cadence_commits_before_a_stall_would`:
a background task keeps feeding silent batches at the real ~200 ms cadence
for 12 iterations (2.4 s, comfortably past `turn::STALL`'s 1.5 s) while the
foreground asserts the commit lands within 1 s — shorter than `STALL`, so
only the energy path can satisfy it. Verified both ways on the reference: the
same `turn.committed(...)` → `false && …` mutation now makes this test FAIL
(`panicked … an energy-judged commit must land within 1 s …`, "session.started"
only), and the unmutated code passes it in ~0.6 s.

## Acceptance

- [ ] `cartridge.json` declares `stt`, `tts`, `brain` and `models`, each with a documented default; `provider` still defaults to `gpt`.
- [ ] `src/transport.rs` accepts `"local"` (`Provider::Local`) alongside `"gpt"`; an unrelated value is still refused before any dial.
- [ ] Driven directly through `local::connect` with a stub speech endpoint (transcribe + speak routes) and a stub brain endpoint on `127.0.0.1:0`, the session emits `session.started`, `session.input_transcript.delta`, `session.output_transcript.delta`, `session.output_audio.delta` in that order, and the audio delta decodes to exactly the PCM the stub tts route returned.
- [ ] A brain reply carrying a `delegate` tool call emits `session.delegation.created` with `delegation.target == "client"` and no `session.output_audio.delta` for that turn.
- [ ] A missing model file, and an endpoint that will not answer (refused outright, or accepted and left hanging), each close the session through the `error` event carrying the reason, which `status` then reports — neither panics. (Restored verbatim from the PRD/parent Acceptance; round 1's spec had dropped "which `status` then reports" and tested only through `local::connect`, which is exactly how B1 went unseen.)
- [ ] A non-default `models` setting is honoured: the reason `status` reports names the *configured* directory, not a hard-coded one.
- [ ] A turn commits within 1 s while speech is followed by silence delivered continuously at real capture's own ~200 ms cadence — past the point `turn::STALL`'s arrival fallback would ever fire — not only from a single burst followed by nothing; the placeholder is judged by frame content, not by a gap in arrivals, and a mutant that disables the content judgement fails this specific test.
- [ ] Nothing in `src/local.rs` or `src/turn.rs` is conditional on the operating system: no `cfg(target_os)`, no `Command::new`/`std::process::Command`.
- [ ] `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md` describe the four settings, the three seams, the timeout and the turn-timing placeholder (content-judged, not arrival-judged, and sensitive to a single loud sample rather than a frame's energy) accurately, and where model files come from.
- [ ] `cargo test --lib` passes for the whole crate, including the existing `socket`/`audio` suites and the one adjusted `service` test, unchanged in intent.
- [ ] A local session already closed by a queued failure never opens the microphone, and `status` can show it: a mutant that removes the guard fails the named test that checks this.

## Steps

1. `cartridge.json`: `stt`, `tts`, `brain`, `models` settings with the documented defaults above; extend `provider`'s doc to mention `local`; add `127.0.0.1` to `grant.net` beside `api.openai.com`.
2. `Cargo.toml`: `reqwest` (`default-features = false`, `rustls-tls`, `json`), reusing the `rustls` already in the tree; add `net` and `io-util` to the existing `tokio` feature list (needed only by the test-only stub HTTP servers).
3. `src/turn.rs`: `Turn` now tracks `quiet_samples` alongside `heard_speech`; `hear` resets the count on a loud frame and grows it on a quiet one after speech; `committed(sample_rate)` compares that count against `SILENCE` (600 ms) converted to samples; `STALL` (1.5 s) is the separate, longer arrival-only fallback. Five tests: the original two plus three for the energy accounting (enough quiet commits, too little does not, speaking again mid-pause resets the count).
4. `src/local.rs`: `Settings`, `Source` (endpoint vs. model-file), `Session`, `connect`, and the STT → brain → TTS turn pipeline with the error/close path, a bounded `reqwest::Client` timeout (N2), a settle wait in the delegation test before asserting no audio followed (N3), and the loop's commit check moved from the timeout arm to right after every frame via `turn.committed(crate::audio::RATE)`, with `turn::STALL` as the arrival branch's new, longer timeout; eight named tests, including
   `speech_then_continuous_silence_at_real_capture_cadence_commits_before_a_stall_would`
   (B3/B4): one loud batch, then a background task feeding silent batches at
   a real 200 ms cadence for longer than `turn::STALL`, while the foreground
   asserts the commit lands within 1 s — shorter than `STALL`, so only the
   energy path can pass it. Verified by mutation: `turn.committed(...)` →
   `false && …` makes this test fail (and no other); reverting makes it pass
   in ~0.6 s.
5. `src/transport.rs`: `Provider::Local`, `Transport::Local` built from `config.models`/`stt`/`tts`/`brain`; both `Transport::open`'s and `local::connect`'s callback bound widened to `Send + Sync + 'static` (the spawned turn-processing task holds the callback across an `.await`, which a bare `Send` closure cannot cross by reference); one new test, one existing test's fixture literal changed from the now-meaningless `"local"` to `"carrier-pigeon"`.
6. `src/lib.rs`: `mod local; mod turn;`.
7. `src/service.rs`: add `models`/`stt`/`tts`/`brain` to `Config`, sourcing `Config::default()`'s values from `local::Settings::default()` so the two cannot drift; replace the `Option<String>` id holder in `start_voice` with the `Buffered` enum described above, reorder the `Live` insert before the flush (B1), hold the holder's lock for the *entire* flush rather than releasing it after the swap to `Known` (N8 — closes the window where a fresh event could dispatch ahead of still-queued older ones), and skip `Voice::start` (and the greeting) when the entry the flush just left is already `closed` (N7 — a queued failure should not still open a microphone nothing will read from); add a `"listening": entry.voice.is_some()` field to `status()`'s per-session shape so N7 is externally observable without touching `src/audio.rs` (out of footprint); change `provider: "local".into()` to `provider: "carrier-pigeon".into()` in `an_unknown_provider_fails_the_voice_call_before_any_dial`; extend `a_local_sessions_missing_model_reaches_status` (proving B1+B2) with a `listening == false` assertion proving N7 — verified by mutation: removing the `already_closed` guard makes this one assertion fail.
8. `README.md`, `.cartridge/help.md`, `.cartridge/docs/README.md`: document the four settings, the three seams, the per-call timeout, the turn-timing placeholder's real (content-judged, not arrival-judged) relationship to `audio.rs`'s batching, that a single loud sample rather than a frame's energy decides "loud" so a noisy room can reset the quiet count (N9, documented rather than fixed — an RMS/energy replacement is more than a placeholder needs and the turn-ends sibling replaces the whole mechanism regardless), and that `send` is a no-op for `local` until `kokoro-speaks-through-onnx-runtime-or-refuses-the-model-it-needs` gives it something to speak through (N4).
9. `prd.md`: append one paragraph to the existing "Footprint widened" body section recording that the round-2 widening was the whole file, not the one line the section's original text still said (N6) — frontmatter untouched, body only.
10. Last, run Verify block 2's command exactly as written: it proves the tests and warms the isolated target directory the block itself pins.

Not changed here, and said plainly rather than fixed: N5 (linking the
turn-taking sibling's `needs` to this child) was resolved by the coordinator
directly, per round 2's review — footprint and `needs` on another PRD were
never this spec's to edit. N8 gets no test: round 3's own review called it
"hard to reach deterministically" after confirming by inspection there is no
deadlock and no reachable window in the code as written (holder → live lock
order is the same in the flush and the callback; neither transport's session
type holds `on_event`, so no session method can re-enter it); the diff
reading stays its backstop, not a flaky timing test manufactured to exercise
a window that may not be schedulable at all under `tokio`'s cooperative
scheduler.

## Verify and Proof

<!--
Engine facts (`prd.ctg/.cartridge/templates/spec.md`): `sh -eu -c`, 120 s each,
first in the lane and then in `repo`, paths relative to the repo root, every
cargo command sets its own isolated `CARGO_TARGET_DIR` inside the block.

Honest ceiling, per `review-plan.md` step 4: this spec's sibling
(`a-setting-chooses-the-transport-and-the-gpt-one-keeps-working/review.md`)
spent five rounds and a dedicated gate round discovering that a textual or
structural gate — matching a function's body, requiring an `assert`, pinning
a `find`-first substring — is beatable by a test whose body doesn't assert
the claimed behaviour, no matter how the gate is sharpened; the round-5 gate
round settled on naming the executed test in the runner's own output and
letting a reviewer's diff reading be the backstop for whether that name's
body actually asserts what it claims, and recorded that a further-sharpened
gate (F24) still falls to a one-line decoy. This spec does not attempt a new
anti-cheat gate: block 2 runs the real suite, requires each named test to
report `... ok` in cargo's own output, and stops there. What it does not
prove — that a test's assertions can't be quietly weakened while keeping its
name and its `ok` — is exactly what the ceiling says a Verify block cannot
prove, and the collecting reviewer's diff reading is the named backstop.

Round 2 note: round 1's own ceiling paragraph was honest about the gate, but
round 1's *Acceptance* itself had quietly narrowed the claim (dropping
"which `status` then reports" and testing only through `local::connect`),
which is a different failure than a beatable gate — B1 was true and
unproven, not proven and beatable. The fix is not a stronger gate; it is
testing the same claim the PRD actually makes, one layer up, through
`Service`/`status()`, which round 2's block 2 now names.

Round 3 note: B3 was the same shape again, one layer down — round 2's own
N1 fix was a real revision, reviewed and merged, but nobody ran it at the
cadence a live microphone actually delivers at, so a timer that looked
plausible in isolation (30 ms too short, then 350 ms "safely longer")
never elapses in practice either way. The fix that round added a named test
driving the *loop in `local.rs`* at real cadence instead of a single
synthetic burst — the right shape, but not yet the right assertion (below).

Round 4 note (B4): the round-3 test drove the right shape and then asked the
wrong question — it stopped feeding and waited, so `turn::STALL`'s own
arrival fallback could commit the turn 1.5 s later and the test could not
tell that path from the energy path it meant to prove. This is not a
beatable gate in the step-4 sense (nobody had to shape a decoy; the test
simply asserted too little), so no gate was designed — the fix is asking the
test to prove the *specific* claim (a commit while frames are still arriving,
inside a deadline `STALL` cannot reach) and confirming by mutation that only
the intended code path satisfies it, which is the same discipline this
spec's own ceiling paragraph already asks of the reviewer's diff reading.
-->

```sh
# Shape and manifest.
test -f src/local.rs
test -f src/turn.rs
grep -q 'Provider::Local' src/transport.rs
grep -q '"local" => Ok(Provider::Local)' src/transport.rs
if grep -q 'cfg(target_os' src/local.rs src/turn.rs; then
  echo "src/local.rs or src/turn.rs is conditional on an operating system"
  exit 1
fi
if grep -qE 'Command::new|std::process::Command' src/local.rs src/turn.rs; then
  echo "src/local.rs or src/turn.rs spawns a platform binary"
  exit 1
fi
bun -e 'const m = await Bun.file("cartridge.json").json();
const settings = m.settings ?? {};
for (const key of ["provider", "stt", "tts", "brain", "models"]) {
  if (settings[key]?.default === undefined || !settings[key]?.doc) {
    console.error("setting missing, undocumented or without a default: " + key);
    process.exit(1);
  }
}
if (settings.provider.default !== "gpt") {
  console.error("provider must default to gpt, is " + settings.provider.default);
  process.exit(1);
}
for (const file of ["README.md", ".cartridge/help.md", ".cartridge/docs/README.md"]) {
  const text = await Bun.file(file).text();
  for (const word of ["provider", "stt", "tts", "brain", "models"]) {
    if (!text.includes(word)) {
      console.error(file + " does not document " + word);
      process.exit(1);
    }
  }
}'
```

```sh
# Behaviour. Each named test must appear as passing in cargo's own output: an
# exit code alone cannot tell a passing suite from an empty one.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/the-local-transport-verify}"
out="${TMPDIR:-/tmp}/live-local-transport-test-$$.txt"
cargo test --lib > "$out" 2>&1 || { cat "$out"; rm -f "$out"; exit 1; }
for t in local::tests::a_session_starts \
         local::tests::events_arrive_in_order_with_the_stubs_own_pcm \
         local::tests::a_delegate_tool_call_is_a_delegation_with_no_audio \
         local::tests::a_missing_model_file_closes_the_session_before_any_dial \
         local::tests::a_refused_endpoint_closes_the_session_without_a_panic \
         local::tests::an_endpoint_that_accepts_and_never_answers_still_closes_the_session \
         local::tests::speech_then_continuous_silence_at_real_capture_cadence_commits_before_a_stall_would \
         turn::tests::silence_alone_is_not_a_turn \
         turn::tests::a_loud_frame_marks_speech \
         turn::tests::speech_then_enough_quiet_samples_commits \
         turn::tests::speech_then_a_short_quiet_frame_does_not_commit \
         turn::tests::quiet_samples_reset_on_the_next_loud_frame \
         transport::tests::local_is_a_known_provider \
         service::tests::an_unknown_provider_fails_the_voice_call_before_any_dial \
         service::tests::a_local_sessions_missing_model_reaches_status; do
  if ! grep -q "$t \.\.\. ok" "$out"; then
    echo "missing or failing test: $t"
    cat "$out"
    rm -f "$out"
    exit 1
  fi
done
# What this child did not change still runs, and nothing failed.
grep -q 'socket::tests::' "$out"
grep -q 'audio::tests::' "$out"
if grep -qE '^test result: FAILED' "$out"; then
  cat "$out"
  rm -f "$out"
  exit 1
fi
rm -f "$out"
cargo clippy --all-targets -- -D warnings
```
