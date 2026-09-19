---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
blast-radius: mid
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/ledger
  - /Users/feb/dev/cartridge/cartridge.ctg/src/loader
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/plan.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/composition
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lib.rs
---

# composition is one folder for what is installed enabled and bound

## Outcome

One folder answers "what is installed, what is enabled, and which provider does each need bind to". Today that job is spread over `src/loader` (reads `init.lua`, the entries and each `cartridge.json`), `src/ledger` (scans the installed cartridges and resolves a need to its provider) and `src/host/plan.rs` (turns both into the `Plan` and the event directory). They become `src/composition`: `document.rs`, `entries.rs`, `installed.rs` (today's `ledger`) and `plan.rs`.

The name `ledger` goes. It is an install registry with no time axis, and the word already means the memory cartridge's daily record.

## Acceptance

- [ ] `src/ledger`, `src/loader` and `src/host/plan.rs` do not exist; `src/composition` holds their contents unchanged apart from paths and the `Ledger` to `Installed` registry rename.
- [ ] Every caller in the crate, the CLI (`cli/listing.rs`, `cli/project.rs`) and the tests names the new paths; nothing re-exports an old one.
- [ ] `ASP.md` and `docs/` name the new paths wherever they named the old ones.
- [ ] `src/composition/README.md` exists in the shape the parent's README child defines, and `src/host/README.md` no longer claims planning.
- [ ] `just test runtime` runs the same test names as before and all pass; `just check runtime` and `just isolation` report nothing.

## Proof and recovery

A move and a path rewrite, no behaviour change. `loader/document.rs` is the manifest schema that peer ASP work edits, so check `git status` in `cartridge.ctg` before claiming. Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`, `just isolation`. Not run.
