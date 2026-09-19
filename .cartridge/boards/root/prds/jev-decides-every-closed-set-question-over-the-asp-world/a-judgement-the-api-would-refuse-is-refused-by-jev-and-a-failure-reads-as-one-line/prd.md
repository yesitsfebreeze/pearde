---
state: "done"
origin: derived
priority: 95
repo: "/Users/feb/dev/cartridge/jev.ctg"
work-kind: leaf
needs:
  - '@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open'
footprint:
  - README.md
  - .cartridge/help.md
  - 'src/jev.ts'
  - '.cartridge/memos/judgement/example-needs-an-llm.md'
  - '.cartridge/memos/type/judgement.md'
  - '.cartridge/tests/integration/decide.test.ts'
commit: "bd7b7e0f11c18d350faee6f9fac8f1cd7197efbb"
---

# a judgement the api would refuse is refused by jev and a failure reads as one line

## Outcome

`validate` refuses a question whose `criteria` the TypeSafe API would refuse,
the shipped example judgement is one the API accepts, and the `reason` of a
failed `auth.jev` call is one line that starts with auth's type word.

## Context (observed 2026-09-19, coordinator-b0)

The first live `jev {op:"decide", point:"@jev/example-needs-an-llm"}` after
the core was collected at jev.ctg `78b7fe4` failed open, as designed, but for
a defect: the API answered HTTP 422, because the example's `criteria` are
strings. The API takes `{true?, false?}` for a `noul`, a required map of
option to description or null for a `choice`, and a required array of at
least two level descriptions for a `score`
(`@auth/auth-answers-a-jev-question-on-the-stored-typesafe-key`, spec, API
facts). `validate` checked none of that. The same call returned the reason
`auth: runtime error: upstream: TypeSafe refused the request (HTTP 422).`
followed by a Lua stack traceback: the host wraps a Lua listener's error, so
auth's type word is not at the start and a consumer cannot match on it.

## Acceptance

- [x] Named tests show `validate` refusing a `noul` with string criteria, a
      `choice` without an option map of at least two options, and a `score`
      without an array of at least two levels, and accepting the documented
      shapes.
- [x] A named test shows that a wrapped failure
      (`auth: runtime error: upstream: …` plus a traceback) gives the one-line
      reason `upstream: …`, and that a message with no type word gives its
      first line.
- [x] The shipped example passes `validate`, and `type/judgement.md` states
      the three criteria shapes.
