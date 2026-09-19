---
state: "done"
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge/docs.ctg"
footprint:
- "cartridge.json"
commit: "a44f957358626a078bde7412935c026ea20d12d9"
---

# The docs.discover event declares its schema

## Outcome

The `docs.discover` event's schema says what the handler really takes: no payload
(`null` or an empty object). The host then refuses any other payload against the
declaration, before the handler runs. A caller learns what to send from the
manifest, not from the cartridge's source.

## Evidence

As of 2026-09-19 (docs.ctg HEAD 7e2d752): docs.ctg commit 282aacc (2026-09-17)
added `"schema": {}` to `docs.discover`. `just audit` now reports
`18 of 18 cartridges pass the hard checks`, and docs.ctg passes, so box 3 already
holds. The remaining gap is that `{}` accepts every JSON value, which means no
call can violate it and the host refuses nothing. The handler
(`src/lib.rs` `fn announce(_: &Lua, (): ())`) reads no payload. Every in-tree
caller sends `null`: the CLI `call|send|run` default, `cartridge verify`'s
contract call, and docs.ctg's host tests.

The original finding, from `just audit` at the superproject root, 2026-09-17, coordinator cartridge-2e:
0 of 17 cartridges pass the hard checks. Besides the seventeen missing READMEs,
the audit reports exactly two schema findings, and this is one of them:

```
  hard: event docs.discover declares no schema
```

The standing memo is that a cartridge "declares its whole surface in
cartridge.json". An event with no schema is surface the manifest does not
describe, so the agent's own discovery path cannot tell a caller what the event
takes.

## Acceptance

- [x] `docs.ctg/cartridge.json` declares a schema for `docs.discover` that
      matches what the handler really accepts, including which fields are
      optional.
- [x] A call that violates the declared schema is refused against the
      declaration rather than failing somewhere inside the handler.
- [x] `just audit` no longer reports `event docs.discover declares no schema`.

## Note on scope

One event, one manifest. The seventeen missing-README findings from the same
audit are filed separately, one per owning board.
