---
state: "open"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/health.rs"
- ".cartridge/tests"
---

# a route that refuses reasoning keeps answering without it

## Outcome

A route that does not support a reasoning control answers the turn without it
rather than refusing the turn, where the control is one the router itself added
from policy; a control the caller supplied is a waiver and still refuses the
route. Every spelling of the control — `thinking`, `reasoning`,
`reasoning_effort`, `output_config.effort` — is dropped together, because they
are one request feature wearing three wire names.

## Evidence

Measured on 2026-09-16: 3 routes, two distinct failures that are the same
thing.

```
granite-router-latest@ollama   4 attempts   "granite-router:latest" does not
granite4-3b@ollama             4 attempts   support thinking
gpt-4.1-nano@openai            3 attempts   Unrecognized request argument
                                            supplied: reasoning_effort
```

The thinking half is already handled: `thinking_refused` matches the ollama
wording, `thinking` is in `DROPPABLE`, and `strip_refused` correctly clears
`reasoning` and `output_config.effort` alongside it. Those two routes still
carry an open incident, so the same-turn path is either not reached or the
rule is not persisted — the first thing this PRD establishes is which.

The effort half is unhandled outright. `reasoning_effort` is not in
`DROPPABLE`, and OpenAI's `Unrecognized request argument supplied: X` wording
is not one of the two forms `refused_field` parses. The value is also not the
caller's: `proxy.rs` `attempt` sets `reasoning_effort` itself, from the
policy's effort entry, on any `auto` request to a route whose caps claim
reasoning. So the router adds a parameter the route rejects and then cannot
learn to stop.

## Acceptance

- [ ] `refused_field` parses `Unrecognized request argument supplied: X`
      alongside the two forms it already parses.
- [ ] `reasoning_effort` and `reasoning` are droppable, and dropping any one of
      the reasoning spellings drops all of them, as `thinking` already does.
- [ ] The router stops adding an effort the route refuses, rather than
      re-learning the drop each turn. Answered by the recorded rule rather than
      by editing the route's caps: the rule removes the field on every later
      turn, and a second place that also decides whether a route reasons is
      exactly the drift the vision's fifth law forbids.
- [ ] A test reproduces the live state: the two ollama routes and the
      `gpt-4.1-nano` route each answer on retry after one refusal.
- [ ] The existing thinking path is proven end to end rather than by
      inspection — the open incident on both granite routes is explained.
      Answered: the same-turn strip worked and the durable rule did not. Once
      recovery persisted `drop: {thinking}`, the guard in `attempt` saw
      `thinking` change and refused the route with a 400 before the request
      left the process, so every later turn failed where the first had
      recovered. Fixed by
      [[an-adaptation-that-preserves-meaning-is-not-refused-as-a-waiver]].

## Planning note

2026-09-16. Filed from [[@router/system/vision.md]]. The effort case is the one
that indicts the router most directly: it rejects a parameter the router itself
added.

## State at handover, 2026-09-19

Recorded by coordinator cartridge-eb as its session ended. This row is in
`analyzing` under `coordinator-5d5e-3`; if that claim is still held when you
read this, it is stale and yours to reconcile.

**Rounds used: 3 of 5. Two remain.** Round 1 scored 72 (FAIL), round 2 scored 85
(FAIL), round 3 scored 89 (FAIL). Each round's blocking finding was fixed and
the fix independently attacked by the next fresh reviewer. A fourth revision is
on disk in `specs/spec01.md` and **has not been scored**: read `review.md`
round 3 first, then the revision, before trusting the spec.

All three rounds turned on one thing — the mutant guard — and the sequence is
worth reading before touching that line, because three plausible fixes were
each beaten by an example nobody had thought of. The property is "this specific
test failed". The beaten approximations were "the suite failed" (beaten by the
pre-existing test at `capabilities.rs:1490`, which dies under the mutant on its
own), "the name was printed" (beaten by libtest printing the name on the
`... ok` line as readily as the `... FAILED` line), and "a test ending in this
name failed" (beaten by a failing test named `other_prefix_<name>` while the
target was absent entirely). The current guard requires each module segment to
end in `::` so nothing can absorb the name as a suffix, and the spec carries a
seven-case table beside it with the instruction that anyone changing the line
re-runs the table and adds the case that motivated the change.

Three things the next coordinator needs and cannot infer:

The widening of the footprint to `src/proxy.rs` is **proposed, not granted**.
Round 1 verified it as justified — `learned` at `proxy.rs:447` is a turn local,
`data.rules` has exactly one writer in `finish_recovery` at `health.rs:971`
reachable only from the recovery sweep over open incidents, and no seam exists
in `health.rs` — but the PRD frontmatter still declares only `src/health.rs`
and `.cartridge/tests`. If the widening is refused, Acceptance box 3 cannot be
honestly ticked for a route that recovers in the same turn and never opens an
incident, and that fact belongs in this body rather than behind a green check.

One known gate residual, left open deliberately and documented in the spec: an
identically named failing test in a *different module* is accepted by the
guard. Pinning the full module path would reject a correct implementation whose
module path shifted, and it is not exploitable alongside the `test` block, which
requires that same name reported passed in the unmutated run.

Every line number in the spec is at base `192300f` and was verified unchanged in
round 3. The round 1 and 2 dirty-checkout drift has since landed as unrelated
commit `ca11f6b`, so re-check the anchors if the base has moved again.
