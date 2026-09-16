---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "analyzing"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: fs
work-kind: leaf
claim: "merge-fs-into-gitfs-verify-and-collect 2026-09-16T06:18:37.485Z"
---

# Merge gitfs into fs

Move gitfs's store, overlay tool, ship, push, secrets, inspection, limits,
provenance and hook binary into the fs crate, declare `tool.gitfs` and
`tool.ship` in the fs manifest, and take gitfs out of the composition.

## Acceptance

- [x] `fs.ctg` builds `libfs` and the `gitfs-hook` binary; the manifest test compares every tool schema, `tool.gitfs` and `tool.ship` included.
- [x] Every gitfs unit suite (store, ship, push, secrets, provenance, snapshot, tool results) runs and passes inside `just test fs`.
- [x] `.cartridge/init.lua`, `config.lua`, the composed justfile and the development routine no longer name gitfs; gitfs board PRDs point `repo:` at fs.ctg.

## Proof and recovery

`just check fs` and `just test fs` from `/Users/feb/dev/cartridge`, 2026-09-15:
pass. Recovery: gitfs.ctg is untouched on disk; re-adding its composition line
and removing the two events from fs restores the split.
