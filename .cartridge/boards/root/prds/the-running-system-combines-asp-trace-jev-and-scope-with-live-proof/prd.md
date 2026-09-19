---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge"
commit: "0b74bc37e7c075234bd22abfefbfe16d114b01b4"
---

# The running system combines ASP trace JEV and scope with live proof

## Outcome

The work in the ASP containment, scope telemetry and JEV panes runs as one
composition. A repeatable live check follows real ASP entities into JEV's two
model passes and observes the resulting activity through scope's endpoint.
Trace cycle telemetry is reachable through ASP. A missing capability or a
failed cartridge must fail the check rather than count as an integrated system.

## Acceptance

- [x] `just test system` passes against the running composition with stored auth.
- [x] JEV retrieves ASP entities and completes both model passes, with file text withheld by default.
- [x] ASP exposes the composition root, trace root and real cycle telemetry, and scope receives activity.
- [x] The standard `just test jev` gate works and its regression suite passes.
- [x] Independent verification, affected owner audits and isolation pass.
