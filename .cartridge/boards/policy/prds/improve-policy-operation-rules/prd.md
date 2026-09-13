---
repo: /Users/feb/dev/cartridge/policy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: policy
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: improve-policy-operation-rules
footprint:
- init.lua
- .cartridge/tests
- .cartridge/memos/routine/policy-tests.md
- .cartridge/docs/policy.md
commit: "a3f5cffface2b7b2bc9ed26d9e55da0ee0f4be2d"
---

# Authorize individual operations with stable precedence

A profile can allow gitfs read/list while retaining ask/deny for writes, and can independently govern each memory mutation.

## Acceptance

- [x] Table-driven fixtures cover tool and operation rules, defaults, unknown operations and deny precedence, including read-only gitfs access.
- [x] MCP, proxy and native agent produce the same decision for equivalent trusted requests; a denied call causes zero backend mutation.

- [x] Parse old profiles unchanged and make new rules opt-in except explicit tested read-only defaults. Reject invalid configuration atomically and retain the prior valid policy. Policy remains separate from runtime sandbox containment.

## Proof and recovery

Start at [init.lua](../../../../../../policy.ctg/init.lua), [cartridge.json](../../../../../../policy.ctg/cartridge.json).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test policy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-policy-operation-rules`; maximum five rounds.

## Verified implementation — 2026-09-13

`bash .cartridge/tests/run` and public `just test policy` pass. The rule matrix
covers 18 cases; four invalid replacements preserve the previous policy. MCP,
proxy and native Agent fixtures execute the allowed read exactly once and the
denied write zero times. Existing defaults stay unchanged and the complete
configuration is validated before publication. No model request is made.

## Reverification for GitFS inspection

GitFS introduces a read-only diff operation. Its reviewed inspection spec adds
diff to this owner's known-operation set without changing policy defaults or
precedence. The unchanged policy gate passed, and the real GitFS MCP proof
permits diff while denying every mutation. Recollect this owner's proof against
the one-line operation registration; prior receipt is collection-bdef8e6a.md.

## Reverification after policy explanations

The shared evaluator now also serves read-only explanations at a3f5cff. The
operation-rule contract is unchanged; rerun the expanded parity and actual
consumer gates against the integrated source. Prior receipt is preserved.
