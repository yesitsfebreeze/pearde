---
complexity: small
footprint:
  - src/health.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
  - .cartridge/help.md
  - .cartridge/docs/recovery.md
---

# spec01 — The widened tool schema is proven end to end, and a dropped conversation is still a waiver

Base: `router.ctg` at `121913eddef9a2c5537e21ee5405cffe1d86291c`
(`Land the requirements helper the collected proxy code already calls`).

**Most of this outcome already landed in `a4ea6e9`.** `Rules::widen_tools`
(`src/health.rs:142-145`), `tool_schema_refused` (`src/health.rs:504-512`),
`propose` learning it (`src/health.rs:249-251`), `widen_tools` /
`widen_schema` (`src/health.rs:424-489`), the generic same-turn retry
(`src/proxy.rs:580-587`) and the `preserves` guard with `"tools"` in
`PRESERVING` (`src/health.rs:152-155`, `219-223`, `src/proxy.rs:846-856`) are
all committed and unchanged by `fae0290` and `121913e`. The spec still states
every Acceptance line and still proves each one, because a claim nobody can
fail is not a claim. What is missing is small and named below.

Outstanding work, in order:

1. **The guard admits a rule that drops the conversation.** `PRESERVING`
   contains `messages`, `input` and `tools`, and `preserves` returns true for
   any of them regardless of *how* they changed. A rule with
   `drop: {"messages"}` therefore deletes the conversation and passes the
   waiver guard at `src/proxy.rs:846-856`. `propose` never learns that rule
   today — `refused_field` is gated on `DROPPABLE`, which excludes it — so
   nothing observed is broken, but Acceptance line 4 asks for a test that pins
   the refusal, and that test fails against `121913e`. Make `preserves` deny a
   key the rule removed: a removal is never an adaptation, whichever key it
   names. One line, in `src/health.rs`. It does not disturb the reasoning-key
   or router-added-field paths, neither of which is in `PRESERVING`.
2. **No loopback proof.** The only tool-schema test is a pure `#[test]` over
   `Rules` (`.cartridge/tests/unit/proxy/capabilities.rs:1609-1649`). Nothing
   drives either observed refusal text through the fixture and asserts the
   route answers on the retry. Acceptance line 5 asks for exactly that; model
   it on `a_renamed_parameter_moves_its_value_instead_of_losing_it`
   (`.cartridge/tests/unit/proxy/capabilities.rs:1654-1688`), which already
   proves the two-call retry shape against the same fixture.
3. **The widening proof covers one shape, and one test cannot gate three.**
   The committed `a_union_tool_schema_is_widened_into_the_object_every_provider_takes`
   (`.cartridge/tests/unit/proxy/capabilities.rs:1609-1649`) widens an object
   carrying a top-level `allOf`, and nothing else. Looping inside one test
   would leave Acceptance line 3 ungated: block 1 asserts only that a named
   test ran and passed, so a test that quietly dropped two of the three
   keywords would still satisfy it. **Split it into three tests, one per
   keyword**, sharing one helper that builds the schema and makes the
   assertions:

   - `an_all_of_tool_schema_is_widened_into_the_object_every_provider_takes`
   - `a_one_of_tool_schema_is_widened_into_the_object_every_provider_takes`
   - `an_any_of_tool_schema_is_widened_into_the_object_every_provider_takes`

   Each asserts, for its keyword, that the widened schema has `type: "object"`,
   that the keyword and `if`/`then`/`else` are gone, that every property any
   branch declared survives — whether it arrived directly on the branch or
   under `then` — that the original `required` is unchanged and no branch's
   conditional `required` was promoted, and that a schema with nothing to
   widen is reported as unchanged. Block 1 names all three, so deleting or
   renaming any one fails the block. The old combined test name goes away.
4. **The docs do not name the adaptation.** Neither `.cartridge/help.md` nor
   `.cartridge/docs/recovery.md` mentions a tool schema at `121913e`. The live
   checkout carries unstaged `recovery.md` rows from a sibling PRD that
   already describe the widening; this change must add what those rows do not
   say, so the proof cannot be credited to someone else's work: the cause
   label `tool-schema` that `router availability` prints for such an incident,
   and the fact that the rewrite is **top level** only.

## Landing: this PRD collects with no lane

This is a precondition, not a preference. `.cartridge/help.md` (+3/−3) and
`.cartridge/docs/recovery.md` (+69/−2) are both dirty in
`/Users/feb/dev/cartridge/router.ctg` with a sibling PRD's unstaged work, and
both are in this spec's footprint because Acceptance line 6 requires editing
them. `collect` refuses only *staged* changes (`prd.ctg/src/lifecycle.ts:104`),
so that dirt survives to the fast-forward at `prd.ctg/src/lifecycle.ts:166`,
where `git merge --ff-only` aborts with "Your local changes to the following
files would be overwritten by merge" — after the lane has already committed
the work (`prd.ctg/src/lifecycle.ts:157-158`), leaving the PRD stuck claimed.

So: **the implementer works directly in `/Users/feb/dev/cartridge/router.ctg`
and the coordinator collects from `specced`, with no lane.** The engine
permits it, and it is how `9f995d9` and `a4ea6e9` collected earlier today.
With no lane there is no worktree, no fast-forward and no abort-after-commit;
the Verify blocks run once, in `repo` (`prd.ctg/src/lifecycle.ts:125`), and
the status sweep runs against the live checkout.

The consequence, stated exactly. `collect`'s status sweep
(`prd.ctg/src/lifecycle.ts:143-155`) runs over `feet(prd)`, which unions the
PRD footprint with every spec footprint (`prd.ctg/src/planner.ts:5-9`). The
PRD's own three entries — `src/health.rs`, `src/protocol.rs` and
`.cartridge/tests/unit/proxy/capabilities.rs` — are clean in the live checkout
and sweep nothing. The whole remaining sweep is the two dirty files this spec
adds: `.cartridge/help.md` and `.cartridge/docs/recovery.md`, each carrying a
sibling PRD's pending hunks, which will therefore land inside this PRD's
`Implement @router/…` commit. Do not stash, revert or separately commit them
to avoid this — that is another session's work and moving it is worse than
carrying it.

The PRD footprint no longer names the bare directory `.cartridge/tests`, so
**every new test in this change goes into
`.cartridge/tests/unit/proxy/capabilities.rs`.** A new file anywhere else
under `.cartridge/tests` would be stranded outside the footprint, uncommitted
and unbuildable from a clean checkout — the failure `fae0290` repaired for
`availability.rs`. If a new file is genuinely wanted, name it in this spec's
footprint first.

`src/proxy.rs` is **deliberately frozen** by this plan. It carries Acceptance
line 4's guard, but the guard already landed in `a4ea6e9` and the remaining
fix is confined to `Rules::preserves` in `src/health.rs`. It is therefore in
neither footprint, and block 2 only reads it. If an implementer finds a
`proxy.rs` edit is genuinely required, collection will abort at
`prd.ctg/src/lifecycle.ts:134` with "committed path is outside the PRD
footprint" — stop and ask the coordinator to widen the footprint rather than
working around it.

Not in scope, and deliberately: `widen_schema` does not wrap a top-level
`enum` or a non-object top-level `type` into an object. No observed refusal
needs it — `cartridge_docs` is an object with an `allOf` — and no Acceptance
line claims it. The Outcome shape says such a schema is left alone and the
route stays refused, which is what the code does.

`src/protocol.rs` needs no change: `rules.apply` runs on `outgoing` in
`src/proxy.rs` `attempt`, after the wire conversion, so the rewrite reaches
every dialect without `to_chat` knowing about it.

## Acceptance

- [x] `Rules` carries a per-route tool-schema normalization, learned from the
      provider's own refusal text through `propose`, exactly as `drop` and
      `developer_role` are.
- [x] `strip_refused`'s same-turn counterpart applies the rewrite and retries
      the same route, so the caller waits once rather than losing the turn.
- [x] Three tests —
      `an_all_of_tool_schema_is_widened_into_the_object_every_provider_takes`,
      `a_one_of_tool_schema_is_widened_into_the_object_every_provider_takes`
      and `an_any_of_tool_schema_is_widened_into_the_object_every_provider_takes`
      — prove the rewrite meaning-preserving, one per union keyword: every
      property any branch declared survives into the widened object, and no
      branch's conditional `required` is promoted. Every input the original
      schema validated, the rewritten one validates. Each is named in block 1,
      so a missing keyword fails the block.
- [x] The guard in `src/proxy.rs` `attempt` that refuses a rule which alters a
      required field admits this rewrite, and a test named
      `a_rule_that_drops_the_conversation_is_still_refused` pins that a rule
      removing `messages` is refused before the network — the route is never
      called and the response is not a success.
- [x] A test named
      `a_refused_tool_schema_is_rewritten_and_the_same_route_answers` drives
      both observed refusal texts — Anthropic's `input_schema does not support
      oneOf` and OpenAI's `schema must have type 'object'` — through the
      loopback fixture, and asserts the same route is called twice and answers
      on the second call with no union left in the tool schema.
- [x] `.cartridge/help.md` and `.cartridge/docs/recovery.md` name the tool
      schema adaptation in the same change, including the `tool-schema` cause
      label `router availability` reports and the fact that the rewrite is top
      level only.

## Verify and Proof

<!--
How collect runs these blocks (engine facts, src/lifecycle.ts collect/verify):
- Each sh/bash/shell block runs as `sh -eu -c`, 120 s limit, empty stdin, the
  collector's environment.
- With a lane it runs twice: first in the lane, then in `repo`. This PRD is
  planned to collect with no lane, so each block runs once, in `repo`.
- Paths are relative to the repo root. Never `cd` to an absolute checkout.
- The host hot-restarts a cartridge when its target/debug dylib changes, so
  every cargo block first sets
  `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/<slug>-verify}"`.
- A block must not write inside the footprint. Scratch goes to mktemp;
  `target/` is gitignored and outside the footprint.
-->

Block 1 — every behavioral claim, and the only gate on Acceptance line 3. One
widening test per union keyword, the two new behavioral tests, and the waiver
regression. The loop names each test exactly, so a keyword that is never
proven makes `--exact` match nothing and the `... ok` guard fails the block —
which is why the widening proof is three tests rather than one loop inside
one. A cold build of this crate into a fresh target dir measures 10–15 s on
this machine, so the 120 s limit holds with room to spare.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/tool-schema-verify}"
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
for t in \
	an_all_of_tool_schema_is_widened_into_the_object_every_provider_takes \
	a_one_of_tool_schema_is_widened_into_the_object_every_provider_takes \
	an_any_of_tool_schema_is_widened_into_the_object_every_provider_takes \
	a_refused_tool_schema_is_rewritten_and_the_same_route_answers \
	a_rule_that_drops_the_conversation_is_still_refused \
	an_adaptation_applies_where_a_waiver_is_refused
do
	cargo test --lib -- --exact "proxy::capability_tests::$t" > "$log" 2>&1 || { cat "$log"; exit 1; }
	cat "$log"
	grep -q "^test .*$t \.\.\. ok$" "$log" || { echo "$t did not run"; exit 1; }
done
```

Block 2 — the rule and the guard are the ones described: learned from the
refusal text, never from a provider's name, and judged by `preserves` rather
than by a whole-request diff. Behavior is block 1's job; this block only pins
that the mechanism did not get replaced by a different one. It therefore
**passes at the base commit by design** — it is a regression tripwire on
already-landed structure, not evidence of the outstanding work, and it pins no
implementation literal of the `preserves` fix, whose proof is block 1's
`a_rule_that_drops_the_conversation_is_still_refused`.

```sh
test -f src/health.rs
test -f src/proxy.rs
grep -q 'pub widen_tools: bool' src/health.rs
grep -q 'next.widen_tools = true' src/health.rs
grep -q 'fn tool_schema_refused' src/health.rs
grep -q 'pub fn widen_schema' src/health.rs
grep -q 'pub fn preserves' src/health.rs
grep -q 'rules.preserves(&key)' src/proxy.rs
grep -q 'crate::requirements::present(body, &key)' src/proxy.rs
if grep -qn 'route.provider' src/health.rs; then
	echo "an adaptation branched on the provider rather than on the refusal"
	exit 1
fi
```

Block 3 — the refusal texts this PRD was filed for are exercised verbatim, and
the docs name the adaptation in words only this change introduces. `oneOf` and
`widen` already appear in the live `recovery.md` from a sibling PRD's pending
rows, so they are not evidence here; `tool-schema` and `top level` are (the
sibling writes "top-level", hyphenated, and never writes the cause label). The
`"$k":` loop is a backstop only — block 1's three named tests are what gate
Acceptance line 3.

```sh
tests=.cartridge/tests/unit/proxy/capabilities.rs
test -f "$tests"
grep -q 'input_schema does not support oneOf' "$tests"
grep -q "schema must have type 'object'" "$tests"
grep -q 'a_refused_tool_schema_is_rewritten_and_the_same_route_answers' "$tests"
grep -q 'a_rule_that_drops_the_conversation_is_still_refused' "$tests"
for k in allOf oneOf anyOf; do
	grep -q "\"$k\":" "$tests" || { echo "$k is never built into a schema"; exit 1; }
done
grep -qi 'tool schema' .cartridge/help.md
grep -q 'tool-schema' .cartridge/docs/recovery.md
grep -qi 'top level' .cartridge/docs/recovery.md
```

## Denied worlds

- Drop the `preserves` change: `a_rule_that_drops_the_conversation_is_still_refused`
  fails, because `PRESERVING` contains `messages` and the route is called with
  the conversation gone.
- Make `preserves` deny every key instead: the rename test
  (`.cartridge/tests/unit/proxy/capabilities.rs:1654-1688`), the role test and
  `a_refused_tool_schema_is_rewritten_and_the_same_route_answers` all fail,
  since each of them changes a key the rule was supposed to be allowed to
  change.
- Promote a branch's `required` into the widened object: all three widening
  tests fail on `schema["required"]`, which is the narrowing the Outcome shape
  forbids.
- Keep one combined widening test, or split it and then let `oneOf`/`anyOf`
  quietly lapse: block 1's loop runs
  `cargo test --lib -- --exact proxy::capability_tests::a_one_of_tool_schema_is_widened_into_the_object_every_provider_takes`,
  the filter matches 0 tests, the run still exits 0, and the
  `grep -q "^test .*$t \.\.\. ok$"` guard fires with
  `a_one_of_… did not run` and exits 1. That guard is the whole gate on
  Acceptance line 3; block 3's `"$k":` greps are a backstop for a schema
  literal that never reaches an assertion, nothing more.
- Special-case a provider name to decide when to widen: block 2 exits 1.
- Claim a lane after all: the fast-forward aborts on the dirty `help.md` and
  `recovery.md` after the lane commit has landed, and the PRD is stuck
  claimed. Recovery is to reset the lane branch and re-collect with no lane —
  which is why this plan never takes one.
