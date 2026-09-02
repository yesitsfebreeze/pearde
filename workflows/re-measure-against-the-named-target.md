---
atomic: re-measure-against-the-named-target
subject: Pinned `KERN_DIR` to the store the artefact names; 21 of 21 ids resolved where 21 had been reported dead
date: 2026-09-02
runs: 1
---

## Do

1. Pin the tool to the target the artefact names, by env var or flag — `KERN_DIR=<store>` here.
2. Re-run the measurement over every item, not the sample the report used.

## Done when

- Every item has a resolved or unresolved verdict against the named target, counted.

## Fails when
