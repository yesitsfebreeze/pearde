---

kind: work
level: 10
status: open
estimate: 4h
needs: [[extension-loader-plugin-tree]]
description: "`extension::inspect(root)` — the fiber tree with states, inject and provide, the effect labels, the services per realm and the listeners per event, as one serde value"
read_when: "debugging why a plugin is Pending, or wiring `memory plugins`"
---

# extension-inspect

## Do

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

## Check

`cargo nextest run -p extension` passes with a test that mounts a provider, a
dependent and a plugin with an unsatisfied inject, then asserts the inspect
value names the three fibers with their states, the dependent's target uid,
the pending fiber's missing key, the provider's `ctx.provide` effect label,
and one listener under its event name. The `memory plugins` command over the
RPC is [[memory-daemon-boots-a-root-context]]'s.
