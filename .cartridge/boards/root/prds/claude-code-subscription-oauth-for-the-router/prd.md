---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
---

# True proxy passthrough for Anthropic models

## Outcome

A request that reaches the harness proxy on the Anthropic wire naming a Claude
model (Fable, Opus, Sonnet, Haiku) is relayed verbatim to the original
Anthropic API, with the caller's own credential forwarded, and the genuine
upstream response — JSON or SSE — is returned unchanged. The proxy stores no
Anthropic credential and substitutes no model: for these requests it is a
true transparent proxy. Requests the router can serve keep the existing
harness loop untouched.

## Findings (verified this session)

- The proxy answers `claude-sonnet-4-5` with `no compatible route` today:
  the shelf has no Anthropic provider credential, and the router's only
  anthropic path is a plain `x-api-key`.
- The keychain subscription credential (`claudeAiOauth`) is dead: the access
  token expired and the refresh token is hard-expired
  (`invalid_grant: Refresh token expired`). Re-login would be needed to use
  it, and the user does not want cartridge to own or extract that token.
- A Claude Code client pointed at the proxy sends its own credential on
  every request (`Authorization: Bearer` for an auth token, `x-api-key` for
  an API key). Today the proxy drops transport headers
  ("Transport headers are not forwarded as provider headers").
- The claude-api docs confirm OAuth tokens require
  `Authorization: Bearer` + `anthropic-beta: oauth-2025-04-20`; both arrive
  from the caller and must be forwarded, not rebuilt.

## Plan

1. Proxy HTTP path: when the request is on the Anthropic wire
   (`POST .../messages`) and the router has no compatible route for the
   requested model, relay the request body and the caller's
   auth/anthropic headers verbatim to `https://api.anthropic.com`
   (override via a proxy setting/env), before any harness injection.
2. Stream the upstream response through unchanged: SSE passthrough when
   `stream` is set, JSON body otherwise. Upstream status codes and error
   bodies reach the caller as-is.
3. Requests the router can serve are untouched: injection, internal tools,
   memory recall and routing apply exactly as today.
4. Tests: a fixture upstream proves a claude-model request is relayed
   verbatim (body + caller headers) and its response streams back
   unchanged; a router-servable model still gets the harness loop.

## Acceptance

- [ ] `POST /v1/messages` with `model: claude-sonnet-4-5` through the proxy
      reaches the real `api.anthropic.com` and returns Anthropic's own
      answer — with a valid caller credential, a real completion from the
      requested model; without one, Anthropic's own 401, not a
      `no compatible route` proxy error.
- [ ] The caller's `Authorization` / `x-api-key` / `anthropic-version` /
      `anthropic-beta` headers are forwarded; no credential is stored.
- [ ] SSE requests stream through token-by-token with one final marker.
- [ ] Router-servable models (`auto`, ollama, chatgpt routes) behave
      exactly as before.
- [ ] `just check proxy` and `just test proxy` pass.