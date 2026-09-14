# Clients share query read and execute contracts — review

Canonical PRD: [@mcp/clients-share-document-execution/client-document-contract](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [clients-share-document-execution](../../../../root/reviews/round-1/clients-share-document-execution.md): reviewer 87/100; Revise. Freeze the public query/read/execute schema and legacy-name collision rule; explicitly stage one-shot client parity separately from later lifecycle modes.
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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.

Reconciliation verdict: **SUPERSEDED**.

Program-level evidence (shared with the runtime runner leaves reviewed in this pass):
- On the route taken, a tool is an event its owner defines and listens to (ws/cartridge.ctg branch `transport-design` `ba198f4`, `docs/transport.txt`: "A tool is an event its owner listens to"). Every client dispatches the same `tool.*` events by a `needs` glob: mcp `needs: ["sessions","policy","policy.*","tool.*"]` (ws/mcp.ctg branch `transport` `e2a971e`, now also on mcp.ctg main). Agent and proxy do the same (their leaves `@agent/agent-document-client` and `@proxy/proxy-document-client` were recorded SUPERSEDED today).
- The shared request/result contract this programme set out to freeze is therefore the `describe`/`call`/`cancel` envelope with `content:string` / `error:boolean`, already shared by all three clients (`@gitfs/tool-results-interoperate` done).
- The open root work memo `.cartridge/memos/work/a-tool-is-declared-by-its-memo.md` requires a tool memo to be "discovered, described and called through the same `tool.*` surface a cartridge tool is". A future document runner, whoever owns it, therefore needs no client-side contract or adoption.
- The runner itself is still wanted (decision `the-tool-contract-is-a-memo.md`, accepted), but its executor is an open choice recorded as CONFLICT on `@runtime/one-runner-executes-documents/approved-document-launch` in this pass.

Leaf evidence:
- "Name collisions are errors rather than last-writer wins" is enforced twice. The base refuses an event declared by two cartridges before start (`docs/transport.txt`, CHECKS). mcp refuses duplicate or non-exact tool keys (`src/service.rs` `Config::validate`: "mcp tools must be unique exact tool keys").
- Owner-qualified legacy names no longer exist: event names are the owner's own.
- Success, tool failure and denial outcomes are already fixture-tested per client. For mcp these are `an_ask_refusal_names_the_operation_and_the_missing_channel` and `an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused` (`.cartridge/tests/unit/tests.rs`) and `approval.test.ts`.
- Stale revision is the tool's own `revision` carried in mcp's catalog (`src/service.rs` observe `revision`).
- "Unsupported sidecar/event modes refuse explicitly" is a property of the runner, not of a client. It belongs with the runtime runner leaves.
- The starting-file links `../../../../service.rs` and `tests.rs` resolve to nothing. The need `memory-document-works-end-to-end` was itself rebased today to prove memory's own surface "rather than through a separate document runner".

Presented revision: `prd.md` SHA-256 `3ec9131930914c6760199f0246368cd86e0724b749338f9823fc584926397098`. Before: `c86c965fef28317dbdf387b1afd0039458e06aff9de3a3a9f524832c92fd4669`. Frontmatter only changed; the body is unchanged.
Disagreement to resolve: the parent `@mcp/clients-share-document-execution` passed round 4 as CURRENT on the premise that clients adopt a shared runner contract. This leaf's evidence contradicts that premise. The coordinator should re-reconcile the parent (likely SUPERSEDED, or reduce it to a cross-client parity check over existing `tool.*` fixtures). This reviewer did not edit the parent.
Disposition: retire recommendation (coordinator/user). Do not delete; `state:` unchanged.
No score recorded (superseded verdicts need none).
Unresolved blocking findings: none for this leaf.
Validation (read-only): `ls`/`rg` over mcp.ctg (main and ws branch `transport`, `e2a971e`), ws/cartridge.ctg `ba198f4` `docs/transport.txt`, root decision and work memos; needs resolution under `boards/<owner>/prds/<slug>/prd.md`; `shasum -a 256`. No product gates (`just test mcp`, `just smoke mcp`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator retires this leaf with the parent, or reopens under the tool-memo work if the user wants a client-visible document contract.
