# Old and new consumers see one compatible memory tool — review

Canonical PRD: [@memory/memory-owns-its-tool/memory-consumer-parity](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [memory-owns-its-tool](../../../../root/reviews/round-1/memory-owns-its-tool.md): reviewer 88/100; Revise. Reconcile the three memory-tool enhancement leaves with adapter retirement and specify the mixed-version interval and exact profile exposure snapshots.
  Original SHA-256: `4725b397890c58624ff423048e24c77dc8863973320aae8be1dc272549d0563a`.

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

Reconciliation verdict: **SUPERSEDED**. This leaf tested a *mixed-version interval*: old consumers reaching memory through the memory-tool wrapper, and new ones reaching the surviving adapter. That interval no longer exists.
- Root `9e4cde8` dropped the memory-tool submodule.
- `rg --hidden memory-tool` finds no composition consumer. The only hits are a comment in `memory.ctg/src/cartridge/src/lib.rs`, historical root notes, and the untracked, unignored scratch lane `.runtime-composer-lane/`, which is not part of the composition.
- Every client now dispatches the one `tool.memory` event memory itself defines (manifest `events`/`listen` at memory.ctg `2e21dcc`). mcp (`needs: tool.*`, ws/mcp.ctg `e2a971e`) and proxy therefore cannot see a second memory tool. The base refuses an event declared twice (cartridge.ctg `docs/transport.txt`, CHECKS).
- Unsupported operations are refused explicitly without store mutation (`tool_call`: "memory tool needs op query|ingest and non-empty text").
- The remaining outcome, one compatible tool, is structural. Its behavior is proven by `ingest_query_tool_and_context_reach_one_store_through_the_base`.

Presented revision: `prd.md` SHA-256 `4d8a3682b80510e0aae96df89651c41473f1211a70da262c9d0c50b684b987fa`. Before: `2e0217d65f98cd76257fc28fdcb416c371d76124c5fa790d3b0cdfa28c7616de`. Frontmatter only changed; the body is unchanged.
Disposition: retire recommendation (coordinator/user). Do not delete; `state:` unchanged. Its needs `@memory/improve-memory-tool-get` and `@memory/improve-memory-tool-errors` remain independent open work and do not depend on this leaf.
No score recorded (superseded verdicts need none).
Unresolved blocking findings: none.
Validation (cwd /Users/feb/dev/cartridge, read-only): `ls`/`rg` existence checks of the cited source and tests on memory.ctg main and ws/memory.ctg branch `transport` (both `2e21dcc`) and on the pre-port revision `c25af4d` (`git show`); `git show --stat 9e4cde8`; `rg --hidden memory-tool` over the composition excluding prd.ctg and target; needs resolution under `boards/<owner>/prds/<slug>/prd.md`; `shasum -a 256`. No product gates (`just test memory`, `just check memory`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator retires this leaf together with closing the parent `memory-owns-its-tool`.
