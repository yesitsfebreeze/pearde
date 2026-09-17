---
state: open
origin: requested
priority: 94
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/lib.rs", "src/local.rs", "src/turn.rs", "src/transport.rs", "cartridge.json", "Cargo.toml", "Cargo.lock", "README.md", ".cartridge/help.md", ".cartridge/docs/README.md"]
needs: ["a-setting-chooses-the-transport-and-the-gpt-one-keeps-working"]
---

# The pipeline hears, thinks and speaks with portable runtimes

## Outcome

With `provider: "local"` the cartridge holds the conversation itself, in this
process, with no network on the conversational path and nothing specific to this
operating system.

Four stages, two runtimes, no sidecar:

- **hearing** — `whisper.cpp` through `whisper-rs`. Measured here on 2026-09-17:
  0.225 s for 6.87 s of English, real-time factor 0.033, and it transcribed
  "pull request" correctly where the platform's own recogniser heard "pool
  request". MIT; Metal, CUDA or CPU.
- **turn taking** — Silero voice activity and smart-turn v3, both ONNX through
  `ort`. The turn ends when the model says the speaker finished, not when a
  timer runs out.
- **thinking** — any OpenAI-shaped `chat/completions` endpoint, streamed, so the
  brain is a setting: Ollama, llama.cpp, a router, whatever answers. A warm 3 B
  model here returns its first token in 25–47 ms.
- **speaking** — Kokoro through ONNX Runtime, the same model file on every
  platform. Measured here: first audio 0.354 s for a clause, real-time factor
  0.27.

The transport emits the events the service already dispatches, and a tool call
from the brain becomes `session.delegation.created`, so delegation to the agent
keeps working untouched.

Model files are data, not code: a setting names the directory they live in, and
a missing file is reported as a refusal naming the file, never a panic.

## Acceptance

- [ ] `cartridge.json` declares `stt`, `tts`, `brain` and `models` settings, each with a documented default.
- [ ] With a stub speech endpoint and a stub brain endpoint bound on `127.0.0.1:0`, the local transport emits `session.started`, `session.input_transcript.delta`, `session.output_transcript.delta` and `session.output_audio.delta` whose payload is exactly the PCM the stub returned, in that order.
- [ ] A brain reply carrying a `delegate` tool call emits `session.delegation.created` with `delegation.target == "client"` and no audio for that turn.
- [ ] A missing model file, and an endpoint that will not answer, each close the session through the `error` event carrying the reason, which `status` then reports — neither panics.
- [ ] Every test names itself, and the Verify block reads those names out of the test runner's own output, because an exit code cannot tell a passing suite from an empty one.
- [ ] Nothing in `src/local.rs` or `src/turn.rs` is conditional on the operating system: no `#[cfg(target_os)]`, no platform framework, no spawned platform binary.
- [ ] `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md` describe the four stages, the settings and where model files come from.
