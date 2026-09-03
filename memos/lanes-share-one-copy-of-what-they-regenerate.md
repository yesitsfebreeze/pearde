---
memo: lanes-share-one-copy-of-what-they-regenerate
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: lanes share one copy of what they regenerate
date: 2026-09-02
---

# lanes-share-one-copy-of-what-they-regenerate — lanes share one copy of what they regenerate

## Decision

A lane's regenerable directories — `resources/board/node_modules`, the
graphify cache, the Obsidian plugin bundles — are one copy per machine under
`<git-common-dir>/pearde-shared/`, symlinked into the checkout and into every
lane. `pearde share` is the command; `lanes.create` runs it on every claim.
A path is linked only when `git status` cannot see the link, judged after the
link is written and undone when it can.

## Why

The board was assumed to be spending disk on worktrees. It was not. Measured
on this repo, 2026-09-02: git tracks 174 files and 2.1 MB, so a worktree costs
2.1 MB; the tree on disk was 273 MB across 15,992 files, and 27 lanes held
143 MB. The difference is not the checkout — it is each lane regenerating its
own graphify cache, fetching its own plugin bundles, installing its own
`node_modules`. Sharing those recovers the duplication and caps a lane at what
git tracks.

## Alternatives considered

**A copy-on-write filesystem — OpenZFS on macOS, or APFS `clonefile` cloning
via `cp -Rc`, `rift`, `cow`** — lost on the mechanism, not on the packaging.
CoW shares a block until one side writes it, and each lane writes its *own*
cache by construction, so the divergence lands exactly where the disk goes.
Measured: an APFS clone of this tree cost 176 MB against 809 MB for a plain
copy — real, and nowhere near free, because 11,766 of these files are under
4 KB and a clone still allocates every inode and directory entry. ZFS adds a
kernel extension, a reboot and reduced security on Apple Silicon to buy the
CoW that APFS already gives for nothing.

**`git clone --shared` / `--reference`** — shares the object store, which is
11 MB here and which worktrees already share. The checkout is untouched.

**A `bindfs` or `unionfs-fuse` overlay** — needs macFUSE (a kext) or FUSE-T,
calls its own macOS support best-effort, and a bind mount is not a writable
overlay, which is what a lane needs. macOS has no OverlayFS.

## Consequences

- A lane costs what git tracks. The store grows once per artefact, not once
  per lane.
- Only ignored paths are shared, and `git status` is the judge — not
  `git check-ignore`, which answers about the path as a directory and cannot
  see that a `node_modules/` pattern stops matching once the path is a
  symlink. This repo's `.gitignore` lost its trailing slash for that reason.
- Nothing a lane *owns* is shared: `pearde/.state/`, the board and the specs
  stay per-lane, as they must.
- It does not fix a cache someone committed. One lane branch carries a tracked
  `.pearde/graphify/cache` of 21.9 MB; `share` refuses it and says so.
- Two lanes may write the shared cache at once. The entries are
  content-addressed or install-once, so they write distinct paths or the same
  bytes. There is no lock, and adding one would be the next decision, not this
  one.
