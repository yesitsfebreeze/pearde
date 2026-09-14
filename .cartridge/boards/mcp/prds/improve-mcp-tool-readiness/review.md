# Discover policy and readiness for exposed tools — review

Canonical PRD: [@mcp/improve-mcp-tool-readiness](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-mcp-tool-readiness](../../../root/reviews/round-1/improve-mcp-tool-readiness.md): reviewer 89/100; Revise. Define the shared readiness producer and response schema; current dependencies name memory readiness but not a generic tool readiness owner.
  Original SHA-256: `a70fb113aef900ad36fc39195d968c984bd1ba4f9fb4bb29195000d86d511c0c`.

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

## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**. Evidence: decision `the-fabric-lives-in-core.md` (no landscape producer); decision `a-cartridge-brings-its-own-surface.md` (a cartridge must not carry sibling knowledge; descriptors declare their own facts such as `reads`, seen in `fs.ctg/src/service.rs`, `memo.ctg/src/service.rs`, consumed by `agent.ctg/src/model_loop.rs`); mcp ported to transport (834b9d9, 4cbf00c); `mcp.ctg/src/service.rs` already has the registry with `descriptor_revision` and `cartridge/policy` inspection via `policy.explain`; no generic readiness producer exists (rg "readiness" finds only memory health and mcp's transport probe). Pre-revision text (SHA-256 `e6617a2227987de0201c03fd44d0163bc763a59141b55cc5b27aed0e5ae6d29a`) assigned readiness rows to landscape, had MCP consume memory store status (conflicts with the surface decision), put UI acceptance in an MCP leaf, and named three missing paths. Blocking.

Revision reviewed: `prd.md` SHA-256 `5b11853534736514432650a3f4ed83699ed42cbee17f323f0717e8181c03d27f` (working tree). Changes: readiness composed from MCP's own registry, the declared policy need and an optional descriptor-declared `readiness` field; unknown when absent; stale marking via descriptor revision; tui view left to `@ui/improve-ui-tool-availability`; dropped the done need on the dissolved landscape contributor contract; real paths and gate.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Bounded diagnostic view; -2 dependency readiness stays `unknown` until owners adopt the field. |
| Ownership and reuse | 19 | MCP-only, reuses registry and policy inspection, respects the surface decision; -1 the field name/shape is not yet agreed with descriptor owners. |
| Dependencies and implementable slices | 18 | Remaining need done; ready; -2 owner adoption of `readiness` is unlinked follow-up work. |
| Observable acceptance and baseline evidence | 19 | Four observable rows/negatives, baseline with known failure; -1 fixture tool set not listed. |
| Failure, recovery and compatibility | 18 | No provider start/grant, re-check on call, additive method; -2 no latency bound for policy explanation across many tools. |
| Reviewer total | 92 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of repo, source, test and doc paths (ls/rg); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke` and `.cartridge/memos/routine/cartridge-development.md` accepts the named owners; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: ready to claim. Coordinator: `@ui/improve-ui-tool-availability` still names `ui` (now tui) and should consume this view.
