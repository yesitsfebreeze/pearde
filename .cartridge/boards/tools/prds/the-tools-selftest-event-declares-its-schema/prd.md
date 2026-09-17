---
state: open
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge/tools.ctg"
footprint:
- "cartridge.json"
---

# The tools.selftest event declares its schema

## Outcome

The `tools.selftest` event declares the shape of what it accepts, so a caller can be
told what to send by the manifest rather than by reading the cartridge's source,
and `just audit` stops reporting `hard: event tools.selftest declares no schema`.

## Evidence

`just audit` from the superproject root, 2026-09-17, coordinator cartridge-2e:
0 of 17 cartridges pass the hard checks. Besides the seventeen missing READMEs,
the audit reports exactly two schema findings, and this is one of them:

```
  hard: event tools.selftest declares no schema
```

The standing memo is that a cartridge "declares its whole surface in
cartridge.json". An event with no schema is surface the manifest does not
describe, so the agent's own discovery path cannot tell a caller what the event
takes.

## Acceptance

- [ ] `tools.ctg/cartridge.json` declares a schema for `tools.selftest` that
      matches what the handler really accepts, including which fields are
      optional.
- [ ] A call that violates the declared schema is refused against the
      declaration rather than failing somewhere inside the handler.
- [ ] `just audit` no longer reports `event tools.selftest declares no schema`.

## Note on scope

One event, one manifest. The seventeen missing-README findings from the same
audit are filed separately, one per owning board.
