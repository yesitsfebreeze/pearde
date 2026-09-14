# Workspace tools improvement plan — review

Canonical PRD: [@runtime/improve-tools-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-tools-programme](../../../root/reviews/round-1/improve-tools-programme.md): reviewer 85/100; Rehome. Connect the three leaves to the surviving runtime-owned development package and preserve their behavioral gates across relocation.
  Original SHA-256: `b4dc92ae34f045e532f49340bdcd7af6ee121baa0acc9126f88ce358c76c439c`.

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

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `c07e4f0f6c0650d46133384446eac7cb290ea3f59befee46d72b13b57816a865`.

Reconciliation verdict: **REBASE**. The outcome is still wanted, but owner and paths moved. `cartridge.ctg/scripts/workspace.py` and `repositories.json` no longer exist (last touched in cartridge.ctg `f9b8d9a`). Decision `tui-and-tools-are-cartridges` gives bundle/lane operations to the `tools` cartridge, and `tools.ctg/src/service.rs` implements `bundle`, `lane`, `land` and `lane-rm`. Decision `cartridge-repositories-keep-records-and-executable-memos` removed Python. Revision: `repo` moved to tools.ctg, the current implementation and tests are named, the integration gate is `just test tools` / `just check tools`, and the shared `service.rs` footprint is stated.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | Short roll-up with an integration gate; −2: the gate's `lane.test.ts` fixture validity is unverified. |
| Ownership and reuse | 18 | Correct repository and current source; −2: the record still sits on the runtime board while the owner is tools (rehome is for the coordinator). |
| Dependencies and slices | 18 | All three `needs` resolve to runtime-board leaves, and preflight/bundle-provenance were rebased to tools.ctg in this pass; −2: the leaves share one file and must land serially. |
| Acceptance and baseline | 18 | `just test tools` exists (cargo -p tools plus `lane.test.ts`); −2: no baseline recorded. |
| Failure and compatibility | 18 | Limitations are recorded per leaf; −2: the roll-up has no rollback statement of its own beyond its leaves. |
| Reviewer total | 90 / 100 | |

Result: **PASS**. Blocking findings: none.
Findings: (1) rehoming to the tools board is recommended to the coordinator; (2) `lane.test.ts` launches `cartridge.ctg/target/debug/cartridge --dir cartridge.ctg/builtin`, and `builtin` no longer exists, so the gate may not run (handled as step one of the worktree-resume leaf).
Validation: `ls`/`rg` of tools.ctg sources and tests, the `_cargo` owner cases in `.cartridge/memos/routine/cartridge-development.md`, and needs resolution. No product gates were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: implement a leaf; the preflight and resume leaves are dependency-free.
