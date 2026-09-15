---
repo: /Users/feb/dev/cartridge
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
description: "Run a bounded work memo through an MCP-discoverable PeaRDe-style pass with analyst, implementer and verifier sub-agents"
---

# Restore the MCP work pass

## Outcome

A caller can discover and read `routine/work-pass.md` through the current Cartridge MCP and use it to take one explicitly selected work memo through analysis, review, implementation and independently verified collection. The coordinator owns the live record; worker reports supply evidence. This is an agent-executed routine using existing MCP and host agent tools, not a new scheduler service or MCP operation.

The first pass delivers this routine and aligns its three supporting routines. Future passes select existing cartridge improvement leaves. Scope is one native memo pass; the existing Pearde PRD engine remains authoritative for its separate boards.

## Baseline

On 2026-09-13 the connected MCP read of `routine/work.md`, `system/work.md` and `@memory/system/work.md` returned "memo not found". The legacy sys skill preserves the desired pass. Current MCP reads of spec-a-work-memo, implement-a-work-memo and land-a-worked-lane succeed, but their procedures still require unavailable `just lane`, `just land` and `just lane-rm` recipes and disagree about which actor records completion.

The live `type/type.md` requires globally unique memo leaves; `type/work.md` already exists. Therefore the new canonical routine is `work-pass`, discovered by work/PRD/PeaRDe queries, not another local leaf named work. `just board-plan` scans 16 owner-local PRDs; it does not include or dispatch the native work-memo inventory. The workspace and owner repository already contain unrelated changes.

## Owner and footprint

Owning repository: `cartridge.ctg`, starting HEAD `a44b8489f375cf87cebcc14f275fa3355f6a9105`; the live trusted record is its `.cartridge/memos`.

Implementation may change only:
- `routine/work-pass.md` (new).
- `routine/spec-a-work-memo.md`.
- `routine/implement-a-work-memo.md`.
- `routine/land-a-worked-lane.md`.

Coordinator-owned records: this work memo, `note/restore-mcp-work-pass-review.md`, and `note/restore-mcp-work-pass-evidence.md`. They are bookkeeping for this delivery, not a second board. No existing parent scope, PRD state, active claim, source code, runtime profile, plugin registration, global skill installation or external repository changes are included.

No hard work dependencies: the connected memo read/write/resolve operations and this host's collaboration tools already exist. Related context: [[@prd/routine/plan-cartridge-work.md]], [[@prd/routine/spec-a-work-memo.md]], [[@prd/routine/implement-a-work-memo.md]], [[@prd/routine/land-a-worked-lane.md]]. The existing 45-improvement programme is separate downstream work, not implicitly assigned.

## Approach

1. Analyst inspects the existing procedures and live MCP contracts; records missing operations, naming conflicts and exact source revisions. Coordinator records the plan and base revisions.
2. Independent reviewer evaluates this exact plan using [[@prd/routine/plan-cartridge-work.md]] and the root review method. Preserve five-round history and any actual user feedback. Resolve findings before dispatching dependent implementation.
3. Implementer reads this memo and the reviewed contract. Produce four complete replacement Markdown drafts in an assigned temporary directory. Record-only workers do not write the live record or need code worktrees. Coordinator alone publishes validated MCP writes with the latest expected_revision for existing paths; stale revisions stop publication for reconciliation.
4. The work-pass routine defines:
   - Named-scope selection; MCP landscape/resolve/read first; paginated list for native work and explicit Pearde scan only for PRDs. Search result limits never mean the backlog is exhausted.
   - Re-read statuses, owner, legacy claim, prerequisites and existing pass checkpoint before dispatch. Unknown/malformed dependencies, unresolved questions, rejected or missing required review, active ownership, or overlapping footprints prevent dependent dispatch. Parent roll-ups are not implementation leaves. Do not remove claims merely for age.
   - One bounded analyst, implementer or verifier brief per worker, carrying canonical memo path, revision, exact footprint, needed context, acceptance commands and report location. Respect host capacity; wait for every child to finish or be confirmed dead before returning. Use host collaboration capabilities, not nonexistent kern tools or assumed agent types.
   - Analyst returns SPECCED, SPLIT or QUESTION with evidence and proposed record edits. Implementer returns DONE, FAILED or BLOCKED with patch/draft paths and actual checks. These are report verdicts, not memo status values.
   - Coordinator alone updates native open/active/blocked/done/cancelled and owner through validated revision-aware writes. A claim is advisory, not a lock; the workflow promises no atomic compare-and-swap or distributed exclusion. Release only this pass's ownership and preserve other actors.
   - Code workers use coordinator-assigned isolated Git worktrees at a verified owning-repository revision with required dependencies; reuse a verified existing attempt. Never assume main, copy an unrelated dirty tree, or invoke missing lane recipes. Record workers use assigned draft/report paths and coordinator publication.
   - Independent verification reruns the memo's observable checks against the actual resulting revision. Coordinator serially reviews/integrates only assigned changes, reruns applicable combined checks, records completion only after observed acceptance, and distinguishes saved drafts, published memos and landed code.
   - Resume from a bounded session-specific memo checkpoint with worker IDs, footprints, attempts, revisions, evidence and next action. Failed/uncertain effects are investigated before retry; no blind mutation replay. Missing host capability or permission is an explicit result. A bounded one-memo pass ends without starting unrelated standing routines.
5. Align spec/implement/land routines with that same role, workspace and completion contract. Remove their mandatory missing lane commands and worker-owned live-status writes. Keep their bounded Outcome/Approach/Check discipline and failure evidence.
6. Verifier independently reads the published routines via MCP, tests discovery and linked ingredient reads, and walks concrete ready/unspecced/owned/blocked/failed/stale-resume cases. Record observed tool results separately from procedure walkthroughs; neither proves a scheduler exists.
7. Coordinator rereads all four saved documents, verifies their final revisions and the original naming/type record, and updates Check/Result only for observed proof. Leave broader implementation and external shipping to separately selected work.

## Acceptance
- [x] MCP `read` returns all four valid routine documents with Inputs, Do, Check and Failure, while `type/work.md` remains unchanged.
- [x] MCP `resolve` with usage run and query "work pass PeaRDe sub-agents" returns `routine/work-pass.md`, and every routine/type reference needed for the next step can be read.
- [x] The four procedures agree on coordinator-owned live record writes, current native statuses, worker report verdicts, isolated code ownership, record-only draft publication, and independent verification before completion.
- [x] A verifier's recorded walkthrough covers ready and unspecced leaves; another owner's claim; missing/failed prerequisites; missing user review; conflicting footprints; failed checks; stale revision; and interrupted-worker recovery without inventing completion or replaying unknown mutations.
- [x] This delivery actually uses a separate analyst, implementer and verifier/reviewer, retains their bounded reports, and records the final published routine revisions. Scenario walkthroughs are labelled separately from executed implementation.
- [x] MCP readback confirms this memo's final evidence and Result; unrelated files and claims have not been included in the publication.

## Verification commands and evidence

Run from the connected Cartridge MCP:
`{"op":"read","path":"routine/work-pass.md"}`;
`{"op":"resolve","usage":"run","query":"work pass PeaRDe sub-agents","limit":20}`;
read the three supporting routine paths and `type/work.md` individually.
Use the MCP revision digests for identity and the validated write response for structural validity. Capture pre/post reads and the verifier's actual results in the evidence note. No runtime source is changed, so broad Rust build/test gates do not demonstrate this documentation outcome.

## Failure and rollback

Preserve every pre-write body/revision and each successful publication revision in the evidence report. If a later write fails, record precisely which documents are already published and resume reconciliation from live readback; never claim an atomic four-file update. If rollback is needed, restore only this pass's changed documents with current revision guards after checking for concurrent edits. A stale write, unreadable dependency or failed verification leaves the work open with evidence and retained drafts, or blocked only for a named external dependency. Publishing a routine never grants additional tool authority.

## Result

Published and independently verified the MCP-discoverable coordinator [[@prd/routine/work-pass.md]] and its three aligned supporting routines. Analyst /root/workflow_analyst, implementer /root/workflow_implementer and verifier /root/workflow_verifier completed their bounded tasks. Independent plan review was94/100 under the user's explicit delegated-rating instruction; no user score was requested or invented after the correction. [[@prd/note/root--restore-mcp-work-pass-evidence.md]] retains publication and independent verification evidence, including17 prose scenario walkthroughs clearly separated from executed MCP operations.

Current canonical record is /Users/feb/dev/cartridge/.cartridge/memos following a concurrent migration; the owner/record paths in Baseline describe the original plan. The user's later namespace request was implemented separately as [cartridge-memos-keep-their-qualified-identity](../cartridge-memos-keep-their-qualified-identity/prd.md), including the trusted MCP cwd correction. The coordinator now checks workspace-local leaf uniqueness while preserving shipped qualified identities. No PRD state, foreign claim or unrelated delivery was collected.

Final published revisions:
- routine/work-pass.md: `88d0495361e5093b4cc0ac922273065ba67ee11226f2273b693b099797345f6a` (one namespace wording alignment after original independent verification).
- routine/spec-a-work-memo.md: `1988695281277d8874a81acd45b389f5fb250a2cba7ed34cfa938920cae46bb6`.
- routine/implement-a-work-memo.md: `a5810a349d925892c506162ece53cfa1cb237d446be3632eeb0080d6308f732b`.
- routine/land-a-worked-lane.md: `abe3aa32e034a0882acdca3bf9c587a82e44dedc7bb5a697cbfbb20d42a7791c`.

Final existing-connection MCP reads matched all four revisions. type/work.md remains unchanged at `6539b3f54b1ee04f45e55b7eb3ecf4ea6da6d0f60ae2dc5e12eb08d7fb3054de`. Required planning/type/usage references read successfully. The final resolve query returns work-pass first at its final revision and score30.5. Artifacts: /tmp/cartridge-work-pass.hikK5c; final resolve response /tmp/cartridge-namespace-final-resolve.json. This is a published agent-executed workflow using host sub-agents, with no added scheduler or MCP operation.
