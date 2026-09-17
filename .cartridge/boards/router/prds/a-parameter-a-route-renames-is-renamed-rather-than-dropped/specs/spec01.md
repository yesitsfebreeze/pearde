---
complexity: small
footprint:
  - .cartridge/tests/unit/proxy/capabilities.rs
---

# spec01 — The rename the provider asked for is proven, including the two halves nobody tests

Base: `router.ctg` at `08d9463fea82e1484242ae446d0d17c3ad8cfc59`
(`Implement @router/a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect`),
the commit that landed while this spec was written. The PRD was briefed at
`121913e`; the only behaviour this spec depends on that moved between the two is
`Rules::preserves`, which gained a leading `!self.drop.contains(key)` — it
tightens the waiver guard and does not touch the rename path.

**This outcome is already implemented in production code. No line of
`src/health.rs` or `src/proxy.rs` needs to change.** What is missing is proof:
two of the six Acceptance lines are claims no committed test can fail. The spec
still states all six and still gates all six, because a claim nobody can fail is
not a claim.

What is committed, per Acceptance line:

| # | Claim | Committed at `08d9463` | Gated by a test? |
| - | - | - | - |
| 1 | `Rules` carries a per-route rename map, learned through `propose` | `pub rename: BTreeMap<String, String>` `src/health.rs:141`; `next.rename.insert(from, to)` `src/health.rs:246`; `renamed_field` reads the `Use 'X' instead` clause `src/health.rs:311-330` | Only indirectly. No test asserts `propose` returns the map. **Gap.** |
| 2 | `max_tokens` is renamed, never dropped; a test pins it out of `DROPPABLE` | `DROPPABLE` `src/health.rs:267-278` has 12 entries and `max_tokens` is not one; the rename branch runs *before* the drop branch (`src/health.rs:245-251`, `else if`) | **No. `DROPPABLE` is private and no test names it or its exclusion. This is the gap the PRD asks for by name.** |
| 3 | The rename applies in the same turn | the generic same-turn retry `src/proxy.rs:580-587` | Yes — `a_renamed_parameter_moves_its_value_instead_of_losing_it` asserts the refused route is called twice in one turn. |
| 4 | The `attempt` guard admits a value-carrying rename, still refuses a rule that loses the value | `src/proxy.rs:848-856`; `Rules::preserves` `src/health.rs:221-226` returns true for either side of the rename map | Yes, both halves. Admit: the rename test asserts the refused route is called **twice** — strip the rename clauses from `preserves` and the guard returns `WAIVER_REFUSED` before the network, so the retry never reaches the server and `first.len() == 2` fails. (The turn still answers `200` through the fixture's sibling route, so the status assertion alone would not catch it.) Refuse: `an_adaptation_applies_where_a_waiver_is_refused` asserts the route is never called. |
| 5 | A test drives the observed message through the loopback fixture | — | Yes — `a_renamed_parameter_moves_its_value_instead_of_losing_it` uses the PRD's evidence string verbatim and asserts `max_completion_tokens == 100`. |
| 6 | A rename is learned only when the message names both sides | `renamed_field` returns `None` unless the text has both `not supported` and `use ` and two distinct quoted, name-shaped, non-conversation tokens (`src/health.rs:314-329`) | **No. Nothing exercises a one-sided message, and nothing pins that `messages`/`input`/`tools` are refused as rename targets. Gap.** |

Outstanding work, in order. Both items are tests, both go into
`.cartridge/tests/unit/proxy/capabilities.rs`, and both are pure `#[test]`s
over `Rules::propose` — no fixture, no network, sub-millisecond.

1. **`an_output_budget_is_renamed_rather_than_dropped`** — Acceptance line 2,
   and the `propose` half of line 1. Feed `propose` the observed refusal and
   assert the learned rule maps `max_tokens` to `max_completion_tokens` **and**
   that `drop` is empty. Then feed it the same refusal with the second half cut
   off — `Unsupported parameter: 'max_tokens'` — and assert `propose` returns
   `None`. That second assertion is the test the PRD asks for: it fails the
   moment anyone adds `max_tokens` to `DROPPABLE`, without naming the private
   constant or grepping for its literal.

2. **`a_rename_is_learned_only_when_the_message_names_both_sides`** —
   Acceptance line 6, which is a conjunction, so it takes one probe per
   conjunct. Four assertions, all against `propose`:
   `Unsupported parameter: 'temperature'` still learns a drop and no rename;
   `cause("Unsupported parameter: 'max_tokens'")` is `unknown`, which is the
   degraded incident the line names, and which also fails if `max_tokens` ever
   enters `DROPPABLE`; a message carrying **two** quoted, name-shaped tokens
   that the provider never joined with `use` —
   `… 'max_tokens' is not supported with this model. Try 'max_completion_tokens' instead.` —
   learns nothing; and a both-sides message whose refused name is `messages`
   learns nothing, because rewriting the conversation is not a spelling
   difference.

   The third probe is the one that matters and the one a shorter test misses.
   `renamed_field` guards on two conjuncts, `not supported` **and** `use `
   (`src/health.rs:314-316`), before pairing quoted tokens at `:317-319`. Every
   probe carrying a single quoted token returns `None` at the pairing step
   whether or not the `use ` guard exists, so a test built only from one-sided
   messages leaves that guard entirely unproven: deleting it is invisible.
   Only a message that *would* pair — two names, no instruction joining them —
   distinguishes the two. Verified in both directions below.

Both tests were written and run against this base before this spec was
published; both pass, block 1 exits 1 without them, and block 1 exits 1 again
when the `use ` conjunct is deleted from `renamed_field` (see **Observed**). The
verified
source, to append to `.cartridge/tests/unit/proxy/capabilities.rs` — the file's
`use super::*` already supplies `Rules` and `json!`, and `crate::health::cause`
is public:

```rust
/// The output limit is the caller's budget: a route that spells it differently
/// gets it under the name it accepts, and a route that merely refuses the name
/// never gets to throw the budget away. `max_tokens` is deliberately absent
/// from `DROPPABLE`, and a one-sided refusal of it therefore learns nothing.
#[test]
fn an_output_budget_is_renamed_rather_than_dropped() {
	let body = json!({"model":"fixture","max_tokens":100});
	let observed = "Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.";
	let learned = Rules::default()
		.propose(&body, observed)
		.expect("the message names both sides");
	assert_eq!(
		learned.rename.get("max_tokens").map(String::as_str),
		Some("max_completion_tokens"),
		"the budget moves to the name the route accepts"
	);
	assert!(
		learned.drop.is_empty(),
		"a renamed parameter is never also dropped"
	);
	assert!(
		Rules::default()
			.propose(&body, "Unsupported parameter: 'max_tokens'")
			.is_none(),
		"max_tokens stays out of DROPPABLE, so a one-sided refusal learns no drop"
	);
}

/// A rename needs the provider to name both sides *and* say which one to use.
/// One half falls to the drop rule when the field is droppable and to a
/// degraded incident when it is not; two names with no instruction joining
/// them are two names, not a substitution; and a message that names the
/// conversation is never a spelling difference.
#[test]
fn a_rename_is_learned_only_when_the_message_names_both_sides() {
	let body = json!({"model":"fixture","max_tokens":100,"temperature":0.5});
	let dropped = Rules::default()
		.propose(&body, "Unsupported parameter: 'temperature'")
		.expect("a droppable field is still learned");
	assert!(dropped.rename.is_empty(), "one half is not a rename");
	assert!(dropped.drop.contains("temperature"));
	assert_eq!(
		crate::health::cause("Unsupported parameter: 'max_tokens'"),
		"unknown",
		"a refusal the router cannot adapt degrades rather than guessing"
	);
	// Both names are present and both are name-shaped, so the quoted-pair step
	// would happily pair them. Only the `use` clause makes the second name a
	// replacement rather than a second complaint.
	assert!(
		Rules::default()
			.propose(
				&body,
				"Unsupported parameter: 'max_tokens' is not supported with this model. Try 'max_completion_tokens' instead."
			)
			.is_none(),
		"two names the provider never joined with `use` are not a rename"
	);
	assert!(
		Rules::default()
			.propose(
				&body,
				"Unsupported parameter: 'messages' is not supported with this model. Use 'input' instead."
			)
			.is_none(),
		"rewriting the conversation is not a spelling difference"
	);
}
```

## Landing: this PRD collects with no lane

The implementer works directly in `/Users/feb/dev/cartridge/router.ctg` and the
coordinator collects from state `specced`, with no lane. The engine permits it:
`prd.ctg/src/lifecycle.ts:113` accepts `claimed` **or** `specced`, and with no
lane directory `:125` selects `tree = code`, so `:166`'s `git merge --ff-only`
never runs and there is no abort-after-commit. Three PRDs landed this way today,
the most recent being `08d9463` an hour before this spec. With no lane the
Verify blocks run once, in `repo`.

The consequence, stated exactly. `collect`'s status sweep
(`prd.ctg/src/lifecycle.ts:143-155`) runs `git status` over `feet(prd)` — the
union of the PRD footprint and every spec footprint
(`prd.ctg/src/planner.ts:5-9`) — and commits **every** dirty path it finds
there. This spec's footprint is one file. The observed tree at `08d9463`:

```
$ git -C /Users/feb/dev/cartridge/router.ctg status --porcelain=v1 --untracked-files=all
 M .cartridge/docs/cost-latency.md
 M .cartridge/tests/unit/auth/tests.rs
 M .cartridge/tests/unit/catalog/capabilities.rs
 M .cartridge/tests/unit/settings/tests.rs
 M .cartridge/tests/unit/sync/tests.rs
 M cartridge.json
 M src/catalog.rs
 M src/known.json
 M src/service.rs
 M src/sync.rs
?? .cartridge/memos/system/vision.md
?? .cartridge/memos/type/system.md
```

`.cartridge/tests/unit/proxy/capabilities.rs` and `src/health.rs` are **clean**:
the neighbour PRD collected them into `08d9463` while this analysis ran. So this
spec's footprint sweeps nothing but the two new tests the implementer writes.

**Precondition on the coordinator, before collecting.** The PRD frontmatter
still names the bare directory `.cartridge/tests`. `feet` resolves it to the
directory and the sweep matches every path under it, so collection would commit
`auth/tests.rs`, `catalog/capabilities.rs`, `settings/tests.rs` and
`sync/tests.rs` — 87 insertions of another session's uncollected work, under an
`Implement @router/a-parameter-…` message. **Narrow the PRD footprint to
`src/health.rs` and `.cartridge/tests/unit/proxy/capabilities.rs`** before
collecting, exactly as the neighbour PRD's footprint was narrowed. An analyst
may not edit that frontmatter, so it is named here as a gate rather than done.
`src/health.rs` stays in the PRD footprint although this spec changes nothing in
it; it is clean, so it sweeps nothing.

**No new file under `.cartridge/tests`.** Both tests go into
`.cartridge/tests/unit/proxy/capabilities.rs`, appended near
`a_renamed_parameter_moves_its_value_instead_of_losing_it`. A new file there
would need a `#[path]` module declaration in `src/` — outside this spec's
footprint, therefore uncommitted, therefore a crate no clean checkout can build.
That failure happened on this repository today and cost two repair commits,
`fae0290` and `121913e`.

`src/health.rs` and `src/proxy.rs` are **deliberately frozen**. Every behaviour
the Acceptance lines claim is already in them; the gap is proof, not code. Block
2 only reads them. If an implementer concludes a `health.rs` edit is genuinely
required, stop and tell the coordinator rather than working around it — a
production change here would mean this evidence table is wrong.

Not in scope, deliberately, and the tension named plainly. `renamed_field`
recognises exactly one wording: `not supported` somewhere, `use ` somewhere,
and the first two quoted tokens in order. A provider that words the same
disagreement without quotes, that names the replacement before the refusal, or
that instructs the substitution with any verb other than *use* — "try", "pass",
"send", "switch to" — is **not** adapted, and the route degrades with cause
`unknown`.

That is a real narrowing of the Outcome, and this spec accepts it knowingly
rather than silently. All five shelved routes send OpenAI's one sentence
verbatim, no Acceptance line claims a second wording, and `unknown` is the
router's way of naming the next shape to learn, so widening the parser now
would be guessing at a message nobody has seen. The cost of the narrowing is
bounded and visible: such a route is shelved and shows up in
`router availability` as `unknown`, which is the trigger for the next PRD.
What this spec does insist on is that the `use ` conjunct is *deliberate* and
stays deliberate — hence the third probe, which fails the moment someone
"generalises" the parser by deleting the guard rather than by widening it on
purpose.

## Acceptance

- [x] `Rules` carries a per-route rename map (`src/health.rs:141`) that
      `propose` fills from the `Use 'X' instead` clause of the provider's own
      message, and a test named `an_output_budget_is_renamed_rather_than_dropped`
      asserts the learned rule maps `max_tokens` to `max_completion_tokens`.
- [x] The same test asserts the learned rule's `drop` set is empty, and that a
      refusal naming only `max_tokens` teaches `propose` nothing — pinning
      `max_tokens` out of `DROPPABLE` by behaviour rather than by naming the
      private constant.
- [x] `a_renamed_parameter_moves_its_value_instead_of_losing_it` asserts the
      refused route is called twice within one turn, so the rename applies
      before the caller loses the turn.
- [x] That same two-call assertion is what proves the `attempt` guard
      (`src/proxy.rs:848-856`) admitted the rename: it only reaches the server a
      second time because `preserves` (`src/health.rs:221-226`) recognises both
      sides of the rename map. And `an_adaptation_applies_where_a_waiver_is_refused`
      asserts a rule that removes a field the caller supplied is refused before
      the network.
- [x] `a_renamed_parameter_moves_its_value_instead_of_losing_it` drives the
      PRD's observed message verbatim through the loopback fixture and asserts
      the retried request carries `max_completion_tokens` with the original
      value `100`, and no `max_tokens`.
- [x] A rename is learned only from a message that names both sides **and**
      says which one to use; anything less still falls to the drop rule or to a
      degraded incident. `a_rename_is_learned_only_when_the_message_names_both_sides`
      proves the property one conjunct at a time: a one-sided refusal of a
      droppable field still learns a drop and no rename; a one-sided refusal
      the router cannot adapt reports cause `unknown`; two quoted, name-shaped
      tokens the provider never joined with `use` learn nothing; and a
      both-sides message naming `messages` learns nothing. The third probe is
      the only one that exercises the `use ` conjunct at `src/health.rs:314-316`
      — every single-token probe returns `None` at the quoted-pair step
      regardless of it.

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

Block 1 — every Acceptance line. Four tests, each named exactly: the two this
change adds and the two already committed that carry lines 3, 4 and 5. `--exact`
against a name that does not exist matches nothing and still exits 0, so the
`... ok` grep after each run is the real gate — a deleted, renamed or filtered-out
test fails the block with `<name> did not run`. Measured cold into a fresh target
dir on this machine: 12 s for the whole loop, well inside the 120 s limit.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/rename-verify}"
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
for t in \
	an_output_budget_is_renamed_rather_than_dropped \
	a_rename_is_learned_only_when_the_message_names_both_sides \
	a_renamed_parameter_moves_its_value_instead_of_losing_it \
	an_adaptation_applies_where_a_waiver_is_refused
do
	cargo test --lib -- --exact "proxy::capability_tests::$t" > "$log" 2>&1 || { cat "$log"; exit 1; }
	grep -q "^test .*$t \.\.\. ok$" "$log" || { echo "$t did not run"; exit 1; }
	echo "ran $t"
done
```

Block 2 — the mechanism is still the one this evidence table describes: a rename
learned from the refusal text, stored per route, and judged by `preserves`
rather than by a whole-request diff. Behaviour is block 1's job; the `grep`s
here are a regression tripwire on structure that already landed, so they
**pass at the base commit by design** and are not evidence of the outstanding
work. Two guards do more than that:

- The negative `route.provider` guard: an adaptation decided by a provider's
  name instead of by what the provider said would satisfy every test in block 1
  and still be the wrong mechanism.
- The untracked-file guard, which the sibling tool-schema spec's round-3 review
  deferred to the next spec on this board. This spec forbids a new file under
  `.cartridge/tests` in prose, and prose does not fail a block. With the
  footprint narrowed to one file, a new test file there is invisible to
  `collect`'s sweep, is never committed, and strands the `#[path]` declaration
  that `src/proxy.rs:1244` would need — a crate no clean checkout can build.
  That failure cost this repository two repair commits today (`fae0290`,
  `121913e`). `git ls-files --others --exclude-standard` lists exactly the
  paths the sweep would miss, so the guard fires precisely when the hazard is
  real; a file that *is* tracked, or one the sweep will commit, does not trip
  it. Verified in both directions below.

```sh
test -f src/health.rs
test -f src/proxy.rs
grep -q 'pub rename: BTreeMap<String, String>' src/health.rs
grep -q 'fn renamed_field' src/health.rs
grep -q 'next.rename.insert(from, to)' src/health.rs
grep -q 'self.rename.contains_key(key)' src/health.rs
grep -q 'rules.preserves(&key)' src/proxy.rs
if grep -qn 'route.provider' src/health.rs; then
	echo "the rename was learned from a provider name rather than from the refusal"
	exit 1
fi
stray="$(git ls-files --others --exclude-standard -- .cartridge/tests)"
if [ -n "$stray" ]; then
	echo "untracked test file outside the footprint, unbuildable from a clean checkout:"
	echo "$stray"
	exit 1
fi
```

### Observed

Run by the analyst in `/Users/feb/dev/cartridge/router.ctg` at `08d9463`, with
`CARGO_TARGET_DIR` pointed outside the checkout so the live daemon was not
restarted:

| Block | Tree | Exit |
| - | - | - |
| 1 | base, without the two new tests | `1` — `an_output_budget_is_renamed_rather_than_dropped did not run` |
| 1 | base + the two new tests appended | `0` — all four `ran` |
| 1 | base + the two new tests, with the `use ` conjunct deleted from `renamed_field` (`src/health.rs:314`) | `1` — `a_rename_is_learned_only_when_the_message_names_both_sides` panics with `two names the provider never joined with \`use\` are not a rename` |
| 2 | base | `0` |
| 2 | base + an untracked `.cartridge/tests/unit/proxy/stray_probe.rs` | `1` — the stray path is named |

Every probe was reverted. `src/health.rs` is back at
`md5 43ef55079d62d207380da942756b2efd` with an empty `git diff`, and
`.cartridge/tests/unit/proxy/capabilities.rs` at
`md5 4fa525ed65e4e54d24406123cf1c9475`, both unchanged from before the probes;
the working tree carries none of this analyst's edits.

## Denied worlds

- Skip either new test: block 1's `--exact` filter matches nothing, `cargo test`
  still exits 0, and the `... ok` grep fires `<name> did not run` and exits 1.
  This is the only gate on Acceptance lines 2 and 6.
- Add `max_tokens` to `DROPPABLE` to "simplify" the refusal path:
  `an_output_budget_is_renamed_rather_than_dropped`'s third assertion fails,
  because `propose` now learns a drop from `Unsupported parameter: 'max_tokens'`
  instead of returning `None` — and the caller's output budget is gone.
- Move the rename branch after the drop branch in `propose` (`src/health.rs:245-251`):
  **this is not gated, and honestly is not a hazard.** `refused_field` cannot
  parse the two-sided message at all — it strips the `Unsupported parameter: `
  prefix and then `trim_matches(['\'', '"'])` leaves
  `max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.`,
  which matches nothing in `DROPPABLE` (`src/health.rs:285-286,304`). So the
  `else if` ordering is defensive rather than load-bearing: reordering it
  changes no observed outcome and `learned.drop.is_empty()` still passes. That
  assertion earns its place against a different mutation again — not against
  making the two branches additive (which also leaves it passing, exit `0`), and
  not against `DROPPABLE` *and* a reorder (which exits `1` on the third
  assertion at `capabilities.rs:2164`, firing on the `DROPPABLE` change alone).
  What it catches is a rename that *also* records a drop of the old name, which
  fails at `capabilities.rs:2160`.
- Delete the `use ` conjunct from `renamed_field` (`src/health.rs:314`):
  `a_rename_is_learned_only_when_the_message_names_both_sides` fails on its
  third probe, because `… 'max_tokens' … Try 'max_completion_tokens' …` now
  pairs its two quoted tokens into a rename the provider never asked for.
  Observed: exit `1`. No other probe in either test catches this — a test built
  only from one-sided messages returns `None` at the pairing step with or
  without the guard, which is exactly how this conjunct went ungated in the
  first draft of this spec.
- Accept `messages` as a rename source (`src/health.rs:324-329`): the same
  test fails on its fourth probe, because the conversation would be moved to
  `input` on a route that only ever said it could not read `messages`.
- Add `max_tokens` to `DROPPABLE` while leaving `renamed_field` alone: two
  assertions fail — `an_output_budget_is_renamed_rather_than_dropped`'s third,
  and the `cause(…) == "unknown"` assertion, which becomes `refused-field`.
- Drop the rename clauses from `preserves`: the `attempt` guard sees
  `max_tokens` changed, `requirements::present(body, "max_tokens")` is `Some`,
  and it returns `WAIVER_REFUSED` **before the network**. The turn still
  answers `200`, because the fixture's sibling route serves it unadapted — so
  the status assertion does *not* fail.
  `a_renamed_parameter_moves_its_value_instead_of_losing_it` fails on
  `assert_eq!(first.len(), 2)`: the refused route is called once and never
  retried. That is the assertion carrying Acceptance line 4's admit half, and
  it is why line 4 needs the two-call count rather than the status code.
- Make `preserves` admit everything instead:
  `an_adaptation_applies_where_a_waiver_is_refused` fails, because a rule
  dropping the caller's `temperature` would reach the network.
- Add a new test file under `.cartridge/tests`: it is outside both footprints,
  so collection never commits it, its `#[path]` declaration in `src/` is outside
  the footprint too, and the crate stops building from a clean checkout —
  `fae0290` all over again. Block 2's `git ls-files --others --exclude-standard`
  guard fires and names the path; observed exit `1` against a planted
  `.cartridge/tests/unit/proxy/stray_probe.rs`.
- Collect without narrowing the PRD's bare `.cartridge/tests` footprint entry:
  four unrelated test files carrying 87 insertions of another session's work are
  committed under this PRD's message.
- Claim a lane: a lane worktree of a submodule needs its `../*.ctg` siblings to
  build, and the fast-forward at `prd.ctg/src/lifecycle.ts:166` would run
  against a checkout dirty in `src/catalog.rs`, `src/sync.rs`, `src/known.json`
  and six more — after the lane commit has already landed, leaving the PRD stuck
  claimed.
