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
review-status: delivered-pending-verification
canonical-scope: extension-inspect
needs:
- '@runtime/extension-loader-plugin-tree'
---

# extension-inspect

Map the obsolete extension Inspect proposal onto current runtime inspection and Landscape. Retain a read-only, bounded snapshot of owner identity, phase, provided/injected keys, missing dependencies and owned effects without calling plugin code. No removed extension crate is rebuilt inside memory.

## Acceptance

- [ ] A provider, dependent and pending fixture yield correct owner/generation and missing-key evidence.
- [ ] Snapshot collection does not await arbitrary user callbacks while holding registry locks and respects output limits.
- [ ] Scoped/private providers do not leak; unavailable fields are labelled unknown and existing runtime status callers remain compatible.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `extension-inspect`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--extension-inspect.md` (status open, estimate 4h). The PRD state above is authoritative.

> `extension::inspect(root)` — the fiber tree with states, inject and provide, the effect labels, the services per realm and the listeners per event, as one serde value

### Do

- `Inspect { fibers: Vec<FiberView>, services: Vec<ServiceView>, listeners: BTreeMap<String, Vec<ListenerView>> }`
  with `FiberView { uid, name, parent_uid, state, inject, provide, entry: Option<String>, target: Option<Vec<(String, u64)>>, effects: Vec<EffectMeta> }`,
  `EffectMeta { label, children }` (the labels `ctx.effect` collects, nested
  as in the vendored `getEffects`), `ServiceView { name, realm, provider_uid, active }`,
  `ListenerView { fiber_uid, prepend, global }`. All `serde::Serialize`.
- `extension::inspect(root: &Context) -> Inspect` reads every lock once and
  awaits nothing.
- A `Pending` fiber's view names the injected keys that resolve to no
  `Active` provider in its realm, which is the answer to "why is it not
  running".

### Check

`cargo nextest run -p extension` passes with a test that mounts a provider, a
dependent and a plugin with an unsatisfied inject, then asserts the inspect
value names the three fibers with their states, the dependent's target uid,
the pending fiber's missing key, the provider's `ctx.provide` effect label,
and one listener under its event name. The `memory plugins` command over the
RPC is [memory-daemon-boots-a-root-context](../../../memory/prds/memory-daemon-boots-a-root-context/prd.md)'s.
