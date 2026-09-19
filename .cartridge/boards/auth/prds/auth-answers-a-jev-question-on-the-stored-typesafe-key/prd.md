---
state: "done"
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
commit: "fa3490b6ed4229d09687e6183b6430870a854c84"
---

# auth answers a jev question on the stored typesafe key

## Outcome

Another cartridge sends `auth.jev` a state and a set of typed questions and
gets JEV's answers back. auth holds the TypeSafe key, fixes the destination
and makes the call. The caller supplies neither a credential nor a URL,
which is the invariant `auth.live` already keeps.

## Context

The TypeSafe API facts this rests on (endpoint, request and answer shapes,
limits, `429`/`529` backoff) are in `specs/spec01.md`, read from
https://docs.typesafe.ai/api.md, models.md and confidence.md on 2026-09-19.

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
- Spec rebased on `auth.ctg` `c5e8871`, the collected pass leaf.
- The six type words cover failures inside auth. Host outcomes (a schema
  refusal, `timed_out`, an absent or untrusted cartridge) arrive with the
  host's wording, and a consumer maps both.
- The live probe against the real API is not an Acceptance box, because it
  needs the collected manifest trusted and the person's key. The coordinator
  runs it after collect with the spec's by-hand commands and records the
  result in `collection.md`.

## Start at

- `auth.ctg/src/openai.ts` and `auth.ctg/src/wire.ts`: how `auth.live` fixes
  its destination and keeps the key in the process.
- `auth.ctg/cartridge.json`: `grant.net` gains `api.typesafe.ai`.

## Acceptance

- [x] `auth.jev {state, questions, model?}` returns `{answers, usage}` as
      the API gives them. A named test runs it against a local fixture
      server and asserts the bearer header and the fixed path.
- [x] A request naming a URL, a host or a key is rejected by the schema.
- [x] A named test shows `429` then `200` succeeding after one backoff, and
      `529` throughout ending in a bounded, typed failure.
- [x] With no `cartridge/typesafe/api-key` entry the call fails with
      `unavailable` before any request leaves the process.
- [x] `README.md` and `.cartridge/help.md` document `auth.jev`.
