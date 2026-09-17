---
state: open
origin: requested
priority: 88
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/audio.rs", "src/local.rs", "src/turn.rs"]
needs: ["the-turn-ends-when-the-speaker-is-done-not-when-silence-runs-out"]
---

# The user can cut the voice off mid-sentence

## Outcome

Speaking over the assistant stops it. On confirmed user speech during playback
the provider cancels the front model's generation, drops the synthesis queue,
clears the playback ring with a short fade so the cut does not click, and
records only the audio that was actually played, computed from the playback
read cursor rather than the clock. The conversation record then says what the
assistant really said, not what it intended to say.

Three guards keep it from firing on nothing: a grace period after the
assistant starts speaking during which only raw speech energy may interrupt, a
minimum of sustained speech before an interrupt counts, and a backchannel list
("mhm", "right", "okay") that never takes the floor. Published measurements put
energy-only detection at a 45–52% false-interrupt rate on backchannels.

With a speaker instead of headphones the microphone hears the assistant, so
this child also carries acoustic echo cancellation, fed from the playback
buffer as its reference signal.

## Acceptance

- [ ] User speech during playback stops the assistant within a documented time and leaves no audible click.
- [ ] The transcript records only the milliseconds of audio the playback cursor reports as played.
- [ ] A backchannel spoken over the assistant does not stop it; a real interruption does.
- [ ] With the speaker in use and echo cancellation enabled, the assistant does not interrupt itself.
