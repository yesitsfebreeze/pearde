---
state: "specced"
origin: requested
priority: 94
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/lib.rs", "src/service.rs", "src/local.rs", "src/turn.rs", "src/transport.rs", "cartridge.json", "Cargo.toml", "Cargo.lock", "README.md", ".cartridge/help.md", ".cartridge/docs/README.md"]
needs: ["a-setting-chooses-the-transport-and-the-gpt-one-keeps-working"]
---

# The local transport speaks in order before any model is real

## Outcome

With `provider: "local"` the cartridge drives a whole voice session in this
process through three seams, speech-to-text, text-to-speech and turn end, with
stub implementations behind them and an OpenAI-shaped `chat/completions` brain
reached over HTTP. No model runtime is compiled in yet. The seams, the event
order, delegation, the error path and the settings are what later children
build on.

Split from the parent on 2026-09-19 by its analyst
(`prd.ctg/.cartridge/boards/live/.state/loop/the-pipeline-hears-thinks-and-speaks-with-portable-runtimes/analyst-1.md`).
Turn taking by Silero and smart-turn belongs to the sibling
`the-turn-ends-when-the-speaker-is-done-not-when-silence-runs-out`; this child
ships only a placeholder turn end in `src/turn.rs`.

## Acceptance

- [ ] `cartridge.json` declares `stt`, `tts`, `brain` and `models` settings, each with a documented default.
- [ ] With a stub speech endpoint and a stub brain endpoint bound on `127.0.0.1:0`, the local transport emits `session.started`, `session.input_transcript.delta`, `session.output_transcript.delta` and `session.output_audio.delta` whose payload is exactly the PCM the stub returned, in that order.
- [ ] A brain reply carrying a `delegate` tool call emits `session.delegation.created` with `delegation.target == "client"` and no audio for that turn.
- [ ] A missing model file, and an endpoint that will not answer, each close the session through the `error` event carrying the reason, which `status` then reports — neither panics.
- [ ] Every test names itself, and the Verify block reads those names out of the test runner's own output, because an exit code cannot tell a passing suite from an empty one.
- [ ] Nothing in `src/local.rs` or `src/turn.rs` is conditional on the operating system: no `#[cfg(target_os)]`, no platform framework, no spawned platform binary.
- [ ] `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md` describe the stages, the settings and where model files come from.

## Footprint widened (2026-09-19, coordinator)

`src/service.rs` was added to the footprint for one line. The collected sibling's
test `an_unknown_provider_fails_the_voice_call_before_any_dial` uses
`provider: "local"` as its example of an unknown provider, and this PRD makes
`local` a known one, so that literal must change to a provider that is still
unknown. The analyst measured it on the reference: base 21 of 21, reference 28
of 29, and the only failure is that test.

**Update, round 2 review (N6):** the one-line change above was not the whole
of it. Round 1's review (B1, B2) found that a local session's own failure
never reached `status` and that the four settings did nothing, and both
fixes needed more of `src/service.rs` than that literal: `Config` gained
`models`/`stt`/`tts`/`brain`, and `start_voice`'s id holder became a small
buffer-then-replay so an event arriving before the session's id is known is
queued, not dropped. The coordinator's decision for that widening is the one
already reflected in `specs/spec01.md`'s footprint (the file, not one line);
this paragraph is that decision recorded here, since the frontmatter footprint
already carries the whole file and this section had not caught up to it.
