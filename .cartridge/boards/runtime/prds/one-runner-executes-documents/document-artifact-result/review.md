# An artifact result reads only the approved output — review

Canonical PRD: [@runtime/one-runner-executes-documents/document-artifact-result](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [one-runner-executes-documents](../../../../root/reviews/round-1/one-runner-executes-documents.md): reviewer 79/100; Revise. Resolve the open launch-authority/platform prerequisites explicitly; bind approved execution to immutable recipe bytes and specify artifact path/readback authority.
  Original SHA-256: `51d35f31e677cd03aa5d431d7144750c56f629fab1b4700f397af51c170fd993`.

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

Reconciliation verdict: **CONFLICT** (needs a user decision). This leaf carries the same executor/authority decision recorded in full in [approved-document-launch round 3](../approved-document-launch/review.md). In brief:
- The outcome is still wanted (decision `the-tool-contract-is-a-memo`, open work memo `a-tool-is-declared-by-its-memo`).
- No executor exists on main or on the transport branches: cartridge.ctg `src/runtime.rs` and `src/service.rs` are gone, and memo `83bf1ad` only freezes the invocation with `launch_authorized: false`.
- Whether an owning cartridge (A), memo (B) or the base (C) runs the recipe, or execution is retired (D), is a material choice. It changes this leaf's repo, board, starting files and gate.

Leaf-specific note: the artifact root and the readback authority depend on whose grant ran the recipe. Under A it is the owner's own `grant.write`; under B it is memo's `write: ["/"]`, which makes "beneath its permitted root" meaningless without a narrower declared root; under C it is the owner's wall.

Presented revision: `prd.md` SHA-256 `7445acacf92558aa5963914a9534f9cf85a1a62c2a3bf196a3008cfded967189`. Before: `4db53a49f738d44d1c681b887ba3010971e0edcf7499810bb49f718cbd9fc539`.
Change: frontmatter (review-round 3, review-status needs-decision). The dead starting-file line was replaced by a pointer to the decision. Acceptance and needs are unchanged.
No score recorded: a CONFLICT verdict is not scored until the choice is made.
Unresolved blocking findings: the executor/authority choice (user decision); rehome once chosen (coordinator).
Validation (read-only): `ls`/`rg` over cartridge.ctg main (`e8a4da3`) and ws/cartridge.ctg branch `transport-design` (`ba198f4`: `docs/transport.txt`, `src/node.rs` `spawn`, no `src/runtime.rs`/`src/service.rs`); memo.ctg `83bf1ad` (main = ws branch `transport`: `src/validation.rs`, `cartridge.json` `grant`); mcp/agent/proxy transport manifests; root decisions `the-tool-contract-is-a-memo`, `a-cartridge-brings-its-own-surface`, `tui-and-tools-are-cartridges`; work memo `a-tool-is-declared-by-its-memo`; `.cartridge/tools/memo-run`; coordination `PORTING.md`; needs resolution; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: rebase with its siblings in round 4 after the choice; retire under D.
