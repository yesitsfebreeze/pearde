# The composed system passes the complete workflow and retires redundant wrappers — review

Canonical PRD: [the-composed-system-proves-the-plan](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-composed-system-proves-the-plan](../../reviews/round-1/the-composed-system-proves-the-plan.md): reviewer 88/100; Revise. Include the improvement programme and sandbox prerequisites in the release census; a 16-PRD completion cannot establish completion of the wider open backlog.
  Original SHA-256: `359d4f868e0c42a3a60c1863ea87cdc82077009a761c1bd2c7b9d2bc74e47d1d`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `46c58f4d28ec4be126c508053c73636d1cecfebb916589761507b847d9195b45`. Composition: root `24aa2be` (dirty), memo.ctg `9a1cf99`, memory.ctg `c25af4d`, cartridge.ctg `c9ef10b`, prd.ctg `077e57a2` (dirty).
Change: gates rewritten to the current root recipes (`just check`, `just test`, `just smoke`, `just verify`, `just isolation`), baseline from .cartridge/memos/note/release-status.md, recovery rule; added `@runtime/the-sandbox` (open round-1 finding). Pre-revision SHA-256 `cacdb47bae46323a3db7fed72c6e4191759b48b0e0b1fc63ae592bb88c356d70`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 17 | Release gate still wanted. -3: 'retires redundant wrappers' has no named wrapper list. |
| Ownership and reuse | 16 | Root is the right owner for the release gate. -4: two needs sit on the dissolved `landscape` board. |
| Dependencies and slices | 12 | All ten needs resolve on disk and are acyclic, but `@landscape/context-quality-is-measured` and `@landscape/recursive-development-graph` target a dissolved owner (decision the-fabric-lives-in-core), `@tools/development-tooling-has-one-home` is `superseded-recommend-retire` in its own review, and `@runtime/documents-own-live-processes` is still pre-rewrite. -8. |
| Acceptance and baseline | 19 | Five concrete root gates at pinned SHAs plus retirement census rule. -1: known red baseline. |
| Failure and compatibility | 18 | Red gate attributed to changed pin; last green SHA set retained; no replay. -2. |

Agent score: **82/100 — FAIL**.
Findings: The PRD's own text is now current; its dependency set is not.
Unresolved blocking findings: needs on the dissolved landscape board and a superseded tools item must be rehomed or removed by their owning boards.
Disposition: keep; coordinator rehomes/retires the listed needs, then re-review.
Validation (cwd /Users/feb/dev/cartridge): existence checks of the named starting files, fixtures and justfile recipes (`.cartridge/justfile`: check, test, smoke, verify; root `justfile`: isolation); `rg` for the named symbols and tests; `git log` in the owner submodules; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md` and every relative link; `shasum -a 256`. No product gates (`just check`, `just test`, `just smoke`, `just verify`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator fixes cross-board needs; one re-review (2 rounds remain).

### Citation correction after the round above — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). Coordinator correction: decision memo `the-fabric-lives-in-core` is outdated; cartridge.ctg `939e7d1` deleted core `src/graph.rs`, `src/fabric.rs`, `src/evidence.rs`. The fabric graph is `memo.ctg/src/fabric_graph.rs` and the evidence contract is the crate `memo.ctg/evidence` (memo `8d6a803`); owner memo, gate `just test memo`.
Change (citation only): replaced the link to that decision memo with source/commit evidence.
- Before: `sit on the board dissolved by [the-fabric-lives-in-core](../../../../../../.cartridge/memos/decision/the-fabric-lives-in-core.md)`
- After: `sit on the dissolved landscape board (no landscape.ctg; fabric work is owned by memo, `memo.ctg/src/fabric_graph.rs` and `memo.ctg/evidence`, gate `just test memo`)`
SHA-256 before `46c58f4d28ec4be126c508053c73636d1cecfebb916589761507b847d9195b45`, after `d5127d0639d9f310876b7d46770061a016f3bf3bd936f16e5eccd66415054ac0`. No acceptance, need, owner, gate or scope changed, so the score, result and round count above stand; no round consumed. Earlier mentions of that decision in this history refer to the outdated memo; the facts relied on (op renamed to `fabric`, landscape dissolved, fabric owned by memo) are verified in source.
