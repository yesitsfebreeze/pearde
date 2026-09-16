---
complexity: small
footprint:
  - src/proxy.rs
  - src/health.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
---

# spec01 — The guard reads the rule's own change report, not a diff

Base: `router.ctg` dirty tree at `effe3c5f57b634996a810c98bef756c90c630682` and after, which already holds this PRD's implementation.

## Acceptance

- [x] `Rules::apply` reports which top-level keys it changed, rather than the caller inferring it from a before/after comparison.
- [x] A change is admitted when it preserves the request's meaning: a rename whose value arrives under the new name, a tool-schema rewrite, a role relabel, or the removal of a field the caller did not supply.
- [x] A change is refused when it drops a field the caller did supply, and the existing `response_format` test still passes unchanged.
- [x] A test pins the router-added case directly: a route that refuses `reasoning_effort` answers when the router added it, and a route that refuses a caller-supplied `temperature` still refuses.
- [x] The three-key exemption list is gone, replaced by the meaning test, so the rule set and the guard cannot drift apart again.

## Verify and Proof

Block 1 — both behavioral tests, in an isolated target dir, on the tree under verification.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/adapt-waiver-verify}"
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
cargo test --lib an_adaptation_applies_where_a_waiver_is_refused > "$log" 2>&1 || { cat "$log"; exit 1; }
cargo test --lib no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields >> "$log" 2>&1 || { cat "$log"; exit 1; }
cat "$log"
grep -q "an_adaptation_applies_where_a_waiver_is_refused .* ok" "$log"
grep -q "no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields .* ok" "$log"
```

Block 2 — the meaning test is the guard, not a parallel list. The old
three-key exemption must be gone; `preserves` is the only gate, and the
caller-supplied field check `crate::requirements::present(body, &key)` is what
makes a router-added drop admissible.

```sh
test -f src/proxy.rs
test -f src/health.rs
if grep -Fq '"user", "metadata", "stream_options"' src/proxy.rs src/health.rs; then
    echo "the three-key exemption list is back"
    exit 1
fi
grep -q 'rules.preserves(&key)' src/proxy.rs
grep -q 'crate::requirements::present(body, &key)' src/proxy.rs
grep -q 'pub fn preserves' src/health.rs
grep -q 'PRESERVING' src/health.rs
```

## Denied worlds

- Restore the old before/after guard without `preserves` or the
  caller-supplied check: the router-added drop of `reasoning_effort` makes
  `an_adaptation_applies_where_a_waiver_is_refused` fail on the first clause
  (the route is refused before the network, `calls` stays empty).
- Remove `preserves` alone: the rename test at
  `.cartridge/tests/unit/proxy/capabilities.rs:1660-1688` fails because the
  renamed budget arrives under a changed key.
- Re-add the three-key exemption: block 2 of this spec exits 1.
