---
state: "specced"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
blast-radius: low
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/transport/settings.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/transport/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/settings
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/settings.txt
---

# declared settings live in settings

## Outcome

The settings schema lives with the settings. `src/transport/settings.rs` (`Kind`, `Spec`, `merge`, `get`, `set`, `defaults`, `apply`, `undeclared`, `declared`) moves to `src/settings/spec.rs`. It describes and validates declared settings and carries no transport concern.

## Acceptance

- [ ] `src/transport/settings.rs` does not exist and `src/settings/spec.rs` holds its contents unchanged apart from paths.
- [ ] Every `transport::settings` path in the crate and its tests names `settings::spec`; nothing re-exports the old path.
- [ ] `src/settings/README.md` exists in the shape the parent's README child defines.
- [ ] `just test runtime` runs the same test names as before and all pass; `just check runtime` reports nothing.

## Proof and recovery

A move and a path rewrite, no behaviour change. Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`. Not run. Recovery is `git revert`.
