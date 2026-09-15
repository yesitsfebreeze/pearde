---
repo: /Users/feb/dev/cartridge/agent.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
superseded-by: "@root/a-worker-launches-in-tmux-through-the-proxy"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: the-agent-spawns-wakes-and-owns-sub-agents
needs:
- '@sessions/sub-agent-sessions-record-parent-and-mailbox'
- '@pty/improve-pty-input-ownership'
footprint:
- /Users/feb/dev/cartridge/agent.ctg/cartridge.json
- /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/help.md
---

# the-agent-spawns-wakes-and-owns-sub-agents

The agent serves sub-agents — sessions in its own process with a recorded parent — through declared spawn, send, wait and peek events documented in its `.cartridge/help.md`. Child identity, parent, launch intent and wake cursor persist before spawn or send is answered. A send to an idle child wakes one run carrying the parked message; wakes coalesce per idle generation and a setting bounds active children. A child's shell request routes to its owner under a PTY input lease. Parent disposal stops admission and reports owned children, killing nothing unrelated.

## Acceptance

- [ ] Spawn, send to an idle child, wake and report: the child's report lands in the parent transcript naming the child.
- [ ] A crash around spawn or wake yields at most one live run per child generation, with replayable mailbox evidence.
- [ ] Two children run concurrently to terminal states with attributed reports; parent restart shows unfinished children as unknown without replaying mutations.
- [ ] A forged owner or session, or a shell request without a current lease, is refused before shell input; an owner-routed request returns attributable readback in the child transcript.

## Proof and recovery

Baseline (agent `fad6d3b`, sessions `e9725e8`): no spawn surface (`agent.ctg/src/lib.rs:235`); one `Control` per session lives in `Agent.runs` (`agent.ctg/src/lib.rs:164`). Sessions already authenticates child lineage and mailbox messages with IDs and sequence (`sessions.ctg/src/mailbox.rs:132-175`). No input lease exists in `pty.ctg/src`, hence the PTY ownership need.

Precondition without a PRD: agent still targets the host API removed in cartridge `ee7e295` (`agent.ctg/src/main.rs:14,42`); no agent gate builds until it is ported to declared events.

First probe: a failing spawn→send→wake test in `run_state.rs` with its sessions fake. Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just test sessions`, `just check agent`. Not run for this plan. Failure: a refused spawn writes no child; an unanswered send wakes nothing; an over-limit spawn is `declined`, never queued silently.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).

## From the retired work memo

Folded 2026-09-15 from `work/the-agent-spawns-wakes-and-owns-sub-agents.md` (status open). The PRD state above is authoritative.

> The agent cartridge spawns, wakes, waits on and owns sub-agents, keeping the visible shell to the owner

### Outcome

The agent cartridge serves sub-agents — sessions in the same agent process with
a parent recorded on them — concurrently, and exposes `spawn`, `send`, `wait`
and `peek` as discoverable session services invoked through the existing shell
and explained by memos. Sending a message into an idle sub-agent's mailbox
wakes a new run whose prompt carries the parked message. The visible shell
stays owned: a sub-agent's file-operation request routes to its owner, who
serializes it and returns attributable readback; an unowned execution is
refused and the user's shell is untouched. The parent records what a child
reports into its own transcript naming the child.

### Check

- [ ] A test spawns a sub-agent session, starts its run, sends it a message,
      wakes a new run with the parked message, and reads the child's report in
      the parent's transcript.
- [ ] Two sub-agent sessions run at once and both reach a terminal state without
      either blocking the other.
- [ ] A sub-agent execution request naming no owner is refused, and the probe
      records that no tool reached the user's shell.
- [ ] A sub-agent's execution request routed to its owner returns attributable
      readback visible in the child's transcript.
