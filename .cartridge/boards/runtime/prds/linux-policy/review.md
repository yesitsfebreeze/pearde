# linux-policy — Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement. — review

Canonical PRD: [@runtime/linux-policy](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [linux-policy](../../../root/reviews/round-1/linux-policy.md): reviewer 89/100; Revise. Require a named executable Linux verification job/environment before claim; preserve runtime denial proof and unsupported-kernel refusal as distinct gates.
  Original SHA-256: `6d3aad5283d8981676c7821ee2d04d5f0a8c005ff2e424be286a69ee010777c0`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 13 | Linux enforcement needs a real runner with a recorded kernel/Landlock ABI; this checkout supplies only a refusal implementation. |
| Acceptance and baseline | 17 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **86/100 — FAIL**.
Finding: Linux enforcement needs a real runner with a recorded kernel/Landlock ABI; this checkout supplies only a refusal implementation.
Blocking review findings: Linux enforcement needs a real runner with a recorded kernel/Landlock ABI; this checkout supplies only a refusal implementation.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: resolve the named prerequisite and review a substantive revision.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `ae23a905edd60bf7d056a5f2cc255af69fe982df9e7ecb50d9efd3e56e5b6237`.

Reconciliation verdict: **REBASE**. The outcome is unchanged and still undelivered: `src/sandbox_linux.rs` (17 lines) refuses all execution. The old starting files `src/runtime.rs`/`src/service.rs` and the `.pearde` command-adapter link are gone. Revision: current files named; macOS profile semantics adopted as the reference, including sockets directory and semaphores (`81a138e`, `92b7a5d`); the dead link dropped. The round-2 blocker ("no runner identified") is addressed. `docker context ls` shows an active `orbstack` context and `limactl` is installed (no instance). Step one records kernel, Landlock ABI and seccomp, with an explicit stop condition.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Unblocks all Linux execution; clear parity target; −1: UDP denial needs seccomp, not Landlock, so the implementation must use both. |
| Ownership and reuse | 19 | Runtime `sandbox` module and existing test file; −1: the container invocation is not yet a recipe. |
| Dependencies and slices | 17 | No hard needs; the runner is named with a stop condition; −3: runner Landlock ABI not yet observed (docker was not run in this pass). |
| Acceptance and baseline | 18 | Real-child allow/deny, refusal, and compile-vs-enforce separation; −2: no baseline. |
| Failure and compatibility | 18 | The refusal remains the fallback and partial policy is forbidden; −2: kernels with partial ABI support need a recorded minimum. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Blocking findings: none (the round-2 blocker is resolved by naming a runner plus a stop condition). Non-blocking: if the OrbStack kernel lacks ABI 4, choose a Lima VM image with a newer kernel before implementation.
Validation: `wc -l src/sandbox*.rs`, reading of `sandbox.rs`, `which docker limactl orb`, `docker context ls`, `limactl list`. No product gates or containers were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: probe the container kernel and ABI; record the output in this review before specs.
