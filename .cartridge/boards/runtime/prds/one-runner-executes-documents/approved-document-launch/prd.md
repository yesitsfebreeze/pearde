---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: needs-decision
canonical-scope: one-runner-executes-documents
needs:
- '@memo/one-document-serves-every-reader/executable-document-validation'
- '@runtime/launch-authority'
---

# Only an approved frozen invocation reaches spawn

Bind owner, source digest, recipe, argv, cwd and policy using host-resolved launch authority.

## Acceptance

- [ ] Changing source after approval either executes the frozen bytes or refuses.
- [ ] Forged identity, stale revision, invalid cwd and denial spawn zero processes.
- [ ] Real launch-path fixtures establish the supported platform's containment.

## Proof and recovery

Decision needed first (review round 3: CONFLICT). The starting files `cartridge.ctg/src/runtime.rs` and `src/service.rs` are gone, and on the transport route the base runs no tool commands. Nothing executes memo's frozen invocation yet (`memo.ctg/src/validation.rs`, `launch_authorized: false`). The user must choose who executes it, and inside whose grant; the concrete alternatives are in [review.md](review.md), round 3. The acceptance above is executor-neutral. Do not specify or implement it until that choice is recorded.

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-runner-executes-documents`; maximum five rounds.
