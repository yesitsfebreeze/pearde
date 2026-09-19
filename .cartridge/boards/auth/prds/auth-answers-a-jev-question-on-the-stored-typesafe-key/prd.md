---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/auth.ctg"
work-kind: leaf
needs:
  - '@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values'
footprint:
  - 'src/**'
  - 'cartridge.json'
  - 'README.md'
  - '.cartridge/help.md'
  - '.cartridge/docs/README.md'
  - '.cartridge/tests/**'
  - 'init.lua'
---

# auth answers a jev question on the stored typesafe key

## Outcome

Another cartridge sends `auth.jev` a state and a set of typed questions and
gets JEV's answers back. auth holds the TypeSafe key, fixes the destination
and makes the call. The caller supplies neither a credential nor a URL,
which is the invariant `auth.live` already keeps.

## Context

JEV is TypeSafe's System One model. It has one endpoint,
`POST https://api.typesafe.ai/v1/systemone`, with `Authorization: Bearer`.
A request is `{state, model: "jev-latest", questions}`. `state` is a string,
object or array of text. Each question is a `noul` (yes or no, answered as a
number from 0 to 1), a `choice` (one option, with `probabilities` and
`confidence`) or a `score` (a level, with `probabilities` and `confidence`).
The model does not generate text. The limits are 64k tokens per request, 32k
for the state plus the longest question, 250,000 tokens per second and 1,200
requests per minute. `429` and `529` ask for exponential backoff. The
references are https://docs.typesafe.ai/api.md,
https://docs.typesafe.ai/models.md and
https://docs.typesafe.ai/model-jaggedness/jev-1.13.md.

## Decision (2026-09-19, coordinator)

- The event is `auth.jev`, not a generic `auth.fetch {provider, path}`. One
  provider does not justify the abstraction. When a third authenticated
  provider arrives, `auth.live` and `auth.jev` are folded into one.
- The key is the pass entry `cartridge/typesafe/api-key`.
- Retry with exponential backoff on `429` and `529` lives here, bounded by a
  `timeout_ms` declared in auth's manifest, because a caller cannot cancel a
  cartridge call (see the memory note of that name).
- The footprint includes `init.lua` (2026-09-19, coordinator-b0, from the
  analyst's pre-draft). `init.lua:12` registers each served event by name,
  `{ "auth", "auth.live" }`, so `auth.jev` has no listener without it.
- The API's `questions` and `answers` are maps keyed by the caller's ids,
  not lists, and `auth.jev` passes both through unchanged
  (https://docs.typesafe.ai/api.md, read 2026-09-19). A `noul` answer
  carries no `confidence`; only `choice` and `score` do
  (https://docs.typesafe.ai/confidence.md). An error body is undocumented,
  so `auth.jev` never parses or forwards one.
- A failure is a message that starts with one type word: `invalid`,
  `unavailable`, `unreachable`, `upstream`, `rate_limited` or `overloaded`.
  A caller passes the message through as its reason.
- The pre-draft spec is `proposals/spec01-draft.md`, read at `auth.ctg`
  `d875108` against the pass prerequisite's spec. It calls `entry("typesafe")`
  and `read(name, deps)` from `src/pass.ts`, and is revalidated when that
  file lands.

## Start at

- `auth.ctg/src/openai.ts` and `auth.ctg/src/wire.ts`: how `auth.live` fixes
  its destination and keeps the key in the process.
- `auth.ctg/cartridge.json`: `grant.net` gains `api.typesafe.ai`.

## Acceptance

- [ ] `auth.jev {state, questions, model?}` returns `{answers, usage}` as
      the API gives them. A named test runs it against a local fixture
      server and asserts the bearer header and the fixed path.
- [ ] A request naming a URL, a host or a key is rejected by the schema.
- [ ] A named test shows `429` then `200` succeeding after one backoff, and
      `529` throughout ending in a bounded, typed failure.
- [ ] With no `cartridge/typesafe/api-key` entry the call fails with
      `unavailable` before any request leaves the process.
- [ ] One live probe against the real API is recorded in the evidence note,
      with its latency and `usage`.
- [ ] `README.md` and `.cartridge/help.md` document `auth.jev`.
