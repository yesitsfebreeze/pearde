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
commit: "e442bef2c9f07635f9e8b8e1d87a47193841569f"
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

Push catalog revalidation at e442bef: existing operation-rule and explain acceptance remains unchanged; semantic evaluator revision now reflects the recognized operation catalog.

## From the retired work memo

Folded 2026-09-15 from `work/improve-policy-operation-rules.md` (status open). The PRD state above is authoritative.

### Outcome

A profile can allow gitfs read/list while retaining ask/deny for writes, and can independently govern each memory mutation.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [headless-policy-approval-channel](../../../root/prds/headless-policy-approval-channel/prd.md).

### Footprint

Policy; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `policy.ctg/init.lua`
- `policy.ctg/cartridge.json`
- `cartridge.ctg/scripts/smoke.py`
- `agent.ctg/model_loop.rs`
- `mcp.ctg/service.rs`
- `proxy.ctg/service.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Table-driven fixtures cover tool and operation rules, defaults, unknown operations and deny precedence, including read-only gitfs access.
- [ ] MCP, proxy and native agent produce the same decision for equivalent trusted requests; a denied call causes zero backend mutation.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Add operation-scoped rules with explicit precedence: matching explicit deny wins; specific allow cannot override a broader deny; otherwise specific rule then tool rule then default. Reject ambiguous/malformed configuration and maintain existing tool-rule compatibility. Centralize interpretation for all callers.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test policy
just check policy
just smoke policy
```


### Compatibility and recovery

Parse old profiles unchanged and make new rules opt-in except explicit tested read-only defaults. Reject invalid configuration atomically and retain the prior valid policy. Policy remains separate from runtime sandbox containment.

### Handoff

Priority P0; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
