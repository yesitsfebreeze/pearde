---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/local.rs", "src/service.rs"]
needs: ["live-speaks-and-listens-through-local-sidecars"]
---

# The voice hands real work to the agent and holds the floor while it runs

## Outcome

The front model answers conversation and nothing else. Anything that needs the
repository, the machine or careful reasoning becomes a delegation, which takes
the path `live` already has: `session.delegation.created` with a client target,
the watching session or the local agent, and `reply` coming back to be spoken.

While that work runs the voice keeps the floor: an immediate short
acknowledgement, then a holding line on an idle timer that resets whenever the
agent reports progress, so a minute of work is not a minute of silence. When
the answer arrives it is spoken in at most two sentences and written to the
record in full.

## Acceptance

- [ ] A spoken greeting is answered locally and creates no delegation.
- [ ] A question about this repository creates exactly one delegation and the answer is spoken.
- [ ] Work that outlasts the idle timer produces a holding line, and the timer resets on progress rather than stacking lines.
- [ ] The full answer is in the record; the spoken form is the short one.
