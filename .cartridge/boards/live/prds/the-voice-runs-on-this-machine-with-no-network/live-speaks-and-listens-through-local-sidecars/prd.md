---
state: "open"
origin: requested
priority: 95
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/lib.rs", "src/local.rs", "src/service.rs", "src/socket.rs", "src/transport.rs", "tools/stt/sttd.swift", "cartridge.json", "Cargo.toml", "Cargo.lock", ".gitignore", "README.md", ".cartridge/help.md", ".cartridge/docs/README.md"]
---

# Live speaks and listens through local sidecars

## Outcome

`live` gains a `provider` setting, `"gpt"` or `"local"`. With `"local"` the
cartridge opens no socket to OpenAI. Instead it runs the conversation itself:
captured audio goes to a speech-to-text sidecar, the transcript goes to a front
model over an OpenAI-shaped HTTP endpoint, the reply is chunked by clause and
synthesised by a text-to-speech sidecar, and the audio is played through the
speaker this cartridge already owns.

The local transport emits the event names the GPT transport emits, so the
record, delegation, `watch`/`reply` and the MCP bridge keep working unchanged:
`session.input_transcript.delta`, `session.output_transcript.delta`,
`session.output_audio.delta`, `session.delegation.created` and
`session.closed` are the arms `Service::event` already dispatches, and
`session.started` is consumed by the transport itself, as the GPT transport
consumes it inside `connect` today.

The speech-to-text sidecar is a small Swift binary that is fed PCM on stdin and
answers NDJSON on stdout, and that finalises a turn when it is signalled, so
the microphone grant stays with this process and no second application asks for
one. The text-to-speech sidecar is a resident local server; its address, model
and voice are settings.

## Acceptance

- [ ] `cartridge.json` declares `provider`, `stt`, `tts` and `brain` settings with documented defaults, and `grant.exec` names `tools/stt/sttd` — read out of the manifest, not grepped for, because the sandbox allows exactly the programs it is given.
- [ ] With `provider: "local"`, the transport reaches only its configured endpoints: it carries no host or URL literal, and its tests bind loopback.
- [ ] Driven with a stub speech command and two loopback endpoints, the local transport emits `session.started`, `session.input_transcript.delta`, `session.output_transcript.delta` and `session.output_audio.delta` whose payload is exactly the PCM the stub returned; a `delegate` tool call emits `session.delegation.created` instead.
- [ ] `cargo test --lib` passes, including the `mod tests` already in `src/socket.rs`, `src/audio.rs` and `src/service.rs`, and `src/socket.rs` still holds the GPT Live endpoint constant.
- [ ] `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md` describe both providers, the settings and the sidecar contract.

Proving this against a real microphone, a real model and a real voice is the
parent PRD's acceptance, not this one's: this child ends at the transport's
own contract, which is what the tests can observe without a device.

## Landing

This PRD is collectable only once the other session's uncommitted work in
`live.ctg` is committed or reverted by its owner: `src/service.rs`,
`src/store.rs`, `cartridge.json`, `.cartridge/help.md` and
`.cartridge/docs/README.md` carry it, and four of those are in this footprint.
The dirty-path sweep (`prd.ctg/src/lifecycle.ts:145`) runs in the lane and will
not see it; what refuses is the fast-forward of `repo` onto the lane (`:166`)
and the post-integration footprint check (`:174`). Implementation proceeds in
the lane meanwhile.

## Questions

Five review rounds are spent (61, 75, 83, 73, 81; the bar is 90) and the
allowance is exhausted, so this needs an answer before it can move.

Each round found something real that would otherwise have shipped: a Verify
block whose exit code was swallowed by `tail`; a test that read the signal it
asserted from a pipe the transport owns; a `grant.exec` check a build recipe
satisfied on its own, leaving the sandbox unable to spawn the sidecar; an
acceptance surface `cargo test --lib` would have passed with no tests written at
all. None of that was cosmetic.

What round 5 still blocks on is one box: an endpoint that will not answer should
close the session with its reason, and the reason was routed through the
`session.closed` arm, which keeps no reason — the arm that keeps one is `error`.
The reviewer named three edits that would pass it: a seventh test
`a_refused_endpoint_closes_the_session`, that box rewritten onto the `error`
arm, and an assertion in the existing manifest check that the `brain` and `tts`
defaults are loopback.

It also named a structural change worth more than the edits: **split the Swift
speech sidecar into a sibling leaf**. Every finding that survived all five
rounds lives in the sidecar half — a `grant.exec` entry pointing at a binary
nothing builds, a `build-stt` recipe the manifest never executes, and the only
`swiftc` Verify block on any board, which proves a file compiles and nothing
this PRD's outcome claims. The Rust half was executed by the reviewer end to
end and holds.

1. Grant a sixth round for the three named edits, split the sidecar into its own
   leaf, or both? The recommendation from here is both: the edits are small and
   the split is what stops this shape recurring.
2. If it is split, do the children inherit the five used rounds? The workflow
   says they do unless you say otherwise, which would leave each child with none.

Independent of the answer: collection cannot complete until the other session's
uncommitted work in `live.ctg` lands, because four of those six dirty paths are
in this footprint. That has been true through all five rounds and is not
something a review can fix.

### Answer, 2026-09-17

The user answered both questions: find a cross-platform solution, and give the
children fresh review rounds.

That answer dissolves the blocking finding rather than fixing it. The Swift
speech sidecar was the Apple-only part, and every finding that survived five
rounds lived in it — a `grant.exec` entry pointing at a binary nothing built, a
`build-stt` recipe the manifest never ran, and the only `swiftc` block on any
board. There is nothing to split out because there is nothing left to split: the
sidecar goes, and with it the boxes that could not be checked.

What replaces it, measured on this machine on 2026-09-17:

- speech to text: `whisper.cpp` through `whisper-rs` — 0.225 s for 6.87 s of
  English, real-time factor 0.033, and a transcript that got "pull request"
  right where the Apple path heard "pool request". MIT, and it runs on Metal,
  CUDA or plain CPU.
- speech: Kokoro through ONNX Runtime — first audio 0.354 s for a clause,
  real-time factor 0.27. Apache-2.0, and the same model file everywhere.
- voice activity and end of turn: Silero and smart-turn v3, both ONNX through
  `ort`, which is where the `ort` dependency was going anyway.

The pipeline becomes one Rust process with two inference runtimes and no
sidecar, no Python and no platform API. This PRD is therefore refined into two
children: the seam, which is small and fully checkable, and the pipeline behind
it. Both start with a fresh review allowance, as the user directed.
