---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/agent.ctg"
capability-owner: agent
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/"
- ".cartridge/tests/unit/run_state.rs"
commit: "f7c38fe778ec79c10323c526c510ef123dfecfd8"
---

# Agent runs key per attached instance, not per process

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies agent runs as
per-instance state: agent's single-flight guard only works inside one
process, so two hosts can drive one session and overwrite its transcript.
Under the one daemon, two attached instances must be able to drive two runs
of their own without the in-node guard serializing them into one session.

## Outcome

Agent runs in the one node are keyed by attached instance: an instance's run
references its own session and transcript, single-flight applies per
instance, and two instances never overwrite one transcript.

## What changes

The audit's premise was that agent's single-flight guard is node-wide. Analysis
on 2026-09-16 (analyst-1) shows it never was: `Agent.runs` (`src/lib.rs:169`) is
keyed by session id, `start` refuses `run_active` only for that same session
(`src/lib.rs:283-291`), every other op resolves by session through
`Agent::control` (`src/lib.rs:339-357`), and the transcript is checkpointed
through `sessions` under an `expected_revision` CAS (`src/lib.rs:525-546`), not
held in the node. The session already is the per-instance key.

What the audit really caught is a many-*node* symptom: each node's
`Agent::recover` (`src/lib.rs:219-237`) checkpoints every unfinished session to
`interrupted` at node start, clobbering another host's live run. One daemon
removes that, and the attach child that delivers it is this PRD's `needs`.

What is missing is the proof. The existing `concurrent_starts_...` test
(`.cartridge/tests/unit/run_state.rs:293`) starts twice on *one* session, so a
regression to a node-wide lock would still pass the suite.

- No production change in `src/`.
- Add the regression test that two sessions hold concurrent runs with separate
  transcripts, pinning the per-session keying against a future node-wide lock.

## Acceptance

- [x] Two attached instances can each hold one active agent run
      simultaneously; neither is refused by the other's single-flight guard.
- [x] One instance resuming its run never reads or writes the other's
      transcript or session.
- [x] agent.ctg's share of "exactly one agent node with the daemon running":
      the cartridge itself starts no host, node or child process, so a second
      node can only come from the host. (The daemon-wide count is the done
      sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently`
      and this PRD's `needs`.)

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1. Two coordinator edits to
this record: the footprint gained `.cartridge/tests/unit/run_state.rs` (this
repo `#[path]`-includes its unit tests from `src/lib.rs:894`, so the only file
the spec changes sat outside the declared `src/` footprint and collect would
have refused it), and acceptance box 3 was narrowed to what agent.ctg can
prove, because the daemon-wide count is not observable from this repo. Handed
up, out of footprint: `agent.event` fans out node-wide (`src/lib.rs:549-556`),
so every attached instance sees every run's events; they carry `{session, run}`
so subscribers filter and no transcript leaks, but narrowing delivery is
cartridge.ctg event routing.
