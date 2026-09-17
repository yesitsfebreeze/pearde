---
complexity: small
footprint:
  - src/audio.rs
  - src/service.rs
  - src/socket.rs
---

# spec01 — Stop the voice by waiting for it, report the device that would not open, and prove both on a real socket

Base: `live.ctg` `f808262`, clean.

Three of the four boxes are about the same missing thing: nothing in this
cartridge has ever executed `voice`, `start_voice`, `stop_voice` or `event`.
The behaviours they name are half present —

- `stop_voice` (`src/service.rs:277-289`) removes the session and drops the
  `Voice`, but `Drop` (`src/audio.rs:126-130`) only stores a flag that the audio
  thread reads on a 50 ms tick. The call returns while both devices are still
  open, so "capture stopped" is a hope with no instant at which it is true.
- The reason a device would not open exists (`src/audio.rs:182-241`, held on the
  session at `src/service.rs:244-249`, plus `Voice::failure` for one that fails
  later) but reaches only `status` (`:160`). `state` (`:179-187`) has no error.
- Nothing can be tested at all while the destination
  (`src/socket.rs:14`, a constant) and the devices (`src/audio.rs:145`, a direct
  call to `open`) are both wired in place.

So this spec opens exactly two seams — where the session is dialled, and how the
devices are opened — makes stopping wait, routes the error to `state`, and adds
the tests those seams make possible. Everything downstream of both seams is the
cartridge's own code, running for real.

## Acceptance

- [x] `Voice`'s `Drop` joins the audio thread. A test opens fake devices whose close takes a known 300 ms, stops the voice, and finds **both devices already down the moment the call returns** — with no sleep of its own — having taken at least that 300 ms and less than 2 s.
- [x] `live {op:"voice", enabled:true}` runs against a GPT Live service on `127.0.0.1:0`: a real TCP listener, a real WebSocket handshake, a real socket. The service receives the `session.start` this cartridge builds, answers `session.started`, and it refuses every bearer but the fixture's dummy — a key that happens to be on this machine fails the test instead of being spent.
- [x] What the fake microphone hears crosses that socket as `session.input_audio.append` carrying PCM16 the test decodes back to the samples it supplied, through the real capture loop — its tick, its half-duplex gate, its batching.
- [x] A `session.output_transcript.delta` the service sends lands in the store and comes back out of `state`.
- [x] A device that will not open leaves the session running and its reason readable in `state`, not only in `status`.
- [x] `cartridge.json` grants `audio`, and `grant.exec` names exactly the binaries `src/**` actually spawns — no more and no fewer.

Every one of these was run against a tree built to deny it; the observed exit
codes are in `## Verify and Proof`.

## Steps

1. **`src/audio.rs` — one seam for the devices.** Add
   `pub type Opened = (Box<dyn std::any::Any>, Arc<Mutex<Vec<f32>>>, u32)` and
   `pub type Opener = fn(&Arc<Playback>, &Arc<Mutex<Option<String>>>) -> Result<Opened>`.
   `open` becomes `pub(crate)` and returns `Ok((Box::new((out_stream, in_stream)), held, in_rate))`
   — the two `cpal::Stream`s go into the box together, so they are still built
   and dropped on the audio thread and nowhere else, which is the invariant the
   module opens with. The `Devices` alias goes. `run` takes the opener and calls
   it instead of `open`; its destructure becomes `(_devices, held, in_rate)`.
   `Voice::start` takes the opener as its first argument and passes it through.
   **No trait, no generic, no dyn dispatch**: an `Opener` is a plain `fn`
   pointer, which is what makes step 6's fake state explicit rather than hidden.

2. **`src/audio.rs` — stopping waits.** `Voice` gains
   `thread: Option<std::thread::JoinHandle<()>>`, kept from `start`. `Drop` sets
   the flag as before and then joins. This is the root-cause placement: *every*
   path that drops a `Voice` now waits, not just `stop_voice` — the service's
   `dispose`, a replaced session in `start_voice`, and a panic unwinding past
   one included. The cost is the tick plus the device close, measured at
   ~350 ms with a 300 ms fake close.

3. **`src/socket.rs` — one seam for the destination.** `URL` becomes `pub`, and
   `connect` takes `destination: &str` as its first argument in place of reading
   the constant. Nothing else in the function changes: the handshake, the
   `session.start`, the `session.started` wait, the two relay tasks and `close`
   all stay exactly as they are, which is the point — the test drives them,
   rather than a stand-in for them.

4. **`src/socket.rs` — test-only statics.** `#[cfg(test)] pub(crate) static TEST: std::sync::Mutex<()>`
   and `#[cfg(test)] pub(crate) const DUMMY: &str`. `cargo test` runs one process
   with many threads, and both the process environment and step 6's fake devices
   are global; `TEST` is what serialises the tests that touch either.
   `the_environment_key_wins` takes it too — it sets `OPENAI_API_KEY` today with
   nothing stopping another test reading it mid-flight.

5. **`src/service.rs` — the two seams on the service.** `Service` gains
   `endpoint: String` (`socket::URL.to_owned()`) and `opener: audio::Opener`
   (`audio::open`). `start_voice` passes both. Both are private fields with
   production defaults and **no manifest setting**: a test in the same module
   sets them, and nothing outside the crate can.

6. **`src/audio.rs` — `#[cfg(test)] pub(crate) mod fake`.** `open` registers a
   shared capture buffer and returns a `Streams` marker whose `Drop` sleeps
   `CLOSING` (300 ms) and then records `["speaker", "microphone"]`; `refuse`
   returns `Err("microphone: the fake device is not available")`; `heard()`
   pushes samples into the capture buffer; `put_down()` reads the record without
   waiting. The sleep is the whole measurement: a caller that only set a flag
   returns long before the record exists, so the box-1 clause is **false in the
   denied world by construction**, not by a race. The module lives inside
   `audio` because it must set `Playback::rate`, which is private there.

7. **`src/service.rs` — the error reaches `state`.** Add `voice_error(conversation)`,
   returning `entry.error` or `Voice::failure()` for this conversation's session,
   and put it in `state`'s `voice` object. **It is called before the store guard
   is taken**: `event` takes the sessions and then the store, so taking the two
   in the other order here would be a deadlock waiting for a transcript to
   arrive while a surface reads `state`. `status` is left alone.

8. **`src/service.rs` — `stop_voice` releases the map first.** The entries come
   out of the map, the guard is dropped, and only then are they closed and
   dropped — so the socket's own relay task, which takes that same map in
   `event`, is not held up for the 350 ms the devices take to close. Dropping the
   entry drops its `Voice`, which is where the wait from step 2 happens.

9. **`src/service.rs` — the tests.** A `Fixture`: `tokio::net::TcpListener` on
   `127.0.0.1:0`, `accept_hdr_async` refusing the upgrade with 401 unless the
   request carries `Bearer <DUMMY>`, answering `session.start` with
   `session.started`, recording every client event and able to speak server
   events back. Three `#[tokio::test(flavor = "multi_thread")]`: the wire-and-stop
   test, the refused-device test, and one that sets a key the fixture does not
   know and asserts the session never opens and the message does not repeat the
   key. Two sync tests in `audio.rs` cover the join and the refusal at the
   `Voice` level. `tokio/net` is already enabled through `tokio-tungstenite`
   (`cargo tree -e features`), so **`Cargo.toml` is not touched** — which matters,
   because it is outside this PRD's footprint.

10. **`mod tests` carries `#[allow(clippy::await_holding_lock, clippy::result_large_err)]`**
    with the reason in a comment: the held lock is deliberately held across
    awaits because it serialises whole tests, and the refusal type is
    tungstenite's. `cargo clippy --all-targets` is exit 0 with it and exit 101
    without — `warnings = "deny"` is on in `Cargo.toml`.

Not done, deliberately: **no microphone-permission probe.** On macOS a denied
microphone delivers silence, not an error (`src/audio.rs:179-181`); the user was
offered the probe and declined it, so no box claims denial is detected and the
`state` error covers only devices that refuse to open or fail later.

## Option chosen

**A seam at the destination and a seam at the opener, and nothing else faked.**

The alternative with history behind it is the one the deleted TypeScript test
took (`live.ctg 7d89976:.cartridge/tests/integration/voice.test.ts`): an
in-process `FakeSocket` and injected `capture`/`playback` functions. It was
rejected on this PRD and on `@auth/gpt-live-connects-over-websocket-on-the-discovered-credential`
for the same reason — replacing the socket replaces the code the boxes are
about, and four of that sibling's seven clauses could not fail. Here, faking the
socket would leave `socket::connect` — the handshake, the `session.start`, the
`session.started` wait, the relay tasks — unexecuted, and box 2's "runs a session"
would again be true of nothing.

So the socket is real and only its *destination* moves. That costs one `&str`
parameter and buys: the bearer actually being sent and checked, the base64 audio
actually crossing a wire, the relay task actually delivering the transcript.

The devices are the one thing that **cannot** be real — the safety rule forbids
opening the microphone, and a machine running collect may have no input device
at all. The seam is therefore placed as low as it can go: at `open` itself, so
the resampling, the batching, the half-duplex gate and the thread lifecycle above
it are all the shipped code. `Box<dyn Any>` rather than a `Streams` trait because
there is exactly one production implementation and the box's only job is to be
dropped in the right place.

`Drop` rather than a `stop()` method for the join, because `stop_voice` is not
the only place a `Voice` dies, and a guard in the shared destructor is a smaller
diff than one at every call site — and does not leave the sibling paths broken.

The `state` error goes in the existing `voice` object rather than a new
top-level key: `voice()` writes the intent row before it starts a session, so an
error always has an intent to hang off, and a reader that already looks at
`state.voice` for `enabled` finds it without learning a new shape.

## Remaining risk

- **The `error` is lost if a session exists with no intent row.** Not reachable
  through `voice()`, which writes the intent first, but it is a shape the type
  allows. Recorded rather than defended with a branch that nothing can reach.
- **`Drop` joins on whatever thread drops the `Voice`**, which for `stop_voice`
  is a tokio worker, blocked for ~350 ms. Acceptable on the multi-thread runtime
  this module builds (`src/bridge.rs:46-53`); `block_in_place` is the upgrade if
  a voice ever shares that runtime with something latency-sensitive.
- **The 2 s upper bound in the box is pinned by the test's own assertion**, and
  the fake close is what sets the lower one. A device that hangs on close would
  hang the join; nothing bounds a real `cpal` stream's teardown, and adding a
  timeout would mean abandoning a thread that still owns a device. Recorded.
- **The fake devices are global state**, serialised by `crate::socket::TEST`. A
  future test that uses them and forgets the lock gets cross-test pollution; that
  failure was observed once during this spec's own validation (the audio-level
  test without the lock made `put_down()` report four entries) and is why both
  sync tests take it too.

## Verify and Proof

<!--
How collect runs these blocks (engine facts, src/lifecycle.ts collect/verify):
- Each sh/bash/shell block runs as `sh -eu -c`, 120 s limit, empty stdin, the
  collector's environment.
- It runs twice: first with cwd = the lane, a worktree of the PRD's `repo` at
  `prd.ctg/.cartridge/boards/<board>/.lanes/<slug>`; then, after the
  fast-forward, with cwd = `repo` itself.
- Paths are relative to the repo root. Never `cd` to an absolute checkout.
- Pass 2 runs in the live checkout, so every cargo block pins CARGO_TARGET_DIR.
- A block must not write inside the footprint; `target/` is not in it, and
  scratch goes to `mktemp`.
-->

Block 1 — the suite, and the four tests it must still be running. Measured at
**8 s wall from an empty target directory** on this machine, well inside the
120 s limit.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/voice-headless-verify}"
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
cargo test --lib > "$log" 2>&1 || { cat "$log"; exit 1; }
cat "$log"
for named in \
	a_voice_puts_its_devices_down_before_stopping_returns \
	voice_runs_a_session_on_the_wire_and_puts_both_devices_down_before_it_returns \
	a_device_that_will_not_open_is_a_readable_voice_error_in_the_state \
	a_key_the_fixture_does_not_know_never_opens_a_session
do
	if ! grep -q "${named} \.\.\. ok" "$log"; then
		echo "the suite no longer runs ${named}"
		exit 1
	fi
done
```

Block 2 — the manifest grants what the code needs, and only that. No cargo, so
it is fast in both passes.

```sh
test -f cartridge.json
test -d src
python3 - <<'PY'
import json, pathlib, re, sys

manifest = json.loads(pathlib.Path("cartridge.json").read_text())
grant = manifest.get("grant", {})
if grant.get("audio") is not True:
    sys.exit("cartridge.json does not grant `audio`, and this cartridge opens both devices itself")
spawned = set()
for source in sorted(pathlib.Path("src").rglob("*.rs")):
    spawned |= set(re.findall(r'Command::new\("([^"]+)"\)', source.read_text()))
granted = set(grant.get("exec", []))
if granted != spawned:
    sys.exit(f"grant.exec is {sorted(granted)} but src spawns {sorted(spawned)}")
print(f"audio granted; grant.exec == what src spawns == {sorted(spawned)}")
PY
```

### Denied worlds, each built and run

Every clause was run against a tree constructed to make it false. Observed exit
codes, all from `cargo test --lib` or the block itself:

| Denied world | What was changed | Observed |
| --- | --- | --- |
| M1 | `Drop for Voice` back to a bare flag, no join | exit **101**, 14 passed / **2 failed** — both stop-measurement tests, `left: [] right: ["speaker","microphone"]` |
| M2 | the fixture accepts any non-empty bearer | exit **101**, 14 passed / **2 failed**, including `a_key_the_fixture_does_not_know_never_opens_a_session` |
| M3 | `Session::audio` sends `session.input_audio.nowhere` | exit **101**, 15 passed / **1 failed** — the capture clause, at the append that never arrives |
| M4 | `event` stops matching the transcript deltas | exit **101**, 15 passed / **1 failed** — the store clause |
| M5 | `state` reports `"error": Value::Null` | exit **101**, 15 passed / **1 failed** — `a_device_that_will_not_open_is_a_readable_voice_error_in_the_state` |
| G1 | a `Command::new("say")` added to `src/service.rs` | block 2 exit **1**: `grant.exec is ['tmux'] but src spawns ['say', 'tmux']` |
| G2 | `"ffplay"` added to `grant.exec` | block 2 exit **1**: `grant.exec is ['ffplay','tmux'] but src spawns ['tmux']` |
| G3 | `"audio": false` in the manifest | block 2 exit **1**: `does not grant audio` |
| G4 | one of the four tests deleted | `cargo test` still exit 0, 15 passed — **block 1 exit 1**, `the suite no longer runs a_key_the_fixture_does_not_know_never_opens_a_session` |

A sixth was attempted and is recorded because it did not behave as a mutation:
making the capture callback drop its samples left `Session::audio` unused, and
`warnings = "deny"` turned that into a compile error rather than a test failure.
M3 replaces it with the behavioural form.

### Prototype

`attempt-1.patch`, beside this file — `src/audio.rs`, `src/service.rs`,
`src/socket.rs`, 675 lines of diff, no other file. Validated in a fresh
worktree of `f808262`: `git apply --check` exit 0, `git apply` exit 0,
`git status --porcelain` showing those three files and nothing else, block 1
exit 0 (16 passed / 0 failed) and block 2 exit 0 from that isolated tree.
`cargo clippy --all-targets` exit 0.
