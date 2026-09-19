---
state: open
origin: requested
priority: 94
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/local.rs", "cartridge.json", "Cargo.toml", "Cargo.lock", "README.md", ".cartridge/help.md", ".cartridge/docs/README.md"]
needs: ["the-local-transport-speaks-in-order-before-any-model-is-real"]
---

# Whisper hears through whisper-rs, or refuses the model it needs

## Outcome

Hearing runs on `whisper.cpp` through `whisper-rs`, behind the speech-to-text
seam the first child creates. A model file that is missing is refused by name
through the `error` event, never a panic.

**Landing precondition:** `whisper-rs-sys` needs a system `cmake`, and this
machine has none; the analyst's probe build failed on it on 2026-09-19. It must
be installed before this child is implemented. No spec can route around a
missing system toolchain.

## Acceptance

- [ ] With `provider: "local"`, speech-to-text runs through `whisper-rs` behind the first child's seam.
- [ ] A missing Whisper model file closes the session through the `error` event naming the file; a test proves it and nothing panics.
- [ ] A named executed test transcribes a short checked-in or generated fixture when a model file is present, and the diff reading is the recorded backstop for accuracy and latency claims, because Verify cannot download model weights.
- [ ] The docs name the model file and where it comes from.
