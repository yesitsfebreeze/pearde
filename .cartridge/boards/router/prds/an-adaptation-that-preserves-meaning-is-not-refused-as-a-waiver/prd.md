---
state: "done"
origin: requested
priority: 99
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/proxy.rs"
- "src/health.rs"
- ".cartridge/tests/unit/proxy/capabilities.rs"
commit: "a4ea6e985361a29a3649b6013e5f30aa5b37bb9d"
---

# an adaptation that preserves meaning is not refused as a waiver

## Outcome

The guard that stops a compatibility rule from silently discarding what the
caller asked for keeps doing exactly that, and stops refusing rules that
discard nothing. A rename, a widened tool schema, a role swap, and the removal
of a field the router itself added all apply. Dropping a field the caller
supplied still refuses the route.

## Evidence

`proxy.rs` `attempt`, as of 2026-09-16:

```rust
let required = outgoing.clone();
rules.apply(&mut outgoing);
for key in required.as_object().into_iter().flatten().map(|(key, _)| key) {
    if !["user", "metadata", "stream_options"].contains(&key.as_str())
        && required[key] != outgoing[key]
    {
        return Err(Failure { status: 400, message:
            "route compatibility rules cannot preserve required request fields".into() });
    }
}
```

Three keys are exempt. `DROPPABLE` in `health.rs` names ten fields a route may
learn to drop:

```
temperature  top_p  logprobs  top_logprobs  user
metadata  max_output_tokens  stream_options  thinking  context_management
```

Seven of the ten are outside the exemption. For those, `propose` learns the
rule, `finish_recovery` persists it after a verified probe, and the next
request that carries the field is refused with a 400 before it reaches the
provider. The adaptation path is complete and inert.

The guard's intent is right and is pinned by the existing test
`no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields`:
a rule that drops the caller's `response_format` must not quietly change the
contract. The defect is that the guard measures *whether a key changed*, which
cannot distinguish a waiver from an adaptation.

Two facts make the distinction available at the point of the check. `attempt`
holds both the caller's normalized `body` and the `outgoing` request it built,
so it can tell a field the caller supplied from one the router added — it adds
`reasoning_effort` itself, from the policy's effort entry, on any `auto`
request to a reasoning-capable route. And a rule knows what kind of change it
made: a rename carries a value to a new name, a schema widening accepts a
superset, a role swap relabels the same message.

## Acceptance

- [x] `Rules::apply` reports which top-level keys it changed, rather than the
      caller inferring it from a before/after comparison.
- [x] A change is admitted when it preserves the request's meaning: a rename
      whose value arrives under the new name, a tool-schema rewrite, a role
      relabel, or the removal of a field the caller did not supply.
- [x] A change is refused when it drops a field the caller did supply, and the
      existing `response_format` test still passes unchanged.
- [x] A test pins the router-added case directly: a route that refuses
      `reasoning_effort` answers when the router added it, and a route that
      refuses a caller-supplied `temperature` still refuses.
- [x] The three-key exemption list is gone, replaced by the meaning test, so
      the rule set and the guard cannot drift apart again.

## Planning note

2026-09-16. Found while planning the other six and filed ahead of them: each of
those PRDs adds a rule kind, and every rule kind lands inert until this one is
done. Recorded in [[@router/system/vision.md]] under "where this stands".
