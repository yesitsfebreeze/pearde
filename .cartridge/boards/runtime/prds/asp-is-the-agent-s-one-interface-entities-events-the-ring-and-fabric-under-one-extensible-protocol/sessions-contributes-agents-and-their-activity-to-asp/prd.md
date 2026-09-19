---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/sessions.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
footprint:
  - /Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/integration/asp.py
  - /Users/feb/dev/cartridge/sessions.ctg/src/asp
  - /Users/feb/dev/cartridge/sessions.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/changes.rs
  - /Users/feb/dev/cartridge/sessions.ctg/src/change_record.rs
  - /Users/feb/dev/cartridge/sessions.ctg/cartridge.json
  - /Users/feb/dev/cartridge/sessions.ctg/init.lua
  - /Users/feb/dev/cartridge/sessions.ctg/README.md
  - /Users/feb/dev/cartridge/sessions.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/unit/asp.rs
commit: "aa766580095db02d902201687b59da0fa5bde6e6"
---

# sessions contributes agents and their activity to ASP

## Outcome

sessions is an ASP provider and the canonical owner of `agent:` (the session
id). It contributes the agent's roster facts and its attributed activity. The
change evidence it already records (actor, target path, revision before and
after) becomes `touched` edges from `agent:` to `file:`, each carrying the
revision. Expanding a file shows which agents changed it and at which
revisions, without a separate call to sessions.

## Start at

- `sessions.ctg/src/change_record.rs:40-96`: `Actor`, `Target`, `Version`
  and `Evidence`.
- `sessions.ctg/src/changes.rs:20-64`: the bounded change log.
- The delivered roster work: `@sessions/an-agent-is-one-lookup-from-the-roster`.
- `@sessions/the-board-log-replays-who-did-what` (deferred): board activity
  replay, which this PRD can feed into the ring.

## Acceptance

- [x] A named test expands an `agent:` entity and gets its roster facts.
- [x] A named test records a change through fs. Expanding the file then
      returns a `touched` edge from the agent that carries the new revision.
- [x] sessions' `cartridge.json` declares the `agent` scheme and the `touched`
      edge. The README and help page are updated.
