---
state: open
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/health.rs"
- "src/catalog.rs"
- "src/sync.rs"
- ".cartridge/tests"
---

# a model that names another endpoint is routed to that endpoint

## Outcome

A model the provider serves only on its Responses endpoint is routed there.
The router already speaks that wire and already has a way to mark a route as
needing it; the mark is simply missing on the routes that need it, and the
provider's refusal is the evidence that sets it.

## Evidence

Measured on 2026-09-16:

```
gpt-5.3-codex@openai   14 attempts   This model is not supported in the
                                     v1/chat/completions endpoint. Use the
                                     v1/responses endpoint instead.
```

The catalog already carries this distinction: a route whose `model` begins
`responses/` is dispatched on the Responses wire, and `proxy.rs` `attempt`
strips the prefix before sending. Several routes carry it —
`responses-gpt-5.5@openai`, `responses-gpt-5.6-luna@chatgpt`. `gpt-5.3-codex`
does not, so `sync` admitted it as a Chat route and every attempt goes to the
endpoint that refuses it.

Fourteen attempts against a fixed, permanent property of the model.

## Acceptance

- [ ] The provider's `Use the v1/responses endpoint instead` refusal moves the
      route to the Responses wire and records it, so the correction survives a
      restart and a `sync`.
- [ ] The corrected route answers on retry in the same turn.
- [ ] `sync` does not undo the correction on its next inventory refresh, and a
      test proves it.
- [ ] A test asserts the retried request went to the Responses endpoint with
      the model id carrying no `responses/` prefix on the wire.
- [ ] The correction is recorded per route, not as a rule about the provider:
      the same provider serves both wires.

## Planning note

2026-09-16. Filed from [[@router/system/vision.md]]. This is the only one of
the seven causes where the router already has the capability and is merely
pointing a route at the wrong half of it.
