---
state: "open"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/policy.ctg"
work-kind: leaf
canonical-scope: bounded-search-guard-rules
---

# Unbounded repository searches are refused with a bounded retry

A recursive grep from a repository root or a find with no depth bound is the cheapest way for an agent to spend a minute and fill its context with nothing. `policy.ctg` already decides tool calls and explains its rules; add the rules that refuse an unbounded search before the shell sees it.

The refusal has to teach, not just block. The reason goes back to the caller naming what was unbounded and what a bounded form would be, so the next attempt is bounded rather than a retry of the same command. This is a policy rule and not a new cartridge: the decision point already exists, and a second gate in front of the shell would be a second place for the answer to disagree.

An explicit escape stays available — a caller that means it can say so and is allowed through, with the override recorded.

## Acceptance

- [ ] A recursive grep from a repository root and a find with no depth bound are each refused, and the refusal names the unbounded part and a bounded alternative.
- [ ] The same commands scoped to a subdirectory or given a depth bound are allowed.
- [ ] A refused command is recorded with its caller and the rule that refused it, readable afterwards.
- [ ] An explicit per-call override is honoured and recorded as an override; the rule is not disabled globally by one override.
- [ ] `policy.ctg`'s rule explanation names these rules and the conditions that trigger them, consistent with the decision the tool call actually receives.
- [ ] The rules are tested offline in `just test policy` over command fixtures, with no shell executed.

## Proof and recovery

Mechanism from `/Users/feb/dev/pi/packages/coding-agent/src/core/search-guard.ts` (201 lines at survey, verified present), which vetoes the call before the shell runs it and logs every block. Ported as rules rather than as a module: `policy.ctg` is pure Lua decisions today and this stays that way, with the logging going through the composition's existing observation journal.

Reconcile at implementation with `@policy/improve-policy-operation-rules` and `@policy/improve-policy-explain`, which touch the same rule surface.

Gates, cwd `/Users/feb/dev/cartridge`: `just test policy`, `just check policy`. Not run for this plan.
