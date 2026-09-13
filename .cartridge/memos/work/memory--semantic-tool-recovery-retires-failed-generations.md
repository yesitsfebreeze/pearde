---
kind: work
level: 10
status: open
estimate: 4h
description: Failed editor or language-server generations cannot poison later queries or leave owned analyzer processes behind
read_when: semantic queries stay unavailable after editor failure or analyzers outlive their owner
---

# semantic-tool-recovery-retires-failed-generations

## Do

A failed or interrupted semantic-service initialization does not leave later
queries waiting on a permanently rejected or pending generation. Recovery waits
for owned teardown, preserves cancellation, and prevents stale callbacks from
invalidating a healthy replacement. Service retirement affects only processes
whose ownership is established, never another session's editor or unsaved work.

The existing harness already has failed-readiness eviction and teardown barriers;
the shared editor should obtain the same lifecycle guarantees without a duplicate
provider framework. [[@prd/work/memory--the-warm-lsp-times-out.md]] completed an investigation, not a
lifecycle repair. [[@prd/work/memory--the-lsp-answer-asks-a-positive-control.md]] already protects empty
answers and must remain intact: unavailable or indexing is not no references.

This work requires evidence of the affected ownership boundary before any repair.
It does not authorize machine-wide process cleanup or weaken semantic fallback.
