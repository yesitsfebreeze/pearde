---
atomic: prove-the-false-negative-in-a-clean-room
subject: Reproduced the empty-store auto-create in a fresh temp dir, so the mechanism is a fact about the tool and not a story about this repo
date: 2026-09-02
updated: 2026-09-02
runs: 1
---

## Do

1. Make an empty directory outside the repository at run time.
2. Run the failing command there and list what the directory holds afterwards.

3. Remove the directory. It now holds a real store, and a stray one on the
   machine is the next false positive.

## Done when

- The mechanism reproduces with no repository present, or it is shown to be repo-specific.

## Fails when
