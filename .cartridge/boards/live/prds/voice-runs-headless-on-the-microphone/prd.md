---
state: "open"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/**", ".cartridge/**", "cartridge.json", "init.lua"]
---

# Voice runs headless on the microphone

## Outcome

When voice is wanted on a conversation (`live {op:"voice"}` enabled), the Live
service opens a GPT Live session over its socket transport, captures the default
microphone **in process through `cpal`** and plays `session.output_audio.delta`
the same way. No browser page, no WebRTC peer, no fifo and no child processes.
Turning voice off closes the session; delegated work keeps running. The mic is
gated while speech plays — off the shared `Playback` clock
(`src/audio.rs:82-86`, `:165-168`) — unless the conversation is set to duplex
(headphones).

## Acceptance

- [ ] Enabling voice starts capture and a session; disabling it stops both and
      the session, **measured** — `stop_voice` joins the audio thread rather
      than setting a flag and returning — and no capture or playback stream
      outlives it.
- [x] Transcripts and delegations from the session land in the same store the
      WebRTC path used.
- [ ] The manifest grants what the code actually needs (`"audio": true`, and
      `exec` only for what is genuinely spawned), and a device-open failure
      surfaces as a readable voice error in `state`, not only in `status`.
- [ ] A test drives the service against a fake transport and fake audio
      devices, with each clause failing in the world it denies — no in-process
      stand-in that cannot fail.

## Questions

2026-09-16, coordinator cartridge-1b, from analyst-1.

**The ticks were never earned by a working session.** `git log -p --follow` on
this `prd.md` has exactly one commit — the planning commit that *created* the
PRD — and boxes 1, 2 and 4 are `[x]` in its `+` lines. They were true of the
**TypeScript** cartridge recorded at `live.ctg 7d89976`, which `d782360` then
replaced with a Rust one. At `7d89976`, `grant.exec` was
`["bun","mkfifo","ffmpeg","ffplay",…]`, `needs` carried `auth.live`, and
`.cartridge/tests/integration/voice.test.ts` was exactly box 4. At HEAD
`f808262` none of that exists.

Audited against `f808262`:

- **Box 2 holds**, by inspection only, with no test: transcripts
  `src/service.rs:415-434`, delegations `:435-443` → `delegated()` persisting at
  `:490`, and `src/store.rs:80-91` creating the same tables the TypeScript path
  used.
- **Box 1 is unticked.** Enable and disable are implemented
  (`src/service.rs:205-222`, `:224-271`, `:277-289`), but no test calls
  `voice()`, `stop_voice` never joins the audio thread — so the 2 s bound is a
  comment, not a measurement — and "leaving no `ffmpeg`/`ffplay` process"
  **cannot fail**, because nothing spawns either binary any more.
- **Box 4 is unticked.** The test was deleted along with the cartridge it
  tested. `cargo test --lib` is 11 tests, none of which opens a device, binds a
  port, opens a socket or mentions `auth.live`. This is worse than the auth
  sibling, where the test was merely weak.

**The decision this needs.** Box 3's first clause — "`grant.exec` names `ffmpeg`
and `ffplay`" — is contradicted by the landed design: `cartridge.json:162-164`
is `"exec":["tmux"]`, `:168` is `"audio": true`, and `src/audio.rs:182-241`
opens both devices through `cpal` in-process. Adding that grant with nothing to
spawn would be another unfailable tick. So the PRD cannot be specced as written.

- **(A) Restate the PRD to the landed design (recommended).** Drop `ffmpeg`,
  `ffplay` and `auth.live` from the Outcome; rewrite box 3 as the audio grant
  plus the `state` error; reword boxes 1 and 4 for `cpal` and a fake transport;
  keep box 2. The rewrite is landed and better on its own terms — no fifo, no
  subprocesses, and a half-duplex gate off the shared `Playback` clock
  (`src/audio.rs:82-86`, `:165-168`). This also settles `needs:
  ["@auth/gpt-live-connects-over-websocket-on-the-discovered-credential"]`,
  which the code no longer honours. No footprint change.
- **(B) Revert the audio rewrite** to preserve the PRD's wording.

One caveat either way, from `src/audio.rs:179-181`: a denied microphone on macOS
delivers **silence, not an error**, so "microphone permission surfaces as a
readable voice error" is not implementable as written without a separate
permission probe. Box 3's second clause — a readable voice error in `state` — is
a real, small gap that survives the redesign: the errors exist
(`src/audio.rs:119-123`, held at `src/service.rs:244-249`) but surface only via
`status` (`:160`), and `state` (`src/service.rs:179-187`) carries no error field.

## Answer

2026-09-16, the user chose **(A) restate the PRD to the landed design**, and for
box 3 chose **scope it to the errors that exist**.

So the Outcome and boxes above are rewritten for the Rust cartridge as it
actually is: `cpal` in process, no `ffmpeg`/`ffplay`, no fifo. `needs` on
`@auth/gpt-live-connects-over-websocket-on-the-discovered-credential` is
**dropped**, because the landed code no longer honours it.

Box 3 now asks only for what is implementable: the manifest granting what the
code needs, and a device-open failure reaching `state`. **Recorded limit, not a
requirement:** on macOS a denied microphone delivers *silence, not an error*
(`src/audio.rs:179-181`), so denial is not detectable without a separate
permission probe. The user was offered that probe and chose not to require it;
it is not in scope and no box claims it.

Box 1's old "leaving no `ffmpeg`/`ffplay` process" clause is gone because it
could not fail — nothing spawns those binaries any more. Its replacement demands
a measurement: today `stop_voice` never joins the audio thread, so the previous
2 s bound was a comment.

Box 4's replacement says explicitly that an in-process stand-in which cannot
fail does not satisfy it. The deleted `voice.test.ts` used a `FakeSocket` with
injected `VoiceDeps` functions — restoring it verbatim would re-tick the box on
the shape already ruled insufficient here and on the auth sibling.

## Session-end note

2026-09-16, coordinator cartridge-1b, at session end.

`specs/spec01.md` is published but **UNREVIEWED** — no review round has run on
it. Do not treat it as passed. It comes from analyst-1 after the user chose (A),
and its footprint is `src/audio.rs`, `src/service.rs`, `src/socket.rs` with
`Cargo.toml` deliberately untouched (`tokio/net` already arrives transitively via
`tokio-tungstenite`, confirmed with `cargo tree -e features`), so no footprint
change is needed.

The analyst built and ran a denied world for every box: `Drop` back to a bare
flag → 14/2 on both stop tests; the fixture accepting any bearer → 14/2; a
misdirected audio append → 15/1; `event` no longer matching transcript deltas →
15/1; `state` reporting a null error → 15/1; a `Command::new("say")` in src,
`"ffplay"` added to `grant.exec`, and `"audio": false` each turning block 2 red;
and deleting one named test leaving `cargo test` green at 15 passed while block 1
goes red.

Two things it recorded rather than smoothed: a sixth mutation produced a
*compile* failure under `warnings = "deny"` instead of a test failure, so it was
replaced; and cross-test pollution was observed for real during validation, which
is why both sync tests take the lock and why the risk is named in the spec.

Next coordinator: review this spec before `specced`.
