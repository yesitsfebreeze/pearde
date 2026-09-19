---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/live.ctg"
work-kind: leaf
capability-owner: live
footprint:
  - /Users/feb/dev/cartridge/live.ctg/src/service.rs
  - /Users/feb/dev/cartridge/live.ctg/README.md
  - /Users/feb/dev/cartridge/live.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/live.ctg/.cartridge/docs/README.md
commit: "0d502e15e3691ee20e5a8953feb96425ca6864de"
---

# live reads the composition from asp

## Outcome

The voice session's instructions list every composed cartridge with the events it provides, read from the host's ASP `types` (`cartridge.host("asp", {op:"types"})`, whose `events` map names each event's owner) instead of `memo {op:"fabric"}`, which no longer exists.

## Acceptance

- [x] A named test shows the composition is the last thing the voice session is given.
- [x] `rg -n fabric live.ctg/src` finds nothing.
