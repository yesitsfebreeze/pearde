---
state: open
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/local.rs", "src/service.rs", "cartridge.json", ".cartridge/docs", "README.md", ".cartridge/help.md"]
needs: ["live-speaks-and-listens-through-local-sidecars"]
---

# A persona record chooses the voice and the turn-taking dials

## Outcome

Who the voice is stops being a string in `service.rs`. A persona memo names the
voice and the behaviour, and the local provider resolves it when a conversation
opens: the timbre (a named voice or a reference clip), speaking rate, how
readily it takes the floor, how patient it is before deciding a turn ended, how
often it backchannels, whether it uses a holding phrase while work runs, and
the spoken style that goes into the instructions.

Changing persona is changing one record, and it takes effect on the next
conversation without a rebuild.

## Acceptance

- [ ] The persona type documents the voice fields, with defaults for every one.
- [ ] Opening a conversation with a named persona uses that voice and those dials; a second persona sounds and behaves differently on the same machine.
- [ ] An absent or malformed persona falls back to documented defaults rather than failing the conversation.
- [ ] The hardcoded instruction string in `service.rs` no longer decides the character.
