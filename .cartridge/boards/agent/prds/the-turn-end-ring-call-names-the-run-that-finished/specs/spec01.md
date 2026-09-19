---
complexity: small
footprint:
  - src/lib.rs
  - .cartridge/tests/unit/run_state.rs
---

# spec01 — the turn-end ring call names the run that finished

Base: `agent.ctg` HEAD `620857dde75fb9f3afe3dd6f646b3adf74538600`.

## Mechanism

`Run::finish` (`src/lib.rs:592`) fires `(self.agent.call)("harness".into(),
json!({"op":"ring"}))` with no subject once a run is durably terminal. Add
`"session":self.session,"run":self.run` to that same object literal — both
are already plain `String` fields read the same way two lines above in
`emit` (`src/lib.rs:550`), so no new clone or lifetime issue. The call stays
`tokio::spawn`ed and its result stays discarded (`let _ = sweep.await;`):
nothing about the fire-and-forget shape changes, only the payload.

`harness.ctg/src/lib.rs:795` (`fn ring`, read-only checked, not touched)
already reads `args["session"]` / `args["run"]` as `Option<&str>` and only
attempts per-turn distillation `if config.slim` and both are present;
`Value::Null` (today's call has neither key) makes both `None` and the
`match` falls to `_ => None`, i.e. today's bare `{"op":"ring"}` is silently
tolerated exactly as the PRD states. Adding the two keys is additive from
harness's side in both directions: this PRD can land before or after
harness's `slim` PRD.

Confirmed not touched by this change: `cartridge.json` (no setting, need or
event on this cartridge changes), and no other call site of `op":"ring"`
exists in `src/lib.rs`.

## Steps

1. Apply this diff (also saved at
   `prd.ctg/.cartridge/boards/agent/.state/loop/the-turn-end-ring/draft/prototype.patch`,
   produced as `diff -ruN` between the pristine archive of
   `620857dde75fb9f3afe3dd6f646b3adf74538600` and the prototype copy, paths
   relative to the repo root):

```diff
--- a/src/lib.rs
+++ b/src/lib.rs
@@ -588,8 +588,12 @@
 		// Sweep the turn ring once this turn is durably terminal. Distilling an
 		// evicted turn costs a summarization request, so the turn that just
 		// finished never waits for it, and a failed sweep deletes nothing: the
-		// next finished turn retries it.
-		let sweep = (self.agent.call)("harness".into(), json!({"op":"ring"}));
+		// next finished turn retries it. The subject travels with the ring so
+		// harness's distillation knows which run just ended.
+		let sweep = (self.agent.call)(
+			"harness".into(),
+			json!({"op":"ring","session":self.session,"run":self.run}),
+		);
 		tokio::spawn(async move {
 			let _ = sweep.await;
 		});
--- a/.cartridge/tests/unit/run_state.rs
+++ b/.cartridge/tests/unit/run_state.rs
@@ -26,6 +26,11 @@
 	harness: Option<std::sync::Arc<crate::http_fake::Harness>>,
 	/// Bearer keys released through the router `release` op.
 	releases: Vec<String>,
+	/// Every `harness ring` call this fake received, in order.
+	rings: Vec<Value>,
+	/// When set, every `harness ring` call fails; the sweep is fire-and-forget
+	/// so this must never affect a run's terminal state or its done/error event.
+	ring_error: bool,
 }
 
 impl Fakes {
@@ -41,6 +46,8 @@
 			gate: Arc::new(Notify::new()),
 			harness: None,
 			releases: Vec::new(),
+			rings: Vec::new(),
+			ring_error: false,
 		}))
 	}
 
@@ -141,6 +148,15 @@
 							.collect::<Vec<_>>();
 						Ok(json!({"system":"SYSTEM","messages":messages,"tools":tools}))
 					}
+					"ring" => {
+						let mut fakes = fakes.lock().unwrap();
+						fakes.rings.push(args.clone());
+						if fakes.ring_error {
+							Err("ring failed".into())
+						} else {
+							Ok(json!(true))
+						}
+					}
 					other => Err(format!("unexpected harness op {other}")),
 				},
 				"router" => match args["op"].as_str().unwrap() {
@@ -866,5 +882,75 @@
 	for text in [&ta, &tb] {
 		assert_eq!(count_kind(text, "run_started"), 1);
 		assert_eq!(count_kind(text, "run_finished"), 1);
+	}
+}
+
+/// Waits for the fake harness to have received `n` ring calls. The sweep is
+/// spawned after `finish` returns, so a terminal phase does not guarantee it
+/// has landed yet.
+async fn wait_rings(fakes: &Arc<Mutex<Fakes>>, n: usize) {
+	let deadline = std::time::Instant::now() + Duration::from_secs(5);
+	loop {
+		if fakes.lock().unwrap().rings.len() >= n {
+			return;
+		}
+		assert!(std::time::Instant::now() < deadline, "ring not received");
+		tokio::time::sleep(Duration::from_millis(10)).await;
+	}
+}
+
+#[tokio::test(flavor = "multi_thread")]
+async fn completed_run_rings_harness_with_its_own_session_and_run() {
+	let fx = fixture("allow", driver_ok(), fast());
+	let rid = started(&fx, "hi").await;
+	wait_phase(&fx.agent, "s1", &rid, "completed").await;
+	wait_rings(&fx.fakes, 1).await;
+	let rings = fx.fakes.lock().unwrap().rings.clone();
+	assert_eq!(rings.len(), 1);
+	assert_eq!(rings[0]["op"], "ring");
+	assert_eq!(rings[0]["session"], "s1");
+	assert_eq!(rings[0]["run"], rid);
+}
+
+#[tokio::test(flavor = "multi_thread")]
+async fn failed_run_rings_harness_with_its_own_session_and_run() {
+	// A "deny" policy fails the driver's tool call directly, no approval wait.
+	let fx = fixture("deny", driver_tool(1, false), fast());
+	let rid = started(&fx, "hi").await;
+	wait_phase(&fx.agent, "s1", &rid, "failed").await;
+	wait_rings(&fx.fakes, 1).await;
+	let rings = fx.fakes.lock().unwrap().rings.clone();
+	assert_eq!(rings.len(), 1);
+	assert_eq!(rings[0]["op"], "ring");
+	assert_eq!(rings[0]["session"], "s1");
+	assert_eq!(rings[0]["run"], rid);
+}
+
+#[tokio::test(flavor = "multi_thread")]
+async fn ring_error_leaves_run_terminal_and_its_done_event_unchanged() {
+	let fx = fixture("allow", driver_ok(), fast());
+	fx.fakes.lock().unwrap().ring_error = true;
+	let rid = started(&fx, "hi").await;
+	wait_phase(&fx.agent, "s1", &rid, "completed").await;
+	// The done event, emitted before the sweep, carries the normal summary.
+	let mut events = Vec::new();
+	while let Ok(event) = fx.rx.try_recv() {
+		events.push(event);
+	}
+	let done = events
+		.into_iter()
+		.find(|e| e["kind"] == "done")
+		.expect("done event");
+	assert_eq!(done["run"], rid);
+	assert_eq!(done["phase"], "completed");
+	assert!(done["error"].is_null());
+	// The failed sweep is observed, and the run stays completed regardless.
+	wait_rings(&fx.fakes, 1).await;
+	let status = fx
+		.agent
+		.status(&json!({"session":"s1","run":rid}))
+		.await
+		.unwrap();
+	assert_eq!(status["phase"], "completed");
+	assert!(status["checkpoint_error"].is_null());
+}
```

2. Run the Verify blocks below from the repo root (`agent.ctg`).

`just check agent` and `just test agent`, run from `/Users/feb/dev/cartridge`
after this PRD integrates, are the coordinator's post-integration
confirmation named in the PRD's Acceptance box 4. They run from the
superproject, not this repo's root, so they are not a Verify block here
(the engine runs every block's paths relative to *this* repo's root and
never `cd`s to another checkout) — they are follow-up, not part of this
spec's proof.

## Acceptance

- [x] After a run reaches `completed`, the `harness` ring call it issues
      carries that run's `session` and `run` ids
      (`run_state::completed_run_rings_harness_with_its_own_session_and_run`).
- [x] The same holds for a run that ends `failed`
      (`run_state::failed_run_rings_harness_with_its_own_session_and_run`).
- [x] A ring call that returns an error leaves the run terminal and its
      `done`/`error` event emitted unchanged
      (`run_state::ring_error_leaves_run_terminal_and_its_done_event_unchanged`).
- [x] `cargo clippy --all-targets -- -D warnings` and
      `cargo fmt --all -- --check` pass.

## Verify and Proof

Prototyped in a throwaway archive of `620857d` under `$TMPDIR` (never in the
live `agent.ctg`), with `CARGO_TARGET_DIR` isolated under `$TMPDIR` and every
`cargo` invocation run as `env -u CARTRIDGE_YOLO ...`.

Red (same test file, unmodified `src/lib.rs`, `cargo test --lib -- ring`,
`--test-threads=1`): 2 passed, 2 failed —

```
test run_state::completed_run_rings_harness_with_its_own_session_and_run ... FAILED
  left: Null
 right: "s1"
test run_state::failed_run_rings_harness_with_its_own_session_and_run ... FAILED
  left: Null
 right: "s1"
test run_state::ring_error_leaves_run_terminal_and_its_done_event_unchanged ... ok
```

(`ring_error_leaves_run_terminal_and_its_done_event_unchanged` is a
preservation check — it holds before the fix too, since nothing before this
PRD lets a ring error touch terminal state; the other two are the actual red
lines the fix must turn green.)

Green (same test file, patched `src/lib.rs`, full `cargo test --lib`,
`--test-threads=1`): `test result: ok. 24 passed; 0 failed; 0 ignored; 0
measured; 0 filtered out` — every pre-existing test still passes alongside
the three new ones.

`env -u CARTRIDGE_YOLO cargo clippy --all-targets -- -D warnings`: exit 0, no
warnings. `env -u CARTRIDGE_YOLO cargo fmt --all -- --check`: exit 0, no
diff.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/the-turn-end-ring-verify}"
env -u CARTRIDGE_YOLO cargo clippy --all-targets -- -D warnings
env -u CARTRIDGE_YOLO cargo fmt --all -- --check
```

```test
run: env -u CARTRIDGE_YOLO env CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/the-turn-end-ring-verify}" cargo test --lib -p agent
pass: run_state::completed_run_rings_harness_with_its_own_session_and_run
pass: run_state::failed_run_rings_harness_with_its_own_session_and_run
pass: run_state::ring_error_leaves_run_terminal_and_its_done_event_unchanged
```
