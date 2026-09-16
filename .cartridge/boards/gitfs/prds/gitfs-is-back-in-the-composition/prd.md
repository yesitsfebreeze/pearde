---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
footprint: [".gitmodules", ".cartridge/init.lua"]
commit: "ec30e588487504e763721b5a4b36bf67e68ac9c8"
---

# gitfs is back in the composition

## Outcome

The user wants every installed cartridge enabled and working together
(2026-09-16). The question below is **answered: option (b), retire gitfs.ctg** —
and the user made that call themselves, in superproject commit `9a84e46` ("Drop
the gitfs submodule, absorbed into fs", Stefan Hoevelmanns, 2026-09-16 13:17
+0200, an ancestor of HEAD), which removed the `.gitmodules` section and the
gitlink. `.gitmodules` no longer mentions gitfs and the `gitfs.ctg` directory is
gone.

So the outcome is no longer "gitfs is back": it is that the composition is clean
after the retirement. No cartridge is installed-but-not-enabled, fs is the one
file cartridge and owns `tool.gitfs` and the branch-backed write path, and the
`gitfs` board and policy row keep the owner alias with `repo` pointing at
fs.ctg.

## Acceptance

- [x] `cartridge help` reports no cartridge as "installed and not enabled" (it
      reported "1 installed and not enabled", gitfs, before the retirement).
- [x] fs is the single provider of `tool.gitfs` and `tool.ship`; no second
      provider of either key exists in the composition, so the host's
      duplicate-key refusal (`cartridge.ctg/src/host/plan.rs:244`) cannot fire.
- [x] The host starts cleanly and fs's write/read path still passes.

## Questions

2026-09-16, coordinator cartridge-c4, from analyst-1 (`.state/loop/gitfs-is-back-in-the-composition/`). Evidence:
- `gitfs.ctg` declares only `tool.gitfs` and `tool.ship`. fs declares both too, since it absorbed gitfs today (fs.ctg 75e76e6). The host refuses a second provider of a key (`cartridge.ctg/src/host/plan.rs:244`), so whichever of the two loads second fails.
- Both use `refs/gitfs/<session>` branches and the `.cartridge/gitfs` store. 10 of gitfs's 15 source files are identical to fs's copies.
- `cartridge help` reports "1 installed and not enabled" (gitfs).

Which outcome do you want?  
**Answered by the user in `9a84e46`: (b).**
- **(b) Retire gitfs.ctg (recommended).** Remove the submodule, so every installed cartridge is enabled and fs stays the one file cartridge with branch-backed commits. Spec drafted: superproject repo, `.gitmodules` + `gitfs.ctg`.
- (a) Re-enable gitfs under new tool keys, store and branch prefix. That duplicates fs.
- (c) Reverse today's absorption, putting the session-branch tools back into gitfs and taking them out of fs.

## Planning note

2026-09-16, coordinator cartridge-1b. The peer session cartridge-7e pointed at
`9a84e46`; I verified it in the repo rather than taking the report on trust —
the commit is authored by the user, is an ancestor of HEAD, drops both the
`.gitmodules` section and the gitlink, and its message states the decision and
its reasons in the user's own words. That is an answer to the question, not a
guess on the user's behalf, so this row leaves `question` with the commit as
evidence.

The retirement work itself is already landed outside the engine, so what is left
for this PRD is proof that the composition is clean — which is what the rewritten
Acceptance asks for. The Outcome and Acceptance were rewritten because the
question's chosen option contradicts the original premise ("gitfs is back");
leaving the old boxes would have made this PRD uncollectable by construction.

## Planning note, second entry

2026-09-16, coordinator cartridge-1b, from analyst-2. `repo` moved from `fs.ctg`
to the superproject and the footprint from `.cartridge/config.lua` to
`.gitmodules` + `.cartridge/init.lua`. The old pair was not merely mis-scoped, it
was unusable: `collect` maps each foot with `path.relative(code, f)`
(`prd.ctg/src/lifecycle.ts:133,142,173`), so a superproject path under
`repo: fs.ctg` resolves to `../.cartridge/config.lua` and escapes the repository
git is pointed at. Every acceptance box is a claim about the composition root —
the installed `*.ctg` set, `.cartridge/init.lua`, `.gitmodules`, the composed
host — and none of that lives inside `fs.ctg`.

The two chosen paths are what would have to change for the outcome to become
false again. A footprint is required (`lifecycle.ts:31`) but need not be dirty:
with nothing changed, `collect` skips the commit (`lifecycle.ts:167`) and the
receipt records HEAD. `.cartridge/config.lua` stays out — its `gitfs`/`ship`
policy rows name tools fs serves, and `fs.store_dir = ".cartridge/gitfs"` is fs's
own key.

**This PRD is verification-only**: all three boxes already hold, because the
user's `9a84e46` did the work. The analyst rejected two invented extras (a bun
test asserting "0 not enabled", and cleaning historical `gitfs.ctg` strings out
of `prd.ctg/.cartridge/reports/record-migration/manifest.json`, which is a
migration record rather than a live reference).

**Collect with no lane.** A superproject lane has empty submodules, so pass 1
would find no cartridges at all. `collect` uses a lane only if the directory
exists (`lifecycle.ts:130`), so the coordinator must simply not claim this from
`specced`.

## Evidence note for the ticked boxes

2026-09-16, coordinator cartridge-1b, from reviewer-2 (round 1, PASS 93).

This PRD is verification-only: the user's `9a84e46` did the work, so there is no
implementation to verify separately. The boxes are ticked on the reviewer's
independent execution in the real repository — all three Verify blocks exit 0
(`19 cartridges enabled, 0 installed and not enabled`; one owner per tool key
with `fs.ctg/cartridge.json` the only manifest; `cartridges active: 19` plus a
live write -> read -> ls on `refs/gitfs/...`) — and `collect` runs the same
blocks again before writing the receipt.

The reviewer went past the analyst's four failure probes to eight, so every
guard is known to fire on its own: a regressed tree, a `.gitmodules`-stanza-only
regression, an `init.lua`-entry-only regression, a stub help printing
`1 installed and not enabled`, a missing `CARTRIDGE_BIN`, a stub ledger with two
owners per key, a stub status reporting `failed`, and an empty tree.

Two corrections to the record from that round. The `repo`/`footprint` retarget
was not merely mis-scoped: `git -C fs.ctg diff --name-only --no-renames -z $H $H
-- ../.cartridge/config.lua` exits **128**, and `assertFootprint` checks that
exit code, so the old pair would have aborted collection before any verification
ran. And `cartridge help` from `/tmp` exits **1**, not 0 as the analyst reported
— immaterial to the plan, but the block must run inside the project either way,
since from outside it reports `0 enabled, 9 installed and not enabled` from the
global-home fallback.
