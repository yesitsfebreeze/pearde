---
title: deleting-a-chezmoi-source-is-half-a-retirement-the-other-hal
date: 2026-09-02
type: conclusion
tags: [chezmoi, conclusion, deploy, dotfiles, retirement]
sources:
  - "[[260902-f203]]"
  - "[[260902-7c3a]]"
derived_from: []
---

# Deleting a chezmoi source is half a retirement; the other half is a .chezmoiremove line

Removing a file from the chezmoi source tree does not remove it from any
machine it was already deployed to — `chezmoi apply` only writes and
updates, it does not reap orphans ([[260902-f203]]). A deletion is
therefore two edits, not one: drop the source file, and add the target
path to `home/.chezmoiremove`.

Doing it by hand (`rm ~/.config/…`) fixes the machine in front of you and
nothing else. The `.chezmoiremove` line is the part the repo carries, so
the retirement holds on the next machine that still has the old deploy.

The removal is state-dependent and can fail loudly ([[260902-7c3a]]): a
target that differs from what chezmoi last wrote, or whose entry chezmoi
has forgotten, is prompted for, and a headless apply then exits 1 rather
than skipping. Where the retirement is intended, `--force`; where a script
must be sure, assert the target's absence afterwards instead of trusting
the apply's exit code.

The check that closes this is at the DEPLOYED path, never the source path:
`test ! -e ~/.config/<name>`, plus `grep -qxF '<target>' home/.chezmoiremove`.
