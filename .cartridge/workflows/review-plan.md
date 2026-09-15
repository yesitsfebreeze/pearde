---
atomic: review-plan
subject: Improve a plan to an agent review score of at least 90 within five rounds
date: 2026-09-13
tags:
  - atomic
---

## Do

Review the selected plan and its specs using the method below before implementation.
This is one bounded review loop, not a new work-state engine. Use the review record
template at `prd.ctg/.cartridge/templates/review.md`; existing PRD transitions still apply.

User requirement, 2026-09-13: "User rating from 0 to 100. Everything below 90 will
fail and you can do up to 5 turns per plan." Scope clarification: "All the open
work items." The user then requested recording this method in the workflow.

Superseding user instruction, 2026-09-13: "i dont rate, you do". Agents perform
the ratings. Use an independent reviewer when sub-agents are available; the
coordinator records its attributed score and resolves findings. Do not request
a numeric user rating or invent one. Preserve the 90/100 threshold, five-round
limit and actual user feedback; ask only for a material unresolved user decision.

User refinement: create small, defined PRDs and split broad work. An executable
PRD owns one observable outcome, one accountable cartridge, hard prerequisites,
three to five acceptance checks, and a concrete proof/recovery boundary. Aim for
150–300 words; split independent outcomes before a leaf exceeds 400 words.
Use the PRD refinement operation for same-board children. Cross-owner leaves live in their
owner boards and are referenced through `needs`. Keep parents as short indexes;
retain detailed evidence in linked source/review records, not pasted text blocks.
Consult [the canonical work map](../boards/root/work-map.json) before creating or claiming
work. Source aliases preserve history and claims; they are not additional tasks.

1. Establish the inventory and current authority. Include open centrally stored PRD for the source owners,
   every board's open PRDs and explicit current work lists; identify claimed/blocked owners
   without reclaiming their work. Distinguish executable leaves, roll-up parents,
   standing visions and historical proposals. Resolve duplicates to a canonical
   owner and record keep, revise, split, merge, rehome or retire recommendations.
   An old open marker does not override current repository instructions.
2. Read the actual plan, dependencies, relevant source and existing evidence.
   Check the current owner boundary, shared footprints, integration order and
   compatibility path. Reproduce suspected defects in disposable fixtures when
   needed; a proposed improvement is not evidence that behavior is absent.
3. Score each plan separately on five dimensions, each 0–20: current user value
   and scope; ownership and reuse; dependencies and implementable slices;
   observable acceptance and baseline evidence; failure, recovery and compatibility.
   Record concrete evidence and deductions, not only a total. Review user-visible
   behavior, authority, cancellation, stale revisions, latency/bounds and test
   validity where relevant. Missing implementation tests are expected in an open
   PRD; its plan must state the necessary proof for the next step.
4. Record the reviewer score and actionable findings. Below 90 is FAIL; do not
   average across plans, relax the threshold, hide blockers, or repeatedly score
   unchanged text until it passes. A reviewer score is not the user's rating or
   measured product quality. A reviewer score at least 90 with no blocking
   finding passes the delegated review gate within the user's authorized scope.
5. Revise failures within the authorized scope, preserving history and claims.
   Make one coherent revision that addresses the findings, then recheck changed
   contracts, links, dependencies and relevant gates. If a change requires a real
   unresolved user choice, prepare the concrete alternatives before asking.
   Rehome/retire recommendations alone do not authorize deleting source or records.
6. Record the agent reviewer's rating against the concrete reviewed revision;
   use an independent agent when available, otherwise identify the self-review.
   Below 90 fails the round; revise and re-review within the remaining allowance.
   At least 90 passes only with no unresolved blocking finding. Incorporate actual
   user feedback when supplied, preserving its provenance; a user score is not
   required. Continue authorized implementation after the gate passes.
7. Count one round per substantive reviewed revision presented for evaluation,
   not per tool call or status update. Preserve the count across sessions and
   feedback. At most five rounds are allowed per plan. After round five fails,
   record exhaustion and unresolved findings; stop automatic revisions for that
   plan. A pending fifth agent review remains pending. Do not reset the allowance by
   renaming, splitting, moving or copying the same scope; children inherit its
   used rounds unless the user explicitly grants a new allowance.
8. Bind evidence to canonical plan identity and content digests for the plan,
   specs and relevant contract/dependency inputs. Agent ratings apply only to the
   reviewed revision. A substantive later change makes acceptance stale and
   requires another available round. Formatting-only changes can preserve the
   prior rating only with a recorded diff showing no semantic change. Preserve
   reviewer/user attribution and historical results; never invent either.

Store one append-only review history per canonical plan. For a PRD use
`prds/<slug>/review.md`; for a record without a PRD directory use a centrally stored linked review note
through that owner's validated writing path. Inventory scorecards reference that
history instead of becoming a second implementation status. Existing
`OPEN-WORK-REVIEW.json` entries are historical round-1 reviewer assessments. Their
old pending-user fields remain historical; apply the delegated review rule to
the current revision, without inventing prior scores or restarting counters.

## Done when

The current substantive revision has agent reviewer score >=90,
no unresolved blocking finding, and a review history using at most five
rounds. Identity, input digests, findings, revisions and validation evidence are
recorded. The plan/specs and their owner/dependency paths agree.

This gate is followed by the worker. Pearde's existing workflow validator checks
library structure; it does not enforce numeric ratings or reviewer provenance.
Do not describe a green `just board-check` as a passed review or product test.

## Fails when

| seen | means | do |
| --- | --- | --- |
| Agent score is below 90, or a blocker remains | The revision fails | Record findings; revise and review within the remaining rounds. |
| Agent review is missing or does not name the reviewed revision | Review is pending | Obtain a revision-bound agent review before dependent implementation. |
| Fifth round fails | This plan exhausted its allowance | Record remaining gaps and stop automatic revisions; leave other plans independent. |
| Accepted substantive inputs changed | The rating is stale | Reassess using the next available round; preserve earlier evidence. |
| Unknown owner, duplicate scope or contradictory current instructions | The proposed plan is not executable as written | Resolve or present the disposition before continuing. |
