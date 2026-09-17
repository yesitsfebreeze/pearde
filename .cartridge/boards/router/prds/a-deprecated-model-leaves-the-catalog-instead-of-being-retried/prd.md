---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/health.rs"
- "src/sync.rs"
- ".cartridge/tests"
commit: "192300fd5003f94ef1492876cfb0fc6f22430185"
---

# a deprecated model leaves the catalog instead of being retried

## Outcome

A provider that says a model is gone is believed. The route stops being ranked,
stops being probed, and stops consuming a recovery budget that cannot succeed.
The operator sees one line saying the model was withdrawn, not a route that
fails forever.

## Evidence

Measured on 2026-09-16: 5 routes, 14 attempts each, all the same answer.

```
gpt-5.1-codex@openai        The model `gpt-5.1-codex` has been deprecated,
gpt-5.1-codex-max@openai    learn more here:
gpt-5.1-codex-mini@openai   https://platform.openai.com/docs/deprecations
gpt-5.2-codex@openai
gpt-5-chat-latest@openai    (2 attempts)
```

`classify` files these under `Compatibility` because the status is 400, and
compatibility incidents are the kind the recovery sweep re-probes. Fourteen
probes against a withdrawn model is fourteen probes that were never going to
pass, spent on a route that will also be ranked ahead of working ones until the
incident is open.

A withdrawal is not a compatibility problem. Nothing about the request is
wrong, and no adaptation exists. It is a catalog fact: the provider's inventory
still lists these ids — `sync` reports 130 models for `openai` — and the
inventory is wrong.

## Acceptance

- [x] `classify` distinguishes a withdrawn model from a request the route could
      not accept, from the provider's own wording.
- [x] A withdrawn route is shelved permanently rather than probed: no recovery
      budget is spent and no retry is scheduled.
- [x] A stale inventory entry cannot resurrect the route. Answered by keeping
      the withdrawal in the health store rather than deleting the catalog row:
      `sync` re-admits the id, and the route stays unavailable because the
      incident outlives the refresh. Deleting it in `sync` was rejected — the
      provider republishes the id on every refresh, so the deletion would have
      to be refought each time, and an un-deprecated model could never return.
- [x] The `status` view names the withdrawal in one line, distinct from a
      compatibility incident, so the operator can tell "gone" from "not yet
      adapted".
- [x] A test asserts that a withdrawn route is not ranked as a candidate for
      `auto`.
- [x] Withdrawal is not inferred from a 404 alone: a 404 from a misconfigured
      base URL must still read as transport or compatibility.

## Planning note

2026-09-16. Filed from [[@router/system/vision.md]], which names this as the
third rule the router must obey: never keep a route it knows is gone.

## Verification (2026-09-17, coordinator cartridge-2e, from verifier-1)

An independent verifier — not the analyst, not the implementer — reran every
Verify block and gate against the lane and reported VERIFIED PASS with every
Acceptance clause in this PRD and in spec01 verified on named observed evidence.
Blocks 1 and 2 exit 0; lane `cargo clippy --all-targets -- -D warnings` exit 0;
`cargo fmt --check` exit 0. With the guard reverted and nothing else changed:
`91 passed; 2 failed`, the two failures being exactly this PRD's own tests with
the predicted `left: 3 / right: 1` and `no override reaches a withdrawal`. The
guard is therefore both necessary and narrow.

Two things established beyond the tests:

1. **The base moved three times while this was verified** — `7b2917a` (suite 90)
   to `3417992` (still 90; the flake fix edited an existing test rather than
   adding one) to `9b5897b` (91, adding
   `a_shelf_of_withdrawn_routes_is_refused_rather_than_waited_for`) to `459d043`
   (README only). The lane did **not** fast-forward onto `9b5897b` or `459d043`:
   `git merge-tree` reports an add/add conflict at the tail of
   `.cartridge/tests/unit/proxy/capabilities.rs`, where `9b5897b` appended one
   test and this lane appended two. `src/health.rs` auto-merges. The coordinator
   rebased and resolved it by keeping both sides' tests, then re-ran everything
   on the rebased commit: 93 passed, clippy 0, fmt 0.
2. **The flake is fixed and independently load-tested.** The implementer saw
   `a_turn_waits_for_the_first_reopening_rather_than_failing_on_a_full_shelf`
   fail twice in 55 whole-suite runs at the old base. On the resolved merge the
   verifier ran 32 more (20 sequential with per-run logs, 12 concurrent four at
   a time): 32 green, zero failures. Across both merges, 0 reds in 64 runs.
   The four-second margin holds.

The `src/proxy.rs` last-resort residue is out of this footprint, untested here,
and declared in spec01 and in the commit body. It is owned by
`@router/the-last-resort-pass-does-not-ask-a-model-the-provider-withdrew`, which
now also carries a stronger observation contributed by the author of `9b5897b`:
with routes marked withdrawn and providers healthy, a request was **answered
200 by a withdrawn model**.
