---
state: "analyzing"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/auth.ctg"
work-kind: leaf
needs:
  - '@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values'
footprint:
  - 'src'
  - 'cartridge.json'
  - 'README.md'
  - '.cartridge/help.md'
  - '.cartridge/docs/README.md'
  - '.cartridge/tests'
claim: "coordinator-e4-1 2026-09-19T14:51:55.857Z"
---

# auth writes the router's credential file from pass

## Outcome

The router streams model traffic with a provider key held in its own
process, so auth cannot make those calls for it. auth instead calls
`router {op:"login"}` and `router {op:"logout"}` through a declared need, with
the pass store's current contents; the router still owns and writes its own
`credentials.json` (mode `0600`). pass is the source of truth and the file is a
derived cache. The router does not change.

Amended 2026-09-19 by planner cartridge-e4 on the analyst's evidence: auth
writing the router's file directly would break the isolation rule, and auth's
own sandbox grants it no write under the router's directory.

## Context

`router {op:"login", provider, key}` writes `<PROVIDER>_API_KEY` into
`credentials.json` (`router.ctg/src/service.rs:200-220`,
`router.ctg/src/auth.rs:1061`). After this PRD a key is added with
`pass insert cartridge/<provider>/api-key`, and
`auth {op:"materialize"}` rewrites the file. OAuth device flows and refresh
tokens stay with the router and are out of scope.

## Acceptance

- [ ] `auth {op:"materialize"}` writes every `cartridge/<provider>/api-key`
      entry as `<PROVIDER>_API_KEY`, atomically and with mode `0600`, keeps
      the entries the router wrote for OAuth, and returns names only.
- [ ] A named test shows that a key removed from pass disappears from the
      file on the next materialize.
- [ ] The response and every published envelope are asserted free of the
      fixture's value.
- [ ] `README.md` and `.cartridge/help.md` tell the user to add a key with
      `pass insert`, and say that the router's `login` with a `key` is
      superseded.
