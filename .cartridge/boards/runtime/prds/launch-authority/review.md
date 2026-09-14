# launch-authority — Discovery, direct, resolver and nested launches use trusted host-resolved policies while preserving scoped wire behavior and descendant teardown. — review

Canonical PRD: [@runtime/launch-authority](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [launch-authority](../../../root/reviews/round-1/launch-authority.md): reviewer 87/100; Split. Strong real-boundary probes, but scope includes both launch mediation and an unrelated SDK reload restoration; reconcile current SDK first and link this gate to the runner.
  Original SHA-256: `918b061ac90341253f04b3aa09c427abf1baa00ce6259dc3768268d67af3fd51`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 18 | Resolved hard dependencies and child links; external prerequisites require recorded owner handoff. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **93/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `890c0050f4a07dafcfd18ebf53a4e9a6f26117b5d4a971f173e4a8ddcbe55759`.

Reconciliation verdict: **REBASE**. The old scope (discovery, direct, resolver and nested routes; `Host::on_reload`; `src/runtime.rs` and `src/service.rs`; the `.pearde/.../command-adapter` evidence) no longer exists after the transport rewrite (cartridge.ctg `939e7d1`, `ee7e295`, `c9ef10b`). Most of the original outcome is delivered:
- Manifests are data (`src/loader/document.rs:10`).
- The single host start is `src/host/process.rs:35` into `crate::sandbox::command`.
- `cartridge.spawn` (`src/node.rs:364`) runs inside the node's wall.
- Host-only calls are refused ("not granted", `tests/host.rs:518`).

Still unproven: nested-child denial, spawn-nothing on a refused wall, and nested teardown. Revision: the scope is narrowed to those three proofs. The CLI `launch` branch is excluded, per decision `core-composes-and-the-cli-selects-services`.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | Remaining authority proof is bounded; −2: much of the outcome is already delivered, so the value is proof, not behavior. |
| Ownership and reuse | 19 | Runtime owns host, node and sandbox; reuses the existing test file and fixture helpers; −1: a Linux case is borrowed from another leaf. |
| Dependencies and slices | 17 | No hard needs; −3: acceptance 2 can only complete on the linux-policy runner, a soft completion dependency. |
| Acceptance and baseline | 18 | Real-child checks on macOS; −2: no baseline run recorded. |
| Failure and compatibility | 19 | No unconfined fallback, and the single route is preserved; −1: token and env inheritance of nested children is not examined. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Blocking findings: none. Finding: consider whether a nested child should inherit `HOST_TOKEN` from the node environment (`src/host/process.rs` sets it; tokio `Command` inherits env). It stays within the node's authority, so it is recorded rather than blocking.
Validation: `rg Command::new` across `src`, reading of `process.rs`, `node.rs` spawn, `sandbox.rs` and `tests/host.rs`, and the `just test runtime` routing in `cartridge-development.md`. No product gates were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: add the macOS nested-denial fixture.
