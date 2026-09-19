---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/plan.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/socket.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/transport.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs
commit: "804a08b63fd44a3fc1f473ce25d1fc789bedc262"
---

# the agent reaches asp as tool.asp and the base owns that event

## Outcome

ASP is one of the agent's tools. Every cartridge that needs `tool.*` (mcp,
proxy, agent, harness) finds `tool.asp` beside the other tools and speaks the
same envelope to it: `describe`, `call`, `cancel`. No cartridge ships the
tool. The base is a participant of its own composition: it owns the event
`tool.asp`, listens to it on the host socket, and appears as its owner `host`.

An action is never run through ASP by a cartridge. ASP tells the agent which
tool an action names and with which arguments, and the agent runs that tool
through its own dispatch, where policy is asked. Only the command line may
`act`.

## Decision (2026-09-19, ASP coordinator)

- The base takes part through one synthetic plan (`host_plan`), so the
  catalogue, the `tool.*` glob, the clash check, a sender's directory and the
  readiness check all treat `tool.asp` like any other event, with no special
  case in any of them.
- Policy is asked by each harness before it sends a tool event; there is no
  central tool dispatch. A cartridge-reachable `act` would therefore be a way
  around policy, so it is refused on both doors a cartridge has
  (`cartridge.host("asp")` and `tool.asp`).

## Acceptance

- [x] A named test gives a cartridge that needs `tool.*` the need `tool.asp`,
      owned by `host`, and gets `describe` and an `expand` through it.
- [x] A named test shows that `act` asked by a cartridge is refused on both
      doors and that the action's tool is never reached.
- [x] A cartridge that declares `tool.asp` itself fails with the usual clash.
      Covered by the catalogue order; the base's plan comes first.
- [x] `docs/asp.txt` and `docs/transport.txt` describe the tool and the rule.
