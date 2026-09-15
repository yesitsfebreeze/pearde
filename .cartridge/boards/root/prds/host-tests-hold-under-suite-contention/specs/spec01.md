---
complexity: small
footprint:
  - cartridge.ctg/src/host/socket.rs
  - cartridge.ctg/.cartridge/tests/unit/src/cli/setup.rs
---

# spec01 — Unblock the check gate and stop one failing test poisoning two others

## Evidence (2026-09-15, HEAD f8a2c00, from /Users/feb/dev/cartridge)

`just check cartridge`: exit 1. `cargo fmt --all --check` fails on an
uncommitted, unformatted debug block in `src/host/socket.rs` (`git status`
shows only this file modified, 6 insertions):

```
--- a/src/host/socket.rs
+++ b/src/host/socket.rs
@@ pub(crate) async fn listen(...) {
+	eprintln!(
+		"[listen-debug] {:?}: exists={} dirs={:?}", ...
+	);
```
This is live scratch instrumentation (its exact text changed twice while this
investigation ran, confirming another session is editing it right now to
diagnose the failures below — see PRD Result). It is not committed at
f8a2c00.

`just test cartridge` (`cargo test --workspace`): exit 1, 163 tests, 3 failed
(11/14 pass in the `main.rs` binary; all 152 `lib.rs` tests pass):

1. `cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask`
   panics at `.cartridge/tests/unit/src/cli/setup.rs:180:46`:
   `Result::unwrap() on Err(Remote("/tmp/cartridge-501/c169a3a06900/host.sock is already served"))`.
   The live debug output shows the run directory going from empty to
   `["94648"]` to `["94648", "host.sock"]` across two `listen()` calls for the
   same descriptor within the one test (setup phase, then `doctor()`
   phase) — the second `listen()` hits the `BindOutcome::AlreadyRunning`
   branch in `src/host/socket.rs` (the `match` in `listen()`, right after the
   debug block) instead of reusing or waiting for the first. This is the "four
   CLI failures" the PRD's Result section says the host-owning session already
   has a diagnosis for; do not re-derive a fix here — land theirs.
2. `cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds` and
3. `cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither`
   both panic at `.cartridge/tests/unit/src/cli/setup.rs:7:18`:
   `Result::unwrap() on Err(PoisonError { .. })`. `trust_home()`
   (`setup.rs:5-8`) is a single process-wide `static Mutex<()>` that every
   `CARTRIDGE_HOME`-touching test takes a turn on (grep confirms
   `std::env::set_var("CARTRIDGE_HOME", ...)` at `setup.rs:99,213,243`,
   `trust.rs:10`, `tests/mod.rs:22`, `settings.rs:106,115` — all cooperative,
   process-global mutation, exactly what Acceptance box 2 calls out). Failure
   #1 above panics while holding that mutex's guard (`_turn` in
   `setup.rs:97`), poisoning it, so every later test that calls `trust_home()`
   fails immediately — these two failures are downstream noise from #1, not
   independent bugs.

## Acceptance

- [ ] `cargo fmt --all --check` (run via `just check cartridge` from
  `/Users/feb/dev/cartridge`) exits 0: the uncommitted debug block in
  `src/host/socket.rs` is gone or reformatted, and no other diff remains
  beyond what is already committed at the revision this runs against.
- [ ] `just check cartridge` exits 0 from `/Users/feb/dev/cartridge`
  (clippy and fmt both clean).
- [ ] A test that panics while holding `trust_home()`'s guard no longer fails
  unrelated tests: `TURNS.lock().unwrap()` at
  `.cartridge/tests/unit/src/cli/setup.rs:7` recovers a poisoned lock (e.g.
  `.unwrap_or_else(std::sync::PoisonError::into_inner)`) instead of
  propagating `PoisonError` to the next test that takes a turn.
- [ ] `just test cartridge` exits 0 from `/Users/feb/dev/cartridge`, three
  consecutive runs, with the suite in parallel (default `cargo test`
  threading — no `--test-threads=1` added).
- [ ] `cli::setup` and `cli::trust` tests all pass in that run, including
  `setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask`
  (the real `host.sock already served` collision, item 1 above — this box can
  only be ticked once the host-owning session's fix for the socket collision
  in `src/host/socket.rs`'s `listen()` lands; this spec does not prescribe
  that fix).

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge
git -C cartridge.ctg status --porcelain   # expect clean or only intended edits
just check cartridge                       # expect exit 0
just test cartridge                        # expect exit 0
just test cartridge                        # 2nd consecutive run, exit 0
just test cartridge                        # 3rd consecutive run, exit 0
grep -rn "set_var(\"CARTRIDGE_HOME\"" cartridge.ctg/.cartridge/tests
  # confirm every call sites still route through trust_home()/an equivalent
  # single-writer guard; none run un-guarded.
```

Do not stop or kill any running `cartridge node`/host process while probing
this — several belong to other sessions on this machine (confirmed via `ps
aux`, 10:23-10:53AM entries under `agent.ctg`/other cartridges).
