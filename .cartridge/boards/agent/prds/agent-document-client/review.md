# The agent executes the selected document revision — review

Canonical PRD: [@agent/agent-document-client](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [clients-share-document-execution](../../../root/reviews/round-1/clients-share-document-execution.md): reviewer 87/100; Revise. Freeze the public query/read/execute schema and legacy-name collision rule; explicitly stage one-shot client parity separately from later lifecycle modes.
  Original SHA-256: `477b9dbaa76fb4c625623164c619b6a2cdc7a5b3d8c6b4cd3ad2af717abe6755`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 19 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14 (reconciliation)

Reconciliation verdict: **SUPERSEDED**.

Reviewed revision: prd.md SHA-256 `97dd9e81daff68c6b27f49f6505f271b51b43f23eaf1092c2399b00f1da2ebb5`; afterwards only frontmatter changed (review-round 3, review-status superseded-recommend-retire), body unchanged, now `6043f14a28ad60794a3b2ba1517520c8f36525485744e9353eba26db745232b7`. Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

Evidence: the plan consumed a shared document-execution contract routed "through landscape" (round-1 source `clients-share-document-execution`). Landscape is gone, and every client now dispatches the same profile-injected `tool.*` keys: the agent takes them from its needs (`agent.ctg/src/main.rs:19-26`) and describes each per run (`agent.ctg/src/model_loop.rs:152-170`). Decision `.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md` (2026-09-14, decided_by user) makes each cartridge's descriptor (`reads`) and help page its own surface; the agent parallelises on `reads` (`agent.ctg/src/model_loop.rs:276-288`). No owner ships a document the agent could execute, and the needed `@mcp/clients-share-document-execution/client-document-contract` is open and stale-after-migration (its links cite nonexistent `mcp.ctg/service.rs`). The leaf's remaining themes already exist for tool calls: exact-call approval binding (`approved_call_executes_exactly_once_and_duplicate_stale_answers_fail`, `run_state.rs:332`) and unknown-outcome recovery without replay (`run_state.rs:453,493`). Consistent with the SUPERSEDED verdict recorded for `@proxy/proxy-document-client` in the same pass.
Disposition: retire recommendation (coordinator/user). Do not delete; `state:` unchanged. If an executable tool memo is still wanted it belongs to root memo `a-tool-is-declared-by-its-memo`, not to this agent leaf.
No score recorded (superseded verdicts need none).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: SUPERSEDED — recommend retire.
Unresolved blocking findings: none for this leaf.
Rounds used / remaining: 3 / 2.
Next action: coordinator confirms retirement together with the mcp parent.
