---
state: open
origin: requested
priority: 35
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: repo-checks-cartridge-registered
needs:
  - repo-checks-cartridge/the-checks-cartridge-exists-and-runs-a-repository-s-declared-checks
footprint:
  - ".gitmodules"
  - ".cartridge/init.lua"
  - ".cartridge/justfile"
  - ".cartridge/memos/routine/cartridge-development.md"
---

# The checks cartridge is registered in the composition

## Outcome

`checks.ctg` becomes a member of this composition rather than a directory beside
it: the host loads it, `just check checks` and `just test checks` resolve, and
`just audit checks` has a profile entry to find. Four superproject files carry
that registration, and none of them is under `checks.ctg`, which is why this is
its own child with its own footprint instead of a widened one on the sibling.

The four, each read from the file that carries it:

1. `.cartridge/justfile`, recipe `_fan`, hard-codes the owner list per gate in
   its `check)` and `test)` lines. `just check checks` and `just test checks` do
   not resolve until `checks` is in both.
2. `.cartridge/memos/routine/cartridge-development.md` is the command
   implementation behind those gates. Its `_cargo` recipe ends in
   `*) echo "Unknown owner: $module" >&2; exit 2;;`, so an owner not named in the
   case arm is rejected by name, and its `all` loop carries the same list again.
3. `.cartridge/init.lua` is the one list of cartridges the host loads. A missing
   profile entry is a hard `just audit` encapsulation failure, and without it the
   host never loads the cartridge, so `cartridge call checks` has nothing to
   answer.
4. `.gitmodules` registers the submodule. Most `*.ctg` directories here are submodules, and a collection against the superproject records
   `checks.ctg` as a gitlink only once it is registered.

## Acceptance

- [ ] `just test checks` and `just check checks` resolve from the superproject root and run the cartridge's own tests, rather than failing with an unknown owner.
- [ ] `just audit checks` finds a composition-profile entry whose path resolves to the cartridge's manifest, and reports no hard finding for it.
- [ ] `just isolation` reports nothing for `checks`.
- [ ] The host loads the cartridge from the profile, and a call to it is answered.
- [ ] `checks.ctg` is recorded as a submodule gitlink, in the same shape every sibling uses, rather than as ordinary committed files or an untracked directory.

## Questions

**Where does the cartridge's own remote live?** The sibling cartridges are
submodules of remotes under `yesitsfebreeze/<name>.ctg`. `checks.ctg` has no
remote today, and `git submodule add` needs a URL that exists. This PRD will not
invent one.

- Recommended: the user creates `yesitsfebreeze/checks.ctg` empty, and this child
  registers it exactly as its siblings are registered.
- Alternative: register the submodule against a local path or a file URL now and
  retarget the remote later, which keeps the composition working but leaves
  `.gitmodules` naming something no other checkout can clone.
- Alternative: keep `checks.ctg` as ordinary tracked files in the superproject,
  as `web.ctg` is. That contradicts "a cartridge is its own repository with its
  own remote", so it needs the user's own words before anyone takes it.

## Proof and recovery

The footprint's four paths are shared with every other port in the
`@root/port-the-flow-engine-and-companion-tool-cartridges` tree, so those
registrations are serial by construction: one port registers at a time. At the
time of writing `.cartridge/justfile` also carries an uncommitted edit belonging
to another session, and `collect` commits every dirty path inside the footprint,
so this child must not be collected until
`git -C /Users/feb/dev/cartridge status --porcelain -- .cartridge/justfile` is
empty or the edit is confirmed as ours.

Recovery: each of the four edits is additive and reversible on its own, and
removing the profile entry returns the composition to not knowing the cartridge
exists.
