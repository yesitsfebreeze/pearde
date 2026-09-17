---
state: open
origin: requested
priority: 95
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/lib.rs", "src/service.rs", "src/socket.rs", "src/transport.rs", "cartridge.json", "README.md", ".cartridge/help.md"]
---

# A setting chooses the transport, and the GPT one keeps working

## Outcome

`live` gains a `provider` setting. Today `start_voice` fetches a credential and
dials `socket::connect` at one call site; after this it asks a seam which
transport to build, and the GPT transport is one implementation of that seam,
behaving exactly as it does now.

Nothing else changes. `Service::event` keeps its arms, the record keeps its
shape, and with `provider: "gpt"` — the default — a conversation is
indistinguishable from today's. The second implementation is the next child's
work; this one only makes room for it, and proves that making room broke
nothing.

The seam is deliberately small: `send`, `audio`, `close`, `id`, and a
constructor taking the session configuration and an event callback. Those are
the only four things the service asks of a session today.

## Acceptance

- [ ] `cartridge.json` declares `provider` with default `"gpt"` and a documented doc string.
- [ ] `src/transport.rs` holds the seam as an enum, and `src/socket.rs` is one variant of it with its behaviour and its endpoint constant unchanged.
- [ ] `src/service.rs` builds the transport through the seam: `socket::credential` is reached only on the GPT branch, and `socket::connect` is not named in `src/service.rs` at all.
- [ ] Selecting an unknown provider fails the `voice` call with a message naming the setting and the values it accepts, rather than falling back silently.
- [ ] The existing `mod tests` in `src/socket.rs`, `src/audio.rs` and `src/service.rs` — three, three and five tests — pass unchanged, and a new test asserts the seam returns the GPT variant for `"gpt"` and an error for anything unknown.
- [ ] `README.md` and `.cartridge/help.md` describe the setting and both values.
