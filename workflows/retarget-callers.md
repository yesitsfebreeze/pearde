---
atomic: retarget-callers
subject: swaps every stale call site to the symbol's current home in one pass — `grep` first to catch siblings the report didn't name
date: 2026-09-04
runs: 0
tags:
  - atomic
---

## Do

1. Edit every call site found in step 1 to the symbol's current qualified name, matching the surviving callers that were already updated (if any) rather than inventing a new call shape.

## Done when

- `grep` for the old name across the footprint returns nothing

## Fails when
