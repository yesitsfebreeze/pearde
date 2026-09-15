---
repo: /Users/feb/dev/cartridge/policy.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: policy
work-kind: leaf
review-round: 3
review-status: needs-decision
canonical-scope: improve-policy-resource-scope
needs:
- '@policy/improve-policy-operation-rules'
footprint:
- /Users/feb/dev/cartridge/policy.ctg/init.lua
- /Users/feb/dev/cartridge/policy.ctg/cartridge.json
---

# Constrain granted file operations to declared resources

Define a supported operation target schema and canonical root identity. The mutating backend must bind the authorized target to its actual open/commit operation using platform-supported handle-relative/no-follow semantics; a string canonicalization followed by an unconstrained open is insufficient. Opaque shell commands require separate permission and make no path-confinement promise.

## Acceptance

- [ ] Traversal, outside symlink and a symlink swapped between preview and open cannot write outside the authorized root.
- [ ] A target revision/root change invalidates the preview before mutation.
- [ ] Unsupported platform/operation binding refuses scoped execution with an explicit reason rather than pretending the generic shell is confined.

## Proof and recovery

Start at [init.lua](../../../../../../policy.ctg/init.lua), [cartridge.json](../../../../../../policy.ctg/cartridge.json).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test policy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-policy-resource-scope`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-policy-resource-scope.md` (status open). The PRD state above is authoritative.

### Outcome

A grant can restrict repository and path targets with deterministic checks before a mutating backend call.

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
- [ ] A permitted edit inside a temporary allowed root succeeds while traversal, symlink escape and another repository are rejected.
- [ ] Changing a target after preview invalidates authorization; operations with opaque effects do not falsely claim path confinement.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. This is a large slice: use that bounded probe to split implementation into smaller child outcomes if more than one independent state transition or migration is required.
2. Define which operations have inspectable targets and validate canonical workspace-relative resources, including symlink/path traversal cases. Shell strings cannot be made safe by path matching: require separate shell permission and leave OS containment to the sandbox. Bind any approved preview to the arguments actually executed.
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

Priority P1; scope size L (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-policy-operation-rules](../improve-policy-operation-rules/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
