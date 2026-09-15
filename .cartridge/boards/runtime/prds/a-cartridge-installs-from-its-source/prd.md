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
review-status: passed
canonical-scope: a-cartridge-installs-from-its-source
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/src/cli/setup.rs
- /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/cli/setup.rs
needs:
- "@root/a-cartridge-declares-what-it-needs"
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

## From the retired work memo

Folded 2026-09-15 from `work/a-cartridge-installs-from-its-source.md` (status open, estimate 2d). The PRD state above is authoritative.

> A cartridge can be fetched from the source its manifest names, pinned in a lockfile and run only after explicit approval

### Outcome

A cartridge that is not in the tree can be brought in from the repository its
manifest names: fetched into a cache, pinned to an exact commit recorded in a
lockfile beside the profile, and referenced by a profile entry like any local
folder. What loads changes only when the pin changes. Nothing fetched executes —
not even its declaration read — until the user has approved that cartridge at
that pin, and an approval is for a pin, not for a repository.

Scope is retrieval, pinning and approval. Publishing, versioning across a
registry and automatic updates are not part of this outcome.

### Check

- [ ] Adding a cartridge from a local `file://` git repository writes a lockfile
      entry with its resolved commit, and a second add is a no-op that reports
      the existing pin.
- [ ] A profile entry pointing at the cache loads the fetched cartridge and
      reaches its service, with its needs resolved by the same index as a local
      folder.
- [ ] New upstream commits change nothing about what loads until the pin is
      updated explicitly; the test pushes to the source repository and asserts
      the running generation is unchanged.
- [ ] An unapproved cartridge in the cache is never executed: no process spawn,
      no Lua evaluation, and the run reports what needs approving.
- [ ] A fetch whose content does not match the pinned commit fails the install
      and leaves the cache unchanged.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. `cartridge.json` already carries `source` as a retrieval
reference (`core/loader.rs:73`), and `sdk::Host::landscape` reports it as the
place an installed artifact came from — but nothing reads it: there is no fetch,
no pin, no cache, no lockfile. Profile paths resolve to folders under the
workspace or beside the executable, so a third-party cartridge today means
copying a folder in by hand. `.zirkle/credentials` shows the profile directory is
already where per-profile state lives, so a lockfile belongs beside `init.lua`.

### Spec

Retrieval is a cartridge, not core. Core's part is only that a profile path may
resolve into the cartridge cache; fetching, pinning and approval live in an
install cartridge, so a host that never installs anything carries none of it and
the security surface stays outside the composition core.

The pin is the contract: `<profile>/cartridges.lock` maps a cartridge name to
its source URL and resolved commit, and the cache stores that commit's tree
under a content-addressed path. Resolution reads the lock, never the network; an
install or an explicit update writes it. This is what makes a dependency tree of
linked repositories reproducible rather than "whatever upstream is today".

Trust is explicit and narrow, decided here rather than left open: approval is
recorded per cartridge and pin, the approval record is the profile's, and an
unapproved entry is inert — the composer treats it as undeclared, so it cannot
be started by demand activation either. No auto-update, no transitive approval:
a cartridge that pulls in others surfaces each of them for approval by name.
