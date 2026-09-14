# extension-inspect — review

Canonical PRD: [@runtime/extension-inspect](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [extension-inspect](../../../root/reviews/round-1/extension-inspect.md): reviewer 30/100; Rehome. The proposed extension crate is absent and excluded from memory; compare the requested read-only snapshot with existing runtime inspection and Landscape first.
  Original SHA-256: `a3368808d5844ef316c1b8fdbd358b9482414239101208b473b55edb1ecbf32e`.

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

Reconciliation verdict: **DELIVERED**. The proposed extension crate is gone, and per the direction digest "Landscape" became `Host::snapshot`. The read-only inspection is in the host:
- `status()` (`cartridge.ctg/src/host/mod.rs:202`) gives each entry's state, error, the `waiting` needs that have no active listener, and its events, needs and listen.
- `snapshot()` (mod.rs:673) gives entries with dependencies (the listeners per need), sources and context.
- Both read synchronous locks and await nothing.
- Nodes reach them through `cartridge.host("status"|"snapshot"|"cartridges")`.
- Tests `a_missing_listener_waits_and_says_for_what` and `a_cartridge_asks_the_host_what_only_the_host_knows` (`.cartridge/tests/unit/src/tests/host.rs:479,496`) cover pending/missing-need evidence and provider/dependent visibility.
- `bridge.status` reports the generation (mod.rs:762).

Small residuals, not worth a separate leaf unless asked: `status`/`snapshot` do not carry the generation, and there is no explicit output bound. The scoped/private provider concept no longer exists (per-edge tokens replace it). The dependency on `extension-loader-plugin-tree` is not needed. The PRD still links the absent `src/runtime.rs`/`src/service.rs`.
Presented revision (frontmatter status only changed): `eda60c9cf118f5cf4a853c8aa703bf348bc8466507d29585aadbc7e9021f06c2` (stale body digest `5ea160e19c6b3ee784f1a5af82fa497e8305002e32bce870ff80bd8016eaf02c`).
Verification to close: from cwd `/Users/feb/dev/cartridge`, `just test runtime`, confirming the two named tests pass. Not run in this pass. `state:` is left unchanged.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `git remote -v`; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: coordinator runs verification and decides done/retire.
