---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge"
work-kind: rollup
needs:
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol'
---

# jev decides every closed-set question over the asp world

## Outcome

Every closed-set judgement in the composition goes to JEV first: whether,
which, how much and enough. JEV answers with a typed decision and a
confidence. A confident answer is acted on, and an uncertain one falls to
the path that decides today, which is an LLM or a rule. JEV reaches the
whole ASP world by pulling the slice a decision needs, and every decision it
makes is itself a fact in that world.

## Direction (2026-09-19, user)

"We want to build the cartridge as best and integrated as possible so pretty
much every decision, every ask, every question should go to Jev, who has the
whole ASP available." And: "put focus on JEV after the ASP is done." This
rollup therefore needs the ASP master PRD, and its priority sits below
ASP's. The key goes through auth: "cant we use the auth cartridge for the
key???"

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

Three limits in JEV's own documentation shape the design.

1. It does not generate text. An open question stays with an LLM. JEV
   decides whether an LLM is needed, which one, and with what context.
2. "Accuracy falls as the state grows with content unrelated to the
   decision", and the state is capped at 32k tokens. The whole ASP is
   therefore never sent. It is reachable, and JEV narrows its own input.
3. It is weak at arithmetic, dates, counting and adversarial content. Code
   computes what code can compute. JEV is never in a permission path, and
   policy.ctg remains the only authority on what may run.

## Decision (2026-09-19, coordinator)

- `jev.ctg` is a new cartridge. It is pure logic: it has no net grant, no
  env grant and no key setting. Its `needs` are `auth.jev?` and `memo?`, both
  optional, which is how fail-open is declared. It never needs `asp`: `asp`
  is the base's own service key and is reached without a need
  (`cartridge.ctg/docs/asp.txt`). It starts as a plain tracked directory like
  `web.ctg`, because a submodule needs a remote that only the user may
  create; child 1 records the reasoning (2026-09-19, coordinator-b0).
- A decision point is a memo of kind `judgement`: the question, the
  criteria, the gates and the fallback. The kind `decision` already exists
  and means a settled choice, so it is not reused. A memo needs no new
  manifest block, so `deny_unknown_fields` in
  `cartridge.ctg/src/loader/document.rs` is not touched, and a threshold
  changes without a rebuild.
- JEV fails open. Unavailable, rate-limited and low-confidence all mean that
  today's path runs. JEV never blocks a request.

## Children

1. `@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open`
2. `@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-pulls-asp-slices-narrows-them-in-two-passes-and-sends-only-allowed-schemes`
3. `@root/jev-decides-every-closed-set-question-over-the-asp-world/every-jev-decision-is-an-asp-entity-and-its-recorded-outcome-tunes-the-gate`

The first consumers are on their owners' boards:
`@harness/jev-picks-which-memos-and-entities-enter-the-context`,
`@memo/memo-resolve-asks-jev-which-memos-match-the-situation` and
`@router/jev-routes-a-request-to-a-model-tier-by-intent`.

Later consumers get a PRD only after the first three show a measured gain:
the proxy's choice of entities to enrich a request with, the agent's tool
pre-selection and its "done" and "stalled" checks, live's voice intent
routing, the fabric's rerank, and advisory screening of tool results for
injected instructions.

## Acceptance

- [ ] Every child and the three first consumers are collected.
- [ ] Integration check: with the composition running, a request passes
      through the harness, JEV picks its context from ASP entities, the
      `jev.decided` event is in the ring, and the `decision:` entity names
      the entities it was about. With auth's TypeSafe entry removed, the
      same request completes on today's path.
