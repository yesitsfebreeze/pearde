# the-swarm-talks-on-a-board — review

Canonical PRD: [@sessions/the-swarm-talks-on-a-board](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-swarm-talks-on-a-board](../../../root/reviews/round-1/the-swarm-talks-on-a-board.md): reviewer 80/100; Revise. Add scope/permission, durable wake and bounded event-delivery contracts; parent completion must include crash/restart and adversarial attribution tests.
  Original SHA-256: `a70322864d180a5fb897fae09a5f02f5e227bc3368fa927b557f15fa79929c8b`.

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

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **CURRENT**. The parent names no stale path, API or owner; its four needs resolve (roster done, three leaves open and rebased this pass). Architecture changes affect the leaves, not this index.
Presented revision: prd.md SHA-256 `2cef1beddb1fbb4c4ef5029ac0bfff097473c30c2ee0f6aa60f5baeb30d430a4`. Source inspected at sessions.ctg e9725e8 (ported to transport 0d4310f), memo.ctg 9a1cf99, agent.ctg working tree, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 17 | Correct roll-up of the swarm board. -3: "record tested mitigations and remaining limitations" is not an observable outcome. |
| Ownership and reuse | 19 | sessions owns every leaf. -1: no mention of what already exists. |
| Dependencies and slices | 18 | needs resolve, DAG acyclic. -2: no landing order for the shared `channels.rs` footprint. |
| Acceptance and baseline | 15 | -5: no integration proof; round-1 finding (crash/restart and adversarial attribution tests at parent completion) is unaddressed; no gate. |
| Failure and compatibility | 15 | -5: no restart, refusal or baseline statement. |
| Reviewer total | **84 / 100** | |

Result: **FAIL**. Blocking finding: parent completion has no integration proof covering restart and forged attribution (round-1 finding still open).
Rounds used / remaining: 3 / 2. Next: one revision adding integration acceptance and gate.

## Round 4 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **CURRENT** (unchanged).
Presented revision: prd.md SHA-256 `d5e2adfefa1c956c2208debde647468f8aa7e2f9d577fe137dd81b9eac3db43d`. Source inspected at sessions.ctg e9725e8 (ported to transport 0d4310f), memo.ctg 9a1cf99, agent.ctg working tree, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: states delivered basis; adds a two-actor restart/replay acceptance, a forged-`from`/out-of-scope refusal acceptance, an explicit limitation (wake coalescing belongs to a harness listener), and an integration gate with the known red baseline.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | Outcome now observable end-to-end. -2: wake coalescing, part of the original swarm value, is only recorded as a limitation. |
| Ownership and reuse | 19 | Existing channels/cursors/roster named. -1: no link to the harness follow-up. |
| Dependencies and slices | 18 | needs resolve; leaves independent. -2: landing order stated in the log leaf, not here. |
| Acceptance and baseline | 18 | Restart replay with no loss/duplication; forged attribution refused. Current gate baseline: `.cartridge/memos/note/release-status.md` records 8 failing sessions workspace tests; the plan requires naming them before judging new failures. -2. |
| Failure and compatibility | 18 | Restart and refusal paths covered. -2: no statement on disabling sessions mid-exchange. |
| Reviewer total | **91 / 100** | |

Result: **PASS**. Blocking findings: none (round-3 blocker resolved by the integration acceptance).
Validation: file existence; `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 4 / 1.
Next: leaves first; parent collects at one pinned sessions revision.
