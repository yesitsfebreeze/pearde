# The shipped policy defaults to ask — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/the-shipped-policy-defaults-to-ask` (`prd.md`).
Scope: one leaf. A fresh composition asks before a mutating tool runs.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **CONFLICT** (needs a user decision).

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `af44ffc850493ba5820c794798c2c6561a60635e1b9b25b455ebd760e78d0a07` (frontmatter only; prior text `e3a92125e897202e5d9d98ddaadb2c5cb98dba55de9942a470a3533068faab40`).
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- `policy.ctg` in root and `ws/policy.ctg` `e478864`;
- prd.ctg `077e57a2`, dirty.

Evidence:

- **The target file is gone.** `b1494bb` ("This repository is the base, not a composition") emptied `cartridge.ctg/.cartridge/config.lua` to `return {}` on both lines. The `repo:` and starting file are wrong, and the runtime is no longer the owner.
- **Where the posture lives now:**
  1. `policy.ctg/cartridge.json` declares `default` with `"default": "allow"`, identical in root and `ws/policy.ctg`. Its doc reads: "Approval, where it happens, happens at the client".
  2. `policy.ctg/.cartridge/help.md` states the design: policy "never executes the target, prompts anyone, or grants sandbox capability, so approval stays with whichever client made the call".
  3. The root composition `/Users/feb/dev/cartridge/.cartridge/config.lua:39-57` (untracked) pins `default = "allow"` with a comment explaining the choice.
- **Decision constraint.** Under `a-cartridge-brings-its-own-surface` (2026-09-14), per-tool rules belong to the composition's `config.lua`, and the policy cartridge knows no tool.
- **Acceptance 3 is already met.** `cartridge settings` prints which file settled each key (root `config.lua:7-9`; `cli/settings.rs::host_settled`).

The PRD's outcome, "ask" by default, contradicts the current design statement in the policy cartridge. Alternatives for the user:

- **A. Keep allow-by-default.** Retire this leaf. The client-side approval and the observation journal are the control.
- **B. Flip the declaration.** Set `policy.ctg/cartridge.json` `default` to `"ask"` and let the root composition keep its explicit `allow` as the developer override. Rehome the leaf to `@policy` with `repo: /Users/feb/dev/cartridge/policy.ctg` and gate `just test policy`. This does not conflict with the surface decision, because policy still names no tool.
- **C. Ask at setup.** Keep the declaration at `allow`, but have policy's own `cartridge setup` question write `policy = { default = "ask" }` into new projects. That is owned by `policy.ctg`; `cartridge.ctg/src/cli/setup.rs` must not name policy.

Recommended default if the user wants the original intent: B. It is one declared value and needs no new mechanism.

Result: no score (verdict round). Status: `needs-decision`.
Unresolved blocking findings: owner and posture need a user choice between A, B and C.
Validation (read-only):
- `cat` of `cartridge.ctg/.cartridge/config.lua` on both lines and `git log -S'default = "allow"'` in `cartridge.ctg`;
- reads of the root `.cartridge/config.lua`, `policy.ctg/cartridge.json` (root and ws) and `policy.ctg/.cartridge/help.md`;
- `ls prd.ctg/.cartridge/boards/policy/prds`;
- `shasum -a 256`.

Rounds used / remaining: 2 / 3.
Next action: the coordinator asks the user. On B or C, rehome to the `policy` board before revising.
