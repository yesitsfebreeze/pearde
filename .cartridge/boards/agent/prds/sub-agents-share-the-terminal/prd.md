---
repo: /Users/feb/dev/cartridge/agent.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
superseded-by: "@root/the-orchestrator-sees-and-talks-to-its-workers"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: sub-agents-share-the-terminal
---

# sub-agents-share-the-terminal

The agent spawns sub-agents that report back through a mailbox, the terminal view shows and switches between them, and the visible shell stays owned. Per decision `the-agent-surface-preserves-the-visible-shell`, collaboration is exposed through discoverable declared events, never hidden execution tools. This parent coordinates the children; it is not implementation work.

## Acceptance

- [ ] Each linked child passes its own review and acceptance.
- [ ] Integration: in a disposable profile a parent spawns two children that run concurrently, a child's shell request routes through the parent's PTY input lease, the panel switches between them, and both reports land in the parent transcript; the user's PTY and editor stay intact.
- [ ] Two children editing one workspace are serialized by their owner, or the gap is recorded as a named limitation with its reproducing fixture.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [sub-agent-sessions-record-parent-and-mailbox](../../../sessions/prds/sub-agent-sessions-record-parent-and-mailbox/prd.md) — done
- [the-agent-spawns-wakes-and-owns-sub-agents](../the-agent-spawns-wakes-and-owns-sub-agents/prd.md) — carries the `@pty/improve-pty-input-ownership` lease prerequisite
- [the-panel-switches-to-a-sub-agent](../../../ui/prds/the-panel-switches-to-a-sub-agent/prd.md) — `ui` board, source now `tui.ctg`
- [the-swarm-talks-on-a-board](../../../sessions/prds/the-swarm-talks-on-a-board/prd.md)
- [the-run-is-a-stream-of-typed-events](../the-run-is-a-stream-of-typed-events/prd.md)

## Integration gate

After the children pass and the agent is ported to declared events (no PRD yet), from `/Users/feb/dev/cartridge`: `just test agent`, `just test sessions`, `just test tui`, `just smoke`. Not run for this plan.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).

## From the retired work memo

Folded 2026-09-15 from `work/sub-agents-share-the-terminal.md` (status open). The PRD state above is authoritative.

> The agent spawns sub-agents that report back through a mailbox, and the agent view shows and switches between them

### Outcome

The agent can spawn a sub-agent for a task, send it messages, and be told what
it found. A sub-agent is a session in the same agent process with a parent
recorded on it; it retrieves context through memos and has no implicit shell ownership, because
the visible shell is shared with the user and the root agent. File operations
still go through the visible shell: a child sends an execution request to its
owner, who serializes it and returns attributable readback. No hidden file tool
or per-child PTY is introduced. Messages travel through a mailbox
on the sessions cartridge: the user is a sender like any other, so the composer
and the agent use the same path, and a message to an idle agent wakes it.

The full agent view shows them: a panel lists every live sub-agent with what it is doing
and how long it has been at it, and opening one switches the transcript and
composer to it. Messages appear in both transcripts, naming who sent them.
The gutter's agent column shows the root agent's state; a working sub-agent is
visible there too, so the user knows work is in flight without opening the
full transcript.

### Check

- [ ] Every child listed in `subwork:` is done with recorded evidence.

### Approach

Confirm the agent cartridge runs sessions concurrently before anything else;
if it does not, that is this memo's first commit. Expose `spawn`, `send`, `wait` and `peek` as discoverable session services
invoked through the existing shell and explained by memos. The default model
interface remains `shell` and `memo`. Nothing here spawns a shell, a PTY or a multiplexer
([[the-agent-surface-preserves-the-visible-shell]]). Concurrent edits between sub-agents are a
known hazard and out of scope; a worktree per sub-agent is the answer if it
bites.

Surface amendment, 2026-09-12: collaboration remains wanted. The dependency
on the historically named sidebar work now means the composer/full-transcript
integration, not a left sidebar. Gutter indicators supplement the latest-tool
footer and status; no child output is painted into the foreground editor.
