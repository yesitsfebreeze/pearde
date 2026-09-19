---
state: "done"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/jev.ctg"
work-kind: leaf
needs:
  - '@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open'
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
footprint:
  - 'src'
  - '.cartridge'
  - 'cartridge.json'
  - 'README.md'
commit: "215007548e4d26907ba51893b8084aa63d662c90"
---

# jev pulls asp slices narrows them in two passes and sends only allowed schemes

## Outcome

A caller names entities or a search instead of building a state:
`jev {op:"decide", point, about: [ids], search?}`. jev.ctg pulls those
entities from `asp`, asks JEV which of them bear on the question, and sends
only the survivors with the real question. The whole ASP world is within
JEV's reach, and no request carries more of it than the decision needs.

## Decision (2026-09-19, coordinator)

- The first pass is one request with one `noul` per candidate ("does this
  entity bear on <the judgement's subject>?"), the shape of TypeSafe's
  re-ranking cookbook. The second pass sends the top `k` as an object keyed
  by entity id, since JEV's documentation recommends named fields. `k` and
  the first-pass threshold are fields of the judgement.
- Egress is a setting, `allow_schemes`, which defaults to
  `["symbol", "event", "agent", "memo"]`. The contents of `file:` and
  `range:` entities leave the machine only when the user adds those schemes.
  An entity of a scheme that is not allowed is sent as its id only, and
  the response names what was withheld. Arbitrary attributes are excluded
  because trace attributes carry complete records.
- Numbers, dates and counts are computed in code before the request and
  passed as labelled fields. No judgement asks JEV to compare or to count.

## Start at

- The ASP core PRD's `expand` and `search`.
- https://docs.typesafe.ai/cookbooks/rerank_typesafe.md and
  https://docs.typesafe.ai/patterns/fan-out.md.

## Acceptance

- [x] A named test with a fixture `asp` of 200 entities shows that the
      second request carries at most `k` of them and stays under the token
      budget.
- [x] A named test shows that a `file:` entity's body is absent from the
      outgoing request under the default setting, is present once `file` is
      allowed, and that the response lists what was withheld.
- [x] A named test shows that a stale or retracted entity from ASP is
      dropped before the first pass.
- [x] A live probe on the real composition records both latencies and both
      `usage` values in the evidence note.
- [x] `README.md` and `.cartridge/help.md` document `about`, `search` and
      `allow_schemes`.
