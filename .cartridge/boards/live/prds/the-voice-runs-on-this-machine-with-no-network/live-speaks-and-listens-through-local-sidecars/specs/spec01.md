---
complexity: medium
footprint:
  - src/lib.rs
  - src/local.rs
  - src/service.rs
  - src/socket.rs
  - src/transport.rs
  - tools/stt/sttd.swift
  - cartridge.json
  - Cargo.toml
  - Cargo.lock
  - .gitignore
  - README.md
  - .cartridge/help.md
  - .cartridge/docs/README.md
---

# spec01 — One transport seam, and a local pipeline behind it

Base: `live.ctg` at `HEAD`. **Landing precondition:** the working tree carries
roughly 245 uncommitted lines from another session in `src/service.rs`,
`src/store.rs`, `cartridge.json`, `init.lua`, `.cartridge/help.md` and
`.cartridge/docs/README.md`. Four of those paths are in this footprint. The dirty-path sweep
(`prd.ctg/src/lifecycle.ts:145`) runs `git status` in the *lane*, so it will not
pick those edits up; what stops collection is the fast-forward of `repo` onto
the lane (`:166`), which refuses over a dirty `src/service.rs`, and the
post-integration footprint check (`:174`), which aborts when pass 2 finds the
footprint changed under it. Either way this PRD is collectable only once that
work is committed or reverted by its owner. Implementation proceeds in the lane
meanwhile; collection waits.

`src/socket.rs:14` holds the GPT Live endpoint as a constant and `start_voice`
calls `socket::credential` and then `socket::connect` directly. Everything
downstream is already transport-agnostic: `Service::event` dispatches on event
names, and the session object exposes `send`, `audio`, `close` and an `id`.

The seam is one enum with two variants, and the local variant drives three
processes it does not implement:

- **ears** — a Swift sidecar fed PCM16 on stdin, answering NDJSON on stdout.
  It never opens the microphone, so the host's existing audio grant stays the
  only one. Measured on this machine: it holds results until asked, so the end
  of a spoken turn is **SIGUSR1**, which makes it call
  `SpeechAnalyzer.finalize(through: nil)` and emit a `final` while the session
  stays open. Two turns proved in one process.
- **brain** — any OpenAI-shaped `chat/completions` endpoint, streamed. A warm
  3 B model here answers its first token in 25–47 ms.
- **mouth** — any OpenAI-shaped `audio/speech` endpoint returning PCM16 at
  24 kHz. Kokoro-82M through `mlx-audio` returns first audio for a clause in
  0.119 s here.

The tests drive `local::connect` directly and collect what it emits. That is
deliberate: `Service::event` has no `session.started` arm (the GPT transport
consumes it inside `connect`), and its `session.output_audio.delta` arm returns
into the playback queue without touching the record, so neither is observable
through the service. The transport's own callback is where both are observable,
and it is the contract this PRD adds.

No model, no daemon and no network are needed to run them: the speech command
is a script the test writes, and the two endpoints are `tokio` listeners the
test binds on `127.0.0.1:0`.

## Acceptance

- [ ] `cartridge.json` declares `provider` (default `"gpt"`), `stt`, `tts` and `brain` with documented defaults, and `grant.exec` names `tools/stt/sttd` beside `tmux`, because the sandbox emits one `(allow process-exec <path>)` per granted program (`cartridge.ctg/src/sandbox/mod.rs:239-265`).
- [ ] `src/transport.rs` is an enum over both transports exposing `send`, `audio`, `close`, `id` and a constructor taking the session configuration and an event callback; `src/service.rs` selects by setting and reaches `socket::credential` only on the GPT branch.
- [ ] Six named tests in `src/local.rs` pass, each observing the transport's own callback: `a_session_starts`, `speech_becomes_an_input_transcript`, `a_reply_is_spoken_as_audio_and_transcript`, `the_brain_is_asked_with_the_instructions_and_the_transcript`, `the_turn_end_signals_the_speech_command`, `a_tool_call_becomes_a_delegation`.
- [ ] `a_reply_is_spoken_as_audio_and_transcript` decodes `session.output_audio.delta` to exactly the PCM16 the stub speech endpoint returned, and asserts the order `session.started`, `session.input_transcript.delta`, `session.output_transcript.delta`, `session.output_audio.delta`.
- [ ] `the_turn_end_signals_the_speech_command` reads the signal from a file the stub appends to, named in the stub's environment — not from stdout, which the transport parses.
- [ ] `a_tool_call_becomes_a_delegation` sees `session.delegation.created` with `delegation.target == "client"` and the tool's prompt, and no audio delta for that turn.
- [ ] The existing `mod tests` in `src/socket.rs`, `src/audio.rs` and `src/service.rs` — three, three and five tests — still pass unchanged, and `src/socket.rs:14` still holds `wss://api.openai.com/v1/live/sessions`.
- [ ] Every endpoint comes from configuration — the transport holds them as fields set from the settings — and an endpoint that will not answer closes the session with `session.closed` carrying the reason instead of panicking.
- [ ] `.gitignore` ignores the compiled sidecar `tools/stt/sttd`; the `.swift` source stays tracked.
- [ ] `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md` each describe both providers, the four settings and the sidecar's stdin/stdout/SIGUSR1 contract.

## Steps

1. `cartridge.json`: the four settings, `grant.exec` plus `tools/stt/sttd`, a
   `build-stt` command.
2. `Cargo.toml`: an HTTP client for the two endpoints — `reqwest`,
   `default-features = false`, with `rustls-tls`, `json` and `stream`, reusing
   the `rustls` already in the tree.
3. `src/transport.rs`, with `src/socket.rs` as one variant of it.
4. `src/local.rs`: spawn and feed the speech command, signal it at the turn's
   end, stream the brain, split the reply at clause boundaries, synthesise each
   clause, emit the events; a tool call becomes a delegation.
5. `src/service.rs`: choose the variant.
6. `tools/stt/sttd.swift` — `@main`, built with `-parse-as-library`.
7. The six tests, the three documents, `.gitignore`.
8. Last, run Verify block 2's command exactly as written: it proves the tests
   and warms the target directory that block depends on. Nothing else warms it
   — `just test live` fans to `_cargo`, which pins no target directory, and
   `doc.commands` are only ever printed (`cartridge.ctg/src/cli/manual.rs:538`).

## Verify and Proof

<!--
Engine facts (`prd.ctg/.cartridge/templates/spec.md`): `sh -eu -c`, 120 s each,
first in the lane and then in `repo`, paths relative to the repo root.
- Nothing is piped: a pipeline's status is its last command's, so `cargo test |
  tail` would report `tail`'s and a failing test would collect.
- Negated checks are `if grep -q ...; then exit 1; fi`; `! grep` does not trip
  `set -e`.
- Every check discriminates. A grep for a name a build recipe also carries
  proves nothing, so the manifest is parsed and its values asserted; and the
  test names are read out of cargo's own output, because `cargo test --lib`
  passes with no tests written.
- Scratch and the pinned target directory go to `${TMPDIR:-/tmp}`, which the
  collector may write, outside the footprint and away from the `target/` the
  running host loads from. Step 8 warms it, so collection recompiles one crate.
-->

```sh
# Shape and manifest.
test -f src/transport.rs
test -f src/local.rs
test -f tools/stt/sttd.swift
grep -q 'wss://api.openai.com/v1/live/sessions' src/socket.rs
if grep -qn 'socket::connect' src/service.rs; then exit 1; fi
grep -qx 'tools/stt/sttd' .gitignore
bun -e 'const m = await Bun.file("cartridge.json").json();
const exec = m.grant?.exec ?? [];
if (!exec.some((p) => String(p).endsWith("tools/stt/sttd"))) {
  console.error("grant.exec does not name the speech sidecar: " + JSON.stringify(exec));
  process.exit(1);
}
const settings = m.settings ?? {};
for (const key of ["provider", "stt", "tts", "brain"]) {
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
  for (const word of ["provider", "stt", "tts", "brain", "SIGUSR1"]) {
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
export CARGO_TARGET_DIR="${TMPDIR:-/tmp}/cartridge-verify/live-local"
export CARGO_INCREMENTAL=0
out="${TMPDIR:-/tmp}/live-local-test-$$.txt"
cargo test --lib > "$out" 2>&1 || { cat "$out"; rm -f "$out"; exit 1; }
for t in a_session_starts \
         speech_becomes_an_input_transcript \
         a_reply_is_spoken_as_audio_and_transcript \
         the_brain_is_asked_with_the_instructions_and_the_transcript \
         the_turn_end_signals_the_speech_command \
         a_tool_call_becomes_a_delegation; do
  if ! grep -q "local::tests::$t \.\.\. ok" "$out"; then
    echo "missing or failing test: $t"
    cat "$out"
    rm -f "$out"
    exit 1
  fi
done
# What the seam did not change still runs.
grep -q 'socket::tests::' "$out"
grep -q 'audio::tests::' "$out"
grep -q 'service::tests::' "$out"
rm -f "$out"
```

```sh
# The sidecar builds on this machine's toolchain, into scratch.
out="${TMPDIR:-/tmp}/sttd-verify-$$"
swiftc -parse-as-library -O tools/stt/sttd.swift -o "$out"
test -x "$out"
rm -f "$out"
```
