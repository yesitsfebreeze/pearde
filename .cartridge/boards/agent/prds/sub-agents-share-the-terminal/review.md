# sub-agents-share-the-terminal — review

Canonical PRD: [@agent/sub-agents-share-the-terminal](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [sub-agents-share-the-terminal](../../../root/reviews/round-1/sub-agents-share-the-terminal.md): reviewer 82/100; Revise. Concurrent shared edits cannot remain an unowned hazard; bind child execution to PTY leases and workspace ownership, with crash/restart reconciliation.
  Original SHA-256: `9b2760cf64c0e69d2793aa4599a4135a875774fb20e79dd008df8b9e9bd06914`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 20 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 20 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: Parent reduced to linked scope and integration acceptance; only leaves are implementation work.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14 (reconciliation and rebase)

Reconciliation verdict: **REBASE**. The collaboration goal stands (decision `the-agent-surface-preserves-the-visible-shell`: expose it through discoverable services, no hidden execution tools). Changes: `ui` was renamed `tui` (root `9e4cde8`/`bc2c190`; `@ui/the-panel-switches-to-a-sub-agent` still resolves in the `ui` board but its repo is `tui.ctg`); services are declared events on the rewritten host; the sessions child is done. Round 1's unowned concurrent-edit hazard and PTY-lease binding had no integration coverage.

Presented revision: prd.md SHA-256 `ff825323c718d6675e9ba8ea288ea183fbe32317c071d880d52ab130baab70c6` (rebased from `0475be7a4d3fecd7657fa1d96a71ccf4b308879e75dd4ad91657e3204014768d`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Parent only; decision constraint stated. −2: swarm board child widens the roll-up beyond the terminal goal. |
| Ownership and reuse | 18 | Children in their owner boards; lease prerequisite carried by the spawn leaf. −2: `ui` board naming lags the `tui` rename. |
| Dependencies and slices | 18 | All five needs resolve; acyclic. −2: several children stale or failing review; events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | End-to-end integration check; concurrent-edit hazard is serialized or recorded with a fixture; gates exist (`just test tui`, `just smoke`). −2: `just smoke` currently fails for mcp/proxy per release status. |
| Failure, recovery and compatibility | 18 | User PTY/editor preserved; limitations recorded. −2: crash/restart reconciliation across children delegated to the spawn leaf only. |
| Reviewer total | **90 / 100** | |

Findings and concrete revisions: (1) integration check and gate added. (2) Concurrent-edit hazard from round 1 given an observable disposition. (3) Board-rename and lease pointers annotated.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased). Coordinator: retarget `@ui` needs if the board is renamed to `tui`.
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (90/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: children proceed; integration after the events port.
