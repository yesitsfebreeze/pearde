---
complexity: moderate
footprint:
  - src/health.rs
  - .cartridge/tests
  # PROPOSED ADDITION — for the reviewer to judge. See "Why proxy.rs" below.
  # Four lines at proxy.rs:586 plus the correction of the now-false comment at
  # proxy.rs:444-447. Without it the same-turn rule dies with the turn and the
  # drop is re-learned on every later turn, which is the literal wording of the
  # PRD's third Acceptance box.
  - src/proxy.rs
---

# spec01 — the reasoning drop is proven end to end and outlives the turn that learned it

Revision 2. Every line number is at
`192300fd5003f94ef1492876cfb0fc6f22430185`, the base the lane is cut from. The
checkout this was read in carries ~279 uncommitted lines in `src/health.rs` and
`src/proxy.rs` from other sessions; anchor edits on the named symbols, not on
the numbers.

## What is already true

Commit `a4ea6e9` (`Implement
@router/an-adaptation-that-preserves-meaning-is-not-refused-as-a-waiver`, an
ancestor of the base) already landed most of this PRD's mechanism **and part of
its test coverage**. Do not re-add any of it.

The code:

- `src/health.rs:283-287` — `refused_field` strips `Unrecognized request
  argument supplied: ` and trims `'`, `"` and a trailing `.`.
- `src/health.rs:263` — `const REASONING: [&str; 3] = ["thinking", "reasoning",
  "reasoning_effort"]`; `DROPPABLE` at 267 carries all three.
- `src/health.rs:173-183` — in `Rules::apply` (161): dropping any `REASONING`
  key removes all three and `output_config.effort`, reporting `output_config`
  in `changed`.
- `src/health.rs:248` — in `Rules::propose` (229): `body.get(field).is_some() ||
  REASONING.contains(&field)`. The second disjunct is the whole reason a field
  the *router* added is learnable at all.
- `src/proxy.rs:998-1017` — `attempt` injects the effort from
  `catalog.policy.entry(task, route)`, gated on the caller's `model` being
  exactly `auto` or starting with `auto:`, on no caller-supplied reasoning, and
  on `route.caps["reasoning"] == true`. It runs *before* `rules.apply` at 1052.
- `src/proxy.rs:1053` — the waiver guard skips a changed key when
  `crate::requirements::present(body, &key).is_none()`, so a router-injected
  field withdraws cleanly and a caller-supplied one does not.

The tests — and this is the part a previous revision of this spec got wrong.
`.cartridge/tests/unit/proxy/capabilities.rs` at the base sha already contains:

- **`a_refused_thinking_request_loses_every_spelling_of_reasoning`** (line
  1490). A pure `#[test]` that already proves the PRD's **first and second**
  Acceptance boxes, across all three live wordings: the Anthropic `adaptive
  thinking is not supported` case dropping `thinking` *and*
  `output_config.effort` while keeping `output_config.format`; the ollama
  `"granite4:3b" does not support thinking` case against a body carrying
  `reasoning_effort`, asserting the returned `changed` set is exactly
  `{"reasoning_effort"}`; and the OpenAI `Unrecognized request argument
  supplied: reasoning_effort` case. It also asserts `propose` returns `None`
  once there is nothing left to learn.
- **`a_route_that_will_not_reason_and_use_tools_together_drops_the_effort`**
  (line 2200) — the `effort_refused` wording, and that the endpoint move is not
  learned while a cheaper remedy is offered.

So `refused_field` parsing the OpenAI wording, and the four-spelling cascade,
are already gated by an executed named test. **This spec must not duplicate
them.** A previous revision proposed
`both_reasoning_refusals_propose_one_drop_that_clears_every_spelling` in
`availability.rs`; that test is a near-copy of line 1490 and has been deleted
from this spec.

## What is actually missing

**1. Nothing drives a turn.** Every existing test above is a pure `Rules`
unit test on `propose`/`apply`. None of them exercises the path the PRD's
evidence is about: the router *injecting* an effort, the provider refusing it,
and the same-turn retry answering on that same route. The injection at
`src/proxy.rs:998-1017`, the ordering against `rules.apply` at 1052, and the
waiver guard at 1053 are all untested for the reasoning case. That is the PRD's
fourth Acceptance box and it is unmet.

**2. A rule learned by the same-turn path is never recorded.**
`src/proxy.rs:447` declares `let mut learned: BTreeMap<String, Rules>`, 625
writes the proposed rule into it, 531 reads it back. It is a turn local. The
successful same-turn retry (619-627) `continue`s *past* `proxy.health.fail(...)`,
so no incident is opened — and the only writer of `data.rules` is
`Health::finish_recovery` (`src/health.rs:971`), which returns early without an
open incident and runs only from the recovery sweep.

So a route that recovers in the same turn starts the next turn from
`Rules::default()`, injects the effort again, eats the same 400 again, and
learns the same rule again. One wasted upstream round-trip per turn, for the
life of the route. That is the literal wording of the PRD's third Acceptance
box, "rather than re-learning the drop each turn".

For the three routes the PRD measured this is masked: they already carry open
compatibility incidents, so the recovery sweep does persist their rule. It is
the *fresh* route — the one that recovers in the same turn and never gets
shelved — that pays forever.

## Why proxy.rs

The recording must happen where the turn has committed to this route:
`src/proxy.rs:586`, the `decision.selected(selected);` statement. It is the
first statement after the non-streaming failure check at 573-583, and the only
point where `learned`, `route.id` and `proxy.health` are all in scope.

It is **not** "the first statement after the response is known good" — that is
false for a stream. Line 559 spawns `stream_response` and the stream can still
die later, at which point `stream_response` calls `proxy.health.fail` around
1352. Line 586 is nonetheless the right place, for a different reason: the rule
records a claim about the *request shape*, and the upstream accepting the
request and returning headers is exactly the evidence for that claim. A stream
that dies mid-body is not a shape refusal and is classified elsewhere.

There is no seam inside `health.rs`. `Health::success` is `(&self, route: &str)`
at `src/health.rs:797` and takes no rules, `Rules::propose` is `&self` on
`Rules` with no handle on `Health`, and a `record_rules` with no caller is dead
code that `just check` would reject.

If the reviewer refuses the widening, say so rather than working around it: the
third Acceptance box then cannot be honestly ticked for a route without an
incident, and that belongs in the PRD body, not behind a green check.

## The second writer of `data.rules`, and the comment it falsifies

This change gives `data.rules` a second writer, and the comment being edited
already says the opposite of what will be true — `src/proxy.rs:444-447`:

> What a route taught this turn about the shape it accepts. Held here rather
> than in the health store because no probe has verified it yet, and per route
> because one route's dialect is not another's.

Correct it in the same edit rather than leaving it false. The correction is
also the justification for the second writer: a same-turn retry that answered
is *stronger* evidence than the structural probe `finish_recovery` records a
rule from. The probe sends a synthetic body with no conversation; the retry sent
the caller's actual request and the provider answered it.

```rust
// What a route taught this turn about the shape it accepts, per route because
// one route's dialect is not another's. A rule stays here until the retry it
// proposed actually answers; at that point it is written through to the health
// store, because a turn the provider answered is stronger evidence for a shape
// than the conversationless probe `finish_recovery` learns from.
```

Ceiling, stated rather than engineered around: nothing invalidates a recorded
rule if the route later stops needing it. That is already true of every rule
`finish_recovery` writes, so this adds no new class of staleness, and inventing
an expiry here would be a second policy on rule lifetime with no measured
demand. If rule staleness is worth solving it is one PRD for both writers.

## Implementation

1. `src/health.rs`, next to `pub async fn rules` (line 865):

   ```rust
   /// Record the shape a route was observed to accept. The recovery sweep
   /// learns a rule from a route that is already shelved; this is the other
   /// way a rule is learned — the same-turn retry that answered, whose rule
   /// would otherwise die with the turn and be paid for again on the next one.
   pub async fn record_rules(&self, route: &str, rules: Rules) {
       let mut data = self.data.write().await;
       if data.rules.get(route) == Some(&rules) {
           return;
       }
       data.rules.insert(route.into(), rules);
       drop(data);
       self.persist().await;
   }
   ```

   The equality guard makes the call idempotent, so a long run of turns writes
   the health file once rather than once per turn.

2. `src/proxy.rs`, immediately before `decision.selected(selected);` at 586,
   plus the comment correction above:

   ```rust
   if let Some(rules) = learned.get(&id) {
       proxy.health.record_rules(&id, rules.clone()).await;
   }
   ```

3. Tests, all in `.cartridge/tests/unit/proxy/capabilities.rs`, which is already
   wired at `src/proxy.rs:1584`. No `#[path]` module is added and `health.rs`
   needs no test-only edit.

### 3a. Making the injection fire — the recipe already exists, reuse it

The injection does not fire in the default fixture:
`Catalog::new` sets `policy: crate::frontier::Policy::default()`
(`src/catalog.rs:438`) and `Policy` is an empty `frontiers` map
(`src/frontier.rs:21-24`), so `board()` and `entry()` return `None`; and the
fixture's hops declare no `reasoning` capability.

**Do not invent a fixture extension for this.**
`a_policy_reload_during_fallback_does_not_change_the_attributed_snapshot`
(`.cartridge/tests/unit/proxy/capabilities.rs:510-545`) already does exactly
what is needed, in this file, at the base sha. Lift its opening into a small
helper and call it from each test below:

```rust
// Clone the catalog, make every route reasoning-capable, and rank a policy
// entry for the task this body detects — the three conditions the effort
// injection at proxy.rs:998-1017 requires before it adds anything.
async fn with_effort(fixture: &Fixture, body: &Value, effort: &str) {
    let task = crate::frontier::task(body["model"].as_str().unwrap(), body).to_owned();
    let mut cat = (**fixture.proxy.catalog.read().await).clone();
    for route in &mut cat.routes {
        route.caps["reasoning"] = json!(true);
    }
    cat.policy.frontiers.insert(
        task,
        vec![crate::frontier::Entry {
            model: "fixture".into(),
            score: 1.0,
            benchmark: "fixture".into(),
            source: "fixture".into(),
            date: "2026-09-19".into(),
            effort: Some(effort.into()),
        }],
    );
    *fixture.proxy.catalog.write().await = Arc::new(cat);
}
```

Three details that are load-bearing and were each got wrong once already:

- The task key must be **computed**, `crate::frontier::task(...)`, not
  hardcoded. `task` returns on the `auto:` prefix first, then
  `cartridge_task`, then the modality — and `request()` carries an `image_url`,
  so a plain `auto` body detects `vision`, not `text` or `agent`
  (`src/frontier.rs:200-224`). Computing it is correct whatever `request()`
  later becomes.
- `Entry.model` is `"fixture"`, the route **alias**. `Board::entry` looks a
  route up by `rank(&[&route.alias, &route.id], &route.model)`
  (`src/frontier.rs:109`) and `Board::new` indexes entries under `names(e.model)`
  (line 75), so the alias matches through the `exact` map. Every field but
  `effort` is non-`Option` (`src/frontier.rs:27-36`), so all seven are required.
- The selector is plain **`body["model"] = json!("auto")`**, with no pin and no
  `cartridge_strict`. Both alternatives fail: `auto@last` does **not** pass the
  injection gate, because `src/proxy.rs:998-1001` tests the raw string
  (`m == "auto" || m.starts_with("auto:")`) and `"auto@last"` is neither; and
  `cartridge_strict` cannot be combined with any `auto` form, because strict
  keeps only `preferred(r, canonical, pin)` (`src/catalog.rs:497`, `650-652`),
  which compares `route.alias == canonical`, and for a base of `auto` the
  canonical is `"auto"`, which no alias matches — the turn ends with zero calls.

With plain `auto` the natural call order is settled by
`actual_failover_skips_incompatible_routes_and_preserves_required_fields`
(line 169): `first` answers 503, `incompatible` is skipped before the network
because `request()` carries tools it does not declare, and `last` answers. So a
`ONCE:` refusal armed on `last` gives a recorded provider sequence of
**`["first", "last", "last"]`** — `calls[1]` is the injected request and
`calls[2]` is the retry. Do not copy the `["last","last"]` assertion from
`a_refused_tool_schema_is_rewritten_and_the_same_route_answers` (line 1823);
that test pins `fixture@last` with `cartridge_strict`, which is unavailable
here for the reason above. Copy its *structure* — `ONCE:` override, drive the
turn, assert 200, assert the provider sequence, inspect the retried body — not
its selector.

**Anti-vacuity rule, mandatory:** assert `calls[1].1["reasoning_effort"]` was
actually set before asserting anything about `calls[2].1`. Without it every
test below passes the moment the injection stops firing, which is the exact
failure they exist to catch.

### 3b. The tests

- `a_route_that_refuses_the_injected_effort_answers_without_it` — `ONCE:` 400 on
  `last` carrying `{"error":{"message":"Unrecognized request argument supplied:
  reasoning_effort"}}`. Assert 200; provider sequence `["first","last","last"]`;
  `calls[1].1["reasoning_effort"]` set; `calls[2].1` carries none of `thinking`,
  `reasoning`, `reasoning_effort`, and no `effort` under `output_config`.
- `an_ollama_thinking_refusal_drops_the_effort_the_router_added` — the same with
  `{"error":{"message":"\"granite4:3b\" does not support thinking"}}`. Not a
  duplicate of the pure test at line 1490: that one hands `apply` a body it
  built itself, while this one proves the router's *own injected* field is the
  one that goes, through the real `attempt` path and past the waiver guard.
- `a_learned_reasoning_drop_outlives_the_turn_that_learned_it` — run the first
  turn, then assert
  `fixture.proxy.health.data.read().await.rules.get("fixture@last")` names a
  reasoning spelling in its `drop`. Then drive a second turn through the same
  `Proxy` with no `ONCE:` armed, and assert that turn's calls to `last` number
  exactly one and that its body carries no reasoning spelling. This is the box
  that fails today.
- `a_reasoning_control_the_caller_asked_for_is_still_a_waiver` — the same
  refusal, but the caller's body carries `reasoning_effort` itself (which also
  closes the injection gate, so the anti-vacuity rule does not apply here).
  Assert the route is refused with `crate::health::WAIVER_REFUSED` rather than
  silently answered without what the caller asked for, and that the refusal
  happens before a second call to that route.
  `a_rule_that_drops_the_conversation_is_still_refused` (line 1878) is the
  pattern for asserting a pre-network refusal; it covers `messages`, not
  reasoning.

## Decided, not open

A reasoning control the **caller** supplied stays a waiver: the route is
refused, not silently answered without what was asked for. Settled; this spec
does not reopen it. Three warrants: the vision's first law, that a rewrite which
cannot preserve meaning is a refusal rather than a silent downgrade; the
distinction is the collected outcome of `a4ea6e9`, so inverting it inside a test
file would undo a landed PRD; and `requirements::present` at
`src/requirements.rs:22` already draws the line on the caller's body exactly
where this PRD's evidence puts it. The PRD's Outcome carries the matching scope
clause.

## Verify and Proof

The engine gives each block `sh -eu -c`, 120 s, an empty environment, and two
passes (the lane, then `repo`). The PRD's `repo` is `router.ctg`, so every path
is relative to that crate root. All blocks spell `CARGO_TARGET_DIR` as
`target/reasoning-verify` identically so they cannot diverge. Nothing writes
inside the footprint.

**The claim is that a cold run finishes well inside the 120 s block, and it is
measured.** A previous revision claimed the opposite without measuring and moved
the mutant into an Acceptance box; that claim was wrong and is withdrawn.

Plan against the slower of the two independent measurements, not the faster.
A second machine, same design — `$TMPDIR` tree, fresh `CARGO_TARGET_DIR`,
`cargo test -p router --lib` cold — recorded **25.4 s** and **26.3 s**, both 93
passed. This machine recorded 17 s (ambient `CARTRIDGE_YOLO=1`) and 18 s (`env
-u CARTRIDGE_YOLO`), same 93 passed, with a 4 s warm rerun. The roughly 50
percent gap is unexplained and is not worth a round to chase: both leave more
than 90 s of headroom, and the margin holds even if a third machine is slower
again than the slowest here. If a cold run ever approaches the block limit, that
is the signal to filter — not the faster number.

The suite is left unfiltered deliberately: the test phase itself is about four
seconds on both machines, and running it whole catches regressions a filter
would hide.

```sh
export CARGO_TARGET_DIR="$PWD/target/reasoning-verify"
cargo build -p router --lib
```

```test
run: env CARGO_TARGET_DIR=target/reasoning-verify cargo test -p router --lib
pass: a_route_that_refuses_the_injected_effort_answers_without_it
pass: an_ollama_thinking_refusal_drops_the_effort_the_router_added
pass: a_learned_reasoning_drop_outlives_the_turn_that_learned_it
pass: a_reasoning_control_the_caller_asked_for_is_still_a_waiver
pass: a_refused_thinking_request_loses_every_spelling_of_reasoning
```

The last name is the pre-existing test at line 1490. It is pinned rather than
rewritten, so that the collapse of the four spellings into one feature stays
gated even though this PRD adds nothing to it.

The mutant. The `test` block pins names; this proves the bodies are
load-bearing. It collapses every reasoning spelling onto one name in a throwaway
copy — the single change that makes "three wire names, one feature" untrue — and
requires the suite to notice **in this PRD's own end-to-end test**. That last
condition matters: the pre-existing test at line 1490 already dies under this
mutant, so a block that only required "the suite failed" would pass against an
implementation that added nothing at all.

The copy is made from `.`, so it follows the lane in pass 1 and the live tree in
pass 2; nothing `cd`s to an absolute checkout and nothing is written inside the
repository. Mechanics exercised end to end before this spec was written: the
`tar` copy, the `sed` anchor, the `cmp` no-op detection, and a mutant build and
suite run all behaved as written.

The final guard was tested adversarially, over three review rounds, because a
guard only ever seen accepting the good case is not tested. The property it must
assert is **"this specific test failed"**, and three earlier versions each
asserted something merely adjacent to it, each beaten by an example nobody had
thought of yet: "the suite failed" (beaten by the pre-existing unit test at line
1490, which dies under this mutant on its own), "the name was printed" (beaten
by the `... ok` line), and "a test whose name ends in this name failed" (beaten
by `some_other_prefix_<name>`). If you change this line, re-run the table below
and add the case that motivated your change.

Measured in a standalone crate, `cargo test --lib`, current pattern:

| # | case | required | result |
| --- | --- | --- | --- |
| 1 | target test **passes**, unrelated test fails | reject | reject |
| 2 | target test **fails** among six, concurrent runner | accept | accept |
| 3 | target absent, only an unrelated test fails | reject | reject |
| 4 | target absent, failing test named `other_prefix_<name>` | reject | reject |
| 5 | target absent, failing test named `<name>_and_more` | reject | reject |
| 6 | target **passes** while `other_prefix_<name>` fails | reject | reject |
| 7 | target absent, identical name in a different module fails | — | accept |

Cases 4 and 6 are what the `([a-z_0-9]+::)*` boundary is for: an open class
there accepts both. Case 5 is closed by the ` \.\.\. FAILED$` tail. Case 2
confirms libtest still emits `test <name> ... FAILED` whole on one line under
the concurrent runner, so the `$` anchor is not defeated by interleaving. Of the
four lines carrying the name in a failing log, only the status line satisfies
`^test `; the panic dump header, the `thread '<name>' panicked` line and the
indented `failures:` entry all fail it.

Case 7 is a known residual, deliberately left: the guard identifies the test by
name rather than by full module path, which is the same rule the engine's own
`test` block uses ("a name matches exactly or as the last `::` segment").
Pinning `proxy::capability_tests::` here would make the gate reject a correct
implementation whose module path shifted. It is not exploitable in combination
with the `test` block above, which requires this same name to be reported
**passed** in the unmutated run — a permanently failing twin elsewhere fails
that gate instead.

```sh
mutant="${TMPDIR:-/tmp}/reasoning-mutant-$$"
mkdir -p "$mutant"
tar -cf - --exclude target --exclude .git . | tar -xf - -C "$mutant"
cp "$mutant/src/health.rs" "$mutant/health.rs.before"
sed -e 's/^const REASONING: \[&str; 3\] = .*$/const REASONING: [\&str; 3] = ["thinking", "thinking", "thinking"];/' \
    "$mutant/health.rs.before" > "$mutant/src/health.rs"
# A silent no-op edit would let the mutant "pass" by never having been applied.
if cmp -s "$mutant/health.rs.before" "$mutant/src/health.rs"; then
  echo "mutant not applied: the reasoning name list was not where this block looks for it"
  exit 1
fi
cd "$mutant"
if env CARGO_TARGET_DIR="$mutant/target-mutant" cargo test -p router --lib > "$mutant/out.log" 2>&1; then
  echo "every reasoning spelling was collapsed onto one name and the suite still passed:"
  echo "nothing here distinguishes the spellings from each other"
  exit 1
fi
# The pre-existing unit test dies under this mutant on its own, so "the suite
# failed" proves nothing about this PRD. Assert that THIS test died: libtest's
# status line for it, with a module path that must end in `::` so no other
# test's name can absorb this one as a suffix. A bare substring match also hits
# the `... ok` line; an open character class before the name lets
# `other_prefix_<name>` satisfy it.
if grep -Eq '^test ([a-z_0-9]+::)*a_route_that_refuses_the_injected_effort_answers_without_it \.\.\. FAILED$' "$mutant/out.log"; then
  :
else
  echo "the suite failed under the mutant, but the turn-driving test did not:"
  echo "the reasoning path is still proven only by unit tests on Rules"
  exit 1
fi
```

## Acceptance

- [ ] A route that refuses the router-injected effort answers inside the same
      turn, on the route that just refused, and the test asserts the injected
      request carried `reasoning_effort` before asserting the retry does not.
- [ ] The retried request carries none of the four spellings — `thinking`,
      `reasoning`, `reasoning_effort`, `output_config.effort` — proven through
      the real `attempt` path rather than by handing `Rules::apply` a body.
- [ ] Both live wordings reach that outcome end to end, and the ollama case is
      proven with a request that carried `reasoning_effort` and a refusal that
      named `thinking`.
- [ ] The rule learned by the same-turn retry is present in `health.data.rules`
      after the turn, and a second turn to the same route costs one upstream
      call carrying no reasoning spelling. A route that answers in the same turn
      opens no incident, so the recovery sweep is not the answer here.
- [ ] A reasoning control the caller supplied is still refused as a waiver, so
      the router-added field and the caller's field stay distinguishable.
- [ ] The comment at `src/proxy.rs:444-447` no longer states that the learned
      rule is held out of the health store, because it no longer is.
- [ ] `a_refused_thinking_request_loses_every_spelling_of_reasoning` and the
      rest of the pre-existing reasoning coverage are left intact, not rewritten
      or duplicated.
- [ ] The mutant block passes: collapsing the reasoning spellings onto one name
      makes the suite fail, and fail in this PRD's turn-driving test rather than
      only in the unit test that already covered it.
