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
review-status: passed
canonical-scope: a-cartridge-installs-from-its-source
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/src/cli/setup.rs
- /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/cli/setup.rs
---

# a-cartridge-installs-from-its-source

`cartridge setup` installs a repository cartridge at a recorded commit, and a later run finds the same tree. Today `install` in [setup.rs](../../../../../../cartridge.ctg/src/cli/setup.rs) runs an unpinned `git clone` straight into `<root>/<name>` and records nothing; a failed clone can leave a partial folder, and nothing notices a tree that changed after installation. Runtime owns this in the base's installation tool (commit b02b200).

Recommended default: clone into a temporary folder under the root, check `cartridge.json`, rename into place, and write the resolved commit to a lock file next to the profile that `write` produces. `cartridge doctor` compares installed trees with it. Stop and ask if the lock needs a format other cartridges must read.

## Acceptance

- [ ] Installing a repository cartridge records its resolved commit; a second setup from that lock checks out the same commit even after upstream moves.
- [ ] A failed clone or a repository without `cartridge.json` leaves no folder under the root and keeps the previous lock byte-identical.
- [ ] `cartridge doctor` reports a cartridge whose HEAD or tracked tree differs from its lock, names it, and changes nothing.
- [ ] Folder (symlink) installs and existing profiles without a lock keep working.

## Proof and recovery

First reproduce the partial-folder case with a local bare repository fixture (no network) in the existing entry point [tests/unit/src/cli/setup.rs](../../../../../../cartridge.ctg/.cartridge/tests/unit/src/cli/setup.rs). Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`. Not run for this plan. Rollback: remove the lock writer; installed folders stay usable. Source history is never rewritten.

## Dependencies and review

No hard prerequisites: manifest-only declarations already exist (`needs`/`listen` in [document.rs](../../../../../../cartridge.ctg/src/loader/document.rs)). [Review](review.md): inherits 2 rounds; at most five.
