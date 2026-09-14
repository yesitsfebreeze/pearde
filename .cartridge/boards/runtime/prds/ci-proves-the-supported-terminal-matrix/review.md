# Repository CI runs the gates and reports terminal coverage explicitly — review

Canonical PRD: [@runtime/ci-proves-the-supported-terminal-matrix](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [ci-proves-the-supported-terminal-matrix](../../../root/reviews/round-1/ci-proves-the-supported-terminal-matrix.md): reviewer 64/100; Rewrite. Replace ignored builtin/memory bootstrap and obsolete kern pin with current recursive submodules; prove the actual Linux/macOS jobs and full gate failure propagation.
  Original SHA-256: `7247b7330fe892145d993a07a27890af60351ddc0231c4eee0bf9ada0c595824`.

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

Reconciliation verdict: **CONFLICT**. Where CI runs and what it gates is now a user choice:
- The composed root `/Users/feb/dev/cartridge` has no git remote (`git remote -v` prints nothing), so a root workflow cannot run.
- `cartridge.ctg` has a remote but is "the base, not a composition" (b1494bb), so composed gates do not belong there.
- The Linux host refuses all node execution until Landlock/seccomp exist (`cartridge.ctg/src/sandbox_linux.rs`; open leaf `@runtime/linux-policy`), so a Linux job cannot pass the host tests.
- `.cartridge/memos/note/release-status.md` lists failing workspace tests (gitfs 6, harness 1, mcp 1, pty 2, router 2, sessions 8).
- The old spec (`builtin/memory` kern pin, `core/tests` Python probe, `scripts/ci-*.sh`) and its external prerequisite `fresh-checkouts-can-run-the-gates` (vendored kern bootstrap) are obsolete now that memory.ctg is a submodule.
- A per-owner pattern already exists: `memory.ctg/.github/workflows/ci.yml` checks out `cartridge.ctg` beside itself.

Presented revision (frontmatter status only changed): `f4fdf9d8d81eb7cc9c15e7cb444da2793d6a76ff84c0e38bbdc659ee6cd133e1` (stale body digest `477dcf8593cb990c5edab500845e4564a73f9b0cd3a8b3b4e48a5ae86eb03d5c`).

Alternatives for the user:
- A. Publish the composed root with a remote. Put `.github/workflows/ci.yml` there with a recursive submodule checkout (read token as in memory.ctg), a gating macOS job for `just check`/`just test`, and a Linux job that runs `just check` and reports tests as blocked on `linux-policy`. Recommended.
- B. Per-owner CI only, following memory.ctg: `cartridge.ctg` CI runs its own `cargo test --workspace` on macOS, and no composed matrix exists.
- C. Defer until `linux-policy` lands and the release test failures are fixed.

Not scored: needs a user decision. Unresolved blocking finding: CI home and Linux policy dependency.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `git remote -v`; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: user decision, then one rebase revision (repo, needs `@runtime/linux-policy` for the Linux gate, current gates).
