---
title: periodic-leak-summaries-distinguish-a-fixed-leak-from-a-grow
date: 2026-09-03
type: conclusion
tags: [conclusion, leak-detection, memcheck, rust, valgrind]
sources:
  - "[[260903-bbff]]"
  - "[[260903-a311]]"
derived_from: []
---

# periodic-leak-summaries-distinguish-a-fixed-leak-from-a-growing-one

Valgrind needs no Rust-specific setup — memcheck attributes allocations correctly against system malloc without a jemalloc suppression file — but a single end-of-run leak-check report is the wrong tool for a long-running process, because it cannot tell a one-time startup leak from a leak that grows with every keystroke or request. The fix is procedural, not a flag: judge only definitely-lost and indirectly-lost counts (still-reachable blocks at exit are allocator noise), and for growth, capture two leak summaries at different points in the same run by sending a termination signal mid-session, then diff them.

Consequence: gate CI on a one-shot `valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --error-exitcode=1` run, but investigate RSS growth separately by driving the binary interactively and comparing mid-run summaries — a clean CI gate does not rule out a leak that only shows up under load.
