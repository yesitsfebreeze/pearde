---
state: "done"
origin: requested
priority: 95
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/health.rs"
- "src/protocol.rs"
- ".cartridge/tests/unit/proxy/capabilities.rs"
commit: "08d9463fea82e1484242ae446d0d17c3ad8cfc59"
---

# a tool schema the provider rejects is rewritten to its dialect

## Outcome

A route that refuses a tool's JSON Schema because of the dialect it is written
in receives the same tool in the dialect it accepts, and answers. No route is
shelved for a schema the router could have rewritten without changing what the
tool means.

## Evidence

Measured against the live router on 2026-09-16: 11 of 211 routes carry an open
`compatibility` incident caused by a tool schema, and they are the most
valuable routes on the shelf — every Anthropic-family route the subscription
offers.

```
claude-fable-5-1@claude-code   20 attempts  tools.5.custom.input_schema:
claude-fable-5@claude-code     18 attempts  input_schema does not support
claude-opus-4-8@claude-code    15 attempts  oneOf, allOf, or anyOf at the
claude-sonnet-5@claude-code    18 attempts  top level
... 6 more claude-code routes
gpt-4o-mini@openai              6 attempts  Invalid schema for function
                                            'cartridge_docs': schema must have
                                            type 'object' and not have
                                            'oneOf'/'anyOf'/'allOf'/'enum'
```

Both providers are refusing the same thing: a tool whose top-level schema is a
union rather than an object. `protocol.rs` `to_chat` copies `input_schema` (or
`parameters`) through verbatim, so the caller's dialect reaches every provider
unchanged. The tool named in the OpenAI message, `cartridge_docs`, is this
composition's own MCP tool, so the condition reproduces on any turn that offers
the full tool set.

`health.rs` cannot express the fix. `Rules` can drop a whole top-level request
field or rename the `system` role, and dropping `tools` would change the
meaning of the turn rather than adapt it.

## Outcome shape

A schema rewrite is a meaning-preserving normalization, not a downgrade:

- A top-level `oneOf`/`anyOf`/`allOf` collapses into one object schema whose
  properties are the union of the branches' properties, with `required` limited
  to the properties every branch requires. The union of branches is a superset
  of what each branch accepts, so a call the original schema permitted is still
  permitted.
- A top-level `enum` or a non-object top-level `type` is wrapped in an object
  under a single named property only when the provider refuses it.
- Anything the rewrite cannot express without narrowing what the tool accepts
  is left alone and the route stays refused, per the vision's rule that an
  adaptation preserves meaning or is not made.

## Acceptance

- [x] `Rules` carries a per-route tool-schema normalization, learned from the
      provider's own refusal text through `propose`, exactly as `drop` and
      `developer_role` are.
- [x] `strip_refused`'s same-turn counterpart applies the rewrite and retries
      the same route, so the caller waits once rather than losing the turn.
- [x] The rewrite is proven meaning-preserving by a test: every input the
      original schema validated, the rewritten one validates.
- [x] The guard in `proxy.rs` `attempt` that refuses a rule which alters a
      required field admits this rewrite, and a test pins that it still
      refuses a rule that drops the conversation.
- [x] A test drives both observed refusal texts — Anthropic's
      `input_schema does not support oneOf` and OpenAI's
      `schema must have type 'object'` — through the loopback fixture and
      asserts the retry succeeds.
- [x] `.cartridge/help.md` and `.cartridge/docs/recovery.md` name the new
      adaptation in the same change.

## Verification qualification (2026-09-17)

A fresh verifier re-ran every Verify block and both owner gates against the
implemented tree and reported `just test router` at 82 passed / 0 failed. All
six Acceptance lines above are ticked on that evidence, with one qualification
worth recording rather than hiding.

Line 3 read literally — "every input the original schema validated, the
rewritten one validates" — is proven structurally only. No JSON Schema
validator is executed and no instances are validated anywhere in the proof.
What the three named tests prove is the structural property the spec restated
that line as: the union's branch properties all survive, from both the direct
and the `then` branch, the original `required` is unchanged, no conditional
`required` is promoted, and a schema with nothing to widen is reported
unchanged. Under spec01's restatement the line is fully proven; under the
literal universal-quantifier reading it is not, and proving that reading would
mean running a validator over generated instances. That is a larger piece of
work than this PRD, and if it is wanted it belongs in its own PRD.

The verifier also checked the fixture change the implementer made — an override
whose body starts with `ONCE:` is spent when served — by reading every insert
into `fixture.responses` and confirming none begins with that sentinel, so the
existing behaviour is byte-identical and no existing test is weakened. It was
needed because a permanent override can only ever refuse again, which made
"the same route answers on the retry" unobservable.

## Planning note

2026-09-16. Filed from [[@router/system/vision.md]] as the first of seven
causes, and ordered first because it alone accounts for 11 of the 26
router-side compatibility incidents.

2026-09-17, analysis against `121913e`. Most of this landed before the PRD was
analyzed: `Rules::widen_tools`, `tool_schema_refused`, `widen_schema` and the
`"tools"` entry in `PRESERVING` are all committed, and the same-turn retry in
`proxy.rs` was already generic over `propose`. Four things are not done — the
waiver guard still admits a rule that removes `messages`, because `preserves`
reads only which key changed and not that the rule dropped it; no test drives
either refusal text through the loopback fixture; the widening proof covers
`allOf` only; and neither `.cartridge/help.md` nor `.cartridge/docs/recovery.md`
names the adaptation. Because both doc files carry a sibling PRD's unstaged
hunks, this PRD collects with **no lane**: a lane's fast-forward would abort on
them after the lane commit had already landed. See `specs/spec01.md`.
