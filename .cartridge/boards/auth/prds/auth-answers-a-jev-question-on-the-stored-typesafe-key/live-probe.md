# Live probe of auth.jev against the real TypeSafe API

Run by coordinator cartridge-b0 on 2026-09-19 after the collect at auth.ctg
`fa3490b`, with auth.ctg trusted alone and `cartridge reload auth`. The key
was stored by the planner session through `src/insert.ts` on the user's
behalf. This note is separate from `collection.md`, which the collect wrote
and which is left untouched.

- `cartridge call auth '{"op":"status","provider":"typesafe"}'` answered
  `state: available_unverified`, `source: pass`,
  `entry: cartridge/typesafe/api-key`.
- One `cartridge call auth.jev` with a `noul` question (`is_urgent`) and a
  three-option `choice` question (`dept`) over a one-sentence state: exit 0,
  wall-clock 1061 ms including the gpg read and the CLI round trip.
- Answer: `is_urgent` was `{type: "noul", noul: 0.98}` with no `confidence`
  field, as the docs say. `dept` was `{type: "choice", choice: "technical",
  confidence: 1, probabilities: {billing: 0, sales: 0, technical: 1}}`.
- `usage` was `{input_tokens: 358, output_tokens: 58}`.
- A request with an extra `url` property was refused by the host before
  auth: "`auth.jev` payload rejected by its schema: Additional properties are
  not allowed ('url' was unexpected)". The host compiled the new schema.
- No `rate_limited` or `overloaded` answer was seen, so the retry headers of a
  real 429 or 529 remain unobserved.
- After the reload every cartridge in `cartridge status` was `active`.

jev's provisional 3000 ms timeout leaves about 1.9 s of headroom over this
one measurement.
