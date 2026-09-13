---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: every-enabled-tool-ships-a-contract-probe
---

# Every enabled tool ships a contract probe

Use the owner-capability migration as canonical delivery. A probe declaration names capability identity, recipe revision, fixture requirements, allowed effects, timeout and expected assertions; discovery reads metadata only. One provider owns both the capability and its probe.

## Acceptance

- [ ] Every exposed capability has a resolvable probe or an explicit unverified reason; disabled capabilities do not appear callable.
- [ ] Merely listing or reading probes starts no subprocess/model/store, and malformed fixture/effect declarations are rejected before execution.
- [ ] Probe changes invalidate previous evidence and the runtime census derives from actual exposure rather than a central handwritten list.

## Proof and recovery

Start at [settings.md](../../settings.md), [justfile](../../../../../../justfile).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [debug-mode-opens-and-closes-from-the-shell](../../../../memos/work/root--debug-mode-opens-and-closes-from-the-shell.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `every-enabled-tool-ships-a-contract-probe`; maximum five rounds.
