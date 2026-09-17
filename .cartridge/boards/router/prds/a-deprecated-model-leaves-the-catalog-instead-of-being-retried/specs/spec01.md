---
complexity: small
footprint:
  - /Users/feb/dev/cartridge/router.ctg/src/health.rs
  - /Users/feb/dev/cartridge/router.ctg/.cartridge/tests/unit/proxy/capabilities.rs
---

# spec01 — The periodic override stops re-asking a model the provider withdrew

## Base and dependencies

Base: `router.ctg` at **`7b2917a`** ("Keep answering while accounts wall, and
come back when they reopen"), which is HEAD and a clean working tree. The PRD
was briefed at `05bef5a`; `42bddc0` and `7b2917a` landed while this spec was
written, and every line number and measurement below was re-derived against
`7b2917a`, not carried over. No dependency on unlanded work remains.

What the two new commits changed for this outcome:

- `Health::fail` now takes `Answer<'_>` instead of `(status, error)`, and
  `availability()` expires every kind at its own `retry_at`. `Kind::Withdrawn`
  is exempt because it returns early above that condition
  (`src/health.rs:810`). Nothing in this spec calls `fail` or `Answer`: the
  tests drive real turns through `Proxy::execute` and read `Incident` fields,
  so they are indifferent to that signature.
- The deferred queue in the routing loop became `Vec<(u64, Route)>` sorted by
  `retry_at` (`src/proxy.rs:437,449-450`). A withdrawn route carries
  `retry_at = u64::MAX`, so it is now the *last* of the deferred routes a
  last-resort pass reaches. It is still reached — see the residue below.

Five of the PRD's six Acceptance lines already hold at `7b2917a`. The one that
does not is the one the PRD names last: a withdrawn route **is** still ranked
and still asked, once every `limits.retry_every` (default 10,
`cartridge.json:288-290`) turns, by the periodic override at
`src/proxy.rs:464`. Measured, not inferred: 24 `auto` turns against a fixture
whose top-ranked route answers `400 … has been deprecated` asked it **3** times.

## The change

One guard, in the one function that decides whether health's verdict may be
overridden. `src/health.rs:652`:

```rust
	pub async fn retry_due(&self, route: &str) -> bool {
		let mut skips = self.skips.lock().await;
```

becomes, unchanged below the guard:

```rust
	pub async fn retry_due(&self, route: &str) -> bool {
		// A withdrawn model is the one prediction that cannot be wrong: the
		// periodic override exists to re-test health's guess, and there is no
		// guess here. Spending a turn's attempt on it buys nothing.
		if self
			.data
			.read()
			.await
			.incidents
			.get(route)
			.is_some_and(|i| i.kind == Kind::Withdrawn && i.state != "recovered")
		{
			return false;
		}
		let mut skips = self.skips.lock().await;
```

The read lock is taken and released before the `skips` mutex, so it cannot
deadlock against `fail()`/`persist()`, which take `data` and release it before
writing. Verified against `7b2917a` in a scratch copy: this exact patch turns
the 3 calls above into 1, both new tests go from red to green, and the suite is
92/92 (90 committed + 2 new).

Nothing else in `src/` changes. `sync.rs` in particular is **not** touched: the
PRD rejected deleting the catalog row, the provider republishes the id on every
refresh, and at `7b2917a` `sync.rs` never mentions `incidents` at all. The
withdrawal outliving the refresh is a property of the health store, and block 2
pins that it stays one.

## What already holds at 7b2917a (do not rebuild)

| PRD line | Holds? | Evidence at `7b2917a` |
| - | - | - |
| 1. `classify` distinguishes a withdrawal from a refused request | yes | `classify` `src/health.rs:54`, the `withdrawn()` matcher `:110-118` (three provider phrasings, wording only), and `deprecated_parameter` `:335` which keeps "`temperature` is deprecated **for this model**" a droppable field rather than a withdrawal |
| 2. shelved permanently, no recovery budget, no retry | partly | `fail()` sets `Recovery::degraded(t, "model_withdrawn_by_provider")` `src/health.rs:725` and `retry_at = u64::MAX` `:758-759`; the healer refuses it by authority `src/proxy.rs:1507`; `availability()` returns it before any expiry test `src/health.rs:810`. **But the routing loop still asks it through `retry_due` `src/proxy.rs:464`** — this spec's change |
| 3. a stale inventory entry cannot resurrect it | yes | `src/sync.rs` contains no reference to `incidents` (0 matches); the withdrawal lives in the health store and survives a reload. Untested — block 1 test 3 |
| 4. `status` names the withdrawal, distinct from compatibility | yes | `health::availability()` `src/health.rs:389-415` itemises only `Kind::Compatibility` under `adaptable` and counts the rest by kind name; measured for a withdrawn route: `{"adaptable":[],"operator":{"withdrawn":1}}`. The per-incident `state:"withdrawn"` and the provider's own sentence survive into `op status`, because `summarize` keeps the text for `Kind::Withdrawn` `:976-979` |
| 5. a test asserts it is not ranked as a candidate for `auto` | **no** | no such test exists, and the behaviour is false at `7b2917a` |
| 6. not inferred from a 404 alone | yes | `withdrawn()` reads wording only; `classify(404, "unknown endpoint") == Compatibility`, already asserted by `a_withdrawn_model_is_shelved_for_good_rather_than_probed` |

**Known residue, out of footprint.** When *every* other candidate is shelved,
the loop's last-resort pass (`src/proxy.rs:449-450,497`) drains the deferred
queue and still asks the withdrawn route — last, now that the queue sorts by
`retry_at`, but it asks. Measured with this spec's guard applied: 3 turns where
both siblings answer 503 asked the withdrawn route 5 times. Removing that needs
`src/proxy.rs`, which this PRD's footprint does not allow, and that path only
runs on a turn that was already going to fail. Acceptance line 5 is therefore
specified as: **while the turn has any other candidate, a withdrawn route is
never asked again.** A follow-up PRD owning `src/proxy.rs` should exempt
`Kind::Withdrawn` from the last-resort override; after this change it is the
only path left that can reach a withdrawn route.

## Acceptance

- [x] `retry_due` returns `false` for a route whose open incident is
      `Kind::Withdrawn`, and is unchanged for every other route.
- [x] Driven through `Proxy::execute` with `model: "auto"`, a route the provider
      answered with "has been deprecated" is asked exactly once and never ranked
      again over `2 × limits.retry_every` turns, while another route serves
      every turn.
- [x] The withdrawal survives a reload of the health store from disk: a fresh
      `Health::load` of the same file still reports the route unavailable and
      still refuses `retry_due`, while the catalog row for that id is untouched.
- [x] `src/sync.rs` still never touches the health store, and the withdrawal is
      reported as `operator.withdrawn`, never under `adaptable`.
- [x] The committed `a_withdrawn_model_is_shelved_for_good_rather_than_probed`
      still passes unchanged, including `classify(404, …) == Compatibility`, and
      the whole unit suite is green.
- [x] No new file appears under `.cartridge/tests`: both tests go into
      `.cartridge/tests/unit/proxy/capabilities.rs`, the only test file in this
      footprint. An untracked sibling would be invisible to `collect`'s sweep
      and would strand the `#[path]` module at `src/proxy.rs:1569`.

## Verify and Proof

<!--
How collect runs these blocks (engine facts, src/lifecycle.ts collect/verify):
- Each sh/bash/shell block runs as `sh -eu -c`, 120 s limit, empty stdin, the
  collector's environment.
- It runs twice: first with cwd = the lane, a worktree of `repo` at
  `prd.ctg/.cartridge/boards/router/.lanes/<slug>`; then, after the
  fast-forward, with cwd = `repo` itself.
- Paths are relative to the repo root. Never `cd` to an absolute checkout.
- Pass 2 runs in the live checkout, so every cargo block first sets
  `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/withdrawn-verify}"`
  and never builds into `target/debug`, which would hot-restart the live
  cartridge.
- A block must not write inside the footprint; scratch goes to `mktemp`.
-->

Block 1 — behaviour. Three named tests: the one already committed and the two
this spec adds. `--exact` against a name that does not exist matches nothing and
still exits 0, so the `... ok` grep after each run is the real gate — a renamed,
deleted or filtered-out test fails the block with `<name> did not run`. Measured
against `7b2917a` on this machine: 10 s cold into a fresh target dir, 1.3 s for
the whole 92-test suite warm. Both new tests fail at the base commit (`3 != 1`,
and `no override reaches a withdrawal`) and pass with the guard.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/withdrawn-verify}"
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
for t in \
	a_withdrawn_model_is_shelved_for_good_rather_than_probed \
	a_withdrawn_route_is_not_ranked_again_for_auto \
	a_reloaded_store_still_refuses_a_withdrawn_route
do
	cargo test --lib -- --exact "proxy::capability_tests::$t" > "$log" 2>&1 || { cat "$log"; exit 1; }
	grep -q "^test .*$t \.\.\. ok$" "$log" || { echo "$t did not run"; exit 1; }
	echo "ran $t"
done
cargo test --lib > "$log" 2>&1 || { cat "$log"; exit 1; }
grep -q "^test result: ok\." "$log" || { echo "the unit suite is not green"; exit 1; }
```

Block 2 — mechanism and the rejected alternatives. The guard lives inside
`retry_due` and the withdrawal stays a health fact rather than a catalog
deletion. Each negated guard is written as `if grep -qn …; then exit 1; fi`,
because `! grep …` is inert under `sh -eu`. The `sed` range was checked in both
directions: at `7b2917a` it prints `retry_due` without `Kind::Withdrawn` and the
block fails; with the guard it prints it and the block passes.

```sh
test -f src/health.rs
test -f src/sync.rs
sed -n '/pub async fn retry_due/,/^	}/p' src/health.rs | grep -q 'Kind::Withdrawn' \
	|| { echo "retry_due does not exempt a withdrawn route"; exit 1; }
grep -q 'has been deprecated' src/health.rs
grep -q 'Kind::Withdrawn && incident.state != "recovered"' src/health.rs
if grep -qn 'incidents' src/sync.rs; then
	echo "sync touched the health store: the withdrawal must outlive the refresh, not be refought on every refresh"
	exit 1
fi
if grep -qn 'routes.retain\|models.remove' src/sync.rs; then
	echo "the catalog row was deleted in sync; the PRD rejected that"
	exit 1
fi
stray="$(git ls-files --others --exclude-standard -- .cartridge/tests)"
if [ -n "$stray" ]; then
	echo "untracked test file outside the footprint, unbuildable from a clean checkout:"
	echo "$stray"
	exit 1
fi
```

## The two tests, as probed

Both go at the end of `.cartridge/tests/unit/proxy/capabilities.rs`, appended,
touching no existing line. Both were compiled and run against a scratch copy of
`7b2917a`: red at base, green with the guard. The `.clone()` on the snapshot is
load-bearing — `health::availability` takes `&Snapshot`, and a
`RwLockReadGuard` does not coerce there.

```rust
/// The periodic override exists to re-test health's guess. A withdrawal is not
/// a guess, and the live router spent fourteen attempts each on five of them.
#[tokio::test]
async fn a_withdrawn_route_is_not_ranked_again_for_auto() {
	let fixture = fixture(Wire::Chat).await;
	let gone = json!({"error":{"message":"The model `fixture-model` has been deprecated, learn more here: https://platform.openai.com/docs/deprecations"}}).to_string();
	fixture.responses.lock().unwrap().insert("first".into(), (400, gone));
	let body = json!({"model":"auto","messages":[{"role":"user","content":"answer"}]});
	// Twice the retry_every budget: at base the override fires on turns 10 and 20.
	for turn in 0..24 {
		let response = fixture.proxy.clone().execute("fixture-key", Wire::Chat, body.clone()).await;
		assert_eq!(response.status(), StatusCode::OK, "turn {turn}");
	}
	let calls = fixture.calls.lock().unwrap();
	assert_eq!(
		calls.iter().filter(|(name, _)| name == "first").count(),
		1,
		"a withdrawn route is asked once and never ranked again while another route can serve"
	);
}

/// The provider keeps publishing the id, so the catalog keeps the row. The
/// route stays gone because the incident outlives the refresh — and the restart.
#[tokio::test]
async fn a_reloaded_store_still_refuses_a_withdrawn_route() {
	let fixture = fixture(Wire::Chat).await;
	let gone = json!({"error":{"message":"The model `fixture-model` has been deprecated, learn more here: https://platform.openai.com/docs/deprecations"}}).to_string();
	fixture.responses.lock().unwrap().insert("first".into(), (400, gone));
	let body = json!({"model":"auto","messages":[{"role":"user","content":"answer"}]});
	assert_eq!(
		fixture.proxy.clone().execute("fixture-key", Wire::Chat, body).await.status(),
		StatusCode::OK
	);
	assert!(fixture.proxy.catalog.read().await.routes.iter().any(|r| r.id == "fixture@first"));
	// load() clamps every retry_at to now + max_cooldown, so only the Withdrawn
	// early return in availability() keeps this route off the shelf.
	let reloaded = Health::load(fixture.path.join("health.json")).await.unwrap();
	let incident = reloaded.availability("fixture@first", false).await.expect("still unavailable");
	assert_eq!(incident.kind, Kind::Withdrawn);
	assert_eq!(incident.state, "withdrawn");
	for _ in 0..24 {
		assert!(!reloaded.retry_due("fixture@first").await, "no override reaches a withdrawal");
	}
	let report = crate::health::availability(&reloaded.data.read().await.clone());
	assert!(report["adaptable"].as_array().unwrap().is_empty());
	assert_eq!(report["operator"]["withdrawn"], 1);
}
```
