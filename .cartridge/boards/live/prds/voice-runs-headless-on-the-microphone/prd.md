---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/live.ctg"
needs: ["@auth/gpt-live-connects-over-websocket-on-the-discovered-credential"]
footprint: ["src/**", ".cartridge/**", "cartridge.json", "init.lua"]
---

# Voice runs headless on the microphone

## Outcome

When voice is wanted on a conversation (`POST /api/voice` or `live {op:"voice"}`
enabled), the Live service opens a GPT Live WebSocket session through
`auth.live`, captures the default microphone with `ffmpeg` (PCM16 mono 24 kHz)
and plays `session.output_audio.delta` with `ffplay`. No browser page and no
WebRTC peer. Turning voice off closes the session; delegated work keeps
running. The mic is gated while speech plays unless the conversation is set to
duplex (headphones).

## Acceptance

- [x] Enabling voice starts capture and a session; disabling it stops capture, playback and the session within 2 s, leaving no `ffmpeg`/`ffplay` process.
- [x] Transcripts and delegations from the WebSocket session land in the same store the WebRTC path used.
- [ ] `grant.exec` names `ffmpeg` and `ffplay`; missing binaries or microphone permission surface as a readable voice error in `state`.
- [x] A test drives the service against a mock `auth.live` and fake capture/playback commands.
