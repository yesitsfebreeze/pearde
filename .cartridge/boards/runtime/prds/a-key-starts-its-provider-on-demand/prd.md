---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: needs-decision
canonical-scope: a-key-starts-its-provider-on-demand
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

## From the retired work memo

Folded 2026-09-15 from `work/a-key-starts-its-provider-on-demand.md` (status open, estimate 2d). The PRD state above is authoritative.

> A composed profile starts only the chain something reaches, and declarations are read without spawning anything

### Outcome

Composing a profile does not start it. Declarations are read from manifests, and
a cartridge is started when something first reaches a key it provides — the
chain that key needs starting with it, and nothing else. A key that no cartridge
provides still fails immediately with the same named error as today, rather than
waiting for a timeout. A cartridge the profile enables but nothing reaches costs
one manifest read.

Scope is first-touch activation. Stopping an idle subtree again is deliberately
out of scope; nothing in this outcome depends on it.

### Check

- [ ] `zirkle run tool.memo '{"op":"types"}'` against the default profile starts
      `memo` and its chain and starts no `router`, `gitfs`, `pty` or `memory`
      process, asserted from the spawned-executable list, and prints the same
      reply as before.
- [ ] The same run spawns no `hello` process for an unreached cartridge.
- [ ] `zirkle run` for a key no cartridge provides fails with a message naming
      the key, without waiting out a timeout.
- [ ] A key whose provider needs a second cartridge activates both, in
      dependency order, proven by the fibers' transition events.
- [ ] `zirkle run ui` still brings up the full surface: reaching `ui` reaches
      everything it needs, so the terminal starts with the same services active
      as today, asserted from the landscape rows.
- [ ] Concurrent first touches of one key activate its provider once, proven by
      a single apply under a parallel-call test.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. `reconcile` instantiates every enabled entry and
`instantiate` spawns each one immediately (`core/loader.rs:703`, `:677`); reading
declarations runs `program hello` per enabled process cartridge
(`core/loader.rs:632`). `run_mode` then waits until some fiber both is active and
provides the key, and otherwise reports the stalled set (`core/loader.rs:553`).
So a `tool.memo` call today pays for the whole default profile, and an absent key
is distinguishable from a slow one only by the 30-second timeout. The runtime is
already reactive on key availability, and `Ctx::get` returns `Error::Inactive`
for a key with no active provider (`core/runtime.rs:527`) — that error is the
exact place where activation belongs instead.

### Spec

Two changes, in this order.

First, declarations without execution. With `provide` and `needs` in the manifest
from [a-cartridge-declares-what-it-needs](../../../root/prds/a-cartridge-declares-what-it-needs/prd.md), the composer builds its graph from
the folder scan alone. `hello` stops being a boot step and becomes what verifies
a cartridge at apply.

Second, demand activation. The composer registers each resolved key as claimable
by its provider without instantiating it. A `get` or service call for an
unactivated key activates that provider's subtree and waits for it, so the
first touch pays the start cost and later ones do not; a key with no registered
claim fails at once rather than timing out. Activation is single-flight per
entry: concurrent touches join one apply. `run_mode`'s wait loop reduces to
activating the requested key and awaiting that one fiber, and `stalled` keeps
reporting only entries that were asked for and failed, so a diagnostic never
starts anything.

Entries that must run without being called — the wrapped shell, the socket, the
UI — stay eager, declared as such by the profile entry rather than inferred.
`zirkle list` and the landscape report declared-but-unstarted as a state, so the
distinction between "not composed", "not started" and "failed" stays visible.
