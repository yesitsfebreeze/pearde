---
complexity: small
footprint:
  - .cartridge/tests/unit/run_state.rs
---

# spec01 — pin that agent runs key by session, so two attached instances never collide

Base: agent.ctg `4e544f2` ("Give the loop tests their own CARTRIDGE_HOME").

## Option chosen

**No production change. Add the regression test that the outcome is missing.**

The PRD's `What changes` assumes agent's single-flight guard is "global in the
node". It is not. Traced end to end:

- The guard is `Agent.runs: Mutex<HashMap<String, Arc<Control>>>`
  (`src/lib.rs:169`), keyed by **session id**. `start` refuses with
  `run_active` only when *that same session* already holds an unfinished
  control (`src/lib.rs:283-291`). Two different sessions never contend.
- Every other op resolves through `Agent::control` (`src/lib.rs:339-357`),
  which looks the control up by `args["session"]` and then requires
  `args["run"]` to equal that control's own snapshot run, else `run mismatch`.
  `status`, `answer`, `cancel` all route through it. There is no ambient
  "current run".
- The transcript is not agent state at all: `Run::save` checkpoints through
  `sessions` with `{"op":"checkpoint","id": self.session, ...}` and an
  `expected_revision` CAS (`src/lib.rs:525-546`). The run id is derived from
  the session's own revision, `format!("{id}:{revision+1}")`
  (`src/lib.rs:293-300`). `Run::new` even takes `cwd` from the session record
  (`src/lib.rs:489`), never from the node's process.
- agent.ctg holds no per-process ambient state that an instance could collide
  on: `module.rs` keeps one `AGENT` (`src/module.rs:23`), one relay `PIPE`
  (`:24`) and a `PENDING` ask map keyed by an `AtomicU64` per call (`:25-27`).
  It spawns no process (`grep -rn 'Command::new|std::process' src/` → no hits).

So the session **is** the per-instance key. What the audit actually caught was
a *many-node* symptom, and it is fixed by the parent's host-attach child (done,
`an-instance-attaches-to-the-daemon-and-never-composes-silently`): with N agent
nodes, each node's `Agent::recover` (`src/lib.rs:219-237`) ran at start and
checkpointed every unfinished session to `interrupted`, clobbering the other
host's live run, and the guard of node A could not see node B's run. One node
removes both. Introducing an instance id above the session would be a second
name for the same thing — rejected.

The one real gap is proof: the existing
`concurrent_starts_produce_one_run_one_error_one_checkpoint_pair`
(`.cartridge/tests/unit/run_state.rs:293`) starts twice on **one** session and
asserts the *refusal*. Nothing pins that two sessions run at once, so a later
change to a node-wide lock would pass the suite. This spec pins it.

## Steps

1. `.cartridge/tests/unit/run_state.rs`: append
   `two_sessions_hold_concurrent_runs_with_separate_transcripts`
   (`#[tokio::test(flavor = "multi_thread")]`), reusing the file's existing
   `Fakes`, `call_fn`, `fast`, `wait_phase` and `count_kind` helpers. Prototype
   in `attempt-1.patch`, which passes unmodified against `src/`:
   - A driver that idles until an `AtomicBool` is released **or**
     `run.cancelled()`, so both runs stay live at the same time. (The existing
     `Notify` gate cannot be reused: a cancelled run would never wake, and
     `notify_waiters` races a re-created `notified()` future.)
   - `tokio::join!` a `start` on `s1` and on `s2`; bind both `json!` values to
     `let`s first (the macro temporaries are dropped inside `join!` otherwise).
     Assert both are `Ok`, runs `s1:1` and `s2:1` — neither refused.
   - `wait_phase` both to `running`: two active runs in one node.
   - Cross-keying: `status({"session":"s1","run":"s2:1"})` and its mirror both
     error `run mismatch`.
   - `cancel` s1 only; s1 reaches `cancelled` while s2 is still `running`.
   - Release; s2 reaches `completed`. Each transcript holds only its own
     prompt, exactly one `run_started` and one `run_finished`.
2. Nothing else. No change under `src/`. If a step wants to touch `src/`, stop
   and report: the behaviour is already correct and the diff would be churn.

## Acceptance

- [x] Two attached instances can each hold one active agent run
      simultaneously; neither is refused by the other's single-flight guard.
      (Two sessions both reach `running`, both `start`s return `Ok`.)
- [x] One instance resuming its run never reads or writes the other's
      transcript or session. (Cross-session `status` errors `run mismatch`;
      cancelling one leaves the other running; each transcript holds only its
      own prompt and exactly one `run_started`/`run_finished`.)
- [x] agent.ctg's share of "exactly one agent node exists with the daemon
      running": the cartridge starts no host, node or child process of its own,
      checked below. The daemon-wide count is not observable from this repo and
      is delivered by
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` (done)
      and re-proven composed by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.
      agent.ctg's own contribution is that it starts no host or node of its
      own, checked below.

## Verify and Proof

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/agent-runs-key-verify}"
cargo test --lib run_state
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/agent-runs-key-verify}"
cargo clippy --all-targets
cargo fmt --check
```

```sh
# The new test must exist and must drive two distinct sessions, not one.
grep -q 'two_sessions_hold_concurrent_runs_with_separate_transcripts' .cartridge/tests/unit/run_state.rs
grep -q '"session":"s2"' .cartridge/tests/unit/run_state.rs
# The run key stays the session id: no node-wide single-run lock.
grep -q 'runs: Mutex<HashMap<String, Arc<Control>>>' src/lib.rs
# agent.ctg starts no host, node or child process of its own.
! grep -rn 'Command::new\|std::process\|cartridge daemon' src/
```

## Remaining risk

- Two instances that deliberately pass the **same** session id still get
  `run_active` for the second. That is the intended single-flight, not a
  regression: one session has one transcript.
- Distinct session ids for concurrent `start`s with no `session` argument come
  from `sessions {"op":"create"}`; that uniqueness is owned by
  `sessions-runs-once-in-the-daemon-with-one-buffer-id-space`.
- `agent.event` is emitted node-wide (`src/lib.rs:549-556`), so every attached
  instance sees every run's events. Each carries `session` and `run`, so a
  subscriber filters, and it is not a transcript read. Narrowing delivery to
  the owning instance is host event routing in cartridge.ctg — out of this
  footprint; handed to the parent.
- `Agent.runs` never drops finished controls, so one long-lived daemon keeps
  one small entry per session ever started. Deliberate: `status` serves
  `checkpoint_error` from that entry and it exists nowhere else. Add pruning
  only if a daemon's run map is ever measured as a problem.
