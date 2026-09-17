---
state: open
origin: requested
priority: 92
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/audio.rs", "src/local.rs", "src/turn.rs", "Cargo.toml", "Cargo.lock", "tools"]
needs: ["live-speaks-and-listens-through-local-sidecars"]
---

# The turn ends when the speaker is done, not when silence runs out

## Outcome

The local provider decides that a spoken turn has ended with a model, not a
stopwatch. Silero VAD marks speech and silence on 20 ms frames, and on a short
silence the smart-turn v3 classifier (8 MB int8 ONNX, BSD-2) reads the recorded
waveform and says whether the speaker finished or paused to think. A pause
extends the wait; a finished turn commits immediately.

This replaces the fixed silence timeout the first child ships with, which cuts
the user off whenever they think mid-sentence. Published measurements put a
turn model at about a 10% false-cutoff rate where a plain silence rule sits
near 28% at the same latency.

Capture must also change: today `audio.rs` batches a fifth of a second and
polls every 50 ms, so no detector can see audio sooner than 250 ms. The
capture path gains a 20 ms frame callback; the batching stays for the GPT
provider.

## Acceptance

- [ ] Capture delivers 20 ms frames to the local provider, and the GPT provider still receives its 200 ms batches.
- [ ] Silero VAD and smart-turn v3 run in-process through `ort`, with the model files vendored or fetched to a documented path.
- [ ] A fixture utterance that ends mid-clause is not committed; the same utterance completed is committed.
- [ ] The wait has a documented floor and ceiling, and the ceiling forces a decision.
