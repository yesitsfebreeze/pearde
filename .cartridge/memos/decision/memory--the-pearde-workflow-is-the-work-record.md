---
kind: decision
date: 2026-09-08
status: superseded
description: pearde's board, nine states and pass project onto the record with no new kind and no new state word — a work memo is the PRD, its `## Check` the spec, seven derived bands are the states, `memory plan` is the scan, and [[@prd/routine/run-board.md]] is the pass
read_when: "asking where a pearde word lands in memory, running the plan, or adding a state the board seems to lack"
---

# the-pearde-workflow-is-the-work-record

Raised by the user 2026-09-08: "a full workflow port with the current memo
system of memory of the pearde tool — not a straight copy, but routines, tools,
types and everything needed to project the workflow we had in PRD onto the
system we are running". Extends [[@prd/decision/memory--the-plan-is-a-gantt.md]], which ported the
timeline and left the loop, the scan and the states unported.

This records a superseded design. Current planning is owned by the native PRD cartridge; source cartridges no longer provide a scheduler or planning loop.

## Decision

**Every pearde thing already has a memory name, and the port is the table
that says which.** Nothing is added to the kind vocabulary and nothing to
`status:`; what pearde carried as nine written states the record derives on
every read, so a state can never be stale.

| pearde | memory |
|---|---|
| the board, `.pearde/prds/` | `memos/work/`, every `kind: work` memo |
| a PRD, `prd.md`, the request as a contract | a work memo — `## Do` is the contract: what exists when done, never how |
| a spec, `specs/specNN.md`, boxes an implementer ticks | the memo's `## Spec` (the how) and `## Check` (the boxes and the verify block), both the analyst's; one memo is one spec, and a memo holding more carries `subwork:` children at level 10 ([[@prd/note/memory--work-memo.md]]) |
| `vision.md`, `terminals:` | [[@prd/work/memory--the-vision.md]], level 1; its `subwork:` are the terminals |
| `state: open` | `status: open`, no `claim:` |
| `analyzing`, `claimed` — a worker holds it | a `claim: <who> <stamp>` line, whatever `status:` says; `analyzing` when the memo has no `## Spec` yet |
| `specced` — ready to implement | open with `## Spec` and `## Check` |
| `refine` — needs a split | open with no `## Spec`: the `spec` band, and the analyst writes the Spec, the children, or the question |
| `question` — waits on a person | open, `needs:` a `kind: question` memo still holding `A: ?` — the `asking` band |
| `blocked` — waits on a named event | `status: blocked` |
| `failed` — the attempt did not produce the work | open again, the failure written as its first question ([[@prd/routine/run-board.md]] step 6) — so red is `asking` too |
| `done` | `status: done`, only when the Check passed |
| `claim`, `release`, `retry` | the `claim:` line, written and struck through `memo write` |
| `collect` | [[@prd/routine/run-board.md]] steps 6 and 7: run the Check literally, `just land` |
| `sweep`, `claim-ttl` | a claim older than a day whose lane holds no new commit is struck by the pass |
| a memo, `.pearde/memos/` | `kind: decision` |
| a workflow and its atomics | `kind: routine` |
| a persona | `kind: persona` |
| `complexity`, weight | `estimate:` in hours — memory settled on time, not weight |
| `footprint` | nothing — every memo runs in its own lane and git merges the files |
| `.state/pass.md` | `memos/dashboards/work-checkpoint.md`, maintained by [[@prd/routine/run-board.md]] and session handoffs |
| `pearde scan`, the progress line | the `plan` operation: `memory plan`, `mcp__memory__plan`, one call for the whole board |
| the dispatcher and `pearde-pass` | [[@prd/routine/run-board.md]], which dispatches one agent per ready memo, each in its lane |
| `pearde-analyst`, `pearde-implementer` | `memory-analyst`, `memory-implementer` in `.claude/agents/` — the analyst probes and writes Spec and Check, the implementer runs the Spec and ticks the boxes, and neither thinks past its brief |

**Seven bands, in pressure order**, replace the six of [[@prd/decision/memory--the-plan-is-a-gantt.md]]:
`spec`, `asking`, `blocked`, `claimed`, `ready`, `later`, `done`. `asking` is
pearde's "waiting on you" — the one band only a person moves — and it is
derived from a `needs:` link to an unanswered question memo, so answering the
question is what releases the work, the same way it did on the board.

## Why

Pearde's states were written because its tools had nothing else to read; the
record has a Check, a claim line, a needs line and a question kind, and the
band is a function of those four. Writing a tenth word would make two
registers say one thing ([[one-vocabulary-not-two]]). Footprints and the
worker cap are dropped because a lane per memo and an unlimited-hands
schedule make them nothing; `complexity` is dropped because the user asked
for time. What pearde had that the record lacked was the scan — the board on
one page, read through the tool, never by walking files — and the pass that
reads it; both are ported as one operation and one routine rather than as
twenty Python commands, because every transition the commands guarded is a
one-line front matter edit here, and the gate on it is the Check.

## Consequences

- Revised 2026-09-09: `## Do` had drifted into the how, and the requester was
  writing the Check. The section split is now three authors — asker, analyst,
  hand — and the `spec` band dispatches an analyst instead of a drill.

- A work memo waiting on a question links it in `needs:`; a question memo
  answered in full stops holding the memo without any edit to the memo.
- A claim with no lane commit for a day is a stale claim; the pass strikes it
  and says so.
- `memory plan` is the read and moves nothing; [[@prd/routine/run-board.md]] is the move.
  No command both reads the board and moves it.
