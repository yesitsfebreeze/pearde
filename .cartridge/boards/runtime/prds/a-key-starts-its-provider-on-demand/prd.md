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
canonical-scope: a-key-starts-its-provider-on-demand
needs:
- '@runtime/the-profile-is-the-root-composer'
---

# a-key-starts-its-provider-on-demand

Start by comparing current loader/resolver behavior with the old core-path observations. Implement only a demonstrated missing first-touch transition; retain manifest-only discovery, per-entry single-flight activation and explicitly eager profile entries. Idle stopping remains outside this item.

## Acceptance

- [ ] Two concurrent requests activate the same provider once and share its result/error; dependency order is observed from lifecycle events.
- [ ] A missing key fails immediately, while a declared failed provider reports its actual startup failure.
- [ ] A memo-only request starts no unrelated process or hello; explicit eager UI/socket entries still initialize as configured and reload resets only the affected generation.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [a-cartridge-declares-what-it-needs](../../../../memos/work/root--a-cartridge-declares-what-it-needs.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-key-starts-its-provider-on-demand`; maximum five rounds.
