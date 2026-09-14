# Retiring the wrapper preserves stores and consumers — review

Canonical PRD: [@memory/memory-owns-its-tool/memory-wrapper-retirement](prd.md). Reviewer: `/root` (self-review).
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

Reconciliation verdict: **DELIVERED**. The wrapper was retired as one composition change in root `9e4cde8` ("drop memory-tool and workspace, rename ui to tui"). That commit touched `.gitmodules` and removed the `memory-tool.ctg` gitlink, and its message records that the recursive-clone source-layout test failed on the dead paths and passes with the new layout (acceptance 2). Every consumer points at the surviving implementation:
- The root profile `.cartridge/init.lua` composes `{ id = "memory", path = "memory" }`.
- harness injects `memory`.
- `.cartridge/config.lua` configures `memory` / `tool.memory` only.
- No tracked composition file names memory-tool (`rg --hidden`; only historical notes and the untracked `.runtime-composer-lane/` scratch copy mention it).

Store bytes are untouched: the bank stays at `memory` setting `dir` (`.cartridge/memory`). The compatibility entry is restorable from git history (`9e4cde8^`), and the absorbed envelope lives on in `src/cartridge/src/lib.rs` (`ToolContext`, "the same envelope the former separate memory-tool cartridge carried").

Presented revision: `prd.md` SHA-256 `da0f83735d4b042ef9422930e8b5fc360a3392ae4b514673fbdf755770a541fb`. Before: `dbfd227c32d455c1d7dd45174487199c751564d2e761ee313f5161a735722529`. Frontmatter only changed; the body is unchanged.

Agent score: not scored (delivered-pending-verification).
Findings: (1) The need `memory-consumer-parity` is SUPERSEDED in this pass. The retirement happened without that matrix, so the edge is historical. (2) The untracked `.runtime-composer-lane/` still carries memory-tool profile text (`default/init.lua`, `mcp/init.lua`, `live/init.lua`). It is not a consumer, but the coordinator may delete or ignore it. `state:` is untouched.
Unresolved blocking findings: none.
Validation (cwd /Users/feb/dev/cartridge, read-only): `ls`/`rg` existence checks of the cited source and tests on memory.ctg main and ws/memory.ctg branch `transport` (both `2e21dcc`) and on the pre-port revision `c25af4d` (`git show`); `git show --stat 9e4cde8`; `rg --hidden memory-tool` over the composition excluding prd.ctg and target; needs resolution under `boards/<owner>/prds/<slug>/prd.md`; `shasum -a 256`. No product gates (`just test memory`, `just check memory`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator confirms a fresh recursive clone at root HEAD and marks done.
