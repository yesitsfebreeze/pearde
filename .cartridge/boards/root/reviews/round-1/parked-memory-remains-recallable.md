---
kind: work
level: 10
status: open
estimate: 2d
description: parked durable memory resolves through a bounded cold read without unbounded hydration or wasted seed slots
read_when: completing recall across resident and unloaded memories
---

# parked-memory-remains-recallable

## Do

A durable claim remains recallable after its memory leaves memory. Candidate
selection and resolution agree before top-k truncation across dense, lexical
and reason-derived paths. Cold resolution has explicit I/O, latency and
residency bounds; unavailable cold data is reported without blocking available
results. Recall remains read-only and touches no LLM, and parking does not
churn index membership.

This implements [[which-side-of-the-unload-resolve-seam-moves]] for
[[the-graph-converges]]. Resident filtering alone is not completion because it
would hide parked memory.
