---
state: "analyzing"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/auth.ctg"
footprint: ["src/**", ".cartridge/**", "cartridge.json", "init.lua"]
claim: "cartridge-ed-58f7a3 2026-09-16T09:58:10.065Z"
---

# GPT Live connects over WebSocket on the discovered credential

## Outcome

`auth.live` opens a GPT Live session on the WebSocket transport
(`wss://api.openai.com/v1/live/sessions`, `session.start` first) with the
credential auth discovers, so a consumer can stream microphone audio and
receive speech without a browser or WebRTC peer. The key never leaves auth:
consumers see the session id, relayed server events on `auth.live.event`, and
send client events (including `session.input_audio.append`) through the
existing `send` op.

The credential is the OpenAI Platform key the user already stores through the
router (`router {op:"login", provider:"openai", key}`), read from the
router's configured store — not an environment constant.

## Acceptance

- [x] `auth.live {op:"create", request:{session, transport:{type:"websocket"}}}` connects, sends `session.start` with the given session config, and resolves with `{session:{id}}` on `session.started`; the WebRTC path is unchanged.
- [ ] Server events of a WebSocket session reach `auth.live.event` with `session_id`; `send` forwards client events; `close` sends `session.close` and waits for `session.closed` (bounded 15 s).
- [x] Discovery finds an OpenAI key stored through the router's `login` op in the router's configured credential store; `auth {op:"status"}` reports its source and never the value.
- [x] A test against a local mock WebSocket server covers start, relay, audio append, close, and asserts no event or log line carries the key.

## Questions

- Where is the existing OpenAI Platform key? The router's connections list only a ChatGPT login and auth's checked stores hold no API key. Recommended: the user stores it once with `router login {provider:"openai", key}`; auth reads it from there.
