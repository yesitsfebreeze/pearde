---
atomic: verify-with-a-probe
subject: leaves a runnable check in the tree proving the old name is gone and the call path completes
date: 2026-09-04
runs: 0
tags:
  - atomic
---

## Do

1. Write a small script under the PRD's `probe/` that reproduces the original failure path with the minimum stubbing needed, and assert it now succeeds.
2. Run it.

## Done when

- the probe exits zero and the assertions include a `grep`-style check that the old name is gone, not just that the new call worked

## Fails when
