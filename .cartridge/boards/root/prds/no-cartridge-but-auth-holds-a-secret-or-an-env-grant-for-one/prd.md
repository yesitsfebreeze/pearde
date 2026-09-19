---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge"
work-kind: rollup
needs:
  - '@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values'
  - '@auth/auth-writes-the-router-s-credential-file-from-pass'
---

# no cartridge but auth holds a secret or an env grant for one

## Outcome

auth is the only cartridge whose manifest grants access to a secret. No
other cartridge declares `grant.env` for a key, has a `*_key_env` setting or
reads a credential file. Each of them either asks auth to make the call or
reads a file that auth derived.

## Context

This is a rollup. The analyst adds one child per owner, on that owner's
board, and gives this PRD no footprint of its own. The census on 2026-09-19:

- `live.ctg`: `grant.env: ["OPENAI_API_KEY"]`.
- `web.ctg`: `grant.env: ["WEB_*"]` and the setting `brave_api_key_env`.
- `proxy.ctg`: `CARTRIDGE_PROXY_KEY`, through `key_env` in
  `.cartridge/config.lua`.
- `harness.ctg`: `grant.env: ["HARNESS_ROSTER_*"]`. Confirm whether it holds
  a secret at all.
- `sessions.ctg`: `grant.env: ["SESSIONS_MAILBOX_*"]`. Confirm the same.
- `router.ctg`: `login` with a `key`, and the environment names in its
  catalog.
- `auth.ctg`: the discovery steps after pass.

## Acceptance

- [ ] Every owner in the census has a child PRD, or a recorded decision that
      it holds no secret.
- [ ] `just audit` fails a cartridge other than auth that declares an env
      grant for a key or a `*_key_env` setting.
- [ ] The superseded settings, grants and discovery steps are deleted in the
      same changes that replace them.
