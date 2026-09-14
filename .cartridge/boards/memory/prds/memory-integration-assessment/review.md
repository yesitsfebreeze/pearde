# memory-integration-assessment — review

Canonical PRD: [@memory/memory-integration-assessment](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [memory-integration-assessment](../../../root/reviews/round-1/memory-integration-assessment.md): reviewer 55/100; Reconcile. Revalidate current children and supported query/health/readback surfaces; answer generation and old model/MCP hosting must not become memory acceptance again.
  Original SHA-256: `353b371e6c2406ec317406d00274cf32773757ab9211c5c2c3e037893756815c`.
- [memory/the-vision](../../../root/reviews/round-1/memory--the-vision.md): reviewer 25/100; Rewrite. The proxy/memo/plugin destination conflicts with current memory database/CLI scope and WORK_ITEMS.md; replace active release criteria while preserving this historical vision.
  Original SHA-256: `6df08bba37e57e74ced208ea26b5d607f81e94160b3212260f14a0a6dcc037da`.

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

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.
Reconciliation verdict: **SUPERSEDED — the 2026-09-07 assessment observed failures in the pre-transport daemon RPC and `memory mcp` surface (`no tokio runtime`, `daemon rpc: rpc adapter: eof`; see round-1 source). Memory was ported to the cartridge transport on 2026-09-14 (memory.ctg `9cc0f0b`, `c25af4d`) and MCP hosting left memory (`.cartridge/docs/WORK_ITEMS.md` 'Not carried forward'). None of its ten original subwork items exists on the board. The round-2 snapshot only re-buckets leaves already tracked elsewhere: memory-002 and memory-004 under keep-the-tree-and-record-true, memory-adapter-core under memory-owns-its-tool and the-agent-surface-is-usable, and every-mutation-holds-the-store-writer-boundary is done. Its live-probe requirement is carried by the-agent-surface-is-usable's integration gate.**

Presented revision: `prd.md` SHA-256 `8ef69fa96161352ada162d7401b39e267094a78a299b83981f9a0ec7d9360f16`. Frontmatter only changed (review-round, review-status); body unchanged.
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

Agent score: not scored (superseded-recommend-retire).
Findings: Recommend retiring this rollup; no requirement is lost (mapping above). `state:` left untouched.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Coordinator: retire or mark void in work-map; no implementation.
