---
kind: routine
description: Run one selected native work memo through a bounded MCP PeaRDe-style pass with analyst, implementer and verifier sub-agents
uses:
  - usage: "[[run-usage]]"
    when: [running a work pass, orchestrating work memos with sub-agents, using PeaRDe for native work, selecting work versus a PRD board]
    tags: [work, PeaRDe, sub-agents]
---

# Work pass

## Inputs

One explicitly selected native `work/<name>.md`, or a named scope from which the
caller selects one leaf; the current MCP connection; host collaboration tools;
and a coordinator session ID. Read `type/work.md`, `type/routine.md` and
[[@prd/routine/plan-cartridge-work.md]]. This is an agent-executed pass, not a scheduler or a new
MCP operation. A native memo pass and the central PRD board have separate
state authorities; a PRD scan does not enumerate native work or authorize it.

## Do

1. Discover before acting: call memo `landscape` with the named scope, then
   `{"op":"resolve","usage":"run","query":"work pass PeaRDe sub-agents","limit":20}`,
   and `read` the selected paths and applicable instructions. For native inventory,
   call `{"op":"list","kind":"work"}` and follow its returned pagination cursor
   until the selected scope is accounted for. Ranked search limits never prove
   exhaustion. Use the native PRD service only for explicitly selected PRDs; preserve its
   recorded transitions and owner. Continuous board orchestration follows
   [[@prd/routine/run-board.md]].
2. Re-read the selected memo, its revision, `owner`, any legacy `claim`, `needs`,
   `subwork`, linked review history and prior pass checkpoint. Walk prerequisites:
   work must be `done`, questions `answered`, decisions `accepted`; read their
   type declarations when needed. Missing targets, malformed links, unknown
   kinds/statuses, cycles or failed prerequisites prevent dependent dispatch.
   A parent with subwork is a roll-up, not an implementation leaf. Another active
   owner or unresolved claim prevents taking work; age alone never clears it.
   New dispatch requires an unowned `open` leaf. Leave `done`/`cancelled` untouched.
   A `blocked` leaf requires evidence its named Blocker cleared and coordinator
   reopening before dispatch. An `active` leaf may only resume this pass's prior
   attempt after reconciling its effects; never take foreign active ownership or
   an unresolved legacy claim.
3. Save a bounded session-specific checkpoint as a linked `kind: note` through
   validated memo writes. Include canonical work path and revisions, owner repo
   and base, review identity/rounds, dependencies, exact allowed footprint,
   worker IDs/roles and attempt paths, deadline, observed checks, publication or
   integration revisions, uncertain effects and next action. Keep one current
   checkpoint with evidence links rather than copying the entire inventory.
   The coordinator alone writes live records, statuses, checked boxes and owner.
   Use the latest read `expected_revision` for existing memos, preserve pre-write
   bodies/revisions, and read back every successful write. These guards and claims
   are advisory; they do not provide distributed exclusion or an atomic multi-file
   transaction. Recheck a new path and workspace-unique leaf immediately before
   creation; shipped documents retain their separate `@cartridge/kind/name.md`
   identities. if it exists, reconcile it. Absence still leaves a creation race.
4. If Outcome/Approach/Check is incomplete, dispatch one analyst using
   [[@prd/routine/spec-a-work-memo.md]]. Its `SPECCED`, `SPLIT` or `QUESTION` is a report verdict,
   never a native status. Validate its proposals and publish prerequisites before
   dependents. A split or unresolved question ends this leaf's implementation
   dispatch; record the next selected step without silently widening this pass.
5. Before implementation, apply [[@prd/routine/plan-cartridge-work.md]] to the exact substantive
   revision and material inputs with an independent reviewer. Preserve the five-round
   history across retries/splits; require an attributed agent score of at least
   90/100 and no blockers under the current delegated-rating policy. The user's
   instruction "i dont rate, you do" replaces the old numeric user-rating gate.
   Record that instruction, agent score and actual user feedback separately;
   never request or invent a user number. Honor any later explicit user revision
   to this policy without rewriting historical attribution. Missing required,
   rejected, exhausted or stale review prevents implementation. Ownership-only
   changes may retain review with a recorded diff showing unchanged contract.
6. Immediately before dispatch, recheck readiness, ownership, revision and shared
   footprints. Use only available host tools: `spawn_agent` for a bounded brief,
   `send_message` for progress, `followup_task` for an idle agent's next bounded
   task, `list_agents`/`wait_agent` for collection and `interrupt_agent` for stopping.
   Inspect host capacity and live agents; reserve the coordinator slot and never
   exceed remaining capacity. Sequence roles when necessary; the verifier must be
   distinct from the implementer. No worker may delegate further without an assigned
   slot and scope. Missing required host capabilities is an explicit limitation,
   not permission to invent a kern/lane API or claim independent verification.
7. Every brief names role, canonical memo and revision, exact allowed paths,
   relevant context, prerequisite/review evidence, cwd and actual acceptance
   commands, attempt/draft directory, report path and finite deadline. Default
   worker budget is 20 minutes with at most one additional 10-minute extension
   based on observed progress; record any different finite budget before dispatch.
   Permit concurrent workers only for independent disjoint footprints; this pass
   normally sequences analysis, implementation and verification on one leaf.
8. For code, identify the owning Git repository and approved target/base revision;
   inspect `git status --short` and `git rev-parse HEAD`. Reuse a verified isolated
   attempt with its required dependency commits, or create a clean worktree with
   `git -C <owner> worktree add -b <unique-branch> <attempt-path> <verified-revision>`.
   Never assume `main`, discard another actor's changes, or copy an unrelated dirty
   tree. For records, assign draft/report paths; workers do not need a code checkout
   and do not publish memos. Before implementation, coordinator records `active`
   with this pass's owner and dispatches [[@prd/routine/implement-a-work-memo.md]]. `DONE`, `FAILED`
   and `BLOCKED` are report verdicts, not memo statuses or proof of collection.
9. Collect the report and inspect actual artifacts/check output. Stop on footprint
   drift, stale inputs or unknown effects. Independently verify the resulting
   revision using a separate agent; then collect serially through
   [[@prd/routine/land-a-worked-lane.md]]. For records, publish supporting ingredients before their
   coordinator and independently verify final MCP readback/discovery. For code,
   verify both the attempt and the actual combined target. Only the coordinator
   marks `done` after every observable Check and child prerequisite passes,
   records Result/evidence and removes only its own ownership. Saved drafts,
   published memos and landed code are distinct outcomes. End after this memo;
   do not start unrelated standing routines or dispatch newly unblocked work.

## Check

Read back the selected memo and checkpoint. Every checked box has observed
evidence at the actual resulting revision; independent verification and applicable
combined checks passed before `done`. Live native statuses remain exactly
`open`, `active`, `blocked`, `done`, `cancelled`. Workers supplied bounded reports;
the coordinator published state. Every child finished or was confirmed stopped
before a normal return, with no uncollected mutations or unrelated scope included.

When verifying this routine, separately label executed MCP reads/writes and
procedure walkthroughs. Walk ready and unspecced leaves, another owner's claim,
missing/failed prerequisites, missing required review versus explicit delegation,
overlapping footprints, failed checks, stale writes/new-path races, interrupted
resume and cancellation. A walkthrough does not prove an autonomous scheduler.

## Failure

Wait in intervals no longer than 60 seconds, inspect progress and communicate.
At the finite deadline, stop dispatch/publication, request interruption of this
pass's children and allow at most 60 seconds to confirm stopped/finished status.
An interrupt request alone is not confirmation. Preserve draft/worktree/report
paths, checkpoint IDs and uncertain side effects. If the host cannot confirm
termination, report a blocked supervision handoff with the unresolved IDs; retain
ownership and do not claim a normal completed pass, retry or publish their output.
This is a finite exception report, not an endless wait or invented worker death.

User cancellation immediately stops new dispatch and publication, requests the
same bounded shutdown and checkpoints known/unknown effects. Cancelling only
the pass leaves the wanted outcome `open` once its workers are confirmed stopped
and this pass's ownership can safely end. Use `cancelled` with a Result reason
only when the user cancels the outcome itself. Preserve other owners and claims.

For an ordinary failed check, retain evidence and leave wanted work `open` after
ending this pass's ownership; use `blocked` only with a named Blocker and what
clears it. On restart, re-read live revisions, inspect artifacts and worker state,
and determine whether each recorded mutation occurred before choosing the next
step. Never blindly replay a failed/uncertain write, commit or integration.
Stale revision stops publication for reconciliation. Partial publication stays
recorded per document; rollback only this pass's changes after checking for
concurrent edits and using current revision guards. No routine grants extra
permission or requires unavailable lane recipes.
