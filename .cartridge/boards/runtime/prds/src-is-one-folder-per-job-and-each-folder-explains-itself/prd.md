---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: rollup
capability-owner: runtime
needs:
- "@runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/declared-settings-live-in-settings"
- "@runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/the-correlation-id-and-the-diagnostics-sink-are-two-folders"
- "@runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/composition-is-one-folder-for-what-is-installed-enabled-and-bound"
- "@runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/the-ring-and-events-leave-the-transport-file"
- "@runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/every-src-folder-has-a-fresh-eyes-readme-and-the-audit-demands-it"
---

# src is one folder per job and each folder explains itself

## Outcome

A person who opens `cartridge.ctg/src` for the first time sees one folder per responsibility, one level deep, and a short README in each folder that says what it does. Nothing behaves differently afterwards; only where code lives changes.

Today the jobs are tangled. `transport/cartridge.rs` holds event routing, the channel ring and the connection server in 1023 lines. `transport/settings.rs` is the settings schema and has nothing to do with transport. `ledger/`, `loader/` and `host/plan.rs` share one job: deciding what is installed, enabled and bound. `ledger` is an install registry, not a log, and its name collides with the memory ledger. `trace/mod.rs` holds both the correlation id and the diagnostics sink.

## Target layout

```
asp/          One interface to the world: merges what every cartridge says about an entity and ranks it.
ring/         What happened: per-channel sequence, the last 1024 envelopes, replay from a cursor, live subscribers.
events/       How cartridges talk: who listens to what, schema check, send with timeout, emit, bail, gather, ask, and serving cartridge connections.
transport/    Bytes only: socket and pipe adapters, frame codec, bind and adopt, the JSON-RPC peer.
composition/  What is installed and enabled: reads init.lua and manifests, scans cartridges, binds each need to a provider, yields the Plan.
host/         The daemon: starts, stops and replaces cartridge processes, reconciles to the Plan, hot reload, takeover.
node/         One cartridge process: runs its Lua entry and hands it the cartridge API.
lua/          The interpreter with a memory and instruction budget.
sandbox/      Confines a cartridge process, per operating system.
policy/       Decides allow, ask or deny, asks the person, and records trusted files. (`trust/` until `@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow` lands.)
settings/     Declared settings: spec, defaults, merge, validation.
trace/        The correlation id carried through a request.
log/          The diagnostics sink: redaction, bounded queue, capped file.
error/        The crate's error type.
cli/          The `cartridge` command.
```

Dependencies point one way: `transport` ← `ring` ← `events` ← `composition` ← `host`; `asp` reads `ring` and `composition`.

## Decision (2026-09-19, user)

The user asked for the folders ordered by responsibility, naming ASP, a ring and events, "and the rest ordered in the same manor, per job, still only one module folder deep", and for each module "an readme explaining what the module does for someone who doesnt know about the system (fresh eyes explanation, short no prose on the point for fast understanding)". No folder is named fabric: the user corrected that "fabric and asp are the same thing" (note `asp-is-the-fabric-with-a-better-protocol`).

## Decision (2026-09-19, coordinator)

The names `composition` and `log`, and the split of `trace/`, are the coordinator's. The user was asked and had not answered when this was filed; a rename costs nothing until the child that introduces the folder is claimed.

## Order

The first three children are independent of each other. The fourth touches `transport/cartridge.rs`, which `@runtime/a-listener-subscribes-to-event-types` and the ring PRDs under the ASP rollup also name in their footprints and `Start at` anchors, so it lands before them and retargets them. The README child lands last.

## Acceptance

- [ ] Every child is done.
- [ ] `src/` holds exactly the folders listed above, one level deep, and `transport/cartridge.rs`, `ledger/` and `loader/` no longer exist.
- [ ] The names of the tests `just test runtime` runs are the same before the first child and after the last, and all pass.
- [ ] `just check runtime`, `just audit` and `just isolation` report nothing.
