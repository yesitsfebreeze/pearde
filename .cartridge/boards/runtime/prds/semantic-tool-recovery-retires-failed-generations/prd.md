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
canonical-scope: semantic-tool-recovery-retires-failed-generations
---

# semantic-tool-recovery-retires-failed-generations

Rehome editor/LSP provider lifecycle to the actual host tooling owner; current memory scope excludes that automation. First identify a concrete maintained provider and teardown API before implementation. Preserve generation-safe cancellation and the positive-control distinction between unavailable/indexing and a genuine empty result.

## Acceptance

- [ ] A failed initialization is retired before another query can select it; retry creates one new owned generation.
- [ ] A stale callback cannot invalidate its healthy successor and cancellation waits for owned teardown without touching another session's editor.
- [ ] If no current maintained provider can be identified, this remains a named ownership question rather than invented memory work.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `semantic-tool-recovery-retires-failed-generations`; maximum five rounds.
