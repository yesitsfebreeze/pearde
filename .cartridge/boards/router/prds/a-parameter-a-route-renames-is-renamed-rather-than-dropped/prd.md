---
state: "done"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/health.rs"
- ".cartridge/tests/unit/proxy/capabilities.rs"
commit: "05bef5a54aeebd8d7aaf04881c083dccf9d22391"
---

# a parameter a route renames is renamed rather than dropped

## Outcome

A route that refuses a parameter under one name but accepts it under another
receives it under the name it accepts. The output limit in particular survives
the translation, so a turn keeps its budget instead of losing it.

## Evidence

Measured on 2026-09-16: 5 routes shelved, each having spent 4 attempts to learn
the same sentence.

```
gpt-5.1@openai            Unsupported parameter: 'max_tokens' is not supported
gpt-5.2@openai            with this model. Use 'max_completion_tokens' instead.
gpt-5.4@openai
gpt-5.4-mini@openai
responses-gpt-5.5@openai
```

`health.rs` `refused_field` already parses exactly this message — it strips the
`Unsupported parameter: ` prefix and takes the field name. It then looks the
name up in `DROPPABLE`, which does not contain `max_tokens` and must not: the
output limit is the caller's budget, and dropping it changes the turn. So the
parse succeeds, the lookup fails, `propose` returns nothing, and the route
degrades with "unsupported compatibility diagnosis".

The provider's message names the replacement. The router reads the half of the
sentence that says what is wrong and discards the half that says what to do.

## Acceptance

- [x] `Rules` carries a per-route rename map, learned through `propose` from
      the `Use 'X' instead` clause of the provider's message.
- [x] `max_tokens` is renamed, never dropped; a test pins that it stays out of
      `DROPPABLE`.
- [x] The rename applies in the same turn, so the first request on a fresh
      route answers rather than failing while recovery learns.
- [x] The guard in `proxy.rs` `attempt` admits a rename that carries a required
      field's value to its new name, and still refuses a rule that loses the
      value.
- [x] A test drives the observed message through the loopback fixture and
      asserts the retried request carries `max_completion_tokens` with the
      original value.
- [x] A rename is only learned when the message names both sides; a message
      that names only the refused parameter still falls to the drop rule or to
      a degraded incident.

## Planning note

2026-09-16. Filed from [[@router/system/vision.md]]. Second of seven causes.

## Verification qualification (2026-09-17)

A fresh verifier re-ran both Verify blocks and both owner gates — `just test
router` at 84 passed / 0 failed, up from 82 — and confirmed byte fidelity: the
appended tests diff clean against the spec's embedded source, `+69` lines, no
deletions, no change to `src/health.rs`.

It did not take the tests' value on trust. It mutated `src/health.rs` five
times and restored it exactly after each, ending at md5
`43ef55079d62d207380da942756b2efd` with an empty diff: deleting the `use `
conjunct fails at `capabilities.rs:2193`; adding `max_tokens` to `DROPPABLE`
fails at `:2164`; a rename that also records a drop fails at `:2160`; removing
`messages` and `input` from the rename blocklist fails at `:2202`; and the
second test alone under the `DROPPABLE` mutation fails at `:2185`. The last two
were the verifier's own additions, gating the remaining conjuncts of line 6.

What is proved and what is not. Lines 1, 2 and 6 are mutation-tested on every
assertion. Lines 3, 4 and 5 are proved to be *gated* by the tests, by
inspection plus an observed pass, but were not mutation-tested: every
falsifying mutation for them lives in `src/proxy.rs`, which this plan freezes
and the verifier was forbidden to edit. Line 6's first conjunct — that
`temperature` still learns a drop — rests on inspection alone. Both gaps are
unchanged from the base commit and this PRD adds no code those lines depend on.

Record gap: the implementer reported writing
`.state/loop/a-parameter-a-route-renames-is-renamed-rather-than-dropped/implementer-1.md`
and that file does not exist. Its commands and exit codes survive only in the
coordinator's transcript. Nothing rests on them — every claim it made was
independently reproduced by the verifier against the tree.
