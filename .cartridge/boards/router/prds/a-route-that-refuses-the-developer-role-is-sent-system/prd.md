---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/health.rs"
- ".cartridge/tests"
---

# a route that refuses the developer role is sent system

## Outcome

The instruction message reaches every route under a role that route accepts.
The `system`/`developer` disagreement is adapted in both directions, not one.

## Evidence

Measured on 2026-09-16:

```
qwen3.8-max@opencode-go   Error from provider (Console Go): Upstream request
                          failed: [invalid_parameter_error] developer is not
                          one of ['system', ...]
```

`protocol.rs` `to_chat` writes the instruction as `role: "developer"`, and
`to_responses` converts `system` to `developer` as well. `Rules` has a
`developer_role` flag that rewrites `system` into `developer` — the direction
that was already needed once — and no way to express the reverse.

One route today. The reason to fix it is not the route: it is that the
adaptation mechanism is directional for no reason, and the next provider to
disagree about roles will disagree in whichever direction it likes.

## Acceptance

- [ ] The role adaptation is two-directional: a route can be recorded as
      wanting `developer` or as wanting `system`, and a route with no recorded
      preference is sent the default the wire translation produces.
- [ ] `propose` learns the reverse direction from the observed wording, which
      names the accepted roles rather than the refused one.
- [ ] The same rewrite covers both `messages` and `input`, as the existing flag
      does.
- [ ] A test drives the observed message through the loopback fixture and
      asserts the retry carries `role: "system"`.
- [ ] A test pins that the two directions cannot both be recorded for one
      route.

## Planning note

2026-09-16. Filed from [[@router/system/vision.md]]. Small, and worth doing
with the rest because it removes the last place where the adaptation record
encodes a single provider's preference rather than a per-route fact.
