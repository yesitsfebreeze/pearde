---
atomic: ask-the-tool-what-it-actually-read
subject: kern status` named the store it resolved and every other store on the machine — the reported reading was against a store that was not the subject
date: 2026-09-02
runs: 1
tags:
  - atomic
---

## Do

1. Run the tool's own status or config subcommand — `kern status` here — and read which path it resolved.
2. Compare that path against the one the artefact was written against.

## Done when

- The resolved path is known, and it is stated whether it is the subject's own store.

## Fails when
