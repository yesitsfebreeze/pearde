---
state: "done"
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge/tools.ctg"
footprint:
- "cartridge.json"
commit: "f1207c8d86dd02a19a896a3f93bfcc555fabfe24"
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

- [x] `tools.ctg/cartridge.json` declares a schema for `tools.selftest` that
      matches what the handler really accepts, including which fields are
      optional.
- [x] A call that violates the declared schema is refused against the
      declaration rather than failing somewhere inside the handler.
- [x] `just audit` no longer reports `event tools.selftest declares no schema`.
      Satisfied, but not by this change: commit 8d0dbe6 had already added
      `"schema": {}`, and the audit rule at
      `.cartridge/memos/routine/audit-cartridges.md:118` is `if (!event.schema)`,
      which an empty object clears while refusing nothing. The verifier observed
      `just audit tools` exit 0 against the live tree that still carries `{}`.
      This change cannot regress it, and the other two boxes are what it earns.

## Note on scope

One event, one manifest. The seventeen missing-README findings from the same
audit are filed separately, one per owning board.
