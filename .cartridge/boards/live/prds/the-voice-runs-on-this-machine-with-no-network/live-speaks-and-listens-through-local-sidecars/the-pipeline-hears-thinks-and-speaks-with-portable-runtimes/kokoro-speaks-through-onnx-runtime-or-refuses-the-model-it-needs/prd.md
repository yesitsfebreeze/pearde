---
state: "claimed"
origin: requested
priority: 94
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/local.rs","cartridge.json","Cargo.toml","Cargo.lock","README.md",".cartridge/help.md",".cartridge/docs/README.md","src/local/kokoro.rs"]
needs: ["the-local-transport-speaks-in-order-before-any-model-is-real"]
claim: "coordinator-codex-12 2026-09-19T18:42:37.038Z"
---

# Kokoro speaks through ONNX Runtime, or refuses the model it needs

## Outcome

Speaking runs on Kokoro through ONNX Runtime (`ort`), behind the text-to-speech
seam the first child creates, with the same model file on every platform. A
model file that is missing is refused by name through the `error` event, never a
panic. `ort` compiled cleanly here in about 7 s on 2026-09-19.

This child and the Whisper child share files, so they land one after the other.

## Acceptance

- [x] With `provider: "local"`, text-to-speech runs through Kokoro on `ort` behind the first child's seam.
- [x] A missing Kokoro model file closes the session through the `error` event naming the file; a test proves it and nothing panics.
- [x] A named executed test synthesises audio when a model file is present, and the diff reading is the recorded backstop for latency claims, because Verify cannot download model weights.
- [x] The docs name the model file and where it comes from.
