# analyst-1 — @live/voice-runs-headless-on-the-microphone

2026-09-16. Analyst for coordinator `coordinator-cartridge-1b-1`.
Source of record: `live.ctg` `f8082627c21e4e1107360e51bc7792cd1d8ff0d7`, confirmed
HEAD, `git status --porcelain` empty. Footprint as briefed
(`src/**`, `.cartridge/**`, `cartridge.json`, `init.lua`). Nothing was written to
the live checkout; all probing happened in a detached scratch worktree.

**Verdict: QUESTION.**

## The finding that drives everything below

The three ticks were not earned by a session that did the work and then ticked
them. They arrived **already ticked in the planning commit that created the
PRD** — `prd.ctg 808dff09`, "Advance planning: auth and live boards, verify-block
rules in the template". `git log -p --follow` on `prd.md` has exactly one commit,
and its `+` lines are boxes 1, 2 and 4 already carrying `[x]`.

They were true at the time, of a **TypeScript** cartridge that no longer exists.
Three commits later that cartridge was deleted and replaced:

- `780dd89` "Speak from the host itself and drop the HTTP surface"
- `7d89976` "Record the TypeScript live cartridge before the Rust rewrite"
- `d782360` "Hold the microphone and the speaker in the cartridge itself"

At `7d89976` the cartridge matched the PRD's Outcome word for word:
`cartridge.json` `grant.exec` was `["bun","mkfifo","ffmpeg","ffplay",…]`, `needs`
contained `auth.live`, and `.cartridge/tests/integration/voice.test.ts` (111
lines) drove the service against a mock `auth.live` and injected
`capture`/`playback`. At `f808262` **none of that is in the tree.** The
microphone and the speaker are `cpal` streams in this process (`src/audio.rs`),
the socket is opened here (`src/socket.rs:92-108`), the credential is discovered
here (`src/socket.rs:22-49`), `grant.exec` is `["tmux"]` and the manifest instead
declares `"audio": true` (`cartridge.json:162-168`). No file in `src/`,
`cartridge.json` or `init.lua` contains the strings `auth.live`, `ffmpeg`,
`ffplay`, `mock` or `fake` (`grep -rn`, exit 1).

So the PRD is written against a design the repository deliberately abandoned,
and the rewrite regressed two of the three ticked boxes to nothing.

## Per-box audit against `f808262`

### Box 1 — "Enabling voice starts capture and a session; disabling stops capture, playback and the session within 2 s, leaving no `ffmpeg`/`ffplay` process." — PARTLY IMPLEMENTED, UNPROVEN, AND ITS LAST CLAUSE IS NOW VACUOUS

Implemented: `src/service.rs:205-222` is the `voice` op; `:224-271`
`start_voice` opens the socket (`:232`) and then the devices
(`src/audio.rs:98-117` via `service.rs:243`); `:277-289` `stop_voice` removes the
`Live` entry and calls `entry.session.close()` (`src/socket.rs:75-77`), and
dropping the entry drops `Voice`, whose `Drop` (`src/audio.rs:126-130`) sets the
stop flag that `run()` reads on a 50 ms tick (`src/audio.rs:157-158`), after
which both `cpal` streams are dropped on the audio thread.

Not supported:

- **"within 2 s" is asserted, not measured.** No test calls `voice()` at all.
  `stop_voice` does not join the audio thread — `Drop` only stores a flag
  (`src/audio.rs:128`) — so the interval between the op returning and capture
  actually ceasing is nowhere bounded, observed or logged. A comment is not a
  measurement.
- **"leaving no `ffmpeg`/`ffplay` process" cannot fail.** The cartridge never
  spawns either binary at `f808262`, so the clause is true of a world it does
  not describe. This is precisely the shape the auth sibling's audit condemned:
  a clause that passes because nothing ever happened.

### Box 2 — "Transcripts and delegations from the WebSocket session land in the same store the WebRTC path used." — HOLDS BY INSPECTION; NO TEST

- Transcripts: `src/service.rs:415-434` maps
  `session.input_transcript.delta` / `session.output_transcript.delta` to a
  `Fragment` and `self.store().fragment(...)`.
- Delegations: `src/service.rs:435-443` routes `session.delegation.created` to
  `delegated()`, which persists the `Task` at `src/service.rs:490`
  (`self.store().save(&task)`).
- "the same store": `src/store.rs:80-91` creates `conversations`, `fragments`,
  `tasks`, `notes`, `lifecycle`, `voice_intent` and the two indexes with column
  definitions **identical** to the TypeScript store at
  `7d89976:src/store.ts:38-53`. (That file additionally created
  `context_ring`, `context_snapshots`, `agent_requests`,
  `context_access_events`, `graph_access`, `live_migrations`; the tables this
  box is about are byte-identical, and `src/store.rs:1-3` states the intent.)

This is the only ticked box the repository still supports. It is supported the
way box 3 of the auth sibling was: **by inspection only**. No test drives
`Service::event`; the five tests in `src/service.rs:963-1071` exercise `open`,
`note`, `spoken`, `commentary` and `transcript`, none of which reaches the
event router.

### Box 4 — "A test drives the service against a mock `auth.live` and fake capture/playback commands." — DOES NOT HOLD. The test was deleted by the rewrite.

`cargo test --lib` at `f808262`: **11 tests, all passing** (`src/audio.rs` 3,
`src/socket.rs` 3, `src/service.rs` 5). Not one of them:

- starts a server, binds a port or opens a socket — `socket::connect`
  (`src/socket.rs:82-177`) is never called from a test;
- opens or fakes a device — `Voice::start` (`src/audio.rs:98`) is never called
  from a test;
- mentions `auth.live` — the cartridge does not reach `auth.live` at all any
  more; `src/socket.rs:22-49` reads `OPENAI_API_KEY`, then
  `<credentials>/credentials.json`, then `$XDG_CONFIG_HOME/cartridge/…`, then
  `~/.codex/auth.json`, and `src/socket.rs:92-108` dials
  `wss://api.openai.com/v1/live/sessions` directly;
- drives the `voice` op, `start_voice`, `stop_voice` or `event`.

The nearest thing to what the box claims is `socket::tests::the_environment_key_wins`
(`src/socket.rs:210-216`), which sets a dummy `OPENAI_API_KEY` and reads it back.
The box's own subject — the service, a mock `auth.live`, fake capture and
playback — has **zero** coverage. This is stronger than the auth sibling's
finding: there the test existed and was weak; here the test was deleted with the
cartridge it tested and `7d89976:.cartridge/tests/integration/voice.test.ts` is
the only place it still lives.

Two further notes on that recoverable file: its capture/playback were **injected
`VoiceDeps` functions, not commands** (`7d89976:…/voice.test.ts:38-41`), so even
the original tick read "commands" loosely; and its `FakeSocket`
(`…/voice.test.ts:11-17`) is the same in-process fake the auth audit rejected.
Recovering it verbatim would re-tick box 4 on the shape that was already ruled
insufficient once.

## Box 3 — what it needs

`- [ ] grant.exec names ffmpeg and ffplay; missing binaries or microphone permission surface as a readable voice error in state.`

Two clauses, in opposite conditions.

**Clause A — `grant.exec` names `ffmpeg` and `ffplay` — is contradicted by the
landed design and cannot be specced without reversing it.** `cartridge.json:162-164`
is `"exec": ["tmux"]`, and `:168` is `"audio": true`. There is no binary to
grant: `src/audio.rs:182-241` opens the default output and input devices through
`cpal` in this process, on a thread of its own because a CoreAudio stream is not
`Send` (`src/audio.rs:5-8`). Adding `ffmpeg`/`ffplay` to `grant.exec` to satisfy
the letter of the box, while nothing spawns them, would be a tick on a grant with
no referent — the same unfailable shape as box 1's last clause.

**Clause B — a readable voice error in `state` — is a real, small, un-done gap,
and it survives the design change intact.** The machinery to produce the error
exists; the route to `state` does not:

- `src/audio.rs:182-241` returns `Err("no output device on this machine")`,
  `"no microphone on this machine"`, `"speaker: {e}"`, `"microphone: {e}"`;
  `src/service.rs:244-249` catches that and stores it as `Live.error` rather than
  failing the op ("A refused microphone is not a reason to drop the
  conversation").
- A device that fails *after* it opened lands in `Voice::failure`
  (`src/audio.rs:119-123`, set from the `cpal` error callbacks at
  `src/audio.rs:208` and `:235`).
- Both are surfaced **only** by `status` (`src/service.rs:160`), keyed by live
  session id.
- **`state` carries no error at all**: `src/service.rs:179-187` returns
  `conversation`, `voice` (the stored intent), `fragments`, `tasks`, `notes`.

So clause B needs: `state` to look up the `Live` entry for the conversation and
include `entry.error` / `Voice::failure()` — a few lines in
`src/service.rs:179-187` — plus a test that drives it. Nothing of it exists.

A macOS-specific wrinkle worth carrying into whatever spec follows: a denied
microphone **is not an error** on this platform. `src/audio.rs:179-181` records
that a microphone this process may not use delivers silence, so a denied grant
is indistinguishable from a quiet room. The box's "microphone permission
surfaces as a readable voice error" is therefore **not implementable as written**
against `cpal` on macOS without a separate permission probe (e.g. `AVCaptureDevice`
authorization status), which is new work and outside anything the current tree
does.

## Why QUESTION and not SPECCED

The routine reserves QUESTION for a material unresolved choice needing an
explicit answer, and says a failed command is failure evidence, not a question.
This is the former. The PRD's Outcome names `ffmpeg`, `ffplay` and `auth.live`;
the repository at `f808262` uses none of them, by a deliberate commit. To write
a spec that makes box 3 tickable I would have to choose, on the coordinator's
behalf, between:

- **(A) restate the PRD to the landed design** — drop `ffmpeg`/`ffplay` and
  `auth.live` from the Outcome; rewrite box 3 to the audio grant plus the `state`
  error; untick boxes 1 and 4 and rewrite them in terms of `cpal` streams and a
  fake transport rather than fake commands; leave box 2 ticked (it holds) or
  untick it for want of a test; or
- **(B) revert the rewrite's audio decision** — bring back `ffmpeg`/`ffplay`
  subprocesses and the `auth.live` session so the PRD text stands, recovering
  `voice.test.ts` from `7d89976`.

That is a product decision about what this cartridge *is*, not a technical
uncertainty, and it also decides the fate of `needs:
["@auth/gpt-live-connects-over-websocket-on-the-discovered-credential"]`, which
the code no longer honours.

**Recommendation: (A).** The rewrite is landed, tested as far as it goes, and
better on its own terms — no fifo, no two subprocesses, no PCM crossing a process
boundary, and a half-duplex gate (`src/audio.rs:82-86`, `:165-168`) that works
off the shared `Playback` clock in a way two piped binaries cannot. (B) throws
that away to preserve wording. Under (A) one spec then closes the whole
remainder: a test harness that drives `voice` enable/disable and `event` against
a loopback GPT Live service and a fake device layer, a measured stop bound, and
the `state` error field. I did not draft it, because its Acceptance would have to
restate boxes the coordinator has not yet rewritten.

## Commands, with observed exit codes

All run from the scratch worktree or from read-only inspection. Nothing wrote to
`/Users/feb/dev/cartridge/live.ctg`.

| # | Command (cwd) | Exit |
| --- | --- | --- |
| 1 | `git log --oneline -8` / `git status --porcelain` / `git rev-parse HEAD` (`live.ctg`) | 0 — HEAD `f808262`, tree clean |
| 2 | `git log -p --follow -- …/voice-runs-headless-on-the-microphone/prd.md` (`prd.ctg`) | 0 — one commit, `808dff09`, boxes created ticked |
| 3 | `git show 7d89976:cartridge.json` piped through `python3 -c json` (`live.ctg`) | 0 — `grant.exec` had `ffmpeg`,`ffplay`; `needs` had `auth.live` |
| 4 | `git show 7d89976:.cartridge/tests/integration/voice.test.ts` (`live.ctg`) | 0 — 111 lines, the deleted box-4 test |
| 5 | `git grep -ln "ffmpeg\|ffplay" 7d89976 -- .` (`live.ctg`) | 0 — 5 files then |
| 6 | `grep -rn "auth\.live\|mock\|fake\|127\.0\.0\.1\|localhost" src/ cartridge.json init.lua` (`live.ctg`) | **1** — no match at `f808262` |
| 7 | `grep -rn "#\[test\]" src/` (`live.ctg`) | 0 — 11 tests, in `audio.rs`, `socket.rs`, `service.rs` only |
| 8 | `git worktree add --detach <scratch>/live.ctg f808262` (`live.ctg`) | 0 |
| 9 | `CARGO_TARGET_DIR=<scratch>/target cargo test --lib` (scratch worktree) | 0 — 11 passed, 0 failed, 0.00 s |
| 10 | `pgrep -fl ffmpeg` / `pgrep -fl ffplay`, before the probe | 1 / 1 — none |
| 11 | positive control: `( exec -a ffplay-probe sleep 4 ) &` then `pgrep -fl ffplay` | **0** — matched `81159 ffplay-probe 4`; the pattern does match an argv-renamed process |
| 12 | after `kill`: `pgrep -fl ffplay` | 1 — none; no strays left |
| 13 | guard-shape check, run against a file **built to fail it**: `if grep -qn 'ffmpeg' bad.json; then exit 1; fi` on a file containing `ffmpeg` | **1** — the guard fires as intended |

Command 9's compile emitted no warnings under `[lints.rust] warnings = "deny"`.

## How the microphone and the credential were kept out of it

- **No device was opened.** `Voice::start` / `audio::open` were never invoked:
  the only test binary run was `cargo test --lib`, whose 11 tests are listed
  above and none of which reaches `src/audio.rs:98` or `:182`. Nothing played.
- **No stray processes.** Checked before and after with a pattern proven to
  match (row 11 of the table: `pgrep -fl ffplay` found a deliberately
  argv-renamed `ffplay-probe`, so a clean result is a real clean result, not the
  `cartridge daemon` mistake the sibling hit). Clean both times.
- **No credential was read, printed, spent or rotated.** `auth {op:"status"}`
  was not run. `~/.codex/auth.json`, `.cartridge/credentials`, the keychain and
  `security(1)` were not opened or invoked. `api.openai.com` was not contacted —
  `socket::connect` is unreachable from `cargo test --lib`. The one credential
  test that ran, `socket::tests::the_environment_key_wins`
  (`src/socket.rs:210-216`), sets and then removes its own literal
  `sk-from-the-environment` and reads a `/nowhere` config dir; it never touches
  a real store.
- **The project daemon was not started, stopped, replaced or reloaded.** All
  cargo work used `CARGO_TARGET_DIR` inside the scratchpad, so no dylib under
  `live.ctg/target` changed and nothing hot-restarted.
- **The live checkout was not written to.** The worktree was detached at
  `f808262` in the scratchpad; `live.ctg` remains clean.

## Artifacts and remaining work

- Scratch worktree: created detached at `f808262` under
  `…/scratchpad/voice-headless/live.ctg` with its own `…/voice-headless/target`,
  and **removed again** (`git worktree remove`, exit 0). `live.ctg` is back to
  `f808262` with `git status --porcelain` empty and no worktree registration of
  mine left; `git worktree list` shows only `main` and a pre-existing prunable
  `cartridge-worktrees/ws/live.ctg` that is not mine. Final `pgrep -fl ffmpeg`
  and `pgrep -fl ffplay` both exit 1.
- No `spec01.md` and no `attempt-1.patch` were written: SPECCED was not the
  verdict, and drafting Acceptance for boxes the coordinator has not yet decided
  the wording of would prejudge the question above.
- Reusable when the question is answered:
  `7d89976:.cartridge/tests/integration/voice.test.ts` as a **specification of
  the behaviours to cover** (enable → session config, the half-duplex gate, the
  audio delta path, disable → stop), not as a file to restore — its socket and
  device fakes are in-process and its "commands" are injected functions.

---

# analyst-1, second pass — SPECCED

2026-09-16, after the user answered **(A) restate the PRD to the landed design**
and, for box 3, **scope it to the errors that exist**. The PRD was re-read at its
rewritten revision (new Outcome, four boxes, `needs` dropped, `## Answer`
present). Source of record unchanged: `live.ctg` `f808262`, clean, and clean
again at the end.

**Verdict: SPECCED.**

- `…/.state/loop/voice-runs-headless-on-the-microphone/spec01.md`
- `…/.state/loop/voice-runs-headless-on-the-microphone/attempt-1.patch` —
  `src/audio.rs`, `src/service.rs`, `src/socket.rs`, 675 diff lines, no fourth
  file. `Cargo.toml` is **not** touched, which matters: it is outside the
  footprint, and `tokio/net` turned out to be already enabled through
  `tokio-tungstenite` (`cargo tree -e features`), so the loopback listener needs
  no dependency change.

Footprint unchanged and not widened: all three files are under `src/**`.

## What the spec does, in one paragraph

Two seams and nothing else faked. `socket::connect` takes its destination as an
argument instead of reading the constant, so the test drives the real handshake,
the real `session.start`, the real `session.started` wait and the real relay
tasks against a `tokio::net::TcpListener` on `127.0.0.1:0`. `audio::open`
becomes one `fn`-pointer `Opener` with `Box<dyn Any>` for the streams, so the
devices — the one thing safety forbids being real — are the only thing replaced,
and the resampling, batching, half-duplex gate and thread lifecycle above them
are shipped code. `Voice`'s `Drop` joins the audio thread, which is the
root-cause placement: every path that drops a `Voice` waits, not only
`stop_voice`. `state` gains the voice error, computed **before** the store guard
is taken because `event` takes the sessions then the store and the other order
would deadlock. `stop_voice` releases the session map before closing, so the
relay is not held up behind a 350 ms device close.

## Each box's denied world, constructed and observed

Nothing below is inferred. Each row is a tree that was actually built and run.

| Denied world | Construction | Observed |
| --- | --- | --- |
| M1 | `Drop for Voice` reverted to a bare flag | exit **101**, 14 passed / 2 failed; both stop tests, `left: [] right: ["speaker","microphone"]` |
| M2 | fixture accepts any non-empty bearer | exit **101**, 14 passed / 2 failed, incl. `a_key_the_fixture_does_not_know_never_opens_a_session` |
| M3 | `Session::audio` sends `session.input_audio.nowhere` | exit **101**, 15 passed / 1 failed, at the append that never arrives |
| M4 | `event` stops matching the transcript deltas | exit **101**, 15 passed / 1 failed |
| M5 | `state` reports `"error": Value::Null` | exit **101**, 15 passed / 1 failed |
| G1 | `Command::new("say")` added to `src/service.rs` | block 2 exit **1** |
| G2 | `"ffplay"` added to `grant.exec` | block 2 exit **1** |
| G3 | `"audio": false` | block 2 exit **1** |
| G4 | one of the four named tests deleted | `cargo test` exit **0** (15 passed) but block 1 exit **1** |

Two things are recorded rather than smoothed over:

- **A sixth mutation did not behave as a mutation.** Making the capture callback
  drop its samples left `Session::audio` unused, and `warnings = "deny"` turned
  that into `error: method audio is never used` — a compile failure, not a test
  failure. M3 is the behavioural replacement. The dead-code denial is a real
  signal but not the one the clause is about.
- **M2 failed two tests, not one.** The second is incidental: with the fixture
  accepting anything, the foreign-key test's session opens and is never stopped,
  so the fake devices' global record still holds its entries when the main test
  reads them. It is a property of the mutation, not of the delivered tree.
- **Cross-test pollution was observed once, for real, during validation.** The
  first run of the audio-level stop test did not hold `crate::socket::TEST` and
  reported `["speaker","microphone","speaker","microphone"]` — exit 101. Both
  sync tests take the lock for that reason, and the risk is named in the spec.

## Commands, second pass, with observed exit codes

| # | Command | Exit |
| --- | --- | --- |
| 14 | `git worktree add --detach <scratch>/proto f808262` | 0 |
| 15 | `cargo build --tests` (first attempt) | **101** — `Voice` has no `Debug`, so `expect_err` will not compile; fixed with a `let Err(…) else` |
| 16 | `cargo build --tests` (after the fix) | 0, no warnings under `warnings = "deny"` |
| 17 | `cargo test --lib` (first run) | **101** — 15 passed / 1 failed, the pollution above |
| 18 | `cargo test --lib` (after both sync tests take `TEST`) | 0 — **16 passed, 0 failed** |
| 19 | `cargo clippy --all-targets` | **101** — 4 lints: 3 × `await_holding_lock`, 1 × `result_large_err` |
| 20 | `cargo clippy --all-targets` (after one reasoned `#[allow]` on `mod tests`) | 0 |
| 21 | cold-build timing: empty `CARGO_TARGET_DIR`, `cargo test --lib` | 0 — **10 s wall**, cargo reporting 8.73 s |
| 22 | M1 … M5, G1 … G4 | as the table above — 101 ×5, 1 ×4 |
| 23 | `cargo test --lib` after every mutation was reverted | 0 — 16 passed, and `git diff` byte-identical to the pre-mutation patch |
| 24 | Verify block 1, real tree, empty target dir | 0 — **8 s wall** |
| 25 | Verify block 2, real tree | 0 — `audio granted; grant.exec == what src spawns == ['tmux']` |
| 26 | `git worktree add --detach <scratch>/isolated f808262` | 0 |
| 27 | `git apply --check attempt-1.patch` / `git apply` in that fresh tree | 0 / 0 |
| 28 | `git status --porcelain` there | 0 — exactly `src/audio.rs`, `src/service.rs`, `src/socket.rs` |
| 29 | Verify blocks 1 and 2 from the isolated tree | 0 / 0 — 16 passed |
| 30 | strays: `pgrep -fl ffmpeg` / `ffplay` after everything | 1 / 1 |
| 31 | positive control: `( exec -a ffmpeg-probe sleep 3 ) &` then `pgrep -fl ffmpeg` | **0** — matched `20155 ffmpeg-probe 3`; the clean results above are real |
| 32 | `pgrep -fl ffmpeg` after killing the control | 1 |

Every cargo command ran with `CARGO_TARGET_DIR` inside the scratchpad, or — in
the two Verify-block runs — with the block's own
`$PWD/target/voice-headless-verify` default inside a scratch worktree. No dylib
under `/Users/feb/dev/cartridge/live.ctg/target` was written, so nothing
hot-restarted, and the project daemon was not started, stopped, replaced or
reloaded.

## How the microphone and the credential stayed out of the second pass

- **No real device was opened.** `audio::open` — the only `cpal` caller — appears
  exactly once outside its own definition, as the production default at
  `src/service.rs:95`, and every test overrides it through the `wired()` helper
  or passes `fake::open`/`fake::refuse` directly. Grepping the isolated run's log
  for `coreaudio`, `default_input_device` and `no microphone on this machine`
  matched **one line**, and it was `Compiling coreaudio-rs v0.14.2` — a build
  line, not a device open. Nothing played; `Playback` was only ever drained by
  the existing unit test.
- **No stray processes**, checked with a pattern proven to match in the same run
  (row 31).
- **No real credential was read, sent, printed or spent.** Every voice test sets
  `OPENAI_API_KEY` to the literal `sk-fixture-live-not-a-real-key` and **never
  reads the previous value** — deliberately not saved and not restored, because
  saving it would mean reading a real key into memory for no benefit; the test
  binary exits with the dummy in place, and `the_environment_key_wins` sets its
  own. The fixture refuses every bearer but that dummy, which is asserted by a
  test of its own, so even a broken lock would fail the run rather than send a
  key. Nothing dialled `api.openai.com`: the only destination any test uses is
  `ws://127.0.0.1:<ephemeral>`. `auth {op:"status"}` was not run;
  `~/.codex/auth.json`, `.cartridge/credentials`, the keychain and `security(1)`
  were not opened or invoked.
- **Nothing was written to the live checkout.** Both worktrees are detached
  inside the scratchpad, and `live.ctg` itself is `f808262` with
  `git status --porcelain` empty. The two scratch worktrees
  (`…/scratchpad/voice-headless/proto` and `…/isolated`) are **still registered**:
  removing them needs `git worktree remove --force`, which this session's guard
  rules block, and the safe alternatives (`git checkout -- .` to clear the
  applied patch) are blocked too. They hold nothing the coordinator needs — the
  patch is `attempt-1.patch` in the loop directory — so
  `git -C live.ctg worktree prune` after deleting the scratchpad clears both
  registrations. `git worktree list` also shows one pre-existing prunable entry
  at `cartridge-worktrees/ws/live.ctg`, which is not mine.
