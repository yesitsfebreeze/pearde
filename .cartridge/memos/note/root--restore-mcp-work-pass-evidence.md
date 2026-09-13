---
kind: note
description: Baseline, worker ownership and observed results for the MCP work-pass restoration
uses:
  - usage: "[[read-usage]]"
    when: [resuming the MCP work-pass restoration, checking work-pass implementation evidence]
---

# MCP work-pass restoration evidence

Date: 2026-09-13.
Canonical work: [[@prd/work/root--restore-mcp-work-pass.md]].
Plan revision presented: `89a6dc2e2bf6cd0aeb86ab51f7b16bb93b5eec8bbbd1954056c95a48beed191c`.
Owner repository starting HEAD: `a44b8489f375cf87cebcc14f275fa3355f6a9105`.
This note is a checkpoint and evidence record, not a second task status.

## Observed baseline

- Connected MCP reads of routine/work.md, system/work.md and @memory/system/work.md returned "memo not found".
- MCP reads of the three supporting routines succeed. Their existing lane commands are absent from both current Justfiles.
- MCP type/type.md declares unique memo leaves. The existing type/work.md prevents naming the new routine work.md.
- Root `just board-plan` exited 0 and reported 16 PRDs, with two dispatchable and fourteen gated. This is the separate PRD board, not the 373 native work records returned by the paginated MCP work listing.
- One concurrent MCP read returned "memo record busy: lock acquisition failed because the operation would block; retry after the current operation". A subsequent individual read succeeded. Read contention is not a missing memo and is not permission denial.
- Existing unrelated worktree changes were observed before this pass. No source edits, existing claims or PRD states were changed.

## Base document digests

| Path | SHA-256 |
| --- | --- |
| routine/spec-a-work-memo.md | 3aa35bf1ee0e790adb6e06d9f3e32c4d06a4101690004f9ae33f1b5f85e390c7 |
| routine/implement-a-work-memo.md | 9b95e3a31c05741a4ed0f2ce1e480cfe4cc17b851fb4da7ad957aa7dd13711ec |
| routine/land-a-worked-lane.md | 1cdb3683722caa1c59dab4e6d6891a03a37b3bd2aa8b5d6700ddbdc4226f904e |
| type/work.md | 6539b3f54b1ee04f45e55b7eb3ecf4ea6da6d0f60ae2dc5e12eb08d7fb3054de |
| type/routine.md | 08807a4c813f20dc196c44745547cfe2c2b4288537cca3012858be9c09ed25c5 |
| type/type.md | 2ccec06bed4a2018c626dac20147782dbaee0d0a1fa6fe68e00f59f38a6bba3e |

Complete pre-change Markdown bodies are backed up in `/tmp/cartridge-work-pass.hikK5c/baseline.json`. Temporary artifacts are local to this run; reread live documents if the temporary directory is absent on resume.

## Worker ownership and state

- Coordinator: /root. Sole writer of this pass's live record changes.
- Analyst: /root/workflow_analyst. Finished read-only analysis; recommended four-routine scope and the collision-free work-pass name. No owned branch or source edits.
- Reviewer: /root/workflow_reviewer. Finished independent plan review: 94/100, no blocking findings; exact reviewed revision above. Finished the explicit user-directed review-policy correction review; no blocker.
- Implementer: /root/workflow_implementer, finished. Owns only four drafts and its report under `/tmp/cartridge-work-pass.hikK5c`; no live record writes or code branch.
- Delivery verifier: /root/workflow_verifier, finished independent published MCP reads, discovery and procedure review; PASS.
- This work is active under coordinator owner `/root/restore-mcp-work-pass`.

## User-directed review policy

The user selected "Restore the MCP work coordinator" and said "i dont rate, you do". The 94/100 independent review now passes under explicit delegation; no numeric user rating is invented. The shared review method, implementation gate, workflow step, README and review/PRD templates were aligned with this instruction. The MCP routine/plan-cartridge-work.md was updated by validated write to revision `da4b4b73569055326cb2befd3a767dd04d91e04ed987b19345fca35ce69d4a3c`. These adjacent policy edits are authorized by the user's correction, not a silent expansion of the four-routine implementation.

Root `just board-check` exited 0 after these edits. Its memo/workflow/grammar/scan checks establish board structure only, not agent behavior or completion.

## Publication and independent verification

The coordinator published all four routines, supporting routines first, using validated MCP writes and exact readback. Full before/after publication log: /tmp/cartridge-work-pass.hikK5c/publication.json. Analyst and implementer reports are alongside it. The complete independent verifier report follows; its executed checks and prose scenario walkthroughs remain distinct.

# Independent delivery verification: restore MCP work pass

Verdict: PASS for the four published routines. No delivery blocker found.
Verifier: /root/workflow_verifier, 2026-09-13.
Canonical work read through MCP: work/restore-mcp-work-pass.md, revision
bd2a1f2b225d9479a0ccb9903f1c09b9e05a739b852c2f9a3b946d13601f3510, still active.
Coordinator completion bookkeeping and its final Result/evidence readback remain
pending after this report; this verdict does not claim that later write occurred.

## Executed observations

After the coordinator explicitly notified publication completion, I independently
called mcp__cartridge__memo read on all four routines, their types, the planning
ingredient and relevant usage/dependency types. All reads succeeded. I compared
the full returned MCP text against the final draft files, then independently
checked local live-file SHA-256 against drafts and publication.json. Every text
and digest matched. Each routine has kind routine, declared run usage, and exactly
one Inputs, Do, Check and Failure section. Local comparison/shape assertions exited 0.

| Published path | Final MCP revision / SHA-256 |
| --- | --- |
| routine/spec-a-work-memo.md | 1988695281277d8874a81acd45b389f5fb250a2cba7ed34cfa938920cae46bb6 |
| routine/implement-a-work-memo.md | a5810a349d925892c506162ece53cfa1cb237d446be3632eeb0080d6308f732b |
| routine/land-a-worked-lane.md | abe3aa32e034a0882acdca3bf9c587a82e44dedc7bb5a697cbfbb20d42a7791c |
| routine/work-pass.md | 058beab97d836c672e71c6e158ad044778bcc69e4e3c060f36e8e15440132676 |

Executed resolver request:
`{"op":"resolve","usage":"run","query":"work pass PeaRDe sub-agents","limit":20}`.
The first result was routine/work-pass.md at the revision above, score 30.5.
It returned 20 of 71 ranked matches, more=true, conflicts=[], problems=[].
This establishes discovery; neither the limit nor result count establishes backlog
exhaustion or execution of a routine.

MCP reads and local baseline comparisons confirmed unchanged declarations:

| Path | Revision |
| --- | --- |
| type/work.md | 6539b3f54b1ee04f45e55b7eb3ecf4ea6da6d0f60ae2dc5e12eb08d7fb3054de |
| type/routine.md | 08807a4c813f20dc196c44745547cfe2c2b4288537cca3012858be9c09ed25c5 |
| type/type.md | 2ccec06bed4a2018c626dac20147782dbaee0d0a1fa6fe68e00f59f38a6bba3e |

Additional successful MCP reads: routine/plan-cartridge-work.md
(da4b4b73569055326cb2befd3a767dd04d91e04ed987b19345fca35ce69d4a3c),
usage/run-usage.md, usage/read-usage.md, usage/compose-usage.md,
type/question.md, type/decision.md, type/note.md, and the canonical work/review.
The planning routine's two local method/template references also read successfully.
The four routines' required ingredients and type instructions are available;
the native dependency states agree with their type declarations.

## Procedure walkthroughs — not executed workflow scenarios

These are concrete hypothetical inputs traced through the published prose. No
fixture memo, claim, child dispatch, cancellation, stale write or code integration
was executed by this verifier. PASS below means the instructions prescribe the
required outcome; it does not establish automatic enforcement by a scheduler.

| Scenario/input | Expected path in the published procedure | Result |
| --- | --- | --- |
| Ready leaf: unowned open, complete Outcome/Approach/Check, satisfied needs, current 94 review | work-pass Do 2/5/6/8 rechecks inputs, claims active as coordinator, dispatches bounded implementation, then independent verification/collection before done | PASS |
| Unspecced open leaf has Outcome but incomplete Approach/Check | Do 4 invokes spec analyst; SPECCED is a report followed by validation/review; SPLIT or QUESTION stops this leaf's implementation and records next step | PASS |
| Foreign active owner, or unresolved legacy claim on an open leaf | Do 2/6 prevents taking it; age does not release ownership; no worker or coordinator clears another actor's claim | PASS |
| Selected blocked leaf still names unavailable service | No new dispatch; actual blocker-clearance evidence and coordinator reopening are required | PASS |
| Selected done leaf | Do 2 leaves it untouched; no additional implementation is inferred | PASS |
| Selected cancelled leaf | Do 2 leaves it untouched; no reopening without changed outcome authority | PASS |
| Missing prerequisite target, malformed link, unknown kind/status, cycle, unfinished work, unanswered/cancelled question or superseded decision | Do 2 reads/walks needs and subwork and prevents dependent dispatch; type/question confirms cancellation does not satisfy a dependency | PASS |
| Review absent, stale, rejected, or failed fifth round | Do 5 and plan-cartridge-work prevent implementation; histories/rounds survive splits and retries | PASS |
| No user number, but explicit delegated-rating instruction and current independent 94 with no blocker | Do 5 accepts agent review and preserves attribution; no invented user number or repeated rating request | PASS |
| Two otherwise independent workers both touch the same support routine | Do 6/7 footprint recheck prevents concurrent overlapping assignments; collection is serial | PASS |
| Worker reports DONE but an acceptance read fails | land Do 1/2/3 rejects completion and retains artifacts; ordinary failure returns wanted work open only after safe ownership release | PASS |
| Existing live revision changes between draft and publication | Do 3 and land Do 3 require expected_revision; stale result stops publication and triggers reconciliation | PASS |
| New work-pass path appears after initial absence check | Immediate path/unique-leaf reread requires reconciliation; residual creation race is explicitly acknowledged, never called exclusion | PASS |
| Two supporting files publish, third write fails | Failure and land Failure retain exact per-document state, reread before retry/rollback, and never report atomic four-file success | PASS |
| Interrupted resume finds active owner for this pass, preserved worker IDs and uncertain write | Do 2/3 and Failure inspect worker state, live revisions and artifacts to determine actual effects; no blind mutation replay or invented completion | PASS |
| User cancels pass while child is running, versus cancels desired outcome | Stops dispatch/publication, requests bounded shutdown and preserves effects; confirmed safe pass cancellation returns open, outcome cancellation records cancelled with reason | PASS |
| Worker exceeds finite deadline; host cannot confirm termination | Default 20 minutes plus at most one progress-based 10-minute extension, then at most 60-second confirmation; unresolved IDs/ownership retained in blocked supervision handoff, no normal completion or publication of uncertain output | PASS |

Across all four procedures, live native statuses remain open/active/blocked/done/
cancelled, analyst and implementation verdicts remain reports, and only the
coordinator publishes state. Code attempts use verified isolated owning-repository
worktrees; records use assigned drafts. Missing lane recipes are not required.
Independent verification checks actual final publication or combined code revision.
The supervisor's finite exception handoff does not pretend an unconfirmed child died.

## Actual delivery evidence inspected

- Read analyst-report.md, explicitly labelled a coordinator-preserved transcription
  of /root/workflow_analyst's final handoff. It records SPECCED, four-routine scope,
  collision-free naming, current contracts and observed baseline probes. I did not
  rerun its inventory scan or independently observe its earlier turn.
- Read the independent reviewer report embedded in live review revision
  32a9b38071e7cde9a3bf929b31ff40ac530672183ef8f1f96fca601f551a0886.
  It rates substantive plan revision 89a6dc2e2bf6cd0aeb86ab51f7b16bb93b5eec8bbbd1954056c95a48beed191c
  at 94/100 with no blockers and identifies bounded cancellation/publication
  clarifications now present. The appended explicit user delegation supersedes
  historical pending-user fields without inventing a numeric user rating.
- Read the final implementer-report.md and all four actual drafts. The report
  distinguishes its completed drafts from pending coordinator publication checks;
  its final digests match the published files. The selected-status clarification
  is recorded and present in the final work-pass.
- Actual collaboration list_agents showed /root/workflow_implementer and
  /root/workflow_reviewer completed, with their bounded final reports; this verifier
  is a separate agent. The reviewer also confirmed the delegated policy correction.
- Read baseline.json and publication.json. Baseline contains the full three prior
  routine bodies and type bodies/digests. Publication log identifies coordinator
  /root, each pre/post revision and serial support-before-coordinator order.
  Publication writes and immediate guarded readbacks are coordinator-reported
  evidence; my subsequent exact MCP reads independently establish the final content.
- Coordinator reports final board-check exit 0 and a concurrently changed PRD
  inventory (earlier 16; now 153). I did not rerun that unrelated board scan and
  do not treat either count as the native work backlog or proof of this routine's
  behavior. The four document identities remain independently verified above.

Only this temporary verifier report was written. No live memo writes, claims,
source edits, commits, installation, external publication, additional sub-agents
or unrelated Rust tests were performed. This delivery is a published agent-executed
routine, with actual analyst/reviewer/implementer/verifier evidence, not an autonomous
scheduler. Coordinator should preserve this report, update observed Check/Result,
release only its own ownership, and independently read the final work/evidence back.


## Relocation and completion checkpoint

Concurrent migration moved this record to /Users/feb/dev/cartridge/.cartridge/memos. The four published routines survived byte-for-byte. The trusted MCP cwd correction in cartridge.ctg commit 8379190 restored reads from that root. The planning ingredient was republished there with corrected relative workflow/template links at revision 8266f8882893395577b49986121c1b810065b0b02e7cfcc9b9dade832289025b.

The user separately requested the discovered duplicate-cartridge fix; its code and runtime proof are tracked in [[@prd/work/root--cartridge-memos-keep-their-qualified-identity.md]]. Live activation and final discovery succeeded. The work-pass creation rule now uses workspace-local uniqueness and preserves shipped qualified identities. The coordinator read back the final Result before completing this work. No unrelated PRD state or foreign claim belongs to this publication.

## Final independent review and completion

The three supporting routines and type/work remain at the original independently verified digests. Final work-pass revision is `88d0495361e5093b4cc0ac922273065ba67ee11226f2273b693b099797345f6a`. Root repeated existing-connection MCP reads and resolve after that change: first result work-pass at the final revision, score30.5. Raw final result: /tmp/cartridge-namespace-final-resolve.json. The final reviewer independently compared the local texts/digests and found no blocker; its resumed turn lacked the MCP tool, so its inspected live responses are coordinator evidence, not independently repeated transport calls.

# Independent final namespace verification

Reviewer: /root/workflow_reviewer, 2026-09-13. Read-only examination; only this temporary report was written.

Verdict: PASS for the final local routine correction, preserved supporting documents, and namespace guidance. No new implementation or documentation blocker found. Live MCP observations below are coordinator-produced evidence inspected independently, not tool calls successfully repeated by this reviewer.

## Independently observed local state

The live owner repositories report memo HEAD `604f47e4bd1f6da661490918bc302f4e33443e6d` and landscape HEAD `361374c6b1e2a6d0736e57904a004d7ae5a79dad`.

| Root-record document | Independently calculated SHA-256 |
| --- | --- |
| routine/work-pass.md | 88d0495361e5093b4cc0ac922273065ba67ee11226f2273b693b099797345f6a |
| routine/spec-a-work-memo.md | 1988695281277d8874a81acd45b389f5fb250a2cba7ed34cfa938920cae46bb6 |
| routine/implement-a-work-memo.md | a5810a349d925892c506162ece53cfa1cb237d446be3632eeb0080d6308f732b |
| routine/land-a-worked-lane.md | abe3aa32e034a0882acdca3bf9c587a82e44dedc7bb5a697cbfbb20d42a7791c |
| type/work.md | 6539b3f54b1ee04f45e55b7eb3ecf4ea6da6d0f60ae2dc5e12eb08d7fb3054de |
| type/type.md | 126e0fbaaa64b21bbbfc69329beeb56e0be1c9d468d4531f52a455b51eaa3c90 |
| type/system.md | 944d7c20f4cd1def0ccd5a2385c4a5b2d5604a6f01e7d93b3e04261ab00f757a |
| type/usage.md | 67c783662ae26f08e0b44b6a55bb530e46dc7c3255def7b7f8ace272914d34e0 |

Compared the work-pass text with the previously verified final draft. Its sole diff changes globally unique leaves to workspace-unique leaves and explicitly preserves shipped `@cartridge/kind/name.md` identities. This corrects the namespace scope without changing coordinator ownership, review, dispatch, verification or recovery procedures. The three support digests match publication.json and the earlier independent verifier report. The work type matches its original baseline digest.

Read updated type/type, type/system and type/usage documents. They agree with the reviewed implementation: qualified identities coexist; contextual shorthand prefers the originating cartridge, then workspace, then a unique external candidate; system composition retains all enabled kind:system memos with qualified shipped headings; shipped usage declarations retain qualified identities. No new contradictory requirement found.

## Inspected coordinator MCP evidence

Source: `/tmp/cartridge-namespace-live-probes.json`.

- Successful reads of `@memo/type/type.md` (71f82003eaa30155dc564fd89bfc3aca6ef39ab8342e762d0ec7524c8dd56cf0) and `@memory/system/type.md` (b7ed13f34630069eb4307c8a3ad174e56cf895c0fdbe912fe08385b126b42cb4). Independently computed local source digests equal these response revisions.
- System result names root `/Users/feb/dev/cartridge/.cartridge/memos`, contains 11 memos, and includes both shipped kind:system documents with their qualified headings in the template. `@memory/system/type.md` has kind:type, so its read succeeds but it is correctly absent from automatic kind:system composition.
- Resolve request for run/work-pass ranks `routine/work-pass.md` first with no problems. The saved result names the pre-correction revision `058beab97d836c672e71c6e158ad044778bcc69e4e3c060f36e8e15440132676`; it proves earlier discovery, not live MCP readback of final revision 88d049. Root was notified of this evidence timestamp distinction.
- Landscape response reports 1,677 nodes and qualified shipped hits, with 4,561 links, 433 uses, 12 injects and 13 provides edges. This is an observed response, not proof of complete backlog execution.

## Verification limit

This resumed reviewer turn no longer exposes the Cartridge MCP tools. Ten attempted read calls returned `MCP tool cartridge/memo is not available to the model`; subsequent tool discovery omitted Cartridge and a system/resolve/landscape invocation encountered an unavailable function. These failures occur at model tool availability, not as memo-service responses. No transport restart, tool exposure change or substitute claim of independent live execution was attempted.

The coordinator's reported 50 tests, formatting and Clippy results remain its evidence. This reviewer previously reviewed both source implementations and confirmed fixes for exact-reference fallback and coverage ownership. Earlier delivery verification independently exercised MCP before the namespace correction. No additional test execution was needed for the final prose-only scope change.


The final resolve evidence mentioned above was captured after the initial probes and resolves the report's pre-correction timestamp distinction. All children have finished their assigned work. Both work memo Results have been saved and read back; final status writes release only this pass's owners. Broader cartridge improvement work remains unassigned.
