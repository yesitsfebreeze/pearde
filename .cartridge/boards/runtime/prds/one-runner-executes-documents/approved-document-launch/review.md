# Only an approved frozen invocation reaches spawn — review

Canonical PRD: [@runtime/one-runner-executes-documents/approved-document-launch](prd.md). Reviewer: `/root` (self-review).
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

Reconciliation verdict: **CONFLICT** (needs a user decision).

Why not REBASE: the parent `one-runner-executes-documents` (round 3, FAIL) recommended "memo executes its own approved invocation inside its grant" and left the rehome to the coordinator or user. Reviewers of the client leaves (`@agent/agent-document-client`, `@proxy/proxy-document-client`, and in this pass `@mcp/.../client-document-contract` and `mcp-document-client`) found the client side SUPERSEDED. This reviewer's reading of source and decisions:

1. **The outcome is still wanted.** Decision `the-tool-contract-is-a-memo.md` (accepted 2026-09-12) is not superseded by a later decision, and root work memo `a-tool-is-declared-by-its-memo.md` is open. Its Check requires a tool memo to be "discovered, described and called through the same `tool.*` surface a cartridge tool is — no Rust change to add it".
2. **Nothing executes a document today on either branch.** memo emits a frozen invocation (`src/validation.rs`: `command {program: just, argv}`, `launch_authorized: false`). memo `83bf1ad` has no `just` process start, although port `3dc1f61` added `grant.exec: ["git","just"]`. cartridge.ctg has no host runner: `src/runtime.rs` and `src/service.rs` are gone, and the base "runs no commands" (`creating-cartridges.txt`: `commands` are "documentation, never run by the base"). The only executor is the trusted dev adapter `.cartridge/tools/memo-run`.
3. **The executor placement is a genuine open choice, not a path fix.** On the events model (ws/cartridge.ctg `transport-design` `ba198f4`, `docs/transport.txt`), every event is declared statically in a `cartridge.json` and checked before start, and "a tool is an event its owner listens to". That makes the work memo's "no Rust change" per-document discovery contradict static declaration unless someone changes it. A grant is per node, so the choice of executor decides whose authority a recipe runs under. Decision `a-cartridge-brings-its-own-surface.md` (2026-09-14) and `tui-and-tools-are-cartridges.md` pull against a base-owned runner. Choosing among the options below changes the repo, board, grant and acceptance of all three leaves. It is a material user choice.

Concrete alternatives:
- **A. Owner-declared tool memos (recommended default).** A cartridge that ships a tool memo declares `tool.<name>` in its own `cartridge.json` (schema from the memo). Its `init.lua` listener asks `memo` (declared need) to validate the memo and freeze the invocation, then runs the frozen argv with `cartridge.spawn` inside its *own* grant (`grant.exec: just`). Approval stays the clients' existing policy `ask` on `tool.*`. Pros: no base change; authority stays with the owner; fits both 2026-09-14 decisions and static events. Cons: one manifest entry per tool memo, which amends the work memo's "no Rust change" to "no Rust change, one declaration". Leaves rehome per owner; the first owner would be the one shipping the first tool memo.
- **B. memo executes.** memo adds a run operation (for example `tool.memo` op `run`) that re-validates the digest and spawns the frozen `just` argv inside memo's grant (`read/write /`, `exec just`). Pros: one runner, reuses validation in-process. Cons: every owner's recipe runs with memo's broad authority; documents are not individual `tool.*` events, so per-tool discovery and policy keys are lost; memo gains execution behavior for other cartridges' records. Leaves rehome to the memo board (the parent's current recommendation).
- **C. The base derives and runs tool memos.** At plan time the base reads an owner's `.cartridge/documents` tool memos, declares their events and spawns their recipes inside that owner's wall. Pros: exact work-memo shape and per-owner authority. Cons: behavior in core, contradicting `tui-and-tools-are-cartridges` and cartridge.ctg `b1494bb` ("the base, not a composition"). Leaves stay on the runtime board, rebased to `src/host/plan.rs` and `src/node.rs`.
- **D. Retire execution.** Tool memos stay documentation plus validation; `memo-run` remains the trusted development adapter; decision `the-tool-contract-is-a-memo` is amended. All three leaves and the parent are retired.

Presented revision: `prd.md` SHA-256 `d7f248e67d9fdd73b9fe33be407e38e35a61bf30d0c2ba2117a50f4a2807352c`. Before: `b7094076e544c2bc16e985ceefc07a1cb8f33e16ba47169e87f50a596b148c70`.
Change: frontmatter (review-round 3, review-status needs-decision). The dead starting-file line was replaced by a "Decision needed first" pointer to these alternatives. Title, acceptance and needs are unchanged. The need `@runtime/launch-authority` (passed round 3) stays valid under A–C, and `@memo/.../executable-document-validation` is specced with an implementation at memo `45d5a54`.
No score recorded: a CONFLICT verdict is not scored until the choice is made. The stale text would fail on ownership and dependencies regardless.
Unresolved blocking findings: (1) the executor/authority choice above (user decision); (2) rehome of all three leaves once chosen (coordinator).
Validation (read-only): `ls`/`rg` over cartridge.ctg main (`e8a4da3`) and ws/cartridge.ctg branch `transport-design` (`ba198f4`: `docs/transport.txt`, `src/node.rs` `spawn`, no `src/runtime.rs`/`src/service.rs`); memo.ctg `83bf1ad` (main = ws branch `transport`: `src/validation.rs`, `cartridge.json` `grant`); mcp/agent/proxy transport manifests; root decisions `the-tool-contract-is-a-memo`, `a-cartridge-brings-its-own-surface`, `tui-and-tools-are-cartridges`; work memo `a-tool-is-declared-by-its-memo`; `.cartridge/tools/memo-run`; coordination `PORTING.md`; needs resolution; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied. User feedback: none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator asks the user to pick A–D. Then rebase this leaf and its two siblings in one round (round 4) against the chosen owner.
