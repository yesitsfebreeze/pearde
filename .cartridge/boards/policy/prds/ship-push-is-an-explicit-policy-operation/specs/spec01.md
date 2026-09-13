---
complexity: small
footprint:
- init.lua
- .cartridge/tests/policy.rs
- .cartridge/tests/contract/Cargo.lock
- .cartridge/docs/policy.md
---

# Recognize recorded push through the existing operation policy

Add push to known_operations.ship. Reuse the existing pure evaluator and validation;
no separate capability, approval state, transport or containment mechanism. Existing
rules retain their order: tool deny wins, otherwise explicit operation decision
wins, then the tool grant and configured/default fallback. The actual default is
ask; default=deny remains deny. No new implicit allow is introduced. A blanket
explicit ship tool allow covers its recognized operations; a specific push deny
can restrict that grant. Unknown operations still fail closed. Preview, commit and
reconcile remain separate requests with their full inputs visible to consumers,
but phase-specific rule semantics are not invented by this operation-only policy.

Both policy and policy.explain must agree for push. Explanations remain observations
and never grant approval or execute the tool. Bump the evaluator semantic marker
from policy-evaluator:2 to :3: the recognized operation catalog changes decisions
under an otherwise identical configuration. This revision is not a permission token.
Invalid replacement configurations must leave the prior valid policy callable.

Use the current policy-owned runtime fixture and actual MCP process with a counted
ship producer to prove allowed push executes once, denied/ask push executes zero
calls, and tool deny still overrides operation allow. Table-test preview/commit/
reconcile under default ask, configured deny, explicit operation allow/deny/ask,
blanket tool allow and unknown operations. The existing MCP/proxy/native-agent
suite remains the regression gate. No real Git remote or credential is needed for
this policy contract; actual GitFS publication/reconciliation belongs to its owner.

The one-line fixture Cargo.lock update resolves the current runtime's sha2 dependency
and introduces no new policy dependency. The parent shipping rollup must require
this leaf and reverify the prior policy receipts after integration. Keep all source
changes policy-owned and leave shared board/map collection to the coordinator.

## Acceptance

- [x] Real policy and policy.explain recognize push configuration and agree on defaults, exact precedence, unknown operation rejection and semantic revision without executing any producer.
- [x] Actual MCP executes exactly one allowed push producer call; deny/ask/tool-deny cases execute zero calls and preserve explicit failure/approval behavior.
- [x] Invalid replacement retains the previous valid policy and the complete public policy suite passes against current source dependencies.

## Verify and Proof

```sh
bash .cartridge/tests/run
```

The baseline uses the real runtime/Lua policy with tools.ship=allow and observes
push denied as unknown, so the new GitFS operation cannot be authorized through
this surface. Retain exact baseline command, source revision, failure log and the
removed probe. Inherited rounds1–2 apply; independent round3 precedes implementation.
