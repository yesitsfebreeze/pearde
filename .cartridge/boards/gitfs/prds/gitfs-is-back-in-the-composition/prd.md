---
state: "question"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/fs.ctg"
footprint: ["/Users/feb/dev/cartridge/.cartridge/config.lua"]
---

# gitfs is back in the composition

## Outcome

The user wants every installed cartridge enabled and working together
(2026-09-16). gitfs, taken out in f231611 when fs took the session-branch
settings, is enabled again alongside fs without the two fighting over the
same store or branch.

## Acceptance

- [ ] `cartridge help` lists gitfs as enabled; no cartridge reports "installed and not enabled".
- [ ] gitfs and fs do not share a store directory or session branch; the split of ownership is written in both help pages.
- [ ] The host starts cleanly with both (`cartridge call gitfs` status answers; fs write/read still pass).

## Questions

2026-09-16, coordinator cartridge-c4, from analyst-1 (`.state/loop/gitfs-is-back-in-the-composition/`). Evidence:
- `gitfs.ctg` declares only `tool.gitfs` and `tool.ship`. fs declares both too, since it absorbed gitfs today (fs.ctg 75e76e6). The host refuses a second provider of a key (`cartridge.ctg/src/host/plan.rs:244`), so whichever of the two loads second fails.
- Both use `refs/gitfs/<session>` branches and the `.cartridge/gitfs` store. 10 of gitfs's 15 source files are identical to fs's copies.
- `cartridge help` reports "1 installed and not enabled" (gitfs).

Which outcome do you want?
- **(b) Retire gitfs.ctg (recommended).** Remove the submodule, so every installed cartridge is enabled and fs stays the one file cartridge with branch-backed commits. Spec drafted: superproject repo, `.gitmodules` + `gitfs.ctg`.
- (a) Re-enable gitfs under new tool keys, store and branch prefix. That duplicates fs.
- (c) Reverse today's absorption, putting the session-branch tools back into gitfs and taking them out of fs.
