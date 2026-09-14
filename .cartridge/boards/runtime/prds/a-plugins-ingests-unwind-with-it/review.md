# a-plugins-ingests-unwind-with-it — review

Canonical PRD: [@runtime/a-plugins-ingests-unwind-with-it](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-plugins-ingests-unwind-with-it](../../../root/reviews/round-1/a-plugins-ingests-unwind-with-it.md): reviewer 48/100; Rehome. The durable-versus-retractable distinction is valuable; runtime disposal belongs outside memory while source retraction integrity remains an engine contract.
  Original SHA-256: `ef052d5dd072ae9e45f4d36c03688db631c1e0ba66bb372a07ed734b79f63902`.

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

Reconciliation verdict: **SUPERSEDED**. The fiber/effect model this outcome was built on is gone: plugin projections identified by owner generation and effect ID no longer exist. It was replaced by node processes that serve their own sockets (cartridge.ctg 939e7d1, ee7e295; `docs/architecture.txt`). The runtime part is delivered by construction:
- Disposal is per node (`cartridge.on_dispose`, `docs/transport.txt`).
- `stop_slot` bumps the generation before stopping, and replacement runs one at a time under the host `op` lock (`src/host/mod.rs:469-534`). A stale disposer therefore cannot overlap its successor.
- A stale exit is ignored by generation (mod.rs:455).

What remains belongs to memory. `memory.ctg/src` has no source-retraction operation (`rg retract` finds nothing; only `delete_one_memory` at `src/store/core/src/lib.rs:808`). Under decision `a-cartridge-brings-its-own-surface`, a cartridge would reach that through a declared need on a memory-owned event, not through runtime unwinding. The PRD also links the absent `src/runtime.rs`/`src/service.rs`.
Presented revision (frontmatter status only changed): `3e4cc316a5a1174887fdfb2ef8307c15169bd9d39240a4942bf1d8361572a9e7` (stale body digest `1aa6887a6b83b1991047683ed5523b504f911bcee7eb9d8ac512148cf66389f9`).
Recommendation: retire here. The coordinator decides whether @memory needs a leaf for source retraction with provenance, which would inherit this scope's 3 used rounds. No score needed.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `git remote -v`; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: coordinator retire/rehome decision.
